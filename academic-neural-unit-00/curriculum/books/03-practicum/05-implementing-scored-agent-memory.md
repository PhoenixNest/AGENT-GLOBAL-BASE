# Implementing Scored Agent Memory

**实现带评分的智能体记忆**

| Field   | English                                                                 | 中文                                               |
| ------- | ----------------------------------------------------------------------- | -------------------------------------------------- |
| Level   | Practicum                                                               | 实战                                               |
| Cluster | Hands-On Coding Practicum                                               | 实战编程练习                                       |
| Author  | Dr. Inés Roldán, Research Scientist — Software Engineering / CS, ANU-00 | ANU-00 软件工程与计算机科学研究员 Inés Roldán 博士 |

---

## 0. Where This Module Fits

**本模块的定位**

This module has one prerequisite:
[`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md)
("Agent Memory Systems: Short-Term, Long-Term & Episodic Memory"), and it assumes nothing beyond
what that module already taught. `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory
[`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §5](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)
defined the recency/importance/relevance scoring formula from Park et al.'s 2023 "Generative Agents"
paper, worked a hand-computed example over three candidate memories, and showed by hand that the
memory which was recent, important, _and_ relevant outranked one that was merely more recent. This
module builds the code that computes that ranking, and checks its output against that same
hand-computed example.

本模块只有一个前置模块：[`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md)（《记忆系统：短期记忆、长期记忆与情景记忆》），本模块不假设读者具备该模块之外的任何知识。`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 5 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)已经定义了源自 Park 等人 2023 年“Generative Agents”论文的新近度/重要性/相关性评分公式，并手工推算了一个包含三条候选记忆的算例，用手算方式证明了：一条既新近、又重要、且相关的记忆，其排名会高于一条仅仅更新近的记忆。本模块要构建的，正是计算这一排名的代码，并将其输出与那同一份手算算例进行核对。

That module also introduced CoALA's fuller taxonomy — working, long-term, episodic, semantic, and
procedural memory — in
[`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §2](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#2-a-taxonomy-grounded-in-two-traditions).
This module implements only the piece that taxonomy needs a scoring mechanism for: episodic
retrieval. Working memory ([`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §3](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#3-working-memory-the-context-window-in-action) of
`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory) is just the context window and needs no data structure of its own; semantic and
procedural memory ([`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §6](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#6-semantic-and-procedural-memory-briefly)) reuse the same
retrieval mechanics or are not runtime-retrieved at all. This module writes no application code
outside its own fenced code blocks — everything below lives in this markdown file, exactly as
[`practicum/README.md` §3](https://anu00.dev/curriculum/books/03-practicum/README.md) requires.

那个模块还在[`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 2 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#2-a-taxonomy-grounded-in-two-traditions)中介绍了 CoALA 更完整的分类体系——工作记忆、长期记忆、情景记忆、语义记忆与程序性记忆。本模块只实现该分类体系中真正需要一套评分机制的那一部分：情景记忆检索。工作记忆（`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 3 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#3-working-memory-the-context-window-in-action)）本身就是上下文窗口，无需自己的数据结构；语义记忆与程序性记忆（[`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 6 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#6-semantic-and-procedural-memory-briefly)）要么复用同一套检索机制，要么根本不在运行时被检索。本模块不会在自身的代码围栏之外撰写任何应用代码——以下所有内容都保存在这一份 markdown 文件之中，正如 [`practicum/README.md` 第 3 节](https://anu00.dev/curriculum/books/03-practicum/README.md)所要求的那样。

---

## 1. What We're Building: The Four Moving Parts

**我们要构建什么：四个组成部分**

Reduced to its engineering essentials, `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory
[`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §5](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)'s
scoring formula needs four things built to become runnable code: a **record** (what a single stored
memory looks like — its text, when it was written, when it was last touched, how important it was
rated), a **relevance signal** (a way to compare a query against a memory's meaning, which needs an
embedding of some kind), a set of **scoring functions** (recency's exponential decay, cosine
similarity for relevance, and min-max normalization to combine both fairly with the stored importance
value), and a **store** (the object that holds every record and answers "given this query, right
now, which memories matter most").

从工程角度来看，要让 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 5 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)中的评分公式变成可运行的代码，需要构建四样东西：一份**记录**（单条被存储的记忆是什么样子——它的文本内容、写入时间、最近一次被访问的时间、被评定的重要性），一个**相关性信号**（用于比较查询与某条记忆含义之间关系的方式，这需要某种形式的嵌入向量），一组**评分函数**（新近度的指数衰减、用于相关性的余弦相似度，以及用于将二者与存储的重要性数值公平地组合起来的最小-最大归一化），以及一个**存储库**（持有全部记录，并能够回答“给定这个查询，此时此刻，哪些记忆最重要”这一问题的对象）。

Building a real embedding model is out of scope for a from-scratch practicum module — that is a
whole trained neural network, covered separately in `introductory/01` — Neural Networks & Deep Learning Foundations and `introductory/02` — The Transformer Architecture & Attention. This
module instead builds a small, deterministic, dependency-free embedding stand-in
([§3](#3-step-2-a-deterministic-embedding-stub) below) purely so that the _scoring machinery_ can be
demonstrated end to end offline; [§10](#10-common-pitfalls) is explicit about what that stand-in does
and does not capture.

从零构建一个真实的嵌入模型，超出了本实战模块的范围——那是一整个经过训练的神经网络，已在 `introductory/01` — 神经网络与深度学习基础 与 `introductory/02` — Transformer 架构与注意力机制 中单独讲解过。本模块转而构建一个体积小、确定性、不依赖任何第三方库的嵌入替身（见下方[第 3 节](#3-step-2-a-deterministic-embedding-stub)），其唯一目的是让*评分机制*本身能够被端到端地离线演示；[第 10 节](#10-common-pitfalls)会明确说明这一替身能够体现哪些内容、又无法体现哪些内容。

---

## 2. Step 1 — The Memory Record

**第 2 节：步骤一——记忆记录**

A single stored memory needs exactly the fields `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory
[`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §5](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)'s
formula computes over: its text, the simulated clock time it was created and last accessed (in
hours, matching that module's own units), the importance score it was rated at write time, and the
embedding vector used for relevance comparisons:

一条被存储的记忆，需要恰好具备 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 5 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)公式所要计算的那些字段：它的文本内容、以模拟时钟计量的创建时间与最近一次被访问的时间（以小时为单位，与该模块所用单位一致）、写入时被评定的重要性分数，以及用于相关性比较的嵌入向量：

```python
from dataclasses import dataclass


@dataclass
class MemoryRecord:
    text: str
    created_at_hours: float
    last_accessed_hours: float
    importance: float
    embedding: list[float]
```

**Verification (this block):** mental trace, confirmed against the official Python `dataclasses`
documentation (cited in References, same source already confirmed in `practicum/03` — Building a ReAct Agent From Scratch) for
`@dataclass`'s generated `__init__` semantics; exercised directly by every `MemoryStore.add` call in
the scratch-runs below.

**本代码块的验证方式：** 心算追踪，并对照官方 Python `dataclasses` 文档（见“参考文献”，与 `practicum/03` — 从零构建一个 ReAct 智能体 中已核实的来源相同）核实了 `@dataclass` 所生成 `__init__` 方法的语义；下方各次脚本运行中的每一次 `MemoryStore.add` 调用都直接对其加以验证。

`last_accessed_hours` is tracked separately from `created_at_hours` on purpose: `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory
[`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §5](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)'s
recency formula decays from the time a memory was _last touched_, not from when it was first
written, so a memory that gets retrieved again should have its recency clock reset —
[§6](#6-step-5-the-memorystore-class) below implements that reset explicitly.

`last_accessed_hours` 之所以被刻意与 `created_at_hours` 分开追踪，是因为 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 5 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)的新近度公式，衰减的起点是记忆*最近一次被触及*的时间，而非它最初被写入的时间，因此一条被再次检索到的记忆，其新近度时钟理应被重新归零——下方[第 6 节](#6-step-5-the-memorystore-class)将明确实现这一重置逻辑。

---

## 3. Step 2 — A Deterministic Embedding Stub

**第 3 节：步骤二——确定性嵌入桩**

`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §5](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)
defines relevance as the cosine similarity between two embedding vectors — numeric representations
of text meaning, produced by a separate trained model. This module needs _some_ embedding function
to demonstrate the scoring pipeline, but training or downloading a real one is out of scope; instead
this step builds a small, offline, dependency-free stand-in that turns text into a fixed-size vector
by hashing each word into one of a fixed number of buckets and counting occurrences — a crude
bag-of-words sketch, not real distributional semantics:

`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 5 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)将相关性定义为两个嵌入向量之间的余弦相似度——即由一个独立训练的模型所产出的、用于表示文本含义的数值表示。本模块需要*某种*嵌入函数来演示整套评分流水线，但训练或下载一个真实的嵌入模型超出了本模块的范围；因此，本步骤转而构建一个体积小、可离线运行、且不依赖任何第三方库的替身，它通过将每个单词哈希到固定数量的桶中并统计出现次数，把文本转换为一个固定长度的向量——这是一种粗糙的词袋式草图，而非真正的分布式语义表示：

```python
import hashlib
import re

VOCAB_SIZE = 64


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9_]+", text.lower())


def _bucket(token: str, vocab_size: int) -> int:
    digest = hashlib.md5(token.encode("utf-8")).hexdigest()
    return int(digest, 16) % vocab_size


def toy_embed(text: str) -> list[float]:
    vec = [0.0] * VOCAB_SIZE
    for token in _tokenize(text):
        vec[_bucket(token, VOCAB_SIZE)] += 1.0
    return vec
```

**Verification (this block):** scratch-run, as part of [§9](#9-step-8-a-multi-day-scenario-end-to-end)'s
multi-day scenario below, where `toy_embed` is exercised on real memory text and successfully
produces a relevance signal strong enough to rank a genuinely relevant memory above an irrelevant
one; the `hashlib`/`re` mechanics themselves are Python standard-library behavior, not something
this module claims independently.

**本代码块的验证方式：** 脚本实际运行，作为下方[第 9 节](#9-step-8-a-multi-day-scenario-end-to-end)多日场景的一部分——在该场景中，`toy_embed` 被应用于真实的记忆文本，并成功产出了足够强的相关性信号，使一条真正相关的记忆排名高于一条不相关的记忆；`hashlib`/`re` 本身的行为属于 Python 标准库的既有行为，本模块并未对其另行提出任何独立主张。

Using Python's built-in `hash()` here would have been a natural first instinct and is worth flagging
as a mistake to avoid: CPython randomizes the hash of `str` objects by default, per process, for
security reasons, which would make `toy_embed`'s output — and therefore this whole module's
retrieval rankings — different every time the script runs. `hashlib.md5`, applied explicitly to each
token's UTF-8 bytes, is deterministic across runs and across machines, which is what lets this
module's verification blocks below claim exact, reproducible numbers rather than "approximately."

在这里直接使用 Python 内置的 `hash()` 函数，是一种很自然的第一反应，但值得特别指出这是一个应当避免的错误：出于安全考量，CPython 默认会对 `str` 对象的哈希值按进程进行随机化处理，这将导致 `toy_embed` 的输出——进而导致本模块整套检索排名——在每次运行脚本时都各不相同。而显式地对每个词元的 UTF-8 字节应用 `hashlib.md5`，则能够在不同运行之间、乃至不同机器之间保持确定性，这正是下方本模块验证代码块能够给出精确、可复现数字、而非“大致如此”这类说法的原因。

---

## 4. Step 3 — Recency: Exponential Decay

**第 4 节：步骤三——新近度：指数衰减**

`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §5](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)
states the recency component as exponential decay applied to hours since last access, with a decay
factor of 0.995 per hour (Park et al., 2023). As a formula, for $h$ hours since a memory was last
accessed:

`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 5 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)将新近度分量表述为对“自上次访问以来经过的小时数”施加指数衰减，衰减因子为每小时 0.995（Park et al., 2023）。用公式表示，设 $h$ 为记忆自上次被访问以来经过的小时数：

$$\text{recency}(h) = 0.995^{h}$$

This is a direct, single-line translation of that formula into code:

这只是把这个公式直接、逐行地翻译成代码：

```python
RECENCY_DECAY = 0.995


def recency_score(hours_since_access: float) -> float:
    return RECENCY_DECAY ** hours_since_access
```

**Verification (this block):** scratch-run, checked against `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory
[`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §5](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)'s
own three approximated values from its worked example. Running `recency_score(5.0)`,
`recency_score(2.0)`, and `recency_score(200.0)` and printing them produces:

**本代码块的验证方式：** 脚本实际运行，并对照 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 5 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)自身算例中已给出的三个近似数值进行了核对。运行 `recency_score(5.0)`、`recency_score(2.0)` 与 `recency_score(200.0)` 并打印结果，会得到：

```text
recency(5h)=0.975 recency(2h)=0.990 recency(200h)=0.367
```

which matches, to three decimal places, `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory's own $0.995^5 \approx 0.975$,
$0.995^2 \approx 0.990$, and $0.995^{200} \approx 0.367$ — this code reproduces the earlier module's
own arithmetic exactly, not merely a plausible-looking approximation of it.

这与 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 自身给出的 $0.995^5 \approx 0.975$、$0.995^2 \approx 0.990$ 以及 $0.995^{200} \approx 0.367$ 精确吻合到小数点后三位——这段代码精确复现了前一个模块自身的运算结果，而不仅仅是一个看似合理的近似值。

---

## 5. Step 4 — Relevance: Cosine Similarity From Scratch

**第 5 节：步骤四——相关性：从零实现余弦相似度**

`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §5](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)
defines relevance as the cosine similarity between two embedding vectors — a standard measure of how
closely two vectors point in the same direction, independent of their length. For two vectors $a$
and $b$ of equal dimension:

`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 5 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)将相关性定义为两个嵌入向量之间的余弦相似度——这是衡量两个向量方向相似程度的标准指标，与向量的长度无关。对于两个维度相同的向量 $a$ 与 $b$：

$$\cos(a, b) = \frac{a \cdot b}{\lVert a \rVert \, \lVert b \rVert}$$

where $a \cdot b$ is the dot product and $\lVert a \rVert$ is $a$'s Euclidean norm — the square root
of the sum of its squared components. Written directly with the standard library's `math.sqrt`
(confirmed against the official Python documentation, cited in References) and no third-party
numerical library at all:

其中 $a \cdot b$ 为点积，$\lVert a \rVert$ 为 $a$ 的欧几里得范数——即其各分量平方和的平方根。直接使用标准库中的 `math.sqrt`（已对照官方 Python 文档核实，见“参考文献”）来实现，完全不依赖任何第三方数值计算库：

```python
import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)
```

**Verification (this block):** scratch-run — exercised directly inside
[§9](#9-step-8-a-multi-day-scenario-end-to-end)'s multi-day scenario against real `toy_embed` output
below, and its `norm_a == 0.0` guard is a deliberate defensive check: an all-zero embedding (for
instance, text made entirely of tokens outside what a real embedding model was trained on) would
otherwise divide by zero; returning `0.0` similarity for that case is the same choice a production
embedding library makes, treating "no signal" as "no relevance" rather than crashing retrieval.

**本代码块的验证方式：** 脚本实际运行——在下方[第 9 节](#9-step-8-a-multi-day-scenario-end-to-end)的多日场景中，针对真实的 `toy_embed` 输出直接执行验证；其中 `norm_a == 0.0` 这一防护判断是刻意加入的：一个全零的嵌入向量（例如，某段文本完全由真实嵌入模型训练语料之外的词元构成）若不加处理，将导致除零错误；对这种情形返回 `0.0` 相似度，与生产级嵌入库所采取的做法一致——将“无信号”视为“不相关”，而非直接导致检索崩溃。

---

## 6. Step 5 — Normalizing and Combining the Three Signals

**第 6 节：步骤五——归一化并组合三项信号**

`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §5](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)
states that recency, importance, and relevance are each normalized to the $[0, 1]$ range with
min-max scaling before being summed with equal weights — the same normalization technique
scikit-learn's `MinMaxScaler` implements as a standard preprocessing step (confirmed against its
official documentation, cited in References), applied here by hand across a small list rather than a
full array library:

`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 5 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)指出：新近度、重要性与相关性这三项分量，在按等权重求和之前，均需先通过最小-最大缩放归一化到 $[0, 1]$ 区间——这与 scikit-learn 的 `MinMaxScaler` 作为标准预处理步骤所实现的归一化方法（已对照其官方文档核实，见“参考文献”）完全相同，此处只是手工地将其应用于一个较小的列表，而非借助完整的数组计算库：

$$x_{\text{norm}} = \frac{x - \min(X)}{\max(X) - \min(X)}$$

```python
def min_max_normalize(values: list[float]) -> list[float]:
    lo, hi = min(values), max(values)
    if hi == lo:
        return [1.0 for _ in values]
    return [(v - lo) / (hi - lo) for v in values]
```

**Verification (this block):** scratch-run, both against the worked-example reproduction in
[§7](#7-step-6-verifying-against-intermediates-04-worked-example) and against a dedicated degenerate-input
check: calling `min_max_normalize([4.0, 4.0, 4.0])` produces `[1.0, 1.0, 1.0]` rather than raising a
`ZeroDivisionError`.

**本代码块的验证方式：** 脚本实际运行，既在[第 7 节](#7-step-6-verifying-against-intermediates-04-worked-example)的算例复现中得到验证，也通过一次专门的退化输入检验加以确认：调用 `min_max_normalize([4.0, 4.0, 4.0])` 会得到 `[1.0, 1.0, 1.0]`，而不会抛出 `ZeroDivisionError`。

The `hi == lo` branch is worth explaining rather than treating as an edge-case afterthought: when
every candidate has the _same_ raw value on some axis (all equally recent, say), that axis carries
no discriminating information at all, and dividing by `hi - lo` (which would be zero) is undefined.
Returning `1.0` for every candidate in that case is a deliberate, safe choice — since every candidate
gets the same constant contribution from that axis, it shifts every candidate's total score equally
and therefore cannot change their relative ranking, which is the only property that actually matters
for retrieval.

`hi == lo` 这一分支值得专门加以说明，而不应仅仅被当作一个事后补上的边缘情形来处理：当每一条候选记忆在某个维度上的原始数值*完全相同*时（例如全都同样新近），该维度本身就不携带任何可用于区分的信息，此时用 `hi - lo`（其值将为零）作除数便是未定义的。在这种情况下，对每条候选记忆都返回 `1.0`，是一个刻意做出的安全选择——因为每条候选记忆都会从该维度获得相同的常数贡献，这一贡献会将所有候选记忆的总分同等地平移，因而不会改变它们之间的相对排名，而这恰恰是检索场景中唯一真正重要的性质。

---

## 7. Step 6 — Verifying Against `intermediate/04`'s Worked Example

**第 7 节：步骤六——对照 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 的算例进行验证**

Before assembling a full `MemoryStore`, it is worth checking these three scoring functions directly
against the exact numbers `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory
[`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §5](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)
worked by hand: Memory A (200 hours old, importance 2, relevance 0.30), Memory B (5 hours old,
importance 7, relevance 0.85), and Memory C (2 hours old, importance 3, relevance 0.10) — with the
earlier module's claim that Memory B wins despite Memory C being the most recent of the three:

在组装完整的 `MemoryStore` 之前，值得先直接将这三个评分函数，对照 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 5 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)手算得出的确切数字进行核对：记忆 A（200 小时前，重要性 2，相关性 0.30）、记忆 B（5 小时前，重要性 7，相关性 0.85），以及记忆 C（2 小时前，重要性 3，相关性 0.10）——并核对此前模块所提出的论断：尽管三者之中记忆 C 最为新近，最终胜出的仍是记忆 B：

```python
raw_recency = [recency_score(200.0), recency_score(5.0), recency_score(2.0)]
raw_importance = [2.0, 7.0, 3.0]
raw_relevance = [0.30, 0.85, 0.10]

norm_recency = min_max_normalize(raw_recency)
norm_importance = min_max_normalize(raw_importance)
norm_relevance = min_max_normalize(raw_relevance)

scores = [r + i + v for r, i, v in zip(norm_recency, norm_importance, norm_relevance)]
labels = ["A", "B", "C"]
for label, s in zip(labels, scores):
    print(f"Memory {label}: score={s:.3f}")
ranked = sorted(zip(labels, scores), key=lambda pair: pair[1], reverse=True)
print("Ranking:", ranked)
```

Running this block produces:

运行这段代码，会得到如下输出：

```text
Memory A: score=0.267
Memory B: score=2.976
Memory C: score=1.200
Ranking: [('B', 2.976...), ('C', 1.2), ('A', 0.267...)]
```

**Verification (this block):** scratch-run — executed with `python3` in the course of authoring this
module. Memory B outranks both A and C by a wide margin, and Memory C (most recent, but low
importance and low relevance) outranks Memory A (least recent, and also low on both other axes) —
exactly the ordering `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory [`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §5](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)
described in prose, now reproduced numerically from this module's own implementation rather than
taken on faith.

**本代码块的验证方式：** 脚本实际运行——在撰写本模块期间已用 `python3` 实际执行过。记忆 B 以较大优势胜过 A 与 C 两者；而记忆 C（三者中最新近，但重要性与相关性均较低）则胜过记忆 A（三者中最不新近，且在另外两个维度上同样表现较低）——这正是 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 5 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)用文字描述过的排序结果，如今已由本模块自身的实现以数值方式重新复现出来，而非仅凭信任而接受。

---

## 8. Step 7 — The `MemoryStore` Class

**第 8 节：步骤七——`MemoryStore` 类**

With every scoring function checked individually, they can now be assembled into a store that holds
records, embeds new ones on write, and scores every stored record against a query on read:

在各个评分函数都已单独检验通过之后，现在可以将它们组装成一个存储库：在写入时为新记录生成嵌入向量，并在读取时针对查询为每一条已存储的记录打分：

```python
from dataclasses import dataclass


@dataclass
class ScoredMemory:
    record: MemoryRecord
    recency: float
    importance: float
    relevance: float
    score: float


class MemoryStore:
    def __init__(self, embed_fn=toy_embed):
        self._records: list[MemoryRecord] = []
        self._embed_fn = embed_fn

    def add(self, text: str, importance: float, now_hours: float) -> MemoryRecord:
        record = MemoryRecord(
            text=text,
            created_at_hours=now_hours,
            last_accessed_hours=now_hours,
            importance=importance,
            embedding=self._embed_fn(text),
        )
        self._records.append(record)
        return record

    def retrieve(self, query: str, now_hours: float, top_k: int = 1) -> list[ScoredMemory]:
        if not self._records:
            return []
        query_embedding = self._embed_fn(query)
        raw_recency = [recency_score(now_hours - r.last_accessed_hours) for r in self._records]
        raw_importance = [r.importance for r in self._records]
        raw_relevance = [cosine_similarity(query_embedding, r.embedding) for r in self._records]

        norm_recency = min_max_normalize(raw_recency)
        norm_importance = min_max_normalize(raw_importance)
        norm_relevance = min_max_normalize(raw_relevance)

        scored = []
        for record, rec, imp, rel in zip(self._records, norm_recency, norm_importance, norm_relevance):
            score = rec + imp + rel
            scored.append(ScoredMemory(record=record, recency=rec, importance=imp, relevance=rel, score=score))

        scored.sort(key=lambda s: s.score, reverse=True)
        top = scored[:top_k]
        for s in top:
            s.record.last_accessed_hours = now_hours
        return top
```

**Verification (this block):** scratch-run — exercised end to end in
[§9](#9-step-8-a-multi-day-scenario-end-to-end) below with three real added memories and a real
query.

**本代码块的验证方式：** 脚本实际运行——在下方[第 9 节](#9-step-8-a-multi-day-scenario-end-to-end)中，针对三条真实添加的记忆与一次真实查询进行了端到端验证。

`score = rec + imp + rel` is a direct translation of `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory
[`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §5](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)'s
$\text{score} = \alpha_{\text{recency}} \cdot \text{recency} + \alpha_{\text{importance}} \cdot
\text{importance} + \alpha_{\text{relevance}} \cdot \text{relevance}$ with every $\alpha$ set to 1,
exactly as Park et al.'s own implementation does (Park et al., 2023). The line
`s.record.last_accessed_hours = now_hours` inside the `top` loop is the recency-reset mentioned in
[§2](#2-step-1-the-memory-record): only memories that were actually retrieved have their clock reset,
matching the behavior `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory's formula describes — being retrieved is itself an access,
and a subsequent retrieval should treat that memory as freshly touched.

`score = rec + imp + rel` 正是 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 5 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)中 $\text{score} = \alpha_{\text{recency}} \cdot \text{recency} + \alpha_{\text{importance}} \cdot \text{importance} + \alpha_{\text{relevance}} \cdot \text{relevance}$ 公式、在三个 $\alpha$ 均取 1 时的直接翻译，与 Park 等人自身实现的做法完全一致（Park et al., 2023）。`top` 循环内部的 `s.record.last_accessed_hours = now_hours` 一行，正是[第 2 节](#2-step-1-the-memory-record)中提到的新近度重置逻辑：只有真正被检索到的记忆，其时钟才会被重置，这与 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 公式所描述的行为一致——被检索本身就是一次访问，而后续的检索理应将该条记忆视为刚被触及过。

---

## 9. Step 8 — A Multi-Day Scenario End to End

**第 9 节：步骤八——端到端的多日场景**

`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §8](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#8-worked-example-a-multi-day-coding-assistant)
walked through a coding-assistant agent that, on day one, stores a memory about fixing a
`NoneType` crash with a guard clause, and on day five, when asked to fix a similar bug, retrieves
that memory ahead of an unrelated, low-importance one about indentation preferences. This step runs
that scenario for real, using `toy_embed` for the first time on genuine text rather than the
hand-supplied numbers of [§7](#7-step-6-verifying-against-intermediates-04-worked-example):

`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 8 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#8-worked-example-a-multi-day-coding-assistant)讲述了一个编程助手智能体的场景：第一天，它存储了一条关于用防护判断修复 `NoneType` 崩溃的记忆；第五天，当被要求修复一个类似的缺陷时，它检索到这条记忆，并将其排在了一条无关的、关于缩进偏好的低重要性记忆之前。本步骤将真正运行这一场景，首次让 `toy_embed` 作用于真实文本，而非[第 7 节](#7-step-6-verifying-against-intermediates-04-worked-example)中人工给定的数字：

```python
store = MemoryStore()
store.add("user prefers tabs over spaces for indentation", importance=2.0, now_hours=0.0)
store.add(
    "fixed a NoneType crash in parse_config by adding a guard clause, "
    "user rejected a try/except fix first",
    importance=7.0,
    now_hours=0.0,
)
store.add("the CI pipeline was renamed last quarter", importance=3.0, now_hours=0.0)

results = store.retrieve(
    query="how should I fix this NoneType crash in the config parser",
    now_hours=120.0,
    top_k=3,
)
for r in results:
    print(f"{r.score:.3f}  rec={r.recency:.2f} imp={r.importance:.2f} rel={r.relevance:.2f}  -> {r.record.text[:60]!r}")
```

Running this block produces:

运行这段代码，会得到如下输出：

```text
3.000  rec=1.00 imp=1.00 rel=1.00  -> 'fixed a NoneType crash in parse_config by adding a guard cla'
1.269  rec=1.00 imp=0.20 rel=0.07  -> 'the CI pipeline was renamed last quarter'
1.000  rec=1.00 imp=0.00 rel=0.00  -> 'user prefers tabs over spaces for indentation'
```

**Verification (this block):** scratch-run — executed with `python3` in the course of authoring this
module. The guard-clause memory is retrieved first, matching `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory
[`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §8](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#8-worked-example-a-multi-day-coding-assistant)'s
claim.

**本代码块的验证方式：** 脚本实际运行——在撰写本模块期间已用 `python3` 实际执行过。防护判断相关的记忆被排在检索结果首位，与 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 8 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#8-worked-example-a-multi-day-coding-assistant)所述结论一致。

Every recency value in this output is `1.00` — worth noticing rather than glossing over. All three
memories were added at `now_hours=0.0` and retrieved together at `now_hours=120.0`, so all three
have an _identical_ raw recency value before normalization; [§6](#6-step-5-normalizing-and-combining-the-three-signals)'s
degenerate-case handling (`hi == lo` → every candidate gets `1.0`) is exactly what fires here, and it
is not a bug — with recency tied across all three candidates, the ranking is correctly decided
entirely by importance and relevance, which is what actually distinguishes them in this scenario.
The guard-clause memory wins on both of the remaining axes: its `imp=1.00` reflects that it was
rated the most important of the three (7, versus 3 and 2), and its `rel=1.00` reflects that
`toy_embed`'s crude word-overlap signal picked up shared vocabulary — "crash," "config," "guard" —
between the memory's text and the query text, which the other two memories' text does not share.

这段输出中每一条记忆的新近度都是 `1.00`——这一点值得专门指出，而不应一带而过。三条记忆均在 `now_hours=0.0` 时被添加，并在 `now_hours=120.0` 时被一并检索，因此三者在归一化之前的原始新近度数值*完全相同*；[第 6 节](#6-step-5-normalizing-and-combining-the-three-signals)中针对退化情形的处理逻辑（`hi == lo` → 每条候选记忆均取 `1.0`）正是在此处被触发，这并非一个缺陷——由于三条候选记忆在新近度上完全打平，最终排名完全由重要性与相关性决定，而这恰恰是本场景中真正能够区分它们的因素。防护判断相关的记忆在剩余两个维度上均胜出：其 `imp=1.00` 反映出它在三者中被评为最重要（评分为 7，另两者分别为 3 与 2）；其 `rel=1.00` 则反映出 `toy_embed` 这种粗糙的词汇重合信号，捕捉到了该记忆文本与查询文本之间共享的词汇——“crash”“config”“guard”——而另外两条记忆的文本并不包含这些共享词汇。

---

## 10. Common Pitfalls

**第 10 节：常见陷阱**

`toy_embed` is a bag-of-words hash, not a trained embedding model, and `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory
[`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §7](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#7-failure-modes-what-memory-systems-get-wrong)'s
warning about purely embedding-based relevance retrieving text that is "superficially similar in
wording but substantively irrelevant" applies to it even more sharply than to a real model: two
memories that share common words but discuss unrelated topics ("the guard clause fixed the crash"
versus "the security guard clocked out at 5") would register as more similar under `toy_embed` than
a real semantic embedding would judge them to be, since `toy_embed` has no notion of word meaning at
all — only word identity. A production system replaces `toy_embed` with a real embedding model (a
sentence-transformers model, or a hosted embeddings API) precisely to close this gap, at the cost of
a network call or a loaded model instead of a few lines of hashing.

`toy_embed` 是一种基于哈希的词袋方法，而非一个经过训练的嵌入模型，`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 7 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#7-failure-modes-what-memory-systems-get-wrong)中关于纯嵌入式相关性检索可能“检索出措辞表面相似、但实质上毫不相关”的警示，套用在它身上甚至比套用在真实模型上更为尖锐：两条恰好共享常见词汇、但讨论主题完全无关的记忆（例如“防护判断修复了这次崩溃”与“保安在 5 点打卡下班”），在 `toy_embed` 之下会被判定为比真实语义嵌入模型所判定的更为相似，因为 `toy_embed` 完全不具备任何词义概念——它只能识别词形是否相同。生产系统会用一个真实的嵌入模型（例如某个 sentence-transformers 模型，或一个托管的嵌入 API）来替换 `toy_embed`，正是为了弥补这一差距，其代价则是需要一次网络调用或加载一个模型，而不再只是寥寥几行哈希代码。

A second pitfall sits in `retrieve`'s recency-reset behavior itself: because a retrieved memory's
`last_accessed_hours` is bumped forward to `now_hours` every time it is retrieved, a memory that is
frequently but shallowly relevant to many queries (a broad, generic fact) will keep resetting its
own recency clock and can crowd out a more specific, more valuable memory that simply has not been
queried recently — the exact same "stale versus frequently-refreshed" trade-off
`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory [`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §7](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#7-failure-modes-what-memory-systems-get-wrong)
names as a reason every production memory system needs monitoring and a way to correct a memory that
turns out to be systematically over- or under-retrieved.

第二个陷阱则出在 `retrieve` 本身的新近度重置行为之中：由于一条被检索到的记忆，其 `last_accessed_hours` 每次被检索时都会被推进到 `now_hours`，一条与许多查询都存在浅层相关、但本身价值有限的记忆（一条宽泛、笼统的事实）便会不断重置自身的新近度时钟，从而可能挤占一条本身更具体、更有价值、只是最近恰好没有被查询过的记忆——这正是 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 7 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#7-failure-modes-what-memory-systems-get-wrong)所指出的“陈旧记忆与被频繁刷新记忆”之间的权衡，也正是每一个生产级记忆系统都需要监控机制、以及在某条记忆被系统性地过度或不足检索时加以纠正的机制的原因。

---

## 11. Summary and What Comes Next

**第 11 节：小结与后续内容**

This module built the scored episodic-retrieval mechanism `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory
[`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §5](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)
developed in theory: a memory record, a deterministic embedding stand-in, recency and relevance
scoring functions checked directly against that module's own hand-computed numbers, a normalization
step with an explicit degenerate-case guard, and a `MemoryStore` verified end to end against the
multi-day coding-assistant scenario from `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory
[`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory §8](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#8-worked-example-a-multi-day-coding-assistant).

本模块构建了 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 5 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#5-episodic-memory-remembering-specific-experiences)在理论层面所阐述的评分式情景记忆检索机制：一份记忆记录、一个确定性的嵌入替身、直接对照该模块自身手算数字加以检验的新近度与相关性评分函数、一个带有显式退化情形保护的归一化步骤，以及一个已针对 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 [`intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 第 8 节](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md#8-worked-example-a-multi-day-coding-assistant)多日编程助手场景完成端到端验证的 `MemoryStore`。

`practicum/03-building-a-react-agent-from-scratch.md`, by the same author, builds the ReAct agent
loop this memory store is meant to be retrieved _into_ — this module's `MemoryStore.retrieve` output
is exactly the kind of content that belongs in the `Observation:` line, or the system prompt, of the
loop that module constructs. `practicum/04-building-a-minimal-rag-pipeline.md` develops the
retrieval mechanics this module's `toy_embed` deliberately simplified, with a real embedding model
in place of a hash. `advanced/03-agent-harness-engineering-production-grade-agent-loops.md` covers
where memory management fits alongside tool execution, error handling, and observability in a full
production harness.

同一作者撰写的 `practicum/03-building-a-react-agent-from-scratch.md`，构建了本记忆存储库理应被检索并*纳入*的那个 ReAct 智能体循环——本模块 `MemoryStore.retrieve` 的输出，正是该模块循环中 `Observation:` 行、或系统提示词中应当纳入的那类内容。`practicum/04-building-a-minimal-rag-pipeline.md` 将进一步发展本模块中 `toy_embed` 刻意简化掉的检索机制，用一个真实的嵌入模型取代哈希方法。`advanced/03-agent-harness-engineering-production-grade-agent-loops.md` 则会讲解：在一套完整的生产级运行框架中，记忆管理如何与工具执行、错误处理及可观测性共同构成整体。

---

## References

**参考文献**

### External Sources

- [Park, J. S., O'Brien, J., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)
- [Sumers, T. R., Yao, S., Narasimhan, K., & Griffiths, T. L. (2023/2024). Cognitive Architectures for Language Agents (CoALA)](https://arxiv.org/abs/2309.02427)
- [Python Software Foundation. `dataclasses` — Data Classes](https://docs.python.org/3/library/dataclasses.html)
- [Python Software Foundation. `math` — Mathematical functions](https://docs.python.org/3/library/math.html)
- [scikit-learn developers. `sklearn.preprocessing.MinMaxScaler`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html)

### Internal Cross-References

- [`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md)
- [`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md)
- [`introductory/01` — Neural Networks & Deep Learning Foundations](https://anu00.dev/curriculum/books/01-introductory/01-neural-networks-and-deep-learning-foundations.md)
- [`introductory/02` — The Transformer Architecture & Attention](https://anu00.dev/curriculum/books/01-introductory/02-the-transformer-architecture-and-attention.md)
- [`advanced/03` — Agent Harness Engineering: Building Production-Grade Agent Loops](https://anu00.dev/curriculum/books/04-advanced/03-agent-harness-engineering-production-grade-agent-loops.md)
- [`practicum/03` — Building a ReAct Agent From Scratch](https://anu00.dev/curriculum/books/03-practicum/03-building-a-react-agent-from-scratch.md)
- [`practicum/04` — Building a Minimal RAG Pipeline](https://anu00.dev/curriculum/books/03-practicum/04-building-a-minimal-rag-pipeline.md)
