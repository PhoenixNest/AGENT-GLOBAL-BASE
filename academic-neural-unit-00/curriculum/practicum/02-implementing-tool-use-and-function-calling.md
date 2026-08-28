# Implementing Tool Use & Function Calling

**实现工具使用与函数调用**

| Field   | English                                                                 | 中文                                        |
| ------- | ----------------------------------------------------------------------- | ------------------------------------------- |
| Level   | Practicum                                                               | 实战                                        |
| Cluster | Hands-On Coding Practicum                                               | 动手编程实战                                |
| Author  | Dr. Kaito Fujimori, Research Scientist — Agent Systems Research, ANU-00 | ANU-00 智能体系统研究员 Kaito Fujimori 博士 |

---

## 1. From Contract to Code

**从契约到代码**

[`introductory/04`](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md) is the prerequisite for this module. It defined the three-part function-calling contract — a developer-written **schema**, the LLM's structured **call** proposing a tool and arguments, and the harness's execution of that call producing a **result** — and it walked through that contract by hand for a `multiply` tool and again for `get_weather`/`get_population`. This module does not re-teach that contract. Its job is to implement it: a general `Tool` type, a registry that can hold more than one tool, parsing of a raw structured request into something validated and typed, per-argument schema checking, and a dispatch step that runs a call and never crashes the harness — matching, piece by piece, the mechanics [`introductory/04` §§3–8](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#3-the-function-calling-contract-schema-call-result) described in prose.

[`introductory/04`](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md)是本模块的前置模块。它定义了函数调用的三方契约——由开发者编写的**模式**、LLM 提议某个工具及其参数的结构化**调用**，以及运行框架执行该调用所产出的**结果**——并针对一个 `multiply` 工具、以及 `get_weather`/`get_population` 分别手动演示了这一契约。本模块不会重新讲授这份契约，它的任务是把它实现出来：一个通用的 `Tool` 类型、一个能够容纳不止一个工具的注册表、把原始结构化请求解析为经过校验且带类型的对象、逐参数的模式检查，以及一个执行调用却绝不会使运行框架崩溃的分发步骤——逐一对应[`introductory/04` 第 3–8 节](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#3-the-function-calling-contract-schema-call-result)以文字描述的机制。

This module also builds directly on [`01`](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md), which implemented the agent loop itself around one hardcoded tool, validated only by name (its [§7](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#7-guarding-against-hallucinated-actions) said as much explicitly). Everything below replaces that one-tool, name-only setup with something general, while the loop's own shape — perceive, think, act, observe, bounded by a step limit — does not need to change at all; [§8](#8-putting-it-together-a-multi-tool-agent-loop) shows exactly how little of [`01`](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md)'s loop has to move.

本模块同样直接建立在[《01》](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md)之上——该模块围绕一个硬编码的工具实现了智能体循环本身，且仅按名称进行校验（其[第 7 节](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#7-guarding-against-hallucinated-actions)已明确指出这一点）。下文的全部内容，都是要把那种“单一工具、仅按名称校验”的设置，替换为通用的机制，而循环本身的结构——感知、思考、行动、观察，并以步数上限约束——完全不需要改变；[第 8 节](#8-putting-it-together-a-multi-tool-agent-loop)会具体展示，[《01》](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md)的循环需要变动的部分究竟有多小。

As with [`01`](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md), every code block below was actually executed against a Python 3 interpreter while writing this module, and the verification method stated next to each block records how.

与[《01》](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md)相同，撰写本模块时，下文的每一段代码都曾在 Python 3 解释器中实际执行过，每段代码旁标注的验证方式会记录具体做法。

---

## 2. A Tool as Data: The `Tool` Type

**作为数据的工具：`Tool` 类型**

[`introductory/04` §3](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#3-the-function-calling-contract-schema-call-result) described a tool's schema as carrying "its name, what it does in plain language, and the names and types of its arguments." A registry needs one more piece a schema alone does not carry: the real Python function to call once a request is validated. Bundling these four things — name, description, JSON-Schema-shaped parameters, and the callable itself — into one small dataclass (the same tool [`01` §2](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#2-the-shape-of-a-decision) used for `ToolCall`/`FinalAnswer`) is the first step.

[`introductory/04` 第 3 节](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#3-the-function-calling-contract-schema-call-result)将工具的模式描述为携带“其名称、用通俗语言表述的功能，以及其参数的名称与类型”。而一个注册表还需要一样模式本身并不携带的东西：一旦请求通过校验后，真正要调用的那个 Python 函数。把这四样东西——名称、描述、呈 JSON Schema 形态的参数定义，以及可调用对象本身——捆绑进一个小型的数据类（与[《01》第 2 节](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#2-the-shape-of-a-decision)用来表示 `ToolCall`/`FinalAnswer` 的手法相同），是第一步。

```python
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Tool:
    """One registered tool: its schema (name, description, parameters) plus the
    real Python callable the harness runs once a request against it validates."""
    name: str
    description: str
    parameters: dict  # JSON-Schema-shaped: {"type": "object", "properties": {...}, "required": [...]}
    fn: Callable[..., Any]
```

**Verification: scratch-run.** Constructed a `Tool` for a `get_weather`-shaped function (`Tool(name="get_weather", description="...", parameters={"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}, fn=get_weather)`) and confirmed `tool.fn("Tokyo")` calls through to the real function, returning its dict result unchanged.

**验证方式：草稿运行。** 为一个 `get_weather` 形态的函数构造了一个 `Tool`（`Tool(name="get_weather", description="...", parameters={"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}, fn=get_weather)`），并确认 `tool.fn("Tokyo")` 会正确调用到真实函数，且原样返回其字典结果。

The `parameters` field's shape — `{"type": "object", "properties": {...}, "required": [...]}` — is not an invention of this module. It is the same JSON Schema vocabulary [`introductory/04` §5](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#5-json-schema-basics-for-tool-definitions) already introduced for the `multiply` example, and it matches what the official JSON Schema documentation describes: `properties` as "an object, where each key is the name of a property and each value is a schema used to validate that property," and `required` as "an array of zero or more strings," each one naming a property that must be present. §5 below writes the code that actually checks arguments against this shape.

`parameters` 字段的形态——`{"type": "object", "properties": {...}, "required": [...]}`——并非本模块自行发明。它正是[`introductory/04` 第 5 节](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#5-json-schema-basics-for-tool-definitions)已经针对 `multiply` 示例介绍过的同一套 JSON Schema 词汇，也与官方 JSON Schema 文档的描述相符：`properties` 是“一个对象，其中每个键是某个属性的名称，每个值是用于校验该属性的一份模式”，而 `required` 则是“一份由零个或多个字符串组成的数组”，其中每个字符串都指明一个必须出现的属性。下文第 5 节会给出真正依照这一形态校验参数的代码。

---

## 3. A Tool Registry: A Place for Tools to Live

**工具注册表：工具的容身之所**

[`01` §4](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#4-the-one-tool-a-deterministic-weather-function) used a single-line dictionary, `TOOLS = {"get_weather": get_weather}`, to map a tool's name to its callable. A registry generalizes that dictionary into a small class with three responsibilities: accept new tools, look one up by name, and produce the list of schemas that would be handed to an LLM alongside the conversation — the "inclusion in the LLM's input" step [`introductory/04` §3](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#3-the-function-calling-contract-schema-call-result) named.

[《01》第 4 节](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#4-the-one-tool-a-deterministic-weather-function)用一行字典 `TOOLS = {"get_weather": get_weather}` 把工具名称映射到其可调用对象。注册表把这个字典泛化为一个承担三项职责的小类：接收新工具、按名称查找工具，以及产出应与对话一并交给 LLM 的模式列表——即[`introductory/04` 第 3 节](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#3-the-function-calling-contract-schema-call-result)所述的“纳入 LLM 输入”这一步骤。

```python
from typing import Optional


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def schemas(self) -> list:
        """The list handed to the LLM alongside the conversation -- the
        'inclusion in the LLM's input' step (introductory/04 SS3, step 2)."""
        return [
            {"name": t.name, "description": t.description, "parameters": t.parameters}
            for t in self._tools.values()
        ]
```

**Verification: scratch-run.** Registered two tools (`get_weather`, `get_population`) and called `.schemas()`; the result, printed via `json.dumps(..., indent=2)`, was a two-element list each shaped exactly like the `multiply` schema in [`introductory/04` §5](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#5-json-schema-basics-for-tool-definitions) (`name`, `description`, `parameters` with nested `properties`/`required`). Registering a duplicate name a second time raised `ValueError` as expected, and `.get("nonexistent")` returned `None` rather than raising.

**验证方式：草稿运行。** 注册了两个工具（`get_weather`、`get_population`）并调用 `.schemas()`；通过 `json.dumps(..., indent=2)` 打印出的结果，是一个包含两个元素的列表，其形态与[`introductory/04` 第 5 节](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#5-json-schema-basics-for-tool-definitions)中 `multiply` 的模式完全一致（`name`、`description`，以及带有嵌套 `properties`/`required` 的 `parameters`）。第二次注册同名工具时按预期抛出了 `ValueError`，而 `.get("nonexistent")` 返回 `None` 而非抛出异常。

Raising on a duplicate registration and returning `None` (rather than raising) on a missing lookup are both deliberate choices, not arbitrary ones: registering two tools under one name is a programming mistake the developer should hear about immediately, at registration time, while an LLM proposing a name that was never registered is an ordinary runtime event — the hallucinated-action failure mode [`introductory/03` §8](https://anu00.dev/curriculum/introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#8-common-failure-modes-of-the-agent-loop) named — that the dispatch step in §6 must handle gracefully, not treat as a program bug.

“重复注册时抛出异常”与“查找缺失时返回 `None`（而非抛出异常）”，都是刻意的选择，而非随意为之：以同一个名称注册两个工具，是开发者应当在注册那一刻就立即知晓的编程错误；而 LLM 提议一个从未注册过的名称，则是一次普通的运行时事件——正是[`introductory/03` 第 8 节](https://anu00.dev/curriculum/introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#8-common-failure-modes-of-the-agent-loop)所指出的幻觉行动失效模式——第 6 节中的分发步骤必须优雅地处理它，而不能将其当作程序缺陷对待。

---

## 4. Structured Tool-Call Parsing: From Raw Text to a Validated Request

**结构化工具调用解析：从原始文本到经过校验的请求**

[`introductory/04` §8](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#8-tool-use-across-providers-a-brief-comparison) showed that real providers hand back an already-parsed structure — OpenAI's Responses API returns an `output` array that can include an item with `"type": "function_call"`, and Claude's response "can include a `tool_use` content block." Whichever SDK is used, that structure ultimately arrives as data that was serialized somewhere along the way — most commonly JSON — and a harness has the same underlying obligation either way: turn text that came from outside the program's control into a validated, typed value before touching it. This module models that obligation directly by having `think` (§8) hand back raw JSON text, and writing the parser that turns it into a typed request.

[`introductory/04` 第 8 节](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#8-tool-use-across-providers-a-brief-comparison)已经展示过，真实的提供商会返回一个已经解析好的结构——OpenAI 的 Responses API 会返回一个 `output` 数组，其中可以包含一个 `"type": "function_call"` 的条目，Claude 的响应则“可以包含一个 `tool_use` 内容块”。无论使用哪种 SDK，这一结构最终都是以某种方式（最常见的是 JSON）序列化后传递过来的数据，而运行框架在这两种情况下都承担着同样的底层义务：在触碰任何来自程序控制范围之外的文本之前，先把它转化为经过校验、带类型的值。本模块通过让 `think`（第 8 节）返回原始 JSON 文本，来直接模拟这一义务，并编写把它转化为带类型请求的解析器。

Python's standard `json` module is the tool for the first half of that job. `json.loads` "deserialize[s] a str … containing a JSON document" into ordinary Python objects (dicts, lists, strings, numbers), and — critically for a harness that must never blindly trust its input — the documentation states it raises `json.JSONDecodeError` "when the data being deserialized is not a valid JSON document," rather than returning something silently wrong.

Python 标准库中的 `json` 模块承担了这项工作的前半部分。`json.loads` 会“将一段包含 JSON 文档的 str …… 反序列化”为普通的 Python 对象（字典、列表、字符串、数字），而对于一个绝不能盲目信任其输入的运行框架而言，至关重要的是——文档中指出，当“被反序列化的数据不是一份合法的 JSON 文档”时，它会抛出 `json.JSONDecodeError`，而不是悄无声息地返回某个错误的结果。

```python
import json
from dataclasses import dataclass


class ToolCallError(Exception):
    """Raised for any problem with a proposed tool call: malformed JSON, a
    missing 'name'/'arguments' field, an unknown tool, or a schema mismatch."""


@dataclass
class ToolCallRequest:
    name: str
    arguments: dict


def parse_tool_call(raw_llm_output: str) -> ToolCallRequest:
    """Parses a structured tool-call request out of raw text. Real providers
    hand back an already-parsed object (introductory/04 SS8); this function
    models the underlying obligation any harness has either way: turn
    untrusted text into a validated, typed request before touching it."""
    try:
        payload = json.loads(raw_llm_output)
    except json.JSONDecodeError as exc:
        raise ToolCallError(f"malformed tool-call JSON: {exc}") from exc
    if "name" not in payload or "arguments" not in payload:
        raise ToolCallError("tool-call JSON missing 'name' or 'arguments'")
    return ToolCallRequest(name=payload["name"], arguments=payload["arguments"])
```

**Verification: scratch-run.** `parse_tool_call('{"name": "get_weather", "arguments": {"city": "Tokyo"}}')` returned `ToolCallRequest(name='get_weather', arguments={'city': 'Tokyo'})`. Feeding it deliberately malformed JSON, `'{"name": "get_weather", "arguments": {city: "Tokyo"}}'` (an unquoted key, invalid JSON), raised `ToolCallError: malformed tool-call JSON: Expecting property name enclosed in double quotes: line 1 column 39 (char 38)` — the underlying `JSONDecodeError`'s message, re-raised through `ToolCallError` rather than propagating an uncaught exception type the rest of the harness doesn't know about.

**验证方式：草稿运行。** `parse_tool_call('{"name": "get_weather", "arguments": {"city": "Tokyo"}}')` 返回了 `ToolCallRequest(name='get_weather', arguments={'city': 'Tokyo'})`。刻意输入格式错误的 JSON，`'{"name": "get_weather", "arguments": {city: "Tokyo"}}'`（键未加引号，属于非法 JSON），抛出了 `ToolCallError: malformed tool-call JSON: Expecting property name enclosed in double quotes: line 1 column 39 (char 38)`——即底层 `JSONDecodeError` 的错误信息，通过 `ToolCallError` 重新抛出，而不是让运行框架其余部分接触到一个它并不认识的未捕获异常类型。

---

## 5. Validating Arguments Against a Schema

**依照模式校验参数**

A `ToolCallRequest` that parsed successfully is not yet safe to run — [`01` §7](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#7-guarding-against-hallucinated-actions) was explicit that checking only a tool's name "checks only that the tool's _name_ is known, not that its _arguments_ are well-formed or of the right type." This section writes the check that was missing there: walk the tool's `parameters` schema (§2) and confirm every `required` field is present and every supplied field has the declared JSON type.

一个成功解析出来的 `ToolCallRequest`，尚且还不能安全地运行——[《01》第 7 节](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#7-guarding-against-hallucinated-actions)已经明确指出，仅检查工具名称“只检查了工具的*名称*是否已知，并未检查其*参数*是否格式正确或类型是否恰当”。本节要编写的正是那里所缺失的检查：遍历工具的 `parameters` 模式（第 2 节），确认每一个 `required` 字段均已提供，且每一个已提供字段都符合所声明的 JSON 类型。

```python
_JSON_TYPE_CHECKS = {
    "string": lambda v: isinstance(v, str),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
}


def validate_arguments(schema: dict, arguments: dict) -> None:
    """Checks `arguments` against a JSON-Schema-shaped `parameters` block
    (introductory/04 SS5): every `required` field present, every supplied
    field's value matching its declared `type`. Raises ToolCallError on the
    first mismatch found; raises nothing if `arguments` is valid."""
    properties = schema.get("properties", {})
    required = schema.get("required", [])

    for field_name in required:
        if field_name not in arguments:
            raise ToolCallError(f"missing required argument: {field_name}")

    for field_name, value in arguments.items():
        if field_name not in properties:
            raise ToolCallError(f"unexpected argument: {field_name}")
        expected_type = properties[field_name].get("type")
        check = _JSON_TYPE_CHECKS.get(expected_type)
        if check is not None and not check(value):
            raise ToolCallError(
                f"argument '{field_name}' expected type '{expected_type}', "
                f"got {type(value).__name__}"
            )
```

**Verification: scratch-run.** Against `get_weather`'s schema (`{"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}`): `validate_arguments(schema, {"city": "Tokyo"})` returned normally (no exception); `validate_arguments(schema, {})` raised `ToolCallError: missing required argument: city`; `validate_arguments(schema, {"city": 42})` raised `ToolCallError: argument 'city' expected type 'string', got int` — confirming both the required-field check and the type check fire independently and correctly.

**验证方式：草稿运行。** 针对 `get_weather` 的模式（`{"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}`）：`validate_arguments(schema, {"city": "Tokyo"})` 正常返回（未抛出异常）；`validate_arguments(schema, {})` 抛出 `ToolCallError: missing required argument: city`；`validate_arguments(schema, {"city": 42})` 抛出 `ToolCallError: argument 'city' expected type 'string', got int`——确认了必填字段检查与类型检查均能独立且正确地触发。

Note the `isinstance(v, (int, float)) and not isinstance(v, bool)` guard for `"number"` and the analogous one for `"integer"`: in Python, `bool` is a subclass of `int`, so a bare `isinstance(True, int)` is `True` — without the extra `not isinstance(v, bool)` clause, a JSON `true`/`false` value would silently pass as a valid number or integer. This is a small, specific example of a broader lesson: writing a validator against another language's type system (JSON's) using a host language's own type-checking primitives (Python's `isinstance`) requires checking where the two disagree, not assuming they line up.

请注意针对 `"number"` 所加的 `isinstance(v, (int, float)) and not isinstance(v, bool)` 判断，以及针对 `"integer"` 的类似判断：在 Python 中，`bool` 是 `int` 的子类，因此单纯的 `isinstance(True, int)` 会返回 `True`——如果没有额外的 `not isinstance(v, bool)` 这一判断条件，一个 JSON 中的 `true`/`false` 值就会被悄悄当作合法的数字或整数而通过校验。这是一个具体而微的例子，说明了一个更普遍的道理：当使用宿主语言自身的类型检查原语（Python 的 `isinstance`）去校验另一种语言（JSON）的类型系统时，必须检查两者不一致的地方，而不能想当然地认为它们是对齐的。

---

## 6. The Dispatch Function: Executing One Call Safely

**分发函数：安全地执行一次调用**

[`introductory/04` §7](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#7-error-handling-when-tools-fail) stated the rule for what happens when something goes wrong: "the harness's job when a tool call fails is not to hide the failure from the LLM but to translate it into a clear, structured observation." `dispatch` is that translation, applied uniformly to every way a call can fail: unknown tool (§3), invalid arguments (§5), or the tool's own code raising an exception once it actually runs.

[`introductory/04` 第 7 节](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#7-error-handling-when-tools-fail)阐明了出错时应遵循的规则：“当工具调用失败时，运行框架的职责不是向 LLM 隐瞒失败，而是将其转化为清晰、结构化的观察”。`dispatch` 正是这一转化的体现，并统一应用于调用可能失败的每一种情形：未知工具（第 3 节）、参数无效（第 5 节），或工具自身的代码在真正运行时抛出异常。

```python
def dispatch(registry: ToolRegistry, request: ToolCallRequest) -> dict:
    """Executes one validated tool-call request and returns a structured
    observation -- {'result': ...} or {'error': ...} -- never raising, per
    introductory/04 SS7's error-handling rule."""
    tool = registry.get(request.name)
    if tool is None:
        return {"error": f"no such tool: {request.name}"}

    try:
        validate_arguments(tool.parameters, request.arguments)
    except ToolCallError as exc:
        return {"error": str(exc)}

    try:
        result = tool.fn(**request.arguments)
    except Exception as exc:  # the tool's own code failed; report, don't crash the harness
        return {"error": f"tool '{request.name}' raised: {exc}"}

    return {"result": result}
```

**Verification: scratch-run.** Six cases against a registry holding `get_weather`/`get_population` (the latter raising `ValueError` on an unknown city, standing in for a real tool's own internal failure): a valid call returned `{'result': {'condition': 'rain', 'temp_c': 19}}`; an unregistered tool name returned `{'error': 'no such tool: get_stock_price'}`; a missing required argument returned `{'error': 'missing required argument: city'}`; a wrong-typed argument returned `{'error': "argument 'city' expected type 'string', got int"}`; and a city the tool itself doesn't recognize returned `{'error': "tool 'get_weather' raised: city not found: Atlantis"}` — in every case a plain dict came back, and no exception ever escaped `dispatch`.

**验证方式：草稿运行。** 针对一个注册了 `get_weather`/`get_population` 的注册表（后者在遇到未知城市时会抛出 `ValueError`，用以模拟真实工具自身的内部失败）测试了六种情形：一次合法调用返回 `{'result': {'condition': 'rain', 'temp_c': 19}}`；一个未注册的工具名称返回 `{'error': 'no such tool: get_stock_price'}`；缺失必填参数返回 `{'error': 'missing required argument: city'}`；参数类型错误返回 `{'error': "argument 'city' expected type 'string', got int"}`；工具自身无法识别的城市返回 `{'error': "tool 'get_weather' raised: city not found: Atlantis"}`——每一种情形都返回了一个普通字典，从未有任何异常从 `dispatch` 中逃逸出去。

The `except Exception` clause deserves a second look, because catching a broad `Exception` is normally a code smell — it can hide bugs that should have crashed loudly during development. It is deliberate here for a specific reason: a tool registered by a third party can fail in ways its own author never anticipated (a network timeout, a permissions error, a bug), and `dispatch` cannot know that space of failures in advance. What makes this safe rather than a bug-hiding trick is that the exception's message is preserved and returned, never silently swallowed — exactly the distinction [`introductory/04` §7](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#7-error-handling-when-tools-fail) drew between translating a failure and hiding it.

`except Exception` 这一处值得再多看一眼，因为捕获宽泛的 `Exception` 通常被视为一种代码坏味道——它可能掩盖了本应在开发阶段就大声报错的缺陷。这里之所以刻意如此，是出于一个具体的理由：由第三方注册的工具，可能以其作者自己都未曾预料到的方式失败（网络超时、权限错误、代码缺陷等），而 `dispatch` 无法预先知晓这一整片可能的失败空间。使这种做法安全、而非沦为“掩盖缺陷的把戏”的关键在于：异常的信息被完整保留并返回，从未被悄悄吞掉——这正是[`introductory/04` 第 7 节](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#7-error-handling-when-tools-fail)在“转化失败”与“隐瞒失败”之间所划出的那条界线。

---

## 7. Parallel and Sequential Dispatch

**并行分发与顺序分发**

[`introductory/04` §6](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#6-parallel-and-sequential-tool-calls) distinguished a **parallel tool call**, where "the harness executes all three (typically concurrently, since they don't depend on each other)," from a **sequential tool call**, required "whenever a later call's arguments depend on an earlier call's result." `dispatch` (§6) already handles one call; `dispatch_all` extends it to a list, using the standard library's `concurrent.futures.ThreadPoolExecutor` — described in the official documentation as "an `Executor` subclass that uses a pool of threads to execute calls asynchronously" — to run independent calls concurrently rather than one after another.

[`introductory/04` 第 6 节](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#6-parallel-and-sequential-tool-calls)区分了**并行工具调用**——“运行框架会（由于三者互不依赖，通常并发地）执行全部三次调用”——与**顺序工具调用**，后者是“当后一次调用的参数依赖于前一次调用的结果时”所必需的。`dispatch`（第 6 节）已经能处理单次调用；`dispatch_all` 借助标准库中的 `concurrent.futures.ThreadPoolExecutor`——官方文档将其描述为“一个 `Executor` 子类，它使用一个线程池来异步执行调用”——把这一能力扩展到一份列表上，使互不依赖的调用能够并发执行，而不是逐一顺序执行。

```python
from concurrent.futures import ThreadPoolExecutor


def dispatch_all(registry: ToolRegistry, requests: list) -> list:
    """Executes multiple tool-call requests. Independent requests (the common
    case for a parallel tool call, introductory/04 SS6) can run concurrently
    since none of dispatch()'s side effects depend on another call's result."""
    if not requests:
        return []
    with ThreadPoolExecutor(max_workers=max(1, len(requests))) as pool:
        return list(pool.map(lambda r: dispatch(registry, r), requests))
```

**Verification: scratch-run.** `dispatch_all(registry, [get_weather("Tokyo"), get_weather("Osaka"), get_weather("Kyoto")])` (as three `ToolCallRequest`s) returned a three-element list of `{'result': {...}}` dicts, one per city, in the same order the requests were given — `Executor.map`'s documented behavior of returning results in input order, not completion order, is what makes this order guarantee hold even though the calls ran concurrently.

**验证方式：草稿运行。** `dispatch_all(registry, [针对 Tokyo、Osaka、Kyoto 的三个 get_weather ToolCallRequest])` 返回了一个由三个 `{'result': {...}}` 字典组成的列表，顺序与请求给出的顺序一致，对应各自城市——`Executor.map` 文档所述“按输入顺序而非完成顺序返回结果”的行为，正是即便各调用是并发执行的，这一顺序保证依然成立的原因。

Demonstrating the sequential case means constructing one where a later call genuinely needs an earlier one's result — exactly [`introductory/04` §6](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#6-parallel-and-sequential-tool-calls)'s own example: find whichever of three cities has the highest population, then check that city's weather.

要展示顺序调用的情形，需要构造一个后一次调用确实需要前一次调用结果的场景——正是[`introductory/04` 第 6 节](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#6-parallel-and-sequential-tool-calls)自身给出的例子：先在三座城市中找出人口最多的那座，再查询该城市的天气。

```python
# Step A (parallel: these three don't depend on each other):
pop_requests = [
    ToolCallRequest(name="get_population", arguments={"city": c})
    for c in ("Tokyo", "Osaka", "Kyoto")
]
pop_results = dispatch_all(registry, pop_requests)

# Step B (sequential: this call's argument depends on step A's results):
most_populous = max(pop_results, key=lambda r: r["result"]["population"])["result"]["city"]
weather_request = ToolCallRequest(name="get_weather", arguments={"city": most_populous})
weather_result = dispatch(registry, weather_request)
```

**Verification: scratch-run.** With the population figures used in this module's test data, `most_populous` resolved to `"Tokyo"`, and `weather_result` was `{'result': {'condition': 'rain', 'temp_c': 19}}` — confirming the second call's argument really was computed from the first three calls' results, and could not have been issued before they returned.

**验证方式：草稿运行。** 使用本模块测试数据中的人口数字，`most_populous` 解析为 `"Tokyo"`，`weather_result` 为 `{'result': {'condition': 'rain', 'temp_c': 19}}`——这确认了第二次调用的参数确实是根据前三次调用的结果计算得出的，且不可能在它们返回结果之前就发出。

Which of the two patterns a task needs is not something `dispatch_all` decides — [`introductory/04` §6](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#6-parallel-and-sequential-tool-calls) was explicit that this is "exactly the kind of decision the LLM's 'think' step is responsible for." `dispatch_all` only supplies the mechanism (run a given batch concurrently); §8 shows `think` making that batching decision.

任务需要这两种模式中的哪一种，并非由 `dispatch_all` 来决定——[`introductory/04` 第 6 节](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#6-parallel-and-sequential-tool-calls)已经明确指出，这“恰恰是 LLM‘思考’步骤逐任务负责的决策”。`dispatch_all` 只提供了机制本身（并发执行给定的一批调用）；第 8 节将展示 `think` 是如何做出这一分批决策的。

---

## 8. Putting It Together: A Multi-Tool Agent Loop

**整合：一个多工具智能体循环**

[`01` §5](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#5-the-loop-wiring-perceive-think-act-and-observe-together) built `run_agent_loop` around one hardcoded tool and a `think` function that matched history strings by hand. This section reuses that loop's shape — perceive, think, act, observe, bounded by `max_steps` — and replaces only the parts this module built a real version of: `think` now returns raw JSON text (the shape §4 parses), and the "act" step now goes through `dispatch_all` and the registry instead of a bare dictionary lookup.

[《01》第 5 节](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#5-the-loop-wiring-perceive-think-act-and-observe-together)围绕一个硬编码工具、以及一个手动匹配历史字符串的 `think` 函数，构建了 `run_agent_loop`。本节复用该循环的结构——感知、思考、行动、观察，并以 `max_steps` 加以约束——只替换本模块已经构建出真实版本的那些部分：`think` 现在返回原始 JSON 文本（即第 4 节所解析的形态），而“行动”步骤现在通过 `dispatch_all` 与注册表来完成，而不再是一次简单的字典查找。

```python
def think(history: list) -> str:
    """A deterministic stand-in for the LLM's 'think' step (same role as
    01 SS3's think(), now returning raw JSON -- the shape SS4's parser expects,
    and the shape a real provider's structured tool-call output takes,
    introductory/04 SS8)."""
    last_entry = history[-1]

    if last_entry.startswith("user_request:"):
        text = last_entry[len("user_request:"):].lower()
        if "compare" in text and "weather" in text:
            cities = [c for c in ("tokyo", "osaka", "kyoto") if c in text]
            calls = [{"name": "get_weather", "arguments": {"city": c.capitalize()}} for c in cities]
            return json.dumps({"calls": calls})  # a parallel batch: SS7
        return json.dumps({"calls": []})

    if last_entry.startswith("tool_results:"):
        results_text = last_entry[len("tool_results:"):]
        return json.dumps({"final_answer": f"Comparison complete: {results_text}"})

    return json.dumps({"final_answer": "I'm not sure how to proceed."})


def run_multi_tool_loop(user_request: str, max_steps: int = 5) -> str:
    history = [f"user_request:{user_request}"]  # Perceive (step 1)

    for step in range(1, max_steps + 1):
        raw_decision = think(history)  # Think
        decision = json.loads(raw_decision)

        if "final_answer" in decision:
            return decision["final_answer"]

        # Act: parse each proposed call, then dispatch the whole batch.
        requests = [
            ToolCallRequest(name=c["name"], arguments=c["arguments"])
            for c in decision["calls"]
        ]
        results = dispatch_all(registry, requests)
        print(f"Step {step}: dispatched {len(requests)} call(s) -> {results}")

        # Observe: the batch of results becomes the next observation.
        history.append(f"tool_results:{results}")

    raise RuntimeError(f"Agent did not reach a final answer within {max_steps} steps.")
```

**Verification: scratch-run.** `run_multi_tool_loop("Compare the weather in Tokyo and Osaka")` printed `Step 1: dispatched 2 call(s) -> [{'result': {'condition': 'rain', 'temp_c': 19}}, {'result': {'condition': 'sunny', 'temp_c': 24}}]` and returned `"Comparison complete: [{'result': {'condition': 'rain', 'temp_c': 19}}, {'result': {'condition': 'sunny', 'temp_c': 24}}]"` — the two-city comparison ran as a single parallel batch in step 1, and the loop terminated in exactly two `think` calls, mirroring [`introductory/03` §4](https://anu00.dev/curriculum/introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#4-worked-example-a-weather-checking-agent-traced-step-by-step)'s observation that "a harder question … would require the loop to run at least three times" only when the calls cannot be batched.

**验证方式：草稿运行。** `run_multi_tool_loop("Compare the weather in Tokyo and Osaka")` 打印出 `Step 1: dispatched 2 call(s) -> [{'result': {'condition': 'rain', 'temp_c': 19}}, {'result': {'condition': 'sunny', 'temp_c': 24}}]`，并返回 `"Comparison complete: [{'result': {'condition': 'rain', 'temp_c': 19}}, {'result': {'condition': 'sunny', 'temp_c': 24}}]"`——两座城市的比较在第一步中作为单次并行批处理完成，循环恰好经过两次 `think` 调用便告终止，与[`introductory/03` 第 4 节](https://anu00.dev/curriculum/introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md#4-worked-example-a-weather-checking-agent-traced-step-by-step)中“更难的问题……只有在调用无法被合并处理时，才需要循环至少运行三次”这一观察相印证。

Compare this loop's body to [`01`](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md)'s: the `for` loop, the `max_steps` bound, and the final `RuntimeError` are unchanged line for line. Only `think`'s return type (JSON text instead of a `Decision` object) and the "act" branch (a registry-backed batch dispatch instead of one dictionary lookup) are new — concrete evidence that [`01` §9](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#9-what-changes-with-a-real-llm-and-what-doesnt)'s claim about the loop's stability under a smarter "think" step holds for a smarter "act" step too.

把这个循环的主体与[《01》](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md)对照一下：`for` 循环、`max_steps` 约束，以及最终的 `RuntimeError`，逐行都未曾改变。真正新增的，只有 `think` 的返回类型（由 `Decision` 对象变为 JSON 文本）与“行动”分支（由一次字典查找变为基于注册表的批量分发）——这为[《01》第 9 节](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#9-what-changes-with-a-real-llm-and-what-doesnt)关于“循环在‘思考’步骤变得更智能时依然保持稳定”这一论断提供了具体的证据：这一论断对“行动”步骤变得更强大时同样成立。

---

## 9. Exercising the Failure Modes Once More

**再次演练失效模式**

[`01` §7](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#7-guarding-against-hallucinated-actions) exercised a hallucinated-tool-name guard that only checked membership. It is worth confirming, briefly, that this module's version — going through `parse_tool_call`, `validate_arguments`, and `dispatch` together — handles the same failure and the deeper ones [`01`](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md) admitted it could not catch: a malformed request, a missing argument, and a wrong-typed argument, none of which ever reach the real tool function.

[《01》第 7 节](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#7-guarding-against-hallucinated-actions)演练过的幻觉工具名称防护，当时只做了成员检查。这里值得简要确认一下：本模块的版本——把 `parse_tool_call`、`validate_arguments` 与 `dispatch` 结合在一起——不仅能处理同样的失效情形，也能处理[《01》](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md)当时坦承自己无法捕获的更深层问题：格式错误的请求、缺失的参数，以及类型错误的参数，这些都不会有机会触及真正的工具函数。

| Failure                     | Where it is caught                        | Observation returned                                          |
| --------------------------- | ----------------------------------------- | ------------------------------------------------------------- |
| Malformed JSON from `think` | `parse_tool_call` (§4)                    | `ToolCallError` raised before a `ToolCallRequest` ever exists |
| Hallucinated tool name      | `dispatch` → `registry.get` (§§3, 6)      | `{"error": "no such tool: ..."}`                              |
| Missing required argument   | `dispatch` → `validate_arguments` (§§5–6) | `{"error": "missing required argument: ..."}`                 |
| Wrong argument type         | `dispatch` → `validate_arguments` (§§5–6) | `{"error": "argument '...' expected type '...', got ..."}`    |
| Tool's own code raises      | `dispatch`'s second `try`/`except` (§6)   | `{"error": "tool '...' raised: ..."}`                         |

All five rows share the same shape [`introductory/04` §7](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#7-error-handling-when-tools-fail) required: a clear, structured observation the next "think" step can reason about, never a crash and never a silently wrong answer.

以上五行结果共享着[`introductory/04` 第 7 节](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#7-error-handling-when-tools-fail)所要求的同一种形态：一条清晰、结构化的观察，供下一次“思考”步骤据以推理，而绝非一次崩溃，也绝非一个悄无声息的错误答案。

**Verification: scratch-run.** Each row was independently produced during the development of §§4–6 above (see each section's own verification note for the exact input and output); this table is a summary cross-reference, not a new execution.

**验证方式：草稿运行。** 表格中的每一行结果，均在上文第 4–6 节的开发过程中被独立产出过（具体的输入与输出请见各节自身的验证说明）；本表只是一份汇总性的交叉引用，并非一次新的执行。

---

## 10. Summary and What's Next

**小结与后续内容**

This module implemented the function-calling contract [`introductory/04`](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md) described: a `Tool` type bundling schema and callable, a `ToolRegistry` that can hold any number of tools, a JSON-based parser that turns untrusted text into a validated `ToolCallRequest`, a schema validator that checks required fields and JSON types, a `dispatch` function that never lets a tool's own failure crash the harness, and a `dispatch_all` that runs independent calls concurrently while still supporting the sequential, dependency-driven case. All of it was then wired into the exact loop shape [`01`](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md) built, replacing only the parts that needed to grow.

本模块实现了[`introductory/04`](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md)所描述的函数调用契约：一个捆绑了模式与可调用对象的 `Tool` 类型、一个能够容纳任意数量工具的 `ToolRegistry`、一个把不可信文本转化为经过校验的 `ToolCallRequest` 的 JSON 解析器、一个检查必填字段与 JSON 类型的模式校验器、一个绝不会让工具自身的失败拖垮运行框架的 `dispatch` 函数，以及一个既能并发执行相互独立的调用、又仍然支持顺序的、依赖驱动情形的 `dispatch_all`。随后，所有这些都被接入了[《01》](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md)所构建的那个循环结构之中，只替换了确实需要扩展的部分。

Two simplifications remain, both intentional and both named so a reader does not mistake them for the full picture. First, `validate_arguments` checks only primitive JSON types, not the fuller JSON Schema vocabulary (nested objects, array item schemas, string patterns, numeric ranges) — enough to demonstrate the mechanism [`introductory/04` §5](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#5-json-schema-basics-for-tool-definitions) taught, not a production-grade validator. Second, `think` is still a deterministic stub, for the same reproducibility reason [`01` §3](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#3-a-deterministic-stand-in-for-the-think-step) gave; [`01` §9](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#9-what-changes-with-a-real-llm-and-what-doesnt)'s argument for why that stub can be swapped for a real LLM API call without touching anything else applies unchanged here. [`intermediate/03`](https://anu00.dev/curriculum/intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md) picks up from exactly this point, building the named, formal agent design patterns — ReAct, Plan-and-Execute, Reflexion — directly on top of the loop and tool-calling mechanics this module and its prerequisite established.

仍然保留了两处简化，二者都是刻意为之，且都在此明确指出，以免读者将其误认为全貌。第一，`validate_arguments` 只检查了基本的 JSON 类型，而未涵盖更完整的 JSON Schema 词汇（嵌套对象、数组元素模式、字符串模式、数值范围等）——足以演示[`introductory/04` 第 5 节](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md#5-json-schema-basics-for-tool-definitions)所讲授的机制，但并非一个生产级别的校验器。第二，`think` 仍然是一个确定性替身，原因与[《01》第 3 节](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#3-a-deterministic-stand-in-for-the-think-step)所述的可复现性理由相同；[《01》第 9 节](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md#9-what-changes-with-a-real-llm-and-what-doesnt)关于该替身可以在不触动其他任何部分的前提下替换为真实 LLM API 调用的论证，在这里同样成立、无需改动。[`intermediate/03`](https://anu00.dev/curriculum/intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md)将正好从这一点接续下去，直接在本模块与其前置模块所确立的循环与工具调用机制之上，构建具名的、正式的智能体设计模式——ReAct、Plan-and-Execute 与 Reflexion。

---

## References

**参考文献**

### External Sources

- [Python Software Foundation — `json` — JSON encoder and decoder (Python 3 documentation)](https://docs.python.org/3/library/json.html)
- [Python Software Foundation — `concurrent.futures` — Launching parallel tasks (Python 3 documentation)](https://docs.python.org/3/library/concurrent.futures.html)
- [JSON Schema — "object" (Understanding JSON Schema reference)](https://json-schema.org/understanding-json-schema/reference/object)
- [Anthropic — "Tool use with Claude" (Claude Platform Docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [OpenAI — "Function calling" (OpenAI API Guide)](https://developers.openai.com/api/docs/guides/function-calling)

### Internal Cross-References

- [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](https://anu00.dev/curriculum/introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md)
- [`introductory/04` — Tool Use & Function Calling Basics](https://anu00.dev/curriculum/introductory/04-tool-use-and-function-calling-basics.md)
- [`intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion](https://anu00.dev/curriculum/intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md)
- [`01` — Building a Basic Agent Loop](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md)
