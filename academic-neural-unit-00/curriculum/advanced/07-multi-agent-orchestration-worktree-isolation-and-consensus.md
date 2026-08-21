# Multi-Agent Orchestration: Worktree Isolation & Consensus

**多智能体编排：工作树隔离与共识**

| Field   | English                          | 中文                              |
| ------- | -------------------------------- | --------------------------------- |
| Level   | Advanced                         | 高级                              |
| Cluster | Multi-Agent Systems & Evaluation | 多智能体系统与评估                |
| Author  | Dr. Aditi                        | ANU-00 基础人工智能首席研究科学家 |

---

Aditi Bhandari 博士

---

## 1. Introduction: From Coordination to Concurrent Execution

**导论：从协调到并发执行**

This module builds strictly on `intermediate/07` (Multi-Agent Communication & Coordination
Protocols), `intermediate/03` (Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion),
`intermediate/04` (Agent Memory Systems), `introductory/07` (Introduction to Multi-Agent Systems),
and `introductory/03` (What Is an AI Agent? Concepts & the Agent Loop) — named explicitly wherever
this chapter relies on them, per the curriculum's citation rule for intermediate/advanced modules.

本章严格建立在 `intermediate/07`（多智能体通信与协调协议）、`intermediate/03`（智能体设计模式：
ReAct、计划-执行与 Reflexion）、`intermediate/04`（智能体记忆系统）、`introductory/07`（多智能体系统
导论）以及 `introductory/03`（什么是人工智能智能体？概念与智能体循环）之上；凡本章依赖这些前置模块之
处，均按课程对中高级模块的引用规则明确点名。

`intermediate/07` established how two or more agents exchange messages — request/response
patterns, shared blackboards, and publish-subscribe channels — so that a coordinator can
assign work and collect results. That module answers the question "how do agents talk to each
other?" This module answers a harder, adjacent question: once a group of agents is talking, what
happens when several of them need to **act on the same underlying resource at the same time** —
the same codebase, the same shared document, the same decision — without one agent's work
silently clobbering another's, and without the group producing an answer that no single agent
would actually stand behind? Those are two separate engineering problems, and this chapter treats
them as such: **worktree isolation** solves the first (concurrent access to a
shared filesystem), and **consensus** solves the second (concurrent agents converging on
one trustworthy output). Multi-agent orchestration, as used throughout this
chapter, means the combined discipline of assigning work to multiple agents, keeping their
concurrent execution from interfering with each other, and combining their outputs into a single
result the system can act on.

`intermediate/07` 讨论了两个或多个智能体如何相互交换消息——请求/响应模式、共享黑板、发布-订阅通道——
从而让协调者能够分配任务并收集结果。那一章回答的是"智能体之间如何交流？"这个问题。本章
要回答一个更难、但与之紧密相关的问题：当一组智能体已经能够彼此通信之后，如果其中几个智能体需要**在同一
时刻对同一份底层资源采取行动**——同一份代码库、同一份共享文档、同一个决策——会发生什么？我们既不希望某个
智能体的工作悄无声息地覆盖了另一个智能体的成果，也不希望整个群体给出一个连任何单个智能体都不会真正认同
的答案。这是两个彼此独立的工程问题，本章也将它们分开处理：**工作树隔离**解决第
一个问题（对共享文件系统的并发访问），**共识**解决第二个问题（并发智能体如何收敛到一个
可信的输出）。本章通篇所说的多智能体编排，指的是"把任务分配给多个智能体、
防止它们的并发执行相互干扰、并将它们的输出合并为系统可以采纳的单一结果"这一整套综合性工作。

The two problems are related but not the same, and conflating them is a common design mistake.
Isolating agents' filesystem access (worktree isolation) guarantees that Agent A's uncommitted
edits cannot corrupt Agent B's uncommitted edits — it says nothing about which of Agent A's or
Agent B's _finished_ work should be kept when the two disagree. Conversely, a consensus mechanism
that decides "keep Agent A's answer, discard Agent B's" is useless if Agent A and Agent B were
editing the same live files and already corrupted each other's work before a decision could even
be reached. Production multi-agent systems need both, in that order: isolate first, so that each
agent's candidate output is a clean, independently-produced artifact; then reach consensus, so
that the group converges on one artifact to keep. This chapter builds each half in turn and then
combines them in a single worked example in §8.

这两个问题彼此相关，但并不是同一回事，把它们混为一谈是一种常见的设计错误。隔离智能体对文件系统的访问
（工作树隔离）能保证智能体 A 尚未提交的修改不会破坏智能体 B 尚未提交的修改——但它并不能告诉我们，当 A 和
B 各自"完成"的工作出现分歧时，应该保留哪一份。反过来说，一个只负责"保留 A 的答案、丢弃 B 的答案"的共识
机制，如果 A 和 B 一开始就在同一份实时文件上编辑、并且在做出决策之前就已经互相破坏了对方的工作，那么这
个共识机制也毫无意义。生产级的多智能体系统需要两者兼备，且顺序不能颠倒：先隔离，让每个智能体的候选输出
都是一份干净、独立产出的成果；再达成共识，让整个群体收敛到应当保留的那一份成果上。本章将依次构建这两个
部分，并在第 8 节的完整实例中将二者结合起来。

---

## 2. Recap: Orchestration Topologies and the Coordinator's Job

**回顾：编排拓扑与协调者的职责**

`intermediate/07` introduced the coordinator role and the message-passing protocols agents use to
report status and results back to it. This section briefly recaps the shapes that coordination
can take — the **swarm topology**, i.e. the graph structure describing which agents
communicate with which — because the topology chosen determines where isolation and consensus
need to be applied. In a **hierarchical topology**, a single coordinator dispatches
work to subordinate agents and collects their results, mirroring a tree; in a **flat
topology**, every agent reports to one orchestrator with no intermediate layer; in a
**mesh topology**, agents communicate peer-to-peer without a central coordinator; in a
**pipeline topology**, agents hand work to each other in sequence (A finishes, then
B starts on A's output); and a **hybrid topology** combines these shapes for
real-world systems that do not fit one pattern cleanly.

`intermediate/07` 已经介绍了协调者角色，以及智能体用来向协调者汇报状态和结果的消息传递协议。本节先简要
回顾一下协调可以采取的几种形态——**集群拓扑**，也就是描述"谁与谁通信"的图结构——因为
选择哪种拓扑，决定了隔离与共识需要施加在系统的哪个环节。在**层级拓扑**中，单
一协调者向下属智能体派发任务并收集结果，整体呈树状结构；在**扁平拓扑**中，每个智能体
都直接向一个编排器汇报，中间不设分层；在**网状拓扑**中，智能体之间点对点通信，不存在
中心协调者；在**流水线拓扑**中，智能体依次将工作交接给下一个智能体（A 完成后 B 才
开始处理 A 的产出）；而**混合拓扑**则将上述几种形态组合起来，用于那些无法被单一模式
完整描述的真实系统。

Worktree isolation matters most in flat and hierarchical topologies where several agents are
dispatched to work **concurrently and independently** on the same repository — the coordinator
fans work out, and the agents do not need to talk to each other while they work, only when they
report back. Consensus matters most whenever the coordinator has dispatched the _same_ question
to more than one agent on purpose — a deliberate redundancy strategy, not an accident — precisely
so that their answers can be compared and combined rather than blindly trusted from a single
source. Mesh and debate-style topologies (§7) are built around consensus from the start, since
peer agents critiquing each other's answers _is_ a consensus mechanism. Pipeline topologies
generally need neither, since each stage's output is the sole input to the next stage and there is
nothing to isolate concurrently or reconcile by vote — which is precisely why this chapter, unlike
`intermediate/07`, narrows its focus to the flat/hierarchical and mesh cases where isolation and
consensus actually do work.

工作树隔离在扁平拓扑和层级拓扑中最为关键，因为在这两种拓扑里，多个智能体被派去**并发且独立地**处理同一
个代码库——协调者把任务分发出去，智能体在各自工作期间并不需要相互交流，只有在汇报结果时才需要。共识则
在协调者**有意**把同一个问题派发给多个智能体时最为关键——这是一种刻意的冗余策略，而不是意外情况——目的
正是为了让它们各自的答案可以被比较、被综合，而不是盲目相信某一个来源。网状拓扑和辩论式拓扑（见第 7 节）
从设计之初就是围绕共识构建的，因为让若干对等智能体互相评判对方的答案，本身就是一种共识机制。流水线拓扑
通常两者都不太需要，因为每个阶段的输出就是下一阶段唯一的输入，既没有需要并发隔离的东西，也没有需要通过
投票来调和的分歧——这也正是本章不同于 `intermediate/07` 之处：本章把讨论范围收窄到隔离与共识真正发挥
作用的扁平/层级与网状场景。

---

## 3. The Filesystem Contention Problem

**文件系统争用问题**

Consider the simplest possible failure: an orchestrator dispatches two worker agents to the same
checked-out copy of a codebase, one to add a backend endpoint and one to add the corresponding
frontend component. Both agents read the same files into their context windows (a mechanism
`intermediate/07` already covers) and both begin writing edits to disk. If Agent A saves the file
`config.py` with its change, and Agent B — which read `config.py` _before_ Agent A's save — now
saves its own, unrelated change to the same file, Agent B's save silently discards Agent A's edit,
because Agent B's in-memory copy never had it. Neither agent receives an error. Neither agent
knows anything went wrong. The orchestrator sees two "success" reports and a corrupted file. This
is a **race condition**: an outcome that depends on the unpredictable relative timing
of two concurrent operations, and it is the single most common failure mode in naively-implemented
multi-agent coding systems.

设想一种最简单不过的失败情形：编排器把两个工作智能体派到同一份已检出的代码库副本上，一个负责添加后端
接口，另一个负责添加对应的前端组件。两个智能体都把同一批文件读入各自的上下文窗口（这一机制
`intermediate/07` 已经介绍过），并且都开始把修改写回磁盘。如果智能体 A 保存了它对 `config.py` 的修改，
而智能体 B——它读取 `config.py` 的时刻**早于** A 保存之前——现在也把自己那份与之无关的修改保存到同一个
文件，那么 B 的保存会悄无声息地丢弃 A 的修改，因为 B 内存中的副本从一开始就没有包含 A 的改动。两个智能体
都不会收到任何错误提示，谁也不知道出了问题。编排器看到的是两份"成功"报告，以及一个已经损坏的文件。这就是
所谓的**竞态条件**：结果取决于两个并发操作之间不可预测的相对时序，这也是设计简单粗
糙的多智能体代码系统中最常见的失败模式。

The naive fix — a single global lock so only one agent may write at a time — defeats the purpose
of running agents in parallel: the whole system degrades to sequential execution, and a slow agent
blocks every other agent behind it. What is needed instead is a mechanism that gives each agent
its own private, fully-writable copy of the working state, so agents never observe each other's
in-progress edits at all, combined with a principled way to reconcile those private copies back
into one shared result once each agent finishes. That is exactly the shape of the solution
`core-component-00`'s engineering practice adopted for this workspace's own multi-agent work, and
it is the subject of the next section.

一种朴素的修复方式——设置一把全局锁，同一时刻只允许一个智能体写入——会让并行运行智能体的意义荡然无
存：整个系统退化为串行执行，只要有一个智能体运行得慢，后面所有智能体都会被它卡住。真正需要的是一种机
制，让每个智能体都拥有一份完全私有、可自由写入的工作状态副本，使得智能体之间完全观察不到彼此正在进行
中的修改，同时再配合一套有原则的方法，在每个智能体完成工作之后，把这些私有副本重新调和为一份共享结
果。这正是本工作区 `core-component-00` 工程实践中，为其自身多智能体工作所采用的解决方案的形态，也是
下一节要讨论的主题。

---

## 4. Git Worktree Isolation as Multi-Agent Infrastructure

**将 Git 工作树隔离作为多智能体基础设施**

`intermediate/03` covers the agent loop's action-execution step at the level of a single agent
issuing a tool call. This section scales that up: when several agents each execute
file-modification tool calls concurrently, the underlying version-control system can be used to
give each one an isolated execution environment. `git worktree` is a feature of Git — the
distributed version-control system — that lets one repository support **multiple linked working
directories checked out to different branches at the same time**, all sharing the same underlying
object history (the `.git/` database), per Git's own reference documentation for the command. In
practice, this means an orchestrator can run `git worktree add ../agent-backend -b
agent/backend/dark-mode-api` to create a new directory that is a complete, independent copy of the
working tree, checked out on its own new branch, before assigning Agent A to work exclusively
inside it. A second, third, and fourth call creates equally independent directories for Agents B,
C, and D. None of them can see, let alone overwrite, another agent's uncommitted edits, because
each worktree has its own working-directory files and its own Git index (Git's staging-area
data structure) — only the compressed object history in `.git/` is shared, and Git's own object
model is append-only and content-addressed, so concurrent writers cannot corrupt it by writing to
their own worktrees.

`intermediate/03` 在单个智能体发出工具调用的层面，讨论了智能体循环中"执行动作"这一步骤。本节把这个概
念扩展到多智能体场景：当若干智能体并发地执行文件修改类工具调用时，可以利用底层的版本控制系统，为每个智
能体提供一个相互隔离的执行环境。`git worktree` 是 Git——这一分布式版本控制系统——的一项特性，根据 Git 官
方针对该命令的参考文档，它允许**一个仓库同时支持多个链接的工作目录，各自检出到不同的分支**，但底层共
享同一份对象历史（即 `.git/` 数据库）。在实践中，这意味着编排器可以执行
`git worktree add ../agent-backend -b agent/backend/dark-mode-api`，创建一个全新的目录——它是工作树
的完整、独立副本，检出在自己新建的分支上——然后再把智能体 A 单独指派到这个目录中工作。第二次、第三次、
第四次调用则可以为智能体 B、C、D 分别创建同样独立的目录。这些智能体谁也看不到、更不可能覆盖其他智能体
尚未提交的修改，因为每个工作树都拥有自己独立的工作目录文件和自己独立的 Git 索引（Git 的暂存区数据结
构）——真正共享的只有 `.git/` 中经过压缩的对象历史，而 Git 自身的对象模型是只追加、内容寻址的，因此并发
的写入者各自写入自己的工作树时，不可能破坏这份共享历史。

The full lifecycle this workspace's own multi-agent engineering practice specifies —
`core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`
— has five phases, summarized in the table below.

本工作区自身的多智能体工程实践所规定的完整生命周期——见
`core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`
——分为五个阶段，概述如下表所示。

| Phase         | Action                                                                          | Key Commands                                                |
| ------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| 1 — Provision | Orchestrator creates one isolated worktree per agent, each on a new branch      | `git worktree add ../agent-<name> -b agent/<name>/<task>`   |
| 2 — Execute   | Each agent works exclusively inside its own worktree; commits its own work      | `git add -A && git commit -m "..."`                         |
| 3 — Integrate | Orchestrator (or a dedicated integration agent) merges each agent's branch back | `git merge agent/<name>/<task> --no-ff`                     |
| 4 — Resolve   | Conflicting merges are aborted and re-dispatched, or resolved explicitly        | `git merge --abort`, or manual conflict resolution + commit |
| 5 — Clean up  | Worktrees and (optionally) branches are removed once integrated                 | `git worktree remove ../agent-<name> && git worktree prune` |

Three properties of this lifecycle are worth naming explicitly because they generalize beyond Git.
First, isolation is provisioned **before** execution, never retrofitted after two agents have
already started writing to a shared directory — isolation is a precondition, not a repair. Second,
commit messages in this workflow carry a specific attribution convention: the subject line follows
`agent/<name>: <verb-phrase>` and the body is a hyphen-bulleted list of discrete changes, because
a merge conflict three phases later is far easier to reason about when every commit says, in
`git log --author=<agent>`-readable form, exactly which agent made which change and why — this is
the audit trail a shared-lock system never provides. Third, and most important for the theme of
this chapter, **Phase 3 (Integrate) is where isolation ends and a decision must be made** — if two
agents' branches touch the same lines of the same file, Git cannot resolve that automatically, and
the orchestrator needs a principled way to decide which change wins. That decision problem is
exactly what §5 through §7 formalize.

这套生命周期中有三个特性值得特别指出，因为它们的意义超出了 Git 本身。第一，隔离是在执行**之前**就预先
配置好的，而不是等两个智能体已经开始向同一个目录写入之后再事后补救——隔离是一个前提条件，而不是一种修
复手段。第二，这套工作流中的提交信息带有特定的归属约定：主题行遵循 `agent/<name>: <动词短语>` 的格
式，正文则是以连字符列出的具体改动清单，因为三个阶段之后如果出现合并冲突，如果每一次提交都能以
`git log --author=<agent>` 可读的形式清楚说明是哪个智能体做了什么改动、为什么这么做，那么排查起来会容
易得多——这正是共享锁机制永远无法提供的审计轨迹。第三点，也是与本章主题最相关的一点：**第 3 阶段（集
成）正是隔离结束、必须做出决策的时刻**——如果两个智能体的分支修改了同一份文件的相同代码行，Git 无法自
动解决这种冲突，编排器需要一套有原则的方法来判断应当采纳哪一方的改动。而这正是第 5 节到第 7 节要形式
化处理的决策问题。

Worktree isolation has real operational failure modes of its own, and this workspace's own
multi-agent engineering practice has an instructive, documented case: an agent once needed a new
worktree to access a large, slow-to-populate shared cache directory without re-downloading it, and
used a Windows directory _junction_ — a filesystem-level alias — to point the worktree at the real
shared directory instead of copying it. When that worktree was later removed with `git worktree
remove`, Git's recursive cleanup followed the junction as an ordinary subdirectory and deleted the
shared cache's actual contents in the main repository, not a copy. The lesson generalizes past
Git: **isolation that is implemented as an alias to shared storage is not isolation** — it is a
label on top of shared mutable state, and any tool that assumes "this directory is disposable"
will eventually treat the alias as disposable too. The rule this workspace now enforces — copy
large shared assets into a new worktree rather than symlinking or junctioning them in — is a
direct, worked consequence of that incident, and a useful cautionary example of how an isolation
mechanism can be quietly undermined by a shortcut that looks harmless in the moment it is taken.

工作树隔离本身也存在真实的运维层面的失败模式，本工作区自身的多智能体工程实践中就有一个颇具启发性、且
已被记录在案的案例：某个智能体曾经需要让一个新的工作树访问一个体积庞大、填充缓慢的共享缓存目录，为了
避免重新下载，它没有直接复制这个目录，而是使用了 Windows 的目录**联接**——一种文件系统层
面的别名——让工作树指向真实的共享目录。后来这个工作树被 `git worktree remove` 移除时，Git 的递归清理
逻辑把这个联接当作了一个普通子目录来处理，结果删除的是主仓库中共享缓存的**真实内容**，而不是某份副
本。这个教训的意义超出了 Git 本身：**用指向共享存储的别名来实现的"隔离"，根本不是真正的隔离**——它只是
在共享的可变状态之上贴了一层标签，任何认为"这个目录可以随意丢弃"的工具，迟早也会把这个别名本身当作可
以随意丢弃的东西。本工作区现在强制执行的规则——把大型共享资源复制进新的工作树，而不是用符号链接或联接
的方式引入——正是这次事故所直接得出的、经过实践检验的结论，也是一个很好的警示案例，说明一种隔离机制是
如何被一个当下看似无害的捷径悄悄破坏的。

---

## 5. Foundations of Distributed Consensus

**分布式共识的理论基础**

Worktree isolation solves the problem of agents not interfering with each other's work-in-progress.
It says nothing about what happens at Phase 3 (Integrate) when two agents' _finished_ work
genuinely conflicts, or — the case this chapter is really building toward — when an orchestrator
deliberately sends the same question to several agents and needs a principled way to pick one
answer from several independently-produced candidates. This is the **consensus
problem**: getting a group of independent actors to agree on a single value, even
though each actor only has partial information and no actor can simply command the others. The
field of **distributed consensus** — the study of this problem for computer
processes rather than human generals — is a decades-old branch of distributed-systems theory, and
it gives multi-agent LLM orchestration a rigorous vocabulary and a set of hard limits worth
knowing before inventing an ad-hoc voting scheme.

工作树隔离解决的是"智能体之间不干扰彼此进行中的工作"这一问题，但它并没有回答：当第 3 阶段（集
成）中，两个智能体**已完成**的工作确实发生了冲突时应当怎么办；更进一步——也是本章真正想要引向的场
景——当编排器有意把同一个问题发给多个智能体、并需要从若干独立产出的候选答案中挑出一个时，又应当怎么
办。这就是**共识问题**：如何让一组独立的行动者就单一的值达成一致，即便每个行动
者只掌握部分信息，也没有任何一个行动者能够简单地命令其他人服从。**分布式共识**这一领域——即针对计算机进程而非人类将军研究这一问题——是分布式系统理论中一个已有数十年历
史的分支，它为多智能体大语言模型编排提供了一套严谨的词汇体系，以及一系列在着手设计任何临时投票方案之
前就值得了解的硬性限制。

A consensus protocol is formally judged against three properties. **Agreement** requires that no
two non-faulty participants decide on different final values. **Validity** requires that the
decided value was actually proposed by some participant, not invented out of nowhere. And
**termination** requires that every non-faulty participant eventually decides _something_ — the
protocol cannot stall forever. It might seem obvious that a correct protocol satisfying all three
should always be achievable, but Michael Fischer, Nancy Lynch, and Michael Paterson proved
otherwise in a landmark 1985 result generally known as the **FLP impossibility
result（FLP 不可能性结果）**: in a fully asynchronous system — one where there is no bound on how
long a message may take to arrive — no deterministic consensus protocol can guarantee all three
properties if even a single participant may crash. This does not mean real systems cannot reach
consensus in practice; Paxos and Raft (§6) both do, routinely. It means every practical consensus
protocol has to give up _some_ theoretical guarantee — usually guaranteed termination in the
worst case — in exchange for working reliably under realistic conditions, and any multi-agent
architect should know that "always converges, always agrees, always terminates" is not a
combination any protocol can promise unconditionally.

一个共识协议在形式上要接受三条性质的检验。**一致性**要求任何两个非故障的参与者都不能各
自选定不同的最终值。**有效性**要求最终选定的值确实是由某个参与者提出的，而不是凭空捏造出
来的。**终止性**则要求每个非故障的参与者最终都能得出**某个**决定——协议不能永远悬而不
决。或许有人会觉得，一个同时满足这三条性质的正确协议理应总能实现，但 Michael Fischer、Nancy Lynch 与
Michael Paterson 在 1985 年的一项里程碑式成果中证明了并非如此，这一结果通常被称为 **FLP 不可能性结
果（FLP impossibility result）**：在一个完全异步的系统中——即消息到达所需时间没有任何上限的系统——哪
怕只有一个参与者可能崩溃，也不存在任何确定性的共识协议能够同时保证这三条性质。这并不意味着真实系统在
实践中无法达成共识；Paxos 和 Raft（见第 6 节）都在日常运行中做到了这一点。它真正的含义是：任何实用的
共识协议都必须放弃**某种**理论上的保证——通常是最坏情况下的终止性保证——才能换取在现实条件下的可靠运
行，任何一位多智能体架构师都应当明白，"永远收敛、永远一致、永远终止"这三者的组合，是没有任何协议能够
无条件承诺的。

---

## 6. Classical Consensus Algorithms: Paxos, Raft, and Byzantine Fault Tolerance

**经典共识算法：Paxos、Raft 与拜占庭容错**

**Paxos（Paxos 算法）**, introduced by Leslie Lamport, is the algorithm most often cited as the
founding practical solution to distributed consensus under crash faults (participants that stop
responding but never send incorrect information) — Lamport's own later paper, written because he
felt the original presentation was needlessly hard to follow, restates it "in plain English" and
is titled, fittingly, "Paxos Made Simple." The core idea is a two-phase protocol: a participant
wanting to propose a value first sends a "prepare" message with a proposal number to a majority of
participants, and only if a majority promises not to accept any older proposal does it proceed to
an "accept" phase, again requiring a majority to agree before the value is considered chosen. The
majority requirement is the load-bearing idea: any two majorities of a fixed group must overlap by
at least one member, so a second, later proposal is guaranteed to encounter at least one
participant who already knows about the first — which is exactly the mechanism that prevents two
different values from both being "chosen."

**Paxos 算法（Paxos）** 由 Leslie Lamport 提出，通常被认为是针对崩溃故障（即参与者停止响应、但从不发
送错误信息）情形下分布式共识问题最早的实用解法——Lamport 本人后来又写了一篇论文，因为他觉得最初的讲述
方式不必要地难以理解，于是用"通俗英语"重新阐述了一遍，恰如其分地取名为《Paxos Made Simple》（Paxos
其实很简单）。其核心思想是一个两阶段协议：想要提出某个值的参与者，首先向多数参与者发送带有提案编号的
"准备"消息，只有当多数参与者都承诺不再接受任何更早的提案时，它才会进入"接受"阶
段，同样需要多数参与者同意，该值才被视为已经"选定"。这里的"多数"要求正是整个机制的支撑所在：在一个固
定的群体中，任意两个多数派集合必然至少有一名成员重叠，因此任何一个更晚提出的提案，都必然会遇到至少一
位已经知晓前一个提案的参与者——而这正是防止两个不同的值同时被"选定"的关键机制。

**Raft（Raft 算法）**, introduced by Diego Ongaro and John Ousterhout in a 2014 USENIX paper
titled "In Search of an Understandable Consensus Algorithm," was designed explicitly to produce
the same guarantees as Paxos while being easier for engineers to understand and implement
correctly — the paper reports a user study in which Raft was measurably easier for students to
learn. Raft decomposes consensus into three separable sub-problems: **leader
election**, where participants vote to select a single leader for a fixed
period called a **term**; **log replication**, where the elected leader
appends new entries to a shared, ordered log and replicates them to the other participants; and
safety, ensuring that once a log entry is replicated to a majority, it can never be overwritten,
even across leader changes. Both Paxos and Raft rely on the same numerical threshold: with $n$
total participants, a **quorum** — the smallest set guaranteed to overlap with any
other such set — is $\lfloor n/2 \rfloor + 1$. For a five-participant cluster ($n = 5$), the quorum
is $\lfloor 5/2 \rfloor + 1 = 3$; for a seven-participant cluster, it is $4$. This single formula
is the mathematical backbone of every majority-vote consensus mechanism this chapter discusses,
including the semantic, LLM-output voting schemes in §7.

**Raft 算法（Raft）** 由 Diego Ongaro 与 John Ousterhout 在 2014 年 USENIX 会议上发表的论文《In
Search of an Understandable Consensus Algorithm》（寻找一种易于理解的共识算法）中提出，其设计目标就
是在保证与 Paxos 相同正确性的前提下，让工程师更容易正确理解和实现——论文中报告的一项用户研究显示，学生
学习 Raft 的效果在可测量的意义上确实更好。Raft 把共识问题拆解为三个可以分开处理的子问题：**领导者选
举**，即参与者投票选出一位领导者，任期为一个固定的**任期**；**日志复
制**，即当选的领导者把新的条目追加到一份共享的、有序的日志中，并将其复制给其他参
与者；以及安全性，确保一旦某条日志条目被复制到多数参与者，即便领导者发生更替，它也永远不会被覆盖。
Paxos 与 Raft 都依赖同一个数值门槛：在共有 $n$ 名参与者的情况下，**法定人数**——即能够保证
与任何其他这样的集合发生重叠的最小集合——为 $\lfloor n/2 \rfloor + 1$。对于一个五参与者集群
（$n = 5$），法定人数是 $\lfloor 5/2 \rfloor + 1 = 3$；对于一个七参与者集群，则是 $4$。这一个公式正
是本章讨论的每一种多数投票共识机制的数学骨架，其中也包括第 7 节将要介绍的、针对大语言模型输出的语义投
票方案。

Both Paxos and Raft assume **crash faults** only — a faulty participant simply stops
responding, but never sends deliberately false or contradictory information to different peers.
That assumption does not hold for adversarial or malfunctioning participants, and Leslie Lamport,
Robert Shostak, and Marshall Pease's 1982 paper "The Byzantine Generals Problem" formalizes the
harder case: several generals must agree on a common battle plan by messenger, but some generals
are traitors who may send contradictory messages to different peers to prevent agreement. This
is **Byzantine fault tolerance** — consensus that must survive participants who
actively lie, not merely participants who go silent — and the paper's central quantitative result
is that if participants can only exchange oral (unsigned, un-provenanced) messages, no protocol
can guarantee agreement unless more than two-thirds of participants are loyal. Restated
algebraically: for $n$ total participants and $f$ traitors, agreement requires $n > 3f$, i.e.
$n \geq 3f + 1$. Worked example: to tolerate $f = 1$ Byzantine (actively malicious or
unpredictably-wrong) participant, a system needs at least $n = 4$ total participants; to tolerate
$f = 2$, it needs at least $n = 7$. This threshold reappears, in an approximate and informal form,
wherever multi-agent LLM systems must decide how many independent agents to field before a
majority vote can be trusted against one or two agents that hallucinate or are adversarially
prompted — the subject of §7 and the failure modes in §9.

Paxos 与 Raft 都只假设**崩溃故障**——出故障的参与者只是停止响应，而绝不会向不同的对
等方故意发送虚假或自相矛盾的信息。这个假设对于存在恶意或功能失常参与者的场景并不成立，Leslie
Lamport、Robert Shostak 与 Marshall Pease 在 1982 年发表的论文《The Byzantine Generals
Problem》（拜占庭将军问题）正是把这种更困难的情形形式化：若干将军必须通过信使就共同的作战计划达成一
致，但其中一些将军是叛徒，可能向不同的对等方发送相互矛盾的消息，以阻止大家达成一致。这就是**拜占庭容
错**——共识必须能够在存在主动撒谎的参与者、而不仅仅是沉默不响应的参与者
的情况下依然成立——该论文的核心定量结论是：如果参与者之间只能交换口头（未签名、无法溯源）的消息，那么
除非超过三分之二的参与者是忠诚的，否则任何协议都无法保证达成一致。用代数方式重新表述：在共有 $n$ 名参
与者、其中 $f$ 名为叛徒的情况下，达成一致要求 $n > 3f$，即 $n \geq 3f + 1$。举一个具体例子：要容忍
$f = 1$ 个拜占庭（主动恶意或不可预测地出错）参与者，系统至少需要 $n = 4$ 名参与者；要容忍 $f = 2$
个，则至少需要 $n = 7$ 名。每当多智能体大语言模型系统需要决定，在多数投票能够对抗一到两个产生幻觉或被
对抗性提示操纵的智能体之前，应当部署多少个独立智能体时，这一门槛就会以一种近似、非正式的形式再次出
现——这正是第 7 节以及第 9 节失败模式部分要讨论的主题。

---

## 7. Semantic Consensus Among LLM Agents

**大语言模型智能体之间的语义共识**

Paxos, Raft, and Byzantine fault tolerance were all designed for participants voting on a single,
discrete, exactly-comparable value — a specific log entry, a specific committed transaction, where
"agreement" means bitwise equality. Multiple LLM agents answering the same open-ended question
almost never produce bitwise-identical outputs, even when they agree in substance: one agent might
write "the answer is 42" and another "42 is correct," and treating those as disagreeing values
the way Raft would treat two different log entries misses the point entirely. Multi-agent LLM
orchestration therefore needs **semantic consensus**: agreement on the _meaning_ or
_correctness_ of an answer, not on its literal string representation. This section covers four
concrete, published mechanisms — building on `intermediate/03`'s coverage of the single-agent
ReAct and Reflexion loops, since each mechanism below is best understood as running several
instances of that loop and combining their outputs.

Paxos、Raft 与拜占庭容错协议，设计的初衷都是让参与者就单一、离散、可以逐位精确比较的值进行投票——比如
某一条具体的日志条目、某一笔具体的已提交事务，其中的"一致"意味着逐位相等。而多个大语言模型智能体在回
答同一个开放式问题时，几乎从不会产生逐位相同的输出，即便它们在实质内容上是一致的：一个智能体可能写
"答案是 42"，另一个写"42 是正确的"，如果像 Raft 处理两条不同日志条目那样，把这两者当作互相矛盾的值来
处理，就完全偏离了问题的本质。因此，多智能体大语言模型编排需要的是**语义共识**：就答案的**含义**或**正确性**达成一致，而不是就其字面上的字符串表示达成一致。本节将介
绍四种已在文献中发表的具体机制——它们建立在 `intermediate/03` 已经讲授的单智能体 ReAct 与 Reflexion
循环之上，因为理解下面每一种机制的最佳方式，都是把它看作并行运行多个该循环的实例、再对其输出进行综
合。

The simplest mechanism is **self-consistency（自洽性）**, introduced by Xuezhi Wang and
co-authors in a 2022 paper. Instead of generating one chain-of-thought reasoning path with greedy
decoding, the model samples several independent reasoning paths for the same question — each is
effectively an independent "vote" — and the final answer is chosen by a **plurality
vote** over the paths' final answers, marginalizing out the specific reasoning
that produced each one. Worked example: given five sampled reasoning paths that conclude "A," "A,"
"B," "A," and "C" respectively, self-consistency selects "A" with 3 of 5 votes, discarding the
specific chains of reasoning that produced "B" and "C" even though those chains might individually
look plausible. The intuition, as the original paper puts it, is that a genuinely correct answer
tends to be reachable by multiple different lines of reasoning, while an incorrect answer is less
likely to be reached the same way twice by independent sampling.

最简单的机制是 **自洽性（self-consistency）**，由 Xuezhi Wang 及其合著者在 2022 年的一篇论文中提出。
它不再用贪婪解码只生成一条思维链推理路径，而是针对同一个问题采样若干条相互独立的推理路径——每一条实
质上都相当于一次独立的"投票"——最终答案则通过对各条路径得出的最终结论进行**相对多数投票**来选出，同时边缘化（忽略）掉产生每个结论的具体推理过程。举一个具体例子：假设采样得到五条推理
路径，分别得出结论"A"、"A"、"B"、"A"、"C"，自洽性方法会以 5 票中的 3 票选出"A"，即便得出"B"和"C"的那
两条推理链单独看起来也可能颇为合理，也会被舍弃。正如原论文所说，其直觉在于：一个真正正确的答案往往能
够通过多条不同的推理路径得到，而一个错误的答案，在独立采样下被同一结论重复命中的可能性则要低得多。

Self-consistency samples one model repeatedly; **multiagent debate（多智能体辩论）**, introduced
by Yilun Du and co-authors in a 2023 paper (published at ICML 2024), instead runs several separate
agent instances that each independently answer the same question, then shows every agent the other
agents' answers and reasoning and asks each to reconsider and possibly revise its own answer,
repeating for several rounds before taking a final vote. The paper reports that this debate process
measurably improves both mathematical/strategic reasoning accuracy and factual accuracy, reducing
hallucinated claims relative to any single agent answering alone, framing the effect as a "society
of minds" in which agents' individual errors are corrected by exposure to disagreement rather than
by any one agent being individually more careful. Layered on top of debate, **Mixture-of-Agents
(智能体混合架构)**, introduced by Junlin Wang and co-authors in a 2024 paper, formalizes a
multi-layer architecture: a first layer of several "proposer" agents each generates an independent
answer, and each subsequent layer's agents receive _all_ of the previous layer's answers as
additional context and synthesize an improved answer from them, with the final layer's single
"aggregator" agent producing the system's output. The paper reports that this layered
proposer-aggregator structure, built entirely from open-source models, achieved state-of-the-art
scores on the AlpacaEval 2.0, MT-Bench, and FLASK benchmarks, surpassing GPT-4 Omni on AlpacaEval
2.0 (65.1% vs. 57.5%) at the time of publication.

自洽性方法是对同一个模型反复采样；而**多智能体辩论（multiagent debate）**——由 Yilun Du 及其合著者在
2023 年发表、并于 ICML 2024 上正式刊出的论文提出——采取的做法则不同：运行若干个各自独立的智能体实
例，让它们各自独立地回答同一个问题，然后把每个智能体的答案和推理过程展示给其他所有智能体，请每个智能
体重新考虑、并可能修正自己的答案，如此重复若干轮，最后再进行一次投票得出最终结果。该论文报告称，这种
辩论过程能够可测量地提升数学/策略推理的准确率以及事实性准确率，相比单个智能体独立作答，能显著减少幻
觉性论断的产生，并将这种效应称为一种"群体思维"：智能体各自的错误，是通过接触到彼
此的分歧而得到纠正的，而不是依靠某一个智能体个体变得更加谨慎。在辩论机制之上，**智能体混合架构
（Mixture-of-Agents）**——由 Junlin Wang 及其合著者在 2024 年的论文中提出——进一步将多层架构形式化：
第一层由若干个"提议者"智能体各自独立生成一个答案，随后每一层的智能体都会接收**上一层全部
的答案**作为额外上下文，并在此基础上综合出一个改进后的答案，最后一层由单个"聚合者"智能
体产出系统的最终输出。该论文报告称，这种完全由开源模型构建的分层"提议者-聚合者"结构，在 AlpacaEval
2.0、MT-Bench 与 FLASK 等基准测试上取得了当时最先进的成绩，在 AlpacaEval 2.0 上甚至超过了 GPT-4
Omni（65.1% 对 57.5%）。

None of these three mechanisms specify _how_ the independent agent instances are actually run
concurrently, communicate, or are orchestrated at the systems level — that is an orchestration
framework's job, not a consensus algorithm's job. **AutoGen（AutoGen 框架）**, introduced by
Qingyun Wu and co-authors in a 2023 paper, is an open-source framework built for exactly this:
it provides customizable, "conversable" agents that can be composed into flexible multi-agent
conversation patterns — including debate-like and voting-like patterns — using a mix of LLM calls,
tool use, and human input, and the paper reports empirical case studies spanning mathematics,
coding, question answering, and other domains. A related but distinct line of work is Joon Sung
Park and co-authors' 2023 "Generative Agents" paper, which demonstrates that giving individual
agents a persistent memory stream, a periodic reflection step that synthesizes raw memories into
higher-level insights, and a retrieval mechanism to recall relevant memories — concepts
`intermediate/04` covers in depth for a single agent — is sufficient to produce _emergent_
coordinated behavior across a population of agents (for example, several agents independently
organizing a shared social event) without any explicit consensus vote at all. This is a genuinely
important contrast for a multi-agent architect to hold in mind: consensus mechanisms like
self-consistency, debate, and Mixture-of-Agents are **explicit** protocols that an orchestrator
runs on demand to answer one question at a time, while Generative Agents' emergent coordination is
an **implicit** property that arises from individually-memoried, individually-reflecting agents
observing and reacting to each other over an extended simulated timeline — the two are not
competing techniques so much as different tools for different orchestration topologies (§2):
explicit consensus for flat/hierarchical dispatch of a bounded question, emergent coordination for
open-ended mesh-topology agent populations.

上述三种机制都没有具体规定，这些独立的智能体实例究竟应当**如何**在系统层面被真正并发运行、如何通信、
如何被编排——这是编排框架的职责，而不是共识算法本身的职责。**AutoGen（AutoGen 框架）**——由 Qingyun
Wu 及其合著者在 2023 年的论文中提出——正是为此而生的一个开源框架：它提供了可定制、"可对话"的智能体，
可以组合出灵活多样的多智能体对话模式——包括类似辩论、类似投票的模式——综合运用大语言模型调用、工具使
用与人工输入，论文中还报告了涵盖数学、编程、问答等多个领域的实证案例研究。与之相关但又有所不同的另一
条研究脉络，是 Joon Sung Park 及其合著者 2023 年发表的《Generative Agents》（生成式智能体）论文，该
论文证明：给单个智能体配备一条持续的记忆流、一个能把原始记忆定期综合为更高层次洞见的反思步骤，以及一
套用于回忆相关记忆的检索机制——这些概念 `intermediate/04` 已针对单个智能体做过深入讲解——就足以在一
个智能体群体中产生**涌现式的**协同行为（例如，若干智能体各自独立地组织起一场共同的社交活动），而完全
不需要任何显式的共识投票。这一对比对多智能体架构师而言意义重大：自洽性、辩论、智能体混合架构这类共识
机制，是编排器按需运行、用来一次回答一个具体问题的**显式**协议；而生成式智能体的涌现式协同，则是拥有
各自记忆、各自反思能力的智能体，在一段延展的模拟时间线上彼此观察、彼此回应而自然产生的一种**隐式**特
性——二者与其说是相互竞争的技术，不如说是适用于不同编排拓扑（见第 2 节）的不同工具：面向有边界问题的
扁平/层级式派发场景，适合用显式共识；面向开放式的网状拓扑智能体群体，则适合用涌现式协同。

---

## 8. Worked Example: A Three-Agent Code-Review Swarm with Isolation and Consensus

**完整实例：一个三智能体代码评审集群中的隔离与共识**

This section combines §4 and §7 into one concrete pipeline, following the isolate-then-reconcile
ordering argued for in §1. Suppose an orchestrator needs to implement one bug fix and wants higher
confidence in the result than a single agent's first attempt would give, so it deliberately
dispatches the _same_ bug-fix task to three worker agents in parallel — this is the redundancy
strategy referenced in §2, not an accident of scheduling.

本节把第 4 节与第 7 节结合成一条具体的流程，遵循第 1 节所论证的"先隔离、后调和"顺序。假设编排器需要修
复一个 bug，并且希望得到比单个智能体第一次尝试更高的置信度，于是它有意将**同一个**修复任务并行派发给
三个工作智能体——这正是第 2 节所提到的冗余策略，而不是调度上的偶然巧合。

**Step 1 — Isolate (Phase 1–2 of §4's lifecycle).** The orchestrator provisions three worktrees,
one per agent, each on its own branch, before any agent begins working:

**第一步——隔离（对应第 4 节生命周期的第 1–2 阶段）。** 编排器在任何智能体开始工作之前，先为三个智能
体各自配置一个独立的工作树，每个都检出在自己的分支上：

```bash
git worktree add ../agent-alpha -b agent/alpha/fix-null-pointer
git worktree add ../agent-beta  -b agent/beta/fix-null-pointer
git worktree add ../agent-gamma -b agent/gamma/fix-null-pointer
```

Each agent reads the bug report, works exclusively inside its own directory, and commits its own
candidate fix with an attributed commit message, exactly as §4 describes. Because the three
worktrees share no working-directory state, all three agents can genuinely run concurrently — none
can observe, let alone disturb, either of the other two's in-progress edits.

每个智能体读取 bug 报告，只在自己的目录中工作，并按照第 4 节所述的方式，用带有明确归属的提交信息提交
自己的候选修复方案。由于这三个工作树不共享任何工作目录状态，三个智能体可以真正做到并发运行——谁也观
察不到、更不可能干扰另外两个智能体正在进行中的修改。

**Step 2 — Reconcile by semantic consensus (before Phase 3's merge).** The orchestrator now has
three independently-produced diffs, not three votes on a single discrete value, so a naive
`majority_merge` over the raw diff text would be useless (the three fixes will almost never be
character-identical even if all three are correct). Instead, following the debate-style approach
of §7, the orchestrator shows all three diffs, plus the original bug report, to a fourth,
independent LLM call acting as an aggregator — the Mixture-of-Agents pattern's final layer — and
asks it to judge which of the three candidate fixes correctly and completely resolves the bug, or
to synthesize a better fix informed by all three if none is fully correct. This is deliberately
_not_ a plurality vote over three near-identical patches, because unlike self-consistency's
short, easily-clustered final answers ("A" vs. "B" vs. "C"), full code diffs rarely repeat
verbatim across independent agents even when they agree in substance — an LLM-judged synthesis, in
the spirit of Mixture-of-Agents' aggregator layer, is the right tool here, while a literal
plurality vote remains the right tool for short, clusterable answers like the self-consistency
example in §7.

**第二步——通过语义共识进行调和（在第 3 阶段合并之前）。** 此时编排器手上有三份各自独立产出的差异，
而不是针对单一离散值的三张选票，因此如果对原始 diff 文本做一次朴素的 `majority_merge` 多数
匹配，几乎不会有任何用处（即便三个修复方案都是正确的，它们的文本内容也几乎不可能逐字相同）。因此，按
照第 7 节介绍的辩论式方法，编排器把三份 diff 连同原始的 bug 报告一起，交给第四次独立的大语言模型调
用——扮演聚合者的角色，对应智能体混合架构的最后一层——请它判断这三个候选修复方案中，哪一个正确而完整
地解决了这个 bug；如果三者都不完全正确，则请它综合三者的信息，给出一个更好的修复方案。这里刻意**不**
采用对三份近似相同补丁的相对多数投票，因为与自洽性方法中简短、易于聚类的最终答案（"A" 对 "B" 对
"C"）不同，完整的代码 diff 即便在实质上一致，也很少会在独立智能体之间逐字重复——按照智能体混合架构中
聚合层的思路，由大语言模型判定并综合，才是这里合适的工具；而对于第 7 节自洽性示例中那种简短、可聚类
的答案，字面上的相对多数投票仍然是合适的工具。

**Step 3 — Integrate and clean up (Phases 3–5 of §4's lifecycle).** Once the aggregator selects
(or synthesizes) a winning fix, the orchestrator merges only that branch into the main line, and
removes all three worktrees regardless of which one "won" — the losing agents' worktrees are
disposable precisely because they were isolated and their work was fully captured in a commit
before being discarded, not lost mid-edit the way the race condition in §3 would have lost it.

**第三步——集成与清理（对应第 4 节生命周期的第 3–5 阶段）。** 一旦聚合者选定（或综合）出获胜的修复方
案，编排器就只将那一个分支合并回主线，并且**无论哪个智能体"获胜"**，都会移除全部三个工作树——落选智
能体的工作树之所以可以被随意丢弃，正是因为它们始终处于隔离状态，其工作成果在被丢弃之前已经被完整地记
录在一次提交之中，而不会像第 3 节所述的竞态条件那样，在编辑过程中就被悄悄丢失。

---

## 9. Failure Modes and Anti-Patterns

**失败模式与反模式**

Three failure modes recur across production multi-agent orchestration systems, and each maps
directly onto a concept introduced earlier in this chapter. The first is **isolation-by-alias**,
the junction incident of §4: an engineer implements what looks like isolation but is actually a
pointer into shared mutable state, and the failure only surfaces when a cleanup operation treats
the alias as disposable. The general defense is the rule already stated in §4 — copy shared
resources into an isolated worktree rather than aliasing them in — and, more broadly, to treat
"is this actually a private copy, or just a pointer to something shared?" as a standing question
whenever an isolation mechanism is introduced.

生产环境中的多智能体编排系统反复出现三类失败模式，每一类都能直接对应到本章前面介绍过的某个概念。第一
类是**"以别名冒充隔离"**，即第 4 节中提到的目录联接事故：工程师实现的东西看起来像是隔离，实际上却只
是指向共享可变状态的一个指针，而这种失败只有在某次清理操作把这个别名当作可丢弃对象处理时，才会真正暴
露出来。通用的防范措施，就是第 4 节已经给出的规则——把共享资源复制进隔离的工作树中，而不是用别名指向
它们——更广泛地说，是要养成一种习惯：每当引入某种隔离机制时，都要反复自问"这究竟是一份真正的私有副
本，还是只是指向某个共享对象的指针？"

The second is treating a plurality vote as if it were Byzantine fault-tolerant when it is not. If
an orchestrator dispatches a question to only three agents and takes a simple plurality vote, and
one of those three agents is compromised, adversarially prompted, or simply hallucinating with
high confidence, that single faulty agent can already break a 2-vs-1 vote into a tie, or worse, can
be joined by a second agent that independently makes the same class of mistake (LLM errors are not
always independent — several agents given the same flawed prompt or the same misleading context
may fail identically). The Byzantine Generals result from §6 gives the actual threshold: tolerating
$f$ Byzantine-faulty agents among the group needs $n \geq 3f + 1$ agents, not $n = 2f + 1$ as a
simple crash-fault majority scheme would suggest — three agents give zero Byzantine fault
tolerance ($n \geq 3f+1$ with $f \geq 1$ requires $n \geq 4$), which is a genuine limitation of the
naive three-agent version of §8's worked example that a careful orchestrator design should account
for by fielding at least four independent agents if adversarial or correlated failure is a real
concern, or by using an aggregator's judgment (as §8 actually does) rather than a bare vote, since
an LLM aggregator reasoning over the content of each candidate is not subject to the same
"one bad vote breaks a plurality" arithmetic as literal ballot-counting.

第二类是把一个相对多数投票误当作具备拜占庭容错能力，而实际上并非如此。如果编排器只把问题派发给三个智
能体、并进行简单的相对多数投票，而这三个智能体中有一个被攻陷、被对抗性提示词操纵、或只是以很高的置信度
产生了幻觉，那么这一个出故障的智能体就足以把一次 2 比 1 的投票拉成平局，甚至更糟——还可能被第二个独立
犯下同类错误的智能体"呼应"（大语言模型的错误并不总是相互独立的：如果几个智能体拿到的是同一个存在缺陷
的提示词，或者同一份具有误导性的上下文，它们完全可能犯下完全相同的错误）。第 6 节中拜占庭将军问题给
出的结论正是实际的门槛：要在一组智能体中容忍 $f$ 个拜占庭故障智能体，需要 $n \geq 3f + 1$ 个智能体，
而不是像简单的崩溃故障多数方案所暗示的那样只需要 $n = 2f + 1$——三个智能体的拜占庭容错能力实际上为零
（当 $f \geq 1$ 时，$n \geq 3f+1$ 要求 $n \geq 4$），这正是第 8 节完整实例中那个简单三智能体版本存
在的真实局限性；如果对抗性或相关性故障确实是一个需要认真考虑的问题，谨慎的编排器设计应当至少部署四个
独立的智能体，或者像第 8 节实际所做的那样，采用聚合者的判断而非单纯计票，因为一个针对每份候选方案内
容进行推理的大语言模型聚合者，并不会像逐票统计那样，受到"一票坏票就能打破多数"这种简单算术规则的支
配。

The third is skipping isolation entirely because consensus is being used, on the mistaken
assumption that a later voting or judging step will "catch" any damage done by concurrent,
unisolated writes. It will not: as §3 showed, a race condition can silently destroy one agent's
work before that agent ever produces a candidate output to vote on in the first place — there is
nothing left for a consensus mechanism to evaluate. This is precisely why §1 insisted on the
isolate-then-reconcile ordering and why §8's worked example provisions all three worktrees before
any agent begins working: consensus mechanisms adjudicate between _complete, independently
produced_ candidates, and they cannot repair a candidate that was corrupted before it was ever
finished.

第三类是"因为用了共识机制，就干脆跳过隔离"，其错误假设在于：认为后续的投票或评判环节能够"兜住"并发的
非隔离写入所造成的任何损害。事实并非如此：正如第 3 节所展示的，竞态条件完全可能在某个智能体产出任何
可供投票的候选结果**之前**，就悄无声息地破坏了它的工作成果——到那时，根本没有东西可以留给共识机制去
评判。这正是第 1 节坚持"先隔离、后调和"这一顺序的原因，也是第 8 节完整实例在任何智能体开始工作之前就
先为全部三个智能体配置好工作树的原因：共识机制评判的是**完整、独立产出**的候选方案，它无法修复一个在
尚未完成之前就已经被破坏的候选方案。

---

## 10. Summary

**小结**

This chapter separated two problems that multi-agent orchestration systems routinely conflate:
keeping concurrent agents from corrupting each other's in-progress work (worktree isolation,
built on Git's linked-working-directory feature and this workspace's own five-phase lifecycle),
and combining multiple agents' finished, independent outputs into one trustworthy result
(consensus, ranging from classical crash-fault and Byzantine-fault distributed algorithms — Paxos,
Raft, and the Byzantine Generals result — through the semantic-consensus mechanisms purpose-built
for LLM agents — self-consistency, multiagent debate, and Mixture-of-Agents — to the emergent,
implicit coordination demonstrated by memory-and-reflection-equipped Generative Agents). The
worked three-agent code-review swarm in §8 showed both halves working together in the correct
order, and §9's three failure modes each showed what breaks when that order, or the underlying
fault-tolerance arithmetic, is not respected.

本章把多智能体编排系统中经常被混为一谈的两个问题分开处理：一是防止并发的智能体相互破坏彼此正在进行中
的工作（工作树隔离，建立在 Git 的链接工作目录特性以及本工作区自身的五阶段生命周期之上），二是把多个智
能体各自独立完成的输出综合为一个可信的结果（共识，涵盖从经典的崩溃故障与拜占庭故障分布式算法——
Paxos、Raft 以及拜占庭将军问题的结论——到专为大语言模型智能体设计的语义共识机制——自洽性、多智能体辩
论与智能体混合架构——再到配备记忆与反思能力的生成式智能体所展现出的涌现式、隐式协同）。第 8 节中三智
能体代码评审集群的完整实例，展示了这两部分如何以正确的顺序协同发挥作用；第 9 节的三类失败模式，则分
别展示了当这种顺序、或底层的容错算术未被遵守时，系统会如何出错。

---

## References

**参考文献**

### External Sources

- [In Search of an Understandable Consensus Algorithm (Raft) — Ongaro & Ousterhout, USENIX ATC 2014](https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf)
- [The Byzantine Generals Problem — Lamport, Shostak & Pease, ACM Transactions on Programming Languages and Systems, 1982](https://lamport.azurewebsites.net/pubs/byz.pdf)
- [Paxos Made Simple — Lamport, ACM SIGACT News, 2001](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)
- [Impossibility of Distributed Consensus with One Faulty Process (FLP) — Fischer, Lynch & Paterson, Journal of the ACM, 1985](https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf)
- [Self-Consistency Improves Chain of Thought Reasoning in Language Models — Wang et al., arXiv:2203.11171](https://arxiv.org/abs/2203.11171)
- [Improving Factuality and Reasoning in Language Models through Multiagent Debate — Du et al., arXiv:2305.14325 (ICML 2024)](https://arxiv.org/abs/2305.14325)
- [Mixture-of-Agents Enhances Large Language Model Capabilities — Wang et al., arXiv:2406.04692](https://arxiv.org/abs/2406.04692)
- [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation — Wu et al., arXiv:2308.08155](https://arxiv.org/abs/2308.08155)
- [Generative Agents: Interactive Simulacra of Human Behavior — Park et al., arXiv:2304.03442 (UIST 2023)](https://arxiv.org/abs/2304.03442)
- [git-worktree — Git official reference documentation](https://git-scm.com/docs/git-worktree)

### Internal Cross-References

- [`introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md`](../introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md)
- [`introductory/07-introduction-to-multi-agent-systems.md`](../introductory/07-introduction-to-multi-agent-systems.md)
- [`intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md`](../intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md)
- [`intermediate/04-agent-memory-systems-short-term-long-term-episodic.md`](../intermediate/04-agent-memory-systems-short-term-long-term-episodic.md)
- [`intermediate/07-multi-agent-communication-and-coordination-protocols.md`](../intermediate/07-multi-agent-communication-and-coordination-protocols.md)
- [`advanced/03-agent-harness-engineering-production-grade-agent-loops.md`](./03-agent-harness-engineering-production-grade-agent-loops.md)
- [`advanced/04-agentic-safety-guardrails-and-governance-patterns.md`](./04-agentic-safety-guardrails-and-governance-patterns.md)
