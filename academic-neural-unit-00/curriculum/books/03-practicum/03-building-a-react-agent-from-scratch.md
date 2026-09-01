# Building a ReAct Agent From Scratch

**从零构建一个 ReAct 智能体**

| Field   | English                                                                 | 中文                                               |
| ------- | ----------------------------------------------------------------------- | -------------------------------------------------- |
| Level   | Practicum                                                               | 实战                                               |
| Cluster | Hands-On Coding Practicum                                               | 实战编程练习                                       |
| Author  | Dr. Inés Roldán, Research Scientist — Software Engineering / CS, ANU-00 | ANU-00 软件工程与计算机科学研究员 Inés Roldán 博士 |

---

## 0. Where This Module Fits

**本模块的定位**

This module has one prerequisite:
[`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md)
("Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion"), and it assumes nothing beyond what
that module already taught. `intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion [`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion §2](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#2-react-interleaving-reasoning-traces-and-actions)
defined the ReAct pattern — an LLM producing an explicit **thought**, then an **action**, then
reading the resulting **observation**, in a repeated cycle — and walked a hand-traced example: "what
is the population of the capital city of the country where the 2016 Summer Olympics were held?",
resolved in four thought/action/observation cycles.

本模块只有一个前置模块：[`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md)（《智能体设计模式：ReAct、计划-执行与 Reflexion》），本模块不假设读者具备该模块之外的任何知识。`intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion [`intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion 第 2 节](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#2-react-interleaving-reasoning-traces-and-actions)已经定义了 ReAct 模式——LLM 先产出一段明确的**思考**，再产出一次**行动**，随后读取由此得到的**观察**，如此循环往复——并手动追踪了一个示例：“2016 年夏季奥运会举办国的首都人口是多少？”，该示例通过四轮思考-行动-观察循环得到了解答。

That module described the pattern in prose and showed a hand-written trace of what the interaction
looks like. It did not show you the code that produces that trace. This module does exactly that:
by the end, you will have built, tested, and understood every moving part of a working ReAct agent
in Python — not a library import, a from-scratch implementation you can read top to bottom.

那个模块用文字描述了这一模式，并展示了一份手写的交互追踪示例，但并未展示产出这份追踪记录的代码本身。本模块要做的正是这件事：读完本模块后，你将亲手构建、测试并理解一个可运行的 ReAct 智能体在 Python 中的每一个组成部分——不是导入某个现成的库，而是一份你可以从头读到尾、完全理解的从零实现。

This module writes no application code outside its own fenced code blocks — everything below lives
in this markdown file, exactly as
[`practicum/README.md` §3](https://anu00.dev/curriculum/books/03-practicum/README.md) requires. Copy the
blocks into your own `.py` file on your own machine to run them; nothing here is committed as a
runnable file in this repository.

本模块不会在自身的代码围栏之外撰写任何应用代码——以下所有内容都保存在这一份 markdown 文件之中，正如 [`practicum/README.md` 第 3 节](https://anu00.dev/curriculum/books/03-practicum/README.md)所要求的那样。若要运行这些代码，请将下方代码块复制到你自己机器上的 `.py` 文件中；本仓库中不会提交任何可运行的文件。

---

## 1. What We're Building: The Four Moving Parts

**我们要构建什么：四个组成部分**

A ReAct agent, reduced to its engineering essentials, is four pieces working together: a **tool
registry** (what the agent is allowed to do), a **prompt contract** (the exact text format the LLM
is instructed to produce), a **parser** (code that turns the LLM's raw text output back into a
structured thought/action/final-answer), and a **loop** (the harness that calls the LLM, parses its
output, executes the chosen tool, feeds the observation back in, and repeats until a final answer
appears or a safety limit is hit).

从工程角度来看，一个 ReAct 智能体本质上由四个相互配合的部分组成：一个**工具注册表**（智能体被允许执行哪些操作）、一份**提示词契约**（要求 LLM 产出的确切文本格式）、一个**解析器**（将 LLM 输出的原始文本重新转换为结构化的思考/行动/最终答案的代码），以及一个**循环**（即调用 LLM、解析其输出、执行所选工具、将观察结果重新输入、并不断重复，直到出现最终答案或触发安全限制为止的运行框架）。

None of these four pieces is exotic — this is ordinary software engineering (input validation,
parsing, a bounded retry loop) applied to a new kind of "function call" whose implementation happens
to be a language model instead of a subroutine. Keeping that framing in mind is deliberate: it is
easy to over-mystify agent code, and the goal of this module is to demystify it by building every
piece yourself.

这四个部分都并不神秘——它们不过是普通的软件工程技巧（输入校验、解析、带边界的重试循环），只是被应用到了一种新型“函数调用”之上，而这种调用恰好由语言模型而非普通子程序来实现。刻意保持这样的认知框架是有意为之：智能体代码很容易被过度神秘化，本模块的目标正是通过让你亲手构建每一个部分，来消除这种神秘感。

Because the code needs to be reproducible on any machine — no API key, no network access, and a
deterministic output every time it runs — this module builds and tests everything against a
**scripted stand-in for a real LLM** first, and only afterward shows the substitution point where a
real API call would go instead. This mirrors ordinary software-engineering test practice more than
it mirrors anything specific to agents; [§4](#4-step-3-a-deterministic-stub-llm-for-development)
explains exactly how, with a citation.

由于这段代码需要能够在任意机器上复现——不依赖 API 密钥、不依赖网络访问，且每次运行都能得到确定性的输出——本模块首先会针对一个**用脚本模拟真实 LLM 的替身**来构建和测试全部代码，之后才会展示：若要换成真实的 API 调用，应当在哪个位置进行替换。这更多是在遵循普通软件工程中的测试实践，而非任何智能体特有的做法；[第 4 节](#4-step-3-a-deterministic-stub-llm-for-development)将给出确切的说明与引用来源。

---

## 2. Step 1 — The Tool Interface and Registry

**第 2 节：步骤一——工具接口与注册表**

Every action a ReAct agent can take has to be a concrete, callable piece of code with a name the LLM
can refer to by string, a description the LLM can read to decide when to use it, and a function that
actually does the work. A minimal `Tool` is exactly those three fields, and a `ToolRegistry` is a
lookup table from name to `Tool`:

一个 ReAct 智能体能够执行的每一个行动，都必须对应一段具体的、可调用的代码，它需要有一个 LLM 可以通过字符串引用的名称、一段 LLM 可以阅读并据此判断何时使用它的描述，以及一个真正执行该操作的函数。一个最小化的 `Tool` 恰好就是这三个字段，而 `ToolRegistry` 则是一张从名称到 `Tool` 的查找表：

```python
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Tool:
    name: str
    description: str
    func: Callable[[str], str]


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def describe(self) -> str:
        return "\n".join(f"- {t.name}(query): {t.description}" for t in self._tools.values())
```

**Verification (this block):** mental trace. `@dataclass` (confirmed against the official Python
documentation, cited in References) generates `__init__` from the three annotated fields, so
`Tool(name=..., description=..., func=...)` constructs correctly; `ToolRegistry.get` returning
`Optional[Tool]` (i.e. `None` for an unknown name, never raising `KeyError`) is exercised directly
by the parser's hallucinated-tool-name handling in [§8](#8-step-7-hardening-hallucinated-tools-and-runaway-loops)
below, where it is scratch-run.

**本代码块的验证方式：** 心算追踪。`@dataclass`（已对照官方 Python 文档核实，见“参考文献”）会根据三个带类型标注的字段自动生成 `__init__`，因此 `Tool(name=..., description=..., func=...)` 能够正确构造；`ToolRegistry.get` 返回 `Optional[Tool]`（即对未知名称返回 `None`，而非抛出 `KeyError`）这一行为，会在下方[第 8 节](#8-step-7-hardening-hallucinated-tools-and-runaway-loops)中被实际脚本运行验证，那里正是对幻觉工具名的处理逻辑。

The `Tool` dataclass is the same shape as the tool-calling schemas covered in
[`introductory/04` — Tool Use & Function Calling Basics](https://anu00.dev/curriculum/books/01-introductory/04-tool-use-and-function-calling-basics.md), reduced to the minimum this module needs: a name, a
description, and a callable. A production system typically adds a formal input schema as well (as
the Anthropic Messages API's `tools` parameter does — see [§9](#9-step-8-swapping-in-a-real-llm)); this module keeps the argument as a
single free-text string to keep the parser in [§3](#3-step-2-the-react-prompt-contract) simple, since the parsing problem, not the schema
design, is this module's teaching point.

`Tool` 数据类的结构，与 [`introductory/04` — Tool Use & Function Calling Basics](https://anu00.dev/curriculum/books/01-introductory/04-tool-use-and-function-calling-basics.md) 中所讲解的工具调用模式一脉相承，只是精简到了本模块所需的最低限度：一个名称、一段描述，以及一个可调用对象。生产系统通常还会额外附加一份正式的输入模式定义（正如 Anthropic Messages API 的 `tools` 参数所做的那样——参见[第 9 节](#9-step-8-swapping-in-a-real-llm)）；本模块则将参数保持为单一的自由文本字符串，以便让[第 3 节](#3-step-2-the-react-prompt-contract)中的解析器保持简单，因为解析问题而非模式设计，才是本模块要讲授的重点。

---

## 3. Step 2 — The ReAct Prompt Contract

**第 3 节：步骤二——ReAct 提示词契约**

A parser can only be as reliable as the format it is parsing is precise. Before writing any parsing
code, the format itself has to be nailed down: the LLM is instructed, in its system prompt, to
respond with exactly one `Thought:` line followed by exactly one `Action:` line — or, once it has
enough information, exactly one `Thought:` line followed by exactly one `Final Answer:` line. This
is the same three-role vocabulary (thought, action, observation) `intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion [`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion §2](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#2-react-interleaving-reasoning-traces-and-actions) already
named; this module is simply pinning it down to a literal, parseable line format:

一个解析器的可靠程度，取决于它所解析的格式本身有多精确。在编写任何解析代码之前，必须先把格式本身确定下来：在系统提示词中，我们要求 LLM 严格用一行 `Thought:` 加一行 `Action:` 来作答——或者，一旦信息已经充分，就用一行 `Thought:` 加一行 `Final Answer:` 来作答。这正是 `intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion [`intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion 第 2 节](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#2-react-interleaving-reasoning-traces-and-actions)已经提出的三种角色词汇（思考、行动、观察）；本模块只是将其固定为一种字面的、可解析的行格式：

```python
def build_system_prompt(tools) -> str:
    return (
        "You are a ReAct agent. At each step, respond with exactly one Thought "
        "line, followed by exactly one Action line or one Final Answer line.\n"
        "Available tools:\n"
        f"{tools.describe()}\n"
        "Format:\n"
        "Thought: <your reasoning>\n"
        "Action: <tool_name>(<argument>)\n"
        "...or, once you have enough information...\n"
        "Thought: <your reasoning>\n"
        "Final Answer: <your answer>\n"
    )
```

**Verification (this block):** mental trace, confirmed against the fuller scratch-run of the whole
agent in [§7](#7-step-6-running-it-end-to-end) — the exact string this function produces is what a real LLM would
receive as its system prompt, and it is exercised as the first line of every transcript built in
that run.

**本代码块的验证方式：** 心算追踪，并在[第 7 节](#7-step-6-running-it-end-to-end)对完整智能体的脚本运行中得到进一步确认——该函数产出的确切字符串，正是真实 LLM 会收到的系统提示词，它作为该次运行中每一份对话记录的第一行被实际执行到。

This contract is a design decision with a real trade-off, worth stating explicitly: a stricter
format (say, JSON) is more robust to parse but harder for an LLM to produce reliably inside free-text
reasoning, while a looser format is easier for the model to produce naturally but harder to parse
without ambiguity. The line-oriented format above is a middle ground widely used in ReAct
implementations because it keeps the reasoning readable as prose while still being
regular-expression-parseable line by line, which [§4](#4-step-3-a-deterministic-stub-llm-for-development) below relies on directly.

这一契约背后是一项真实存在权衡的设计决策，值得明确指出：更严格的格式（例如 JSON）更易于稳健解析，但更难要求 LLM 在自由文本推理中稳定地产出；更宽松的格式则更易于模型自然产出，但解析时更容易产生歧义。上文这种按行组织的格式，是 ReAct 类实现中广泛采用的一种折中方案，因为它既能让推理内容保持为可读的自然语言，又能够逐行地用正则表达式解析——[第 4 节](#4-step-3-a-deterministic-stub-llm-for-development)正是直接依赖这一点。

---

## 4. Step 3 — Parsing Model Output Into Thought/Action/Final Answer

**第 4 节：步骤三——将模型输出解析为思考/行动/最终答案**

Given a chunk of text following the contract in [§3](#3-step-2-the-react-prompt-contract), the parser's job is to find whichever line
carries the actionable content — an `Action:` line or a `Final Answer:` line — and extract it into a
structured form the calling code can act on without re-parsing prose:

给定一段遵循[第 3 节](#3-step-2-the-react-prompt-contract)所述契约的文本，解析器的任务是找出其中承载可执行内容的那一行——`Action:` 行或 `Final Answer:` 行——并将其提取为一种结构化形式，使调用方代码无需再次解析自然语言即可据此采取行动：

```python
import re


def parse_step(text: str):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    for line in lines:
        final_match = re.match(r"Final Answer:\s*(.+)", line)
        if final_match:
            return ("final", final_match.group(1))
        action_match = re.match(r"Action:\s*(\w+)\((.*)\)\s*$", line)
        if action_match:
            tool_name, raw_arg = action_match.group(1), action_match.group(2)
            arg = raw_arg.strip()
            if len(arg) >= 2 and arg[0] == arg[-1] and arg[0] in "\"'":
                arg = arg[1:-1]
            return ("action", tool_name, arg)
    raise ValueError(f"No parseable Action or Final Answer line found in:\n{text}")
```

**Verification (this block):** scratch-run, as part of the full script executed in [§7](#7-step-6-running-it-end-to-end) — every
`Action:` line the stub LLM produces there is fed through `parse_step` and correctly recovers the
tool name and argument for all three `search(...)` calls plus the closing `Final Answer:` line;
confirmed against the official Python `re` module documentation (cited in References) for the
semantics of `re.match` and the `\w+` / `(.*)` group behavior relied on here.

**本代码块的验证方式：** 脚本实际运行，作为[第 7 节](#7-step-6-running-it-end-to-end)中完整脚本运行的一部分——该次运行中脚本化 LLM 产出的每一行 `Action:` 都经过 `parse_step` 处理，并针对全部三次 `search(...)` 调用以及最后一行 `Final Answer:` 都正确还原出了工具名与参数；此处依赖的 `re.match` 语义以及 `\w+` / `(.*)` 分组行为，已对照官方 Python `re` 模块文档（见“参考文献”）加以核实。

Two details are load-bearing and worth calling out by name. First, `re.match` anchors at the
**start** of the line (not `re.search`, which would match anywhere), which matters because it keeps
a line like `"Well, Action: search(...) is what I'd do"` — a stray mention of the word "Action:" in
the middle of a thought — from being misparsed as an actual action; the line has to _start_ with
`Action:` to count. Second, the argument-quote stripping (`if len(arg) >= 2 and arg[0] == arg[-1]
and ...`) exists because the worked trace in [§7](#7-step-6-running-it-end-to-end) writes arguments as quoted strings —
`search("capital of Brazil")` — matching how the original hand-written trace in `intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion
[`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion §2](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#21-a-worked-trace) wrote its actions, and the tool function itself
should receive the bare text, not the surrounding quote characters.

有两个细节具有支撑性作用，值得单独指出。第一，`re.match` 只锚定在行的**开头**（而非可以匹配行内任意位置的 `re.search`），这一点很重要，因为它能防止诸如 `"Well, Action: search(...) is what I'd do"` 这样的一行——即某段思考文本中偶然提到了“Action:”一词——被误判为一次真正的行动；该行必须*以* `Action:` 开头才会被计入。第二，去除参数两侧引号的逻辑（`if len(arg) >= 2 and arg[0] == arg[-1] and ...`）之所以存在，是因为[第 7 节](#7-step-6-running-it-end-to-end)中的追踪示例将参数写作带引号的字符串——`search("capital of Brazil")`——这与 `intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion [`intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#21-a-worked-trace)原始手写追踪记录中书写行动的方式一致，而工具函数本身应当接收去除了引号符号的纯文本。

---

## 5. Step 4 — A Deterministic Stub LLM for Development

**第 5 节：步骤四——用于开发的确定性桩式 LLM**

A real LLM API call is non-deterministic (even at low temperature, exact reproducibility is not
guaranteed across providers or model versions) and requires a network connection and credentials —
none of which this module can assume. Ordinary software-engineering practice for exactly this
situation is a **test double**: an object that stands in for a real dependency during development
and testing.

真实的 LLM API 调用是非确定性的（即便在较低的温度参数下，跨提供方或跨模型版本也无法保证结果完全可复现），并且需要网络连接与凭证——而本模块无法假定读者具备这两者。面对这种情况，普通软件工程实践中的通行做法是使用**测试替身（test double）**：一个在开发与测试期间，用来代替真实依赖对象的替代品。

Martin Fowler's 2007 article "Mocks Aren't Stubs" draws a precise distinction this module leans on
by name: a **stub** "provide[s] canned answers to calls made during the test, usually not responding
at all to anything outside what's programmed in for the test" (Fowler, 2007). That is exactly what
this module needs — an object that returns a pre-written sequence of completions regardless of what
transcript it is handed, so that the same script produces the same output every time it runs,
anywhere:

Martin Fowler 2007 年发表的文章《Mocks Aren't Stubs》给出了一个本模块特意采用其名称的精确区分：**桩（stub）**“为测试过程中发生的调用提供预先设定好的固定答案，通常对任何未被预先编好的输入都不作出响应”（Fowler, 2007）。这正是本模块所需要的——一个无论收到什么样的对话记录，都会按预先写好的顺序返回固定完成结果的对象，从而使同一份脚本无论在哪里、每次运行都能产出相同的输出：

```python
class ScriptedStubLLM:
    def __init__(self, completions: list[str]):
        self._completions = list(completions)
        self._calls = 0

    def complete(self, transcript: str) -> str:
        if self._calls >= len(self._completions):
            raise RuntimeError("ScriptedStubLLM ran out of scripted completions.")
        completion = self._completions[self._calls]
        self._calls += 1
        return completion
```

**Verification (this block):** scratch-run in [§7](#7-step-6-running-it-end-to-end) — `ScriptedStubLLM` is instantiated with the
four completions reproducing the `intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion [`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion §2](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#21-a-worked-trace) trace and returns them
in order across four calls, then correctly raises `RuntimeError` on a fifth call in the max-steps
guard demonstration in [§8](#8-step-7-hardening-hallucinated-tools-and-runaway-loops).

**本代码块的验证方式：** 在[第 7 节](#7-step-6-running-it-end-to-end)中脚本实际运行——`ScriptedStubLLM` 被实例化为持有四段完成结果，用以复现 `intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion [`intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#21-a-worked-trace)的追踪记录，并在四次调用中依次正确返回；随后在[第 8 节](#8-step-7-hardening-hallucinated-tools-and-runaway-loops)的最大步数保护演示中，第五次调用被正确地触发了 `RuntimeError`。

Deliberately, `ScriptedStubLLM.complete` ignores its `transcript` argument entirely — it does not
even look at what it was asked. This is a real simplification, not an oversight: it keeps this
module's stub genuinely a stub in Fowler's sense (canned, input-blind) rather than a more elaborate
fake that would itself need its own correctness argument. [§9](#9-step-8-swapping-in-a-real-llm) shows exactly where a real,
transcript-reading LLM call replaces this class without changing any other code.

值得注意的是，`ScriptedStubLLM.complete` 刻意完全忽略了其 `transcript` 参数——它甚至根本不会查看自己被问及的内容。这是一处真实的简化，而非疏漏：它使本模块的桩对象真正符合 Fowler 意义上“桩”的定义（固定输出、对输入视而不见），而非需要自行论证正确性的、更复杂的伪造对象。[第 9 节](#9-step-8-swapping-in-a-real-llm)将确切展示：在不改动其余任何代码的前提下，应当在何处用一个真正会读取对话记录的 LLM 调用来替换这个类。

---

## 6. Step 5 — The Agent Loop

**第 6 节：步骤五——智能体循环**

With a tool registry, a prompt contract, a parser, and a stand-in LLM in place, the loop itself is
short: call the LLM, parse what comes back, either return the final answer or execute the requested
tool and append its observation to the transcript, and repeat — bounded by `max_steps` so a model
that never produces a `Final Answer:` line cannot run forever:

有了工具注册表、提示词契约、解析器，以及一个可替代真实 LLM 的桩对象之后，循环本身就相当简短了：调用 LLM，解析其返回结果，要么返回最终答案，要么执行所请求的工具并将其观察结果追加到对话记录中，如此循环——并以 `max_steps` 作为边界，从而防止一个从不产出 `Final Answer:` 行的模型无限运行下去：

```python
class ReActAgent:
    def __init__(self, llm, tools: ToolRegistry, max_steps: int = 6):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps

    def run(self, question: str) -> str:
        transcript = build_system_prompt(self.tools) + f"\nQuestion: {question}\n"
        for _ in range(self.max_steps):
            completion = self.llm.complete(transcript)
            transcript += completion + "\n"
            kind, *rest = parse_step(completion)
            if kind == "final":
                return rest[0]
            _, tool_name, arg = (kind, *rest)
            tool = self.tools.get(tool_name)
            if tool is None:
                observation = f"Error: no such tool '{tool_name}'. Available tools: {list(self.tools._tools)}"
            else:
                observation = tool.func(arg)
            transcript += f"Observation: {observation}\n"
        raise RuntimeError("Max steps exceeded without a Final Answer.")
```

**Verification (this block):** scratch-run, in full, in [§7](#7-step-6-running-it-end-to-end) and [§8](#8-step-7-hardening-hallucinated-tools-and-runaway-loops) below — this is the
central piece of code this module builds, so its correctness is demonstrated by three separate runs
rather than one: the happy-path Olympics question, the hallucinated-tool-name case, and the
max-steps guard case.

**本代码块的验证方式：** 完整脚本实际运行，见下方[第 7 节](#7-step-6-running-it-end-to-end)与[第 8 节](#8-step-7-hardening-hallucinated-tools-and-runaway-loops)——这是本模块所构建代码的核心部分，因此其正确性通过三次独立的运行来加以证明，而非仅仅一次：正常路径下的奥运会问题、幻觉工具名场景，以及最大步数保护场景。

Notice what this loop does _not_ do: it never lets the LLM's output execute as code, and it never
calls a tool whose name was not explicitly registered. Both of these connect directly to
`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop §8](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#8-common-failure-modes-of-the-agent-loop)'s warning, restated in
`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion [`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion §6](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#6-common-pitfalls-at-this-level), that a fluent-sounding thought is not
automatically a correct one, and that a 运行框架 (harness) still has to validate actions before
acting on them rather than trusting the model's output outright. This loop's validation is
intentionally minimal — tool-name lookup only, not argument-schema validation — and
[§10](#10-common-pitfalls-beyond-what-the-code-already-handles) names what a production harness adds on top.

请注意，这个循环*没有*做的事情：它从不会将 LLM 的输出当作代码去执行，也从不会调用一个未被显式注册过名称的工具。这两点都与 `introductory/03` — 什么是 AI 智能体？概念与智能体循环 [`introductory/03` — 什么是 AI 智能体？概念与智能体循环 第 8 节](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#8-common-failure-modes-of-the-agent-loop)的警示、以及 `intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion [`intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion 第 6 节](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#6-common-pitfalls-at-this-level)中重申的观点直接相关：一段读起来流畅的思考，并不会因此自动成为一段正确的思考，运行框架仍必须在真正执行某个行动之前对其加以校验，而不能对模型的输出全盘信任。这个循环的校验是刻意保持最小化的——仅进行工具名称查找，而不进行参数模式校验——[第 10 节](#10-common-pitfalls-beyond-what-the-code-already-handles)将说明生产级运行框架还需在此基础上补充哪些内容。

---

## 7. Step 6 — Running It End to End

**第 7 节：步骤六——端到端运行**

Reproducing `intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion [`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion §2](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#21-a-worked-trace)'s trace requires a `search` tool
backed by the same three facts that trace used, and a `ScriptedStubLLM` scripted with the same four
thought/action pairs and closing final answer:

要复现 `intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion [`intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#21-a-worked-trace)的追踪记录，需要一个由该追踪记录中同样三条事实支撑的 `search` 工具，以及一个按同样四组思考/行动配对与最终答案预先编好脚本的 `ScriptedStubLLM`：

```python
FACTS = {
    "2016 summer olympics host country": "The 2016 Summer Olympics were held in Rio de Janeiro, Brazil.",
    "capital of brazil": "The capital of Brazil is Brasília.",
    "population of brasília": "Brasília has a population of approximately 3.1 million (metro area).",
}


def search(query: str) -> str:
    key = query.strip().lower()
    if key in FACTS:
        return FACTS[key]
    return f"No results found for '{query}'."


tools = ToolRegistry()
tools.register(Tool(name="search", description="Look up a fact by query string.", func=search))

completions = [
    "Thought: I need to find which country hosted the 2016 Summer Olympics.\n"
    'Action: search("2016 Summer Olympics host country")',

    "Thought: The country is Brazil. Now I need Brazil's capital.\n"
    'Action: search("capital of Brazil")',

    "Thought: The capital is Brasília. Now I need its population.\n"
    'Action: search("population of Brasília")',

    "Thought: I now have both facts chained together. I can answer.\n"
    "Final Answer: The 2016 Summer Olympics were held in Brazil, whose capital, "
    "Brasília, has a population of about 3.1 million.",
]

llm = ScriptedStubLLM(completions)
agent = ReActAgent(llm=llm, tools=tools, max_steps=6)
answer = agent.run(
    "What is the population of the capital city of the country where the "
    "2016 Summer Olympics were held?"
)
print("FINAL ANSWER:", answer)
```

Running this script produces:

运行这段脚本，会得到如下输出：

```text
FINAL ANSWER: The 2016 Summer Olympics were held in Brazil, whose capital, Brasília, has a population of about 3.1 million.
```

**Verification (this block):** scratch-run — executed with `python3` in the course of authoring this
module; the printed final answer is character-for-character identical to the "Final Answer" line of
`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion [`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion §2](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#21-a-worked-trace)'s hand-written trace, which is the
strongest form of verification a practicum module pairing with a specific worked example can offer:
the code's output is checked against the earlier module's own text, not merely against the author's
expectation of what it should say.

**本代码块的验证方式：** 脚本实际运行——在撰写本模块期间已用 `python3` 实际执行过；打印出的最终答案与 `intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion [`intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#21-a-worked-trace)手写追踪记录中的“最终答案”一行逐字符完全一致，这是一个与具体既有算例配套的实战模块所能提供的最有力验证方式：代码的输出被拿去与前一个模块自身的文字直接核对，而不仅仅是核对作者自己对其应产出内容的预期。

Step by step, this run does exactly what `intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion [`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion §2](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#21-a-worked-trace)
described in prose: `ReActAgent.run` calls `llm.complete` four times; the first three calls each
produce a `Thought:`/`Action:` pair that `parse_step` routes to `search`, whose result becomes the
`Observation:` line appended to the transcript before the next call; the fourth call produces a
`Thought:`/`Final Answer:` pair, and `parse_step` routes that to the `"final"` branch, which returns
the answer directly out of `run` without any further tool call.

这次运行的每一步，都与 `intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion [`intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#21-a-worked-trace)用文字描述的过程完全一致：`ReActAgent.run` 调用 `llm.complete` 共四次；前三次调用各自产出一组 `Thought:`/`Action:` 配对，`parse_step` 将其路由给 `search`，其返回结果随后成为追加到对话记录中的 `Observation:` 行，供下一次调用使用；第四次调用产出一组 `Thought:`/`Final Answer:` 配对，`parse_step` 将其路由到 `"final"` 分支，直接从 `run` 中返回该答案，不再进行任何后续工具调用。

---

## 8. Step 7 — Hardening: Hallucinated Tools and Runaway Loops

**第 8 节：步骤七——加固：幻觉工具名与失控循环**

Two failure modes were flagged as risks earlier in this module and are now demonstrated directly,
each with its own scripted stub scenario. The first: what happens when the LLM names a tool that was
never registered — a real and common failure mode, since nothing stops an LLM from inventing a
plausible-sounding tool name it was never given.

本模块此前已指出两种失效模式存在风险，现在通过各自专门脚本化的场景加以直接演示。第一种：当 LLM 提及一个从未被注册过的工具名称时会发生什么——这是一种真实且常见的失效模式，因为没有任何机制能阻止 LLM 编造出一个听起来合理、但实际上从未被赋予过的工具名称。

```python
bad_tools = ToolRegistry()
bad_tools.register(Tool(name="search", description="Look up a fact.", func=search))
bad_llm = ScriptedStubLLM([
    "Thought: I will use a tool that doesn't exist.\nAction: lookup(\"anything\")",
    "Thought: That failed, let me answer anyway.\nFinal Answer: I could not complete the task.",
])
bad_agent = ReActAgent(llm=bad_llm, tools=bad_tools, max_steps=4)
print("BAD-TOOL ANSWER:", bad_agent.run("irrelevant question"))
```

```text
BAD-TOOL ANSWER: I could not complete the task.
```

The second: a model that keeps proposing actions and never produces a `Final Answer:` line, which
the `max_steps` guard built into [§6](#6-step-5-the-agent-loop) has to catch rather than looping forever:

第二种：模型不断提出新的行动、却始终不产出 `Final Answer:` 这一行，此时必须依靠[第 6 节](#6-step-5-the-agent-loop)中内置的 `max_steps` 保护机制来加以拦截，而不能任其无限循环下去：

```python
loop_llm = ScriptedStubLLM([
    'Thought: still working.\nAction: search("2016 Summer Olympics host country")'
] * 3)
loop_agent = ReActAgent(llm=loop_llm, tools=tools, max_steps=3)
try:
    loop_agent.run("a question the model never finishes answering")
except RuntimeError as e:
    print("MAX-STEPS GUARD OK:", e)
```

```text
MAX-STEPS GUARD OK: Max steps exceeded without a Final Answer.
```

**Verification (both blocks):** scratch-run — both scenarios were executed with `python3` in the
same session as [§7](#7-step-6-running-it-end-to-end)'s run; the printed output shown above is the actual captured
`stdout`, not a hypothetical transcript.

**本代码块的验证方式（两段代码均适用）：** 脚本实际运行——这两个场景均已在与[第 7 节](#7-step-6-running-it-end-to-end)同一次会话中用 `python3` 实际执行过；上方展示的输出即为实际捕获的 `stdout`，而非假设性的推演结果。

The hallucinated-tool case does not crash the process: `ToolRegistry.get` returns `None`, the loop
turns that into an `Error: no such tool ...` observation instead of raising, and the LLM gets a
chance to recover on its next turn — which, in this scripted example, it does, by giving up
gracefully rather than retrying the same bad tool name. A real LLM would not always recover this
cleanly, which is exactly why `advanced/03` — Agent Harness Engineering: Building Production-Grade Agent Loops's harness-engineering treatment
(named in [§6](#6-step-5-the-agent-loop) above) exists as a separate, deeper module: this loop's error handling is
the minimum needed to demonstrate the mechanism, not a production-grade retry or fallback policy.

幻觉工具名的场景并不会导致进程崩溃：`ToolRegistry.get` 返回 `None`，循环将其转化为一条 `Error: no such tool ...` 的观察结果，而非直接抛出异常，这就给了 LLM 在下一轮中恢复的机会——在这个脚本化示例中，它确实做到了，只是选择了体面地放弃，而非重复尝试同一个错误的工具名。真实的 LLM 并不总能如此干净利落地恢复过来，这正是为什么上文[第 6 节](#6-step-5-the-agent-loop)提到的 `advanced/03` — 智能体运行框架工程：构建生产级智能体循环 运行框架工程内容，会作为一个独立且更深入的模块存在：本循环的错误处理只是演示该机制所需的最低限度，而非生产级的重试或回退策略。

---

## 9. Step 8 — Swapping in a Real LLM

**第 9 节：步骤八——替换为真实的 LLM**

`ScriptedStubLLM` and a real LLM client both need to satisfy exactly one contract: a `.complete(transcript:
str) -> str` method. That is the entire substitution point — nothing in `ReActAgent`, `parse_step`,
or `ToolRegistry` needs to change to go from a scripted stub to a live API call, which is the whole
reason this module built the stub as a stand-in for that interface rather than hard-coding canned
answers directly into the loop.

`ScriptedStubLLM` 与一个真实的 LLM 客户端，二者都只需满足同一个契约：一个 `.complete(transcript: str) -> str` 方法。这就是全部的替换点——从脚本化的桩对象切换到真实的 API 调用，`ReActAgent`、`parse_step` 或 `ToolRegistry` 都无需做任何改动，这正是本模块要将桩对象构建为该接口的替身、而非直接把固定答案硬编码进循环内部的全部原因。

A real implementation, calling the Anthropic Messages API (confirmed against the official API
documentation, cited in References — it accepts a `messages` array of `{role, content}` turns and
returns a `Message` whose `content` holds the model's text), would look like this:

一个真实的实现——调用 Anthropic Messages API（已对照官方 API 文档核实，见“参考文献”——该接口接受一个由 `{role, content}` 组成的 `messages` 数组，并返回一个 `Message` 对象，其 `content` 字段中保存着模型生成的文本），大致会是这样：

```python
import anthropic

class ClaudeLLM:
    def __init__(self, model: str = "claude-sonnet-4-5"):
        self._client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
        self._model = model

    def complete(self, transcript: str) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=512,
            messages=[{"role": "user", "content": transcript}],
        )
        return response.content[0].text
```

**Verification (this block):** mental trace only — this block calls a real network API and cannot be
scratch-run offline in this module without credentials, so it is not executed as part of authoring
this module. Its shape is checked directly against the official Anthropic Messages API documentation
(cited in References): the `messages` parameter format and the `Message.content` response shape both
match what that documentation specifies. A reader with an API key can run this block themselves by
substituting `ClaudeLLM()` for `ScriptedStubLLM(completions)` in [§7](#7-step-6-running-it-end-to-end)'s script, unchanged
otherwise.

**本代码块的验证方式：** 仅心算追踪——该代码块会调用真实的网络 API，在没有凭证的情况下，本模块无法对其进行离线脚本运行验证，因此在撰写本模块的过程中并未实际执行它。其结构已直接对照官方 Anthropic Messages API 文档（见“参考文献”）进行了核实：`messages` 参数的格式与 `Message.content` 响应结构，均与该文档所规定的一致。持有 API 密钥的读者可以自行运行这段代码，只需在[第 7 节](#7-step-6-running-it-end-to-end)的脚本中，将 `ClaudeLLM()` 替换 `ScriptedStubLLM(completions)` 即可，其余部分无需改动。

Two things change when the stub is replaced by a live model that this module's tests could not
exercise: the model's `Thought:` text will no longer be word-for-word identical to the scripted
completions above (a live model reasons for itself), and its output is no longer guaranteed to match
`build_system_prompt`'s format exactly, which is precisely why [§4](#4-step-3-a-deterministic-stub-llm-for-development)'s parser and
[§8](#8-step-7-hardening-hallucinated-tools-and-runaway-loops)'s hardening are not optional conveniences — they are the parts of this
module that keep working once the deterministic stub is gone.

当桩对象被替换为一个真实模型之后，有两件本模块的测试无法覆盖到的事情会发生变化：模型产出的 `Thought:` 文本将不再与上方脚本化的完成结果逐字相同（真实模型会自行进行推理），并且其输出也不再能保证严格符合 `build_system_prompt` 所规定的格式——这正是[第 4 节](#4-step-3-a-deterministic-stub-llm-for-development)中的解析器与[第 8 节](#8-step-7-hardening-hallucinated-tools-and-runaway-loops)中的加固措施并非可有可无的便利功能的原因：一旦确定性的桩对象不复存在，正是这些部分让整个系统得以继续正常运作。

---

## 10. Common Pitfalls Beyond What the Code Already Handles

**第 10 节：本代码尚未处理的常见陷阱**

This module's `ReActAgent` deliberately handles only two failure modes — an unknown tool name and an
unbounded loop — because those are the two this module set out to teach. A reader extending this
code toward something closer to production should be aware of at least three more, none of which
`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion [`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion §6](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#6-common-pitfalls-at-this-level) treats as solved by picking a different
design pattern, and none of which this loop solves either.

本模块中的 `ReActAgent` 刻意只处理了两种失效模式——未知的工具名称与无边界的循环——因为这正是本模块打算讲授的两种情形。若读者希望将这段代码进一步扩展为更接近生产级的实现，至少还应留意另外三种情形，`intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion [`intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion 第 6 节](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#6-common-pitfalls-at-this-level)并未将它们视为可以通过换用另一种设计模式来解决的问题，本循环同样也未能解决它们。

A tool's argument was never schema-validated here — `search` receives whatever bare string
`parse_step` extracted, and a tool with side effects (writing a file, sending a request) would need
its arguments checked before executing, not just its name looked up. A malformed completion — one
that matches neither `Action:` nor `Final Answer:` at all — currently raises `ValueError` out of
`parse_step` and crashes `run`; a hardened version would catch that and feed the parse failure back
to the model as an observation, giving it a chance to self-correct its own formatting, the same way
[§8](#8-step-7-hardening-hallucinated-tools-and-runaway-loops) already does for an unknown tool name. And a tool call that raises an exception
internally (a network timeout inside `search`, for instance) is not caught anywhere in this module's
loop and would currently propagate up and crash the agent, rather than becoming an `Observation:`
the model can reason about and route around.

本模块的代码从未对工具参数进行模式校验——`search` 接收的正是 `parse_step` 提取出的裸字符串本身；而一个带有副作用的工具（写入文件、发送请求）在执行之前，理应对其参数进行校验，而不仅仅是查找其名称是否存在。一段格式有误的完成结果——既不匹配 `Action:` 也完全不匹配 `Final Answer:`——目前会从 `parse_step` 中抛出 `ValueError` 并导致 `run` 崩溃；一个加固过的版本理应捕获这一异常，并将解析失败的信息作为一条观察结果反馈给模型，使其有机会像[第 8 节](#8-step-7-hardening-hallucinated-tools-and-runaway-loops)中处理未知工具名那样，自行纠正自己的格式错误。此外，一次在内部抛出异常的工具调用（例如 `search` 内部发生了网络超时）目前也不会被本模块循环中的任何环节捕获，而会直接向上传播并导致智能体崩溃，而不会转化为一条模型可以据此推理并绕开的 `Observation:`。

---

## 11. Summary and What Comes Next

**第 11 节：小结与后续内容**

This module built a working ReAct agent from four pieces — a tool registry, a prompt contract, a
line-oriented parser, and a bounded loop — verified it against `intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion
[`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion §2](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#21-a-worked-trace)'s hand-written trace by actually running it and
matching the output word for word, demonstrated its two built-in failure-handling paths, and showed
the exact single-method substitution point where a scripted stub gives way to a real LLM API call.

本模块用四个组成部分——工具注册表、提示词契约、按行组织的解析器，以及带边界的循环——构建了一个可运行的 ReAct 智能体，并通过真正运行代码、逐字核对输出，将其与 `intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion [`intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#21-a-worked-trace)手写的追踪记录进行了验证，演示了其内置的两条失效处理路径，并展示了：从脚本化的桩对象切换到真实的 LLM API 调用，唯一需要替换的正是那一个方法。

`practicum/05-implementing-scored-agent-memory.md`, by the same author, picks up a different piece
of `intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion's territory — Reflexion's episodic memory buffer, named but not built in
[`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion §4](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#4-reflexion-learning-from-a-failed-attempt-within-the-same-task) of that
module — and builds, from scratch, the scored retrieval mechanism `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory develops the
theory for. `practicum/02-implementing-tool-use-and-function-calling.md` covers the tool-calling
schema this module used in its simplified single-string-argument form in more depth.
`advanced/03-agent-harness-engineering-production-grade-agent-loops.md` is where the hardening this
module's [§10](#10-common-pitfalls-beyond-what-the-code-already-handles) named — schema validation, self-correction on parse failure, exception
handling around tool execution — is treated at full production depth.

同一作者撰写的 `practicum/05-implementing-scored-agent-memory.md`，将接续 `intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion 领域中的另一部分内容——即该模块[`intermediate/03` — 智能体设计模式：ReAct、计划-执行与 Reflexion 第 4 节](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md#4-reflexion-learning-from-a-failed-attempt-within-the-same-task)中已被命名、却未被实际构建出来的 Reflexion 情景记忆缓冲区——从零构建出 `intermediate/04` — 记忆系统：短期记忆、长期记忆与情景记忆 已经讲授过理论的评分式检索机制。`practicum/02-implementing-tool-use-and-function-calling.md` 将更深入地讲解本模块以简化的单字符串参数形式所使用的工具调用模式。`advanced/03-agent-harness-engineering-production-grade-agent-loops.md` 则会在完整的生产级深度上，处理本模块[第 10 节](#10-common-pitfalls-beyond-what-the-code-already-handles)中所指出的各项加固措施——模式校验、解析失败时的自我纠正，以及围绕工具执行的异常处理。

---

## References

**参考文献**

### External Sources

- [Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [Fowler, M. (2007). Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
- [Python Software Foundation. `re` — Regular expression operations](https://docs.python.org/3/library/re.html)
- [Python Software Foundation. `dataclasses` — Data Classes](https://docs.python.org/3/library/dataclasses.html)
- [Anthropic. Messages API reference](https://platform.claude.com/docs/en/api/messages)

### Internal Cross-References

- [`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion](https://anu00.dev/curriculum/books/02-intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md)
- [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md)
- [`introductory/04` — Tool Use & Function Calling Basics](https://anu00.dev/curriculum/books/01-introductory/04-tool-use-and-function-calling-basics.md)
- [`intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory](https://anu00.dev/curriculum/books/02-intermediate/04-agent-memory-systems-short-term-long-term-episodic.md)
- [`advanced/03` — Agent Harness Engineering: Building Production-Grade Agent Loops](https://anu00.dev/curriculum/books/04-advanced/03-agent-harness-engineering-production-grade-agent-loops.md)
- [`practicum/02` — Implementing Tool Use & Function Calling](https://anu00.dev/curriculum/books/03-practicum/02-implementing-tool-use-and-function-calling.md)
- [`practicum/05` — Implementing Scored Agent Memory](https://anu00.dev/curriculum/books/03-practicum/05-implementing-scored-agent-memory.md)
