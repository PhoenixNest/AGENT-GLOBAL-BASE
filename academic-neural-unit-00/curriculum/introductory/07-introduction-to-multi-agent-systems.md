# Introduction to Multi-Agent Systems

**多智能体系统导论**

| Field   | English                                                                 | 中文                                        |
| ------- | ----------------------------------------------------------------------- | ------------------------------------------- |
| Level   | Introductory                                                            | 入门                                        |
| Cluster | Multi-Agent Systems & Evaluation                                        | 多智能体系统与评估                          |
| Author  | Dr. Kaito Fujimori, Research Scientist — Agent Systems Research, ANU-00 | ANU-00 智能体系统研究员 Kaito Fujimori 博士 |

---

## 1. From One Agent to Many: Why Multi-Agent?

**从单一智能体到多智能体：为什么需要多智能体？**

`introductory/03` defined an AI agent as an LLM wrapped in a loop — perceive, think, act, observe —
that lets it take actions in an environment using tools, as covered mechanically in
`introductory/04`. A single such agent, however capable, runs into a real limitation once tasks grow
large or varied: one agent has one running context (the accumulated history it reasons over, covered
fully in `introductory/06`), one "personality" set by its instructions, and one thread of attention.
Ask a single agent to "research a topic, write code implementing a finding, and rigorously check
that code for bugs" and it must do all three jobs itself, in the same context, often blurring
between them — the reasoning that makes for careful research is not the same reasoning that makes
for skeptical bug-hunting, and cramming both into one continuous context invites exactly the kind
of context loss named in `introductory/03` §8. A **multi-agent system** (**MAS** for short) splits
such work across two or more separate agents, each with its own context, its own instructions, and
often its own tools, that communicate to accomplish a task none of them could as cleanly alone.

`introductory/03`将 AI 智能体定义为被包裹在一个循环——感知、思考、行动、观察——中的 LLM，使其能够
借助`introductory/04`所讲授的工具在环境中采取行动。然而，单个这样的智能体，无论能力多强，一旦任务
变得庞大或多样，就会遇到一个真实的限制：一个智能体只有一个运行中的上下文（即它据以推理的累积历史，
详见`introductory/06`）、一套由指令设定的"人格"，以及一条注意力线索。如果要求单个智能体"研究某个
课题、编写实现某项发现的代码、并严格检查该代码中的漏洞"，它就必须在同一个上下文中独自完成这三项
工作，往往会导致三者相互混淆——支撑严谨研究的推理方式，与支撑挑剔式漏洞查找的推理方式并不相同，
把二者硬塞进同一个连续上下文，恰恰会招致`introductory/03`第 8 节所述的上下文丢失问题。**多智能体
系统**（简称 **MAS**）将此类工作拆分给两个或更多各自独立的智能体，每个智能体都拥有自己
的上下文、自己的指令，通常还有自己的工具，它们通过通信来共同完成任何一个智能体单独都无法如此清晰地
完成的任务。

---

## 2. Defining a Multi-Agent System (MAS)

**定义多智能体系统（MAS）**

The formal study of multi-agent systems predates modern LLMs by decades, growing out of distributed
artificial intelligence research; Michael Wooldridge's widely used textbook _An Introduction to
MultiAgent Systems_ defines the field around systems composed of multiple interacting, autonomous
agents, each pursuing its own objectives within a shared environment, that must coordinate to
function well together. This curriculum adapts that definition to the LLM-agent case introduced in
`introductory/03`: a **multi-agent system** here means two or more AI agents — each
running its own perceive-think-act-observe loop, each with its own context — that exchange messages
or otherwise share information in order to jointly complete a task. The key word is "own": if two
agent-like components share a single context and are really just one LLM call producing structured
output for two different purposes, that is not a multi-agent system by this definition; separateness
of context and decision-making is what makes it "multi."

多智能体系统的正式研究早于现代 LLM 数十年，其根源可追溯到分布式人工智能研究；Michael Wooldridge
广为使用的教科书《多智能体系统导论》（_An Introduction to MultiAgent Systems_）将该领域界定为围绕
"由多个相互交互、自主的智能体组成的系统"，每个智能体在共享环境中追求自身目标，并且必须协调才能良好
运作。本课程将该定义适配到`introductory/03`所引入的 LLM 智能体情形：此处的**多智能体系统**是指
两个或更多 AI 智能体——各自运行自己的"感知—思考—行动—观察"循环，各自
拥有自己的上下文——通过交换消息或以其他方式共享信息，来共同完成某项任务。关键词是"各自"：如果两个
类智能体的组件共享同一个上下文，实质上只是一次 LLM 调用为两个不同目的产出结构化输出，那么按此定义
它并不是多智能体系统；上下文与决策的相互独立，才是使其成为"多"智能体系统的原因。

---

## 3. Types of Agent Interaction: Cooperation, Coordination, Competition

**智能体交互的类型：协作、协调与竞争**

Agents in a MAS can relate to each other in different ways, and it helps to name the three most
common patterns precisely.

MAS 中的智能体彼此之间可以有不同的关系类型，值得精确地为三种最常见的模式命名。

| Pattern                     | EN                                                                                                                                                                                                                                                                                                                       | 中文                                                                                                                                                                                               |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cooperation** / **协作**  | agents share a common goal and actively help each other reach it — a research agent handing its findings to a writing agent is cooperating.                                                                                                                                                                              | 智能体共享一个共同目标，并积极互相帮助以实现该目标——一个研究智能体把发现交给一个写作智能体，就是在协作。                                                                                           |
| **Coordination** / **协调** | a narrower, more mechanical relationship: agents may not share every goal, but they must still avoid interfering with each other's actions — two agents both editing different parts of the same shared file need to coordinate which sections each may touch, even if neither cares about the other's specific subtask. | 一种更狭窄、更机械化的关系：智能体未必共享全部目标，但仍必须避免相互干扰彼此的行动——两个智能体分别编辑同一份共享文件的不同部分，即便彼此都不关心对方具体的子任务，也仍需协调各自可以触及哪些部分。 |
| **Competition** / **竞争**  | agents have conflicting goals, such as one agent proposing a plan and a second agent explicitly tasked with trying to find flaws in it (a pattern sometimes called adversarial or "red-team/blue-team" design, covered further from a safety angle in `advanced/04`).                                                    | 智能体拥有相互冲突的目标，例如一个智能体提出一项计划，另一个智能体则被明确赋予寻找其缺陷的任务（这种模式有时被称为对抗式或"红队/蓝队"设计，`advanced/04`会从安全角度进一步展开）。                 |

Most practical LLM-based multi-agent systems in production use combine cooperation and
coordination — agents genuinely working toward one shared outcome, while a coordination layer
(covered in §6) keeps their actions from clashing.

绝大多数生产环境中实际使用的基于 LLM 的多智能体系统，都是协作与协调的结合——各智能体真正朝着同一个
共享结果努力，同时由一个协调层（见第 6 节）确保它们的行动不会相互冲突。

---

## 4. Architectures: Centralized, Decentralized, and Hierarchical

**架构：集中式、去中心式与层级式**

How agents are wired together — who talks to whom — is called the system's **coordination
architecture**. Three basic shapes cover most practical designs.

智能体之间如何相互连接——谁与谁通信——被称为系统的**协调架构**。三种基本形态涵盖了大多数实际设计。

| Architecture                     | EN                                                                                                                                                                                                                                                                                                                     | 中文                                                                                                                                                                                                     |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Centralized** / **集中式**     | one agent (often called an **orchestrator** or a **manager agent**) receives the task, decides which other agent should handle each part, and collects their results — every message passes through this central agent, which makes the system easy to reason about but creates a single point of slowdown or failure. | 一个智能体（通常称为**编排器**或**管理智能体**）接收任务，决定应由哪个其他智能体处理哪一部分，并收集它们的结果——所有消息都经过这个中心智能体，这使系统易于推理分析，但也造成了单点瓶颈或单点故障的风险。 |
| **Decentralized** / **去中心式** | agents communicate directly with whichever peer they need, with no single agent in overall control — more resilient to any one agent failing, but harder to predict and debug.                                                                                                                                         | 智能体直接与所需的对等智能体通信，没有任何一个智能体掌握全局控制权——对任何单个智能体的失败更具韧性，但更难预测与调试。                                                                                   |
| **Hierarchical** / **层级式**    | a middle ground: a top-level orchestrator delegates broad sub-tasks to mid-level agents, each of which may in turn coordinate its own small team of specialist agents, so control is distributed across levels rather than concentrated in one agent or spread flatly across all of them.                              | 一种折中：顶层编排器把较大的子任务委派给中层智能体，而每个中层智能体又可能协调自己手下一小队专家智能体，因此控制权分布在多个层级之上，而非集中于单个智能体，也非平铺分散在所有智能体之间。               |

This module names these architectures at an introductory level; `intermediate/07` and
`advanced/07` develop the concrete protocols and topologies that implement them.

本模块在入门层面为这些架构命名；`intermediate/07`与`advanced/07`将进一步展开实现这些架构的具体
协议与拓扑结构。

---

## 5. A Worked Example: Two Agents Writing and Reviewing Code

**实例演练：两个智能体分别编写与审查代码**

Consider a minimal, centralized two-agent MAS: a **Coder agent**, whose instructions
are to write a Python function per a given specification, and a **Reviewer agent**,
whose instructions are to find bugs in code it is shown, with no goal of writing code itself. A
human orchestrates the exchange directly in this simplest version (a human-as-orchestrator pattern is
a valid, common centralized architecture in its own right):

考虑一个最简单的集中式双智能体 MAS：一个**编码智能体**，其指令是按给定的规格说明
编写一个 Python 函数；以及一个**审查智能体**，其指令是在展示给它的代码中查找
漏洞，且并无自己编写代码的目标。在这一最简单的版本中，由人类直接充当二者交互的编排者（"人类作为
编排者"本身就是一种有效且常见的集中式架构）：

```text
Task given to Coder:    "Write a function is_prime(n) that returns True if n is a prime number."
Coder's output:          def is_prime(n):
                              if n < 2: return False
                              for i in range(2, n):
                                  if n % i == 0: return False
                              return True

Task given to Reviewer:  "Review this function for correctness and efficiency: [Coder's code above]"
Reviewer's output:       "Correctness: looks right for n >= 2 and n < 2. Efficiency: the loop runs
                          up to n-1 times; it only needs to check divisors up to sqrt(n), and n=2
                          should be handled as a special prime case explicitly for clarity."

Coder's revision:        def is_prime(n):
                              if n < 2: return False
                              if n == 2: return True
                              for i in range(2, int(n**0.5) + 1):
                                  if n % i == 0: return False
                              return True
```

The two agents never shared a context — the Reviewer never saw the Coder's instructions, and the
Coder never saw the Reviewer's instructions, only its output — yet the final result is better than
either agent produced alone, because each agent's context stayed narrowly focused on its own job.
This is the central practical payoff of a MAS: not that multiple agents are individually smarter
than one, but that separating concerns into separate contexts and roles produces a more careful
result than one agent doing everything in one continuous, increasingly cluttered context.

这两个智能体从未共享同一个上下文——审查智能体从未看到编码智能体的指令，编码智能体也从未看到审查
智能体的指令，只看到了它的输出——但最终结果却优于任何一个智能体单独产出的结果，原因在于每个智能体
的上下文都始终紧密聚焦于自己的任务。这正是 MAS 在实践中带来的核心收益：并非因为多个智能体各自比
单个智能体更聪明，而是因为把关注点拆分到各自独立的上下文与角色中，比让一个智能体在同一个日益杂乱的
连续上下文中包揽一切，能产出更为审慎的结果。

---

## 6. Communication: Messages, Protocols, and Shared State

**通信：消息、协议与共享状态**

For agents to cooperate or coordinate, they need a way to exchange information, and two broad
mechanisms are used in practice, often together. **Message passing** is the direct
exchange seen in §5: one agent's output becomes another agent's input, typically structured as text
or JSON with a clear sender, recipient, and content — the worked example above used message passing.
**Shared state** is an alternative or complement: agents read from and write to a common
resource — a shared file, a shared database, a shared "scratchpad" document — rather than (or in
addition to) sending each other direct messages, and coordination then means agreeing on rules for
who can write to which part of that shared resource and when. Real systems frequently combine both:
an orchestrator might message a sub-agent to "update section 3 of the shared report," where the
message is passed directly but the actual work product lives in shared state. This module names the
concepts; `intermediate/07` covers concrete, named communication protocols (including the
Contract Net Protocol and the FIPA Agent Communication Language) that formalize how these exchanges
are structured in both classical and modern LLM-based multi-agent frameworks.

要使智能体能够协作或协调，它们需要某种交换信息的方式，实践中常用两大类机制，且二者常常结合使用。
**消息传递**即第 5 节中所见的直接交换：一个智能体的输出成为另一个智能体的输入，
通常以文本或 JSON 形式结构化，带有明确的发送方、接收方与内容——上文的实例演练使用的就是消息传递。
**共享状态**是另一种机制，或与消息传递互补：智能体读写某个共同资源——一份共享
文件、一个共享数据库、一份共享的"草稿"文档——而非（或除此之外还）互相发送直接消息，此时"协调"就意味
着就"谁可以在何时写入该共享资源的哪一部分"达成一致规则。真实系统常将二者结合：编排器可能通过消息
告诉某个子智能体"更新共享报告的第 3 节"，消息本身是直接传递的，但实际工作成果却存放在共享状态中。
本模块在此为这些概念命名；`intermediate/07`将介绍具体的、具名的通信协议（包括合同网协议 Contract
Net Protocol 与 FIPA 智能体通信语言），正式规范这些交流在经典多智能体系统与现代基于 LLM 的多智能体
框架中是如何被组织起来的。

---

## 7. Emergent Behavior: What It Means and a Cautionary Note

**涌现行为：其含义与一个提醒**

**Emergent behavior** describes a pattern in a multi-agent system's overall behavior
that was not explicitly programmed into any single agent's instructions, but arises from how the
agents' individual behaviors combine — for instance, a group of agents that were each only
instructed to "avoid duplicating another agent's work" might, without ever being told to, settle
into a stable division of labor over the course of a long task. This is one of the genuine
scientific reasons ANU-00's own research programme studies coordination theory: whether and under
what conditions such patterns emerge is a real, open, falsifiable question, not something that can
simply be assumed. A caution belongs here for a reader at this level: emergent behavior is often
described in popular writing as if it were reliably beneficial "intelligence" appearing on its own,
but the same mechanism can just as easily produce emergent _failure_ — for example, several agents
each independently and reasonably deciding to double-check the same piece of work, wasting cost and
time without anyone having decided that redundancy was needed. Emergence is a description of
unplanned pattern formation, not a guarantee that the pattern is a good one.

**涌现行为**描述的是多智能体系统整体行为中出现的某种模式，它并未被明确编写
进任何单个智能体的指令中，而是源于各智能体各自行为相互组合的结果——例如，一组智能体如果各自仅被
指示"避免重复其他智能体已做的工作"，在长时间任务的过程中，即便从未被明确告知要这样做，也可能自发
形成一种稳定的分工格局。这正是 ANU-00 自身的研究项目之所以研究协调理论的真正科学缘由之一：此类
模式是否会涌现、在何种条件下会涌现，是一个真实、开放且可证伪的问题，而不能被简单假定为理所当然。
在此有必要向本级别的读者提出一个提醒：通俗写作中常把涌现行为描述成某种自发出现、可靠有益的"智能"，
但同样的机制同样容易产生涌现出的*失效*——例如，若干智能体各自独立、且各自看似合理地决定对同一份
工作进行二次核查，在没有任何人真正判定需要这种冗余的情况下白白浪费成本与时间。涌现只是对未经规划
的模式形成过程的一种描述，而非该模式一定良好的保证。

---

## 8. Risks Unique to Multi-Agent Systems

**多智能体系统特有的风险**

Splitting work across agents solves the context-crowding problem from §1, but introduces its own
risks that a single-agent system never faces, and it is worth naming three plainly for a first
encounter with the topic. **Cost multiplication**: each additional agent typically means
additional LLM calls, so a MAS can be substantially more expensive to run than a single agent doing
the same work, and this cost must be weighed against the quality gain demonstrated in §5.
**Cascading errors**: because one agent's output becomes another's input, a mistake made
early — a hallucinated fact, a subtly wrong plan — can be passed downstream and compounded by every
agent that trusts it without re-checking, sometimes producing a confidently wrong final result that
is harder to trace back to its source than a single agent's mistake would be. **Coordination
overhead**: time and computation spent on agents communicating, waiting for each other,
or resolving conflicting claims about shared state is pure overhead that a single-agent system does
not pay at all — beyond some task complexity, a MAS is worth this overhead, but below it, a single
well-designed agent loop is often simply the better engineering choice. These risks are picked up
again with concrete named failure patterns in `intermediate/07`, and with formal mitigation
techniques in `advanced/04` and `advanced/07`.

将工作拆分给多个智能体虽然解决了第 1 节所述的上下文拥挤问题，却也带来了单智能体系统从不会遇到的
自身风险，作为对该主题的初次接触，有必要明确指出三种风险。**成本倍增**：
每增加一个智能体，通常就意味着增加相应的 LLM 调用次数，因此运行一个 MAS 的成本可能大大高于由单个
智能体完成同样工作，这一成本必须与第 5 节所展示的质量提升相权衡。**错误级联**：
由于一个智能体的输出会成为另一个智能体的输入，早期发生的一个错误——一个幻觉出的事实、一个微妙错误
的计划——可能被传递到下游，并被每个不加复核就信任它的智能体不断放大，有时会产生一个自信满满却错误
的最终结果，其错误根源比单智能体犯错时更难追溯。**协调开销**：花费在
智能体之间通信、相互等待，或解决关于共享状态的相互冲突主张上的时间与算力，是单智能体系统完全不需要
承担的纯粹开销——当任务复杂度超过某个阈值后，MAS 值得承担这份开销；但在此阈值以下，一个设计良好的
单智能体循环往往才是更好的工程选择。这些风险将在`intermediate/07`中以具体、具名的失效模式再次
展开，并在`advanced/04`与`advanced/07`中给出正式的缓解技术。

---

## 9. Summary

**小结**

A multi-agent system is two or more separately-contexted AI agents — each running its own
perceive-think-act-observe loop from `introductory/03` — that communicate, via message passing or
shared state, to jointly complete a task. Agents may cooperate, coordinate, or compete, arranged in
a centralized, decentralized, or hierarchical architecture. Splitting a task this way trades context
crowding for new costs — added LLM calls, cascading errors, and coordination overhead — and can
produce emergent behavior, for better or worse, that was never explicitly programmed into any one
agent.

多智能体系统是指两个或更多各自拥有独立上下文的 AI 智能体——每个智能体都运行着`introductory/03`
所述自己的"感知—思考—行动—观察"循环——通过消息传递或共享状态进行通信，以共同完成某项任务。智能体
之间可以是协作、协调或竞争的关系，可按集中式、去中心式或层级式架构组织。这种拆分方式以新的代价换取
了对上下文拥挤问题的缓解——增加的 LLM 调用、错误级联，以及协调开销——并可能产生涌现行为，无论其结果
是好是坏，都并非被明确编写进任何单个智能体之中。

The next module in this cluster, `intermediate/07`, returns to this topic with formal communication
protocols and named coordination frameworks. `intermediate/03` develops single- and multi-step
reasoning patterns (ReAct, Plan-and-Execute, Reflexion) that individual agents inside a MAS commonly
use internally, and `advanced/07` covers production-grade multi-agent orchestration in full
engineering depth.

本主题群的下一个模块`intermediate/07`将带着正式的通信协议与具名的协调框架回归这一主题。
`intermediate/03`将发展出单个智能体在 MAS 内部通常内在使用的单步与多步推理模式（ReAct、
Plan-and-Execute、Reflexion），而`advanced/07`则会以完整的工程深度介绍生产级多智能体编排。

---

## References

**参考文献**

### External Sources

- [Wooldridge, M. — An Introduction to MultiAgent Systems, 2nd Edition (Wiley, 2009)](https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/imas/)
- [Yao, S. et al. (2022) — "ReAct: Synergizing Reasoning and Acting in Language Models"](https://arxiv.org/abs/2210.03629)

### Internal Cross-References

- [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](./03-what-is-an-ai-agent-concepts-and-the-agent-loop.md)
- [`introductory/04` — Tool Use & Function Calling Basics](./04-tool-use-and-function-calling-basics.md)
- [`introductory/06` — Context Windows, Tokens & Memory Basics](./06-context-windows-tokens-and-memory-basics.md)
- [`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion](../intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md)
- [`intermediate/07` — Multi-Agent Communication & Coordination Protocols](../intermediate/07-multi-agent-communication-and-coordination-protocols.md)
- [`advanced/04` — Agentic Safety, Guardrails & Governance Patterns](../advanced/04-agentic-safety-guardrails-and-governance-patterns.md)
- [`advanced/07` — Multi-Agent Orchestration: Worktree Isolation & Consensus](../advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md)
