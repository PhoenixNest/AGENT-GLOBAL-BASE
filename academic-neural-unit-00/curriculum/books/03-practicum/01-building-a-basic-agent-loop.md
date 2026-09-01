# Building a Basic Agent Loop

**构建一个基础智能体循环**

| Field   | English                                                                 | 中文                                        |
| ------- | ----------------------------------------------------------------------- | ------------------------------------------- |
| Level   | Practicum                                                               | 实战                                        |
| Cluster | Hands-On Coding Practicum                                               | 动手编程实战                                |
| Author  | Dr. Kaito Fujimori, Research Scientist — Agent Systems Research, ANU-00 | ANU-00 智能体系统研究员 Kaito Fujimori 博士 |

---

## 1. What This Module Builds

**本模块要构建什么**

[`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md) is the prerequisite for this module, and it did the conceptual work already: it defined an AI agent as a system whose LLM core repeatedly perceives an observation, thinks about what to do, acts on its environment, and observes the result — the **agent loop** — and it walked through that loop by hand for a weather-checking example. This module does not repeat that theory. Its job is narrower and more concrete: take the loop [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop §3](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#3-the-agent-loop-perceive-think-act-observe) described in prose and a table, and build it as real, runnable Python — the same weather example, traced in code instead of in a diagram.

[`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md)是本模块的前置模块，其中的概念性工作已经完成：它把 AI 智能体定义为一种系统，其 LLM 核心反复地感知观察、思考该做什么、作用于环境、再观察结果——即**智能体循环**——并以一个查询天气的例子手动演示了这一循环。本模块不会重复这部分理论，它的任务更加聚焦、也更加具体：把[`introductory/03` — 什么是 AI 智能体？概念与智能体循环 第 3 节](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#3-the-agent-loop-perceive-think-act-observe)以文字与表格描述的循环，构建成真实、可运行的 Python 代码——同一个天气示例，这次不是用图表追踪，而是用代码追踪。

By the end of this module you will have built, from nothing, a working single-tool agent loop: a small set of Python types representing a decision, a stand-in for the LLM's decision-making step, one deterministic tool, a loop that wires perceive/think/act/observe together, and two guardrails against the two failure modes [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop §8](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#8-common-failure-modes-of-the-agent-loop) named as recurring across nearly all agent systems: infinite looping and hallucinated actions. What this module deliberately does _not_ build is a general-purpose tool registry, JSON-Schema-based tool definitions, or multi-tool dispatch — those are the subject of the next module, [`practicum/02` — Implementing Tool Use & Function Calling](https://anu00.dev/curriculum/books/03-practicum/02-implementing-tool-use-and-function-calling.md), which picks up exactly where this one leaves off.

读完本模块后，你将从零构建出一个可运行的单工具智能体循环：一组表示决策的 Python 类型、一个替代 LLM 决策步骤的“替身”函数、一个确定性工具、一个把感知/思考/行动/观察连接起来的循环，以及针对[`introductory/03` — 什么是 AI 智能体？概念与智能体循环 第 8 节](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#8-common-failure-modes-of-the-agent-loop)所指出的两种在几乎所有智能体系统中反复出现的失效模式——无限循环与幻觉行动——所设计的两道防护。本模块刻意*不会*构建通用的工具注册表、基于 JSON Schema 的工具定义，或多工具分发机制——这些是下一模块[`practicum/02` — Implementing Tool Use & Function Calling](https://anu00.dev/curriculum/books/03-practicum/02-implementing-tool-use-and-function-calling.md)的主题，它会正好从本模块结束的地方接续下去。

Every code block below was run against a real Python 3 interpreter while this module was authored, not merely reasoned about on paper — the verification method stated after each block records exactly how, per this practicum's code-verification rule.

下文的每一个代码块，在撰写本模块的过程中都曾在真实的 Python 3 解释器中实际运行过，而不仅仅是停留在纸面推理——每个代码块之后都会按照本实战系列的代码验证规则，说明具体采用的验证方式。

---

## 2. The Shape of a Decision

**决策的形态**

[`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop §3](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#3-the-agent-loop-perceive-think-act-observe) said that the "think" stage "produces a decision: either a final answer, or the next action to take." Before writing any loop logic, it is worth pausing on that sentence, because it is already a complete specification for the first piece of code: a decision is always exactly one of two shapes, never both, and never neither.

[`introductory/03` — 什么是 AI 智能体？概念与智能体循环 第 3 节](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#3-the-agent-loop-perceive-think-act-observe)提到，“思考”阶段“产出一个决策：要么给出最终答案，要么决定下一步要采取的行动”。在动手编写任何循环逻辑之前，值得先停下来推敲这句话，因为它其实已经构成了第一段代码的完整规格说明：一个决策永远恰好是这两种形态之一，不会同时是两者，也不会两者都不是。

Python's `dataclasses` module, part of the standard library, is the natural tool for representing this kind of small, named, structured value: a decorator that automatically generates an `__init__` method (and a few other conveniences) for a class whose job is mainly to hold typed fields. The official documentation describes it as providing "a decorator and functions for automatically adding generated special methods such as `__init__()` and `__repr__()` to user-defined classes" — exactly the boilerplate a hand-written `ToolCall` or `FinalAnswer` class would otherwise need.

Python 标准库中的 `dataclasses` 模块，是表示这类小型、具名、结构化数值的自然工具：它是一个装饰器，能为一个主要用于承载带类型字段的类，自动生成 `__init__` 方法（以及其他若干便利功能）。官方文档将其描述为“提供一个装饰器与若干函数，用于给用户自定义的类自动添加诸如 `__init__()` 与 `__repr__()` 之类的生成方法”——这正是手写 `ToolCall` 或 `FinalAnswer` 这类类时原本需要自己编写的样板代码。

```python
from dataclasses import dataclass
from typing import Union


@dataclass
class ToolCall:
    """A decision to invoke the one available tool with a given argument."""
    tool_name: str
    argument: str


@dataclass
class FinalAnswer:
    """A decision that no further action is needed; this text goes back to the user."""
    text: str


# A "think" step always returns one of these two shapes -- never both, never neither.
Decision = Union[ToolCall, FinalAnswer]
```

**Verification: scratch-run.** Both classes were constructed interactively (`ToolCall(tool_name="get_weather", argument="Tokyo")` and `FinalAnswer(text="done")`) and printed to confirm the auto-generated `__repr__` renders both field name and value, matching the dataclasses documentation's description of the generated methods.

**验证方式：草稿运行。** 这两个类都曾以交互方式构造过（`ToolCall(tool_name="get_weather", argument="Tokyo")` 与 `FinalAnswer(text="done")`），并打印输出以确认自动生成的 `__repr__` 会同时显示字段名与字段值，这与 dataclasses 文档中对其自动生成方法的描述相符。

`Union[ToolCall, FinalAnswer]`, from the standard library's `typing` module, is not a new class — it is a type-hint that documents, for the benefit of both a human reader and a type checker, that any value flowing through this slot must be one or the other. It carries no runtime behavior of its own; the loop below still has to check _which_ one it received with a plain `isinstance` test, the same way any Python code distinguishes between two possible types at runtime.

`Union[ToolCall, FinalAnswer]` 来自标准库中的 `typing` 模块，它并不是一个新的类，而是一个类型提示，用于向人类读者与类型检查器共同表明：流经此处的值必然是二者之一。它本身不带有任何运行时行为；下文的循环仍然需要用一次普通的 `isinstance` 判断来确定收到的究竟是哪一种，就像任何 Python 代码在运行时区分两种可能类型时所做的那样。

---

## 3. A Deterministic Stand-In for the "Think" Step

**“思考”步骤的确定性替身**

A real agent's "think" step calls an LLM. This module deliberately does not — connecting to a real LLM API requires credentials, network access, and a specific provider's SDK, none of which belong in a curriculum module that must run identically for every reader with nothing more than a Python interpreter. Instead, this module writes `think` as a small, deterministic function that inspects the conversation history and returns a `Decision` using plain `if`/`else` logic, standing in for what an LLM's judgment would otherwise decide.

真实智能体的“思考”步骤会调用一个 LLM。本模块刻意不这样做——连接真实 LLM API 需要凭证、网络访问，以及某个具体提供商的 SDK，这些都不适合出现在一个必须让每位读者仅凭一个 Python 解释器就能原样运行的课程模块中。取而代之，本模块把 `think` 写成一个小型、确定性的函数，它检查对话历史，并用普通的 `if`/`else` 逻辑返回一个 `Decision`，替代原本应由 LLM 的判断力所做出的决定。

This kind of stand-in has a name in software engineering: Martin Fowler's widely cited article on test doubles describes a **stub** as an object that "provide[s] canned answers to calls made during the test, usually not responding at all to anything outside what's programmed in for the test" — used to replace a real, often external, dependency with something predictable enough to reason about and reproduce. The `think` function below is a stub for an LLM call in exactly this sense: predictable and reproducible, at the cost of not being genuinely intelligent. Section 9 returns to what changes, and what does not, when this stub is replaced with a real API call.

这类替身在软件工程中有一个专门的名称：Martin Fowler 那篇被广泛引用的关于测试替身的文章，将**桩（stub）**描述为一种对象，它“在测试过程中，为被调用的请求提供预先设定好的答案，通常对测试中未编程设定的其他任何情况都不作任何响应”——用于把一个真实的、往往是外部的依赖，替换为足够可预测、便于推理与复现的东西。下文的 `think` 函数正是在这个意义上充当了 LLM 调用的桩：它是可预测、可复现的，代价是它并不具备真正的智能。第 9 节会讨论，当这一“桩”被替换为真实的 API 调用时，哪些部分会改变，哪些部分不会。

```python
def think(history: list) -> "Decision":
    """
    A deterministic stand-in for the LLM's 'think' step (introductory/03 SS3).
    A real deployment replaces this function's body with an actual LLM API call;
    everything else in this module works identically either way, because the
    loop in SS5 only depends on `think` returning a Decision -- it never depends
    on how that decision was produced.
    """
    last_entry = history[-1]

    if last_entry.startswith("user_request:"):
        request_text = last_entry[len("user_request:"):].strip()
        for city in ("tokyo", "osaka"):
            if city in request_text.lower():
                return ToolCall(tool_name="get_weather", argument=city.capitalize())
        return FinalAnswer(text="I can only check the weather for Tokyo or Osaka right now.")

    if last_entry.startswith("tool_result:"):
        result_text = last_entry[len("tool_result:"):].strip()
        return FinalAnswer(text=f"Here is what I found: {result_text}")

    return FinalAnswer(text="I'm not sure how to proceed.")
```

**Verification: scratch-run.** Called directly with three constructed histories: `["user_request:What's the weather in Tokyo right now?"]` returned `ToolCall(tool_name='get_weather', argument='Tokyo')`; `["user_request:What's the weather in Paris right now?"]` returned a `FinalAnswer` declining the city; `["user_request:...", "tool_result:{'condition': 'rain', 'temp_c': 19}"]` returned a `FinalAnswer` summarizing that result — all three matched the intended branch.

**验证方式：草稿运行。** 曾以三段构造好的历史直接调用该函数：`["user_request:What's the weather in Tokyo right now?"]` 返回 `ToolCall(tool_name='get_weather', argument='Tokyo')`；`["user_request:What's the weather in Paris right now?"]` 返回一个婉拒该城市的 `FinalAnswer`；`["user_request:...", "tool_result:{'condition': 'rain', 'temp_c': 19}"]` 返回一个总结该结果的 `FinalAnswer`——三种情况均命中了预期的分支。

Notice the encoding used for history entries: a plain string with a `"user_request:"` or `"tool_result:"` prefix. This is intentionally the simplest possible representation, not a design recommendation — it is just barely enough structure for `think` to tell "this is the original question" apart from "this is a result I asked for." Real harnesses use much richer structures (typed message objects, role fields, timestamps); [`introductory/06` — Context Windows, Tokens & Memory Basics](https://anu00.dev/curriculum/books/01-introductory/06-context-windows-tokens-and-memory-basics.md) covers how that accumulated history is actually managed once it grows large.

请注意历史条目所采用的编码方式：一个带有 `"user_request:"` 或 `"tool_result:"` 前缀的普通字符串。这是刻意选择的、能想到的最简单表示方式，而非一种设计推荐——它仅仅提供了勉强足够的结构，使 `think` 能够区分“这是最初的问题”与“这是我请求得到的结果”。真实的运行框架会使用远为丰富的结构（带类型的消息对象、角色字段、时间戳等）；[`introductory/06` — Context Windows, Tokens & Memory Basics](https://anu00.dev/curriculum/books/01-introductory/06-context-windows-tokens-and-memory-basics.md)会讲解当这份累积历史变得庞大之后，实际应当如何管理。

---

## 4. The One Tool: A Deterministic Weather Function

**唯一的工具：一个确定性天气函数**

[`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop §4](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#4-worked-example-a-weather-checking-agent-traced-step-by-step) used a tool `get_weather(city: str) -> dict` that "calls a real weather API." This module's version calls no network at all — it looks a city up in a small, hardcoded dictionary — for the same reproducibility reason `think` is a stub rather than a real LLM call: a reader running this code five years from now, offline, on any machine, should see exactly the trace shown below, not whatever a live weather service happens to report that day.

[`introductory/03` — 什么是 AI 智能体？概念与智能体循环 第 4 节](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#4-worked-example-a-weather-checking-agent-traced-step-by-step)所使用的工具 `get_weather(city: str) -> dict` 会“调用一个真实的天气 API”。本模块的版本则完全不访问网络——它只是在一个小型、硬编码的字典中查找某个城市——原因与 `think` 之所以是一个“桩”而非真实 LLM 调用相同：一位读者即便五年后、离线、在任意一台机器上运行这段代码，也应当看到下文完全一致的追踪结果，而不是某个实时天气服务当天恰好报告的数据。

```python
def get_weather(city: str) -> dict:
    """A deterministic stand-in for a real weather API call, so the trace below
    is exactly reproducible for every reader, on every machine, indefinitely."""
    fake_weather_db = {
        "tokyo": {"condition": "rain", "temp_c": 19},
        "osaka": {"condition": "sunny", "temp_c": 24},
    }
    key = city.strip().lower()
    if key not in fake_weather_db:
        return {"error": f"city not found: {city}"}
    return fake_weather_db[key]


# The harness's map from a tool's name (as think() might request it) to the real
# callable that actually runs it -- introductory/03 SS3's "harness executes it".
TOOLS = {"get_weather": get_weather}
```

**Verification: scratch-run.** `get_weather("Tokyo")` returned `{'condition': 'rain', 'temp_c': 19}`; `get_weather("  TOKYO  ")` returned the identical dict, confirming the `strip().lower()` normalization; `get_weather("Atlantis")` returned `{'error': 'city not found: Atlantis'}` rather than raising, confirming the not-found branch produces a value, not an exception.

**验证方式：草稿运行。** `get_weather("Tokyo")` 返回 `{'condition': 'rain', 'temp_c': 19}`；`get_weather("  TOKYO  ")` 返回完全相同的字典，确认了 `strip().lower()` 的归一化处理生效；`get_weather("Atlantis")` 返回 `{'error': 'city not found: Atlantis'}` 而非抛出异常，确认“未找到”分支产出的是一个值，而不是一次异常。

The `TOOLS` dictionary deserves a second look, because it is the smallest possible version of an idea this module's sequel builds out in full. Mapping a tool's _name_ (a plain string the "think" step can put inside a `ToolCall`) to the _callable_ that actually performs it is exactly what a tool registry does — [`practicum/02` — Implementing Tool Use & Function Calling §3](https://anu00.dev/curriculum/books/03-practicum/02-implementing-tool-use-and-function-calling.md#3-a-tool-registry-a-place-for-tools-to-live) generalizes this one-line dictionary into a proper `ToolRegistry` class that also carries a schema and supports more than one tool.

`TOOLS` 这个字典值得再多看一眼，因为它正是本模块后续篇章将要完整展开的那个想法的最小雏形。把工具的*名称*（“思考”步骤可以放入 `ToolCall` 中的一个普通字符串）映射到真正执行它的*可调用对象*，正是工具注册表所做的事情——[`practicum/02` — 实现工具使用与函数调用 第 3 节](https://anu00.dev/curriculum/books/03-practicum/02-implementing-tool-use-and-function-calling.md#3-a-tool-registry-a-place-for-tools-to-live)会把这一行字典泛化为一个正式的 `ToolRegistry` 类，它还会携带模式定义，并支持不止一个工具。

---

## 5. The Loop: Wiring Perceive, Think, Act, and Observe Together

**循环本身：把感知、思考、行动、观察连接起来**

With a `Decision` shape, a `think` stub, and a tool in hand, the loop itself is now mostly bookkeeping: call `think`, branch on what it returned, and if it was a `ToolCall`, run the tool and record the result as a new history entry before looping again. This is the same four-stage cycle from [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop §3](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#3-the-agent-loop-perceive-think-act-observe), just given a name for each stage in a comment so the mapping from prose to code is explicit rather than implied.

有了 `Decision` 的形态、`think` 替身，以及一个工具，循环本身现在主要就只是记账工作：调用 `think`，根据其返回值分支处理，如果是 `ToolCall`，就运行该工具，并把结果作为一条新的历史条目记录下来，然后再次循环。这正是[`introductory/03` — 什么是 AI 智能体？概念与智能体循环 第 3 节](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#3-the-agent-loop-perceive-think-act-observe)中的同一个四阶段循环，只是在注释中为每个阶段标注了名称，使“文字描述”到“代码”的对应关系变得明确，而非只能靠读者自行揣摩。

```python
def run_agent_loop(user_request: str, max_steps: int = 5) -> str:
    # Perceive (step 1, before the loop): the very first observation is the
    # user's request itself.
    history = [f"user_request:{user_request}"]

    for step in range(1, max_steps + 1):
        # Think: the LLM (here, its stub) decides the next Decision.
        decision = think(history)
        print(f"Step {step} -- think: {decision}")

        if isinstance(decision, FinalAnswer):
            return decision.text

        # decision is a ToolCall from here on.
        if decision.tool_name not in TOOLS:
            history.append(
                f"tool_result:{{'error': 'no such tool: {decision.tool_name}'}}"
            )
            continue

        # Act: the harness -- this function, not the LLM -- runs the real tool.
        tool_fn = TOOLS[decision.tool_name]
        result = tool_fn(decision.argument)
        print(f"Step {step} -- act: called {decision.tool_name}({decision.argument!r}) -> {result}")

        # Observe: the tool's result becomes the next perceived observation.
        history.append(f"tool_result:{result}")

    raise RuntimeError(f"Agent did not reach a final answer within {max_steps} steps.")
```

**Verification: scratch-run.** `run_agent_loop("What's the weather in Tokyo right now?")` printed a two-step trace (one `think`/`act` pair for the tool call, one `think` for the final answer) and returned `"Here is what I found: {'condition': 'rain', 'temp_c': 19}"`, matching the two-iteration trace [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop §4](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#4-worked-example-a-weather-checking-agent-traced-step-by-step) described by hand.

**验证方式：草稿运行。** `run_agent_loop("What's the weather in Tokyo right now?")` 打印出一个两步追踪（一次工具调用的 think/act 组合，以及一次给出最终答案的 think），并返回 `"Here is what I found: {'condition': 'rain', 'temp_c': 19}"`，与[`introductory/03` — 什么是 AI 智能体？概念与智能体循环 第 4 节](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#4-worked-example-a-weather-checking-agent-traced-step-by-step)手动演示的两次迭代追踪一致。

Two details are worth calling out explicitly. First, the `if decision.tool_name not in TOOLS` branch does not exist yet for correctness of the happy path — the weather example never triggers it — it exists because a "think" step, real or stubbed, can propose a tool that was never registered, and the loop must not crash when that happens; §7 exercises this branch directly. Second, `max_steps` bounds how many times the loop can run before giving up; §6 explains why this bound is not an optional nicety.

有两个细节值得特别指出。第一，`if decision.tool_name not in TOOLS` 这一分支的存在，并非为了让“顺利路径”正确运行——天气示例根本不会触发它——它的存在是因为“思考”步骤，无论真实还是替身，都可能提议一个从未注册过的工具，而循环在这种情况发生时绝不能崩溃；第 7 节会直接演练这一分支。第二，`max_steps` 限定了循环在放弃之前最多可以运行多少次；第 6 节将解释这一限制为何并非一个可有可无的锦上添花。

---

## 6. Guarding Against Infinite Looping

**防范无限循环**

[`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop §8](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#8-common-failure-modes-of-the-agent-loop) named **infinite looping** as happening "when the LLM repeatedly chooses an action, observes a result, and fails to recognize that the task is either complete or unsolvable" — and it named the fix in the same sentence: "harnesses guard against this with a maximum-step limit." That guard is already sitting in the loop above (`max_steps`, and the `RuntimeError` raised when the `for` loop exhausts its range without an early `return`); this section exists to prove it actually fires, rather than trusting that it would.

[`introductory/03` — 什么是 AI 智能体？概念与智能体循环 第 8 节](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#8-common-failure-modes-of-the-agent-loop)将**无限循环**定义为“发生在 LLM 反复选择行动、观察结果，却始终未能识别任务已完成或已无法解决”的情形——并在同一句话中给出了解决办法：“运行框架通常以最大步数限制来防范此问题”。上文的循环中已经内置了这一防护（`max_steps`，以及当 `for` 循环耗尽其范围却始终未提前 `return` 时抛出的 `RuntimeError`）；本节的目的正是要证明它确实会被触发，而不是仅仅相信它会。

To exercise this, temporarily swap in a broken `think` that always proposes the same tool call and never returns a `FinalAnswer` — modeling exactly the failure [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop §8](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#8-common-failure-modes-of-the-agent-loop) described: the LLM never recognizes the task is complete.

为验证这一点，可以临时替换成一个有缺陷的 `think`，它总是提议同一个工具调用、且从不返回 `FinalAnswer`——这恰好模拟了[`introductory/03` — 什么是 AI 智能体？概念与智能体循环 第 8 节](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#8-common-failure-modes-of-the-agent-loop)所描述的失效情形：LLM 始终无法识别任务已经完成。

```python
def never_finishes(history: list) -> "Decision":
    return ToolCall(tool_name="get_weather", argument="Tokyo")


original_think = think
globals()["think"] = never_finishes
try:
    run_agent_loop("What's the weather in Tokyo right now?", max_steps=3)
except RuntimeError as exc:
    print("Caught expected error:", exc)
globals()["think"] = original_think
```

**Verification: scratch-run.** With `max_steps=3` and `think` swapped for `never_finishes`, the loop printed three `think`/`act` pairs (each calling `get_weather("Tokyo")` again) and then raised `RuntimeError: Agent did not reach a final answer within 3 steps.`, caught exactly as shown — confirming the guard fires rather than looping forever.

**验证方式：草稿运行。** 在 `max_steps=3` 且 `think` 被替换为 `never_finishes` 的情况下，循环打印出三组 think/act（每次都重新调用 `get_weather("Tokyo")`），随后抛出 `RuntimeError: Agent did not reach a final answer within 3 steps.`，并如上所示被正确捕获——这确认了该防护确实会被触发，而不是让循环无限运行下去。

A max-step limit is a blunt instrument on purpose: it does not try to detect _why_ the loop isn't converging, only _that_ it hasn't after a fixed budget. More refined approaches — detecting a repeated identical action, or having the LLM itself periodically judge whether it is making progress — exist and are used in production harnesses, but they are refinements on top of this baseline, not replacements for it; even a system with smarter loop-detection still keeps a hard step ceiling as the last line of defense.

最大步数限制之所以设计得如此“简单粗暴”，是有意为之：它并不试图判断循环*为何*没有收敛，只判断在固定的预算耗尽后循环*是否*收敛了。更精细的方法——例如检测重复出现的相同行动，或让 LLM 自身定期判断是否正在取得进展——确实存在，并被用于生产环境的运行框架中，但它们是建立在这一基线之上的改进，而非对它的替代；即便是配有更智能的循环检测机制的系统，通常仍会保留一个硬性的步数上限作为最后一道防线。

---

## 7. Guarding Against Hallucinated Actions

**防范幻觉行动**

The same section of [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#8-common-failure-modes-of-the-agent-loop) named a second failure mode: **hallucinated actions**, which "happen when the LLM's 'think' step produces a call to a tool that does not exist" — and stated the fix identically in shape to the first: "the harness must validate every proposed action before executing it, never trust the LLM's output blindly." The `if decision.tool_name not in TOOLS` branch inside `run_agent_loop` (§5) is that validation, in its simplest possible form: a membership check against the one tool the harness actually knows how to run.

[`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#8-common-failure-modes-of-the-agent-loop)同一节还指出了第二种失效模式：**幻觉行动**，即“发生在 LLM 的‘思考’步骤生成了一次调用不存在的工具”的情形——并给出了与第一种失效模式形式完全一致的解决办法：“运行框架必须在执行任何提议行动之前对其进行校验，绝不能盲目信任 LLM 的输出”。`run_agent_loop`（第 5 节）内部的 `if decision.tool_name not in TOOLS` 分支，正是这种校验最简单的形式：针对运行框架真正知道如何执行的这一个工具，做一次成员检查。

To see it fire, swap in a `think` that hallucinates a tool the harness never registered.

为观察其触发效果，可以替换成一个会“幻觉”出运行框架从未注册过的工具的 `think`。

```python
def hallucinating_think(history: list) -> "Decision":
    last_entry = history[-1]
    if last_entry.startswith("user_request:"):
        return ToolCall(tool_name="get_stock_price", argument="AAPL")  # never registered
    return FinalAnswer(text=f"recovered after: {last_entry}")


globals()["think"] = hallucinating_think
answer = run_agent_loop("What's AAPL trading at?")
print("Final answer:", answer)
globals()["think"] = original_think
```

**Verification: scratch-run.** Step 1 proposed `get_stock_price`, which is absent from `TOOLS`; the loop appended `tool_result:{'error': 'no such tool: get_stock_price'}` to the history instead of raising or crashing, and step 2's `think` call produced `FinalAnswer(text="recovered after: tool_result:{'error': 'no such tool: get_stock_price'}")` — the agent recovered gracefully and reported the failure rather than pretending to know AAPL's price.

**验证方式：草稿运行。** 第一步提议调用 `get_stock_price`，而它并不在 `TOOLS` 中；循环把 `tool_result:{'error': 'no such tool: get_stock_price'}` 追加到历史记录中，而不是抛出异常或崩溃；第二步的 `think` 调用产出 `FinalAnswer(text="recovered after: tool_result:{'error': 'no such tool: get_stock_price'}")`——智能体优雅地完成了恢复，并如实报告了失败，而不是假装自己知道 AAPL 的股价。

It is worth being honest about how shallow this particular guard is: it checks only that the tool's _name_ is known, not that its _arguments_ are well-formed or of the right type. A `ToolCall(tool_name="get_weather", argument=42)` would sail straight through this check and fail, if at all, only once `get_weather` itself tried to call `.strip()` on an integer. Real, production-grade validation checks the full shape of a proposed call against a declared schema before ever touching the real function — this is precisely the gap [`practicum/02` — Implementing Tool Use & Function Calling](https://anu00.dev/curriculum/books/03-practicum/02-implementing-tool-use-and-function-calling.md) closes, and it is the reason that module exists as a separate, deeper treatment rather than a paragraph appended to this one.

有必要坦率地指出这一具体防护有多么“浅”：它只检查了工具的*名称*是否已知，并未检查其*参数*是否格式正确或类型是否恰当。一个 `ToolCall(tool_name="get_weather", argument=42)` 会毫无阻碍地通过这一检查，即便真的出错，也要等到 `get_weather` 本身试图对一个整数调用 `.strip()` 时才会发生。真正生产级别的校验，会在触碰真正的函数之前，就依照声明好的模式检查被提议调用的完整形态——这正是[`practicum/02` — Implementing Tool Use & Function Calling](https://anu00.dev/curriculum/books/03-practicum/02-implementing-tool-use-and-function-calling.md)所要弥补的缺口，也正是该模块之所以作为一篇独立、更深入的专门论述，而非在本篇末尾附加一段文字的原因。

---

## 8. Running It End to End

**端到端完整运行**

Assembled in one place — the imports, the two types, `think`, `get_weather`, `TOOLS`, and `run_agent_loop`, in that order — this module's code is a complete, self-contained Python program with no external dependencies beyond the standard library. A reader can paste every code block from §§2–5 into a single file and run it directly.

把导入语句、两个类型、`think`、`get_weather`、`TOOLS` 以及 `run_agent_loop` 依次组装在一起，本模块的代码就构成了一个完整、自成一体的 Python 程序，除标准库外不依赖任何外部库。读者可以把[第 2–5 节](#2-the-shape-of-a-decision)的每一段代码依次粘贴进同一个文件中，直接运行。

```python
if __name__ == "__main__":
    final_text = run_agent_loop("What's the weather in Tokyo right now?")
    print("Final answer:", final_text)
```

**Verification: scratch-run.** The full assembled script (all code blocks from §§2–5 plus this entry point) was saved to a file and executed with `python3` directly, no interactive shell involved, producing the same two-step trace and final answer shown in §5 — confirming the pieces compose correctly as an ordinary script, not only when called interactively.

**验证方式：草稿运行。** 完整组装后的脚本（[第 2–5 节](#2-the-shape-of-a-decision)的全部代码加上这一入口点）被保存为文件，并直接以 `python3` 执行，未借助任何交互式命令行，产出的两步追踪与最终答案与第 5 节展示的完全一致——这确认了各部分作为一个普通脚本也能正确组合运行，而不仅仅是在交互调用时才成立。

---

## 9. What Changes With a Real LLM (and What Doesn't)

**换成真实 LLM 后，哪些会变，哪些不会**

It is worth being explicit about the line between what this module built and a production agent, since a reader who has only ever seen the stubbed version could otherwise mistake the stub for the whole story. Replacing `think`'s body with a real call to an LLM provider's API — sending the history as conversation messages, receiving back either ordinary text or a structured tool-call request — changes exactly one thing: how a `Decision` gets produced. It changes nothing about `run_agent_loop` itself, about `TOOLS`, about the `Decision` types, or about either guardrail in §§6–7, because none of that code ever looked inside `think` to see how its answer was reached — it only ever used the `Decision` that came back.

有必要明确指出本模块所构建的内容与生产级智能体之间的界线，否则只见过替身版本的读者可能会误把这一“替身”当作全部故事。把 `think` 的函数体替换为对某个 LLM 提供商 API 的真实调用——把历史记录作为对话消息发送出去，换回普通文本或一个结构化的工具调用请求——所改变的只有一件事：`Decision` 是如何产生的。它不会改变 `run_agent_loop` 本身，不会改变 `TOOLS`，不会改变 `Decision` 类型，也不会改变[第 6–7 节](#6-guarding-against-infinite-looping)中的任一道防护，因为这些代码从未窥探过 `think` 内部是如何得出答案的——它们始终只是使用 `think` 返回的那个 `Decision`。

This is the practical payoff of having given the "think" step a precise input/output contract (a `list` of history strings in, a `Decision` out) back in §2, rather than writing the LLM call and the loop logic as one tangled function: the boundary between "what decides" and "what executes the decision" is exactly where [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop §2](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#2-defining-agent-from-software-objects-to-ai-agents) drew it when it distinguished the LLM core from the surrounding harness, and keeping that boundary sharp in code, not just in prose, is what let this whole module study the loop's mechanics without ever touching a real API key.

这正是第 2 节为“思考”步骤给出精确的输入/输出契约（输入是历史字符串组成的 `list`，输出是一个 `Decision`）所带来的实际好处，而不是把 LLM 调用与循环逻辑纠缠成一个函数：“做决策的部分”与“执行决策的部分”之间的边界，正是[`introductory/03` — 什么是 AI 智能体？概念与智能体循环 第 2 节](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#2-defining-agent-from-software-objects-to-ai-agents)在区分 LLM 核心与周边运行框架时所划定的那条边界，而在代码中——而不仅仅是在文字中——保持这条边界的清晰，正是本模块得以在完全不接触任何真实 API 密钥的情况下，研究整个循环机制的原因所在。

The structured, provider-specific shape of a real tool-call request — what fields it has, how arguments are typed and validated, how multiple tool calls in one turn are handled — is exactly what the next module builds. [`practicum/02` — Implementing Tool Use & Function Calling](https://anu00.dev/curriculum/books/03-practicum/02-implementing-tool-use-and-function-calling.md) replaces the bare `if last_entry.startswith(...)` string-matching in `think` with a real tool registry, structured JSON parsing, and per-argument schema validation, building directly on the prerequisite this module shares: [`introductory/04` — Tool Use & Function Calling Basics](https://anu00.dev/curriculum/books/01-introductory/04-tool-use-and-function-calling-basics.md).

真实工具调用请求那种结构化的、与具体提供商相关的形态——它包含哪些字段、参数如何被赋予类型并加以校验、单轮中的多次工具调用如何处理——正是下一模块要构建的内容。[`practicum/02` — Implementing Tool Use & Function Calling](https://anu00.dev/curriculum/books/03-practicum/02-implementing-tool-use-and-function-calling.md)会把 `think` 中简陋的 `if last_entry.startswith(...)` 字符串匹配，替换为一个真正的工具注册表、结构化的 JSON 解析，以及逐参数的模式校验，并直接建立在本模块所共享的前置模块之上：[`introductory/04` — Tool Use & Function Calling Basics](https://anu00.dev/curriculum/books/01-introductory/04-tool-use-and-function-calling-basics.md)。

---

## 10. Summary and What's Next

**小结与后续内容**

This module took the agent loop [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md) described conceptually and built it as working Python: a `Decision` type representing what the "think" step can produce, a deterministic stub standing in for the LLM itself, one deterministic tool, a loop that wires perceive/think/act/observe together with a hard step limit, and validation of the proposed tool's name before it is ever run. Both guardrails were not just written but exercised — deliberately broken inputs were fed through the loop to confirm each one actually fires, not just that it looks correct on the page.

本模块把[`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md)在概念层面描述的智能体循环，构建成了可运行的 Python 代码：一个表示“思考”步骤可能产出内容的 `Decision` 类型、一个替代 LLM 本身的确定性替身、一个确定性工具、一个把感知/思考/行动/观察连接起来并附带硬性步数上限的循环，以及在真正运行之前对被提议工具名称的校验。这两道防护不仅被写了出来，更被实际演练过——刻意构造的错误输入被送入循环，以确认每一道防护确实会被触发，而不只是看起来正确。

The single hardest simplification in this module was the tool layer: one hardcoded tool, matched by simple string containment in a stub `think` function, validated only by name. [`practicum/02` — Implementing Tool Use & Function Calling](https://anu00.dev/curriculum/books/03-practicum/02-implementing-tool-use-and-function-calling.md) removes that simplification entirely, building a general tool registry, JSON-based structured tool-call parsing, and full schema validation directly on top of [`introductory/04` — Tool Use & Function Calling Basics](https://anu00.dev/curriculum/books/01-introductory/04-tool-use-and-function-calling-basics.md)'s function-calling contract — reusing this module's loop shape without needing to change it.

本模块中最主要的一处简化，在于工具层：一个硬编码的工具，靠替身 `think` 函数中简单的字符串包含匹配来触发，仅按名称进行校验。[`practicum/02` — Implementing Tool Use & Function Calling](https://anu00.dev/curriculum/books/03-practicum/02-implementing-tool-use-and-function-calling.md)将彻底移除这一简化，直接在[`introductory/04` — Tool Use & Function Calling Basics](https://anu00.dev/curriculum/books/01-introductory/04-tool-use-and-function-calling-basics.md)的函数调用契约之上，构建一个通用的工具注册表、基于 JSON 的结构化工具调用解析，以及完整的模式校验——并且无需改动本模块的循环结构即可复用它。

---

## References

**参考文献**

### External Sources

- [Python Software Foundation — `dataclasses` — Data Classes (Python 3 documentation)](https://docs.python.org/3/library/dataclasses.html)
- [Fowler, M. (2007) — "Mocks Aren't Stubs"](https://martinfowler.com/articles/mocksArentStubs.html)

### Internal Cross-References

- [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md)
- [`introductory/04` — Tool Use & Function Calling Basics](https://anu00.dev/curriculum/books/01-introductory/04-tool-use-and-function-calling-basics.md)
- [`introductory/06` — Context Windows, Tokens & Memory Basics](https://anu00.dev/curriculum/books/01-introductory/06-context-windows-tokens-and-memory-basics.md)
- [`practicum/02` — Implementing Tool Use & Function Calling](https://anu00.dev/curriculum/books/03-practicum/02-implementing-tool-use-and-function-calling.md)
