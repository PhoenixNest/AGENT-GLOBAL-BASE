# Multi-Agent Communication & Coordination Protocols

**多智能体通信与协调协议**

| Field   | English                                                                 | 中文                                        |
| ------- | ----------------------------------------------------------------------- | ------------------------------------------- |
| Level   | Intermediate                                                            | 中级                                        |
| Cluster | Multi-Agent Systems & Evaluation                                        | 多智能体系统与评估                          |
| Author  | Dr. Kaito Fujimori, Research Scientist — Agent Systems Research, ANU-00 | ANU-00 智能体系统研究员 Kaito Fujimori 博士 |

---

## 1. Recap and Where This Chapter Goes Further

**回顾与本章的深入之处**

This module builds strictly on four earlier modules, named explicitly wherever this chapter relies
on them: `introductory/07-introduction-to-multi-agent-systems.md` (the definition of a multi-agent
system, and its centralized/decentralized/hierarchical organizational sketch),
`introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md` (the single-agent loop),
`introductory/04-tool-use-and-function-calling-basics.md` (structured tool calls as a model for
structured messages), and this author's own
`intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md` (the cognitive patterns —
ReAct, Plan-and-Execute, Reflexion — that a single agent inside a multi-agent system commonly runs
internally).

本模块严格建立在四个前置模块之上；凡本章依赖这些前置模块之处，均明确点名： [`introductory/07`](../introductory/07-introduction-to-multi-agent-systems.md)（多智能体系统的定义及其集中式/去中心式/层级式组织方式概述）、[`introductory/03`](../introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md) （单智能体循环）、[`introductory/04`](../introductory/04-tool-use-and-function-calling-basics.md)（结构化工具调用，作为结构化消息的范式），以及本作者自己撰写的 [`intermediate/03`](03-agent-design-patterns-react-plan-execute-reflexion.md)（ReAct、计划-执行、Reflexion 这三种认知模式——单个智能体在多智能体系统内部通常会运行其中之一）。

[`introductory/07`](../introductory/07-introduction-to-multi-agent-systems.md) defined a multi-agent system (**MAS** for short) as two or more AI agents, each
running its own agent loop ([`introductory/03`](../introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md)), that communicate via messages or shared state to
work toward a shared task, and sketched three organizational shapes at a high level: centralized
(one agent directs the others), decentralized (agents coordinate as peers), and hierarchical (a tree
of delegation).

[`introductory/07`](../introductory/07-introduction-to-multi-agent-systems.md) 将多智能体系统（简称 **MAS**）定义为两个或更多各自运行着自己的智能体循环（[`introductory/03`](../introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md)）的 AI 智能体，它们通过消息或共享状态进行通信，共同致力于完成某项任务，并在较高层面上勾勒了三种组织形态：集中式（一个智能体指挥其他智能体）、去中心式（智能体作为对等方相互协调）以及层级式（一种委托关系构成的树状结构）。

That module deliberately stopped at the sketch, leaving two concrete questions unanswered: what does
a message between two agents actually _contain_, in a form precise enough to implement, and what
role does a coordinator play once agents actually need to exchange results and be kept from working
at cross purposes? This module answers both, building a vocabulary of message patterns, named
protocols, and topology types that later modules — including [`advanced/07`](../advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md), already published in
this curriculum — depend on directly.

那一章刻意止步于概述层面，留下了两个具体问题尚未解答：两个智能体之间的一条消息，究竟*包含*什么内容，其形式要精确到足以被实现？而当智能体真正需要交换结果、并需要避免相互掣肘时，协调者又扮演着怎样的角色？本模块将对这两个问题一一作答，构建出一套消息模式、具名协议与拓扑类型的词汇体系——本课程中已发布的 [`advanced/07`](../advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md) 等后续模块，都将直接依赖这套词汇。

---

## 2. What a Message Actually Is: Speech Acts and Performatives

**消息究竟是什么：言语行为与施为动词**

[`introductory/04`](../introductory/04-tool-use-and-function-calling-basics.md) established that a tool call is not free text but a structured object — a name
plus arguments matching a schema — and the same discipline applies to inter-agent messages: a
message that is just an unstructured string ("tell Agent B to check the database") is far more
fragile than one with an explicit, parseable **performative**, the classical term from speech act
theory for the _type_ of communicative act a message performs, independent of its content.

[`introductory/04`](../introductory/04-tool-use-and-function-calling-basics.md) 已经确立了这样一个原则：一次工具调用不是自由文本，而是一个结构化对象——一个名称加上符合某种模式的参数——同样的原则也适用于智能体之间的消息：一条只是无结构字符串（例如“告诉智能体 B 去检查数据库”）的消息，远比一条带有明确、可解析的**施为动词**的消息脆弱得多。“施为动词”是言语行为理论中的经典术语，指的是一条消息所执行的通信行为的*类型*，与其具体内容相互独立。

The **Foundation for Intelligent Physical Agents (FIPA)** formalized this into the **FIPA Agent
Communication Language (FIPA ACL)**, whose message structure specification defines a set of
mandatory and optional parameters — most importantly a `performative`, plus `sender`, `receiver`,
and `content` — where the performative is drawn from a fixed vocabulary of communicative-act types
such as `inform` (assert a fact), `request` (ask the receiver to perform an action), `query-if` (ask
whether something is true), `propose` (offer to do something, typically under a condition),
`accept-proposal`, and `reject-proposal` (FIPA, ACL Message Structure Specification).

**智能物理智能体基金会（Foundation for Intelligent Physical Agents，FIPA）** 将这一思路正式化为 **FIPA 智能体通信语言（FIPA Agent Communication Language，FIPA ACL）**，其消息结构规范定义了一组必选与可选参数——其中最重要的是 `performative`，此外还有 `sender`、 `receiver` 与 `content`——施为动词取自一套固定的通信行为类型词汇表，例如 `inform`（陈述一个事实）、`request`（要求接收方执行某个行动）、`query-if`（询问某事是否为真）、 `propose`（提议做某事，通常附带条件）、`accept-proposal`（接受提议）与 `reject-proposal`（拒绝提议）（FIPA，ACL 消息结构规范）。

The value of this vocabulary is that it separates _what kind of communicative act_ a message is from
_what it is about_ — a `request` for `run_tests()` and an `inform` about `run_tests() succeeded` are
structurally different kinds of messages even though they concern the same underlying action, and a
receiving agent can dispatch on the performative alone before even parsing the content, exactly as a
harness dispatches on a tool name before parsing its arguments.

这套词汇的价值在于，它把“这条消息属于哪一类通信行为”与“这条消息是关于什么的”区分开来——一条针对 `run_tests()` 的 `request` 消息，与一条关于“`run_tests()` 已成功”的 `inform` 消息，尽管涉及的是同一个底层行动，但在结构上却是不同种类的消息，接收方智能体仅凭施为动词本身即可进行分派处理，而无需先解析其内容——这与运行框架先根据工具名称进行分派、再解析其参数的方式如出一辙。

A modern LLM-based multi-agent system rarely implements the full FIPA specification verbatim, but
production frameworks converge on the same underlying discipline: a message is a structured record
with, at minimum, a sender, a recipient (or a broadcast target), a type tag playing the role of a
performative, and a content payload — precisely because an unstructured free-text message is as
brittle between two agents as an unstructured free-text tool call would be between an LLM and a
harness.

现代基于 LLM 的多智能体系统很少会逐字实现完整的 FIPA 规范，但生产级框架都不约而同地遵循着同一套底层准则：一条消息是一份结构化记录，至少包含发送方、接收方（或广播目标）、一个扮演施为动词角色的类型标签，以及内容负载——原因正在于，一条无结构的自由文本消息在两个智能体之间的脆弱程度，不亚于一次无结构的自由文本工具调用在 LLM 与运行框架之间的脆弱程度。

---

## 3. Request/Response and the Contract Net Protocol

**请求/响应与合同网协议**

The simplest message pattern is **request/response**: Agent A sends a `request` for some action,
Agent B performs it and replies with an `inform` describing the outcome. This pattern alone is
enough when A already knows which agent should do the work.

最简单的消息模式是**请求/响应**：智能体 A 就某项行动发送一条 `request`，智能体 B 执行该行动，并以一条描述结果的 `inform` 作为回复。当 A 已经知道该由哪个智能体来完成这项工作时，这一模式本身就已经足够。

It is not enough when A has a task and does not yet know _which_ of several available agents is best
suited to do it — a common situation in a system with specialized agents.

但当 A 有一项任务、却尚不知道现有的若干个可用智能体中*哪一个*最适合完成它时，这一模式就不够用了——在一个拥有多个专精智能体的系统中，这是很常见的情形。

Reid G. Smith's 1980 paper "The Contract Net Protocol: High-Level Communication and Control in a
Distributed Problem Solver" formalizes a negotiation-based answer that is still the conceptual
ancestor of most task-allocation logic in today's multi-agent frameworks: a **manager** agent
broadcasts a **task announcement** describing the work and its requirements to a pool of candidate
agents; each interested agent replies with a **bid** stating its ability to do the work (and
optionally at what cost or with what confidence); the manager evaluates the bids and sends an
**award** to the winning agent, who then executes the task and reports back (Smith, 1980).

Reid G. Smith 1980 年发表的论文《合同网协议：分布式问题求解器中的高层通信与控制》（"The Contract Net Protocol: High-Level Communication and Control in a Distributed Problem Solver"）为此提出了一种基于协商的解答，至今仍是当今多数多智能体框架中任务分配逻辑的概念源头：一个**管理者**智能体向候选智能体池广播一份描述工作内容及其要求的**任务公告**；每个感兴趣的智能体都会回复一份**投标**，说明自己完成该工作的能力（也可以附带成本或置信度等信息）；管理者对各方投标进行评估，向中标的智能体发送**授标**，该智能体随后执行任务并汇报结果（Smith, 1980）。

The Contract Net Protocol is the negotiation-based special case of request/response, and it
generalizes cleanly to the coordinator role covered in [§6](#6-the-coordinator-role-and-swarm-topologies): a **coordinator** in a modern LLM
multi-agent system frequently performs exactly this manager role — deciding which of several
available specialized agents (a "coding agent," a "research agent," a "review agent") should handle
a given subtask — even when the "bid" step is simplified to the coordinator's own LLM call reasoning
about which agent's described capabilities best match the task, rather than a literal competitive
bidding round among the agents themselves.

合同网协议是请求/响应模式中基于协商的一个特例，它可以顺畅地推广为[第 6 节](#6-the-coordinator-role-and-swarm-topologies)所讲的协调者角色：现代 LLM 多智能体系统中的**协调者**，往往正是在扮演这一管理者的角色——判断若干可用的专精智能体（“编程智能体”“研究智能体”“审阅智能体”）中，哪一个应当处理某个给定的子任务——即便“投标”这一步骤已被简化为协调者自身的一次 LLM 调用，用以推理判断哪个智能体所描述的能力与任务最为匹配，而不是智能体之间真正展开一轮竞争性投标。

---

## 4. Shared Blackboard Systems

**共享黑板系统**

Request/response and Contract Net are both **point-to-point** patterns — a message names a specific
sender and receiver. An entirely different pattern lets agents communicate indirectly, through
shared state rather than direct messages.

请求/响应与合同网协议都属于**点对点**模式——一条消息明确指向某个特定的发送方与接收方。而另一种截然不同的模式，则允许智能体通过共享状态、而非直接消息进行间接通信。

Barbara Hayes-Roth's 1985 paper "A Blackboard Architecture for Control" formalizes the
**blackboard** pattern: a shared, structured data store (the "blackboard") that any agent can read
from and write to, together with independent **knowledge sources** — in Hayes-Roth's original
AI-systems context, specialized modules each competent at recognizing certain kinds of partial
solutions and contributing incremental progress toward a shared goal — and a control component that
decides, at each moment, which knowledge source should be given the opportunity to act next, based
on the blackboard's current state (Hayes-Roth, 1985).

Barbara Hayes-Roth 1985 年发表的论文《用于控制的黑板架构》（"A Blackboard Architecture for Control"）将**黑板**模式正式化：一份共享的、结构化的数据存储（“黑板”），任何智能体都可以对其进行读写，配合若干独立的**知识源**——在 Hayes-Roth 最初所研究的 AI 系统语境中，指的是各自擅长识别某类部分解、并为共享目标贡献增量进展的专门化模块——以及一个控制组件，该组件根据黑板当前的状态，在每一时刻决定接下来应当给予哪个知识源采取行动的机会（Hayes-Roth, 1985）。

Applied to an LLM multi-agent system, each agent plays the role of a knowledge source: instead of
one agent sending another a directed message, an agent writes its partial result or observation onto
a shared data structure (a document, a shared list of findings, a key-value store), and any other
agent that needs that information reads it directly, with no message addressed specifically to them
required.

将这一模式应用于 LLM 多智能体系统时，每个智能体都扮演着知识源的角色：智能体并不是把一条定向消息发送给另一个智能体，而是将自己的部分结果或观察写入一份共享数据结构（一份文档、一份共享的发现列表、一个键值存储）之中，任何需要这一信息的其他智能体都可以直接读取它，而无需一条专门发给它们的消息。

The blackboard pattern trades the precision of a directed message (I know exactly who receives this)
for looser coupling (any agent that becomes relevant later can find what it needs without the writer
having anticipated its existence) — a genuine engineering tradeoff, not a strictly superior
alternative to request/response.

黑板模式以更松散的耦合（任何日后才变得相关的智能体，都能找到自己所需的信息，而无需写入者事先预见到它的存在）换取了定向消息所具有的精确性（我确切知道谁会收到这条消息）——这是一种真实存在的工程权衡，而不是一种绝对优于请求/响应模式的替代方案。

It also introduces a coordination risk worth naming precisely here because it recurs later in this
curriculum: if two agents write to overlapping parts of the blackboard concurrently, one write can
silently clobber the other unless the control component (or an external mechanism) serializes access
— the same underlying filesystem-contention problem that [`advanced/07`](../advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md)'s worktree-isolation
discussion addresses for concurrently-executing agents editing a shared codebase, generalized here
to any shared piece of state rather than a filesystem specifically.

它还引入了一种值得在此精确点名的协调风险，因为它会在本课程后续内容中再次出现：如果两个智能体并发地写入黑板上重叠的部分，除非控制组件（或某种外部机制）对访问进行了串行化处理，否则一次写入可能会悄无声息地覆盖掉另一次写入——这与 [`advanced/07`](../advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md) 在讨论工作树隔离时，针对并发执行、编辑同一份共享代码库的智能体所处理的底层文件系统争用问题本质相同，只是在这里被推广到了任何一份共享状态，而不专指文件系统。

---

## 5. Publish-Subscribe Messaging

**发布-订阅消息传递**

A third pattern sits between the tight coupling of request/response and the fully shared state of a
blackboard.

第三种模式，则介于请求/响应的紧密耦合与黑板模式的完全共享状态之间。

Eugster, Felber, Guerraoui, and Kermarrec's 2003 survey "The Many Faces of Publish/Subscribe,"
published in ACM Computing Surveys, characterizes the **publish-subscribe** family of patterns by
three forms of decoupling that distinguish it from request/response: space decoupling (a publisher
does not need to know the identity, or even the existence, of its subscribers), time decoupling (a
publisher and a subscriber do not need to be active participants in the interaction at the same
time), and synchronization decoupling (producing and consuming a message are not blocking operations
for either party) (Eugster et al., 2003).

Eugster、Felber、Guerraoui 与 Kermarrec 2003 年发表于《ACM 计算综述》（ACM Computing Surveys）的综述文章《发布/订阅的多重面貌》（"The Many Faces of Publish/Subscribe"）通过三种解耦形式，将**发布-订阅**这一系列模式与请求/响应模式区分开来：空间解耦（发布者无需知道其订阅者的身份、甚至无需知道其是否存在）、时间解耦（发布者与订阅者无需在同一时刻同时参与这次交互）、以及同步解耦（对交互双方而言，生产消息与消费消息都不是阻塞性操作）（Eugster et al., 2003）。

In practice, an agent **publishes** an event to a named **channel** (or "topic") — for example,
`"code-review-completed"` — without knowing which, if any, agents are listening, and any agent that
has **subscribed** to that channel receives the event when it is published, without the publisher
needing to address it directly.

在实践中，某个智能体会向一个具名的**频道** （或称“主题”）——例如 `"code-review-completed"`——**发布**一个事件，而无需知道究竟有没有智能体在监听；而任何已**订阅**该频道的智能体，都会在事件发布时收到它，发布者无需将其直接指向某个特定接收方。

This decoupling matters directly for the swarm topologies covered next in [§6](#6-the-coordinator-role-and-swarm-topologies).

这种解耦对下文[第 6 节](#6-the-coordinator-role-and-swarm-topologies)将要讲述的集群拓扑而言直接相关。

A flat topology, where several worker agents all report status to whoever is listening without
knowing about each other, is naturally implemented with publish-subscribe: each worker publishes its
progress to a shared "status" channel, and a coordinator (or several interested parties) subscribes
to it, rather than each worker needing a direct reference to the coordinator's address. This is a
genuine architectural choice with a real cost, not a strictly better default: a system built
entirely on publish-subscribe channels sacrifices the request/response pattern's clear expectation
of a specific reply to a specific message, which is why production multi-agent systems typically
combine both — publish-subscribe for status and events, request/response (or Contract Net) for work
that needs a committed assignment and an accountable reply.

在扁平拓扑中，若干工作者智能体都在向“任何正在监听的一方”汇报状态，彼此互不知晓，这种情形天然适合用发布-订阅来实现：每个工作者都将自己的进度发布到一个共享的“状态”频道上，而协调者（或若干感兴趣的一方）订阅该频道，无需每个工作者都持有指向协调者地址的直接引用。这是一种真实存在、且有其代价的架构选择，而非一种绝对更优的默认方案：一个完全建立在发布-订阅频道之上的系统，会牺牲请求/响应模式所具有的、针对某条特定消息给出特定回复的明确预期——这正是为什么生产级多智能体系统通常会将两者结合起来使用：用发布-订阅处理状态与事件，用请求/响应（或合同网协议）处理那些需要明确指派、且需要对方给出可追责回复的工作。

---

## 6. The Coordinator Role and Swarm Topologies

**协调者角色与集群拓扑**

Sections 2–5 covered _what a message looks like_; this section covers _who talks to whom, and in
what shape_. A **coordinator** is the agent (or non-agent controller) responsible for deciding how a
task is broken up, which agent handles which piece, and how the pieces' results are combined — the
role the Contract Net manager and the blackboard's control component both specialize. The graph
structure describing which agents communicate with which is called the **swarm topology**, and five
shapes recur across production multi-agent designs.

[第 2 至 5 节](#2-what-a-message-actually-is-speech-acts-and-performatives)讲的是*一条消息看起来是什么样子*；本节讲的则是*谁与谁交流，以及以何种形态交流*。 **协调者**是负责决定任务如何拆分、由哪个智能体处理哪一部分、以及如何将各部分结果加以合并的智能体（或非智能体控制器）——合同网协议中的管理者、以及黑板架构中的控制组件，都是这一角色的特化形式。描述“谁与谁通信”这一图结构的说法，称为**集群拓扑**，在生产级多智能体设计中反复出现的形态共有五种。

| Topology                                 | EN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 中文                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Hierarchical topology** / **层级拓扑** | a single coordinator dispatches work to subordinate agents and collects their results, mirroring a tree — Anthropic's own June 2025 engineering post "How We Built Our Multi-Agent Research System" describes exactly this shape in production, calling it an "orchestrator-worker pattern, where a lead agent coordinates the process while delegating to specialized subagents that operate in parallel." That post reports two different "90%" figures, and they measure two different things, so it is worth keeping them apart precisely: parallelizing subagent dispatch and tool calls — running several subagents at once, and letting each subagent call several tools at once, rather than running everything serially as the team's system originally did — cut research time by up to 90% for complex queries, a speed comparison against the team's own earlier _sequential_ execution, not against a single-agent baseline. Separately, on an internal research evaluation, a multi-agent system with a Claude Opus 4 lead agent and Claude Sonnet 4 subagents outperformed a single-agent Claude Opus 4 baseline by 90.2% — a quality figure, and the post's actual single-agent-versus-multi-agent comparison (Anthropic, 2025). | 单一协调者向下属智能体派发任务并收集结果，整体呈树状结构——Anthropic 自身于 2025 年 6 月发布的工程博客《我们如何构建多智能体研究系统》（"How We Built Our Multi-Agent Research System"）在生产环境中所描述的正是这一形态，将其称为“编排者-工作者模式，即由一个主导智能体协调整个流程，同时将任务委派给并行运作的专门化子智能体”。该文中报告了两个不同的 "90%"数字，二者衡量的是完全不同的东西，值得在此精确区分开来：将子智能体的派发与工具调用并行化——即让若干子智能体同时运行、并让每个子智能体同时调用多个工具，而不是像该团队系统最初那样完全*串行*执行——把复杂查询的研究耗时最多缩短了 90%，这是与该团队自身此前的*串行*执行方式相比较所得出的速度提升，而并非与单智能体基线的比较。另外，在一项内部研究评测中，由 Claude Opus 4 担任主导智能体、Claude Sonnet 4 担任子智能体的多智能体系统，相较于单智能体 Claude Opus 4 基线，表现提升了 90.2%——这是一个质量指标，也是该文中真正意义上“单智能体对比多智能体”的数字（Anthropic, 2025）。 |
| **Flat topology** / **扁平拓扑**         | every agent reports to one orchestrator with no intermediate layer — the simplest case of the hierarchical shape, one level deep.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 每个智能体都直接向一个编排器汇报，中间不设分层——这是层级形态中最简单的一种特例，只有一层深度。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **Mesh topology** / **网状拓扑**         | agents communicate peer-to-peer without a central coordinator at all; Wu et al.'s 2023 AutoGen paper implements this directly, with each agent an independently configurable "conversable agent" that can be composed into arbitrary conversation patterns, including a "group chat" mode where multiple agents converse with each other in a shared thread rather than through any single dispatcher (Wu et al., 2023).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | 智能体之间点对点通信，完全不存在中心协调者；Wu 等人 2023 年发表的 AutoGen 论文正是直接实现了这一模式，其中每个智能体都是一个可独立配置的“可对话智能体”，可以被组合成任意的对话模式，包括一种“群聊”模式——在该模式下，多个智能体在一个共享线程中彼此交流，而不经由任何单一的分派者（Wu et al., 2023）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **Pipeline topology** / **流水线拓扑**   | agents hand work to each other in sequence — Agent A finishes, then Agent B starts on Agent A's output, and so on — with no need for the concurrent-access patterns of [§§4–5](#4-shared-blackboard-systems) since each stage's input is fully determined before the next stage begins.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 智能体依次将工作交接给下一个智能体——智能体 A 完成后，智能体 B 才开始处理 A 的产出，以此类推——由于每个阶段的输入在下一阶段开始之前就已完全确定，因此不需要第 4、5 两节中所讲的并发访问模式。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **Hybrid topology** / **混合拓扑**       | combines these shapes, which is what most non-trivial real systems actually look like: a hierarchical dispatch to specialized worker pools, each of which may internally run a pipeline, with a mesh-like peer discussion for a disagreement that needs resolving before the coordinator can proceed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | 将上述几种形态组合起来，这也正是绝大多数具有一定复杂度的真实系统实际呈现出的样子：向若干专门化的工作者池进行层级式派发，其中每个工作者池内部又可能运行着一条流水线，再辅以类似网状的对等讨论，用以在协调者能够继续推进之前解决某个需要化解的分歧。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |

---

## 7. A Worked Example: A Three-Agent Research Assistant

**综合算例：一个三智能体研究助手**

Combine the pieces above into a single system: a **coordinator** agent, a **web-research** agent,
and a **fact-checking** agent, tasked with answering "what was the primary cause of the 2008
financial crisis, and is that explanation still considered accurate today?"

将上述各个部分整合为一个完整系统：一个**协调者**智能体、一个**网络研究**智能体，以及一个**事实核查** 智能体，共同负责回答这样一个问题：“2008 年金融危机的主要原因是什么？这一解释在今天是否仍被认为是准确的？”

```text
1. Coordinator publishes a task announcement to a "task-board" channel (Contract Net, §3):
   {performative: "cfp" (call-for-proposals), task: "research 2008 crisis cause"}
2. Web-research agent replies with a bid (it has search tools available); coordinator awards it.
3. Coordinator sends a direct request (§2) to Web-research agent:
   {performative: "request", content: "find primary cause explanations, cite sources"}
4. Web-research agent runs its own internal ReAct loop (intermediate/03) using tools from
   introductory/04, and writes its findings to a shared blackboard (§4) document rather than
   replying only to the coordinator, so the fact-checker can read them directly.
5. Coordinator, watching a "findings-ready" pub-sub channel (§5), is notified and sends a request
   to the Fact-checking agent: "verify these claims against current (2020s) consensus."
6. Fact-checking agent reads the blackboard, runs its own checks, and publishes an "inform" with
   its verdict to the same findings document.
7. Coordinator reads the completed blackboard entry and synthesizes the final answer for the user.
```

```text
1. 协调者向"任务板"频道发布一份任务公告（合同网协议，见第 3 节）：
   {施为动词："cfp"（征集提案）, 任务："研究 2008 年危机的原因"}
2. 网络研究智能体回复一份投标（它拥有可用的搜索工具）；协调者授标于它。
3. 协调者向网络研究智能体发送一条直接请求（见第 2 节）：
   {施为动词："request", 内容："查找关于主要原因的各种解释，并注明来源"}
4. 网络研究智能体运行自己内部的 ReAct 循环（见 intermediate/03），使用 introductory/04 中的工具，并将其研究发现写入一份共享黑板（见第 4 节）文档，而不仅仅是回复给协调者，以便事实核查智能体可以直接读取这些内容。
5. 协调者监听着一个"发现已就绪"的发布-订阅频道（见第 5 节），收到通知后向事实核查智能体发送一条请求："请依据当前（2020 年代）的共识核实这些论断。"
6. 事实核查智能体读取黑板内容，进行自身的核查，并将其结论以一条"inform"消息发布到同一份发现文档中。
7. 协调者读取已完成的黑板条目，并为用户综合出最终答案。
```

This trace uses a **hierarchical topology** (the coordinator dispatches and is not bypassed) that
also relies on a **shared blackboard** for the two worker agents to hand off information without a
second point-to-point round trip through the coordinator — a small hybrid, in the sense of [§6](#6-the-coordinator-role-and-swarm-topologies),
chosen because a strictly hierarchical design would force every piece of information to flow back
through the coordinator even when two workers could exchange it more directly.

这段追踪记录采用的是一种**层级拓扑**（协调者负责派发任务，且未被绕过），同时也依赖于一份**共享黑板**，使得两个工作者智能体无需再经由协调者进行第二轮点对点往返，即可完成信息交接——按照[第 6 节](#6-the-coordinator-role-and-swarm-topologies)的说法，这是一种小型混合方案，之所以如此选择，是因为一个严格的层级式设计会迫使每一条信息都必须经协调者中转，即便两个工作者本可以更直接地交换这条信息。

---

## 8. Coordination Failure Modes

**协调失效模式**

Multi-agent coordination introduces failure modes that do not exist for a single agent running the
loop from [`introductory/03`](../introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md) alone, and naming them precisely here matters because [`advanced/07`](../advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md)
builds its treatment of consensus and isolation directly on this vocabulary.

多智能体协调会引入一些单个智能体独自运行 [`introductory/03`](../introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md) 中所述循环时并不存在的失效模式，在此精确点名这些模式很重要，因为 [`advanced/07`](../advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md) 关于共识与隔离的论述，正是直接建立在这套词汇之上的。

| Failure mode                        | EN                                                                                                                                                                                                                                                                                                                                                      | 中文                                                                                                                                                                                                                                                                               |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Message storms**                  | occur when a topology with too much interconnection (a mesh with many peers, or a poorly-scoped publish-subscribe channel) causes agents to exchange far more messages than the task requires, burning cost and context-window budget ([`introductory/06`](../introductory/06-context-windows-tokens-and-memory-basics.md)) without adding information. | 发生在互联程度过高的拓扑（例如对等方众多的网状拓扑，或范围界定不当的发布-订阅频道）导致智能体交换的消息数量远超任务实际所需时，这会消耗成本与上下文窗口预算（[`introductory/06`](../introductory/06-context-windows-tokens-and-memory-basics.md)），却并未带来任何有效信息的增加。 |
| **Race conditions on shared state** | occur, as flagged in [§4](#4-shared-blackboard-systems), when two agents write to overlapping parts of a blackboard concurrently and one write silently overwrites the other.                                                                                                                                                                           | 如第 4 节所警示的那样，发生在两个智能体并发写入黑板上重叠的部分、而其中一次写入悄无声息地覆盖了另一次写入之时。                                                                                                                                                                    |
| **Coordinator bottlenecks**         | occur in a strictly hierarchical topology when every piece of information must flow through a single coordinator even when two workers could more efficiently exchange it directly — the tension the worked example in [§7](#7-a-worked-example-a-three-agent-research-assistant) deliberately relieved with a blackboard hybrid.                       | 发生在一种严格的层级拓扑中，即便两个工作者本可以更高效地直接交换某条信息，该信息也必须经由单一协调者流转——这正是第 7 节的算例特意通过引入黑板混合方案来缓解的张力。                                                                                                                |

None of these failure modes is solved by choosing a "correct" topology in the abstract; each
topology in [§6](#6-the-coordinator-role-and-swarm-topologies) trades one failure mode's likelihood against another's, which is why [`advanced/07`](../advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md)
treats worktree isolation and consensus as engineering disciplines layered on top of, not a
replacement for, the topology and messaging choices covered here.

这些失效模式都无法仅凭在抽象层面选择一种“正确”的拓扑来一劳永逸地解决；[第 6 节](#6-the-coordinator-role-and-swarm-topologies)中的每一种拓扑，都是在某种失效模式的发生概率与另一种之间做出权衡——这正是为什么 [`advanced/07`](../advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md) 将工作树隔离与共识视为叠加在本章所讲的拓扑与消息传递选择之上的工程学科，而非对它们的替代。

---

## 9. Summary and What Comes Next

**小结与后续内容**

This module gave multi-agent communication a precise vocabulary: messages structured around
performatives rather than free text ([§2](#2-what-a-message-actually-is-speech-acts-and-performatives)); request/response and its negotiation-based specialization,
the Contract Net Protocol ([§3](#3-requestresponse-and-the-contract-net-protocol)); the shared-blackboard pattern for indirect, loosely coupled
communication ([§4](#4-shared-blackboard-systems)); publish-subscribe for space-, time-, and synchronization-decoupled event
notification ([§5](#5-publish-subscribe-messaging)); and the coordinator role together with five recurring swarm topologies —
hierarchical, flat, mesh, pipeline, and hybrid ([§6](#6-the-coordinator-role-and-swarm-topologies)). Each pattern and topology is a real engineering
tradeoff, not a default to reach for automatically, and production systems typically combine several
of them, as the worked example in [§7](#7-a-worked-example-a-three-agent-research-assistant) demonstrated.

本模块为多智能体通信建立了一套精确的词汇体系：围绕施为动词而非自由文本构建的消息（[第 2 节](#2-what-a-message-actually-is-speech-acts-and-performatives)）；请求/响应模式及其基于协商的特化形式——合同网协议（[第 3 节](#3-requestresponse-and-the-contract-net-protocol)）；用于间接、松耦合通信的共享黑板模式（[第 4 节](#4-shared-blackboard-systems)）；用于时间、空间与同步三方面解耦的事件通知的发布-订阅模式（[第 5 节](#5-publish-subscribe-messaging)）；以及协调者角色，连同五种反复出现的集群拓扑——层级式、扁平式、网状式、流水线式与混合式（[第 6 节](#6-the-coordinator-role-and-swarm-topologies)）。每一种模式与拓扑都是一项真实的工程权衡，而非可以自动套用的默认选项，生产系统通常会将其中若干种组合使用，正如[第 7 节](#7-a-worked-example-a-three-agent-research-assistant)的算例所展示的那样。

`advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md` (already published in
this curriculum) picks up exactly where [§8](#8-coordination-failure-modes)'s failure modes left off, developing the full engineering
treatment of concurrent-access isolation and consensus mechanisms for when multiple agents must act
on the same resource or converge on a single trustworthy answer.
`advanced/04-agentic-safety-guardrails-and-governance-patterns.md` extends this module's coordinator
role with the guardrails needed when a coordinator's decisions carry real-world consequences.

本课程中已发布的 `advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md`，正是从[第 8 节](#8-coordination-failure-modes)所述失效模式结束的地方继续讲起，针对多个智能体必须对同一资源采取行动、或需要收敛到单一可信答案的情形，发展出关于并发访问隔离与共识机制的完整工程论述。 `advanced/04-agentic-safety-guardrails-and-governance-patterns.md` 则在本模块协调者角色的基础上，进一步讲解当协调者的决策会带来真实世界后果时所需要的护栏机制。

---

## References

**参考文献**

### External Sources

- [FIPA (Foundation for Intelligent Physical Agents). FIPA ACL Message Structure Specification (SC00061G)](https://www.fipa.org/specs/fipa00061/SC00061G.html)
- [Smith, R. G. (1980). The Contract Net Protocol: High-Level Communication and Control in a Distributed Problem Solver. IEEE Transactions on Computers, C-29(12), 1104–1113.](https://doi.org/10.1109/TC.1980.1675516)
- [Hayes-Roth, B. (1985). A Blackboard Architecture for Control. Artificial Intelligence, 26(3), 251–321.](https://doi.org/10.1016/0004-3702%2885%2990063-3)
- [Eugster, P. T., Felber, P. A., Guerraoui, R., & Kermarrec, A.-M. (2003). The Many Faces of Publish/Subscribe. ACM Computing Surveys, 35(2), 114–131.](https://doi.org/10.1145/857076.857078)
- [Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X., Zhang, S., Liu, J., Awadallah, A. H., White, R. W., Burger, D., & Wang, C. (2023). AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155)
- [Anthropic (2025). How We Built Our Multi-Agent Research System (Anthropic Engineering)](https://www.anthropic.com/engineering/multi-agent-research-system)

### Internal Cross-References

- [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](../introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md)
- [`introductory/04` — Tool Use & Function Calling Basics](../introductory/04-tool-use-and-function-calling-basics.md)
- [`introductory/06` — Context Windows, Tokens & Memory Basics](../introductory/06-context-windows-tokens-and-memory-basics.md)
- [`introductory/07` — Introduction to Multi-Agent Systems](../introductory/07-introduction-to-multi-agent-systems.md)
- [`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion](03-agent-design-patterns-react-plan-execute-reflexion.md)
- [`advanced/04` — Agentic Safety, Guardrails & Governance Patterns](../advanced/04-agentic-safety-guardrails-and-governance-patterns.md)
- [`advanced/07` — Multi-Agent Orchestration: Worktree Isolation & Consensus](../advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md)
