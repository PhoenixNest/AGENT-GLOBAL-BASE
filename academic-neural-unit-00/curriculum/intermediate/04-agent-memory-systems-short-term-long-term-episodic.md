# Agent Memory Systems: Short-Term, Long-Term & Episodic Memory

**记忆系统：短期记忆、长期记忆与情景记忆**

| Field   | English                                                                               | 中文                                               |
| ------- | ------------------------------------------------------------------------------------- | -------------------------------------------------- |
| Level   | Intermediate                                                                          | 中级                                               |
| Cluster | Agent Architecture & Design Patterns                                                  | 智能体架构与设计模式                               |
| Author  | Dr. Inés Roldán, Research Scientist — Software Engineering / Computer Science, ANU-00 | ANU-00 软件工程与计算机科学研究员 Inés Roldán 博士 |

---

## 0. Where This Module Fits

**本模块的定位**

This module builds strictly on four earlier curriculum modules and assumes nothing beyond them.
From `introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md` it assumes the reader
already knows what an AI agent is and understands the basic agent loop —
the perceive-think-act cycle in which a large language model (LLM) receives an observation, reasons
about it, and chooses an action. From `introductory/04-tool-use-and-function-calling-basics.md` it
assumes familiarity with tool use and function calling — the mechanism by which
an agent invokes external code rather than only generating text. From
`introductory/06-context-windows-tokens-and-memory-basics.md` it assumes the reader already knows
what a token is, what a context window is, and the basic fact that everything an
LLM "knows" during a single call is confined to the text inside that window. From
`intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md` it assumes familiarity with
the ReAct, Plan-and-Execute, and Reflexion agent design patterns, and in particular that Reflexion
already introduced the idea of an agent storing self-generated feedback across attempts. This
module does not re-derive any of that material; it names the module whenever it leans on it.

本模块严格建立在此前四个课程模块的基础之上，不假设读者具备这些模块之外的任何知识。模块
`introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md`
已经讲解了什么是人工智能智能体，并介绍了基本的智能体循环——即大语言模型接收观察、进行推理、选择行动的“感知-思考-行动”循环，本模块假定读者已掌握这一概念。模块
`introductory/04-tool-use-and-function-calling-basics.md`
已经讲解了工具使用与函数调用——即智能体调用外部代码而非仅仅生成文本的机制，本模块假定读者对此已经熟悉。模块
`introductory/06-context-windows-tokens-and-memory-basics.md`
已经讲解了什么是词元、什么是上下文窗口，以及一个基本事实：LLM 在单次调用中“知道”的一切都局限于该窗口内的文本，本模块假定读者已掌握这些概念。模块
`intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md`
已经讲解了 ReAct、Plan-and-Execute 与 Reflexion
三种智能体设计模式，其中 Reflexion 已经引入了智能体在多次尝试之间存储自我生成反馈的思路，本模块假定读者对此已经熟悉。本模块不会重新推导上述任何内容，而是在依赖它们时明确指出所依赖的模块。

---

## 1. Why an Agent Loop Alone Is Not Enough

**为什么仅有智能体循环还不够**

The agent loop covered in `introductory/03` describes how a single episode of agent behavior
unfolds: observe, think, act, observe again. But it says nothing about what happens between
episodes, or about what happens when a single episode's history grows larger than the context
window can hold. A customer-support agent that helped a user yesterday and helps the same user
again today has, from the bare agent-loop description alone, no way to know that yesterday
happened at all — each new call to the LLM starts from whatever text is placed in the prompt, and
nothing more. Memory systems are the software and architectural mechanisms that decide
what a past episode leaves behind, where it is stored, and how it is brought back into a future
context window when it is needed.

`introductory/03`
中介绍的智能体循环描述了单次智能体行为片段的展开方式：观察、思考、行动、再观察。但它并未说明片段之间发生了什么，也未说明当单次片段的历史记录增长到超出上下文窗口容量时会发生什么。一个昨天帮助过某位用户、今天又要为同一用户提供服务的客服智能体，仅凭裸的智能体循环描述本身，完全无法知道“昨天”曾经发生过——每一次对
LLM
的新调用都只能从提示词中放入的文本开始，仅此而已。记忆系统正是决定一段过去的片段会留下什么、存放在何处、以及在需要时如何被重新带回未来上下文窗口中的软件与架构机制。

This gap matters for a concrete reason grounded in `introductory/06`: the context window is
finite, measured in tokens, and every token spent on history is a token unavailable for the
current task. An agent that simply appended its entire conversation history forever would
eventually exceed the window and fail outright, and even before that point, a long unstructured
history degrades an LLM's ability to attend to the most relevant parts of it. Memory systems exist
to solve this problem deliberately rather than by accident: they decide, on purpose, what to keep
in the fast but small working set, what to push out to slower but effectively unlimited storage,
and what to bring back and when.

这一缺口之所以重要，有一个源自 `introductory/06`
的具体原因：上下文窗口是有限的，以词元计量，而花在历史记录上的每一个词元，都是当前任务无法使用的词元。一个只会把整段对话历史无限追加下去的智能体，最终会超出窗口限制而彻底失败；而在达到这一极限之前，过长且缺乏结构的历史记录也会削弱
LLM
关注其中最相关部分的能力。记忆系统的存在，正是为了有意识地、而非偶然地解决这一问题：它们有目的地决定哪些内容应保留在快速但容量有限的工作集中，哪些内容应转移到速度较慢但容量近乎无限的存储中，以及在何时、以何种方式将其重新调取回来。

---

## 2. A Taxonomy Grounded in Two Traditions

**扎根于两大传统的分类体系**

The vocabulary "short-term," "long-term," and "episodic" memory did not originate in agent
engineering — it was borrowed from cognitive psychology, and understanding that origin sharpens
the technical definitions used later in this module. Richard Atkinson and Richard Shiffrin's 1968
multi-store model of human memory proposed that memory is not one system but three: a sensory
register, a short-term store (also called working memory) that holds a small amount of information
actively in use, and a long-term store that holds a much larger amount of information for a much
longer duration, with attention and rehearsal acting as the control processes that move
information between them. Four years later, Endel Tulving's 1972 chapter "Episodic and Semantic
Memory" refined the long-term side of that picture by distinguishing episodic memory —
memory for specific, temporally and spatially situated personal events — from semantic memory
— the general, decontextualized knowledge (facts, concepts, word meanings) that a mind
also stores but that is not tied to any one remembered event.

“短期记忆”“长期记忆”“情景记忆”这套词汇并非诞生于智能体工程领域——它借自认知心理学，而理解这一渊源有助于厘清本模块后续所使用的技术定义。Richard
Atkinson 与 Richard Shiffrin 于 1968
年提出的人类记忆多存储模型（multi-store
model）认为，记忆并非单一系统，而是三个系统：感觉登记、短期存储（也称工作记忆）——保存少量正被主动使用的信息，以及长期存储——保存数量大得多、持续时间也长得多的信息，其中注意与复述是在各存储之间转移信息的控制过程。四年后，Endel
Tulving 于 1972 年发表的《情景记忆与语义记忆》（"Episodic and Semantic
Memory"）一文，进一步细化了长期记忆这一侧的图景，将情景记忆——对特定的、具有时间与空间背景的个人事件的记忆——与语义记忆——心智同样会存储、但并不依附于任何单一被记住事件的一般性、去情境化知识（事实、概念、词义）——区分开来。

Agent engineering has adopted and formalized this vocabulary rather than inventing its own.
Theodore Sumers, Shunyu Yao, Karthik Narasimhan, and Thomas Griffiths' 2023 paper "Cognitive
Architectures for Language Agents" (CoALA) proposes a systematic framework for language agents built
explicitly around this heritage, organizing an agent's information storage into working memory
and long-term memory, and further splitting long-term memory into three
kinds: episodic memory, which "stores experience from earlier decision cycles" such as event
histories or past task trajectories; semantic memory, which "stores an agent's knowledge about the
world and itself," whether from an external source such as a document store or from inferences the
agent generated and saved on its own; and procedural memory, which for a language
agent takes two forms — implicit knowledge baked into the LLM's weights, and explicit knowledge
written into the agent's own code, i.e. the procedures that implement its actions and its
decision-making process itself. The rest of this module works through these four categories one at
a time, in the order an engineer building a real agent would encounter them.

智能体工程沿用并形式化了这套词汇，而非自创一套。Theodore Sumers、Shunyu
Yao、Karthik Narasimhan 与 Thomas Griffiths 于 2023
年发表的论文《语言智能体的认知架构》（"Cognitive Architectures for Language Agents"，简称
CoALA）明确基于这一传统，为语言智能体提出了一套系统化框架：将智能体的信息存储划分为工作记忆与长期记忆，并进一步将长期记忆细分为三类：情景记忆——“存储来自此前决策周期的经验”，例如事件历史或过往任务轨迹；语义记忆——“存储智能体关于世界及自身的知识”，无论其来源是外部数据源（如文档库），还是智能体自行生成并保存的推理结论；以及程序性记忆——对语言智能体而言，它有两种形式：一种是固化在
LLM
权重中的隐性知识，另一种是写入智能体自身代码中的显性知识，即实现其行动与决策过程本身的各项程序。本模块接下来将依次讲解这四个类别，其顺序与一名工程师在构建真实智能体时会遇到它们的先后顺序一致。

---

## 3. Working Memory: The Context Window in Action

**工作记忆：运转中的上下文窗口**

In an LLM agent, working memory is not a separate database — it is the context window itself,
covered mechanically in `introductory/06`. Everything the agent is actively reasoning over on this
turn — the system prompt, the current conversation, any tool results just returned, and whatever
fragments of long-term memory were retrieved for this step — all of it lives together as tokens
inside one window, and CoALA's framing of working memory as holding "active and readily available
information as symbolic variables for the current decision cycle" describes exactly this: it is
the one place where the LLM's prompt template, its own parsed outputs, and retrieved content are
all assembled before a single forward pass. Working memory is fast in the sense that nothing needs
to be fetched from outside the call, but it is small and volatile: once the call ends and nothing
is written elsewhere, its contents are gone.

在一个 LLM
智能体中，工作记忆并非一个独立的数据库——它就是上下文窗口本身，其机制部分已在
`introductory/06`
中讲解过。智能体在当前这一轮主动进行推理所依赖的一切——系统提示词、当前对话、刚刚返回的任何工具结果，以及为这一步骤检索到的长期记忆片段——全部作为词元共同存在于同一个窗口之中。CoALA
将工作记忆定义为保存“当前决策周期中作为符号变量的、活跃且随时可用的信息”，描述的正是这一点：它是
LLM
的提示词模板、自身解析出的输出与检索到的内容，在一次前向传播之前汇集在一起的唯一场所。工作记忆之所以“快”，是因为无需从调用之外获取任何内容；但它同时也很小且易失——一旦本次调用结束、且内容未被写入别处，它便会随之消失。

This volatility is precisely why the other three memory types exist: they are the mechanisms by
which something learned in one working-memory episode survives into the next. A useful mental
model is a desk versus a filing cabinet: working memory is the surface of the desk, holding exactly
what is needed for the task in front of you right now, while the remaining memory types are
different drawers of the filing cabinet, each organized for a different kind of retrieval.

正因为工作记忆具有这种易失性，其余三种记忆类型才应运而生：它们正是让某一次工作记忆片段中习得的内容，得以延续到下一次片段中的机制。一个有用的类比是书桌与文件柜的关系：工作记忆是书桌的桌面，只放置当前任务所需的内容；而其余的记忆类型则是文件柜中不同的抽屉，各自按不同的检索方式组织。

---

## 4. Long-Term Memory: Storage Outside the Window

**长期记忆：窗口之外的存储**

Long-term memory in an agent is any store that persists across calls and across the boundary of a
single context window — typically a database of some kind, most often (as will be covered in depth
in a later intermediate module on retrieval) a vector database that holds text alongside an
embedding, a numeric vector produced by a separate model that represents that text's
meaning, so that a new query can be compared against stored entries by vector similarity rather
than exact keyword match. The engineering problem long-term memory solves is not "how do we store
more text" — disks are cheap — but "how do we decide, cheaply and reliably, which small slice of a
much larger store deserves to occupy this call's limited working memory."

智能体中的长期记忆是指任何能够跨越多次调用、跨越单个上下文窗口边界而持续存在的存储——通常是某种数据库，而最常见的形式（将在后续一个专门讲解检索的中级模块中深入介绍）是向量数据库，它将文本与嵌入向量一并存储，嵌入向量是由另一个独立模型生成的数值向量，用以表示该文本的含义，从而使新的查询可以通过向量相似度而非精确关键词匹配的方式，与已存储的条目进行比较。长期记忆所要解决的工程问题，并不是“如何存储更多文本”——磁盘空间是廉价的——而是“如何低成本、可靠地判断，在一个大得多的存储库中，究竟哪一小部分内容值得占据本次调用中有限的工作记忆”。

Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir Patil, Ion Stoica, and Joseph
Gonzalez's 2023 system MemGPT gives a concrete, named answer to that problem by drawing an explicit
analogy to operating systems: just as a traditional OS gives programs the appearance of a large
memory space by paging data between fast RAM and slower disk, MemGPT gives an LLM the appearance of
a context window far larger than its actual token limit by paging data between a small "main
context" — the actual prompt sent to the model — and a much larger "external context" that lives
outside the window. The system uses function calls the LLM itself can issue to move information
between the two tiers, and it uses interrupts to manage when control returns to the LLM versus the
user, so that the model can, in effect, decide for itself when a piece of information should be
evicted from its own working set and archived, or when an archived piece should be paged back in.
This is a direct, load-bearing example of long-term memory management implemented as an explicit
architectural pattern rather than left to chance, and it is the pattern this module's companion
advanced module, `advanced/03-agent-harness-engineering-production-grade-agent-loops.md`, returns
to when discussing how a production harness manages context at scale.

Charles Packer、Sarah Wooders、Kevin Lin、Vivian Fang、Shishir Patil、Ion Stoica 与 Joseph
Gonzalez 于 2023
年提出的系统 MemGPT，通过与操作系统进行明确类比，为这一问题给出了一个具体的、有名可考的答案：正如传统操作系统通过在高速内存与速度较慢的磁盘之间分页数据，让程序产生拥有巨大内存空间的假象，MemGPT
也通过在一个较小的“主上下文”——即实际发送给模型的提示词——与一个位于窗口之外、容量大得多的“外部上下文”之间分页数据，让
LLM
产生其上下文窗口远大于实际词元上限的假象。该系统使用
LLM
自身可以发起的函数调用，在这两个层级之间移动信息，并使用中断机制来管理控制权何时返还给
LLM、何时交给用户，使模型实际上能够自行决定：何时应将某条信息从自己的工作集中清除并归档，或者何时应将某条已归档的信息重新分页调回。这是一个直接、具有支撑意义的例子，说明长期记忆管理可以被实现为一种明确的架构模式，而非听任偶然发生——本模块的姊妹高级模块
`advanced/03-agent-harness-engineering-production-grade-agent-loops.md`
在讨论生产级运行框架如何大规模管理上下文时，也会回到这一模式。

---

## 5. Episodic Memory: Remembering Specific Experiences

**情景记忆：记住具体的经历**

Episodic memory is the memory type most directly responsible for an agent appearing to "remember
you" across sessions, and the clearest worked implementation of it in the literature comes from
Joon Sung Park, Joseph O'Brien, Carrie Cai, Meredith Ringel Morris, Percy Liang, and Michael
Bernstein's 2023 paper "Generative Agents: Interactive Simulacra of Human Behavior." Their agents
keep a memory stream — a running, timestamped, natural-language log of every observation the agent
makes — and when the agent needs to decide what to do next, it does not simply reread the entire
stream; it retrieves the most useful subset of it using a weighted scoring function over three
factors: recency, importance, and relevance. Concretely, the paper defines the retrieval score for
a candidate memory as

情景记忆是最直接决定一个智能体能否在多次会话之间表现出“记得你”的记忆类型，而文献中对其最清晰的实现范例，来自
Joon Sung Park、Joseph O'Brien、Carrie Cai、Meredith Ringel Morris、Percy Liang 与
Michael Bernstein 于 2023
年发表的论文《生成式智能体：人类行为的交互式拟像》（"Generative Agents: Interactive
Simulacra of Human
Behavior"）。他们笔下的智能体维护着一条记忆流——一份持续记录、带时间戳、以自然语言写成的、涵盖智能体每一次观察的日志——而当智能体需要决定下一步行动时，它并不会简单地重新通读整条记忆流，而是通过一个基于三项因素加权的评分函数，检索出其中最有用的一小部分：这三项因素分别是新近度、重要性与相关性。具体而言，论文将某条候选记忆的检索分数定义为：

$$\text{score} = \alpha_{\text{recency}} \cdot \text{recency} + \alpha_{\text{importance}} \cdot \text{importance} + \alpha_{\text{relevance}} \cdot \text{relevance}$$

The paper sets all three weights ($\alpha$) equal to 1 in its implementation. Recency is computed with
exponential decay applied to the number of "sandbox hours" since the memory was last accessed,
using a decay factor of 0.995 per hour, so more recently touched memories score higher. Importance
is obtained by directly asking the LLM to rate the memory's "poignancy" on a scale from 1 (a
mundane event, such as brushing one's teeth) to 10 (a highly significant event, such as a breakup
or an acceptance). Relevance is computed as the cosine similarity between the embedding
vector of the candidate memory's text and the embedding vector of the current query, where cosine
similarity is a standard measure of how closely two vectors point in the same direction regardless
of their length. All three components are normalized to the [0, 1] range with min-max scaling
before being combined, so that no single factor dominates purely because of its raw numeric scale.

论文在其实现中将三个权重（$\alpha$）均设为
1。新近度的计算方式，是对该记忆自上次被访问以来经过的“沙盒小时数”施加指数衰减，每小时的衰减因子为
0.995，因此近期被访问过的记忆得分更高。重要性的获取方式，是直接让
LLM 对该记忆的“深刻程度”打分，评分范围从
1（日常琐事，例如刷牙）到 10（高度重大的事件，例如分手或收到录取通知）。相关性的计算方式，是候选记忆文本的嵌入向量与当前查询的嵌入向量之间的余弦相似度——这是衡量两个向量方向相似程度的标准指标，与向量的长度无关。在三项分量组合之前，均先通过最小-最大缩放归一化到
[0, 1]
区间，以避免任何单一因素仅因原始数值量级较大而主导最终结果。

A worked example makes the formula concrete. Suppose a coding-assistant agent is deciding which of
three stored memories to bring into its working memory to help debug a failing test right now.
Memory A, "user prefers tabs over spaces," was accessed 200 hours ago, rated importance 2 by the
LLM, and has a query-similarity of 0.30. Memory B, "the `parse_config` function throws on empty
input and we fixed it by adding a guard clause," was accessed 5 hours ago, rated importance 7, and
has a query-similarity of 0.85. Memory C, "the CI pipeline was renamed last quarter," was accessed
2 hours ago, rated importance 3, and has a query-similarity of 0.10. Recency for B, at 5 hours,
is $0.995^5 \approx 0.975$; for C, at 2 hours, it is $0.995^2 \approx 0.990$; for A, at 200 hours, it is
$0.995^{200} \approx 0.367$. After min-max normalizing each column across the three candidates and summing
with equal weights, memory B — recent, LLM-rated as clearly important, and closely related to the
current query — comes out on top by a wide margin, even though memory C is technically the most
recent of the three. This is the formula doing exactly what it is designed to do: recency alone is
not enough to win retrieval if a memory is neither important nor relevant to the task at hand.

一个具体的算例可以让这一公式变得直观。假设某个编程助手智能体，正需要从三条已存储的记忆中挑选，以帮助自己调试当前一个失败的测试用例，看应将哪一条调入工作记忆。记忆
A：“用户偏好使用制表符而非空格”，约 8.3 天（200 小时）前被访问过，LLM
给出的重要性评分为 2，与当前查询的相似度为
0.30。记忆 B：“`parse_config`
函数在输入为空时会抛出异常，我们通过添加一个防护判断修复了它”，5
小时前被访问过，重要性评分为 7，与查询的相似度为
0.85。记忆 C：“CI 流水线在上季度被重命名”，2
小时前被访问过，重要性评分为 3，与查询的相似度为
0.10。就新近度而言，记忆 B 经过 5 小时，为
$0.995^5 \approx 0.975$；记忆 C 经过 2 小时，为
$0.995^2 \approx 0.990$；记忆 A 经过 200 小时，为
$0.995^{200} \approx 0.367$。在对三条候选记忆的每一列分别做最小-最大归一化并按等权重求和之后，记忆
B——既新近、又被 LLM
判定为明显重要、且与当前查询高度相关——将以较大优势胜出，尽管从技术上说，三者之中新近度最高的其实是记忆
C。这正是该公式所要实现的效果：如果一条记忆既不重要、也与当前任务无关，仅凭新近度是无法赢得检索的。

Beyond raw retrieval, the same paper introduces a second mechanism worth naming: reflection.
Reflections trigger automatically once the sum of importance scores across an agent's most
recent memories exceeds a threshold — 150 points in the paper's implementation — at which point the
agent queries the LLM to generate salient high-level questions about its own recent experience,
retrieves the memories most relevant to those questions, and prompts the model to synthesize an
insight with the supporting memories cited as evidence. That synthesized insight is itself written
back into the memory stream as a new memory, which means reflections can be built on top of earlier
reflections, forming what the paper describes as a "tree of reflections" — raw observations as leaf
nodes, and increasingly abstract generalizations as higher levels of the tree. This is the same
underlying idea — converting raw experience into a compact, reusable lesson — that Noah Shinn,
Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao's 2023 paper
"Reflexion: Language Agents with Verbal Reinforcement Learning" applies inside a single task rather
than across a simulated life: as covered in `intermediate/03`, a Reflexion agent converts
scalar or binary task feedback into a verbal self-reflection and stores that reflection in an
episodic memory buffer so that its next attempt at the same task starts with the lesson already in
hand, rather than repeating the same mistake. Generative Agents' reflection trees and Reflexion's
episodic buffer are the same architectural idea — episodic memory synthesized into a lesson and
written back for future retrieval — applied at two different timescales.

在原始检索之外，同一篇论文还引入了第二个值得单独介绍的机制：反思。当智能体近期记忆的重要性得分累计超过某一阈值时（在论文的实现中该阈值为
150），反思便会自动触发：智能体会请求
LLM
就自己近期的经历生成一些显著的高层次问题，检索出与这些问题最相关的记忆，并提示模型综合出一条洞见，同时引用相关记忆作为支撑证据。这条综合而成的洞见本身又会被写回记忆流，成为一条新的记忆，这意味着反思可以建立在此前反思的基础之上，形成论文中所称的“反思树”——原始观察作为叶节点，越往上层则是愈发抽象的概括。这与
Noah Shinn、Federico Cassano、Edward Berman、Ashwin Gopinath、Karthik
Narasimhan 与 Shunyu Yao 于 2023
年发表的论文《Reflexion：具有言语强化学习的语言智能体》（"Reflexion: Language
Agents with Verbal Reinforcement
Learning"）中所应用的，其实是同一种底层思想——将原始经历转化为一条简明、可复用的经验教训——只不过应用的范围不同：正如
`intermediate/03`
中所讲解的，Reflexion
智能体将某次任务的标量或二元反馈转化为一段言语化的自我反思，并将该反思存入一个情景记忆缓冲区，使得它下一次尝试同一任务时，能够带着这条经验教训直接开始，而不是重复同样的错误。Generative
Agents 的反思树与 Reflexion
的情景记忆缓冲区，本质上是同一种架构思想——将情景记忆综合为一条经验教训并写回以供未来检索——只是应用在了两种不同的时间尺度上。

---

## 6. Semantic and Procedural Memory, Briefly

**语义记忆与程序性记忆简述**

CoALA's remaining two categories complete the taxonomy without requiring the same depth of worked
example, because their engineering treatment is more familiar from earlier modules. Semantic memory
in an agent is any store of general knowledge not tied to a specific remembered event — a knowledge
base of company policy documents an agent retrieves from, or a set of facts the agent inferred
during past episodes and chose to save as durable, decontextualized knowledge rather than as an
episode-specific memory. The retrieval mechanics that will be developed in a later intermediate
module on retrieval-augmented generation apply to semantic memory just as they apply to episodic
memory — the distinction that matters here is not the software (both can live in the same vector
store) but the content: "the user's ticket #4471 was resolved by restarting the cache" is episodic,
while "restarting the cache resolves stale-config tickets" is semantic — a general rule extracted
from one or many episodes.

CoALA
剩余的两个类别，无需借助同等篇幅的算例即可完整补全整个分类体系，因为它们在工程上的处理方式，读者从此前模块中已相对熟悉。智能体中的语义记忆，是指任何不依附于特定被记住事件的一般性知识存储——例如智能体检索所用的一份公司政策文件知识库，或者智能体在以往片段中推理得出、并选择作为持久的、去情境化知识（而非某一片段专属的记忆）保存下来的一组事实。将在后续一个专门讲解检索增强生成的中级模块中展开的检索机制，同样适用于语义记忆，正如它适用于情景记忆一样——此处真正重要的区别不在于软件层面（二者完全可以存放在同一个向量存储中），而在于内容层面：“用户的
4471 号工单是通过重启缓存解决的”属于情景记忆，而“重启缓存可以解决配置过期类工单”则属于语义记忆——这是从一次或多次片段中提炼出的一条一般性规则。

Procedural memory, as CoALA defines it, is less a store an agent writes to at runtime and more a
description of where an agent's "how-to" knowledge already lives: partly implicit, inside the
weights of the LLM itself (the model's general competence at, say, writing Python, which was never
explicitly stored as a memory but is simply part of what the model is), and partly explicit, inside
the agent's own source code — the concrete procedures that implement each action and the
decision-making loop itself, as covered in `introductory/03` and `intermediate/03`. Framed this
way, procedural memory is the reminder that not all of an agent's "memory" is retrieved text — some
of it is the code that makes the agent an agent in the first place, and no scoring formula is
needed to retrieve it because it is not retrieved at all; it simply runs.

CoALA
所定义的程序性记忆，与其说是智能体在运行时会写入的一种存储，不如说是对智能体“操作性”知识究竟存放于何处这一问题的描述：一部分是隐性的，存在于
LLM
自身的权重之中（例如模型编写
Python
代码的一般能力，这种能力从未被显式地存储为某条记忆，而只是模型本身能力的一部分）；另一部分是显性的，存在于智能体自身的源代码之中——即实现每个具体行动的程序，以及决策循环本身，这些内容已在
`introductory/03` 与 `intermediate/03`
中讲解过。以这种方式来理解，程序性记忆提醒我们：并非智能体的一切“记忆”都是被检索出来的文本——其中一部分，正是让智能体之所以成为智能体的代码本身，它无需任何评分公式来检索，因为它根本不需要被检索，而是直接运行。

---

## 7. Failure Modes: What Memory Systems Get Wrong

**失效模式：记忆系统会在哪些地方出错**

Every mechanism covered above trades an error type for a capability, and a working knowledge of
those trade-offs is as important as knowing the mechanisms themselves. Retrieval systems built on
relevance and recency, as in the Generative Agents scoring formula, can suffer from stale memories
that were accurate when written but have since become false — the coding agent's memory that
"the CI pipeline uses `run_tests.sh`" is a liability, not an asset, once that script is renamed and
the memory is never invalidated. Systems that rely on an LLM to self-rate importance, as Generative
Agents does, inherit whatever biases or inconsistencies that LLM has in judging significance — a
model might rate two functionally identical events differently depending on phrasing alone.
Purely embedding-based relevance can also retrieve text that is superficially similar in wording
but substantively irrelevant, and purely recency-weighted retrieval can surface trivia over
substance simply because it happened recently. None of these are reasons to avoid memory systems —
they are reasons every production memory system needs monitoring, staleness handling, and a way for
a human or the agent itself to correct or delete a memory that turned out to be wrong.

上文所涉及的每一种机制，都是在用某种错误换取某种能力，而对这些权衡有清晰的认识，与理解机制本身同样重要。以相关性与新近度为基础的检索系统（如
Generative Agents
的评分公式）可能会受困于陈旧记忆——这些记忆在写入时是准确的，但此后已经变得不再正确——例如编程智能体记住“CI
流水线使用
`run_tests.sh`”，一旦该脚本被重命名而这条记忆从未被更新，它便从一项资产变成了一个隐患。依赖
LLM 自行评估重要性的系统（如 Generative
Agents）会继承该 LLM
在判断事件重要程度时固有的偏差或不一致——同一模型可能仅因措辞不同，就对两个功能上完全等价的事件给出不同的评分。仅依赖嵌入向量的相关性检索，也可能检索出措辞表面相似、但实质上毫不相关的文本；而仅依赖新近度加权的检索，也可能仅仅因为某条内容发生得较近，就让琐事凌驾于实质内容之上。这些都不是回避记忆系统的理由——它们恰恰说明，任何生产级记忆系统都需要监控机制、陈旧内容处理机制，以及让人类或智能体自身能够纠正或删除一条被证明有误的记忆的方式。

---

## 8. Worked Example: A Multi-Day Coding Assistant

**综合算例：一个跨越多日的编程助手**

Bring the four categories together in one agent. On day one, a coding-assistant agent's working
memory (its context window) holds the current file, the user's request, and a tool result from
running the test suite — this is short-term, volatile, and gone once the call ends. During that
session, the agent writes two things to persistent storage: an episodic memory, "on day 1, fixed a
`NoneType` crash in `parse_config` by adding a guard clause, after the user rejected the first
attempted fix that used a try/except," timestamped and stored in a vector store alongside its
embedding; and, after enough related episodes accumulate, a reflection synthesized from several
such episodes — "this user consistently prefers explicit guard clauses over try/except for
input validation" — which is itself written back as a new memory, exactly as in the Generative
Agents reflection mechanism. On day five, when the user asks the agent to fix a similar bug, the
agent's harness retrieves candidate memories using the recency/importance/relevance formula worked
through in §5, and the reflection memory — highly relevant to "how should I write this fix," rated
important by the LLM, and not too stale — outranks the raw day-one episodic memory and is the one
that makes it into the day-five working memory, shaping the agent's fix before it writes a single
line of code. Long-term storage (the vector store itself, potentially paged the way MemGPT pages
its external context if the store grows very large) is what makes this possible across a five-day
gap that no single context window could span; procedural memory — the agent's underlying coding
competence and the loop that lets it call the file-edit tool at all — was present on every single
day and needed no retrieval at all.

现在把这四个类别整合到同一个智能体中。第一天，一个编程助手智能体的工作记忆（即其上下文窗口）中存放着当前文件、用户的请求，以及一次运行测试套件所得到的工具结果——这些内容属于短期记忆，易失，且在本次调用结束后即消失。在这次会话中，该智能体向持久化存储写入了两项内容：一条情景记忆，“第一天，通过添加一个防护判断修复了
`parse_config`
中的一个 `NoneType`
崩溃问题，此前用户否决了最初使用
try/except 的修复方案”，带有时间戳并连同其嵌入向量一并存入向量存储；以及，在积累了足够多的相关片段之后，一条从若干这类片段中综合而成的反思——“该用户在输入校验方面，始终更偏好使用显式的防护判断，而非
try/except”——这条反思本身又会被写回作为一条新的记忆，与
Generative Agents
的反思机制完全一致。到第五天，当用户要求该智能体修复一个类似的缺陷时，其运行框架会使用第
5
节中详细算过的新近度/重要性/相关性公式来检索候选记忆，而那条反思型记忆——与“应当如何编写这次修复”高度相关、被
LLM
判定为重要、且尚不算陈旧——会胜过第一天那条原始的情景记忆，成为进入第五天工作记忆的那一条，在该智能体写下任何一行代码之前，便已塑造了它的修复思路。长期存储（即向量存储本身，若其规模变得非常大，甚至可以像
MemGPT
分页其外部上下文那样进行分页）正是使这一切得以跨越五天的间隔成为可能的关键——任何单一的上下文窗口都无法跨越这一间隔；而程序性记忆——该智能体底层的编程能力，以及使其能够调用文件编辑工具的循环本身——在每一天都始终存在，且完全无需任何检索。

---

## 9. Summary

**小结**

Agent memory is not one mechanism but a small system of them, and the taxonomy this module worked
through — working memory as the volatile context window, long-term memory as persistent storage
paged in and out the way MemGPT pages its external context, episodic memory as a scored,
retrievable log of specific past experiences as in Generative Agents and Reflexion, and semantic
and procedural memory rounding out CoALA's full picture — gives an engineer a vocabulary for
deciding, deliberately, what an agent should remember, for how long, and how it should be brought
back. The next curriculum module in this author's assignment,
`advanced/03-agent-harness-engineering-production-grade-agent-loops.md`, treats memory management
as one piece of the larger production harness that wraps an agent loop, alongside tool execution,
error handling, and observability.

智能体记忆并非单一机制，而是由若干机制组成的一个小型系统，本模块所梳理的这套分类体系——作为易失性上下文窗口的工作记忆、如
MemGPT
分页其外部上下文那样进出的持久化长期记忆、如
Generative Agents 与 Reflexion
所展示的、带评分且可检索的具体过往经历日志所构成的情景记忆，以及补全
CoALA
完整图景的语义记忆与程序性记忆——为工程师提供了一套词汇，用以有意识地决定：一个智能体应当记住什么、记住多久、以及应当如何将其重新调取回来。本作者负责撰写的下一个课程模块
`advanced/03-agent-harness-engineering-production-grade-agent-loops.md`，将把记忆管理作为包裹智能体循环的更大生产级运行框架中的一个环节来处理，与工具执行、错误处理及可观测性并列。

---

## References

**参考文献**

### External Sources

- [Atkinson, R. C., & Shiffrin, R. M. (1968). Human memory: A proposed system and its control processes (multi-store model overview)](https://en.wikipedia.org/wiki/Atkinson%E2%80%93Shiffrin_memory_model)
- [Tulving, E. (1972). Episodic and Semantic Memory. In Organization of Memory (bibliographic record)](https://www.scirp.org/reference/referencespapers?referenceid=2919588)
- [Park, J. S., O'Brien, J., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)
- [Sumers, T. R., Yao, S., Narasimhan, K., & Griffiths, T. L. (2023/2024). Cognitive Architectures for Language Agents (CoALA)](https://arxiv.org/abs/2309.02427)
- [Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I., & Gonzalez, J. E. (2023). MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)
- [Shinn, N., Cassano, F., Berman, E., Gopinath, A., Narasimhan, K., & Yao, S. (2023). Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)

### Internal Cross-References

- [`introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md`](../introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md)
- [`introductory/04-tool-use-and-function-calling-basics.md`](../introductory/04-tool-use-and-function-calling-basics.md)
- [`introductory/06-context-windows-tokens-and-memory-basics.md`](../introductory/06-context-windows-tokens-and-memory-basics.md)
- [`intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md`](03-agent-design-patterns-react-plan-execute-reflexion.md)
- [`advanced/03-agent-harness-engineering-production-grade-agent-loops.md`](../advanced/03-agent-harness-engineering-production-grade-agent-loops.md)
