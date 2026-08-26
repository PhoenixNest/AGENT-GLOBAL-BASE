# Mixture-of-Experts & Modern Architecture Variants

**专家混合与现代架构变体**

| Field   | English                                                          | 中文                                    |
| ------- | ---------------------------------------------------------------- | --------------------------------------- |
| Level   | Advanced                                                         | 高级                                    |
| Cluster | Foundations                                                      | 基础                                    |
| Author  | Dr. Yuna Baek, Research Scientist — AI / Neural Networks, ANU-00 | ANU-00 AI/神经网络研究员 Yuna Baek 博士 |

---

This chapter assumes everything taught in [`introductory/01`](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md), [`introductory/02`](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md), [`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md),
and [`advanced/01`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md) — neurons, layers, backpropagation ([`introductory/01`](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md)); the Transformer block, its
feed-forward sub-layer, and residual/normalization structure ([`introductory/02` §9](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md#9-the-transformer-block-attention-feed-forward-residuals-and-normalization)); multi-head
attention, the KV cache, and the family of techniques (MQA, GQA, MLA) that trade exact computation
for efficiency ([`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md)); and the observation that predictable scaling relationships link
model size, data, and compute to performance ([`advanced/01`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md)). Nothing beyond those four modules and
secondary-school algebra is assumed. As with every module in this curriculum, any term not already
defined in a prerequisite module is defined here at first use.

本章以 [`introductory/01`](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md)、[`introductory/02`](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md)、[`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) 与 [`advanced/01`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md) 已经讲授的全部内容为前提——神经元、层、反向传播（[`introductory/01`](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md)）；Transformer 块及其前馈子层、残差与归一化结构（[`introductory/02` 第 9 节](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md#9-the-transformer-block-attention-feed-forward-residuals-and-normalization)）；多头注意力、KV 缓存，以及一系列以牺牲精确计算换取效率的技术（MQA、GQA、MLA，见 [`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md)）；以及“模型规模、数据量与算力同性能之间存在可预测的规模关系”这一观察（[`advanced/01`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md)）。除这四个模块与中学代数知识外，本章不假设读者具备任何其他背景。与本课程体系中的每个模块一致，凡是尚未在某个前置模块中定义过的术语，均会在本章首次出现时给出定义。

---

## 1. Recap and Scope

**回顾与范围**

[`introductory/02` §9](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md#9-the-transformer-block-attention-feed-forward-residuals-and-normalization) described the Transformer block as combining a multi-head attention sub-layer
with a position-wise **feed-forward network** (FFN) — an ordinary multi-layer perceptron, applied
independently and identically to every position in the sequence.

[`introductory/02` 第 9 节](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md#9-the-transformer-block-attention-feed-forward-residuals-and-normalization)介绍了 Transformer 块的组成方式：一个多头注意力子层，加上一个逐位置的**前馈网络**（FFN）——一个普通的多层感知机，被独立且完全相同地应用于序列中的每一个位置。

[`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) then spent its entire length deepening the _attention_ half of that block: full
multi-head mathematics, the KV cache, and techniques (MQA, GQA, MLA) that reduce attention's
computational and memory cost without discarding its quality. This chapter turns to the _other_ half
of the block — the feed-forward sub-layer — and to a set of further structural choices
(normalization, gating) that, together with attention variants, define what "a modern large language
model" actually looks like in 2026, as distinct from the original 2017 Transformer.

[`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) 随后用整整一章的篇幅深化了该模块中“注意力”这一半的内容：完整的多头数学推导、KV 缓存，以及在不牺牲质量的前提下降低注意力计算与内存开销的技术（MQA、GQA、MLA）。本章转而聚焦该模块*另一半*——前馈子层，以及一系列进一步的结构性设计选择（归一化、门控），这些选择连同注意力变体一起，共同定义了 2026 年“现代大型语言模型”与 2017 年最初的 Transformer 相比究竟有何不同。

This chapter covers four families of change, in order: sparse **Mixture-of-Experts** (MoE, 专家混合)
architectures, which replace the FFN's single dense computation with a large bank of specialized
sub-networks of which only a few are used per token ([§2](#2-the-feed-forward-sub-layer-as-a-scaling-bottleneck)–[§8](#8-moe-in-a-widely-used-open-model-mixtral-of-experts)); gated feed-forward variants such as
SwiGLU, which change the FFN's internal structure without changing whether it is dense or sparse
([§9](#9-gated-feed-forward-variants-glu-and-swiglu)); RMSNorm, a simplified normalization scheme now more common than the original layer
normalization ([§10](#10-rmsnorm-a-simplified-normalization-for-modern-architectures)); and, briefly, an architecture family that departs from attention entirely
([§11](#11-beyond-attention-entirely-state-space-models)).

本章按顺序涵盖四类变化：稀疏**专家混合**（Mixture-of-Experts，MoE）架构，它用一个庞大的专门化子网络库取代了前馈网络原本单一的稠密计算，每个 token 只会用到其中少数几个子网络（第 2 至[第 8 节](#8-moe-in-a-widely-used-open-model-mixtral-of-experts)）；诸如 SwiGLU 之类的门控前馈变体，它们改变的是前馈网络的内部结构，而不改变其稠密或稀疏的性质（[第 9 节](#9-gated-feed-forward-variants-glu-and-swiglu)）；RMSNorm——一种如今比最初的层归一化更为常见的简化归一化方案（[第 10 节](#10-rmsnorm-a-simplified-normalization-for-modern-architectures)）；以及简要介绍一个完全脱离注意力机制的架构家族（[第 11 节](#11-beyond-attention-entirely-state-space-models)）。

---

## 2. The Feed-Forward Sub-Layer as a Scaling Bottleneck

**前馈子层：规模扩展的瓶颈**

[`advanced/01`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md) established that scaling a model's parameter count, training data, and compute
together tends to improve performance in a predictable way.

[`advanced/01`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md) 指出，将模型的参数量、训练数据量与算力共同扩大，往往能以一种可预测的方式提升性能。

But scaling every parameter of a dense model — one where every parameter is used to process every
token, exactly as the feed-forward network from [`introductory/02` §9](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md#9-the-transformer-block-attention-feed-forward-residuals-and-normalization) does — means training and
inference compute grow proportionally with parameter count: a model with twice as many FFN
parameters costs roughly twice as much compute per token, at both training and inference time.

但如果扩大的是一个稠密模型的每一个参数——即像 [`introductory/02` 第 9 节](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md#9-the-transformer-block-attention-feed-forward-residuals-and-normalization)所述前馈网络那样，每个参数都被用来处理每一个 token——那么训练与推理所需的算力就会随参数量成比例增长：一个前馈网络参数量翻倍的模型，处理每个 token 所需的算力大致也会翻倍。

Shazeer et al.'s 2017 paper on **conditional computation** (条件计算) — computation in which only a
data-dependent subset of a network's parameters is active for any given input — proposed breaking
this proportionality: activate only a small fraction of a very large parameter pool per token, so
that total capacity (and hence potential quality) can grow far faster than the compute actually
spent processing any one token (Shazeer et al., 2017).

Shazeer 等人 2017 年提出的**条件计算**（conditional computation）——即对任意给定输入，网络参数中只有依赖于数据的一个子集被激活的计算方式——提出了打破这种正比关系的思路：每个 token 只激活一个庞大参数库中的一小部分，这样一来，总容量（进而潜在的模型质量）就能以远快于处理单个 token 实际所耗算力的速度增长（Shazeer et al., 2017）。

Shazeer et al. applied conditional computation specifically by replacing a single feed-forward
network with many smaller feed-forward networks, called **experts**, and a small **gating network**
that decides, per token, which few experts to route that token through. The result is called a
**sparsely-gated mixture-of-experts layer** — "sparsely-gated" because the gating network activates
only a small subset of experts per token, not because the experts themselves are sparse in any other
sense. [§3](#3-sparse-mixture-of-experts-the-core-idea)–[§4](#4-the-gating-network-softmax-and-noisy-top-k-gating) build up exactly how the gating network makes this decision.

Shazeer 等人将条件计算具体应用为：用许多规模较小的前馈网络——称为**专家**——取代单一的前馈网络，并配以一个小型的**门控网络**，针对每个 token 决定应将其路由到哪几个专家。这一结构被称为**稀疏门控专家混合层**（sparsely-gated mixture-of-experts layer）——之所以叫“稀疏门控”，是因为门控网络针对每个 token 只激活一小部分专家，而不是因为专家本身在其他意义上是稀疏的。第 3 至[第 4 节](#4-the-gating-network-softmax-and-noisy-top-k-gating)将具体展开门控网络究竟是如何做出这一决策的。

---

## 3. Sparse Mixture-of-Experts: The Core Idea

**稀疏专家混合：核心思想**

A **Mixture-of-Experts (MoE) layer** replaces the single FFN inside a Transformer block with $N$
parallel expert networks, $E_1, E_2, \ldots, E_N$, each structured like an ordinary feed-forward
network (same shape as [`introductory/02` §9](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md#9-the-transformer-block-attention-feed-forward-residuals-and-normalization)'s FFN, with its own independent parameters), plus a
gating network $G$ that, for each token's embedding $x$, outputs a sparse weight vector over the $N$
experts — nonzero for only a handful of experts, zero for the rest. The layer's output is the
weighted sum of the _selected_ experts' outputs:

**专家混合层**用 $N$ 个并行的专家网络 $E_1, E_2, \ldots, E_N$ 取代 Transformer 块内部单一的前馈网络，每个专家的结构都与普通的前馈网络相同（形态与 [`introductory/02` 第 9 节](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md#9-the-transformer-block-attention-feed-forward-residuals-and-normalization)的 FFN 一致，但拥有各自独立的参数），另外配有一个门控网络 $G$，它针对每个 token 的嵌入向量 $x$，输出一个关于这 $N$ 个专家的稀疏权重向量——只有少数几个专家对应非零权重，其余均为零。该层的输出是*被选中*专家输出的加权和：

$$y = \sum_i G(x)_i \cdot E_i(x)$$

(summed only over experts $i$ where $G(x)_i \neq 0$)

Because $G(x)_i = 0$ for most experts, $E_i(x)$ never needs to be computed for those experts at all
— this is what makes the layer computationally cheap despite having enormous total parameter count.

由于对绝大多数专家而言 $G(x)_i = 0$，这些专家的 $E_i(x)$ 根本无需被计算——这正是该层尽管总参数量极为庞大、计算成本却依然低廉的原因所在。

If, for example, only 2 out of 64 experts are active per token, the compute cost per token is close
to that of a single small FFN, while the model's total parameter count — and hence its capacity to
store distinct, specialized knowledge across experts — is close to that of 64 such FFNs. This
distinction between **total parameters** and **active parameters** (per-token compute cost) is the
single most important accounting concept in this chapter, and recurs in every section below.

举例来说，如果每个 token 只激活 64 个专家中的 2 个，那么每个 token 的计算成本就接近于单个小型 FFN 的成本，而模型的总参数量——因而其在各专家间存储不同专门化知识的容量——则接近于 64 个这样的 FFN。 **总参数量**与**激活参数量**（即每 token 的计算成本）之间的这一区分，是本章最重要的核算概念，并将在下文的每一节中反复出现。

---

## 4. The Gating Network: Softmax and Noisy Top-K Gating

**门控网络：Softmax 门控与噪声 Top-K 门控**

The simplest gating network is a plain **softmax gate**: $G_\sigma(x) = \mathrm{Softmax}(x \cdot
W_g)$, where $W_g$ is a learned weight matrix projecting the token embedding down to $N$ scores, one
per expert, and softmax (already defined in [`introductory/01` §4](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#4-activation-functions-why-nonlinearity-matters)) turns them into a probability
distribution. This alone is _not_ sparse — every expert gets some nonzero weight — so Shazeer et al.
add two further mechanisms.

最简单的门控网络是一个纯粹的 **softmax 门控**：$G_\sigma(x) = \mathrm{Softmax}(x \cdot W_g)$，其中 $W_g$ 是一个可学习的权重矩阵，将 token 嵌入投影为 $N$ 个得分，每个专家对应一个，而 softmax（已在 [`introductory/01` 第 4 节](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#4-activation-functions-why-nonlinearity-matters)中定义）将这些得分转化为一个概率分布。但这本身*并非*稀疏的——每个专家都会获得某个非零权重——因此 Shazeer 等人又添加了两个机制。

First, **KeepTopK** zeroes out (formally, sets to $-\infty$ before the softmax, exactly the masking
trick [`intermediate/02` §5](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md#5-causal-masking-for-autoregressive-generation) used for causal attention) every score except the $k$ largest, enforcing
genuine sparsity. Second, during training, tunable Gaussian noise is added to the raw scores before
top-$k$ selection, to encourage exploration across experts and help balance how much training signal
each expert receives — together, the full mechanism is:

第一，**KeepTopK** 会将除最大的 $k$ 个得分之外的所有得分清零（形式上是在 softmax 之前将其设为 $-\infty$，与 [`intermediate/02` 第 5 节](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md#5-causal-masking-for-autoregressive-generation)中用于因果注意力的掩码技巧完全相同），从而强制实现真正的稀疏性。第二，在训练过程中，会在原始得分上加入可调节的高斯噪声，再进行 top-$k$ 选择，以鼓励对不同专家的探索，并帮助平衡各专家所获得的训练信号——综合起来，完整的机制如下：

$$G(x) = \mathrm{Softmax}(\mathrm{KeepTopK}(H(x), k))$$

$$H(x)_i = (x \cdot W_g)_i + \mathrm{StandardNormal}() \cdot \mathrm{Softplus}((x \cdot W_{noise})_i)$$

$$\mathrm{KeepTopK}(v, k)_i = \begin{cases} v_i & \text{if } v_i \text{ is among the top } k \text{ values of } v \\ -\infty & \text{otherwise} \end{cases}$$

As a worked example, take $N = 4$ experts, $k = 2$, and suppose the noisy scores for one token come
out to $H(x) = [2.1, -1.0, 0.4, 1.8]$. The top 2 values are $2.1$ (expert 1) and $1.8$ (expert 4),
so $\mathrm{KeepTopK}(H(x), 2) = [2.1, -\infty, -\infty, 1.8]$. Applying softmax: $e^{2.1} \approx
8.166$, $e^{1.8} \approx 6.050$, $e^{-\infty} = 0$ for the other two, giving a sum of $\approx
14.216$ and final gate weights $G(x) \approx [0.574, 0, 0, 0.426]$. Only experts 1 and 4 are
activated for this token, weighted roughly 57%/43% between them — exactly the sparse routing
described in [§3](#3-sparse-mixture-of-experts-the-core-idea).

举一个手算示例：设 $N = 4$ 个专家，$k = 2$，假设某个 token 带噪声得分为 $H(x) = [2.1, -1.0, 0.4, 1.8]$。其中最大的两个值是 $2.1$（专家 1）与 $1.8$（专家 4），因此 $\mathrm{KeepTopK}(H(x), 2) = [2.1, -\infty, -\infty, 1.8]$。对其应用 softmax：$e^{2.1} \approx 8.166$，$e^{1.8} \approx 6.050$，另外两项因 $e^{-\infty} = 0$，三者之和约为 $\approx 14.216$，最终门控权重为 $G(x) \approx [0.574, 0, 0, 0.426]$。对这个 token 而言，只有专家 1 和专家 4 被激活，二者的权重大致为 57% 与 43%——这正是[第 3 节](#3-sparse-mixture-of-experts-the-core-idea)所描述的稀疏路由。

---

## 5. Scaling MoE to Production: GShard's Top-2 Routing and Expert Capacity

**将 MoE 扩展到生产环境：GShard 的 Top-2 路由与专家容量**

Lepikhin et al.'s 2020 GShard system scaled sparse MoE to a multilingual machine-translation
Transformer with over 600 billion parameters, trained across 2,048 TPU accelerators, and in doing so
introduced two practical mechanisms beyond the gating formula in [§4](#4-the-gating-network-softmax-and-noisy-top-k-gating) (Lepikhin et al., 2020). First,
GShard uses **top-2 routing** ($k = 2$) rather than the larger $k$ values used in some earlier
conditional-computation work, deliberately choosing a point between using many experts per token
(better quality, more compute) and using only one (cheapest, but — as [§6](#6-switch-transformer-simplifying-to-top-1-routing-and-the-load-balancing-loss) discusses — introducing its
own difficulties).

Lepikhin 等人 2020 年提出的 GShard 系统，将稀疏 MoE 扩展到了一个参数量超过 6000 亿、在 2,048 个 TPU 加速器上训练的多语言机器翻译 Transformer 模型，并在此过程中，在[第 4 节](#4-the-gating-network-softmax-and-noisy-top-k-gating)所述门控公式之外，引入了两个具有实践意义的机制（Lepikhin et al., 2020）。第一，GShard 采用**top-2 路由**（$k = 2$），而非此前一些条件计算工作所使用的更大 $k$ 值，刻意在“每个 token 使用较多专家（质量更好但算力开销更大）”与“每个 token 只使用一个专家（成本最低，但正如[第 6 节](#6-switch-transformer-simplifying-to-top-1-routing-and-the-load-balancing-loss)将讨论的那样，会带来其自身的困难）”之间选取了一个折中点。

Second, because a batch's tokens are not evenly distributed across experts by chance, GShard
enforces an **expert capacity** — a hard limit on how many tokens any single expert may process in a
given batch — and any token routed to an already-full expert's slot **overflows**: it is not
processed by that expert at all, only by whichever of its selected experts still has capacity.
GShard additionally routes to its second-choice expert only with a probability proportional to that
expert's gate weight, on the reasoning that a low-weight secondary expert contributes little to the
final weighted output in the first place (Lepikhin et al., 2020).

第二，由于一个批次中的 token 并不会碰巧均匀地分布到各个专家，GShard 强制施加了**专家容量**——即在给定批次中，任何单个专家所能处理的 token 数量上限——任何被路由到已满专家名额的 token 都会**溢出**：它根本不会被该专家处理，只能由其所选专家中仍有余量的那一个来处理。此外，GShard 只以与门控权重成比例的概率将 token 路由给其次优选择的专家，其考量在于：一个权重较低的次要专家，在最终的加权输出中本来贡献就很小（Lepikhin et al., 2020）。

---

## 6. Switch Transformer: Simplifying to Top-1 Routing and the Load-Balancing Loss

**Switch Transformer：简化为 Top-1 路由与负载均衡损失**

Fedus, Zoph, and Shazeer's 2021 Switch Transformer pushed routing simplicity further still, arguing
that even top-2 routing is more complexity than necessary, and using $k = 1$ — each token is routed
to exactly one expert.

Fedus、Zoph 与 Shazeer 于 2021 年提出的 Switch Transformer 将路由简化得更进一步：他们认为即便是 top-2 路由也超出了必要的复杂度，因而采用 $k = 1$——每个 token 恰好被路由到一个专家。

The paper reports that this **switch routing** preserves model quality relative to top-2 routing
while reducing routing computation and communication overhead, and it scaled the approach to models
with over a trillion total parameters (Fedus, Zoph, and Shazeer, 2021). A $k = 1$ design, however,
sharpens a problem already present in [§5](#5-scaling-moe-to-production-gshards-top-2-routing-and-expert-capacity): if the gating network's raw preferences are left
unchecked, training tends to collapse onto routing most tokens to a small handful of "popular"
experts, starving the rest of training signal and wasting the capacity that was the entire point of
using MoE in the first place.

论文报告称，这种 **switch 路由**在相较于 top-2 路由保持模型质量的同时，降低了路由计算与通信开销，并将该方法扩展到了总参数量超过一万亿的模型（Fedus, Zoph, and Shazeer, 2021）。然而，$k = 1$ 的设计，会使[第 5 节](#5-scaling-moe-to-production-gshards-top-2-routing-and-expert-capacity)中已经存在的一个问题变得更加尖锐：如果不对门控网络的原始偏好加以约束，训练往往会坍缩为把大多数 token 都路由给少数几个“热门”专家，使其余专家得不到足够的训练信号，浪费了使用 MoE 本来想要获得的容量优势。

To counter this, Fedus, Zoph, and Shazeer add a **differentiable load-balancing loss** to the
training objective, computed per batch. For a batch of $T$ tokens routed among $N$ experts, let
$f_i$ be the _fraction of tokens whose top choice was expert i_ (a hard, non-differentiable count),
and $P_i$ be the _average router probability mass_ assigned to expert $i$ across the batch (a soft,
differentiable quantity). The auxiliary loss is:

为应对这一问题，Fedus、Zoph 与 Shazeer 在训练目标中加入了一个**可微分的负载均衡损失**，按批次计算。对于一个在 $N$ 个专家间路由的、包含 $T$ 个 token 的批次，设 $f_i$ 为*首选专家为 i 的 token 所占的比例*（一个硬性的、不可微的计数值），$P_i$ 为该批次中分配给专家 $i$ 的*平均路由概率质量*（一个软性的、可微的量）。辅助损失为：

$$\text{loss} = \alpha \cdot N \cdot \sum_i f_i \cdot P_i$$

$$f_i = \frac{1}{T} \sum_{x \in \text{batch}} \mathbb{1}\{\arg\max G(x) = i\}$$

$$P_i = \frac{1}{T} \sum_{x \in \text{batch}} G(x)_i$$

Multiplying by $N$ is a normalization choice: under perfectly uniform routing, $\sum_i f_i P_i =
1/N$ exactly, so the $N \cdot$ factor keeps the loss's magnitude roughly constant regardless of how
many experts the model uses, and any _deviation_ from uniform routing pushes $\sum_i f_i P_i$ above
$1/N$, increasing the loss. Fedus, Zoph, and Shazeer report using $\alpha = 10^{-2}$ throughout
their experiments, after sweeping values from $10^{-1}$ to $10^{-5}$, finding it "sufficiently large
to ensure load balancing while small enough to not... overwhelm the primary cross-entropy objective"
(Fedus, Zoph, and Shazeer, 2021).

乘以 $N$ 是一种归一化选择：在完全均匀的路由下，恰好有 $\sum_i f_i P_i = 1/N$，因此 $N \cdot$ 这一系数使得该损失的量级大致不随专家数量而变化；而任何*偏离*均匀路由的情况，都会使 $\sum_i f_i P_i$ 超过 $1/N$，从而增大损失。 Fedus、Zoph 与 Shazeer 报告称，在从 $10^{-1}$ 到 $10^{-5}$ 扫描了多个取值之后，他们在全部实验中都使用 $\alpha = 10^{-2}$，认为这个取值“足够大，能够确保负载均衡，同时又足够小，不至于……压过主要的交叉熵目标”（Fedus, Zoph, and Shazeer, 2021）。

As a worked numeric example with $N = 4$ experts: if routing is perfectly uniform, $f = P = [0.25,
0.25, 0.25, 0.25]$, giving $\sum f_i P_i = 4 \times 0.0625 = 0.25 = 1/N$, and $\text{loss} = 0.01
\times 4 \times 0.25 = 0.01$.

作为一个 $N = 4$ 个专家的手算示例：若路由完全均匀，$f = P = [0.25, 0.25, 0.25, 0.25]$，则 $\sum f_i P_i = 4 \times 0.0625 = 0.25 = 1/N$，$\text{loss} = 0.01 \times 4 \times 0.25 = 0.01$。

If instead routing is imbalanced — say $f = [0.5, 0.25, 0.125, 0.125]$ and, correspondingly, $P =
[0.4, 0.3, 0.2, 0.1]$ — then $\sum f_i P_i = (0.5)(0.4) + (0.25)(0.3) + (0.125)(0.2) + (0.125)(0.1)
= 0.2 + 0.075 + 0.025 + 0.0125 = 0.3125$, giving $\text{loss} = 0.01 \times 4 \times 0.3125 =
0.0125$ — larger than the uniform case, exactly the penalty needed to push the gating network back
toward balance during training.

若路由不均衡——例如 $f = [0.5, 0.25, 0.125, 0.125]$，相应地 $P = [0.4, 0.3, 0.2, 0.1]$——则 $\sum f_i P_i = (0.5)(0.4) + (0.25)(0.3) + (0.125)(0.2) + (0.125)(0.1) = 0.2 + 0.075 + 0.025 + 0.0125 = 0.3125$，$\text{loss} = 0.01 \times 4 \times 0.3125 = 0.0125$——比均匀情形下更大，这正是在训练过程中把门控网络推回均衡状态所需要的那种惩罚。

---

## 7. Fine-Grained and Shared Experts: DeepSeekMoE

**细粒度专家与共享专家：DeepSeekMoE**

Dai et al.'s 2024 DeepSeekMoE architecture identifies two remaining inefficiencies in the
GShard/Switch style of MoE described in [§5](#5-scaling-moe-to-production-gshards-top-2-routing-and-expert-capacity)–[§6](#6-switch-transformer-simplifying-to-top-1-routing-and-the-load-balancing-loss), and addresses each with a distinct structural change
(Dai et al., 2024). First, **fine-grained expert segmentation**: rather than using a modest number
of relatively large experts, DeepSeekMoE splits each expert's feed-forward hidden dimension into
several smaller experts (holding total parameter count and compute roughly fixed), and
correspondingly activates more experts per token from this larger, finer-grained pool.

Dai 等人 2024 年提出的 DeepSeekMoE 架构，指出了第 5 至[第 6 节](#6-switch-transformer-simplifying-to-top-1-routing-and-the-load-balancing-loss)所述 GShard/Switch 式 MoE 中仍然存在的两个低效之处，并分别用一项结构性改动加以解决（Dai et al., 2024）。第一是**细粒度专家分割**：DeepSeekMoE 不再使用数量适中、规模相对较大的专家，而是将每个专家前馈网络的隐藏维度切分为若干个更小的专家（在总参数量与计算量大致保持不变的前提下），并相应地从这个更大、更细粒度的专家池中为每个 token 激活更多专家。

The authors report this gives the gating network many more possible _combinations_ of experts to
select from per token, allowing more precise, less redundant specialization than a small number of
coarse experts permits.

作者报告称，这样一来，门控网络在为每个 token 进行选择时，可供组合的专家*组合方式*大大增多，从而实现了比少量粗粒度专家所能达到的更精细、冗余更少的专门化。

Second, **shared expert isolation**: a small number of experts are designated as **shared experts**
and are activated for _every_ token unconditionally, alongside whichever routed experts the gating
network selects. The intuition, per Dai et al., is that some knowledge is useful regardless of token
content (basic grammar, common facts), and forcing every routed expert to redundantly re-learn that
shared knowledge wastes capacity that fine-grained specialization could otherwise use for genuinely
distinct knowledge; isolating it into always-on shared experts frees the routed experts to
specialize more cleanly (Dai et al., 2024).

第二是**共享专家隔离**：指定少量专家作为**共享专家**，无条件地对*每一个* token 激活，与门控网络所选择的路由专家并行工作。 Dai 等人的直觉在于：有些知识无论 token 内容如何都是有用的（基本语法、常识性事实），如果强迫每个被路由到的专家都冗余地重新学习这些共享知识，就会浪费本可用于真正差异化知识的专门化容量；将这部分知识隔离到始终激活的共享专家中，能让路由专家实现更纯粹的专门化（Dai et al., 2024）。

---

## 8. MoE in a Widely Used Open Model: Mixtral of Experts

**广泛使用的开放模型中的 MoE：Mixtral of Experts**

Jiang et al.'s 2024 Mixtral 8x7B is a concrete, publicly documented illustration of the total
-versus-active parameter distinction from [§3](#3-sparse-mixture-of-experts-the-core-idea) at production scale. Each Transformer block's
feed-forward sub-layer is replaced by 8 experts, and a top-2 router (in the sense of [§5](#5-scaling-moe-to-production-gshards-top-2-routing-and-expert-capacity)'s GShard
routing, $k = 2$) selects 2 of the 8 experts to process each token, combining their outputs weighted
by the router's softmax output over just those 2 experts.

Jiang 等人 2024 年提出的 Mixtral 8x7B，是[第 3 节](#3-sparse-mixture-of-experts-the-core-idea)“总参数量与激活参数量”这一区分在生产级规模上的一个具体、有公开文档记录的例证。模型中每个 Transformer 块的前馈子层都被替换为 8 个专家，一个 top-2 路由器（即[第 5 节](#5-scaling-moe-to-production-gshards-top-2-routing-and-expert-capacity) GShard 意义上的路由，$k = 2$）为每个 token 选出 8 个专家中的 2 个进行处理，并按路由器仅在这 2 个专家上计算出的 softmax 输出对其结果加权组合。

Because the model's attention sub-layers and other non-expert parameters are shared across all
tokens regardless of routing, the model's total parameter count — every expert's parameters plus the
shared components — is reported by the authors as approximately 47 billion, while the number of
parameters actually used to process any single token is approximately 13 billion, since only 2 of
the 8 experts' parameters (plus the shared components) are active per token (Jiang et al., 2024).

由于模型的注意力子层以及其他非专家参数在所有 token 之间是共享的、不受路由影响，作者报告称，模型的总参数量——每个专家的参数加上共享组件——约为 470 亿，而实际用于处理任意一个 token 的参数量约为 130 亿，因为每个 token 只会激活 8 个专家中的 2 个（加上共享组件）（Jiang et al., 2024）。

The authors report that Mixtral 8x7B matches or exceeds the quality of substantially larger dense
models on most benchmarks evaluated, while its ~13B active-parameter compute cost per token is far
closer to a 13B dense model's inference cost than to a 47B dense model's — the central practical
payoff of the sparse-MoE design introduced in [§2](#2-the-feed-forward-sub-layer-as-a-scaling-bottleneck) (Jiang et al., 2024).

作者报告称，Mixtral 8x7B 在大多数评测基准上，其质量能够匹配甚至超过规模大得多的稠密模型，而其每个 token 约 130 亿激活参数所对应的计算成本，远比接近一个 470 亿参数稠密模型的推理成本，更接近一个 130 亿参数稠密模型的推理成本——这正是[第 2 节](#2-the-feed-forward-sub-layer-as-a-scaling-bottleneck)所引入的稀疏 MoE 设计所带来的核心实际收益（Jiang et al., 2024）。

---

## 9. Gated Feed-Forward Variants: GLU and SwiGLU

**门控前馈变体：GLU 与 SwiGLU**

Independent of whether an FFN is dense (as in [`introductory/02`](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md)) or one expert within a sparse MoE ([§3](#3-sparse-mixture-of-experts-the-core-idea)–[§8](#8-moe-in-a-widely-used-open-model-mixtral-of-experts)), its _internal_ structure can also change. The ordinary FFN from [`introductory/02` §9](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md#9-the-transformer-block-attention-feed-forward-residuals-and-normalization) computes $\mathrm{FFN}(x) = f(xW_1)W_2$ for some activation $f$ (such as ReLU, from [`introductory/01` §4](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#4-activation-functions-why-nonlinearity-matters)). Shazeer's 2020 paper on **Gated Linear Units** (GLU, 门控线性单元) proposes replacing this with a gated variant that computes an elementwise product of two separate linear projections of $x$, one of them passed through a nonlinearity first — for the specific variant called **SwiGLU**, which uses the SiLU/Swish nonlinearity $f(z) = z \cdot \sigma(z)$:

无论 FFN 是稠密的（如 [`introductory/02`](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md) 中所述），还是稀疏 MoE 中的某一个专家（第 3 至[第 8 节](#8-moe-in-a-widely-used-open-model-mixtral-of-experts)），其*内部*结构同样可以发生变化。[`introductory/02` 第 9 节](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md#9-the-transformer-block-attention-feed-forward-residuals-and-normalization)所述的普通 FFN 计算的是 $\mathrm{FFN}(x) = f(xW_1)W_2$，其中 $f$ 是某种激活函数（例如 [`introductory/01` 第 4 节](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#4-activation-functions-why-nonlinearity-matters)中的 ReLU）。Shazeer 于 2020 年提出的**门控线性单元**（Gated Linear Unit，GLU）论文，提议将其替换为一种门控变体：对 $x$ 的两个独立线性投影做逐元素乘积，其中一个投影先经过一个非线性函数——对于其中被称为 **SwiGLU** 的具体变体，所使用的非线性函数是 SiLU/Swish 函数 $f(z) = z \cdot \sigma(z)$：

$$\mathrm{FFN}_{\mathrm{SwiGLU}}(x, W, V, W_2) = (\mathrm{Swish}_1(xW) \otimes xV) W_2$$

($\otimes$ = elementwise product)

Shazeer reports that SwiGLU and related gated variants improve downstream quality over a ReLU-based
FFN of matched parameter count and compute (Shazeer, 2020).

Shazeer 报告称，在参数量与计算量相匹配的前提下，SwiGLU 及相关门控变体相较于基于 ReLU 的 FFN，能够提升下游任务的质量（Shazeer, 2020）。

Matching that count matters because a gated FFN has _three_ weight matrices ($W$, $V$, $W_2$) rather
than the ordinary FFN's two ($W_1$, $W_2$): to hold total parameters fixed, Shazeer's experiments
reduce the hidden dimension $d_{ff}$ by a factor of two-thirds when switching to a gated variant —
concretely, the paper's baseline $d_{ff} = 3072$ becomes $d_{ff} = 2048$ for the GLU variants, which
follows directly from setting $2 \times d_{ff,\text{baseline}} = 3 \times d_{ff,\text{gated}}$ (two
matrices at the wider baseline width equal three matrices at the narrower gated width) and solving
for $d_{ff,\text{gated}} = (2/3) \times 3072 = 2048$ (Shazeer, 2020).

之所以要匹配参数量，是因为门控 FFN 拥有*三个*权重矩阵（$W$、$V$、$W_2$），而普通 FFN 只有两个（$W_1$、$W_2$）：为了保持总参数量不变，Shazeer 的实验在切换到门控变体时，将隐藏维度 $d_{ff}$ 缩减为原来的三分之二——具体而言，论文中基线模型的 $d_{ff} = 3072$，在 GLU 变体中变为 $d_{ff} = 2048$，这直接来自于令 $2 \times d_{ff,\text{baseline}} = 3 \times d_{ff,\text{gated}}$（较宽的基线宽度下两个矩阵的参数量，等于较窄的门控宽度下三个矩阵的参数量）并求解得到 $d_{ff,\text{gated}} = (2/3) \times 3072 = 2048$（Shazeer, 2020）。

SwiGLU-style feed-forward sub-layers, rather than the original ReLU FFN, are used in many widely
deployed large language model families as of this writing.

截至本文撰写之时，许多被广泛部署的大型语言模型系列所使用的前馈子层，采用的都是 SwiGLU 风格，而非最初的 ReLU FFN。

---

## 10. RMSNorm: A Simplified Normalization for Modern Architectures

**RMSNorm：面向现代架构的简化归一化方法**

[`introductory/02` §9](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md#9-the-transformer-block-attention-feed-forward-residuals-and-normalization) introduced **layer normalization** as a way to keep values flowing between
sub-layers in a stable numerical range. The standard layer normalization computes both a mean and a
variance across a layer's activations and re-centers as well as re-scales them. Zhang and Sennrich's
2019 paper on **root mean square layer normalization** (RMSNorm, RMS 层归一化) hypothesizes that the
re-centering (mean-subtraction) part of this computation is not the source of layer normalization's
benefit — only the re-scaling part is — and proposes dropping re-centering entirely. For an
activation vector $a = (a_1, \ldots, a_n)$ and a learned per-dimension gain $g_i$, RMSNorm computes:

[`introductory/02` 第 9 节](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md#9-the-transformer-block-attention-feed-forward-residuals-and-normalization)介绍了**层归一化**（layer normalization），作为使流经各子层之间的数值保持在稳定范围内的一种方法。标准的层归一化会同时计算一层激活值的均值与方差，既做重新居中，也做重新缩放。Zhang 与 Sennrich 于 2019 年提出的**均方根层归一化**（root mean square layer normalization，RMSNorm）论文假设，这一计算中“重新居中”（即减去均值）的部分并非层归一化真正发挥作用的来源——只有“重新缩放”的部分才是——因此提议完全去掉重新居中这一步。对于激活向量 $a = (a_1, \ldots, a_n)$ 与一个可学习的、按维度设置的增益 $g_i$，RMSNorm 的计算方式为：

$$\mathrm{RMS}(a) = \sqrt{\frac{1}{n} \sum_i a_i^2}$$

$$\bar{a}_i = \frac{a_i}{\mathrm{RMS}(a)} \cdot g_i$$

As a worked example, take $a = [3, 4]$ (so $n = 2$) with gain $g = [1, 1]$. $\mathrm{RMS}(a) =
\sqrt{(9 + 16) / 2} = \sqrt{12.5} \approx 3.536$. The normalized output is $\bar{a} = [3/3.536,
4/3.536] \approx [0.849, 1.131]$. Zhang and Sennrich report that RMSNorm matches standard layer
normalization's quality on the tasks they evaluated while being computationally simpler — no mean
needs to be computed or subtracted — which translates directly into faster training and inference
(Zhang and Sennrich, 2019).

举一个手算示例：设 $a = [3, 4]$（因此 $n = 2$），增益 $g = [1, 1]$。 $\mathrm{RMS}(a) = \sqrt{(9 + 16) / 2} = \sqrt{12.5} \approx 3.536$。归一化后的输出为 $\bar{a} = [3/3.536, 4/3.536] \approx [0.849, 1.131]$。 Zhang 与 Sennrich 报告称，在他们所评估的任务上，RMSNorm 的质量能够匹配标准层归一化，同时计算上更为简洁——无需计算或减去均值——这直接转化为更快的训练与推理速度（Zhang and Sennrich, 2019）。

Like SwiGLU in [§9](#9-gated-feed-forward-variants-glu-and-swiglu), RMSNorm has become one of the standard building blocks of the "modern
Transformer" alongside the MoE, GQA/MLA, and RoPE variants covered in this module and
[`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md).

与[第 9 节](#9-gated-feed-forward-variants-glu-and-swiglu)中的 SwiGLU 类似，RMSNorm 如今已与本章及 [`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) 中所讲的 MoE、GQA/MLA 与 RoPE 变体一样，成为“现代 Transformer”的标准构件之一。

---

## 11. Beyond Attention Entirely: State Space Models

**完全脱离注意力机制：状态空间模型**

Every architecture covered so far, in this module and in [`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md), keeps the Transformer's
attention mechanism and modifies something else around it (the feed-forward sub-layer, the
normalization, the number of key/value projections). A structurally different line of work asks
whether attention itself can be replaced.

到目前为止，本章与 [`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) 中所讨论的每一种架构，都保留了 Transformer 的注意力机制，只是改动了它周围的其他部分（前馈子层、归一化方式、键/值投影的数量）。而另一条结构上截然不同的研究路线所探讨的问题是：注意力机制本身是否可以被替代。

Gu and Dao's 2023 Mamba architecture builds on **structured state space models** (SSMs, 结构化状态空间模型) — sequence models with roots in classical control theory, adapted for deep learning — and introduces a **selection mechanism** that lets the model's state-transition parameters depend on the current input, rather than being fixed for the whole sequence as in earlier SSM variants. The resulting architecture processes a sequence with computational cost that scales _linearly_ with sequence length, in contrast to attention's $O(n^2)$ cost established in [`intermediate/02` §4](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md#4-computational-complexity-of-self-attention), while the authors report matching or exceeding Transformer-quality language modeling results at the scales they tested (Gu and Dao, 2023).

Gu 与 Dao 于 2023 年提出的 Mamba 架构，建立在**结构化状态空间模型**（structured state space models，SSMs）——一类根植于经典控制理论、经过改造以适用于深度学习的序列模型——之上，并引入了一种**选择机制**，使模型的状态转移参数能够依赖于当前输入，而不像早期 SSM 变体那样在整个序列中保持固定。由此得到的架构在处理序列时，其计算成本随序列长度*线性*增长，这与 [`intermediate/02` 第 4 节](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md#4-computational-complexity-of-self-attention)中所确立的注意力机制 $O(n^2)$ 成本形成对比；作者报告称，在其所测试的规模下，该架构在语言建模任务上的表现能够匹配甚至超过 Transformer 的质量（Gu and Dao, 2023）。

This is included here as a named, verifiable alternative architecture family, not as a settled
verdict that attention-free models have superseded the Transformer. Whether state-space models match
Transformer-based (including MoE-based) architectures in quality at the very largest scales used in
frontier production systems, and whether hybrid designs combining both approaches outperform either
alone, are active, ongoing research questions rather than settled facts — per this curriculum's
standing rule, this module presents Mamba as a real, verified architectural direction without
asserting a resolved comparison it cannot cite.

在此收录这一内容，是为了介绍一个真实存在、有据可查的替代架构家族，而非断言“无注意力模型已经取代了 Transformer”是一个已成定论的结果。状态空间模型能否在前沿生产系统所使用的最大规模上，匹配基于 Transformer（包括基于 MoE）的架构的质量，以及结合两种方法的混合设计是否会优于单独使用其中任何一种，这些都仍是活跃的、悬而未决的研究问题，而非已经定论的事实——依据本课程体系的一贯规则，本模块将 Mamba 作为一个真实、经过核实的架构方向加以介绍，而不对一个无法引证的比较结论妄下断言。

---

## 12. Summary and What Comes Next

**小结与后续内容**

This chapter completed the Foundations cluster by turning from attention ([`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md)) to the
rest of what defines a modern large language model's architecture: sparse Mixture-of-Experts layers
that decouple total parameter count from per-token compute cost, from their original
conditional-computation motivation ([§2](#2-the-feed-forward-sub-layer-as-a-scaling-bottleneck)–[§3](#3-sparse-mixture-of-experts-the-core-idea)) through the gating mechanics that make routing sparse and
trainable ([§4](#4-the-gating-network-softmax-and-noisy-top-k-gating)), the production-scale systems that made MoE practical (GShard's top-2 routing and
expert capacity, [§5](#5-scaling-moe-to-production-gshards-top-2-routing-and-expert-capacity); Switch Transformer's top-1 routing and load-balancing loss, [§6](#6-switch-transformer-simplifying-to-top-1-routing-and-the-load-balancing-loss); DeepSeekMoE's
fine-grained and shared experts, [§7](#7-fine-grained-and-shared-experts-deepseekmoe); Mixtral's total-versus-active parameter accounting, [§8](#8-moe-in-a-widely-used-open-model-mixtral-of-experts)); gated
feed-forward variants like SwiGLU that change the FFN's internal structure independent of sparsity
([§9](#9-gated-feed-forward-variants-glu-and-swiglu)); RMSNorm as a simplified alternative to layer normalization ([§10](#10-rmsnorm-a-simplified-normalization-for-modern-architectures)); and, briefly, the
state-space-model alternative to attention itself ([§11](#11-beyond-attention-entirely-state-space-models)).

本章通过将视角从注意力机制（[`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md)）转向定义现代大型语言模型架构的其余部分，完成了“基础”（Foundations）主题群的收尾：稀疏专家混合层将总参数量与每 token 的计算成本相解耦，从其最初的条件计算动机出发（第 2 至[第 3 节](#3-sparse-mixture-of-experts-the-core-idea)），到使路由变得稀疏且可训练的门控机制（[第 4 节](#4-the-gating-network-softmax-and-noisy-top-k-gating)），再到使 MoE 在生产环境中变得切实可行的各个系统（GShard 的 top-2 路由与专家容量，[第 5 节](#5-scaling-moe-to-production-gshards-top-2-routing-and-expert-capacity)；Switch Transformer 的 top-1 路由与负载均衡损失，[第 6 节](#6-switch-transformer-simplifying-to-top-1-routing-and-the-load-balancing-loss)；DeepSeekMoE 的细粒度专家与共享专家，[第 7 节](#7-fine-grained-and-shared-experts-deepseekmoe)；Mixtral 的总参数量与激活参数量核算，[第 8 节](#8-moe-in-a-widely-used-open-model-mixtral-of-experts)）；独立于稀疏性、改变 FFN 内部结构的门控前馈变体，如 SwiGLU（[第 9 节](#9-gated-feed-forward-variants-glu-and-swiglu)）；作为层归一化简化替代方案的 RMSNorm（[第 10 节](#10-rmsnorm-a-simplified-normalization-for-modern-architectures)）；以及简要介绍的、完全脱离注意力机制本身的状态空间模型替代方案（[第 11 节](#11-beyond-attention-entirely-state-space-models)）。

Together with [`introductory/01`](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md), [`introductory/02`](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md), [`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md), [`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md), and
[`advanced/01`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md), this module completes the Foundations cluster: every mechanism a reader needs to
understand how a modern large language model is built, trained, and scaled — from a single neuron to
sparse trillion-parameter architectures — has now been introduced with worked examples and verified
citations. The Agent Architecture, Prompt & Context Engineering, and Multi-Agent Systems &
Evaluation clusters build on this foundation to cover what is built _on top of_ the models this
cluster described.

本模块与 [`introductory/01`](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md)、[`introductory/02`](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md)、[`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md)、[`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) 以及 [`advanced/01`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md) 一起，共同完成了“基础”主题群：从单个神经元到稀疏的万亿参数架构，读者理解现代大型语言模型是如何构建、训练与扩展所需的每一个机制，如今都已配以手算示例与经过核实的引文加以介绍。“智能体架构”（Agent Architecture）、“提示与上下文工程”（Prompt & Context Engineering）以及“多智能体系统与评估”（Multi-Agent Systems & Evaluation）这几个主题群，都将建立在这一基础之上，介绍构建于本主题群所描述的模型*之上*的内容。

---

## References

**参考文献**

### External Sources

- [Shazeer, N., Mirhoseini, A., Maziarz, K., Davis, A., Le, Q., Hinton, G., & Dean, J. (2017). Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer.](https://arxiv.org/abs/1701.06538)
- [Lepikhin, D., Lee, H., Xu, Y., Chen, D., Firat, O., Huang, Y., Krikun, M., Shazeer, N., & Chen, Z. (2020). GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding.](https://arxiv.org/abs/2006.16668)
- [Fedus, W., Zoph, B., & Shazeer, N. (2021). Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity.](https://arxiv.org/abs/2101.03961)
- [Dai, D., Deng, C., Zhao, C., Xu, R. X., Gao, H., Chen, D., Li, J., Zeng, W., Yu, X., Wu, Y., Xie, Z., Li, Y. K., Huang, P., Luo, F., Ruan, C., Sui, Z., & Liang, W. (2024). DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models.](https://arxiv.org/abs/2401.06066)
- [Jiang, A. Q., Sablayrolles, A., Roux, A., Mensch, A., Savary, B., Bamford, C., Chaplot, D. S., Casas, D. de las, Hanna, E. B., Bressand, F., et al. (2024). Mixtral of Experts.](https://arxiv.org/abs/2401.04088)
- [Shazeer, N. (2020). GLU Variants Improve Transformer.](https://arxiv.org/abs/2002.05202)
- [Zhang, B., & Sennrich, R. (2019). Root Mean Square Layer Normalization.](https://arxiv.org/abs/1910.07467)
- [Gu, A., & Dao, T. (2023). Mamba: Linear-Time Sequence Modeling with Selective State Spaces.](https://arxiv.org/abs/2312.00752)
- [Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention Is All You Need.](https://arxiv.org/abs/1706.03762)

### Internal Cross-References

- [`introductory/01-neural-networks-and-deep-learning-foundations.md`](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md) — required prerequisite: neurons, layers, activations (ReLU, softmax), backpropagation.
- [`introductory/02-the-transformer-architecture-and-attention.md`](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md) — required prerequisite: the Transformer block, its feed-forward sub-layer ([§9](#9-gated-feed-forward-variants-glu-and-swiglu)), residual connections, and layer normalization.
- [`intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) — required prerequisite: multi-head attention mathematics, the KV cache, $O(n^2)$ attention cost, and MQA/GQA/MLA as precedent for trading exact computation for efficiency.
- [`advanced/01-scaling-laws-and-emergent-capabilities.md`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md) — required prerequisite: the scaling relationship between parameters, data, compute, and performance that motivates decoupling total parameters from per-token compute ([§2](#2-the-feed-forward-sub-layer-as-a-scaling-bottleneck)).
- [`advanced/05-advanced-context-engineering-long-context-and-budgeting.md`](https://anu00.dev/curriculum/advanced/05-advanced-context-engineering-long-context-and-budgeting.md) — covers architectural and systems mitigations for the long-context costs noted in [`intermediate/02` §4](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md#4-computational-complexity-of-self-attention) and touched on again in [§11](#11-beyond-attention-entirely-state-space-models) here.
