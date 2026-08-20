# What Is an AI Agent? Concepts & the Agent Loop

**什么是 AI 智能体？概念与智能体循环**

| Field   | English                                                                 | 中文                                        |
| ------- | ----------------------------------------------------------------------- | ------------------------------------------- |
| Level   | Introductory                                                            | 入门                                        |
| Cluster | Agent Architecture & Design Patterns                                    | 智能体架构与设计模式                        |
| Author  | Dr. Kaito Fujimori, Research Scientist — Agent Systems Research, ANU-00 | ANU-00 智能体系统研究员 Kaito Fujimori 博士 |

---

## 1. Introduction — What Problem Are We Solving?

**引言——我们要解决什么问题？**

Imagine you ask a large language model (LLM — the kind of neural network introduced in
`introductory/01`, trained to predict the next piece of text) a question like "what's the weather
in Tokyo right now, and should I bring an umbrella?" A plain LLM, no matter how capable, cannot
answer this correctly on its own. It was trained on text up to some cutoff date and has no
connection to a live weather service; it can only guess, and a guess dressed up in confident
prose is called a hallucination — a fluent but false statement. To answer correctly, something
needs to (1) recognize that live weather data is required, (2) fetch that data from a real
source, (3) read the result, and (4) turn it into a helpful answer. That "something" — a system
built around an LLM that can decide what to do, take an action in the world, observe what
happened, and decide again — is what this module calls an **AI agent**.

请设想你向一个大语言模型（LLM，即`introductory/01`中介绍过的、经过训练以预测下一段文本的神经网络）
提出这样一个问题："东京现在天气如何？我要不要带伞？"无论多么强大的纯语言模型，都无法凭自身准确回答
这个问题。它的训练数据截止于某个时间点，也没有连接到实时天气服务，因此只能猜测——而用流畅文字包装
起来的猜测，就是所谓的"幻觉"：一句听起来自信却并不真实的陈述。要正确回答这个问题，
必须有某种机制能够：(1) 识别出需要实时天气数据；(2) 从真实来源获取这些数据；(3) 读取结果；(4) 将结果
转化为有帮助的回答。这种"围绕 LLM 构建、能够决定做什么、在世界中采取行动、观察结果、再重新决策"的
系统，本模块称之为 **AI 智能体**。

This module has one job: give you a precise, testable definition of "AI agent" and show you the
mechanical skeleton — the **agent loop** — that almost every agent system, from a
simple customer-support bot to a multi-step coding assistant, is built on. Every term used here is
defined before it is used; where a term was already defined in an earlier module, this module
names that module explicitly rather than assuming you remember it from somewhere else.

本模块只有一个任务：给你一个精确、可检验的"AI 智能体"定义，并展示几乎所有智能体系统——从简单的客服
机器人到多步骤编程助手——共同依赖的机械骨架，即**智能体循环**。本模块中使用的每一个术语，
都会在使用之前先给出定义；凡是此前模块已经定义过的术语，本模块会明确指出出处模块，而不会假定你已经从
别处记住了它。

---

## 2. Defining "Agent": From Software Objects to AI Agents

**定义"智能体"：从软件对象到 AI 智能体**

The word "agent" predates modern AI by decades and is used loosely across computing, so precision
matters. The most widely cited formal definition comes from the textbook _Artificial Intelligence:
A Modern Approach_ by Stuart Russell and Peter Norvig, which defines an agent as "anything that can
be viewed as perceiving its **environment** through **sensors** and acting upon
that environment through **actuators**." A thermostat is an agent by this definition: its
sensor is a temperature reader, its actuator is a switch that turns the heater on or off, and its
"policy" — the rule mapping what it senses to what it does — is simply "if temperature is below the
target, turn on the heater."

"智能体"一词在现代 AI 出现之前几十年就已存在，并在计算机领域被广泛而宽泛地使用，因此精确定义十分
重要。被引用最多的正式定义来自 Stuart Russell 与 Peter Norvig 合著的教科书《人工智能：一种现代方法》
（_Artificial Intelligence: A Modern Approach_），书中将智能体定义为"任何可以被看作通过**传感器**
感知其**环境**、并通过**执行器**作用于该环境的事物"。按此
定义，一个恒温器就是一个智能体：它的传感器是温度读取装置，它的执行器是控制加热器开关的开关，而它的
"策略"——即把感知映射到行动的规则——不过是"如果温度低于目标值，就打开加热器"。

An **AI agent**, as this curriculum uses the term, is the special case where the
decision-making core — the part that turns a percept (what was sensed) into an action (what to do)
— is an LLM, augmented with the ability to call real-world tools. This distinguishes an AI agent
from three simpler things it is often confused with. First, it is not a plain chatbot: a chatbot's
only actuator is "produce the next reply text," while an agent's actuators can include running
code, searching the web, editing a file, or calling any external tool (tool use is covered in full
in `introductory/04`). Second, it is not a fixed script: a script's sequence of actions is written
in advance by a programmer, while an agent's LLM core decides its next action dynamically, based on
what it has just observed. Third, it is not "any program that uses an LLM": a program that calls an
LLM once to summarize a document and stops is not an agent, because there is no loop — no
repeated cycle of observing the world and choosing a new action based on the new observation. The
loop is the defining structural feature, and it is the subject of the rest of this module.

本课程所使用的 **AI 智能体**，特指其中决策核心——即把感知（sensed 到的内容）转化为行动
（要做什么）的那个部分——由一个具备调用真实世界工具能力的 LLM 承担的特殊情形。这一定义把 AI 智能体
与三种常被混淆的更简单事物区分开来。第一，它不是普通聊天机器人：聊天机器人唯一的执行器是"生成下一段
回复文本"，而智能体的执行器可以包括运行代码、搜索网页、编辑文件，或调用任何外部工具（工具使用将在
`introductory/04`中完整介绍）。第二，它不是固定脚本：脚本的动作序列由程序员事先写死，而智能体的
LLM 核心会根据刚刚观察到的内容动态决定下一步行动。第三，它也不是"任何调用了 LLM 的程序"：一个只调用
一次 LLM 来概括文档、随即终止的程序并不是智能体，因为其中没有循环——没有"观察世界、根据新的观察选择
新行动"这样反复进行的周期。这个循环正是智能体的定义性结构特征，也是本模块余下部分的主题。

---

## 3. The Agent Loop: Perceive → Think → Act → Observe

**智能体循环：感知 → 思考 → 行动 → 观察**

The agent loop is the repeated cycle that turns a static LLM into a dynamic agent. In its simplest
form it has four stages, executed one after another, with the last stage feeding back into the
first:

智能体循环是把一个静态 LLM 转变为动态智能体的重复周期。在其最简单的形式中，它由四个依次执行的阶段
组成，最后一个阶段又反馈回第一个阶段：

1. **Perceive** — the agent receives new information: the user's request, the result of a
   previous action, or a change in its environment. This information is called an
   **observation**.
2. **Think** — the LLM core is given the observation plus its accumulated history (its
   **context**, covered fully in `introductory/06`) and produces a decision: either a
   final answer, or the next action to take.
3. **Act** — if the LLM chose an action, the agent's surrounding software (the
   **harness** — the non-LLM code that wires the loop together) executes it:
   calling an API, running code, querying a database, and so on.
4. **Observe** — the result of that action becomes a new observation, and the loop
   returns to step 1.

5. **感知**——智能体接收新信息：用户的请求、上一次行动的结果，或环境中的某个变化。这类
   信息称为**观察**。
6. **思考**——LLM 核心接收该观察以及其累积的历史信息（即**上下文**，将在
   `introductory/06`中完整介绍），并产出一个决策：要么给出最终答案，要么决定下一步要采取的行动。
7. **行动**——如果 LLM 选择了某个行动，智能体周围的软件（**运行框架**，即把整个
   循环连接起来的非 LLM 代码）会执行该行动：调用 API、运行代码、查询数据库等等。
8. **观察结果**——该行动的结果成为一条新的观察，循环回到第一步。

The loop terminates when the LLM's decision in the "think" step is not an action but a final
answer — or when the harness enforces a stopping condition, such as a maximum number of steps, to
guard against the loop running forever (a failure mode discussed in §8). It is worth being precise
about what is _not_ part of the agent loop: the training of the underlying LLM (covered in
`introductory/01`) happens once, long before deployment, and is unrelated to the loop running at
inference time — the loop is entirely a property of how the already-trained model is used, not of
how it was built.

当"思考"步骤中 LLM 的决策不再是某个行动、而是最终答案时，循环便会终止；运行框架也可能强制施加一个
停止条件（例如最大步数限制），以防止循环无限运行下去（这一失效模式将在第 8 节讨论）。有必要明确指出
哪些内容*不属于*智能体循环：底层 LLM 的训练过程（见`introductory/01`）只发生一次，且远在部署之前完成，
与推理阶段运行的循环毫无关系——循环完全是"已训练好的模型如何被使用"的属性，而不是"模型如何被构建"的
属性。

---

## 4. Worked Example: A Weather-Checking Agent, Traced Step by Step

**实例演练：逐步追踪一个查询天气的智能体**

Return to the Tokyo weather question. Suppose the agent has exactly one tool available: a function
`get_weather(city: str) -> dict` that calls a real weather API and returns data like
`{"condition": "rain", "temp_c": 19}`. Here is the full loop trace:

回到东京天气的例子。假设该智能体恰好只有一个可用工具：函数 `get_weather(city: str) -> dict`，
它会调用一个真实的天气 API，并返回类似 `{"condition": "rain", "temp_c": 19}` 的数据。以下是完整
的循环追踪：

```text
Step 1 — Perceive: user says "what's the weather in Tokyo right now, and should I bring an umbrella?"
Step 1 — Think: the LLM has no live data; it decides the action get_weather(city="Tokyo") is needed.
Step 1 — Act: the harness calls get_weather("Tokyo") and receives {"condition": "rain", "temp_c": 19}.
Step 2 — Perceive: the agent observes the tool result {"condition": "rain", "temp_c": 19}.
Step 2 — Think: the LLM now has enough information; it decides no further action is needed.
Step 2 — Act: the LLM produces the final answer, not a tool call.
Final answer: "It's raining in Tokyo right now at 19°C — yes, bring an umbrella."
```

```text
第一步——感知：用户问："东京现在天气如何？我要不要带伞？"
第一步——思考：LLM 没有实时数据，判断需要执行行动 get_weather(city="Tokyo")。
第一步——行动：运行框架调用 get_weather("Tokyo")，收到返回结果 {"condition": "rain", "temp_c": 19}。
第二步——感知：智能体观察到工具返回结果 {"condition": "rain", "temp_c": 19}。
第二步——思考：LLM 此时已有足够信息，判断无需再执行行动。
第二步——行动：LLM 给出最终答案，而不是工具调用。
最终答案："东京现在正在下雨，气温 19°C——是的，请带伞。"
```

Notice that the loop ran exactly twice: once to decide on and execute the tool call, once to
produce the final answer from the tool's result. A harder question — say, "compare the weather in
Tokyo and Osaka and tell me which city to visit this weekend" — would require the loop to run at
least three times: once per city to fetch data, and once more to reason over both results and
decide. The number of loop iterations is not fixed in advance; it is however many steps the LLM's
own decisions require, which is precisely what makes agents useful for tasks whose length cannot be
known ahead of time.

请注意，该循环恰好运行了两次：一次用于决定并执行工具调用，一次用于根据工具结果给出最终答案。若换成
更难的问题——例如"比较东京和大阪的天气，告诉我这个周末该去哪座城市"——循环至少需要运行三次：每座城市
各获取一次数据，再加一次综合两次结果进行推理与决策。循环迭代的次数并非事先固定，而是取决于 LLM 自身
决策所需要的步数——这也正是智能体之所以适用于那些长度事先无法预知的任务的根本原因。

---

## 5. Agents vs. Chatbots vs. Scripts: What Makes It "Agentic"?

**智能体、聊天机器人与脚本的区别：什么才算"具备智能体性质"？**

| Property                      | Fixed Script          | Plain Chatbot (single LLM call) | AI Agent                            |
| ----------------------------- | --------------------- | ------------------------------- | ----------------------------------- |
| Decides its own next action   | No — hardcoded        | No — always "reply with text"   | Yes — chosen by the LLM each step   |
| Can take real-world actions   | Only pre-written ones | No                              | Yes — via tools (`introductory/04`) |
| Loop length known in advance  | Yes                   | Yes — always exactly one step   | No — depends on the task            |
| Uses observations to redecide | No                    | No                              | Yes — this is the defining property |

This table sharpens the boundary drawn in §2. The single property that makes a system "agentic" is
the last row: the ability to take an action, observe a real consequence, and let that consequence
change the very next decision. A system that lacks this — however sophisticated its single LLM
call — is not an agent by the definition this curriculum uses, even if marketing material calls it
one. This distinction matters practically: if a task genuinely needs only one LLM call (e.g.,
"translate this sentence"), building an agent loop around it adds cost and latency for no benefit,
and recognizing that is itself part of agent-system literacy.

这张表进一步厘清了第 2 节所划定的边界。使一个系统"具备智能体性质"的唯一关键属性，正是表格最后一行：
能够采取行动、观察真实后果，并让该后果改变紧接着的下一次决策。一个缺乏这一特性的系统——无论其单次
LLM 调用多么精巧——按本课程所采用的定义都不能算作智能体，即便宣传材料如此称呼它。这一区分在实践中
颇为重要：如果某项任务确实只需一次 LLM 调用（例如"翻译这句话"），却仍为其套上一个智能体循环，只会
增加成本与延迟而毫无收益——能够识别这一点，本身就是理解智能体系统素养的一部分。

---

## 6. The Environment: What the Agent Perceives and Acts Upon

**环境：智能体所感知与作用的对象**

Every agent operates inside an **environment** — the set of things it can perceive and
affect. The environment shapes how hard the agent's job is, and it helps to describe it along a
few dimensions borrowed from classical AI, restated here in plain terms. An environment is
**fully observable** if the agent's perception at each step gives it everything
relevant to decide correctly (e.g., a tic-tac-toe board), and **partially observable**
if important information is hidden (e.g., the real-world weather, most of which the agent cannot
sense directly and must query for). An environment is **deterministic** if the same
action from the same state always produces the same result, and **stochastic** if it does
not (e.g., a flaky network API that sometimes times out). Most real AI-agent deployments — a coding
assistant, a customer-support agent — operate in environments that are partially observable and at
least somewhat stochastic, which is precisely why the loop structure in §3 (observe, then
re-decide) matters: a one-shot plan made without observing intermediate results would be brittle in
such environments.

每个智能体都在某个**环境**中运作——即它能够感知与影响的一切事物的集合。环境决定了
智能体任务的难易程度，借用经典 AI 中的几个维度来描述它会很有帮助，这里用通俗的语言重述。若智能体在
每一步的感知都足以让它做出正确决策所需的全部相关信息（例如一局井字棋），则该环境是**完全可观察**的；
若重要信息被隐藏（例如现实世界的天气，其中大部分智能体无法直接感知、
必须主动查询），则该环境是**部分可观察**的。若同一状态下的同一行动总是
产生同样的结果，则该环境是**确定性**的；若并非如此（例如偶尔超时的不稳定网络
API），则该环境是**随机性**的。绝大多数真实的 AI 智能体部署场景——编程助手、客服
智能体——所处的环境都是部分可观察、且至少带有一定随机性的，这正是第 3 节所述循环结构（先观察、再
重新决策）之所以重要的原因：在这样的环境中，一次性制定、不观察中间结果的计划会十分脆弱。

---

## 7. Autonomy and the Human-in-the-Loop Spectrum

**自主性与"人在回路"光谱**

**Autonomy** describes how much of the agent loop runs without a human approving each
step. Autonomy is not binary; it is a spectrum. At one end, a **human-in-the-loop**
design requires a person to approve every action before the harness executes it — safer, but
slower. In the middle, an agent might act freely for low-risk actions (reading a file) while
pausing for human approval before high-risk ones (deleting a file, sending an email, spending
money). At the far end, a **fully autonomous** agent executes its entire loop, including
high-risk actions, with no human checkpoint at all. Choosing where on this spectrum to place a given
agent is a design decision driven by the cost of a mistake, not a technical limitation — the same
loop mechanics from §3 work identically at every point on the spectrum; only the placement of
approval checkpoints changes. This spectrum is revisited in much more depth, including formal
guardrail patterns, in `advanced/04`.

**自主性**描述的是智能体循环中有多大比例可以在没有人类逐步批准的情况下运行。自主性并非
非此即彼的二元属性，而是一个连续光谱。光谱一端是**人在回路**设计，要求每一次
行动执行前都必须经人工批准——更安全，但更慢。光谱中段，智能体可能对低风险行动（如读取文件）自由执行，
而对高风险行动（如删除文件、发送邮件、花钱）暂停等待人工批准。光谱另一端是**完全自主**的智能体，它执行整个循环——包括高风险行动——完全没有任何人工检查点。将某个具体智能体
置于这一光谱的何处，是由出错代价所驱动的设计决策，而非技术上的限制——第 3 节所述的循环机制在光谱的
任何位置都以同样方式运作，改变的只是审批检查点的设置位置。这一光谱将在`advanced/04`中被更深入地
重新讨论，包括正式的护栏设计模式。

---

## 8. Common Failure Modes of the Agent Loop

**智能体循环的常见失效模式**

Understanding the loop's mechanics also means understanding how it breaks. Three failure modes
recur across nearly all agent systems and are worth naming precisely here, since later modules
(especially `intermediate/03` and `advanced/04`) build directly on this vocabulary. **Infinite
looping** happens when the LLM repeatedly chooses an action, observes a result, and
fails to recognize that the task is either complete or unsolvable, so it never reaches a final
answer — harnesses guard against this with a maximum-step limit. **Hallucinated actions**
happen when the LLM's "think" step produces a call to a tool that does not exist, or with arguments
that do not match the tool's real schema — the harness must validate every proposed action before
executing it, never trust the LLM's output blindly. **Context loss** happens when the
accumulated history from earlier loop iterations grows too large or gets truncated, so the LLM
"forgets" an earlier observation it needs — this is explored fully in `introductory/06`'s
treatment of context windows. None of these failure modes are solved by a bigger or smarter LLM
alone; they are solved by harness-level engineering around the loop, which is why the loop's
structure, not just the model inside it, is the proper unit of study for agent systems.

理解循环的机制，也意味着理解它是如何失效的。几乎所有智能体系统中都会反复出现三种失效模式，值得在此
精确命名，因为后续模块（尤其是`intermediate/03`与`advanced/04`）会直接沿用这套词汇。**无限循环**
发生在 LLM 反复选择行动、观察结果，却始终未能识别任务已完成或已无法解决，因而
永远无法给出最终答案——运行框架通常以最大步数限制来防范此问题。**幻觉行动**
发生在 LLM 的"思考"步骤生成了一次调用不存在的工具、或参数与该工具真实模式不符的行动——运行
框架必须在执行任何提议行动之前对其进行校验，绝不能盲目信任 LLM 的输出。**上下文丢失**
发生在此前循环迭代所累积的历史信息变得过大或被截断，导致 LLM"遗忘"了它仍需要的某条早期观察
——这一问题将在`introductory/06`关于上下文窗口的讨论中得到完整探讨。这些失效模式无一能单靠一个更大
或更聪明的 LLM 来解决；它们要靠围绕循环所做的运行框架层面的工程来解决，这也正是为什么循环本身的结构、
而不仅仅是其中的模型，才是研究智能体系统的恰当基本单位。

---

## 9. Summary and What's Next

**小结与后续内容**

An AI agent is a system whose decision-making core is an LLM that repeatedly perceives an
observation, thinks about what to do, acts on the environment, and observes the result — the agent
loop. What distinguishes an agent from a plain chatbot or a fixed script is precisely this loop:
the ability to let a real consequence change the next decision, running for as many steps as the
task actually requires rather than a number fixed in advance. Autonomy is a spectrum of how much of
this loop runs without human checkpoints, and the loop's own structural weak points — infinite
looping, hallucinated actions, context loss — are engineering problems to be solved around the
model, not inside it.

AI 智能体是这样一种系统：其决策核心是一个 LLM，通过反复地感知观察、思考该做什么、作用于环境、再观察
结果——即智能体循环——来运作。区分智能体与普通聊天机器人或固定脚本的关键，正是这一循环：让真实后果得以
改变下一次决策，且运行的步数取决于任务实际所需，而非事先固定。自主性是一个光谱，描述这一循环中有多少
比例可以在没有人工检查点的情况下运行；而循环自身的结构性弱点——无限循环、幻觉行动、上下文丢失——则是
需要围绕模型加以解决的工程问题，而非模型内部的问题。

The next module, `introductory/04`, opens up the "act" stage of the loop in full detail: what a
tool actually is, how the LLM is told which tools exist, and the precise mechanics of a function
call and its result. `introductory/07` then extends the single-agent loop introduced here to
systems of multiple agents.

下一个模块`introductory/04`将完整展开循环中的"行动"阶段：工具到底是什么、LLM 如何被告知有哪些工具
可用，以及函数调用及其返回结果的确切机制。随后，`introductory/07`会将本模块中介绍的单智能体循环
扩展为多智能体系统。

---

## References

**参考文献**

### External Sources

- [Russell, S. & Norvig, P. — Artificial Intelligence: A Modern Approach, Ch. 2 "Intelligent Agents"](https://people.eecs.berkeley.edu/~russell/aima1e/chapter02.pdf)
- [Yao, S. et al. (2022) — "ReAct: Synergizing Reasoning and Acting in Language Models"](https://arxiv.org/abs/2210.03629)
- [Weng, L. (2023) — "LLM Powered Autonomous Agents"](https://lilianweng.github.io/posts/2023-06-23-agent/)

### Internal Cross-References

- [`introductory/01` — Neural Networks & Deep Learning Foundations](./01-neural-networks-and-deep-learning-foundations.md)
- [`introductory/02` — The Transformer Architecture & Attention](./02-the-transformer-architecture-and-attention.md)
- [`introductory/04` — Tool Use & Function Calling Basics](./04-tool-use-and-function-calling-basics.md)
- [`introductory/06` — Context Windows, Tokens & Memory Basics](./06-context-windows-tokens-and-memory-basics.md)
- [`introductory/07` — Introduction to Multi-Agent Systems](./07-introduction-to-multi-agent-systems.md)
- [`advanced/04` — Agentic Safety, Guardrails & Governance Patterns](../advanced/04-agentic-safety-guardrails-and-governance-patterns.md)
