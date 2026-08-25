# Context Windows, Tokens & Memory Basics

**上下文窗口、词元与记忆基础**

| Field   | English                                                          | 中文                                          |
| ------- | ---------------------------------------------------------------- | --------------------------------------------- |
| Level   | Introductory                                                     | 入门                                          |
| Cluster | Prompt & Context Engineering                                     | 提示与上下文工程                              |
| Author  | Dr. Rafael Ibarra-Costa, Research Scientist — Generalist, ANU-00 | ANU-00 通才研究科学家拉斐尔·伊瓦拉-科斯塔博士 |

---

## 1. Why This Module Exists

**本模块的意义**

Every large language model (LLM) — the kind of system behind ChatGPT, Claude, and the agents this
curriculum trains you to build — has a hard physical limit on how much text it can "see" at once
when it produces a response.

每一个大语言模型（LLM，即支撑 ChatGPT、Claude 以及本课程将教你构建的智能体背后的那类系统）在生成一次回复时，能够“看到”的文本量都存在一个硬性的物理上限。

That limit has a name, a unit of measurement, and real engineering consequences, and understanding
all three is a prerequisite for almost everything later in this curriculum: prompt engineering, tool
use, retrieval, and multi-agent coordination all live inside that limit and are shaped by it. This
module assumes no prior background — you do not need to have read anything about neural networks to
follow it, though it does connect, where useful, to concepts introduced in [`introductory/01`](/academic-neural-unit-00/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md) (neural
network foundations) and [`introductory/02`](/academic-neural-unit-00/curriculum/introductory/02-the-transformer-architecture-and-attention.md) (the Transformer architecture and attention) so that the
"why" behind the limit, not just the "what," is available to you.

这个上限有专门的名称、有计量单位，也会带来真实的工程后果——理解这三者，是学好本课程后续几乎所有内容的前提：提示工程、工具使用、检索增强以及多智能体协作，全部都发生在这个限制之内，并被它深刻塑造。本模块不预设任何背景知识——你完全不需要先读过任何关于神经网络的内容也能跟上；不过在有帮助之处，它会与 [`introductory/01`](/academic-neural-unit-00/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md)（神经网络基础）和 [`introductory/02`](/academic-neural-unit-00/curriculum/introductory/02-the-transformer-architecture-and-attention.md)（Transformer 架构与注意力机制）中引入的概念相互印证，这样你不仅知道限制“是什么”，也能理解它“为什么存在”。

By the end of this module you will be able to:

- define a token and explain how text is broken into them
- explain what a context window is and why it is measured in tokens rather than words or characters
- explain, at a basic level, why context windows cannot simply be made arbitrarily large
- distinguish a model's context window (its working memory for a single interaction) from persistent
  memory systems that survive across interactions
- reason about a simple token budget the way an engineer building an agent has to

学完本模块后，你将能够：

- 给出词元的定义，并解释文本是如何被切分成词元的- 说明什么是上下文窗口，以及为什么它是以词元而非单词或字符来计量的- 在基础层面上解释为什么上下文窗口不能被简单地无限扩大- 区分模型的上下文窗口（它在单次交互中的“工作记忆”）与能够跨越多次交互而持续存在的记忆系统- 能够像构建智能体的工程师那样，对一个简单的词元预算进行推理

---

## 2. What Is a Token?

**什么是词元？**

A language model does not read text the way you do, one letter or one word at a time in the ordinary
sense. Instead, before any text reaches the model, it is broken into pieces called **tokens** — the
smallest unit of text the model actually processes.

语言模型阅读文本的方式，与你我通常逐字逐词阅读的方式并不相同。在任何文本进入模型之前，它都会先被切分成被称为**词元**的片段——这是模型实际处理的最小文本单位。

A token might be a whole common word ("the", "cat"), a fragment of a longer or rarer word ("token",
"ization"), a single punctuation mark, or even a single character, depending on how frequently that
piece appears in the data the tokenizer was built from. This intermediate granularity — smaller than
a word, usually larger than a single character — is deliberate, and the next section explains
exactly how it is chosen.

一个词元可能是一个完整的常见单词（如 "the"、"cat"），也可能是一个较长或较生僻单词的片段（如 "token"、"ization"），还可能是一个标点符号，甚至是单个字符——具体取决于这个片段在构建分词器所用数据中出现的频率。这种介于单词和单个字符之间的中等粒度并非偶然，而是刻意设计的结果，下一节将准确解释它是如何被确定的。

Why not just use whole words as the unit? Two reasons.

为什么不直接以整个单词作为处理单位呢？原因有两个。

First, natural language has an effectively unbounded vocabulary — new words, names, typos, product
names, and code identifiers appear constantly, and a model that only knows a fixed dictionary of
whole words has no way to represent anything outside it. Second, whole-word vocabularies for
morphologically rich languages (languages where a single root word takes many different forms, such
as verb conjugations) would need to be enormous to cover every form. Subword tokenization solves
both problems: any word, known or unknown, can always be represented as some sequence of smaller,
previously-seen pieces, right down to individual bytes in the worst case.

第一，自然语言的词汇量实际上是无限的——新词、人名、拼写错误、产品名称、代码标识符层出不穷，而一个只认识固定词典中完整单词的模型，将完全无法表示词典之外的任何内容。第二，对于形态丰富的语言（即同一个词根会衍生出大量不同形式的语言，例如动词变位）而言，若要以整词为单位覆盖所有形式，词表将变得极其庞大。子词分词同时解决了这两个问题：任何单词，无论是否曾经见过，总能被表示为若干个此前已经学过的、更小片段的序列，在最坏情况下甚至可以细分到单个字节。

---

## 3. Tokenization in Practice: Byte-Pair Encoding

**分词的实践：字节对编码**

The dominant algorithm used to build the token vocabulary for modern LLMs is **Byte-Pair Encoding (BPE, 字节对编码)**, introduced for neural machine translation by Sennrich, Haddow, and Birch (2016). The idea is simple and can be worked through by hand. Start with a text corpus split into individual characters (with a special end-of-word marker). Count every adjacent pair of symbols that appears in the corpus.

现代大语言模型构建词元词表所使用的主流算法是**字节对编码（Byte-Pair Encoding，BPE）**，由 Sennrich、 Haddow 和 Birch 于 2016 年在神经机器翻译研究中提出。这个思路十分简洁，也完全可以手工演算一遍。首先将语料库拆分为单个字符（并附加一个特殊的词尾标记）。然后统计语料库中每一对相邻符号出现的次数。

Merge the single most frequent pair into a new, single symbol. Repeat — counting pairs and merging
the most frequent one — for a fixed number of iterations. Each merge grows the vocabulary by exactly
one new symbol and, at the same time, shortens the sequences that use that pair. The final
vocabulary is the union of every symbol produced this way, from single characters up through the
longest merged units.

将出现频率最高的那一对符号合并成一个新的、单一的符号。接着重复这个“统计相邻对、合并最高频对”的过程，进行固定次数的迭代。每一次合并都恰好为词表新增一个符号，同时也会缩短包含该符号对的序列长度。最终的词表，就是这一过程中产生的所有符号的并集——从单个字符一直到最长的合并单元。

Sennrich et al. (2016) illustrate the algorithm with a small toy vocabulary of word frequencies:
`{'low': 5, 'lower': 2, 'newest': 6, 'widest': 3}`.

Sennrich 等人（2016）用一个小型的示例词表来演示该算法，其中包含单词及其出现频率： `{'low': 5, 'lower': 2, 'newest': 6, 'widest': 3}`。

Written as character sequences with an end-of-word marker `</w>`, this becomes `l o w </w>` (×5), `l
o w e r </w>` (×2), `n e w e s t </w>` (×6), and `w i d e s t </w>` (×3). We can count
adjacent-symbol pairs directly from these frequencies: the pair `(e, s)` occurs in both `newest` and
`widest`, for 6 + 3 = 9 occurrences — tied with `(s, t)`, also 9, and `(t, </w>)`, also 9, all three
driven by the shared suffix "est" that both `newest` and `widest` end in.

如果将其写成带有词尾标记 `</w>` 的字符序列，就得到 `l o w </w>`（出现 5 次）、`l o w e r </w>`（出现 2 次）、`n e w e s t </w>`（出现 6 次）以及 `w i d e s t </w>`（出现 3 次）。我们可以直接根据这些频率来统计相邻符号对：符号对 `(e, s)` 同时出现在 "newest" 和 "widest" 中，共出现 6 + 3 = 9 次——与 `(s, t)`（同样是 9 次）以及 `(t, </w>)`（同样是 9 次）并列最高，这三者都源于 "newest" 与 "widest" 共有的词尾 "est"。

Merging `e` and `s` into a single symbol `es` is one valid first step (any of the three tied top
pairs is a legitimate choice; a real implementation breaks ties by a fixed, deterministic rule such
as iteration order). After that merge, `es` and `t` are now adjacent in both words and together
account for 9 occurrences — the next merge produces `est`.

将 `e` 与 `s` 合并为一个符号 `es` 是一种合理的第一步选择（三个并列最高的符号对中任选一个都是合理的，真实实现通常会按照固定、确定性的规则——例如迭代顺序——来打破平局）。合并之后，`es` 与 `t` 在两个单词中都相邻，合计仍是 9 次出现——下一次合并便产生 `est`。

The pattern that emerges over further merges is exactly the pedagogical point of the example:
because "est" recurs across two otherwise-unrelated words, the algorithm learns it as a reusable
unit, while the less frequent pairs inside `lower` (such as `e` and `r`, appearing only twice)
remain unmerged for longer. This is BPE's central property — frequent, recurring pieces of text earn
their own token; rare pieces get built out of smaller tokens instead.

随着后续合并的展开所呈现出的规律，正是这个示例想要说明的教学要点：由于 "est" 这一片段反复出现在两个原本毫不相关的单词中，算法便会将其学习为一个可复用的单元；而 `lower` 内部出现频率较低的符号对（例如仅出现两次的 `e` 与 `r`）则会在更长时间内保持未合并状态。这正是 BPE 的核心特性——文本中频繁重复出现的片段会获得属于自己的词元，而罕见的片段则会由更小的词元拼接而成。

Modern production tokenizers apply this same idea at the level of raw bytes rather than Unicode
characters, so that any input — including emoji, unusual symbols, or text in any language — can
always be encoded without ever hitting an "unknown character."

现代生产级分词器将同样的思路应用于原始字节层面，而非 Unicode 字符层面，这样任何输入——包括表情符号、罕见符号或任意语言的文本——都总能被编码，而不会出现“未知字符”的情况。

OpenAI's open-source `tiktoken` library, the byte-pair encoding tokenizer used by GPT-family models,
documents this directly: in practice, each token corresponds to roughly 4 bytes of English text on
average.

OpenAI 开源的 `tiktoken` 库，即 GPT 系列模型所使用的字节对编码分词器，其文档中直接指出：在实践中，平均而言每个词元大约对应 4 个字节的英文文本。

This is a genuinely useful rule of thumb for estimating token counts before you have access to the
actual tokenizer, and it also explains a fact worth flagging for a bilingual curriculum: because BPE
vocabularies are built from the statistics of their training corpus, a tokenizer trained mostly on
English-language text tends to represent English prose more token-efficiently, on a per-character
basis, than languages such as Chinese, whose characters carry more information per symbol and were
less frequent in that training corpus — a real, practical consideration when estimating or budgeting
tokens for bilingual or non-English content.

这是一个在你尚未接触实际分词器之前、用于估算词元数量的实用经验法则，同时它也解释了一个对双语课程而言值得特别指出的事实：由于 BPE 词表是根据训练语料的统计特征构建的，一个主要基于英语文本训练的分词器，在按字符计量时，通常会比中文这样“单字符信息密度更高、且在该训练语料中出现频率较低”的语言，更高效地表示英语散文——这是在为双语或非英语内容估算或规划词元预算时，一个真实且实际的考量因素。

---

## 4. What Is a Context Window?

**什么是上下文窗口？**

The **context window** is the maximum number of tokens a model can take into account at once — as
input, as output, or both together, depending on how the provider defines it — when producing a
single response. Anthropic's own developer documentation describes it precisely: "The 'context
window' refers to all the text a language model can reference when generating a response, including
the response itself.

**上下文窗口**是指模型在生成一次回复时，能够同时纳入考量的最大词元数量——具体是仅指输入、仅指输出，还是二者合计，取决于服务提供方的具体定义。 Anthropic 官方开发者文档对此有精确的描述：“'上下文窗口'指的是语言模型在生成一次回复时能够参照的全部文本，包括回复本身在内。

This is different from the large corpus of data the language model was trained on, and instead
represents a 'working memory' for the model." Everything counts toward this budget: the system
prompt, every prior turn of the conversation, any documents or tool definitions supplied, and the
tokens the model itself is about to generate.

这与语言模型训练所用的海量语料库不同，它代表的是模型的'工作记忆'。”计入这一预算的内容包括：系统提示、对话中此前的每一轮交互、所提供的任何文档或工具定义，以及模型即将生成的词元本身。

Context windows vary substantially across models and have grown quickly over the industry's history.

不同模型的上下文窗口大小差异显著，并且在行业发展的历程中增长迅速。

As of this writing, Anthropic's own documentation lists Claude Sonnet 5 and several other current
Claude models as having a 1-million-token context window on the API, while other Claude models,
including Claude Sonnet 4.5, have a 200,000-token context window; OpenAI's documentation lists GPT-4
Turbo's context window as 128,000 tokens. These are large numbers by everyday standards —
Anthropic's documentation notes that 200,000 tokens is roughly equivalent to 500 pages of ordinary
text — but, as [§5](#5-why-context-windows-are-limited-the-cost-of-self-attention) and [§6](#6-more-tokens-is-not-always-better-context-rot) explain, "large" is not the same as "unlimited," and a bigger number does
not automatically mean better results.

截至本文写作时，Anthropic 自身的文档显示，Claude Sonnet 5 及若干其他当前的 Claude 模型在 API 上拥有 100 万词元的上下文窗口，而包括 Claude Sonnet 4.5 在内的其他 Claude 模型则拥有 20 万词元的上下文窗口；OpenAI 的文档则显示 GPT-4 Turbo 的上下文窗口为 12.8 万词元。按日常标准衡量，这些都是相当庞大的数字——Anthropic 的文档指出，20 万词元大致相当于 500 页普通文本——但正如[第 5 节](#5-why-context-windows-are-limited-the-cost-of-self-attention)与[第 6 节](#6-more-tokens-is-not-always-better-context-rot)将要说明的那样，“庞大”并不等同于“无限”，词元数量更大也并不意味着结果自动会更好。

| Model (as documented by its provider)                                    | Context window   |
| ------------------------------------------------------------------------ | ---------------- |
| Claude Sonnet 5 / current Claude models with a 1M window (Anthropic API) | 1,000,000 tokens |
| Claude Sonnet 4.5 (Anthropic API)                                        | 200,000 tokens   |
| GPT-4 Turbo (OpenAI API)                                                 | 128,000 tokens   |

---

## 5. Why Context Windows Are Limited: The Cost of Self-Attention

**上下文窗口为何有限：自注意力机制的代价**

It is natural to ask: why not simply make the context window arbitrarily large? The honest answer
starts with the mechanism [`introductory/02`](/academic-neural-unit-00/curriculum/introductory/02-the-transformer-architecture-and-attention.md) introduces in depth — the **self-attention** mechanism
at the core of the Transformer architecture, from Vaswani et al.'s 2017 paper "Attention Is All You
Need."

一个很自然的问题是：为什么不能简单地把上下文窗口做得无限大呢？坦诚的答案要从 [`introductory/02`](/academic-neural-unit-00/curriculum/introductory/02-the-transformer-architecture-and-attention.md) 深入介绍的机制说起——即 Transformer 架构核心的**自注意力**机制，出自 Vaswani 等人 2017 年发表的论文《Attention Is All You Need》。

Self-attention works by letting every token in the input compare itself against every other token,
to decide how much each one should influence the model's understanding of the others. That "every
token against every other token" comparison is the source of the cost: Vaswani et al.'s own analysis
of computational complexity gives the cost of a self-attention layer as $O(n^2 \cdot d)$, where `n`
is the number of tokens in the sequence and `d` is the size of the internal representation used per
token — growing with the _square_ of the sequence length, not linearly with it.

自注意力机制的运作方式，是让输入中的每一个词元都与其他所有词元进行比较，从而决定每个词元应在多大程度上影响模型对其他词元的理解。正是这种“每个词元都要与其他所有词元比较”的机制，构成了计算代价的根源：Vaswani 等人对计算复杂度的分析给出，一层自注意力的计算代价为 $O(n^2 \cdot d)$，其中 `n` 是序列中的词元数量，`d` 是每个词元所使用的内部表示维度——它随序列长度的**平方** 增长，而非线性增长。

A worked example makes this concrete using only basic arithmetic. Suppose a model processes a
context of 1,000 tokens; the self-attention step involves on the order of 1,000 × 1,000 = 1,000,000
pairwise token comparisons per layer. Double the context to 2,000 tokens, and the comparisons grow
to 2,000 × 2,000 = 4,000,000 — four times as many, not twice as many, for only double the input.

一个仅需基础算术的实例便能让这一点变得具体。假设一个模型处理的上下文包含 1000 个词元，那么自注意力步骤在每一层中所涉及的两两词元比较次数量级约为 1000 × 1000 = 1,000,000 次。若将上下文长度翻倍至 2000 个词元，比较次数则增长为 2000 × 2000 = 4,000,000 次——输入仅仅翻了一倍，比较次数却增长为原来的四倍，而非两倍。

Scale that same reasoning up to a 1-million-token context window, and the pairwise comparison count
reaches 1,000,000 × 1,000,000 = $10^{12}$ per layer, repeated across every layer of the model.

将同样的推理放大到 100 万词元的上下文窗口，每一层的两两比较次数便会达到 1,000,000 × 1,000,000 = $10^{12}$ 次，并且在模型的每一层都会重复出现。

This quadratic growth — not a fixed engineering choice, but a direct mathematical consequence of how
self-attention is defined — is the fundamental reason every context window, no matter how
impressively large, is still finite: the compute and memory required to process it eventually
becomes the limiting resource. (Model providers use substantial engineering effort — some of it
covered later in [`intermediate/02`](/academic-neural-unit-00/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md)'s treatment of the KV-cache — to make long contexts as efficient
as possible in practice, but the underlying quadratic relationship in plain self-attention does not
disappear; it is managed and amortized, not eliminated.)

这种二次方增长——并非某种可以自由调整的工程选择，而是自注意力机制定义方式所带来的直接数学后果——正是每一个上下文窗口，无论表面上看起来多么庞大，终究都是有限的根本原因：处理它所需的计算量与内存量，最终会成为限制性的资源。（模型提供方会投入大量工程努力——其中一部分将在 [`intermediate/02`](/academic-neural-unit-00/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) 关于 KV 缓存的讨论中涉及——来让长上下文在实践中尽可能高效，但纯粹自注意力机制中所固有的二次方关系并不会因此消失；它只是被管理和摊销了，而非被彻底消除。）

---

## 6. More Tokens Is Not Always Better: Context Rot

**词元越多未必越好：上下文衰减**

Even setting the raw compute cost aside, a second and separate finding matters just as much for
anyone building with LLMs: filling a context window to its limit does not guarantee the model uses
all of that information equally well. Anthropic's own developer documentation states this plainly:
"As token count grows, accuracy and recall degrade, a phenomenon known as _context rot_."

即便撇开原始计算成本不谈，还有第二个同样重要、且相互独立的发现，对任何使用大语言模型进行开发的人来说都同样关键：把上下文窗口填满到极限，并不能保证模型会同等有效地利用其中的全部信息。 Anthropic 自身的开发者文档对此有直白的表述：“随着词元数量的增长，准确率与召回率会下降，这一现象被称为'上下文衰减（context rot）'。”

This degradation was studied in detail by Liu et al. (2023) in "Lost in the Middle: How Language
Models Use Long Contexts," which tested models on tasks requiring them to find a specific piece of
information placed somewhere within a long input. The paper's key finding: performance is highest
when the relevant information sits at the very beginning or the very end of the context, and
degrades — sometimes substantially — when the relevant information is buried in the middle, even for
models explicitly designed to handle long contexts.

Liu 等人在 2023 年发表的论文《Lost in the Middle: How Language Models Use Long Contexts》（迷失于中段：语言模型如何使用长上下文）对这一退化现象进行了详细研究，该论文测试了模型在需要从一段较长输入中找出某个特定信息片段这类任务上的表现。论文的核心发现是：当相关信息位于上下文的最开头或最末尾时，模型表现最佳；而当相关信息被埋没在中段时，模型表现会出现退化——有时退化幅度相当可观——即便是那些专门为处理长上下文而设计的模型也不例外。

A 2025 technical report from Chroma, "Context Rot: How Increasing Input Tokens Impacts LLM
Performance" (Hong, Troynikov, and Huber), extended this line of investigation across 18 current
models and found that performance degradation with increasing input length is a broad, consistent
pattern rather than an artifact of any one model or one older architecture, though the exact point
and severity of degradation varies from model to model.

Chroma 公司 2025 年发布的技术报告《Context Rot: How Increasing Input Tokens Impacts LLM Performance》（Hong、Troynikov 与 Huber 合著）将这一研究方向拓展到了 18 个当前模型，发现随着输入长度增加而出现的性能退化，是一种广泛、一致的模式，而非某个单一模型或某种较旧架构的个例，尽管退化出现的具体临界点与严重程度因模型而异。

The practical lesson for this curriculum is not "never use a large context window" — large windows
are genuinely useful and often necessary — but rather that _what_ you put in the context window, and
how it is organized, matters as much as _how much_ you put in. This is precisely the discipline that
[`intermediate/05`](/academic-neural-unit-00/curriculum/intermediate/05-advanced-prompting-cot-few-shot-structured-output.md) (advanced prompting) and [`advanced/05`](/academic-neural-unit-00/curriculum/advanced/05-advanced-context-engineering-long-context-and-budgeting.md) (advanced context engineering) build on:
curating context, not just maximizing it.

对本课程而言，这里得出的实践启示并非“永远不要使用大型上下文窗口”——大型窗口确实有其真实价值，往往也不可或缺——而是：放入上下文窗口中的内容“是什么”、以及它是如何组织的，与放入的内容“有多少”同等重要。这正是 [`intermediate/05`](/academic-neural-unit-00/curriculum/intermediate/05-advanced-prompting-cot-few-shot-structured-output.md)（进阶提示工程）与 [`advanced/05`](/academic-neural-unit-00/curriculum/advanced/05-advanced-context-engineering-long-context-and-budgeting.md)（进阶上下文工程）所建立的核心方法论：精心筛选上下文，而不仅仅是一味地将其填满。

---

## 7. Two Kinds of Memory: Context Window vs. Persistent Memory

**两种记忆：上下文窗口与持久记忆**

A common beginner confusion is treating "the model's memory" as one single thing. It helps to
separate two genuinely different concepts that this curriculum will keep distinct throughout.

初学者常见的一个误区，是把“模型的记忆”当作一个单一整体的概念。将两个确实存在本质区别的概念区分开来会很有帮助，本课程后续也将始终保持这种区分。

| Term                              | EN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | 中文                                                                                                                                                                                                                                                                       |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Working memory**（工作记忆）    | Anthropic's own term, quoted in [§4](#4-what-is-a-context-window) — the context window itself: everything currently loaded into a single request, gone the moment that request finishes unless it is deliberately carried forward into the next one. It is fast, it is exactly as reliable as whatever text is actually inside it, and it is bounded by the limits discussed in [§5](#5-why-context-windows-are-limited-the-cost-of-self-attention) and [§6](#6-more-tokens-is-not-always-better-context-rot). | 这是 Anthropic 官方在第 4 节引用的说法——指的就是上下文窗口本身：当前加载到单次请求中的全部内容，一旦该请求结束，这些内容便会消失，除非被有意地延续到下一次请求中。它速度快，其可靠程度恰好等同于其中实际包含的文本内容，并且受到第 5 节与第 6 节中所讨论的各种限制的约束。 |
| **Persistent memory**（持久记忆） | Sometimes split further into short-term memory that survives a session and long-term memory that survives across sessions entirely — any mechanism that stores information _outside_ the context window and retrieves relevant pieces of it back into the context window only when needed, for a future request.                                                                                                                                                                                               | 有时会被进一步细分为在单次会话内持续存在的短期记忆，以及能够跨越多次会话、长期存续的长期记忆——是指任何将信息存储在上下文窗口“之外”、并且只在未来某次请求真正需要时，才将其中相关的部分重新取回到上下文窗口中的机制。                                                       |

Why does the distinction matter this early in the curriculum? Because it reframes what looks like a
hard ceiling — "the model can only see so much at once" — into a solvable engineering problem:
instead of trying to fit everything into working memory, an agent can store information externally
and pull back only the relevant fragment when it is needed.

为什么这一区分要在课程如此靠前的阶段就提出来？因为它把一个看似坚硬的天花板——“模型一次只能看到这么多”——重新构造成了一个可以通过工程手段解决的问题：与其试图把所有内容都塞进工作记忆，智能体完全可以将信息存储在外部，只在真正需要时才取回其中相关的片段。

That is exactly the idea this curriculum develops next: [`intermediate/04`](/academic-neural-unit-00/curriculum/intermediate/04-agent-memory-systems-short-term-long-term-episodic.md) (agent memory systems)
formalizes short-term, long-term, and episodic memory as engineered components of an agent, and
[`intermediate/06`](/academic-neural-unit-00/curriculum/intermediate/06-rag-fundamentals-retrieval-embeddings-and-grounding.md) (retrieval-augmented generation, also authored as part of this same module pair)
develops the specific mechanism — retrieval — that decides which fragment of persistent memory is
worth pulling back into the context window for a given request. Nothing in this module requires you
to understand those mechanisms yet; the goal here is only to make the vocabulary and the underlying
distinction available before you meet them.

这正是本课程接下来要展开的思路：[`intermediate/04`](/academic-neural-unit-00/curriculum/intermediate/04-agent-memory-systems-short-term-long-term-episodic.md) （智能体记忆系统）将短期记忆、长期记忆与情节记忆形式化为智能体的工程化组件，而 [`intermediate/06`](/academic-neural-unit-00/curriculum/intermediate/06-rag-fundamentals-retrieval-embeddings-and-grounding.md)（检索增强生成，与本模块同为一对由同一作者撰写的模块）则会展开阐述那个具体的机制——检索——用以决定针对某一次特定请求，持久记忆中的哪个片段值得被取回到上下文窗口中。本模块并不要求你此刻就理解这些机制；这里的目标，只是在你真正接触它们之前，先为你准备好相关的词汇与其背后的这一根本区分。

---

## 8. A Worked Example: Managing a Token Budget Across a Conversation

**实例演算：在一段对话中管理词元预算**

Consider a simplified agent with a context window budget of 8,000 tokens, built around a system
prompt of 500 tokens that is present in every request. The user opens with a message of 100 tokens;
the model replies with 300 tokens; that first exchange consumes 500 + 100 + 300 = 900 tokens out of
the 8,000-token budget, leaving 7,100 tokens available. Because Anthropic's own documentation
describes token accumulation as "progressive" — "each user message and assistant response
accumulates within the context window, and previous turns are preserved completely" — every
subsequent turn adds its own tokens on top of everything that came before, rather than replacing it.

设想一个上下文窗口预算为 8000 词元的简化智能体，其系统提示占用 500 词元，且每次请求中都会存在。用户以一条 100 词元的消息开始对话；模型给出 300 词元的回复；这第一轮交互便消耗了 500 + 100 + 300 = 900 个词元，占用 8000 词元预算的一部分，还剩余 7100 词元可用。由于 Anthropic 官方文档将词元的累积过程描述为“渐进式”的——“每一条用户消息与助手回复都会在上下文窗口中不断累积，此前的各轮交互会被完整保留”——因此，之后的每一轮交互都会在此前全部内容的基础上叠加自己的词元数量，而不是将其替换掉。

Suppose the conversation continues for nine more turns, each averaging 700 tokens combined (user
message plus assistant response). After the first turn's 900 tokens, nine more turns at 700 tokens
each add 9 × 700 = 6,300 tokens, for a running total of 900 + 6,300 = 7,200 tokens — still under the
8,000-token budget, but only 800 tokens of headroom remain.

假设对话再继续进行九轮，每轮平均消耗 700 个词元（用户消息与模型回复合计）。在第一轮的 900 词元之后，再加上九轮各 700 词元，即 9 × 700 = 6300 词元，累计总量达到 900 + 6300 = 7200 词元——虽然仍未超出 8000 词元的预算，但剩余的可用空间已仅有 800 词元。

One more turn of typical size would exceed the budget.

再进行一轮典型大小的交互，就会超出预算。

This is precisely the situation Anthropic's documentation describes under "context window overflow
behavior": if input tokens alone already exceed the context window, the API returns an error; if
input plus the requested output would exceed it, current models can still accept the request but
will stop generating once the limit is reached, reporting a specific stop reason rather than
silently continuing. An agent-building engineer has to plan for this before it happens — by
summarizing or truncating older turns, or, as [`intermediate/06`](/academic-neural-unit-00/curriculum/intermediate/06-rag-fundamentals-retrieval-embeddings-and-grounding.md) will develop, by moving information
out of the conversation entirely and retrieving it back only when relevant — rather than discovering
the failure mode in production.

这正是 Anthropic 文档在“上下文窗口溢出行为”一节中所描述的情形：如果仅输入部分的词元数就已经超出上下文窗口，API 会返回错误；如果输入加上请求生成的输出总量会超出窗口，当前的一些模型仍会接受该请求，但一旦达到上限便会停止生成，并报告一个特定的停止原因，而非悄无声息地继续生成下去。构建智能体的工程师必须在这种情况发生之前就做好规划——例如对较早的对话轮次进行摘要或截断，或者如 [`intermediate/06`](/academic-neural-unit-00/curriculum/intermediate/06-rag-fundamentals-retrieval-embeddings-and-grounding.md) 将要展开阐述的那样，把信息彻底移出对话本身，只在真正相关时才将其重新检索回来——而不是等到生产环境中才发现这一失败模式。

---

## 9. Practical Takeaways for Building with LLMs

**面向大语言模型开发的实践要点**

Four practical habits follow directly from this module's material and are worth carrying forward
into every later module.

本模块的内容直接引出了四条实践习惯，值得在后续每一个模块中持续贯彻。

| #   | Habit                             | EN                                                                                                                                                                                                                                                                                                                                                                                                                             | 中文                                                                                                                                                                                                                                                                                                                                                                                                                   |
| --- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Estimate tokens, don't guess**  | use a real tokenizer (such as OpenAI's `tiktoken`) or a provider's token-counting API before assuming a piece of text "should fit."                                                                                                                                                                                                                                                                                            | 在假定某段文本“应该能装得下”之前，先使用真实的分词器（例如 OpenAI 的 `tiktoken`）或服务提供方的词元计数 API 进行核实。                                                                                                                                                                                                                                                                                                 |
| 2   | **Everything counts**             | system prompts, tool definitions, prior conversation turns, and even the model's own internal reasoning (where applicable) all draw from the same token budget, not separate ones.                                                                                                                                                                                                                                             | 系统提示、工具定义、此前的对话轮次，乃至模型自身的内部推理过程（若适用），全部都从同一个词元预算中支取，而非各自独立的预算。                                                                                                                                                                                                                                                                                           |
| 3   | **Placement matters**             | given the "lost in the middle" pattern from [§6](#6-more-tokens-is-not-always-better-context-rot), the most important information in a long context often belongs near the beginning or the end, not buried in the middle.                                                                                                                                                                                                     | 鉴于第 6 节中“迷失于中段”这一模式，长上下文中最重要的信息，往往更适合放在开头或结尾附近，而不是被埋没在中段。                                                                                                                                                                                                                                                                                                          |
| 4   | **Max context ≠ complete answer** | treat "we can just use a 1-million-token window" as a partial answer, not a complete one — [§6](#6-more-tokens-is-not-always-better-context-rot)'s context rot findings mean that curated, well-organized context frequently outperforms maximal context, a theme [`advanced/05`](/academic-neural-unit-00/curriculum/advanced/05-advanced-context-engineering-long-context-and-budgeting.md) returns to in far greater depth. | 把“我们直接用一个百万词元的窗口不就行了”这种想法，当作一个部分正确、而非完整的答案来看待——[第 6 节](#6-more-tokens-is-not-always-better-context-rot)中关于上下文衰减的研究发现意味着，经过精心筛选、组织良好的上下文，往往会胜过一味求“最大化”的上下文，[`advanced/05`](/academic-neural-unit-00/curriculum/advanced/05-advanced-context-engineering-long-context-and-budgeting.md) 将在更深的层次上重新探讨这一主题。 |

---

## 10. Summary

**小结**

A token is the basic unit of text an LLM processes, produced by a subword algorithm such as
byte-pair encoding so that any input, in any language, can always be represented. A context window
is the total token budget — input, output, and everything in between — available for a single
request, and it is fundamentally finite because the self-attention mechanism at the heart of the
Transformer architecture costs $O(n^2 \cdot d)$, growing quadratically with the number of tokens
processed.

词元是大语言模型处理文本的基本单位，由字节对编码等子词算法生成，从而使任意语言的任意输入都总能被表示出来。上下文窗口是单次请求可用的词元总预算——涵盖输入、输出及二者之间的一切内容——它本质上是有限的，因为 Transformer 架构核心的自注意力机制，其计算代价为 $O(n^2 \cdot d)$，会随处理的词元数量呈平方级增长。

A larger context window is not automatically a better one: documented "context rot" and "lost in the
middle" effects mean models use the tokens in front of them unevenly, favoring information near the
start or end of the context. Finally, a model's working memory (its context window) is a
fundamentally different thing from persistent memory systems that store information outside that
window and retrieve it back only when needed — a distinction that sets up both [`intermediate/04`](/academic-neural-unit-00/curriculum/intermediate/04-agent-memory-systems-short-term-long-term-episodic.md)
(agent memory systems) and [`intermediate/06`](/academic-neural-unit-00/curriculum/intermediate/06-rag-fundamentals-retrieval-embeddings-and-grounding.md) (retrieval-augmented generation) in the modules that
follow.

更大的上下文窗口，并不自动意味着更好的效果：已有文献记录的“上下文衰减”与“迷失于中段”现象表明，模型对其眼前的词元的利用是不均衡的，会更偏向位于上下文开头或结尾附近的信息。最后，模型的工作记忆（即其上下文窗口）与那些将信息存储在窗口之外、只在真正需要时才取回的持久记忆系统，本质上是两种不同的事物——这一区分，也为后续模块中的 [`intermediate/04`](/academic-neural-unit-00/curriculum/intermediate/04-agent-memory-systems-short-term-long-term-episodic.md)（智能体记忆系统）与 [`intermediate/06`](/academic-neural-unit-00/curriculum/intermediate/06-rag-fundamentals-retrieval-embeddings-and-grounding.md)（检索增强生成）铺设了基础。

---

## References

**参考文献**

### External Sources

- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762)
- [Neural Machine Translation of Rare Words with Subword Units (Sennrich, Haddow & Birch, 2016)](https://arxiv.org/abs/1508.07909)
- [tiktoken — OpenAI's byte-pair-encoding tokenizer (GitHub)](https://github.com/openai/tiktoken)
- [Lost in the Middle: How Language Models Use Long Contexts (Liu et al., 2023)](https://arxiv.org/abs/2307.03172)
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance (Hong, Troynikov & Huber, Chroma Technical Report, 2025)](https://research.trychroma.com/context-rot)
- [Context windows — Claude Platform Docs (Anthropic)](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [GPT-4 Turbo model details — OpenAI API Docs](https://developers.openai.com/api/docs/models/gpt-4-turbo)

### Internal Cross-References

- [`introductory/01` — Neural Networks & Deep Learning Foundations](/academic-neural-unit-00/curriculum/introductory/01-neural-networks-and-deep-learning-foundations.md)
- [`introductory/02` — The Transformer Architecture & Attention](/academic-neural-unit-00/curriculum/introductory/02-the-transformer-architecture-and-attention.md)
- [`introductory/05` — Prompt Engineering Fundamentals](/academic-neural-unit-00/curriculum/introductory/05-prompt-engineering-fundamentals.md)
- [`intermediate/02` — Attention Deep Dive: Multi-Head Attention, KV-Cache & Positional Encoding](/academic-neural-unit-00/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md)
- [`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory](/academic-neural-unit-00/curriculum/intermediate/04-agent-memory-systems-short-term-long-term-episodic.md)
- [`intermediate/05` — Advanced Prompting: Chain-of-Thought, Few-Shot & Structured Output](/academic-neural-unit-00/curriculum/intermediate/05-advanced-prompting-cot-few-shot-structured-output.md)
- [`intermediate/06` — RAG Fundamentals: Retrieval, Embeddings & Grounding](/academic-neural-unit-00/curriculum/intermediate/06-rag-fundamentals-retrieval-embeddings-and-grounding.md)
- [`advanced/05` — Advanced Context Engineering: Long-Context & Context Budgeting](/academic-neural-unit-00/curriculum/advanced/05-advanced-context-engineering-long-context-and-budgeting.md)
