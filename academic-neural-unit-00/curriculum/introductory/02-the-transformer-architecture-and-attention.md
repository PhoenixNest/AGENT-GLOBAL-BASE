# The Transformer Architecture & Attention

**Transformer 架构与注意力机制**

| Field   | English                                                          | 中文                                    |
| ------- | ---------------------------------------------------------------- | --------------------------------------- |
| Level   | Introductory                                                     | 入门                                    |
| Cluster | Foundations                                                      | 基础                                    |
| Author  | Dr. Yuna Baek, Research Scientist — AI / Neural Networks, ANU-00 | ANU-00 AI/神经网络研究员 Yuna Baek 博士 |

---

This chapter assumes exactly what `introductory/01-neural-networks-and-deep-learning-foundations.md`
already taught — neurons, weighted sums, activation functions, layers, forward propagation, loss
functions, gradient descent, and backpropagation — and introduces nothing beyond secondary-school
algebra and that prior module. Every new term is defined at first use, as required throughout this
curriculum.

本章严格建立在 `introductory/01-neural-networks-and-deep-learning-foundations.md` 已经讲授过的内容之上——神经元、加权求和、激活函数、层、前向传播、损失函数、梯度下降与反向传播——除此之外只要求掌握中学代数知识。按照本课程体系的统一要求，所有新术语均在首次出现时给出定义。

---

## 1. From Feedforward Networks to Sequence Models

**从前馈网络到序列模型**

[`introductory/01`](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md) described a **feedforward network** — data flows in one direction, from input
layer through hidden layers to output layer, with no memory of previous inputs. That kind of network
works well when each input is independent (for example, classifying one image at a time).

[`introductory/01`](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md) 介绍的是**前馈网络**——数据沿单一方向流动，从输入层经隐藏层直至输出层，对之前的输入没有记忆。当每个输入相互独立时（例如逐张分类图像），这种网络表现良好。

Language is different: a sentence is a **sequence** of tokens (token, discussed below) in which
meaning depends heavily on order and on relationships between tokens that may be far apart — "The
trophy didn't fit in the suitcase because _it_ was too big" requires knowing that "it" refers to the
trophy, not the suitcase, a relationship spanning several words. This chapter introduces the
Transformer (Transformer 架构), the architecture that made modern large language models possible by
directly modeling relationships between every pair of positions in a sequence.

而语言则不同：一个句子是一个 token（下文将解释）构成的**序列**，其含义严重依赖于顺序，也依赖于可能相距很远的 token 之间的关系——"The trophy didn't fit in the suitcase because _it_ was too big"（奖杯放不进手提箱，因为*它*太大了）这句话，要求读者知道“它”指的是奖杯而非手提箱，而这一关系横跨了好几个词。本章将介绍 Transformer（Transformer 架构）——这一直接对序列中每一对位置之间的关系进行建模的架构，正是它使当今的大型语言模型成为可能。

Before any of this, text must be converted into numbers a network can process. This is done by
**tokenization**: splitting text into small units called **tokens** — which may be whole words,
sub-words, or individual characters, depending on the tokenizer — and mapping each token to an
integer ID via a fixed **vocabulary**.

在此之前，文本必须先被转换为网络能够处理的数字。这一过程称为**分词**：将文本切分为称作 **token** 的小单元——根据分词器的不同，token 可以是完整的单词、子词，或单个字符——并通过一个固定的**词表**将每个 token 映射为一个整数 ID。

Each ID is then converted into a list of numbers called an **embedding vector** — a learned
representation, of a fixed size `d_model`, that captures something about the token's meaning as
numbers a network can compute with. This chapter treats tokenization and embeddings as a given input
format; the mechanics of how a network processes and updates the embeddings that follow tokenization
is the main subject from [§4](#4-queries-keys-and-values) onward.

随后每个 ID 会被转换为一串数字，称为**嵌入向量**——这是一种固定维度 `d_model` 的可学习表示，以网络能够进行计算的数字形式，捕捉该 token 含义的某些方面。本章将分词与嵌入视为既定的输入格式；从[第 4 节](#4-queries-keys-and-values)开始，本章的核心主题是网络如何处理并更新分词之后所得到的嵌入向量。

---

## 2. Why Sequential Processing Struggles: The Motivation for Attention

**为何顺序处理会遇到困难：注意力机制的动机**

Before the Transformer, the dominant approach to sequences was the **recurrent neural network**
(RNN), which processes a sequence one token at a time, carrying forward a single fixed-size summary
vector (a "hidden state") updated at each step. This design has two structural weaknesses that
motivated the search for an alternative.

在 Transformer 出现之前，处理序列的主流方法是**循环神经网络**（RNN），它逐个 token 地处理序列，并携带一个固定大小的摘要向量（称为“隐藏状态”）在每一步不断更新。这种设计存在两个结构性弱点，正是它们促使人们去寻找替代方案。

First, because information about an early token can only reach a late token by being carried, and
potentially diluted, through every intermediate step, RNNs struggle to preserve relationships
between tokens that are far apart in long sequences.

第一，由于早期 token 的信息只能通过每一个中间步骤被携带（并可能被稀释）之后才能传递到后面的 token，RNN 在长序列中难以保持相距较远的 token 之间的关系。

Second, because step `t` depends on the completed output of step $t-1$, the computation is
inherently **sequential** — it cannot be parallelized across the length of the sequence — which
makes RNNs slow to train on the long sequences and large datasets needed for modern language
modeling. Vaswani et al.'s 2017 paper introducing the Transformer explicitly names both of these
constraints as the motivation for an architecture that eliminates recurrence entirely (Vaswani et
al., 2017).

第二，由于第 `t` 步的计算依赖于第 $t-1$ 步已完成的输出，这种计算本质上是**顺序性的**——无法在序列长度维度上并行化——这使得 RNN 在训练现代语言模型所需的长序列和大规模数据集时速度缓慢。 Vaswani 等人 2017 年提出 Transformer 的论文明确将这两点局限性作为其设计动机，从而彻底摒弃了循环结构（Vaswani et al., 2017）。

---

## 3. The Core Idea of Attention: Letting Every Position Look at Every Other Position

**注意力的核心思想：让每个位置都能“看到”其他所有位置**

The **attention mechanism** replaces step-by-step recurrence with a direct computation: for every
position in a sequence, compute how relevant every other position is to it, and produce an output
for that position as a weighted combination of information from all positions, weighted by
relevance.

**注意力机制**用一种直接的计算方式取代了逐步的循环计算：对于序列中的每一个位置，计算其他每一个位置与它的相关程度，并将该位置的输出表示为所有位置信息按相关程度加权组合而成的结果。

Concretely, in the trophy/suitcase example from [§1](#1-from-feedforward-networks-to-sequence-models), an attention mechanism can let the
representation of "it" directly incorporate information from "trophy," no matter how many words
apart they are, in a single computational step rather than through a chain of sequential updates.
This direct, all-pairs computation is also fully parallelizable — every position's relevance to
every other position can be computed simultaneously — which is the second major advantage attention
has over recurrence.

具体来说，回到[第 1 节](#1-from-feedforward-networks-to-sequence-models)中奖杯/手提箱的例子，注意力机制可以让“它”这个词的表示直接融入“奖杯”一词的信息，无论二者相隔多远，只需一步计算即可完成，而不必经过一连串顺序更新。这种直接的、任意两两位置之间的计算方式还具有完全可并行化的特点——每个位置与其他所有位置的相关程度都可以同时计算——这正是注意力机制相较于循环结构的第二大优势。

The remainder of this chapter builds up exactly how "relevance" is computed and how it is turned
into a weighted combination. The full mathematical treatment — including multiple attention "heads"
computed in parallel — is deferred to [`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md); this chapter covers the single -head
mechanics in enough depth to fully understand what a Transformer computes.

本章接下来的部分将具体讲解“相关程度”究竟是如何计算出来的，以及它又是如何被转化为加权组合的。完整的数学处理——包括并行计算的多个注意力“头”——将留待 [`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) 详细展开；本章将单头注意力的机制讲解到足以让读者完全理解 Transformer 究竟在计算什么的深度。

---

## 4. Queries, Keys, and Values

**查询、键与值**

Attention computes relevance using three vectors derived from each token's embedding, via three
separate learned weight matrices (recall from [`introductory/01` §3](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#3-the-single-neuron-weights-bias-and-activation) that a weight matrix is simply a
collection of the same kind of weighted-sum parameters covered there, applied to a whole vector at
once rather than to single numbers). For a token's embedding vector `x`:

注意力机制通过每个 token 的嵌入向量，经由三个独立的可学习权重矩阵，计算出三个向量来衡量相关程度（回顾 [`introductory/01` 第 3 节](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#3-the-single-neuron-weights-bias-and-activation)可知，权重矩阵不过是该节所讲的同一类加权求和参数的集合，只是这里被整体应用于一个向量，而非单个数字）。对于某个 token 的嵌入向量 `x`：

| Vector                          | EN                                                                                            | 中文                                                                 |
| ------------------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Query**（查询向量）`q = xW_Q` | represents “what this token is looking for” in other tokens.                                  | 表示“这个 token 正在寻找什么”。                                      |
| **Key**（键向量）`k = xW_K`     | represents “what this token offers” as a match target for other tokens' queries.              | 表示“这个 token 能提供什么”，作为供其他 token 的查询进行匹配的目标。 |
| **Value**（值向量）`v = xW_V`   | represents “the actual content this token contributes” once it has been selected as relevant. | 表示“一旦这个 token 被判定为相关，它实际贡献的内容是什么”。          |

`W_Q`, `W_K`, and `W_V` are learned parameter matrices — adjusted by backpropagation exactly as
described in [`introductory/01` §9](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#9-backpropagation-computing-gradients-efficiently) — shared across all positions in the sequence.

`W_Q`、`W_K` 和 `W_V` 都是可学习的参数矩阵——其调整方式与 [`introductory/01` 第 9 节](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#9-backpropagation-computing-gradients-efficiently)所述的反向传播完全相同——并且在序列的所有位置上是共享的。

An analogy: think of a library catalog search. The **query** is the search phrase you type in. Every
book's **key** is the metadata that the search matches against (title, subject tags). Every book's
**value** is the book's actual content, which you receive once your query matches its key well.
Attention performs exactly this match-then-retrieve operation, for every token against every other
token, simultaneously, and does it with soft (weighted) rather than all-or-nothing matches — covered
next in [§5](#5-scaled-dot-product-attention-the-formula).

打个比方：可以把它想象成图书馆目录检索。**查询**就是你输入的搜索词。每本书的**键**是用来与搜索词进行匹配的元数据（书名、主题标签）。每本书的**值**则是这本书的实际内容——一旦你的查询与它的键匹配良好，你就能获取这些内容。注意力机制对每一个 token 相对于其他所有 token，同时执行的正是这种“先匹配、后检索”的操作，并且采用的是软性（加权）匹配，而非非此即彼的硬匹配——这将在下面的[第 5 节](#5-scaled-dot-product-attention-the-formula)中介绍。

---

## 5. Scaled Dot-Product Attention: The Formula

**缩放点积注意力：公式**

Vaswani et al. (2017) define **scaled dot-product attention** with the formula:

Vaswani 等人（2017）给出了**缩放点积注意力**（scaled dot-product attention）的公式：

$$
\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

Here `Q`, `K`, and `V` are matrices stacking the query, key, and value vectors for every position in
the sequence (one row per token). $QK^T$ computes the dot product between every query and every key
— a dot product between two vectors is large when the vectors point in similar directions, so this
step produces a raw relevance score between every pair of positions. $d_k$ is the dimension of the
key vectors, and dividing by $\sqrt{d_k}$ is a scaling step Vaswani et al. found necessary because
for large $d_k$, raw dot products can grow large in magnitude and push the softmax function
(introduced in [`introductory/01` §4](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#4-activation-functions-why-nonlinearity-matters)) into regions where its gradient is extremely small, which harms
learning (Vaswani et al., 2017).

其中 `Q`、`K`、`V` 是分别将序列中每个位置的查询、键、值向量按行堆叠而成的矩阵（每个 token 对应一行）。 $QK^T$ 计算的是每个查询与每个键之间的点积——两个向量的点积在方向相近时数值较大，因此这一步会为每一对位置生成一个原始的相关性得分。 $d_k$ 是键向量的维度，除以 $\sqrt{d_k}$ 是 Vaswani 等人发现必要的一个缩放步骤：当 $d_k$ 较大时，原始点积的数值可能变得很大，从而将 softmax 函数（已在 [`introductory/01` 第 4 节](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#4-activation-functions-why-nonlinearity-matters)中介绍）推向梯度极小的区域，损害学习效果（Vaswani et al., 2017）。

The **softmax** turns each row of relevance scores into a probability distribution — the **attention
weights** — that sums to 1 across all positions being attended to. Finally, multiplying by `V`
produces, for each position, a weighted sum of all value vectors, weighted by how much attention
that position pays to each other position.

**Softmax** 将相关性得分的每一行转化为一个概率分布——即**注意力权重**——在被关注的所有位置上求和为 1。最后，与 `V` 相乘，会为每个位置生成一个所有值向量的加权和，权重取决于该位置对其他每个位置的关注程度。

---

## 6. A Worked Example: Attention by Hand on a Tiny Sequence

**手算示例：微型序列上的注意力计算**

Consider a toy sequence of two tokens, with embedding dimension `d_model = 2`, and — purely to keep
the arithmetic simple for this illustration — suppose `W_Q`, `W_K`, and `W_V` are all the $2 \times
2$ identity matrix, so `Q = K = V = X`, the raw embeddings themselves. Let the two token embeddings
be $x_1 = [1, 0]$ and $x_2 = [0, 1]$, stacked as `X = [[1, 0], [0, 1]]`.

考虑一个由两个 token 组成的玩具序列，嵌入维度 `d_model = 2`。为了使这个示例的运算保持简洁——仅出于说明目的——假设 `W_Q`、`W_K`、`W_V` 均为 $2 \times 2$ 单位矩阵，因此 `Q = K = V = X`，即原始嵌入本身。设两个 token 的嵌入分别为 $x_1 = [1, 0]$ 与 $x_2 = [0, 1]$，堆叠为 `X = [[1, 0], [0, 1]]`。

First, compute raw scores $QK^T = XX^T$:

首先计算原始得分 $QK^T = XX^T$：

$$
XX^T = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \quad (x_1 \cdot x_1 = 1,\ x_1 \cdot x_2 = 0,\ x_2 \cdot x_1 = 0,\ x_2 \cdot x_2 = 1)
$$

Scale by $\sqrt{d_k} = \sqrt{2} \approx 1.414$:

按 $\sqrt{d_k} = \sqrt{2} \approx 1.414$ 进行缩放：

$$
\text{scores} = \begin{bmatrix} 0.707 & 0 \\ 0 & 0.707 \end{bmatrix}
$$

Apply softmax to each row. For row 1, `[0.707, 0]`: $e^{0.707} \approx 2.028$, `e^0 = 1`, sum
$\approx 3.028$, giving attention weights `[0.670, 0.330]`. By symmetry, row 2 gives `[0.330,
0.670]`.

对每一行分别应用 softmax。以第一行 `[0.707, 0]` 为例：$e^{0.707} \approx 2.028$，`e^0 = 1`，两者之和约为 `3.028`，得到注意力权重 `[0.670, 0.330]`。由对称性可知，第二行的注意力权重为 `[0.330, 0.670]`。

Finally, multiply the attention weights by `V = X` to get each position's output. Token 1's output
is $0.670 \cdot [1,0] + 0.330 \cdot [0,1] = [0.670, 0.330]$ — a blend weighted mostly toward its own
value (since $x_1$'s query matched its own key most strongly), with a smaller contribution from
token 2. This is the essential behavior of attention: an output for each position that is a
relevance-weighted mixture of information from across the whole sequence, rather than information
from only that position or only the immediately preceding one.

最后，将注意力权重与 `V = X` 相乘，得到每个位置的输出。token 1 的输出为 $0.670 \cdot [1,0] + 0.330 \cdot [0,1] = [0.670, 0.330]$——这是一个主要偏向自身值的混合结果（因为 $x_1$ 的查询与自身的键匹配程度最高），同时也包含了来自 token 2 的较小贡献。这正是注意力机制的核心行为：每个位置的输出，都是来自整个序列信息、按相关程度加权混合而成的结果，而不仅仅是来自该位置本身或紧邻的前一个位置的信息。

---

## 7. Multi-Head Attention: A First Look

**多头注意力：初步了解**

In practice, Transformers do not compute a single attention pattern per layer; they compute several
attention patterns in parallel, called **heads**, each with its own learned `W_Q`, `W_K`, `W_V`
matrices projecting into a smaller dimension, and then concatenate the heads' outputs back together.

在实际应用中，Transformer 并不会在每一层只计算一种注意力模式，而是并行计算若干种注意力模式，称为**头**，每个头都拥有各自独立学习的 `W_Q`、`W_K`、`W_V` 矩阵，将输入投影到更小的维度，随后再将各个头的输出重新拼接在一起。

Vaswani et al. (2017) motivate this as letting different heads specialize in attending to different
kinds of relationships at once — for example, one head might learn to track subject-verb
relationships while another tracks pronoun references — rather than forcing a single attention
pattern to represent every kind of relevant relationship simultaneously. This chapter introduces the
concept at a high level only; the full mathematics of splitting, computing, and recombining multiple
heads — along with the practical machinery real systems need to run attention efficiently, such as
the KV cache and modern positional encoding schemes — is the entire subject of
`intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md`.

Vaswani 等人（2017）指出，这样设计的动机在于让不同的头能够同时专注于捕捉不同类型的关系——例如，某个头可能学会追踪主谓关系，而另一个头则追踪代词指代关系——而不是强迫单一的注意力模式同时表示所有种类的相关关系。本章仅在较高层面介绍这一概念；关于多头拆分、计算与重新组合的完整数学细节，以及真实系统高效运行注意力所需的实际机制（例如 KV 缓存与现代位置编码方案），将是 `intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md` 的全部主题。

---

## 8. Positional Encoding: Giving the Model a Sense of Order

**位置编码：赋予模型顺序感**

The attention formula in [§5](#5-scaled-dot-product-attention-the-formula) has a notable property: if the positions of two tokens in the input
sequence were swapped, but the tokens themselves stayed the same, the raw attention computation
would treat them identically except for which row/column they occupy — nothing in $QK^T$ inherently
encodes _where_ in the sequence a token sits. This matters because word order carries meaning ("dog
bites man" and "man bites dog" use the same tokens but mean different things).

[第 5 节](#5-scaled-dot-product-attention-the-formula)所给出的注意力公式有一个值得注意的性质：如果输入序列中两个 token 的位置被互换，而 token 本身保持不变，那么原始的注意力计算除了所处的行/列不同之外，会将它们一视同仁——$QK^T$ 本身并未编码某个 token 在序列中所处的*位置*。这一点至关重要，因为词序本身携带着意义（“狗咬人”和“人咬狗”使用的是相同的词，但含义截然不同）。

Vaswani et al. (2017) address this by adding a **positional encoding** vector to each token's
embedding before it enters the attention layers — a vector, unique to each position, generated from
sine and cosine functions of different frequencies, so that the model has direct access to each
token's position, and to the relative distance between any two positions, as part of its input
(Vaswani et al., 2017). This chapter's coverage of positional encoding stops at this original
sinusoidal scheme; newer schemes such as rotary position embedding, which modify the attention
computation itself rather than adding a vector to the input, are covered in [`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md).

Vaswani 等人（2017）通过在每个 token 的嵌入向量进入注意力层之前，加上一个**位置编码**向量来解决这一问题——这是一个对每个位置都独一无二的向量，由不同频率的正弦与余弦函数生成，从而使模型能够直接获取每个 token 的位置信息，以及任意两个位置之间的相对距离，并将其作为输入的一部分（Vaswani et al., 2017）。本章对位置编码的介绍止步于这一最初的正弦方案；诸如旋转位置编码等更新的方案——它们直接修改注意力计算本身，而非在输入上叠加向量——将在 [`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) 中介绍。

---

## 9. The Transformer Block: Attention, Feed-Forward, Residuals, and Normalization

**Transformer 块：注意力、前馈网络、残差连接与归一化**

A single **Transformer block** (Transformer 块) combines several pieces into one repeatable unit,
stacked many times to form a deep network (recall “deep” from [`introductory/01` §12](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#12-deep-learning-why-deep)).

一个完整的**Transformer 块**（Transformer block）将若干组件组合成一个可重复的单元，通过多次堆叠形成一个深层网络（回顾 [`introductory/01` 第 12 节](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#12-deep-learning-why-deep)中“深度”的含义）。

| #   | Component                                        | EN                                                                                                                                                                                                                                                                                                                                                                                                                         | 中文                                                                                                                                                                                                                                                                                                                                          |
| --- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Multi-head attention sub-layer（多头注意力子层） | lets every position gather relevant information from across the sequence ([§7](#7-multi-head-attention-a-first-look)).                                                                                                                                                                                                                                                                                                     | 让每个位置都能从整个序列中汇集相关信息（[第 7 节](#7-multi-head-attention-a-first-look)）。                                                                                                                                                                                                                                                   |
| 2   | **Feed-forward network**（前馈网络）             | a position-wise, ordinary multi-layer perceptron of the kind built in [`introductory/01` §5](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#5-from-one-neuron-to-a-network-layers-and-forward-propagation), applied independently to each position — adds further nonlinear processing capacity.                                                                            | 一个逐位置的网络——即 [`introductory/01` 第 5 节](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#5-from-one-neuron-to-a-network-layers-and-forward-propagation)所搭建的那种普通多层感知机，被独立地应用于每个位置——增加了进一步的非线性处理能力。                                               |
| 3   | **Residual connection**（残差连接）              | adds each sub-layer's input directly to its output (`output = SubLayer(x) + x`), which helps gradients flow through very deep stacks of blocks during backpropagation, addressing a version of the vanishing-gradient difficulty first mentioned in [`introductory/01` §4](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#4-activation-functions-why-nonlinearity-matters). | 将每个子层的输入直接加到其输出上（`output = SubLayer(x) + x`），这有助于梯度在反向传播过程中顺利流经非常深的块堆叠结构，缓解了 [`introductory/01` 第 4 节](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#4-activation-functions-why-nonlinearity-matters)中首次提到的梯度消失难题的一种变体。 |
| 4   | **Layer normalization**（层归一化）              | rescales the values flowing between sub-layers to keep them in a stable numerical range, which stabilizes and speeds up training.                                                                                                                                                                                                                                                                                          | 对子层之间流动的数值进行重新缩放，使其保持在稳定的数值范围内，从而使训练更加稳定和快速。                                                                                                                                                                                                                                                      |

Vaswani et al. (2017) specify this block structure, and it remains, with only minor variations (such
as where normalization is placed relative to each sub-layer), the structural backbone of essentially
every large language model built since.

Vaswani 等人（2017）明确规定了这一块结构，此后除了少量变体（例如归一化相对于各子层的放置位置）之外，它至今仍是几乎所有大型语言模型的结构骨架。

---

## 10. Encoder-Decoder vs. Decoder-Only Architectures

**编码器-解码器架构与仅解码器架构**

Vaswani et al.'s original Transformer (2017) was built for machine translation and used two stacks
of blocks: an **encoder**, which processes the entire input sequence (for example, a sentence in
French) and produces a contextual representation of it, and a **decoder**, which generates the
output sequence (for example, the English translation) one token at a time, attending both to its
own previously generated tokens and to the encoder's representation.

Vaswani 等人最初提出的 Transformer（2017）是为机器翻译任务设计的，使用了两组块堆叠：**编码器**负责处理整个输入序列（例如一句法语），并生成其上下文表示；**解码器**则逐个 token 地生成输出序列（例如对应的英语翻译），在生成过程中既关注自己此前已生成的 token，也关注编码器所产生的表示。

Most modern large language models used for open-ended text generation, however, use a
**decoder-only** architecture: a single stack of Transformer blocks that both reads the input and
generates the output as one continuous sequence, using a restriction called **causal masking** —
preventing each position from attending to positions after it — so that generation remains a
well-defined, position-by-position process. Causal masking and its interaction with efficient
generation are covered in depth in [`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md).

然而，如今大多数用于开放式文本生成的大型语言模型采用的是**仅解码器**架构：使用单一的一组 Transformer 块堆叠，既读取输入，又将输出作为同一个连续序列生成，并通过一种称为**因果掩码**的限制——阻止每个位置关注其之后的位置——使生成过程始终是一个良定义的、逐位置进行的过程。因果掩码及其与高效生成之间的相互作用，将在 [`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) 中深入讲解。

---

## 11. Putting It Together: How GPT-Style Models Use This

**融会贯通：GPT 系列模型如何运用这些机制**

A modern decoder-only language model, in outline, works as follows: input text is tokenized ([§1](#1-from-feedforward-networks-to-sequence-models)) and
converted to embeddings, positional encodings are added ([§8](#8-positional-encoding-giving-the-model-a-sense-of-order)), the resulting vectors pass through
many stacked Transformer blocks ([§9](#9-the-transformer-block-attention-feed-forward-residuals-and-normalization)), each combining causally-masked multi-head attention ([§5](#5-scaled-dot-product-attention-the-formula)–[§7](#7-multi-head-attention-a-first-look),
[§10](#10-encoder-decoder-vs-decoder-only-architectures)) with a feed-forward network, residuals, and normalization, and the final block's output is
converted, via one more weight matrix and a softmax ([`introductory/01` §4](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#4-activation-functions-why-nonlinearity-matters)), into a probability
distribution over the vocabulary for what token comes next.

一个现代的仅解码器语言模型，概括来说是这样工作的：输入文本先被分词（[第 1 节](#1-from-feedforward-networks-to-sequence-models)）并转换为嵌入向量，随后加上位置编码（[第 8 节](#8-positional-encoding-giving-the-model-a-sense-of-order)），得到的向量依次经过多层堆叠的 Transformer 块（[第 9 节](#9-the-transformer-block-attention-feed-forward-residuals-and-normalization)），每个块都将带因果掩码的多头注意力（第 5 至[第 7 节](#7-multi-head-attention-a-first-look)、[第 10 节](#10-encoder-decoder-vs-decoder-only-architectures)）与前馈网络、残差连接和归一化结合在一起，最后一个块的输出再经过一个权重矩阵和 softmax（[`introductory/01` 第 4 节](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md#4-activation-functions-why-nonlinearity-matters)）的处理，转化为词表上关于“下一个 token 是什么”的概率分布。

Generating text one token at a time, feeding each generated token back in as part of the input for
the next step, is the basic operating loop of essentially every GPT-style model — every mechanic in
that loop was introduced across this chapter and [`introductory/01`](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md).

逐个 token 地生成文本，并将每个已生成的 token 反馈回输入中作为下一步的一部分，正是几乎所有 GPT 系列模型的基本运行循环——这一循环中的每一个机制，都已在本章与 [`introductory/01`](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md) 中逐一介绍完毕。

---

## 12. Summary and What Comes Next

**小结与后续内容**

This chapter introduced the Transformer as the answer to a specific problem — modeling relationships
between tokens across a whole sequence, in parallel, without the sequential bottleneck of recurrence
— via queries, keys, values, scaled dot-product attention, positional encoding, and the full
Transformer block combining attention with feed-forward layers, residuals, and normalization.
Together with [`introductory/01`](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md), this chapter completes the introductory Foundations cluster: every
subsequent module in this curriculum, at every level, assumes the vocabulary built across these two
chapters.

本章将 Transformer 引入为解决一个特定问题的方案——在不依赖循环结构所带来的顺序性瓶颈的前提下，并行地建模一整个序列中 token 之间的关系——具体通过查询、键、值、缩放点积注意力、位置编码，以及将注意力与前馈层、残差连接和归一化相结合的完整 Transformer 块来实现。本章与 [`introductory/01`](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md) 一起，共同完成了入门级的“基础”（Foundations）主题群：本课程体系中此后所有层级的每一个模块，都将以这两章所建立的词汇为前提。

`intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md` returns to exactly
the attention mechanism introduced here and works through it in full mathematical detail — the
complete multi-head computation, the KV cache used to make autoregressive generation efficient, and
the family of modern positional encoding schemes (rotary embeddings, ALiBi) that have largely
superseded the original sinusoidal scheme from [§8](#8-positional-encoding-giving-the-model-a-sense-of-order).

`intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md` 将重新回到本章所介绍的注意力机制，并对其进行完整的数学层面的详细展开——完整的多头计算过程、用于提升自回归生成效率的 KV 缓存，以及在很大程度上已取代[第 8 节](#8-positional-encoding-giving-the-model-a-sense-of-order)中最初正弦方案的现代位置编码方案家族（旋转位置编码、ALiBi）。

---

## References

**参考文献**

### External Sources

- [Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention Is All You Need.](https://arxiv.org/abs/1706.03762)
- [Goodfellow, I., Bengio, Y., & Courville, A. (2016). _Deep Learning_. MIT Press.](https://www.deeplearningbook.org/)

### Internal Cross-References

- [`introductory/01-neural-networks-and-deep-learning-foundations.md`](https://anu00.dev/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md) — required prerequisite: neurons, layers, activations, loss, gradient descent, backpropagation.
- [`intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) — extends the single-head attention mechanics introduced here into full multi-head, KV-cache, and positional-encoding detail.
- [`advanced/02-mixture-of-experts-and-modern-architecture-variants.md`](https://anu00.dev/curriculum/advanced/02-mixture-of-experts-and-modern-architecture-variants.md) — extends the Transformer block's feed-forward sub-layer ([§9](#9-the-transformer-block-attention-feed-forward-residuals-and-normalization)) into sparse mixture-of-experts variants.
