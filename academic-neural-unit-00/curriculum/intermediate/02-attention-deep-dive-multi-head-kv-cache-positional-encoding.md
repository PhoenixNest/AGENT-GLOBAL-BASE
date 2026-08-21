# Attention Deep Dive: Multi-Head Attention, KV-Cache & Positional Encoding

**注意力机制深入解析：多头注意力、KV 缓存与位置编码**

| Field   | English                                                          | 中文                                    |
| ------- | ---------------------------------------------------------------- | --------------------------------------- |
| Level   | Intermediate                                                     | 中级                                    |
| Cluster | Foundations                                                      | 基础                                    |
| Author  | Dr. Yuna Baek, Research Scientist — AI / Neural Networks, ANU-00 | ANU-00 AI/神经网络研究员 Yuna Baek 博士 |

---

This chapter assumes everything taught in `introductory/01-neural-networks-and-deep-learning-foundations.md`
(neurons, layers, gradients, backpropagation) and everything taught in
`introductory/02-the-transformer-architecture-and-attention.md` (queries/keys/values, scaled
dot-product attention, the single-head worked example, the Transformer block, and sinusoidal
positional encoding). Nothing beyond those two modules and secondary-school algebra is assumed. As
with every module in this curriculum, terms not already defined in the two prerequisite modules are
defined here at first use.

本章以 `introductory/01-neural-networks-and-deep-learning-foundations.md`（神经元、层、梯度、反向传播）以及 `introductory/02-the-transformer-architecture-and-attention.md`（查询/键/值、缩放点积注意力、单头手算示例、Transformer 块与正弦位置编码）中讲授的全部内容为前提。除这两个模块与中学代数知识外，本章不假设读者具备任何其他背景。与本课程体系中的每个模块一致，凡是这两个前置模块中尚未定义的术语，均在本章首次出现时给出定义。

---

## 1. Recap and Scope

**回顾与范围**

`introductory/02` §5–§6 defined single-head scaled dot-product attention,
$\text{Attention}(Q,K,V) = \text{softmax}(QK^T/\sqrt{d_k})V$, and worked a two-token numeric example by hand.
`introductory/02` §7 introduced multi-head attention only at a conceptual level — several attention
patterns computed in parallel — without the underlying mathematics. This chapter completes that
picture in four parts: the full mathematics of multi-head attention (§2–§3), the computational cost
of attention and why generation needs a cache (§4–§7), the modern positional encoding schemes that
have largely replaced the original sinusoidal scheme (§9), and a brief note on hardware-aware
attention implementations (§10).

`introductory/02` 第 5 至第 6 节定义了单头缩放点积注意力 $\text{Attention}(Q,K,V) = \text{softmax}(QK^T/\sqrt{d_k})V$，并手算了一个双 token 的数值示例。`introductory/02` 第 7 节仅在概念层面介绍了多头注意力——即并行计算若干种注意力模式——而未涉及其底层数学。本章将从四个方面完整补全这一图景：多头注意力的完整数学推导（第 2 至第 3 节）、注意力的计算成本以及生成过程为何需要缓存（第 4 至第 7 节）、在很大程度上已取代原始正弦方案的现代位置编码方案（第 9 节），以及关于硬件感知型注意力实现的简要说明（第 10 节）。

---

## 2. Multi-Head Attention in Full Mathematical Detail

**多头注意力的完整数学细节**

Recall from `introductory/02` §4 that a single attention head projects a token's $d_{\text{model}}$
-dimensional embedding into query, key, and value vectors via learned matrices $W_Q$, $W_K$, $W_V$.
Multi-head attention runs $h$ such projections in parallel, called **heads**, each
with its own independently learned weight matrices $W_Q^i$, $W_K^i$, $W_V^i$ for head $i$, each
projecting into a smaller dimension $d_k = d_{\text{model}} / h$ (so that the total parameter count across
all heads roughly matches a single full-dimensional head). Vaswani et al. (2017) define the
complete operation as:

回顾 `introductory/02` 第 4 节，单个注意力头通过可学习矩阵 $W_Q$、$W_K$、$W_V$，将一个 token 的 $d_{\text{model}}$ 维嵌入投影为查询、键、值向量。多头注意力并行运行 $h$ 个这样的投影，称为**头**，每个头 $i$ 都拥有各自独立学习的权重矩阵 $W_Q^i$、$W_K^i$、$W_V^i$，并投影到更小的维度 $d_k = d_{\text{model}} / h$（这样一来，所有头的参数总量与单个全维度头大致相当）。Vaswani 等人（2017）给出了完整操作的定义：

$$
head_i = \text{Attention}(QW_Q^i, KW_K^i, VW_V^i)
$$

$$
\text{MultiHead}(Q,K,V) = \text{Concat}(head_1, \ldots, head_h)\, W_O
$$

Each head produces its own output vector of dimension $d_k$ for every position, using exactly the
scaled dot-product attention formula from `introductory/02` §5 applied within that head's own
projected subspace. The outputs of all $h$ heads are concatenated back into a single vector of
dimension $h \times d_k = d_{\text{model}}$, and one final learned matrix $W_O$ mixes information across heads
to produce the sub-layer's output. Vaswani et al. used $h = 8$ heads with $d_{\text{model}} = 512$, giving
$d_k = 64$ (Vaswani et al., 2017); modern large models use larger $d_{\text{model}}$ and more heads, but the
same structure.

每个头都会为每个位置独立生成一个维度为 $d_k$ 的输出向量，其计算方式正是将 `introductory/02` 第 5 节的缩放点积注意力公式，应用于该头自身投影出的子空间之内。所有 $h$ 个头的输出会被重新拼接为一个维度为 $h \times d_k = d_{\text{model}}$ 的单一向量，随后再由一个最终的可学习矩阵 $W_O$ 对各头之间的信息进行混合，从而得到该子层的输出。Vaswani 等人使用了 $h = 8$ 个头、$d_{\text{model}} = 512$，因此 $d_k = 64$（Vaswani et al., 2017）；现代大型模型使用更大的 $d_{\text{model}}$ 与更多的头，但结构完全相同。

Why split into multiple smaller heads rather than use one large head? Vaswani et al. observe that
a single attention head, by averaging over all relevant positions via one softmax distribution per
query, inhibits the model from simultaneously attending to different _kinds_ of relationships (for
example, syntactic agreement and long-range coreference) with different weighting patterns; multiple
heads, each free to learn a different pattern of relevance, avoid this averaging-out effect
(Vaswani et al., 2017).

为何要拆分为多个较小的头，而不是使用单个较大的头？Vaswani 等人指出，单个注意力头由于对每个查询只用一个 softmax 分布对所有相关位置取平均，会阻碍模型同时以不同的加权模式关注不同*类型*的关系（例如句法一致性与远距离共指关系）；而多个头各自可以自由学习不同的相关性模式，从而避免了这种平均化效应（Vaswani et al., 2017）。

---

## 3. Worked Example: Multi-Head Attention Computation

**手算示例：多头注意力计算**

Extend the two-token example from `introductory/02` §6. Let $d_{\text{model}} = 2$ and $h = 2$ heads, so
each head has $d_k = 1$. Suppose, purely for illustration, that head 1's projection matrices select
only the first embedding dimension and head 2's select only the second — that is, head 1 works with
scalars $q_{1i} = k_{1i} = v_{1i} = x_i[0]$ (each token's first coordinate) and head 2 works with
$q_{2i} = k_{2i} = v_{2i} = x_i[1]$ (each token's second coordinate), using the same $x_1 = [1,0]$,
$x_2 = [0,1]$ as before.

在 `introductory/02` 第 6 节双 token 示例的基础上进行扩展。设 $d_{\text{model}} = 2$，$h = 2$ 个头，因此每个头的 $d_k = 1$。仅为便于说明，假设头 1 的投影矩阵只选取嵌入的第一维，头 2 的投影矩阵只选取第二维——也就是说，头 1 使用标量 $q_{1i} = k_{1i} = v_{1i} = x_i[0]$（每个 token 的第一个坐标），头 2 使用标量 $q_{2i} = k_{2i} = v_{2i} = x_i[1]$（每个 token 的第二个坐标），仍沿用之前的 $x_1 = [1,0]$、$x_2 = [0,1]$。

For head 1, the query/key values are $[1, 0]$ for tokens 1 and 2 respectively. Scores
$q_{1i} \cdot k_{1j}$ for token 1 as query: against token 1, $1 \times 1 = 1$; against token 2, $1 \times 0 = 0$. With
$d_k = 1$, scaling divides by $\sqrt{1} = 1$ (no change). Softmax of $[1, 0]$ gives approximately
$[0.731, 0.269]$. Token 1's head-1 output is $0.731 \times 1 + 0.269 \times 0 = 0.731$. For head 2, by the
symmetric construction, token 1's query value is $0$, so its scores against both keys ($0$ and
$1$) are $0$ and $0$ — softmax of $[0, 0]$ is $[0.5, 0.5]$ — giving a head-2 output for token 1 of
$0.5 \times 0 + 0.5 \times 1 = 0.5$.

对于头 1，token 1 与 token 2 的查询/键值分别为 $[1, 0]$。以 token 1 为查询时的得分 $q_{1i} \cdot k_{1j}$：与 token 1 的得分为 $1 \times 1 = 1$，与 token 2 的得分为 $1 \times 0 = 0$。由于 $d_k = 1$，缩放时除以 $\sqrt{1} = 1$（数值不变）。对 $[1, 0]$ 做 softmax，得到约 $[0.731, 0.269]$。token 1 在头 1 上的输出为 $0.731 \times 1 + 0.269 \times 0 = 0.731$。对于头 2，由构造的对称性可知，token 1 的查询值为 $0$，因此其与两个键（分别为 $0$ 和 $1$）的得分均为 $0$ 和 $0$——对 $[0, 0]$ 做 softmax 得到 $[0.5, 0.5]$——因此 token 1 在头 2 上的输出为 $0.5 \times 0 + 0.5 \times 1 = 0.5$.

Concatenating the two heads' scalar outputs for token 1 gives $[0.731, 0.5]$, a two-dimensional
vector, which is then passed through the output matrix $W_O$ to produce the sub-layer's final
output for that position. Two observations generalize beyond this toy example: each head computed
a genuinely different attention pattern (head 1 favored token 1's own value strongly; head 2 was
indifferent between the two tokens), and concatenation simply stacks each head's independent
findings side by side before $W_O$ combines them — exactly the mechanism described abstractly in
§2.

将两个头针对 token 1 的标量输出拼接起来，得到二维向量 $[0.731, 0.5]$，随后经过输出矩阵 $W_O$ 处理，得到该位置在该子层的最终输出。这一玩具示例可以推广出两点一般性结论：两个头确实计算出了截然不同的注意力模式（头 1 明显偏向 token 1 自身的值；头 2 则对两个 token 一视同仁），而拼接操作只是在 $W_O$ 将各头的独立发现组合起来之前，把它们简单地并排堆叠在一起——这正是第 2 节所抽象描述的机制。

---

## 4. Computational Complexity of Self-Attention

**自注意力的计算复杂度**

For a sequence of length $n$, computing $QK^T$ requires comparing every position against every
other position, producing an $n \times n$ matrix of scores — the amount of computation and memory this
requires grows proportional to $n^2$ (quadratically with sequence length), in contrast to the
recurrent networks discussed in `introductory/02` §2, whose per-step cost does not grow with total
sequence length in the same way, though their total sequential computation still scales linearly
with $n$ due to the step-by-step dependency. This $O(n^2)$ cost is a well-known and actively
researched limitation of standard attention: doubling the sequence length quadruples the attention
computation and memory required for the score matrix, which becomes the dominant cost for very
long sequences. §10 briefly notes an implementation-level (not asymptotic) mitigation;
`advanced/05-advanced-context-engineering-long-context-and-budgeting.md` covers architectural
mitigations for long-context processing in depth.

对于长度为 $n$ 的序列，计算 $QK^T$ 需要将每个位置与其他每个位置逐一比较，从而生成一个 $n \times n$ 的得分矩阵——所需的计算量与内存量都随 $n^2$（即随序列长度呈平方级）增长，这与 `introductory/02` 第 2 节所讨论的循环网络形成对比：循环网络单步的计算成本并不以同样方式随总序列长度增长，尽管由于其逐步依赖的特性，其总的顺序计算量仍随 $n$ 线性增长。这种 $O(n^2)$ 的开销是标准注意力机制一个广为人知且被积极研究的局限：序列长度翻倍会使得分矩阵所需的注意力计算量与内存量增长为原来的四倍，这在处理极长序列时会成为主要的成本瓶颈。第 10 节将简要提及一种实现层面（而非渐近复杂度层面）的缓解方法；`advanced/05-advanced-context-engineering-long-context-and-budgeting.md` 将深入讲解应对长上下文处理的架构层面缓解方案。

---

## 5. Causal Masking for Autoregressive Generation

**用于自回归生成的因果掩码**

`introductory/02` §10 introduced **causal masking** as the mechanism that prevents a
decoder-only model from attending to future positions. Mechanically, before the softmax step in
$\text{Attention}(Q,K,V) = \text{softmax}(QK^T/\sqrt{d_k})V$, every score $(QK^T)_{ij}$ for which position $j$ comes after
position $i$ is set to $-\infty$ (negative infinity) rather than left as its computed dot product;
after softmax, $e^{-\infty} = 0$, so those positions receive exactly zero attention weight, without
needing to change the shape of any computation. This is why the term is **masking**: a fixed
triangular pattern of allowed/disallowed positions is applied uniformly at every layer, ensuring
that the representation computed for position $i$ never has access to information from positions
after $i$, which is exactly the constraint required for training a model to predict the next token
from only what precedes it, and for that same trained model to generate text one token at a time
at inference.

`introductory/02` 第 10 节引入了**因果掩码**，作为阻止仅解码器模型关注未来位置的机制。从机制上讲，在 $\text{Attention}(Q,K,V) = \text{softmax}(QK^T/\sqrt{d_k})V$ 的 softmax 步骤之前，对于位置 $j$ 位于位置 $i$ 之后的每一个得分 $(QK^T)_{ij}$，都会被设置为 $-\infty$（负无穷），而非保留其原本计算出的点积值；经过 softmax 之后，$e^{-\infty} = 0$，因此这些位置将获得恰好为零的注意力权重，且无需改变任何计算的形状。这正是“掩码”一词的含义：在每一层都统一施加一个固定的三角形允许/禁止位置模式，从而确保为位置 $i$ 计算出的表示永远无法获取位置 $i$ 之后的信息——这恰恰是训练模型仅依据前文预测下一个 token 所需的约束条件，也是同一个训练好的模型在推理时逐个 token 生成文本所需的约束条件。

---

## 6. Autoregressive Decoding and the Redundancy Problem

**自回归解码与冗余问题**

Generating text with a decoder-only Transformer is **autoregressive**: the model
produces one token, appends it to the input sequence, and runs the whole sequence through the
model again to produce the next token, repeating until generation stops. A naive implementation of
this loop recomputes every token's key and value vectors, at every layer, on every single
generation step — even though, due to causal masking (§5), the key and value vectors for all
_previous_ tokens are exactly the same as they were on the previous step, since nothing about an
earlier token's representation depends on tokens that come after it. This recomputation is pure
waste: for a sequence of length $n$, naive autoregressive generation performs roughly $O(n^2)$
total key/value computation across all steps of generating $n$ tokens, when the _necessary_ new
computation at each step is only for the one new token. §7 covers the standard fix.

使用仅解码器 Transformer 生成文本的过程是**自回归的**：模型每生成一个 token，就将其追加到输入序列中，再将整个序列重新输入模型以生成下一个 token，如此循环直至生成结束。这一循环的朴素实现，会在每一层、每一个生成步骤，重新计算每个 token 的键向量和值向量——尽管由于因果掩码（第 5 节）的存在，所有*先前* token 的键向量和值向量与上一步完全相同，因为较早 token 的表示本就不依赖于其之后出现的 token。这种重复计算纯属浪费：对于长度为 $n$ 的序列，朴素的自回归生成在生成 $n$ 个 token 的整个过程中，累计执行的键/值计算量大约为 $O(n^2)$，而每一步*真正必要*的新计算，其实只针对那一个新的 token。第 7 节将介绍这一问题的标准解决方案。

---

## 7. The KV Cache: Mechanism and Memory Cost

**KV 缓存：机制与内存开销**

The **KV cache** (key-value cache) eliminates the redundancy identified in §6 by storing
each layer's key and value vectors for every token already generated, and, on each new generation
step, computing key/value/query vectors for _only_ the newest token, then computing that new
token's attention using its own fresh query against the _cached_ keys and values of all prior
tokens plus its own newly computed key and value (which are then appended to the cache for the
next step). This reduces the per-step cost of generating one new token from re-processing the
whole sequence to processing exactly one token, at the price of memory used to store the growing
cache. Pope et al.'s analysis of efficient Transformer inference at scale treats KV-cache memory
management as one of the central bottlenecks of serving large autoregressive models (Pope et al.,
2022).

**KV 缓存**通过为每一个已生成的 token 存储其在每一层的键向量和值向量，从而消除第 6 节所指出的冗余计算：在每一个新的生成步骤中，*仅*为最新的那个 token 计算键/值/查询向量，随后用这个新 token 自己全新的查询，去关注所有先前 token *缓存*中的键与值，再加上它自己新计算出的键与值（随后二者会被追加进缓存，供下一步使用）。这样一来，生成一个新 token 每一步的成本，就从重新处理整个序列降低到只处理恰好一个 token，代价是需要用内存来存储不断增长的缓存。Pope 等人对大规模高效 Transformer 推理的分析，将 KV 缓存的内存管理视为服务大型自回归模型时的核心瓶颈之一（Pope et al., 2022）。

The memory cost of the KV cache can be computed directly: for a model with $L$ layers, $H$ key
-value heads per layer, head dimension $d_h$, storing both keys and values (hence a factor of 2)
in a numeric precision using $p$ bytes per number, the cache for one sequence of length $n$ requires
approximately $2 \times L \times H \times d_h \times n \times p$ bytes. As a concrete illustration: a model with $L = 32$
layers, $H = 32$ heads, $d_h = 128$, sequence length $n = 2048$, stored in 16-bit floating point
($p = 2$ bytes), requires $2 \times 32 \times 32 \times 128 \times 2048 \times 2 \approx 1.07 \times 10^9$ bytes — roughly 1 gigabyte of
memory _per sequence being generated_, before accounting for the model's own weights. This
memory cost, multiplied across every sequence a server is generating simultaneously, is what
motivates the head-reduction techniques in §8.

KV 缓存的内存开销可以直接计算：对于一个拥有 $L$ 层、每层 $H$ 个键值头、头维度为 $d_h$ 的模型，同时存储键和值（因此有系数 2），并以每个数值占用 $p$ 字节的数值精度存储，那么长度为 $n$ 的一个序列所需的缓存大约为 $2 \times L \times H \times d_h \times n \times p$ 字节。举一个具体的例子：一个拥有 $L = 32$ 层、$H = 32$ 个头、$d_h = 128$、序列长度 $n = 2048$ 的模型，以 16 位浮点数存储（$p = 2$ 字节），所需内存约为 $2 \times 32 \times 32 \times 128 \times 2048 \times 2 \approx 1.07 \times 10^9$ 字节——即在尚未计入模型自身权重的情况下，*每个正在生成的序列*大约需要 1 GB 内存。将这一内存开销乘以服务器同时生成的所有序列数量，正是第 8 节所述“头数缩减”技术的动机所在。

---

## 8. Reducing KV Cache Cost: Multi-Query, Grouped-Query, and Multi-Head Latent Attention

**降低 KV 缓存开销：多查询注意力、分组查询注意力与多头潜在注意力**

Three named techniques reduce the memory computed in §7 by changing how many distinct key/value
head projections a model uses, without discarding multi-head attention's query-side diversity.
**Multi-query attention (MQA)** (多查询注意力), introduced by Shazeer (2019), keeps a separate
query projection per head (preserving each head's distinct "what am I looking for" behavior) but
shares a _single_ key and single value projection across all heads — reducing the $H$ term in
§7's formula for keys/values to $1$, directly shrinking the cache by a factor close to the number
of heads, at the cost of some quality degradation the paper reports as minor (Shazeer, 2019).
**Grouped-query attention (GQA)** (分组查询注意力), introduced by Ainslie et al. (2023), is an
intermediate design: query heads are divided into $G$ groups, and all query heads within a group
share one key/value projection, so $H$ in the cache formula becomes $G$ instead of the full head
count or $1$ — the paper shows this recovers most of the quality of full multi-head attention while
retaining most of MQA's inference speed and memory savings, and additionally describes a recipe
for converting ("uptraining") an existing multi-head checkpoint into a GQA model cheaply (Ainslie
et al., 2023). As a numeric illustration continuing §7's example: reducing $H$ from 32 heads to
$G = 8$ groups shrinks the roughly 1.07 GB cache to roughly $1.07\text{ GB} \times (8/32) \approx 268$ MB per
sequence.

有三种被命名的技术，通过改变模型所使用的独立键/值头投影数量来降低第 7 节所计算的内存开销，同时不牺牲多头注意力在查询侧所具有的多样性。**多查询注意力（MQA）** 由 Shazeer（2019）提出，为每个头保留独立的查询投影（从而保留每个头各自“我在寻找什么”的独特行为），但在所有头之间共享*单一*的键投影和单一的值投影——将第 7 节公式中键/值所对应的 $H$ 项缩减为 $1$，从而将缓存直接缩小至接近头数分之一的规模，代价是论文中报告的轻微质量下降（Shazeer, 2019）。**分组查询注意力（GQA）** 由 Ainslie 等人（2023）提出，是一种折中设计：将查询头划分为 $G$ 个组，同一组内的所有查询头共享一个键/值投影，因此缓存公式中的 $H$ 变为 $G$，而非完整的头数或 $1$——论文表明，这种方法在保留 MQA 大部分推理速度与内存节省优势的同时，能够恢复完整多头注意力的大部分质量，此外还给出了一套将现有的多头检查点低成本“升级训练”（uptrain）为 GQA 模型的方法（Ainslie et al., 2023）。作为延续第 7 节示例的数值说明：将 $H$ 从 32 个头缩减为 $G = 8$ 个组，会使约 1.07 GB 的缓存缩小为每个序列约 $1.07\text{ GB} \times (8/32) \approx 268$ MB。

A different, more recent approach, **multi-head latent attention (MLA)** (多头潜在注意力),
introduced as part of DeepSeek-V2, compresses the keys and values into a lower-dimensional latent
vector via a learned down-projection before caching, and reconstructs full-size keys and values
via a learned up-projection when needed, rather than reducing the _number_ of distinct head
projections as MQA/GQA do; DeepSeek-V2's authors report this achieves better quality than standard
multi-head attention while requiring substantially less cached memory per token (DeepSeek-AI,
2024). All three techniques address the same §7 memory bottleneck from different angles: MQA and
GQA reduce the count of independent key/value projections; MLA reduces the dimensionality of what
gets cached per projection.

另一种更为新近的方法——**多头潜在注意力（MLA）**，作为 DeepSeek-V2 的组成部分被提出，它并不像 MQA/GQA 那样减少独立头投影的*数量*，而是在缓存之前，通过一个可学习的降维投影，将键与值压缩为一个低维的潜在向量，并在需要时通过一个可学习的升维投影重建出完整尺寸的键与值；DeepSeek-V2 的作者报告称，这种方法在实现优于标准多头注意力质量的同时，大幅降低了每个 token 所需缓存的内存量（DeepSeek-AI, 2024）。这三种技术都从不同角度应对第 7 节所述的同一内存瓶颈：MQA 与 GQA 减少的是独立键/值投影的*数量*，而 MLA 降低的则是每个投影所缓存内容的*维度*。

---

## 9. Positional Encoding Revisited: Sinusoidal, Rotary Embeddings, and ALiBi

**再谈位置编码：正弦编码、旋转位置编码与 ALiBi**

`introductory/02` §8 described the original **sinusoidal positional encoding** from Vaswani et al.
(2017): a fixed vector, generated from sine/cosine functions, added to each token's embedding
before it enters the attention layers. This approach has a practical limitation: because the
encoding is added directly to the input, a model's ability to generalize to sequence lengths
longer than it saw during training is limited. Two influential alternatives modify the attention
computation itself rather than the input embedding.

`introductory/02` 第 8 节介绍了 Vaswani 等人（2017）提出的最初**正弦位置编码**：一个由正弦/余弦函数生成的固定向量，在进入注意力层之前被加到每个 token 的嵌入上。这种方法存在一个实际局限：由于编码是直接叠加在输入上的，模型泛化到比训练时所见更长序列的能力因而受到限制。有两种颇具影响力的替代方案，它们改变的不是输入嵌入本身，而是注意力计算过程。

**Rotary position embedding (RoPE)** (旋转位置编码), introduced by Su et al. in the RoFormer
paper, encodes a token's absolute position by rotating its query and key vectors — treating pairs
of dimensions as 2-D coordinates and applying a rotation whose angle depends on the token's
position — before the dot product in the attention score is computed. A key property Su et al.
prove is that the dot product between a rotated query at position $m$ and a rotated key at
position $n$ depends only on their _relative_ distance $m - n$, not on their absolute positions,
which the paper shows helps the resulting attention scores decay naturally as relative distance
grows, and gives the mechanism flexibility to be applied to sequences of varying lengths (Su et
al., 2021). RoPE has been adopted by many widely used open large language model families as their
default positional scheme since publication.

**旋转位置编码（RoPE）** 由 Su 等人在 RoFormer 论文中提出，它通过在计算注意力得分中的点积之前，对查询向量和键向量进行旋转——将成对的维度视为二维坐标，并施加一个角度取决于 token 位置的旋转——来编码 token 的绝对位置。Su 等人证明了一个关键性质：位置 $m$ 处经过旋转的查询与位置 $n$ 处经过旋转的键之间的点积，只取决于二者的*相对*距离 $m - n$，而与它们的绝对位置无关；论文表明，这一性质有助于所得的注意力得分随相对距离增大而自然衰减，并使该机制具备灵活适用于不同长度序列的能力（Su et al., 2021）。自发表以来，RoPE 已被众多广泛使用的开放大型语言模型系列采纳为其默认的位置编码方案。

**Attention with Linear Biases (ALiBi)** (线性偏置注意力), introduced by Press, Smith, and Lewis,
takes an even simpler approach: rather than modifying query/key vectors at all, it adds a fixed,
position-dependent penalty directly to the raw attention scores _before_ the softmax step — a
penalty proportional to the distance between the query and key positions, scaled by a
head-specific constant — so that attention to distant tokens is discouraged in proportion to
distance, with no learned parameters involved in the positional mechanism itself. Press et al.
report that a model trained with ALiBi on shorter sequences extrapolates to substantially longer
sequences at inference time with no loss in quality relative to a sinusoidally-encoded model
trained directly on the longer length, while training faster and using less memory (Press, Smith,
and Lewis, 2021).

**线性偏置注意力（ALiBi）** 由 Press、Smith 和 Lewis 提出，采用了更为简洁的方法：它完全不对查询/键向量做任何修改，而是在 softmax 步骤*之前*，直接在原始注意力得分上加上一个固定的、依赖于位置的惩罚项——该惩罚项与查询和键位置之间的距离成正比，并按特定于每个头的常数进行缩放——从而使模型对距离较远 token 的关注程度随距离成比例地受到抑制，且该位置机制本身不涉及任何可学习参数。Press 等人报告称，一个在较短序列上使用 ALiBi 训练的模型，在推理时能够外推到显著更长的序列，且相较于直接在该更长长度上训练的正弦编码模型，质量没有损失，同时训练速度更快、内存占用更低（Press, Smith, and Lewis, 2021）。

---

## 10. IO-Awareness and FlashAttention

**IO 感知与 FlashAttention**

Separate from the $O(n^2)$ asymptotic cost discussed in §4, standard attention implementations on
GPU hardware are also slowed by how much data must move between a GPU's small, fast on-chip memory
and its larger, slower main memory (high-bandwidth memory, HBM) — computing and storing the full
$n \times n$ score matrix requires repeatedly reading from and writing to the slower memory.
**FlashAttention** (FlashAttention 算法), introduced by Dao et al., is an exact (not approximate)
attention algorithm that restructures the computation into blocks small enough to fit in fast
on-chip memory, computing attention output incrementally without ever materializing the full
$n \times n$ score matrix in slow memory — an optimization the authors term **IO-awareness**, since it
targets memory-movement cost rather than raw arithmetic operation count. Dao et al. report
substantial wall-clock training speedups from this restructuring alone, with mathematically
identical output to standard attention (Dao et al., 2022). This is an implementation-level
optimization — it does not change what attention computes or its $O(n^2)$ asymptotic complexity,
only how efficiently that computation is executed on real hardware.

与第 4 节所讨论的 $O(n^2)$ 渐近复杂度不同，标准注意力在 GPU 硬件上的实现速度还会受到另一个因素的拖累：GPU 中容量小、速度快的片上内存与容量大、速度慢的主内存（高带宽内存，HBM）之间需要搬运多少数据——计算并存储完整的 $n \times n$ 得分矩阵，需要反复对速度较慢的内存进行读写。**FlashAttention**（FlashAttention 算法）由 Dao 等人提出，是一种精确（而非近似）的注意力算法，它将计算重新组织为足够小的分块，使其能够装入速度较快的片上内存，从而在不必将完整的 $n \times n$ 得分矩阵在慢速内存中具体化的前提下，增量式地计算出注意力输出——作者将这一优化称为 **IO 感知**（IO-awareness），因为它针对的是内存搬运成本，而非原始的算术运算次数。Dao 等人报告称，仅凭这一重构就能带来显著的训练实际耗时加速，且输出在数学上与标准注意力完全一致（Dao et al., 2022）。这是一种实现层面的优化——它并不改变注意力所计算的内容，也不改变其 $O(n^2)$ 的渐近复杂度，只是改变了该计算在真实硬件上的执行效率。

---

## 11. Summary and What Comes Next

**小结与后续内容**

This chapter completed the mathematical picture of attention that `introductory/02` introduced at
a conceptual level: the full multi-head computation with its per-head projections and output
mixing (§2–§3); the $O(n^2)$ computational cost of self-attention and the distinct redundancy
problem that autoregressive generation introduces on top of it (§4, §6); the KV cache as the
standard fix for that redundancy, together with its own memory cost and the three named techniques
— MQA, GQA, and MLA — developed to reduce it (§7–§8); the modern positional encoding schemes, RoPE
and ALiBi, that address limitations of the original sinusoidal scheme (§9); and a brief note on
IO-aware, hardware-efficient exact attention implementations (§10).

本章完整补全了 `introductory/02` 仅在概念层面所介绍的注意力机制的数学图景：包含各头独立投影与输出混合的完整多头计算（第 2 至第 3 节）；自注意力的 $O(n^2)$ 计算成本，以及自回归生成在此基础上额外引入的独特冗余问题（第 4、第 6 节）；作为该冗余问题标准解决方案的 KV 缓存，及其自身的内存开销，以及为降低这一开销而发展出的三种被命名的技术——MQA、GQA 与 MLA（第 7 至第 8 节）；应对原始正弦方案局限性的现代位置编码方案 RoPE 与 ALiBi（第 9 节）；以及关于 IO 感知型、硬件高效的精确注意力实现的简要说明（第 10 节）。

`advanced/02-mixture-of-experts-and-modern-architecture-variants.md` builds directly on the
Transformer block structure from `introductory/02` §9 and the attention mechanics from this
chapter, turning to the _other_ major sub-layer of a Transformer block — the feed-forward network
— and how modern architectures replace its single dense computation with a sparse mixture of
specialized sub-networks.

`advanced/02-mixture-of-experts-and-modern-architecture-variants.md` 将直接建立在 `introductory/02` 第 9 节所述的 Transformer 块结构以及本章所讲的注意力机制之上，转而聚焦 Transformer 块*另一个*主要的子层——前馈网络，并探讨现代架构如何用一组稀疏的专门化子网络来取代其单一的稠密计算。

---

## References

**参考文献**

### External Sources

- [Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention Is All You Need.](https://arxiv.org/abs/1706.03762)
- [Shazeer, N. (2019). Fast Transformer Decoding: One Write-Head is All You Need.](https://arxiv.org/abs/1911.02150)
- [Ainslie, J., Lee-Thorp, J., de Jong, M., Zemlyanskiy, Y., Lebrón, F., & Sanghai, S. (2023). GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints.](https://arxiv.org/abs/2305.13245)
- [DeepSeek-AI (2024). DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model.](https://arxiv.org/abs/2405.04434)
- [Su, J., Lu, Y., Pan, S., Murtadha, A., Wen, B., & Liu, Y. (2021). RoFormer: Enhanced Transformer with Rotary Position Embedding.](https://arxiv.org/abs/2104.09864)
- [Press, O., Smith, N. A., & Lewis, M. (2021). Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation.](https://arxiv.org/abs/2108.12409)
- [Dao, T., Fu, D. Y., Ermon, S., Rudra, A., & Ré, C. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness.](https://arxiv.org/abs/2205.14135)
- [Pope, R., Douglas, S., Chowdhery, A., et al. (2022). Efficiently Scaling Transformer Inference.](https://arxiv.org/abs/2211.05102)

### Internal Cross-References

- [`introductory/01-neural-networks-and-deep-learning-foundations.md`](../introductory/01-neural-networks-and-deep-learning-foundations.md) — required prerequisite: neurons, layers, gradients, backpropagation.
- [`introductory/02-the-transformer-architecture-and-attention.md`](../introductory/02-the-transformer-architecture-and-attention.md) — required prerequisite: queries/keys/values, scaled dot-product attention, the Transformer block, sinusoidal positional encoding, causal masking.
- [`advanced/02-mixture-of-experts-and-modern-architecture-variants.md`](../advanced/02-mixture-of-experts-and-modern-architecture-variants.md) — builds on this chapter's Transformer block and attention mechanics to cover the feed-forward sub-layer's sparse variants.
- [`advanced/05-advanced-context-engineering-long-context-and-budgeting.md`](../advanced/05-advanced-context-engineering-long-context-and-budgeting.md) — covers architectural mitigations for the $O(n^2)$ attention cost noted in §4 in depth.
