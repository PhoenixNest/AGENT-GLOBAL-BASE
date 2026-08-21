# RAG Fundamentals: Retrieval, Embeddings & Grounding

**检索增强生成基础：检索、嵌入与事实基础**

| Field   | English                                                          | 中文                                           |
| ------- | ---------------------------------------------------------------- | ---------------------------------------------- |
| Level   | Intermediate                                                     | 中级                                           |
| Cluster | Prompt & Context Engineering                                     | 提示与上下文工程                               |
| Author  | Dr. Rafael Ibarra-Costa, Research Scientist — Generalist, ANU-00 | ANU-00 通才研究科学家 拉斐尔·伊瓦拉-科斯塔博士 |

---

## 0. Where This Module Fits

**本模块的定位**

This module builds strictly on five earlier curriculum modules and introduces no vocabulary beyond
what they establish plus what is defined here for the first time. From
`introductory/01-neural-networks-and-deep-learning-foundations.md` it assumes the reader already
knows what a neural network is, what a parameter is, and the basic idea of a model
transforming numeric input into numeric output. From
`introductory/02-the-transformer-architecture-and-attention.md` it assumes familiarity with the
Transformer architecture and the attention mechanism, since the encoder models that produce
embeddings in this module are built from exactly those components. From
`introductory/05-prompt-engineering-fundamentals.md` it assumes the reader already knows what a
prompt is, and in particular the instruction/context/input-data/output-indicator anatomy of
a well-formed prompt — retrieval, as this module will show, is fundamentally a way of automatically
filling in a prompt's context. From `introductory/06-context-windows-tokens-and-memory-basics.md` —
this same author's own prior module — it assumes the reader already knows what a token and a
context window are, and in particular the distinction that module drew between a model's
working memory (the context window) and persistent memory living outside it. From
`intermediate/04-agent-memory-systems-short-term-long-term-episodic.md` it assumes the reader
already knows, in outline, what a vector database and an embedding are, and in
particular the cosine-similarity-based retrieval-scoring formula worked through in that module's
§5. This module derives cosine similarity from first principles rather than assuming it, but builds
on the reader's prior exposure to the concept. This module does not re-derive any of the material
above; it names the module whenever it leans on it.

本模块严格建立在此前五个课程模块的基础之上，除了这些模块已经确立的词汇，以及本模块首次给出定义的内容之外，不再引入其他任何新词汇。模块
`introductory/01-neural-networks-and-deep-learning-foundations.md` 已经讲解了什么是神经网络、什么是参数，以及“模型将数值输入转换为数值输出”这一基本思想，本模块假定读者已掌握这些概念。模块
`introductory/02-the-transformer-architecture-and-attention.md`
已经讲解了 Transformer 架构与注意力机制，本模块假定读者对此已经熟悉，因为本模块中用以生成嵌入向量的编码器模型，正是由这些组件构建而成的。模块
`introductory/05-prompt-engineering-fundamentals.md`
已经讲解了什么是提示词，特别是“指令、上下文、输入数据、输出指示”这四部分构成的组织良好的提示词结构，本模块假定读者对此已经熟悉——正如本模块将要说明的那样，检索从根本上说，就是一种自动填充提示词“上下文”部分的方式。模块
`introductory/06-context-windows-tokens-and-memory-basics.md`——同样出自本作者之手——已经讲解了什么是词元与上下文窗口，特别是该模块所区分的模型工作记忆（即上下文窗口）与存在于其之外的持久记忆，本模块假定读者已掌握这些概念。模块
`intermediate/04-agent-memory-systems-short-term-long-term-episodic.md`
已经在概要层面讲解了什么是向量数据库与嵌入向量，特别是该模块第 5
节中详细算过的、基于余弦相似度的记忆检索评分公式，本模块假定读者对此已经熟悉。本模块将从第一性原理出发重新推导余弦相似度，而非假定读者已经理解其数学细节，但会建立在读者此前对这一概念的初步接触之上。本模块不会重新推导上述任何内容，而是在依赖它们时明确指出所依赖的模块。

By the end of this module you will be able to: explain what an embedding is and, in outline, how a
neural encoder produces one; compute cosine similarity, dot product, and Euclidean distance by hand
on small numeric examples; explain the difference between sparse retrieval (BM25) and dense
retrieval (embeddings), and compute a BM25 score by hand; describe the architecture Lewis et al.
(2020) named "Retrieval-Augmented Generation," which combines a parametric language model with a
non-parametric retrieval index; explain why exact nearest-neighbor search does not scale to large
corpora and what approximate nearest-neighbor (ANN) search trades away to fix that; walk through a
complete RAG pipeline from document chunking to final generation; and reason about a specific,
well-documented failure mode retrieval systems have with chunked documents, and the technique built
to address it.

学完本模块后，你将能够：解释什么是嵌入向量，并在概要层面说明神经编码器是如何生成它的；在小型数值实例上手工计算余弦相似度、点积与欧几里得距离；解释稀疏检索（BM25）与密集检索（嵌入向量）之间的区别，并手工计算出一个
BM25
分数；描述 Lewis 等人（2020）所命名的“检索增强生成”（Retrieval-Augmented
Generation）架构，该架构将参数化语言模型与非参数化检索索引结合在一起；解释为何精确最近邻搜索无法扩展到大规模语料库，以及近似最近邻搜索为解决这一问题而做出了怎样的取舍；完整走一遍从文档分块到最终生成的
RAG
流水线；并能够就检索系统在处理分块文档时一种具体的、有据可查的失效模式，以及为解决它而设计的技术进行推理。

---

## 1. Why Retrieval-Augmented Generation Exists

**检索增强生成为何存在**

`introductory/06` established that a language model's working memory — its context window — is
finite, and that everything the model can act on during a single call must fit inside that window.
A second, equally important fact follows from how an LLM is trained rather than from the context
window: everything an LLM "knows" beyond what is placed in its prompt was learned once, during
training, and baked into the model's weights as what the field calls parametric knowledge —
knowledge encoded implicitly in the numeric parameters covered in
`introductory/01`, not stored as retrievable, editable text anywhere. Parametric knowledge has two
structural limitations that no amount of clever prompting can fix. First, it has a knowledge
cutoff: the model cannot know about anything that happened after its training data
was collected, because that data simply never entered its weights. Second, it cannot be
selectively updated, corrected, or extended without retraining the whole model — a company's
internal documentation, a user's private files, or a fact that changed yesterday are, by
definition, never part of what any pre-trained model's weights encode.

`introductory/06` 已经指出，语言模型的工作记忆——即其上下文窗口——是有限的，模型在单次调用中能够据以行动的一切，都必须容纳在这个窗口之内。还有另一个同样重要的事实，源自
LLM
的训练方式而非上下文窗口本身：LLM 在提示词之外“知道”的一切，都是在训练过程中一次性习得、并固化进模型权重之中的，业界称之为参数化知识——即隐式编码在 `introductory/01`
中所讲解的那些数值参数之中的知识，而非以某种可检索、可编辑的文本形式存放在任何地方。参数化知识存在两个结构性局限，是任何精妙的提示词技巧都无法弥补的。第一，它存在知识截止日期：模型无法知晓其训练数据收集截止之后发生的任何事情，因为那些数据从未进入过它的权重。第二，它无法被选择性地更新、修正或扩展，除非重新训练整个模型——一家公司的内部文档、某位用户的私人文件，或是昨天才发生变化的某个事实，按定义就从未被编码进任何预训练模型的权重之中。

Anthropic's own developer glossary defines the technique this module is about in terms of exactly
this gap: "Retrieval augmented generation (RAG) is a technique that combines information retrieval
with language model generation to improve the accuracy and relevance of the generated text, and to
better ground the model's response in evidence... This allows the model to access and use
information beyond its training data, reducing the reliance on memorization and improving the
factual accuracy of the generated text." Retrieval-Augmented Generation is the
practice of pairing an LLM with a separate, external, and updatable store of information — a
non-parametric memory, in the sense that this store lives outside the model's
weights as plain retrievable text — and, at the moment a request is made, automatically pulling the
most relevant fragments of that store into the model's context window so that generation can draw
on them. This connects directly to the working-memory-versus-persistent-memory distinction
`introductory/06` introduced: RAG is the specific mechanism that decides which fragment of
persistent memory is worth pulling into working memory, for a given request.

Anthropic 官方的开发者术语表，正是围绕这一缺口来定义本模块所要讲解的这项技术的：“检索增强生成是一种将信息检索与语言模型生成相结合的技术，用以提升生成文本的准确性与相关性，并让模型的回答更好地基于证据（evidence）……这使得模型能够访问和使用训练数据之外的信息，减少对死记硬背式记忆的依赖，从而提高生成文本的事实准确性。”检索增强生成是这样一种实践：将 LLM
与一个独立于模型之外、可持续更新的外部信息存储配对——从这个意义上说，它是一种非参数化记忆，因为这个存储以可检索的普通文本形式存在于模型权重之外——并且在每次请求发起的那一刻，自动将该存储中最相关的片段拉取进模型的上下文窗口，从而使生成过程能够利用这些内容。这与
`introductory/06`
所引入的“工作记忆与持久记忆”这一区分直接相关：RAG
正是那种针对某次具体请求、决定持久记忆中哪个片段值得被拉入工作记忆的具体机制。

The paper that gave this technique its name — Patrick Lewis and eleven co-authors' 2020 paper
"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" — frames the same problem in
almost identical terms from the research side: it proposes "a general-purpose fine-tuning recipe
for retrieval-augmented generation (RAG) — models which combine pre-trained parametric and
non-parametric memory for language generation," motivated by the observation that "pre-trained
models with a differentiable access mechanism to explicit non-parametric memory can overcome"
limitations that purely parametric models face. The rest of this module builds the machinery this
idea requires, piece by piece: how a fragment of text becomes something a computer can compare for
meaning (§2–§3), how the most relevant fragments are found efficiently among millions of candidates
(§4–§7), how the whole system fits together end to end (§8–§9), and what it buys in practice (§10).

首先为这项技术正式命名的论文——Patrick Lewis 与另外十一位合著者于 2020
年发表的论文《面向知识密集型自然语言处理任务的检索增强生成》（"Retrieval-Augmented Generation for
Knowledge-Intensive NLP
Tasks"）——从研究的角度，用几乎完全一致的措辞界定了同一个问题：论文提出了“一种面向检索增强生成的通用微调方案——将预训练的参数化记忆与非参数化记忆相结合，用于语言生成”，其动机在于论文所指出的：“具备可微分方式访问显式非参数化记忆能力的预训练模型，能够克服”纯参数化模型所面临的局限。本模块接下来的内容，将逐一构建这一思想所需要的各项机制：一段文本如何变成计算机可以据以比较语义的对象（第
2 至第 3
节）；如何在数百万个候选片段之中高效地找到最相关的那些（第4至第7节）；整个系统如何端到端地衔接在一起（第8至第9节）；以及它在实践中究竟带来了什么好处（第10节）。

---

## 2. From Words to Vectors: The Idea of an Embedding

**从词语到向量：嵌入的思想**

To retrieve "the most relevant" fragment of text for a query, a computer needs some way to compare
two pieces of text for meaning rather than for exact wording — a user who asks "how do I get my
money back?" should be able to retrieve a document titled "Refund Policy" even though the two share
no words in common. An embedding is the mechanism the field uses to solve exactly
this problem: a fixed-length list of numbers (a vector) produced by a trained neural network from a
piece of text, constructed so that texts with similar meaning are mapped to vectors that are close
together in the resulting numeric space, and texts with different meaning are mapped to vectors
that are far apart. The list of numbers itself carries no obvious human-readable meaning — no single
coordinate corresponds to a clean concept like "is about refunds" — but the geometric relationships
between vectors, which §3 makes precise, do carry meaning that a program can compute with.

要为一次查询检索出“最相关”的文本片段，计算机需要某种方式来比较两段文本在语义上而非措辞上是否相似——一位问“我怎么才能把钱要回来？”的用户，理应能够检索到一份标题为《退款政策》的文档，即便这两段文字之间没有任何一个共同的词。嵌入向量正是该领域为解决这一问题所采用的机制：它是由一个训练好的神经网络从一段文本生成的、固定长度的数字列表（即一个向量），其构造方式使得语义相近的文本会被映射到所生成数值空间中彼此靠近的向量，而语义不同的文本则会被映射到彼此相距较远的向量。这一串数字本身并不携带任何人类可以直观读懂的含义——没有哪一个坐标单独对应着“是否与退款有关”这样一个清晰的概念——但向量之间的几何关系，正如第
3 节将要精确阐明的那样，确实携带着程序可以据以计算的语义信息。

The idea that a neural network could learn such a mapping for individual words, rather than for
whole sentences, was demonstrated at scale by Tomas Mikolov, Kai Chen, Greg Corrado, and Jeffrey
Dean's 2013 paper "Efficient Estimation of Word Representations in Vector Space," which introduced
the word2vec family of models. Word2vec's central, now-famous demonstration is that the learned
vector space captures relationships that behave arithmetically: the vector arithmetic
$\text{vector}(\text{King}) - \text{vector}(\text{Man}) + \text{vector}(\text{Woman})$ lands close to $\text{vector}(\text{Queen})$ in the learned
space, showing that the model had implicitly captured a "royalty" direction and a "gender"
direction as separate, combinable components of meaning, purely from statistics of which words tend
to appear near which other words in a large text corpus — no human ever labeled a "gender axis" for
the model to learn. Word2vec embeds individual words; it says nothing yet about how to embed a
whole sentence or an entire document, which is the more directly useful unit for retrieval and is
covered next.

神经网络能够为单个词语（而非整句话）学习出这样一种映射，这一思想最早由 Tomas Mikolov、Kai
Chen、Greg Corrado 与 Jeffrey Dean 于 2013
年发表的论文《高效估计向量空间中的词表示》（"Efficient Estimation of Word Representations in Vector
Space"）大规模地加以证明，该论文提出了 word2vec
系列模型。word2vec
最核心、如今也最广为人知的示范在于：所习得的向量空间捕捉到了能够以算术方式运作的关系——向量运算
$\text{vector}(\text{King}) - \text{vector}(\text{Man}) + \text{vector}(\text{Woman})$
的结果，在所学到的空间中会落在非常接近 $\text{vector}(\text{Queen})$
的位置，这表明该模型仅仅通过统计一个大型文本语料库中哪些词倾向于出现在哪些词附近，就隐式地学会了将“王室身份”与“性别”作为两个独立、可组合的语义分量捕捉了出来——从未有任何人为这个模型标注过一条“性别轴”供其学习。word2vec
生成的是单个词语的嵌入向量；它本身并未说明如何为一整句话或一整篇文档生成嵌入向量，而这才是检索场景中更直接有用的单位，也是接下来要讲解的内容。

Producing a single, meaning-carrying vector for an entire sentence or passage — rather than one
vector per word — requires the Transformer-based encoder architecture `introductory/02` already
introduced, and Nils Reimers and Iryna Gurevych's 2019 paper "Sentence-BERT: Sentence Embeddings
using Siamese BERT-Networks" is the paper this curriculum grounds that step in. Their key
observation was that BERT-style Transformer encoders (see `introductory/02`) already produce rich
internal representations of a sentence, but that using vanilla BERT to compare sentences for
similarity directly is computationally impractical at scale: finding the most similar pair among a
collection of 10,000 sentences with a standard BERT-based cross-encoder — one that must process
both sentences together, jointly, for every candidate pair — requires roughly 50 million inference
computations. Sentence-BERT instead trains a "siamese" network (two identical copies of the same
encoder, sharing weights, run independently on each sentence) so that each sentence is encoded once
into a single fixed-length vector, entirely independent of any other sentence it might later be
compared against, and similarity between two already-encoded sentences is then a cheap
vector-geometry computation, not a fresh model inference. The paper reports the resulting
efficiency gain concretely: "This reduces the effort for finding the most similar pair from 65
hours with BERT / RoBERTa to about 5 seconds with SBERT, while maintaining the accuracy from BERT."
This encode-once, compare-cheaply property is exactly what makes retrieval over large document
collections computationally feasible, and it is the design this module builds on for the rest of
its treatment of embeddings.

要为一整句话或一整段文本生成一个单一的、承载语义的向量——而不是逐词生成一个向量——需要用到
`introductory/02`
已经介绍过的、基于 Transformer 的编码器架构，而 Nils Reimers 与 Iryna
Gurevych 于 2019 年发表的论文《Sentence-BERT：使用孪生 BERT
网络的句子嵌入》（"Sentence-BERT: Sentence Embeddings using Siamese
BERT-Networks"），正是本课程为这一步骤所依据的文献。他们的核心洞察在于：BERT
风格的 Transformer 编码器（参见 `introductory/02`）本身已经能够为一句话生成丰富的内部表示，但若直接使用原生
BERT
来比较句子之间的相似度，其计算开销在大规模场景下是不切实际的——用标准的基于 BERT
的交叉编码器（即必须把两个句子联合、成对地一同输入模型进行处理）在一个包含 10,000
个句子的集合中找出最相似的一对句子，大约需要 5000 万次推理计算。Sentence-BERT
转而训练一个“孪生”网络（即同一编码器的两个完全相同、共享权重的副本，各自独立地处理一个句子），使得每一句话只需被编码一次，得到一个固定长度的向量，且这一编码过程完全独立于它日后可能要与之比较的任何其他句子；此后，比较两个已编码句子之间的相似度，就只是一次成本低廉的向量几何运算，而非一次全新的模型推理。论文对由此带来的效率提升给出了具体的数字：“这将在
BERT / RoBERTa 上找出最相似句子对所需的工作量，从 65 小时降低到使用 SBERT 约
5
秒，同时保持了与原生 BERT
相当的准确率。”这种“一次编码、低成本比较”的特性，正是使得在大规模文档集合上进行检索在计算上可行的关键所在，本模块后续关于嵌入向量的全部讨论，都建立在这一设计之上。

---

## 3. Measuring Meaning: Cosine Similarity and Other Distance Metrics

**度量语义：余弦相似度与其他距离度量**

Once two pieces of text have each been turned into a vector, "how similar are they in meaning"
becomes a purely geometric question: how similar are two vectors? Three metrics recur throughout
retrieval systems, and it is worth defining all three precisely because they are not
interchangeable.

一旦两段文本各自被转换为一个向量，“它们在语义上有多相似”这个问题，就变成了一个纯粹的几何问题：两个向量究竟有多相似？检索系统中反复出现的度量方式主要有三种，值得逐一给出精确定义，因为它们彼此并不可以随意互换。

| Metric                                                                                 | EN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 中文                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Euclidean distance**（欧几里得距离）$d(a, b) = \sqrt{\sum_i (a_i - b_i)^2}$          | between two vectors `a` and `b`, each with `n` numeric components, is the ordinary straight-line distance formula generalized beyond two or three dimensions. A small Euclidean distance means the two vectors are close together as points in space; it is sensitive to the raw length ("magnitude") of the vectors, not just their direction.                                                                                                                                                                                                                                                                                              | 指两个向量 `a` 与 `b`（各有 `n` 个数值分量）之间的欧几里得距离，是我们熟悉的直线距离公式向二维或三维以外的空间推广而来。欧几里得距离较小，意味着两个向量作为空间中的点彼此靠得很近；它对向量的原始长度（“模长”）很敏感，而不仅仅取决于方向。                                                                                                                                                                                               |
| **Dot product**（点积）$a \cdot b = \sum_i a_i b_i$                                    | of the same two vectors — multiply corresponding components and sum the results — which `intermediate/04` already used in the weighted-sum computation inside a single artificial neuron, and which grows larger both when two vectors point in a more similar direction and when either vector simply has a larger magnitude.                                                                                                                                                                                                                                                                                                               | 是同样这两个向量对应分量两两相乘后求和——`intermediate/04` 在单个人工神经元内部的加权求和计算中已经使用过这一运算；点积的数值会随两个向量方向更相近而增大，也会随任意一个向量本身的模长增大而增大。                                                                                                                                                                                                                                         |
| **Cosine similarity**（余弦相似度）$\cos(a, b) = \dfrac{a \cdot b}{\|a\| \cdot \|b\|}$ | already introduced in `intermediate/04`'s memory-retrieval scoring formula, and defined here from first principles, solves the magnitude-sensitivity problem that both of the metrics above share, by measuring only the angle between two vectors, ignoring their length entirely, where $\|a\| = \sqrt{\sum_i a_i^2}$ is the Euclidean length (norm) of vector `a`. The result always falls in the range [−1, 1]: a value of 1 means the two vectors point in exactly the same direction (maximally similar), 0 means they are perpendicular (unrelated, in this geometric sense), and −1 means they point in exactly opposite directions. | 已经在 `intermediate/04` 的记忆检索评分公式中出现过，此处将从第一性原理出发给出其定义——解决了上述两种度量方式共有的“对模长敏感”这一问题：它只衡量两个向量之间的夹角，而完全忽略其长度，其中 $\|a\| = \sqrt{\sum_i a_i^2}$ 是向量 `a` 的欧几里得长度（即“范数”）。计算结果总是落在 [−1, 1] 区间内：值为 1 意味着两个向量方向完全一致（相似度最高）；值为 0 意味着二者相互垂直（在这一几何意义上互不相关）；值为 −1 意味着二者方向完全相反。 |

This magnitude-independence matters concretely for text retrieval: a long, detailed passage and a
short, terse passage that both discuss the identical topic should not be judged "less similar"
merely because one produced a numerically larger embedding vector than the other, and cosine
similarity is the metric that avoids exactly that distortion.

这种“与模长无关”的特性，对文本检索而言具有具体的实际意义：一段冗长详尽的文字与一段简短精炼的文字，即便二者讨论的是完全相同的主题，也不应仅仅因为其中一段所生成的嵌入向量在数值上更大，就被判定为“相似度较低”，而余弦相似度正是能够避免这种失真的度量方式。

A worked example makes this concrete using a small, illustrative 3-dimensional embedding space —
real sentence embeddings from a model such as Sentence-BERT typically have several hundred
dimensions, and no single dimension corresponds to a clean, human-nameable concept the way the
toy dimensions below do, but the arithmetic mechanism is identical regardless of dimension count.
Suppose a customer-support search system has embedded a user's query, "How do I reset my
password?", as $q = (0.9, 0.1, 0.1)$, and has three candidate passages already embedded: passage
A, "To reset your password, go to Settings and click Reset Password," as $a = (0.85, 0.05, 0.1)$;
passage B, "Our return policy allows returns within 30 days," as $b = (0.05, 0.95, 0.05)$; and
passage C, "Passwords must be at least 12 characters and include a number," as $c = (0.6, 0.1,
0.4)$.

下面用一个小型的、具有示意性的三维嵌入空间给出一个具体的算例——真实的句子嵌入向量（例如由 Sentence-BERT
一类模型生成的）通常有数百个维度，且不存在任何单一维度像下面这个示例中的玩具维度那样对应着某个人类可以清晰命名的概念，但无论维度数量多少，其背后的算术机制是完全一致的。假设某个客服搜索系统已经将用户的查询“我该如何重置密码？”编码为
$q = (0.9, 0.1, 0.1)$，并且已经预先编码了三段候选文本：段落
A，“要重置密码，请前往'设置'并点击'重置密码'”，编码为 $a = (0.85, 0.05,
0.1)$；段落 B，"我们的退货政策允许在 30 天内退货"，编码为 $b = (0.05, 0.95,
0.05)$；段落 C，“密码必须至少 12
个字符，并包含一个数字”，编码为 $c = (0.6, 0.1, 0.4)$。

Computing cosine similarity between the query and each candidate: $\|q\| = \sqrt{0.81+0.01+0.01} \approx
0.910$. For passage A, $q \cdot a = (0.9)(0.85)+(0.1)(0.05)+(0.1)(0.1) = 0.78$, $\|a\| \approx 0.857$, giving
$\cos(q,a) = 0.78 / (0.910 \times 0.857) \approx 0.999$. For passage C, $q \cdot c = (0.9)(0.6)+(0.1)(0.1)+(0.1)(0.4)
= 0.59$, $\|c\| \approx 0.728$, giving $\cos(q,c) = 0.59 / (0.910 \times 0.728) \approx 0.890$. For passage B, $q \cdot b =
(0.9)(0.05)+(0.1)(0.95)+(0.1)(0.05) = 0.145$, $\|b\| \approx 0.953$, giving $\cos(q,b) = 0.145 / (0.910 \times
0.953) \approx 0.167$. Ranking by similarity, passage A (0.999) is the near-exact match, passage C (0.890)
is topically related but answers a different question (password rules, not reset steps), and
passage B (0.167) is essentially unrelated. A retrieval system asked for the single top passage
would correctly surface A; a system asked for the top 2 would surface both A and C — which is
exactly the kind of near-miss result, a relevant-but-wrong-specific-answer passage outranking an
irrelevant one, that later sections' discussion of reranking exists to refine further.

计算查询与三段候选文本之间的余弦相似度：$\|q\| = \sqrt{0.81+0.01+0.01} \approx
0.910$。对于段落
A，$q \cdot a = (0.9)(0.85)+(0.1)(0.05)+(0.1)(0.1) = 0.78$，$\|a\| \approx 0.857$，从而
$\cos(q,a) = 0.78 / (0.910 \times 0.857) \approx 0.999$。对于段落 C，$q \cdot c =
(0.9)(0.6)+(0.1)(0.1)+(0.1)(0.4) = 0.59$，$\|c\| \approx 0.728$，从而 $\cos(q,c) = 0.59 /
(0.910 \times 0.728) \approx 0.890$。对于段落 B，$q \cdot b =
(0.9)(0.05)+(0.1)(0.95)+(0.1)(0.05) = 0.145$，$\|b\| \approx
0.953$，从而 $\cos(q,b) = 0.145 / (0.910 \times 0.953) \approx
0.167$。按相似度排序，段落 A（0.999）几乎是完全匹配；段落 C（0.890）与主题相关，但回答的是另一个问题（密码规则，而非重置步骤）；段落
B（0.167）则基本无关。如果检索系统只被要求返回相似度最高的单一段落，它会正确地返回
A；如果被要求返回前 2
个段落，则会同时返回 A 与 C——这正是一种典型的“擦边”结果：一段“相关但具体答案不对”的文本，排名却高于一段完全无关的文本，而后续章节将要讨论的重排序技术，正是为进一步优化这类结果而存在的。

---

## 4. Sparse Retrieval: TF-IDF and BM25

**稀疏检索：TF-IDF 与 BM25**

Before embeddings were practical at scale, and still very much in production use today alongside
them, information retrieval relied on sparse retrieval: methods that represent a document
as a very long vector with one dimension per unique word in the whole vocabulary — "sparse" because
almost all of those dimensions are zero for any given short document — and score a document against
a query by counting matching words, weighted by how informative each word is. The dominant sparse
scoring algorithm in production search systems is BM25, whose modern, authoritative treatment is
Stephen Robertson and Hugo Zaragoza's 2009 monograph "The
Probabilistic Relevance Framework: BM25 and Beyond," which traces the framework's theoretical
foundations to work by Robertson, Karen Spärck Jones, and collaborators beginning in the 1970s–80s.

在嵌入向量在大规模场景下变得实用之前，信息检索长期依赖稀疏检索（sparse
retrieval）；即便在今天，它依然与嵌入向量并肩活跃于生产系统之中。稀疏检索方法将一篇文档表示为一个维度极高的向量，词表中每一个独立词都占据一个维度——之所以称为“稀疏”，是因为对于任何一篇较短的文档而言，绝大多数维度的取值都是零——并通过统计文档与查询之间匹配词的出现情况、并按每个词的信息量加权，来给文档打分。在生产级搜索系统中占主导地位的稀疏评分算法是
BM25（全称 "Best Matching
25"），其现代、权威的论述见于 Stephen Robertson 与 Hugo Zaragoza 于 2009
年发表的专著《概率相关性框架：BM25 及其延伸》（"The Probabilistic Relevance Framework: BM25 and
Beyond"），该文将这一框架的理论基础追溯至 Robertson、Karen Spärck Jones
及其合作者自二十世纪七八十年代开始的研究工作。

For a query `Q` containing terms $q_1 \ldots q_n$ and a candidate document `D`, the BM25 score is:

对于一个包含词项 $q_1 \ldots q_n$ 的查询 `Q` 与一篇候选文档 `D`，BM25 的评分公式为：

$$
\text{score}(D, Q) = \sum_i \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \dfrac{|D|}{\text{avgdl}}\right)}
$$

$$
\text{IDF}(q_i) = \ln\left(\frac{N - n(q_i) + 0.5}{n(q_i) + 0.5} + 1\right)
$$

where $f(q_i, D)$ is how many times term $q_i$ appears in document `D`; `|D|` is the length of `D` in
words and `avgdl` is the average document length across the whole collection; `N` is the total
number of documents and $n(q_i)$ is how many of them contain term $q_i$ at all; and $k_1$ and `b` are
tunable constants, conventionally $k_1 \in [1.2, 2.0]$ and $b = 0.75$. Two design choices inside this
formula are worth naming explicitly. The $\text{IDF}(q_i)$ term — inverse document frequency —
makes a word that appears in few documents (and is therefore more distinctive) contribute more to
the score than a word that appears in almost every document. The fraction involving $k_1$ implements
term-frequency saturation: as $f(q_i, D)$ grows, its contribution grows more and more slowly rather
than linearly forever, reflecting the intuition that a document mentioning a term 10 times is not
necessarily ten times as relevant as one mentioning it once; the `b`-weighted length-normalization
term inside that same fraction then penalizes documents that are long simply because they are long,
relative to the collection's average length `avgdl`, rather than because they are genuinely more
relevant.

其中，$f(q_i, D)$ 表示词项 $q_i$ 在文档 `D`
中出现的次数；`|D|` 是文档 `D` 的词数长度，`avgdl`
是整个语料库中文档的平均长度；`N`
是文档总数，$n(q_i)$
是包含词项 $q_i$
的文档数量；$k_1$ 与
`b` 是可调常数，通常取 $k_1 \in [1.2, 2.0]$，`b =
0.75`。公式中有两处设计值得专门指出。$\text{IDF}(q_i)$
项——即逆文档频率——使得只在少数文档中出现（因而更具区分度）的词，比几乎在每篇文档中都出现的词对最终得分的贡献更大。涉及
$k_1$ 的这个分式实现的是词频饱和（term-frequency
saturation）：随着 $f(q_i, D)$
的增长，它对得分的贡献增长得越来越慢，而非永远线性增长，这体现了这样一种直觉——一篇文档提及某个词
10 次，未必意味着它就比只提及一次的文档相关十倍；同一分式中带有
`b` 权重的长度归一化项，则会惩罚那些仅仅因为篇幅本身较长（相对于语料库平均长度
`avgdl` 而言）、而非因为内容确实更相关而变长的文档。

A worked example, using $k_1 = 1.5$ and $b = 0.75$, retrieves over a tiny three-document corpus for
the query "password reset." Document D1: "reset your password using the settings page" (7 words).
Document D2: "our return policy allows returns within 30 days" (8 words). Document D3: "password
reset requires email verification and a new password" (9 words, with "password" appearing twice).
$\text{avgdl} = (7+8+9)/3 = 8$; $N = 3$; both query terms appear in D1 and D3 but not D2, so
$n(\text{password}) = n(\text{reset}) = 2$, giving $\text{IDF}(\text{password}) = \text{IDF}(\text{reset}) = \ln\left(\frac{3-2+0.5}{2+0.5}+1\right) =
\ln(1.6) \approx 0.470$ for both terms. For D1, each term has $f = 1$; the length-normalization factor is
$1 - 0.75 + 0.75\times(7/8) \approx 0.906$, giving a denominator of $1 + 1.5\times0.906 \approx 2.359$ per term, so each
term contributes $0.470 \times (2.5/2.359) \approx 0.498$, for a document total of $\approx 0.996$. For D3, "password"
has $f = 2$ and "reset" has $f = 1$; the length-normalization factor is $1 - 0.75 + 0.75\times(9/8) \approx
1.094$, giving denominators of $2 + 1.5\times1.094 \approx 3.641$ and $1 + 1.5\times1.094 \approx 2.641$ respectively, so
"password" contributes $0.470 \times (5/3.641) \approx 0.645$ and "reset" contributes $0.470 \times (2.5/2.641) \approx
0.445$, for a document total of $\approx 1.090$. D2 scores $0$, since it contains neither query term. BM25
therefore ranks D3 (≈1.090) above D1 (≈0.996) above D2 (0) — correctly separating the two documents
that actually discuss password resets from the unrelated returns-policy document, and ranking D3
slightly ahead because its higher raw frequency of "password" outweighs its slightly greater length.

下面用一个算例来说明，取 $k_1 = 1.5$、$b =
0.75$，在一个仅含三篇文档的小型语料库中，针对查询"password
reset"（密码重置）进行检索。文档
D1："reset your password using the settings page"（共 7 个词）。文档 D2："our
return policy allows returns within 30 days"（共 8
个词）。文档 D3："password reset requires email verification and a new
password"（共 9 个词，其中"password"出现两次）。$\text{avgdl} =
(7+8+9)/3 = 8$；$N = 3$；两个查询词均出现在 D1 与 D3
中，但均未出现在 D2 中，因此 $n(\text{password}) = n(\text{reset}) =
2$，两个词的 $\text{IDF}$ 值均为
$\ln\left(\frac{3-2+0.5}{2+0.5}+1\right) = \ln(1.6) \approx 0.470$。对于
D1，两个词的 $f$ 均为
1；长度归一化因子为 $1 - 0.75 + 0.75\times(7/8) \approx
0.906$，每个词对应的分母为
$1 + 1.5\times0.906 \approx
2.359$，因此每个词贡献 $0.470 \times (2.5/2.359) \approx
0.498$，文档总分约为
$0.996$。对于 D3，"password" 的
$f = 2$，"reset" 的
$f = 1$；长度归一化因子为
$1 - 0.75 + 0.75\times(9/8) \approx
1.094$，两个词对应的分母分别为
$2 + 1.5\times1.094 \approx 3.641$ 与
$1 + 1.5\times1.094 \approx
2.641$，因此"password"贡献
$0.470 \times (5/3.641) \approx 0.645$，"reset"贡献
$0.470 \times (2.5/2.641) \approx
0.445$，文档总分约为
$1.090$。D2 得分为 $0$，因为它不含任何一个查询词。由此，BM25
的排序结果为 D3（约
1.090）高于 D1（约
0.996）高于 D2（0）——正确地将两篇真正讨论密码重置的文档，与一篇无关的退货政策文档区分了开来，并且由于
D3 中"password"一词的原始出现频率更高，其得分略高于
D1，超过了因文档略长而受到的轻微惩罚。

BM25's strength and its limitation are the same fact: it matches on literal word overlap (with
stemming and other light normalization typically applied in a real implementation), so it is fast,
requires no training, and is completely transparent about why a document scored the way it did —
but it cannot bridge a vocabulary gap. A query for "how do I get my money back" scores zero against
a document about "refund policy" if the two share no words, exactly the failure case §2 opened with
and exactly the gap dense, embedding-based retrieval closes.

BM25 的优势与局限，其实是同一个事实的两面：它依据字面上的词语重合来匹配（在真实实现中通常还会施加词干还原等轻量归一化处理），因此速度快、无需训练，并且对于一篇文档为何获得这样的分数完全透明可解释——但它无法跨越“用词鸿沟”。一条查询“我怎么才能把钱要回来”，若与一篇关于“退款政策”的文档没有任何共同用词，其得分就会为零，这正是第
2
节开篇所举的那个失败案例，也正是密集的、基于嵌入向量的检索所要弥合的那道鸿沟。

---

## 5. Dense Retrieval: Dual Encoders and Dense Passage Retrieval (DPR)

**密集检索：双编码器与稠密段落检索（DPR）**

Dense retrieval replaces BM25's sparse, mostly-zero word-count vectors with the dense,
every-dimension-meaningful embedding vectors §2 and §3 developed, and finds relevant documents by
cosine similarity or dot product rather than word overlap. Vladimir Karpukhin and seven co-authors'
2020 paper "Dense Passage Retrieval for Open-Domain Question Answering" (DPR) is the paper that
demonstrated this approach could outright beat a strong, well-tuned BM25 baseline rather than merely
complement it, using what the paper calls "a simple dual-encoder framework": one neural encoder
converts the query into a vector, a second, separately-trained encoder converts each candidate
passage into a vector, and both encoders are trained together — on a dataset of question/relevant-
passage pairs — so that a question's vector ends up close, by dot product, to the vector of the
passage that actually answers it. The paper's own headline result: "our dense retriever outperforms
a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval
accuracy" across a range of open-domain QA benchmarks.

密集检索（dense
retrieval）以第 2 节与第 3 节所构建的、每个维度都承载语义的稠密嵌入向量，替代了 BM25
那种大部分维度为零的稀疏词频向量，并通过余弦相似度或点积（而非字面词语重合）来找出相关文档。Vladimir
Karpukhin 与另外七位合著者于 2020 年发表的论文《面向开放域问答的稠密段落检索》（"Dense Passage
Retrieval for Open-Domain Question Answering"，简称
DPR），正是证明这种方法能够彻底超越、而非仅仅补充一个强大且经过良好调优的
BM25 基线的论文，其所采用的是论文中所称的“一个简单的双编码器框架”：一个神经编码器把查询转换为向量，另一个单独训练的编码器把每一段候选文本转换为向量，两个编码器在一个“问题／相关段落”配对数据集上联合训练，使得一个问题的向量最终在点积意义上，与真正能回答该问题的那段文本的向量彼此接近。论文自身给出的核心结果是：“在一系列开放域问答基准测试中，就前
20 篇段落的检索准确率而言，我们的稠密检索器相较于一个强大的
Lucene-BM25 系统，绝对提升幅度普遍达到 9% 到
19%。”

The reason this dual-encoder design matters architecturally, beyond the accuracy gain itself, is
efficiency at retrieval time — the same design property Sentence-BERT exploited in §2. Because the
passage encoder never needs the query at encoding time, every passage in a large document
collection can be encoded exactly once, offline, in advance, and stored; only the query needs to be
encoded at the moment a request arrives, after which finding the closest passage vectors is a
geometry problem over pre-computed vectors, not a fresh pass of the encoder over every candidate
document. This separation — encode the whole corpus once, encode only the query per request — is
precisely what makes dense retrieval computationally viable over millions of documents, and it sets
up the scaling problem §7 addresses next: once millions of passage vectors exist, finding the
closest ones to a query vector by brute-force comparison becomes the new bottleneck.

这种双编码器设计之所以在架构上意义重大，不仅仅在于准确率的提升，更在于检索阶段的效率——这与
Sentence-BERT 在第 2
节中所利用的正是同一种设计特性。由于段落编码器在编码时根本不需要用到查询，一个大型文档集合中的每一段文本都可以离线地、提前地、恰好编码一次并存储下来；只有查询本身需要在请求到达的那一刻才被编码，此后寻找与之最接近的段落向量，就变成了一个在预先计算好的向量之上进行的几何问题，而不再是让编码器对每一篇候选文档重新过一遍。这种“整个语料库只编码一次，每次请求只需编码查询”的分离方式，正是使密集检索在数百万篇文档规模上具备计算可行性的关键所在，也正是引出第
7
节接下来要处理的规模化问题的原因：一旦存在数百万个段落向量，用暴力比较的方式在其中找出与查询向量最接近的那些，本身就会成为新的瓶颈。

---

## 6. The RAG Architecture: Lewis et al.'s Retrieval-Augmented Generation

**RAG 架构：Lewis 等人的检索增强生成模型**

§1 introduced Lewis et al.'s 2020 paper by name; this section describes what the paper actually
built, because "RAG" the general practice and "RAG" the specific named model architecture from that
paper are related but not identical, and a curriculum grounded in verifiable sources should keep
that distinction explicit. The paper's architecture couples two trained components end to end: a
retriever, built on a DPR-style dual-encoder (§5) that returns the top-k most relevant passages
from a large indexed document collection for a given query; and a generator, a sequence-to-sequence
language model (the paper uses BART) that takes both the original query and the retrieved passages
as input and produces the final answer text. Critically, the paper's fine-tuning procedure jointly
trains the query encoder and the generator together end to end — treating the retrieved documents
as a latent variable — while keeping the passage encoder and the document index fixed, so that the
whole system learns, from data, to retrieve passages that actually help the generator produce a
better answer, rather than retrieval and generation being two independently-optimized, disconnected
stages bolted together.

第 1
节已经点名提到了 Lewis 等人 2020
年的论文；本节将说明这篇论文究竟构建了什么，因为作为一种通用实践的"RAG"，与该论文中那个具体命名的模型架构"RAG"，二者相关但并不完全等同，而一部课程建立在可验证来源之上，理应明确保持这一区分。该论文的架构将两个经过训练的组件端到端地耦合在一起：检索器，基于
DPR 风格的双编码器（第 5
节）构建，针对给定查询，从一个已建立索引的大型文档集合中返回相关度最高的前 k
篇段落；以及生成器，一个序列到序列的语言模型（论文中使用的是
BART），它同时接收原始查询与检索到的段落作为输入，并生成最终的答案文本。关键在于，论文的微调流程将查询编码器与生成器端到端地联合训练——把检索到的文档视为一个潜变量——同时保持段落编码器与文档索引固定不变，从而使整个系统能够从数据中学会检索出真正有助于生成器给出更好答案的段落，而不是让检索与生成成为两个各自独立优化、事后拼接在一起、彼此脱节的阶段。

The paper compares two ways of using the retrieved passages inside this joint architecture. In
RAG-Sequence, a single retrieved passage is chosen and used to condition generation of the entire
output sequence, and the final probability is marginalized (summed, weighted by each passage's
relevance) across the top-k retrieved passages considered as alternatives for the whole answer. In
RAG-Token, by contrast, the model is allowed to draw on a different retrieved passage for each
individual output token, marginalizing over passages separately at every generation step — the
paper's own description states this directly: "We compare two RAG formulations, one which
conditions on the same retrieved passages across the whole generated sequence, the other can use
different passages per token." RAG-Token is more flexible (useful when an answer genuinely needs
to synthesize facts from several different passages) at the cost of being more computationally
involved; RAG-Sequence is simpler and often sufficient when one passage contains the whole answer.
Fine-tuned and evaluated on a range of knowledge-intensive NLP tasks, the paper reports that its
models "set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq
models and task-specific retrieve-and-extract architectures" — the paper does not claim RAG beats
every possible baseline on every task, and this module states only that narrower, verified claim
rather than a broader one.

论文比较了在这一联合架构内部使用检索段落的两种方式。在
RAG-Sequence 方案中，系统选定单一一篇检索到的段落，并以其为条件生成整段输出序列，最终的概率是在被视为“整段答案”备选方案的前
k
篇检索段落上做边缘化处理（即按每篇段落的相关度加权求和）。与之相对，在
RAG-Token 方案中，模型被允许在生成每一个输出词元时分别依据不同的检索段落，即在每一个生成步骤上都单独对各篇段落做边缘化处理——论文自身对此有直接的表述：“我们比较了两种
RAG
表述方式，一种在整个生成序列中都以同一批检索到的段落为条件，另一种则可以在每个词元上使用不同的段落。”RAG-Token
更为灵活（当一个答案确实需要综合来自多篇不同段落的事实时尤为有用），但代价是计算过程更为复杂；RAG-Sequence
则更为简单，在单篇段落即足以包含完整答案的情形下往往已经够用。在一系列知识密集型自然语言处理任务上进行微调与评测后，论文报告称其模型“在三个开放域问答任务上取得了当前最优的结果，超过了纯参数化的序列到序列模型以及针对特定任务设计的'检索-抽取'架构”——论文并未声称
RAG 在所有任务上都超越了一切可能的基线方法，本模块也仅陈述这一经过核实的、范围有限的具体结论，而非做出更宽泛的断言。

---

## 7. Searching at Scale: Approximate Nearest Neighbor Search and FAISS

**大规模检索：近似最近邻搜索与 FAISS**

§3's worked example compared a query vector against exactly three candidate passages by hand — an
exact nearest-neighbor search, checking every candidate one by one and keeping the closest. This
approach is correct, but it does not scale: a real document collection for a production RAG system
can easily hold millions of chunks, and comparing a query vector against every single one of them
for every single request quickly becomes computationally prohibitive, echoing the same kind of
scaling concern `introductory/06` raised about self-attention's quadratic cost — a per-query
linear scan over millions of stored vectors, repeated for every incoming query, is exactly the kind
of cost that makes a system unusable in production even though each individual comparison is cheap.

第 3
节的算例，是手工将一个查询向量与恰好三个候选段落逐一比较——这是一种精确最近邻（exact
nearest-neighbor）搜索：逐一检查每一个候选项，并保留距离最近的那个。这种方法是正确的，但无法扩展：一个真实的生产级
RAG 系统所对应的文档集合，很容易就包含数百万个文本块，若每一次请求都要将查询向量与其中的每一个逐一比较，计算开销很快就会变得难以承受，这与
`introductory/06`
所提出的、关于自注意力机制二次方计算代价的规模化担忧遥相呼应——对数百万个已存储向量进行逐一线性扫描，且每一次新请求都要重复这一过程，正是这样一种成本：即便单次比较本身很廉价，累积起来也足以让整个系统在生产环境中变得不可用。

Approximate nearest neighbor search (ANN) solves this by deliberately trading a
small, controllable amount of retrieval accuracy for a large gain in speed: rather than guaranteeing
the mathematically closest vector is always found, an ANN index organizes stored vectors into a
data structure — such as a graph, a tree, or a set of clusters, depending on the specific algorithm
— that lets a search skip the overwhelming majority of vectors that are obviously irrelevant,
checking only a small, promising subset. Jeff Johnson, Matthijs Douze, and Hervé Jégou's 2017 paper
"Billion-scale similarity search with GPUs" introduces FAISS (Facebook AI Similarity Search), one
of the most widely used open-source libraries implementing exactly this idea, reporting a GPU
k-selection design that "operates at up to 55% of theoretical peak performance," and results
demonstrated on collections up to 1 billion vectors, with k-nearest-neighbor graph construction
completed for 95 million high-dimensional image vectors in a matter of hours rather than the far
longer time an unoptimized brute-force search would require at that scale. FAISS and libraries built
on similar principles are what turn dense retrieval (§5) from a technique that works in a paper's
small evaluation set into infrastructure that works over a production-scale document collection.

近似最近邻搜索通过有意用一小部分、可控范围内的检索准确率，换取速度上的大幅提升，来解决这一问题：它不再保证每次都能找到数学意义上最接近的那个向量，而是将已存储的向量组织进某种数据结构之中——具体形式因算法而异，可以是图、树，或一组聚类簇——使搜索过程能够跳过绝大多数明显不相关的向量，只检查一小部分有希望的候选集合。Jeff
Johnson、Matthijs Douze 与 Hervé Jégou 于 2017
年发表的论文《使用 GPU 进行十亿规模的相似度搜索》（"Billion-scale similarity search with
GPUs"），提出了 FAISS（Facebook AI Similarity
Search），这是实现这一思想、使用最广泛的开源库之一；论文报告称其 GPU
上的 k
选择设计“运行效率最高可达理论峰值性能的 55%”，并在多达 10
亿个向量的集合上展示了相关结果——针对 9500 万个高维图像向量的
k
最近邻图构建，仅需数小时即可完成，远短于在同等规模下未经优化的暴力搜索所需的时间。正是
FAISS 及基于类似原理构建的其他库，把密集检索（第 5
节）从一项仅在论文的小型评测集上有效的技术，转变成了能够在生产规模的文档集合上真正运行的基础设施。

---

## 8. The Full RAG Pipeline: Indexing, Retrieval, Augmentation, Generation

**完整的 RAG 流水线：索引、检索、增强与生成**

With embeddings (§2–§3), retrieval algorithms sparse and dense (§4–§6), and scalable search (§7)
all in place, a complete RAG system can be described as four stages, the first performed once
(or periodically) and the remaining three performed for every incoming request.

有了嵌入向量（第 2 至第 3 节）、稀疏与密集检索算法（第 4 至第 6 节），以及可扩展的搜索机制（第 7 节）作为基础，一个完整的 RAG 系统便可以描述为四个阶段：第一个阶段只需执行一次（或定期执行），其余三个阶段则需针对每一次到来的请求分别执行。

| #   | Stage                    | EN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 中文                                                                                                                                                                                                                                                                                                                                                                                                   |
| --- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | **Indexing**（索引化）   | happens offline and in advance: source documents are split into chunks — smaller pieces of text, since a whole document is usually both larger than useful for a single retrieved unit and larger than an embedding model can encode well in one pass — each chunk is passed through an embedding model such as the Sentence-BERT-style encoder from §2 to produce its vector, and the resulting (chunk text, embedding vector) pairs are stored in a vector database, backed by an ANN index such as FAISS (§7) for fast lookup later. | 离线地、提前地进行：源文档被切分为若干文本块——即更小的文本片段，因为一整篇文档通常既过大、不适合作为单次检索的单元，也过大、不利于嵌入模型在一次前向传播中充分编码；每个文本块被送入某个嵌入模型（例如第 2 节中介绍的 Sentence-BERT 风格编码器）以生成其向量，随后所得到的（文本块正文，嵌入向量）配对被存入向量数据库，并由某种如 FAISS（第 7 节）一类的 ANN 索引作为底层支撑，以便后续实现快速查找。 |
| 2   | **Retrieval**（检索）    | happens at request time: the incoming query is embedded with the same (or a matching) encoder used during indexing, and the ANN index returns the top-k chunks whose stored vectors are closest to the query vector by cosine similarity or dot product (§3).                                                                                                                                                                                                                                                                           | 则在请求发生时进行：到来的查询会用与索引化阶段相同（或匹配）的编码器进行编码，随后 ANN 索引会依据余弦相似度或点积（第 3 节），返回其存储向量与查询向量最接近的前 k 个文本块。                                                                                                                                                                                                                          |
| 3   | **Augmentation**（增强） | is the step that connects this module back to `introductory/05`'s anatomy of a prompt: the retrieved chunks are inserted into the model's context window as the context part of a well-formed prompt, typically with the original user query placed alongside them as the instruction and input data, so that the LLM's final call receives both the question and the evidence needed to answer it, all inside one context window as covered in `introductory/06`.                                                                      | 把本模块与 `introductory/05` 中所讲解的提示词构成部分重新联系了起来：检索到的文本块，会被作为一份组织良好的提示词中“上下文”这一部分插入到模型的上下文窗口之中，通常还会将用户原始查询与之并列放置，作为“指令”与“输入数据”，使 LLM 最终这次调用，能够在 `introductory/06` 所讲解的同一个上下文窗口之内，同时收到问题本身以及回答该问题所需的证据。                                                      |
| 4   | **Generation**（生成）   | is the final step, where the LLM produces its answer conditioned on both the query and the retrieved context now sitting in its working memory — mechanically the same generation step covered throughout `introductory/05`, but now grounded, in the sense §10 defines precisely, in retrieved evidence rather than parametric knowledge alone.                                                                                                                                                                                        | 是最后一步，LLM 在此依据当前工作记忆中同时存在的查询与检索到的上下文来生成答案——从机制上说，这与 `introductory/05` 通篇所讲解的生成步骤完全相同，唯一的不同在于，此刻的生成过程已经具备了第 10 节将要精确界定的“事实基础”，即依托于检索到的证据，而非仅仅依赖参数化知识。                                                                                                                              |

Framed this way, the entire RAG pipeline is best understood not as a wholly new mechanism sitting
apart from prompting, but as automated prompt construction: a piece of software, rather than a
human, is deciding what belongs in the context part of the prompt, for every single request.

以这种方式来理解，整条 RAG 流水线，与其说是一种与提示工程完全分离的全新机制，不如说是自动化的提示词构建：是一段软件、而非人类，在为每一次具体请求决定提示词的“上下文”部分应当填入什么内容。

---

## 9. Chunking and the Context-Destruction Problem: Anthropic's Contextual Retrieval

**分块与“上下文破坏”问题：Anthropic 的上下文检索方案**

The chunking step inside indexing (§8) hides a real engineering problem worth naming explicitly,
because it is a common and well-documented cause of retrieval failure in practice. Splitting a
document into independent chunks necessarily strips each chunk of the surrounding context that gave
its content full meaning in the original document — a chunk that reads "revenue grew by 3% over
the previous quarter," taken from the middle of a company's financial filing, says nothing on its
own about which company, or which quarter, it is describing, even though a human reading the whole
filing would never lose that information. A chunk with this problem can fail to be retrieved at all
for a query that should have matched it (because its embedding, computed from impoverished text,
does not resemble a well-formed query embedding closely enough) or, if it is retrieved, can mislead
the generator once it is out of its original context.

索引化流程（第 8
节）中的分块步骤，隐藏着一个值得明确点出的真实工程问题，因为它在实践中是导致检索失败的一个常见且有据可查的原因。将一篇文档切分成一个个相互独立的文本块，必然会剥离掉那些原本赋予其内容完整意义的周边上下文——一个文本块若读作“营收较上一季度增长了
3%”，若取自某公司财报正文中段，单独来看，它根本无法说明这是哪家公司、哪个季度的数据，尽管一个通读整份财报的人绝不会遗漏这些信息。存在这一问题的文本块，可能会在本该被匹配到的查询下完全检索不出来（因为它基于内容贫乏的文本所计算出的嵌入向量，与一个组织良好的查询嵌入向量并不够相似），又或者即便被检索出来，一旦脱离原始语境，也可能误导生成器。

Anthropic's September 2024 engineering post, "Contextual Retrieval," names this failure mode
directly — describing traditional RAG as tending to "destroy context" when documents are split into
chunks — and proposes a fix that stays close to the pipeline already described in §8 rather than
replacing it: before a chunk is embedded (for dense retrieval) or indexed (for BM25-style sparse
retrieval), an LLM (the post uses Claude) is asked to generate a short, 50-to-100-token explanatory
context specific to that chunk — identifying, for instance, which document, section, and topic the
chunk comes from — and this generated context is prepended to the chunk's text before either the
embedding or the BM25 index is built from it, so that both the embedding and the sparse index now
"see" the chunk together with the situating information it was missing. Because this technique
augments a chunk's own text with context rather than depending on any change to the retriever or
generator, it works with both the dense retrieval of §5 and the sparse retrieval of §4 at once, and
the post reports it can be combined with both. The post reports concrete, measured improvements
against a baseline retrieval failure rate of 5.7%: contextual embeddings alone reduced the failure
rate to 3.7% (a 35% relative reduction); combining contextual embeddings with a BM25-style
contextual sparse index reduced it further to 2.9% (a 49% relative reduction); and adding a
reranking step (a second, more expensive relevance-scoring pass applied only to the initial
retrieval's top candidates, developed further in `advanced/06`) on top of both reduced it to 1.9% (a
67% relative reduction).

Anthropic 于 2024 年 9 月发布的工程博客文章《上下文检索》（"Contextual
Retrieval"）直接点名了这一失效模式——将传统 RAG
在把文档切分成文本块时的倾向，描述为会“破坏上下文”——并提出了一种修复方案，该方案并未取代第
8
节已经描述的流水线，而是与之紧密衔接：在某个文本块被用于生成嵌入向量（面向密集检索）或被建立索引（面向
BM25
风格的稀疏检索）之前，先请求一个
LLM（该文章使用的是 Claude）为该文本块生成一段简短的、50 到 100
个词元长度的解释性上下文——例如指明该文本块出自哪份文档、哪个章节、涉及什么主题——并将这段生成出来的上下文，添加在文本块正文之前，再据此构建嵌入向量或
BM25
索引，使得嵌入向量与稀疏索引这两者，此刻都能“看到”该文本块连同它原本所缺失的定位信息。由于这项技术是在文本块自身的文字上增补上下文，而不依赖于对检索器或生成器本身做任何改动，它因而可以同时应用于第
5
节的密集检索与第 4
节的稀疏检索，文章也报告称二者可以结合使用。文章相对于一个 5.7%
的基线检索失败率，给出了具体、经过实测的改进数据：仅使用上下文嵌入，将失败率降低到了
3.7%（相对降幅
35%）；将上下文嵌入与一个 BM25
风格的上下文稀疏索引结合使用，进一步将其降低到了
2.9%（相对降幅
49%）；再在此基础上加入一个重排序步骤（即仅对初次检索得到的头部候选结果，再施加一次成本更高的相关性评分，该主题将在
`advanced/06` 中进一步展开），则将失败率降低到了
1.9%（相对降幅 67%）。

---

## 10. Grounding and Hallucination Reduction

**事实基础与幻觉抑制**

The term "grounding" recurred throughout this module without a precise definition; this section
supplies one. Grounding, in the sense this curriculum uses it, means constraining an
LLM's generated output to be consistent with a specific, checkable piece of evidence presented to
it in context — rather than relying solely on whatever the model happened to encode, unverifiably,
during pretraining. This is precisely the property Anthropic's glossary attributes to RAG: "This
allows the model to access and use information beyond its training data, reducing the reliance on
memorization and improving the factual accuracy of the generated text." Grounding matters because
of hallucination — fluent, confident-sounding output that is factually wrong, a well-known
failure mode of language models operating purely from parametric knowledge, particularly on facts
that are obscure, recent, or specific to a private document the model never saw during training.

“事实基础”一词在本模块中反复出现，却始终没有给出精确的定义；本节将补上这一定义。事实基础，在本课程所使用的意义上，是指将
LLM
生成的输出，约束为与呈现在其上下文中的某一份具体的、可核实的证据保持一致——而不是仅仅依赖模型在预训练阶段无从核实地编码进权重中的那些内容。这正是
Anthropic 官方术语表赋予 RAG
的那种特性：“这使得模型能够访问和使用训练数据之外的信息，减少对死记硬背式记忆的依赖，从而提高生成文本的事实准确性。”事实基础之所以重要，是因为存在幻觉——即那种表达流畅、语气自信，但事实上却是错误的输出，这是纯粹依赖参数化知识运作的语言模型一种广为人知的失效模式，在涉及冷僻、近期，或某份模型在训练时从未见过的私有文档中特有的事实时，尤为突出。

Kurt Shuster, Spencer Poff, Moya Chen, Douwe Kiela, and Jason Weston's 2021 paper "Retrieval
Augmentation Reduces Hallucination in Conversation" studied this connection directly for
conversational agents, examining "neural-retrieval-in-the-loop architectures" for knowledge-
grounded dialogue and reporting that these retrieval-augmented models "substantially reduce" the
well-documented problem of hallucination compared to purely parametric conversational models, while
also generalizing well to topics not seen during the retriever's own training. It is worth stating
this result with the same care the curriculum's citation rule requires: retrieval-augmented
generation reduces hallucination, as a well-documented empirical finding across multiple studies —
it does not eliminate it. A RAG system can still hallucinate if the retriever returns irrelevant or
low-quality passages (the "garbage in" case §9's chunk-context problem exemplifies), if the
generator ignores or misreads the retrieved evidence despite it being correct and relevant, or if
the underlying document collection itself contains errors that are faithfully passed through.
Grounding a claim in retrieved text is a genuine, measurable improvement over ungrounded generation,
not a guarantee of correctness — a distinction this module's own §5–§9 material on retrieval
quality, ranking, and chunk context exists specifically to help an engineer improve.

Kurt Shuster、Spencer Poff、Moya Chen、Douwe Kiela 与 Jason Weston 于 2021
年发表的论文《检索增强能够减少对话中的幻觉》（"Retrieval Augmentation Reduces Hallucination in
Conversation"），针对对话智能体直接研究了这一关联，考察了用于知识落地对话的“检索环路中嵌入神经检索”架构，并报告称，与纯参数化的对话模型相比，这类检索增强模型能够“显著减少”这一广为人知的幻觉问题，同时对检索器自身训练中未曾见过的话题，也具备良好的泛化能力。有必要以本课程引用规则所要求的同等审慎程度，来陈述这一结论：检索增强生成能够减少幻觉，这是多项研究共同证实、有据可查的实证发现——但它并不能彻底消除幻觉。如果检索器返回了不相关或质量低劣的段落（第
9 节中“文本块上下文缺失”问题正是这方面的一个典型案例），或者生成器尽管拿到了正确且相关的检索证据，却对其视而不见或理解有误，又或者底层文档集合本身就含有错误、并被原封不动地传递了下去，RAG
系统依然可能出现幻觉。将某项主张的依据落实在检索到的文本之上，相较于毫无依据的生成，是一项真实的、可测量的改进，但并非正确性的保证——本模块第
5 至第 9
节关于检索质量、排序与文本块上下文的内容，正是为帮助工程师改进这一点而存在的。

---

## 11. Worked Example: An End-to-End RAG Walkthrough

**实例演算：端到端的 RAG 流程**

Bring every stage of §8's pipeline together on a single concrete request, using the customer-
support scenario from §3. During indexing, a company's help-center documentation has already been
split into chunks — including the passages A, B, and C used in §3 — each embedded with a
Sentence-BERT-style encoder (§2), each augmented with a short contextual prefix per §9's Contextual
Retrieval technique (so that, for instance, passage A's stored text actually reads something closer
to "[From: Account Security > Password Help] To reset your password, go to Settings and click Reset
Password," rather than the bare sentence used in §3 for arithmetic simplicity), and all of it stored
in a vector database backed by a FAISS-style ANN index (§7).

把第 8
节流水线的每一个阶段，整合到一次具体的请求之中，沿用第 3
节的客服场景来说明。在索引化阶段，某公司的帮助中心文档已经被切分为若干文本块——其中就包括第
3 节中使用过的段落 A、B、C——每个文本块都用一个 Sentence-BERT
风格的编码器（第 2
节）生成了嵌入向量，并且都按照第 9
节“上下文检索”技术的做法，添加了一段简短的上下文前缀（因此，例如段落
A 实际存储的文本，读起来更接近“【出自：账户安全 > 密码帮助】要重置密码，请前往'设置'并点击'重置密码'”，而不是第 3
节为了便于算术演算而使用的那句裸文本），全部内容都存放在一个由类 FAISS ANN
索引（第 7 节）支撑的向量数据库中。

A user types "How do I reset my password?" into the support chat. Retrieval: the query is embedded
with the same encoder used during indexing, producing the $q = (0.9, 0.1, 0.1)$ vector from §3; the
ANN index efficiently returns the top-2 closest stored chunks without needing to scan the entire
document collection, which §3's arithmetic already showed to be passage A (cosine similarity
≈0.999) and passage C (≈0.890), passage B (≈0.167) correctly excluded as irrelevant. Augmentation:
a piece of software — not a person — assembles a prompt following exactly the anatomy
`introductory/05` defined: an instruction ("Answer the user's question using only the information in
the provided context; if the context does not contain the answer, say so"), the retrieved passages
A and C placed as context, the user's original message placed as input data, and an output
indicator ("respond in two sentences or fewer"). Generation: the LLM receives this assembled prompt
— instruction, context, input, and output indicator all sitting together inside one context window,
exactly as `introductory/06` described token accumulation working — and produces its answer
grounded in passage A's actual reset steps, while passage C's password-length requirement is
available to be mentioned as a secondary detail if relevant, rather than the model needing to
recall (or worse, guess at) either fact from parametric memory alone.

一位用户在客服聊天窗口中输入：“我该如何重置密码？”检索阶段：该查询会用索引化阶段相同的编码器进行编码，生成第
3
节中的向量
$q = (0.9, 0.1, 0.1)$；ANN
索引无需扫描整个文档集合，即可高效地返回相似度最高的前 2
个已存储文本块——第 3
节的算式已经证明，这正是段落 A（余弦相似度约
0.999）与段落 C（约
0.890），而段落 B（约
0.167）被正确地排除在外，视为不相关。增强阶段：一段软件——而非某个人——严格依照
`introductory/05`
所定义的提示词构成，组装出一份提示词：一条指令（“仅使用所提供上下文中的信息来回答用户的问题；如果上下文中不包含答案，请如实说明”）、以检索到的段落
A 与 C
作为上下文、以用户的原始消息作为输入数据，以及一条输出指示（“用不超过两句话作答”）。生成阶段：LLM
接收这份组装完成的提示词——指令、上下文、输入数据与输出指示，全部一同存在于同一个上下文窗口之内，正如
`introductory/06`
所描述的词元累积机制那样——并生成一个以段落 A
中真实的重置步骤为依据的答案，同时段落 C
中关于密码长度的要求，若有相关性，也可以作为一条次要信息一并提及，而无需模型仅凭参数化记忆去回忆（或更糟，去猜测）这两项事实中的任何一项。

---

## 12. Failure Modes and Practical Takeaways

**失效模式与实践要点**

Four practical habits follow directly from this module's material.

本模块的内容直接引出了四条实践习惯。

| #   | Takeaway                                             | EN                                                                                                                                                                                                                                                                                                                                                                                                                                                 | 中文                                                                                                                                                                                                                                                                                                                        |
| --- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Retrieval quality bounds answer quality              | a RAG system's answer quality is bounded above by its retrieval quality: no generator, however capable, can produce a well-grounded answer from passages that were never retrieved in the first place, which is why §7's scalable search and §9's chunk-context fix are not optional engineering polish but load-bearing parts of the pipeline.                                                                                                    | 一个 RAG 系统答案质量的上限，取决于其检索质量：无论生成器能力多强，都无法从一开始就未被检索出来的段落中，生成出一个具备扎实事实基础的答案——这正是为什么第 7 节的可扩展搜索与第 9 节的文本块上下文修复方案，并非可有可无的工程打磨，而是这条流水线中具有支撑作用的关键环节。                                                 |
| 2   | Chunk size is a real trade-off                       | chunk size is a real design decision with a genuine trade-off, not an arbitrary implementation detail: chunks that are too small (as in §9's stripped "revenue grew by 3%" example) lose the surrounding context needed to be retrieved or interpreted correctly, while chunks that are too large dilute a passage's embedding with unrelated content and waste context-window tokens (`introductory/06`) on material irrelevant to any one query. | 文本块大小是一项真实存在、涉及实质取舍的设计决策，而非一个可以随意设定的实现细节：过小的文本块（如第 9 节中被剥离了上下文的“营收增长 3%”示例）会失去被正确检索或正确解读所需的周边信息，而过大的文本块则会用无关内容稀释该段落的嵌入向量，并把上下文窗口（`introductory/06`）中的词元，浪费在与任何具体查询都无关的材料上。 |
| 3   | Sparse and dense retrieval fail differently          | sparse (§4) and dense (§5) retrieval fail on different, complementary kinds of query — sparse retrieval fails on vocabulary mismatch, dense retrieval can fail on queries that hinge on an exact rare term or identifier an embedding model was never trained to weight heavily — which is exactly why §9's Contextual Retrieval findings favor combining both rather than picking one.                                                            | 稀疏检索（第 4 节）与密集检索（第 5 节）会在不同、且相互互补的查询类型上失效——稀疏检索败于用词不匹配，密集检索则可能败于那些高度依赖某个精确的稀有词或标识符的查询，因为嵌入模型从未在训练中学会赋予这类词以足够的权重——这正是第 9 节“上下文检索”的研究结论倾向于将二者结合使用、而非二选一的原因。                         |
| 4   | Grounding reduces but does not guarantee correctness | retrieval augmentation reduces hallucination as a matter of documented evidence (§10) but does not guarantee correctness, so a production RAG system still needs monitoring for retrieval failures, stale or incorrect source documents, and cases where the generator drifts from the retrieved evidence it was given.                                                                                                                            | 检索增强能够减少幻觉，这是有据可查的实证事实（第 10 节），但并不能保证结果正确，因此一个生产级 RAG 系统，依然需要对检索失败、陈旧或错误的源文档，以及生成器偏离其所获得的检索证据这类情形，持续加以监控。                                                                                                                   |

---

## 13. Summary

**小结**

Retrieval-Augmented Generation pairs an LLM's parametric knowledge with an external, updatable,
non-parametric store of information, retrieving the most relevant fragments of that store into the
model's context window for each request rather than relying solely on what was baked into the
model's weights during training. Embeddings — dense, meaning-carrying vectors produced by neural
encoders such as those in the Sentence-BERT lineage — turn "how similar in meaning are these two
texts" into a geometric question answerable by cosine similarity, dot product, or Euclidean
distance. Retrieval itself comes in two complementary families: sparse retrieval (BM25), matching
on literal word overlap weighted by term rarity and document length, and dense retrieval (DPR and
the broader dual-encoder pattern), matching on learned semantic similarity that survives vocabulary
mismatch — with approximate nearest neighbor search, as implemented in libraries such as FAISS,
making dense retrieval computationally viable at the scale of millions of documents. Lewis et al.'s
named RAG architecture couples a retriever and a generator end to end, in two variants
(RAG-Sequence and RAG-Token), and the complete production pipeline — indexing, retrieval,
augmentation, generation — is best understood as automated construction of exactly the kind of
well-formed prompt `introductory/05` introduced. Finally, chunking a document for retrieval risks
destroying the context that gave each chunk its meaning, a documented failure mode Anthropic's
Contextual Retrieval technique addresses with measured, substantial improvements, and while
retrieval augmentation reduces hallucination as a matter of documented evidence, it does not
eliminate it — grounding is a real, measurable improvement over ungrounded generation, not a
guarantee. The next module in this cluster, `advanced/06-rag-at-scale-hybrid-search-reranking-and-
evaluation.md`, builds directly on this one to cover hybrid search combining sparse and dense
retrieval, reranking in more technical depth, and how to rigorously evaluate a RAG system's
performance.

检索增强生成将
LLM 的参数化知识，与一个外部的、可持续更新的非参数化信息存储配对，针对每一次请求，将该存储中最相关的片段检索进模型的上下文窗口，而不再仅仅依赖训练阶段固化进模型权重中的内容。嵌入向量——由
Sentence-BERT
一脉的神经编码器所生成的、稠密且承载语义的向量——把“这两段文本在语义上有多相似”这一问题，转化成了一个可以用余弦相似度、点积或欧几里得距离来回答的几何问题。检索本身分为两大互补的流派：稀疏检索（BM25），依据字面词语重合、并按词的稀有度与文档长度加权来匹配；以及密集检索（DPR
及更广义的双编码器范式），依据习得的语义相似度来匹配，能够跨越用词鸿沟——而如 FAISS
一类库中所实现的近似最近邻搜索，则使密集检索在数百万篇文档的规模下具备了计算上的可行性。Lewis
等人命名的 RAG
架构，将检索器与生成器端到端地耦合在一起，有两种变体（RAG-Sequence 与
RAG-Token）；而完整的生产级流水线——索引、检索、增强、生成——最好被理解为对
`introductory/05`
所引入的那种组织良好的提示词的自动化构建过程。最后，为检索而对文档进行分块，存在破坏“赋予每个文本块以意义”的那层上下文的风险，这是一种有据可查的失效模式，Anthropic
的“上下文检索”技术针对这一问题给出了经过实测、幅度可观的改进；而尽管检索增强能够减少幻觉，这一点已是有据可查的实证事实，它却并不能将幻觉彻底消除——事实基础相较于毫无依据的生成，是一项真实、可测量的改进，而非一种保证。本主题群的下一个模块
`advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`，将直接建立在本模块的基础之上，讲解结合稀疏检索与密集检索的混合搜索、更深层次的重排序技术，以及如何严谨地评估一个
RAG 系统的性能。

---

## References

**参考文献**

### External Sources

- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401)
- [Dense Passage Retrieval for Open-Domain Question Answering (Karpukhin et al., 2020)](https://arxiv.org/abs/2004.04906)
- [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks (Reimers & Gurevych, 2019)](https://arxiv.org/abs/1908.10084)
- [Efficient Estimation of Word Representations in Vector Space (Mikolov et al., 2013)](https://arxiv.org/abs/1301.3781)
- [The Probabilistic Relevance Framework: BM25 and Beyond (Robertson & Zaragoza, 2009)](https://dl.acm.org/doi/abs/10.1561/1500000019)
- [Billion-scale similarity search with GPUs — FAISS (Johnson, Douze & Jégou, 2017)](https://arxiv.org/abs/1702.08734)
- [Retrieval Augmentation Reduces Hallucination in Conversation (Shuster et al., 2021)](https://arxiv.org/abs/2104.07567)
- [Contextual Retrieval — Anthropic Engineering Blog (2024)](https://www.anthropic.com/engineering/contextual-retrieval)
- [Glossary — Claude Platform Docs, entry "RAG (Retrieval augmented generation)" (Anthropic)](https://platform.claude.com/docs/en/about-claude/glossary)

### Internal Cross-References

- [`introductory/01` — Neural Networks & Deep Learning Foundations](../introductory/01-neural-networks-and-deep-learning-foundations.md)
- [`introductory/02` — The Transformer Architecture & Attention](../introductory/02-the-transformer-architecture-and-attention.md)
- [`introductory/05` — Prompt Engineering Fundamentals](../introductory/05-prompt-engineering-fundamentals.md)
- [`introductory/06` — Context Windows, Tokens & Memory Basics](../introductory/06-context-windows-tokens-and-memory-basics.md)
- [`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory](04-agent-memory-systems-short-term-long-term-episodic.md)
- [`advanced/05` — Advanced Context Engineering: Long-Context & Context Budgeting](../advanced/05-advanced-context-engineering-long-context-and-budgeting.md)
- [`advanced/06` — RAG at Scale: Hybrid Search, Reranking & Evaluation](../advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md)
