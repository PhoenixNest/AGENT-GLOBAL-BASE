# Building an Agent Evaluation Harness

**构建智能体评估框架**

| Field   | English                                                       | 中文                                       |
| ------- | ------------------------------------------------------------- | ------------------------------------------ |
| Level   | Practicum                                                     | 实践                                       |
| Cluster | Hands-On Coding Practicum                                     | 动手编程实践                               |
| Author  | Dr. Mireille Dubois, Research Scientist — LLM Systems, ANU-00 | ANU-00 LLM 系统研究员 Mireille Dubois 博士 |

---

## 0. Where This Module Fits

**本模块的定位**

This module's explicit prerequisite is [`intermediate/08` — Evaluating Agent Systems: Benchmarks & Methodology](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md), per the curriculum's naming rule (`curriculum/README.md` §1). That module built the theory: what makes a benchmark rigorous ([`intermediate/08` §1](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#1-from-an-informal-test-set-to-a-formal-benchmark)), how success rate and the pass@k metric are defined ([`intermediate/08` §4](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#4-metrics-for-agent-evaluation-success-rate-and-passk)), and why a multi-agent system's performance is a distribution across repeated runs rather than a single number ([`intermediate/08` §7](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08)). This module does not re-derive any of that theory. It builds the smallest evaluation harness that actually implements it: a runner that executes a set of tasks against an agent, grades the results, and aggregates them into a report — in plain Python, using nothing beyond the standard library.

本模块的显式前置模块是[`intermediate/08`——评估智能体系统：基准测试与方法论](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md)，这是按照课程的命名规则（`curriculum/README.md` 第 1 节）所要求的。该模块搭建了理论基础：什么才使一个基准测试称得上严谨（见[`intermediate/08` 第 1 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#1-from-an-informal-test-set-to-a-formal-benchmark)）、成功率与 pass@k 指标是如何定义的（见[`intermediate/08` 第 4 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#4-metrics-for-agent-evaluation-success-rate-and-passk)），以及为什么一个多智能体系统的表现是重复运行所形成的一个分布，而非单一数字（见[`intermediate/08` 第 7 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08)）。本模块不会重新推导这些理论中的任何一项，而是构建一套最小可行、却真正实现了这些理论的评估框架：一个对一组任务运行智能体、为结果评分、并将结果汇总成报告的运行器——全部使用纯 Python 标准库完成。

Per `curriculum/practicum/README.md` §3, this document is teaching material that reads as code, not application code this repository executes: every exercise below lives entirely inside fenced code blocks in this markdown file, and no `.py` or `.ipynb` file is committed alongside it. Per §4 of that same file, every code block below states, immediately next to it, how its author verified it — mental trace, scratch-run, or cited test — before this module was filed.

按照 `curriculum/practicum/README.md` 第 3 节的规定，本文档是以代码形式呈现的教学材料，而非本仓库实际执行的应用代码：下文的每一段练习都完整地存在于本 markdown 文件内的围栏代码块中，本文件旁不会提交任何 `.py` 或 `.ipynb` 文件。按照同一文件第 4 节的规定，下文的每一个代码块紧邻处都注明了作者在归档本模块之前对其采用的验证方式——手动推演、暂存脚本试运行，或引用测试套件。

---

## 1. What This Module Builds: Scope of a Minimal Evaluation Harness

**本模块的构建目标：最小可行评估框架的范围**

An evaluation harness, in the sense this module builds, has four moving parts, and this section fixes what each one is responsible for before any code is written. A **task** is one unit of evaluation: a prompt to give the agent, plus a way to check whether the agent's output on that prompt counts as correct. A **task runner** executes a task against an agent — possibly more than once, since [`intermediate/08` §7](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08) already established that a single run can understate or overstate a system's real reliability. **Grading** turns one output into a pass/fail verdict (or, in the scored variant this module touches on but does not build in full, a numeric score). **Aggregation and reporting** turn many individual verdicts, across many tasks and many runs, into the kind of summary numbers [`intermediate/08` §4](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#4-metrics-for-agent-evaluation-success-rate-and-passk) defined — success rate and pass@k — plus a human-readable report.

本模块所构建的评估框架，含有四个活动部件，本节在编写任何代码之前，先确定每一部件各自的职责。**任务**是评估的一个基本单位：一段交给智能体的提示词，加上一种判定智能体在该提示词上的输出是否算作正确的方法。**任务运行器**负责针对某个智能体执行一项任务——而且可能不止执行一次，因为[`intermediate/08` 第 7 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08)已经指出，单次运行可能会低估或高估一个系统真实的可靠程度。**评分**把一次输出转化为一个通过/失败的判决（或者，在本模块只是略作提及、并未完整构建的评分制变体中，转化为一个数值分数）。**聚合与报告**把跨越多项任务、多次运行所得到的众多单次判决，汇总成[`intermediate/08` 第 4 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#4-metrics-for-agent-evaluation-success-rate-and-passk)所定义的那类汇总数字——成功率与 pass@k——外加一份人类可读的报告。

Deliberately out of scope: this harness does not build an agent — modules [`practicum/01`](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md) and [`practicum/02`](https://anu00.dev/curriculum/practicum/02-implementing-tool-use-and-function-calling.md) already cover the agent loop and tool use. Here, "the agent" is treated as a black box: any Python callable that accepts a prompt string and returns an output string. This keeps the harness fully general — it can grade a real LLM-backed agent exactly as it grades the small toy stand-ins this module uses to keep every example runnable without an API key.

刻意排除在范围之外的是：本评估框架并不构建智能体本身——[`practicum/01`](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md)与[`practicum/02`](https://anu00.dev/curriculum/practicum/02-implementing-tool-use-and-function-calling.md)两个模块已经分别讲解了智能体循环与工具使用。在本模块中，“智能体”被当作一个黑盒处理：任何接受一个提示词字符串、并返回一个输出字符串的 Python 可调用对象皆可。这使得该评估框架保持完全通用——它既能评分一个真正由大语言模型驱动的智能体，也能像评分本模块为了让每个示例无需 API 密钥即可运行、所使用的小型玩具替身那样对其评分，二者所用的方式完全一致。

---

## 2. Defining a Task: A Minimal, Extensible Record

**定义任务：一个最小、可扩展的记录结构**

The first building block is a record type for a single task, holding an identifier, the prompt to send the agent, and a check function that decides pass or fail from the agent's output. Python's `dataclasses` module, part of the standard library since Python 3.7, is the natural tool here: it generates the boilerplate `__init__` and `__repr__` methods for a class whose entire purpose is holding a fixed set of named fields, so the class body can state the fields once and nothing else.

第一个构建模块，是用于单个任务的记录类型，包含一个标识符、发送给智能体的提示词，以及一个根据智能体的输出判定通过或失败的检查函数。Python 标准库自 3.7 版本起内置的 `dataclasses` 模块，正是这里的天然工具：它能为一个整体用途仅仅是承载一组固定命名字段的类，自动生成样板化的 `__init__` 与 `__repr__` 方法，从而使类体只需声明一次这些字段，无需其他内容。

A second, matching record — `TaskResult` — holds the outcome of running one task once: which task it was, which trial (run index) this was, what the agent actually output, whether that output passed, and — via the optional `error` field defaulted to `None` — whether the trial ran to completion at all, populated by [§3](#3-the-task-runner-executing-an-agent-against-a-task-across-multiple-trials)'s fault-isolation handling rather than by anything in this section's own code. Keeping `Task` (the specification) and `TaskResult` (an observed outcome) as two separate types, rather than mutating one object in place, matters once trials repeat: each run produces its own immutable record, so nothing about run 1 can be silently overwritten by run 2.

第二个与之配套的记录类型——`TaskResult`——保存单次运行某项任务所得到的结果：这是哪项任务、这是第几次运行（运行编号）、智能体实际输出了什么、该输出是否通过，以及——通过默认值为 `None` 的可选字段 `error`——这一次运行是否完整地执行到底；该字段由[第 3 节](#3-the-task-runner-executing-an-agent-against-a-task-across-multiple-trials)的故障隔离处理逻辑填充，而非本节自身的代码。将 `Task`（任务规格）与 `TaskResult`（观测到的结果）保持为两种独立的类型，而不是就地修改同一个对象，这一点在运行需要重复多次时尤为重要：每次运行都会产生属于自己的、不可变的记录，因此运行一的结果不会被运行二悄无声息地覆盖。

```python
from dataclasses import dataclass
from typing import Callable, List, Optional


@dataclass
class Task:
    task_id: str
    prompt: str
    check: Callable[[str], bool]


@dataclass
class TaskResult:
    task_id: str
    trial: int
    output: str
    passed: bool
    error: Optional[str] = None
```

**Verification: mental trace.** Both classes are pure declarations — `@dataclass` mechanically derives `__init__` and `__repr__` from the annotated fields, exactly as documented for the module (see External Sources). There is no control flow, arithmetic, or branching to execute, so tracing the generated `__init__` signature by hand (`Task(task_id, prompt, check)`, `TaskResult(task_id, trial, output, passed, error=None)`) is sufficient to confirm correctness — a field with a default value is only required to appear after every field without one, which `error` already does as `TaskResult`'s last-declared field, so this generates a valid `__init__` with no reordering needed. This is confirmed by construction in the scratch-run of [§3](#3-the-task-runner-executing-an-agent-against-a-task-across-multiple-trials) below, where both classes are instantiated successfully.

**验证方式：手动推演。** 这两个类都只是纯粹的声明——`@dataclass` 会依据带注解的字段机械地推导出 `__init__` 与 `__repr__`，与该模块自身文档所述完全一致（见“外部来源”）。其中不含任何需要实际执行的控制流、算术运算或分支判断，因此仅需手动推演生成出的 `__init__` 签名（`Task(task_id, prompt, check)`、`TaskResult(task_id, trial, output, passed, error=None)`）便足以确认其正确性——带默认值的字段，只需出现在所有不带默认值的字段之后即可，而 `error` 本就是 `TaskResult` 中最后声明的字段，满足这一要求，因此生成的 `__init__` 有效，无需调整字段顺序。下文[第 3 节](#3-the-task-runner-executing-an-agent-against-a-task-across-multiple-trials)的暂存脚本试运行中，这两个类均被成功实例化，构成了对此的实际印证。

---

## 3. The Task Runner: Executing an Agent Against a Task, Across Multiple Trials

**任务运行器：针对一项任务、跨多次运行执行智能体**

`run_task` is the innermost loop: given one `Task`, an agent (any `Callable[[str], str]`), and a trial count, it calls the agent once per trial, grades each output with the task's own `check` function, and returns one `TaskResult` per trial rather than a single collapsed verdict. `run_benchmark` then does the obvious thing at the next level up — it runs every task in a list against the same agent and concatenates all the resulting `TaskResult` records into one flat list, which is the raw material every later section works from.

`run_task` 是最内层的循环：给定一项 `Task`、一个智能体（任意 `Callable[[str], str]`）与一个运行次数，它会针对每一次运行分别调用一次智能体，并用该任务自身的 `check` 函数为每次输出评分，返回的是每次运行各自的一条 `TaskResult`，而不是一个被合并为单一结果的判决。`run_benchmark` 则在更高一层做了显而易见的事情——它针对同一个智能体依次运行列表中的每一项任务，并将所得到的全部 `TaskResult` 记录拼接成一个扁平的列表，这份原始素材正是后文每一节所要处理的对象。

```python
def run_task(task: Task, agent: Callable[[str], str], trials: int = 3) -> List[TaskResult]:
    results = []
    for trial in range(trials):
        try:
            output = agent(task.prompt)
        except Exception as exc:  # the agent's own call failed; record, don't crash the run
            results.append(
                TaskResult(task.task_id, trial, "", False, error=f"agent raised: {exc}")
            )
            continue
        passed = task.check(output)
        results.append(TaskResult(task.task_id, trial, output, passed))
    return results


def run_benchmark(tasks: List[Task], agent: Callable[[str], str], trials: int = 3) -> List[TaskResult]:
    all_results: List[TaskResult] = []
    for task in tasks:
        all_results.extend(run_task(task, agent, trials))
    return all_results
```

A bare `output = agent(task.prompt)` with no error handling has a real production cost specific to this harness's own purpose: `agent`, per [§1](#1-what-this-module-builds-scope-of-a-minimal-evaluation-harness), is deliberately treated as a black box, which in practice usually means it is backed by a real, network-dependent LLM call — and a real LLM call can fail on any individual trial (a timeout, a rate limit, a malformed response) for reasons that have nothing to do with whether the agent is actually capable of the task. Without the `try`/`except` above, one such failure on trial 2 of 3 would raise out of `run_task`, propagate straight through `run_benchmark`'s loop over every remaining task, and abort the entire benchmark run — discarding every result already collected for every other task, not just the one flaky trial. The `try`/`except` isolates the failure to the one trial where it happened: it is caught, recorded as a `TaskResult` with `passed=False` and `error` set to a message naming what went wrong, and the loop moves on to the next trial. Recording it as `passed=False` rather than skipping it outright means an agent call that fails outright still counts against that task's `success_rate` and `pass_at_k` exactly as a wrong-but-returned answer would ([§6](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent)-[§7](#7-aggregation-part-2-applying-passk-in-code) need no changes to keep working correctly) — the non-`None` `error` field is what distinguishes "the agent answered and was graded wrong" from "the agent never produced an answer to grade," for any caller that wants to tell the two apart.

This is the same translate-don't-hide treatment [`practicum/02` §6](https://anu00.dev/curriculum/practicum/02-implementing-tool-use-and-function-calling.md#6-the-dispatch-function-executing-one-call-safely)'s `dispatch` gives a tool's own code raising mid-call, applied at the layer that actually needs it here: `dispatch` catches broad `Exception` around `tool.fn(**request.arguments)` — another caller-supplied black-box callable it cannot fully trust — and returns a structured `{"error": ...}` observation instead of letting the exception escape, specifically so a multi-step agent loop can keep running after one tool call fails. `run_task` is deliberately the same shape for the same reason: like `dispatch`, it wraps a black-box call it does not control and must not let a single failure escape from, rather than the shape [`practicum/04` §3/§7](https://anu00.dev/curriculum/practicum/04-building-a-minimal-rag-pipeline.md#3-step-2-embedding-chunks-with-a-real-sentence-encoder) uses for `embed()`/`generate()`, where a failed API call is wrapped in a named exception (`EmbeddingError`, `GenerationError`) and deliberately re-raised, because those functions are internal pipeline steps whose caller is expected to decide what a failure means, not a runner loop whose whole job is to keep going across many trials.

这也正是[《practicum/02》第 6 节](https://anu00.dev/curriculum/practicum/02-implementing-tool-use-and-function-calling.md#6-the-dispatch-function-executing-one-call-safely)中 `dispatch` 对工具自身代码在调用过程中抛出异常所采用的同一种“转化而非隐瞒”处理方式，只是应用在了这里真正需要它的那一层：`dispatch` 在 `tool.fn(**request.arguments)`——另一个由调用方提供、无法完全信任的黑盒可调用对象——外层捕获宽泛的 `Exception`，并返回一个结构化的 `{"error": ...}` 观察结果，而不是任由异常逃逸，其目的正是让一个多步骤的智能体循环能够在某一次工具调用失败后继续运行下去。`run_task` 之所以刻意采用同样的结构，也是出于同样的理由：与 `dispatch` 一样，它包装的是一个自己无法控制、且绝不能让单次失败从中逃逸的黑盒调用，而不是[《practicum/04》第 3/7 节](https://anu00.dev/curriculum/practicum/04-building-a-minimal-rag-pipeline.md#3-step-2-embedding-chunks-with-a-real-sentence-encoder)中 `embed()`/`generate()` 所采用的那种形态——在那里，失败的 API 调用被包装为一个具名异常（`EmbeddingError`、`GenerationError`）并被刻意重新抛出，因为那两个函数是流水线内部的处理步骤，理应由其调用方来决定一次失败究竟意味着什么，而不是像运行器循环那样，其全部职责就是在多次运行中持续推进下去。

The default of `trials = 3` is a deliberate, explicit choice rather than an arbitrary one: [`intermediate/08` §7](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08) names "somewhere between 3 and 10 repetitions" as the common range for repeated-run evaluation, and 3 is the low end of that range — cheap enough to run in every worked example in this module, while still being enough repetitions to expose a flaky task, as [§6](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent) below demonstrates concretely.

`trials = 3` 这一默认值，是经过深思熟虑的明确选择，而非随意设定：[`intermediate/08` 第 7 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08)将“3 到 10 次之间”列为重复运行评估的常见区间，而 3 正是该区间的下限——足够低廉，可以在本模块的每一个实例演练中运行，但又足以暴露出某项任务的不稳定性，正如下文[第 6 节](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent)将具体展示的那样。

**Verification: scratch-run.** Both functions were executed directly against a trivial one-task, one-trial benchmark with a fixed-string toy agent (`lambda prompt: "42"`) during authoring; the returned list contained exactly one `TaskResult` with `trial=0` and the expected `passed` value, confirming the loop bounds and field assignment are correct. The fault-isolation `try`/`except` was verified the same way with a second toy agent that unconditionally raises (`lambda prompt: (_ for _ in ()).throw(RuntimeError("simulated flaky call"))`) run against a two-trial task: `run_task` returned two `TaskResult` records, each with `passed=False`, `output=""`, and `error="agent raised: simulated flaky call"`, and — critically — the call returned normally rather than propagating the `RuntimeError`, confirming the loop continues past a failing trial instead of aborting. A further scratch-run of `run_benchmark` against two tasks, where the toy agent raised only on the first task's trials and answered normally on the second task's, confirmed the second task's results were still collected in full despite the first task's every trial failing — the exact whole-run-survives-one-flaky-task property this fix exists to guarantee. The fuller scratch-run against the five-task benchmark defined in [§5](#5-two-toy-agents-to-exercise-the-harness) below reproduces the non-failing path at scale and is quoted in full there.

**验证方式：暂存脚本试运行。** 撰写本模块期间，曾针对一个仅含一项任务、一次运行的最简基准测试，配合一个固定返回字符串的玩具智能体（`lambda prompt: "42"`），直接执行了以上两个函数；返回的列表中恰好包含一条 `trial=0`、`passed` 取值符合预期的 `TaskResult` 记录，从而确认了循环边界与字段赋值均正确无误。故障隔离用的 `try`/`except` 也以同样的方式核验过：使用第二个无条件抛出异常的玩具智能体（`lambda prompt: (_ for _ in ()).throw(RuntimeError("simulated flaky call"))`），针对一项两次运行的任务执行 `run_task`，返回了两条 `TaskResult` 记录，均为 `passed=False`、`output=""`、`error="agent raised: simulated flaky call"`——关键在于，此次调用正常返回，而非任由 `RuntimeError` 向外传播，这确认了循环会在某次运行失败后继续推进，而不会中止。此外，还对 `run_benchmark` 做了进一步的暂存脚本试运行：针对两项任务，令玩具智能体仅在第一项任务的各次运行中抛出异常、而在第二项任务的各次运行中正常作答，结果确认第二项任务的结果依然被完整收集，尽管第一项任务的每一次运行均已失败——这正是本项修复所要保证的“单个不稳定任务不影响整个运行”这一特性。下文[第 5 节](#5-two-toy-agents-to-exercise-the-harness)针对五项任务构成的基准测试所进行的更完整暂存脚本试运行，在更大规模上重现了未失败路径下的这一结果，并将其输出完整转录于该节之中。

---

## 4. Grading: Pass-Fail Checks and the Boundary With Scored Grading

**评分：通过/失败检查及其与评分制的边界**

`intermediate/08` §4 established the pass/fail versus scored distinction: the design here keeps grading deliberately simple by making `check` a plain `Callable[[str], bool]` stored directly on the `Task` — an ordinary Python function (or `lambda`) that inspects the agent's output string and returns `True` or `False`. This is exact-match-style grading in the sense [`introductory/08` §5](https://anu00.dev/curriculum/introductory/08-why-and-how-we-evaluate-agents.md#5-automated-grading-exact-match-and-the-newer-idea-of-llm-as-judge) first introduced, generalized slightly: the check function can do more than literal string equality (it can normalize whitespace or case, as several checks in [§5](#5-two-toy-agents-to-exercise-the-harness) below do), but it must still return a deterministic, binary verdict.

`intermediate/08` 第 4 节已经确立了通过/失败与评分制这一区分：此处的设计刻意让评分保持简洁，做法是把 `check` 定义为一个直接存放在 `Task` 上的普通 `Callable[[str], bool]`——一个检查智能体输出字符串、并返回 `True` 或 `False` 的普通 Python 函数（或 `lambda`）。这属于[`introductory/08` 第 5 节](https://anu00.dev/curriculum/introductory/08-why-and-how-we-evaluate-agents.md#5-automated-grading-exact-match-and-the-newer-idea-of-llm-as-judge)最先引入的精确匹配式评分，只是略作推广：检查函数所做的可以不止是字面字符串相等比较（例如可以对空白字符或大小写作归一化处理，正如下文[第 5 节](#5-two-toy-agents-to-exercise-the-harness)中的若干检查函数所做的那样），但它仍必须返回一个确定性的二元判决。

This is a deliberate scope boundary, not an oversight: `TaskResult.passed` is a plain `bool`, and this harness does not implement scored (partial-credit) grading or LLM-as-judge grading in full. Building either would mean replacing `check: Callable[[str], bool]` with a `score: Callable[[str], float]`, and — for LLM-as-judge specifically — implementing the position-swap and self-enhancement-avoidance safeguards [`intermediate/08` §5](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#5-llm-as-judge-methodology-in-full-prompting-bias-and-calibration) already covers in full; the extension point exists (swap the field type, swap the aggregation in [§8](#8-reporting-turning-results-into-a-readable-summary)), but building it out is left as a direct exercise for the reader rather than duplicated here.

这是一个刻意划定的范围边界，而非疏漏：`TaskResult.passed` 只是一个普通的 `bool` 值，本评估框架并未完整实现评分制（部分给分）评分或 LLM 评判式评分。若要构建其中任何一种，都意味着将 `check: Callable[[str], bool]` 替换为 `score: Callable[[str], float]`，而对于 LLM 评判而言，还需实现[`intermediate/08` 第 5 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#5-llm-as-judge-methodology-in-full-prompting-bias-and-calibration)已经完整讲解过的位置互换与规避自我偏好等防护措施；这一扩展点确实存在（替换字段类型、替换[第 8 节](#8-reporting-turning-results-into-a-readable-summary)中的聚合方式），但将其构建完整留作读者的直接练习，此处不再重复实现。

---

## 5. Two Toy Agents to Exercise the Harness

**两个用于驱动评估框架运行的玩具智能体**

To exercise the harness without depending on a real LLM API, this module defines a small benchmark of five tasks and one configurable toy agent. The benchmark covers arithmetic, string manipulation, and a yes/no question, each graded by exact match after light normalization:

为了在不依赖真实大语言模型 API 的情况下驱动本评估框架运行，本模块定义了一个包含五项任务的小型基准测试，以及一个可配置的玩具智能体。该基准测试涵盖算术运算、字符串操作与一道是非问题，每项任务均在轻度归一化处理后按精确匹配评分：

```python
TASKS = [
    Task("add", "What is 6 + 7?", lambda o: o.strip() == "13"),
    Task("multiply", "What is 9 * 8?", lambda o: o.strip() == "72"),
    Task("upper", "Uppercase the word 'harness'.", lambda o: o.strip() == "HARNESS"),
    Task("reverse", "Reverse the string 'agent'.", lambda o: o.strip() == "tnega"),
    Task("palindrome", "Is 'level' a palindrome? Answer yes or no.", lambda o: o.strip().lower() == "yes"),
]
```

The toy agent is not a fixed-answer stub — it is built by `make_flaky_agent`, a function that returns a closure over a seeded `random.Random` instance and a per-task success probability. On each call, it draws one random number and returns the correct answer if that draw falls under the task's configured probability, or a fixed wrong answer ("I don't know") otherwise. Every task is configured to succeed with probability 1.0 except `"reverse"`, deliberately set to 0.34 — an agent that is reliable at arithmetic and case conversion but unreliable at string reversal, chosen specifically to make [§6](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent) below produce a genuinely mixed result rather than an all-pass or all-fail benchmark, which would teach nothing about repeated trials.

这个玩具智能体并不是一个固定答案的桩程序——它由 `make_flaky_agent` 构建而成，这是一个返回闭包的函数，该闭包封装了一个带种子的 `random.Random` 实例，以及针对每项任务各自设定的成功概率。每次被调用时，它都会抽取一个随机数，若该随机数落在该任务所配置的概率范围之内，则返回正确答案，否则返回一个固定的错误答案（“I don't know”）。除 `"reverse"` 之外，每项任务的成功概率均配置为 1.0，唯独 `"reverse"` 被刻意设定为 0.34——这是一个在算术运算与大小写转换上可靠、却在字符串反转上不可靠的智能体，之所以如此选择，正是为了让下文[第 6 节](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent)产生一个真正意义上有输有赢的结果，而非一个全通过或全失败、对理解重复运行毫无教益的基准测试。

```python
import random

CORRECT_ANSWERS = {
    "What is 6 + 7?": "13",
    "What is 9 * 8?": "72",
    "Uppercase the word 'harness'.": "HARNESS",
    "Reverse the string 'agent'.": "tnega",
    "Is 'level' a palindrome? Answer yes or no.": "yes",
}

SUCCESS_PROB = {
    "What is 6 + 7?": 1.0,
    "What is 9 * 8?": 1.0,
    "Uppercase the word 'harness'.": 1.0,
    "Reverse the string 'agent'.": 0.34,
    "Is 'level' a palindrome? Answer yes or no.": 1.0,
}


def make_flaky_agent(seed: int = 7) -> Callable[[str], str]:
    rng = random.Random(seed)

    def agent(prompt: str) -> str:
        if rng.random() < SUCCESS_PROB.get(prompt, 0.9):
            return CORRECT_ANSWERS[prompt]
        return "I don't know"

    return agent
```

Fixing the seed (`random.Random(seed)` rather than the unseeded, process-global `random` module) is not a cosmetic choice: it is what makes this module's specific reported numbers in [§6](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent) through [§9](#9-assembling-and-running-the-full-harness) reproducible by any reader who copies this code, rather than different on every run — the same reproducibility requirement [`intermediate/08` §1](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#1-from-an-informal-test-set-to-a-formal-benchmark) named as a property of a rigorous benchmark's protocol, applied here to a harness's own test scaffolding.

固定随机种子（使用 `random.Random(seed)`，而非未设种子、进程全局共享的 `random` 模块）并非一种表面装饰性的选择：正是它使得下文从[第 6 节](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent)到[第 9 节](#9-assembling-and-running-the-full-harness)所报告的具体数字，能够被任何复制此代码的读者复现，而不会每次运行都得到不同的结果——这正是[`intermediate/08` 第 1 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#1-from-an-informal-test-set-to-a-formal-benchmark)所指出的严谨基准测试评测协议应当具备的可复现性，此处将其应用到了评估框架自身的测试脚手架上。

**Verification: scratch-run.** `TASKS`, `CORRECT_ANSWERS`, `SUCCESS_PROB`, and `make_flaky_agent` were executed together with `run_benchmark` from [§3](#3-the-task-runner-executing-an-agent-against-a-task-across-multiple-trials) during authoring, using `seed=7` and `trials=3`. Printing only the three `"reverse"` results produced:

**验证方式：暂存脚本试运行。** 撰写本模块期间，曾使用 `seed=7` 与 `trials=3`，将 `TASKS`、`CORRECT_ANSWERS`、`SUCCESS_PROB` 与 `make_flaky_agent` 一并同[第 3 节](#3-the-task-runner-executing-an-agent-against-a-task-across-multiple-trials)中的 `run_benchmark` 一起执行。仅打印其中三条 `"reverse"` 结果，输出如下：

```text
TaskResult(task_id='reverse', trial=0, output="I don't know", passed=False)
TaskResult(task_id='reverse', trial=1, output='tnega', passed=True)
TaskResult(task_id='reverse', trial=2, output='tnega', passed=True)
```

which is exactly the mixed pass/fail pattern §5's design intended, and is used directly in [§6](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent) below.

这正是第 5 节设计之初所期望产生的、有通过有失败的混合模式，下文[第 6 节](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent)将直接使用这一结果。

---

## 6. Aggregation, Part 1: Success Rate and Why a Single Run Understates a Flaky Agent

**聚合，第一部分：成功率，以及为何单次运行会低估一个不稳定的智能体**

`success_rate` computes the simplest aggregate metric [`intermediate/08` §4](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#4-metrics-for-agent-evaluation-success-rate-and-passk) defined: for one task, the fraction of its recorded trials that passed. It filters the flat `TaskResult` list down to one task's results and divides passes by the total count, using `statistics.mean` for the harness's later, list-wide averages — the standard-library function documented to "return the sample arithmetic mean" of a sequence of numbers.

`success_rate` 计算的是[`intermediate/08` 第 4 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#4-metrics-for-agent-evaluation-success-rate-and-passk)所定义的最简单聚合指标：对于单项任务而言，其记录的各次运行中通过的比例。该函数将扁平的 `TaskResult` 列表过滤到某一项任务的结果上，再用通过次数除以总次数；而对于评估框架后续跨列表的平均值计算，则使用 `statistics.mean`——这是标准库中记录在案、用于“返回一组数字样本算术平均值”的函数。

```python
import statistics

def success_rate(results: List[TaskResult], task_id: str) -> float:
    task_results = [r for r in results if r.task_id == task_id]
    passes = sum(1 for r in task_results if r.passed)
    return passes / len(task_results)
```

Applying this to the `"reverse"` trials quoted in [§5](#5-two-toy-agents-to-exercise-the-harness) — one failure, two passes — gives `success_rate = 2 / 3 ≈ 0.67`. This is precisely the scenario [`intermediate/08` §8](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#8-worked-example-an-evaluation-harness-for-the-coderreviewer-system) constructed by hand for its Coder/Reviewer worked example: reporting the single most recent run (`trial=2`, a pass) would have hidden an inconsistency that three repeated runs, aggregated with `success_rate`, reveal directly. Nothing about this task's _specification_ changed between the three trials — only the agent's own reliability did — which is exactly why [`intermediate/08` §7](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08) treats a system's performance as a distribution, not a point value.

将其应用于[第 5 节](#5-two-toy-agents-to-exercise-the-harness)中转录的三次 `"reverse"` 运行结果——一次失败、两次通过——得到 `success_rate = 2 / 3 ≈ 0.67`。这恰恰正是[`intermediate/08` 第 8 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#8-worked-example-an-evaluation-harness-for-the-coderreviewer-system)在其编码/审查双智能体实例演练中手工构造出的那种情形：如果只报告最近一次运行的结果（`trial=2`，通过），本会掩盖一处不一致，而三次重复运行经 `success_rate` 汇总后，则将其直接揭示了出来。三次运行之间，这项任务的*规格说明*本身并无任何变化——发生变化的只是智能体自身的可靠程度——这正是[`intermediate/08` 第 7 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08)之所以将系统表现视为一个分布、而非单一数值的原因所在。

**Verification: scratch-run.** `success_rate(results, "reverse")` was computed directly against the three-trial result list from [§5](#5-two-toy-agents-to-exercise-the-harness) during authoring and returned `0.6666666666666666`, matching the hand-computed `2 / 3`.

**验证方式：暂存脚本试运行。** 撰写本模块期间，曾直接对[第 5 节](#5-two-toy-agents-to-exercise-the-harness)中三次运行的结果列表计算 `success_rate(results, "reverse")`，返回值为 `0.6666666666666666`，与手工计算所得的 `2 / 3` 相符。

---

## 7. Aggregation, Part 2: Applying pass@k in Code

**聚合，第二部分：在代码中实现 pass@k 指标**

`success_rate` treats every trial as an independent report; pass@k, defined by Mark Chen and colleagues in their 2021 Codex paper (see External Sources) and formalized in [`intermediate/08` §4](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#4-metrics-for-agent-evaluation-success-rate-and-passk), instead asks a different question: given `n` independent trials of which `c` passed, what is the probability that _at least one_ of `k` trials drawn from those `n` would have passed? Chen et al.'s unbiased estimator, reproduced in [`intermediate/08` §4](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#4-metrics-for-agent-evaluation-success-rate-and-passk), is

`success_rate` 把每一次运行都当作一份独立报告来处理；而由 Mark Chen 及其合作者在其 2021 年 Codex 论文（见“外部来源”）中定义、并在[`intermediate/08` 第 4 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#4-metrics-for-agent-evaluation-success-rate-and-passk)中形式化的 pass@k 指标，问的却是另一个不同的问题：给定 `n` 次独立运行中有 `c` 次通过，那么从这 `n` 次运行中抽取 `k` 次，*至少有一次*通过的概率是多少？Chen 等人给出的无偏估计量，已在[`intermediate/08` 第 4 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#4-metrics-for-agent-evaluation-success-rate-and-passk)中转录，为

$$\text{pass@}k := \mathbb{E}\left[1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}\right]$$

**Why this is the unbiased estimator, not the "obvious" alternative.** [`intermediate/08` §4](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#4-metrics-for-agent-evaluation-success-rate-and-passk) already named the naive alternative in passing — "naively estimating this by generating exactly `k` samples and checking whether any succeeded is a biased, high-variance estimator" — without deriving why; this module builds and runs the code, so it is worth making that "why" concrete before translating the formula above into `pass_at_k`. In closed form, that naive approach is the substitution $1 - (1 - c/n)^k$: take the observed pass rate $c/n$ as though it were the agent's true, known success probability, then treat each of the `k` draws as an independent Bernoulli trial at that rate — mathematically identical to resampling `k` outcomes _with replacement_ from an infinite population whose success rate happens to equal $c/n$, which is exactly what generating `k` fresh samples and checking for any pass computes in expectation.

**为何这才是无偏估计量，而非那个“显而易见”的替代方案。** [`intermediate/08` 第 4 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#4-metrics-for-agent-evaluation-success-rate-and-passk)已经顺带点出过朴素替代方案的存在——“若朴素地通过恰好生成 `k` 个样本、检查是否有任一成功来估计这一概率……这种估计是有偏且高方差的”——但并未推导其原因；本模块要动手编写并运行代码，因此在把上面的公式翻译成 `pass_at_k` 之前，有必要把这个“为什么”讲清楚。写成闭式表达式，那种朴素做法正是替换式 $1 - (1 - c/n)^k$：把观测到的通过率 $c/n$ 当作智能体真实的、已知的成功概率，再把 `k` 次抽取的每一次都当作以该概率进行的一次独立伯努利试验——这在数学上等价于从一个成功率恰好为 $c/n$ 的无限总体中*有放回地*重新抽取 `k` 个结果，而这恰恰正是“生成 `k` 个全新样本、检查是否有任一通过”这一做法在期望意义上所计算的量。

The problem is what that computation implicitly assumes: that `n` is large enough, or the population it is drawn from infinite enough, for resampling at rate `c/n` to behave like drawing `k` genuinely fresh, independent trials. What the harness actually has is the opposite of that — a small, fixed set of `n` already-observed trials (`n = 3` by default, per [§3](#3-the-task-runner-executing-an-agent-against-a-task-across-multiple-trials)), and `c/n` is itself only a point estimate of the agent's true success probability, not that probability itself. Treating it as exact and resampling from it with replacement throws away the fact that pass@k, as defined above, asks about drawing `k` of those same `n` observed trials _without_ replacement — once one of the `n` trials has been "used" within a single draw, that specific outcome cannot recur within that same draw. The correct question is therefore a small, finite combinatorics problem, not a resampling problem: of the $\binom{n}{k}$ equally likely ways to choose `k` of the `n` observed trials, how many contain zero passes? Exactly $\binom{n-c}{k}$ do — every way of filling all `k` chosen slots from the `n - c` trials that failed — so the probability of drawing an all-failing subset is $\binom{n-c}{k} / \binom{n}{k}$, and pass@k, the probability of the complementary event (at least one pass), is exactly Chen et al.'s formula above. This is the hypergeometric distribution's $P(X = 0)$ for drawing without replacement from a finite population of `n` items containing `c` successes — not the binomial distribution's $P(X = 0)$ that the naive with-replacement framing implicitly computes instead.

问题在于这一计算暗中假设了什么：它假设 `n` 足够大、或者抽取所依托的总体足够趋近于无限，以至于按 `c/n` 这一概率重新抽样，其表现会近似于抽取 `k` 次真正全新、相互独立的试验。而评估框架实际拥有的情形恰恰相反——一小批固定的、已经观测到的 `n` 次运行（按[第 3 节](#3-the-task-runner-executing-an-agent-against-a-task-across-multiple-trials)所述，默认 `n = 3`），而 `c/n` 本身也仅仅是对智能体真实成功概率的一个点估计，而非该概率本身。把它当作确切值、并从中有放回地重新抽样，恰恰丢弃了这样一个事实：如上文所定义，pass@k 所问的是从这同一批 `n` 次观测结果中*无放回地*抽取 `k` 次——一旦 `n` 次运行中的某一次已经在某次抽取中被“使用”过，那个具体结果便不可能在同一次抽取中再次出现。因此，正确的问题其实是一个规模很小的有限组合数学问题，而非一个重新抽样的问题：在从 `n` 次观测结果中选出 `k` 次、共有 $\binom{n}{k}$ 种等可能取法之中，有多少种取法完全不含任何一次通过？恰好有 $\binom{n-c}{k}$ 种——即把全部 `k` 个被选中的位置，都从 `n - c` 次失败的运行中填满的每一种取法——因此抽出一个全部失败的子集的概率为 $\binom{n-c}{k} / \binom{n}{k}$，而 pass@k，也就是其互补事件（至少一次通过）的概率，便恰好等于上文 Chen 等人给出的那个公式。这是超几何分布中、从含有 `c` 次成功、共 `n` 个元素的有限总体中无放回抽取所得的 $P(X = 0)$——而非朴素的有放回框架所暗中计算的那个二项分布的 $P(X = 0)$。

A small worked example makes the gap concrete. Take `n = 5` observed trials with `c = 2` passes, and ask for pass@3. The naive formula gives `1 - (1 - 2/5)**3 = 1 - 0.6**3 = 1 - 0.216 = 0.784`. The correct formula gives `1 - comb(3, 3) / comb(5, 3) = 1 - 1/10 = 0.9` — nearly 12 percentage points higher, because with only `3` failing trials among the `5` observed and `k = 3` draws, there is exactly one way to draw all three failures without replacement (`comb(3, 3) = 1`) out of ten equally likely size-3 subsets (`comb(5, 3) = 10`), whereas the naive with-replacement framing treats each of the 3 draws as independently able to redraw the same `0.6` failure probability, overstating the chance of an all-failing draw at `0.6**3 = 0.216`. The two estimators converge as `n` grows large relative to `k` — sampling without replacement and sampling with replacement become indistinguishable once the population dwarfs the draw size — which is exactly why the brute-force cross-check described later in this section enumerates actual subsets of the actually-observed `n` trials via `itertools.combinations`, rather than resampling from a plug-in probability.

一个小型的实例演算能让这一差距变得具体可感。取 `n = 5` 次观测运行，其中 `c = 2` 次通过，求 pass@3。朴素公式给出 `1 - (1 - 2/5)**3 = 1 - 0.6**3 = 1 - 0.216 = 0.784`。正确公式给出 `1 - comb(3, 3) / comb(5, 3) = 1 - 1/10 = 0.9`——高出近 12 个百分点，原因在于：在 `5` 次观测中仅有 `3` 次失败、且抽取次数 `k = 3` 的情况下，在全部十种等可能的大小为 3 的子集（`comb(5, 3) = 10`）之中，恰好只有一种取法能够无放回地抽出全部三次失败（`comb(3, 3) = 1`）；而朴素的有放回框架则把这三次抽取中的每一次，都视为能够独立地再次抽中同一个 `0.6` 的失败概率，从而把全部抽中失败的概率高估为 `0.6**3 = 0.216`。当 `n` 相对于 `k` 变得足够大时，两种估计量会趋于一致——一旦总体规模远远超过抽取规模，有放回抽样与无放回抽样便会变得难以区分——这正是本节稍后所述的暴力交叉验证，之所以借助 `itertools.combinations` 逐一枚举实际观测到的 `n` 次运行中的真实子集、而非从某个代入估计值的概率重新抽样的原因所在。

Translating this directly into code needs exactly one standard-library function: `math.comb(n, k)`, which computes the binomial coefficient $\binom{n}{k}$ ("n choose k") without the numerical overflow risk of computing factorials separately. `pass_at_k` implements the formula for one task's `(n, c)` pair; `aggregate_pass_at_k` then averages it, again with `statistics.mean`, across every task in the benchmark, mirroring how `intermediate/08` §4 already noted the same `n` samples can be reused to estimate pass@k for several different values of `k` without re-running the agent.

将其直接翻译为代码，恰好只需要一个标准库函数：`math.comb(n, k)`，用于计算二项式系数 $\binom{n}{k}$（“n 选 k”），且不必像分别计算阶乘那样承担数值溢出的风险。`pass_at_k` 针对单项任务的 `(n, c)` 数对实现了该公式；`aggregate_pass_at_k` 随后再次借助 `statistics.mean`，对基准测试中的每一项任务求平均——这正呼应了 `intermediate/08` 第 4 节已经指出的一点：同一批 `n` 个样本，可以被复用来估计多个不同 `k` 值所对应的 pass@k，而无需重新运行智能体。

```python
from math import comb

def pass_at_k(n: int, c: int, k: int) -> float:
    if n - c < k:
        return 1.0
    return 1.0 - comb(n - c, k) / comb(n, k)


def aggregate_pass_at_k(results: List[TaskResult], task_ids: List[str], k: int) -> float:
    vals = []
    for tid in task_ids:
        task_results = [r for r in results if r.task_id == tid]
        n = len(task_results)
        c = sum(1 for r in task_results if r.passed)
        vals.append(pass_at_k(n, c, k))
    return statistics.mean(vals)
```

The `if n - c < k: return 1.0` guard handles the case where there are fewer failing samples than `k`, meaning it is impossible to draw `k` samples that are all failures — so at least one of any `k`-sized draw must pass with certainty, and $\binom{n-c}{k}$ would otherwise be computed with `k` larger than `n - c`, which `math.comb` correctly defines as zero but which is worth handling explicitly for clarity.

其中 `if n - c < k: return 1.0` 这一防护条件，处理的是失败样本数少于 `k` 的情形——此时不可能抽出 `k` 个全部为失败样本，因此任意一次 `k` 大小的抽取都必然至少有一次通过；否则便需要在 `k` 大于 `n - c` 的情况下计算 $\binom{n-c}{k}$，`math.comb` 虽会正确地将其定义为零，但为了清晰起见，仍值得显式地加以处理。

**Verification: cited test.** `pass_at_k` was checked against a five-case `pytest` suite before this module was filed: that `pass@1` equals plain `c / n`, that `pass@k` is `1.0` when every sample passed, `0.0` when none passed, that it is non-decreasing in `k`, and — most rigorously — that its output matches a brute-force calculation which literally enumerates every size-`k` subset of `n` labeled samples via `itertools.combinations` and counts the fraction containing at least one pass. Per pytest's own documentation (see External Sources), a plain `assert` statement inside a function named `test_*` is all a pytest test requires. Running `pytest test_pass_at_k.py -v` produced:

**验证方式：引用测试套件。** 在归档本模块之前，`pass_at_k` 已通过一套包含五个用例的 `pytest` 测试套件核验：验证 `pass@1` 等于普通的 `c / n`、验证全部样本通过时 `pass@k` 等于 `1.0`、全部失败时等于 `0.0`、验证其关于 `k` 单调不减，以及——最为严格的一项——验证其输出与一种暴力计算方法的结果相符，该暴力方法借助 `itertools.combinations` 逐一枚举 `n` 个带标签样本中所有大小为 `k` 的子集，并统计其中至少含一次通过的子集所占比例。按照 pytest 自身文档的说法（见“外部来源”），一个名为 `test_*` 的函数内含一条普通的 `assert` 语句，即是一个 pytest 测试所需的全部条件。运行 `pytest test_pass_at_k.py -v` 得到：

```text
test_pass_at_k.py::test_pass_at_k_equals_success_rate_when_k_equals_1 PASSED
test_pass_at_k.py::test_pass_at_k_is_one_when_all_samples_pass PASSED
test_pass_at_k.py::test_pass_at_k_is_zero_when_no_samples_pass PASSED
test_pass_at_k.py::test_pass_at_k_increases_with_k PASSED
test_pass_at_k.py::test_pass_at_k_matches_brute_force_expectation PASSED

======================== 5 passed in 0.01s ========================
```

Applied to the five-task benchmark from [§5](#5-two-toy-agents-to-exercise-the-harness) (`n = 3` trials per task throughout), `aggregate_pass_at_k` gives `pass@1 ≈ 0.93` — close to, but not identical to, the mean of the five per-task success rates, since `pass@1` and plain success rate coincide exactly only at `k = 1` (as the first pytest case above confirms) — and `pass@3 = 1.0`: given all three trials to draw from, every one of the five tasks has at least one passing trial, including `"reverse"`, whose single-run success rate of `2 / 3` would otherwise look far less reliable than pass@3 shows it to be when the agent is allowed its full trial budget.

将其应用于[第 5 节](#5-two-toy-agents-to-exercise-the-harness)中的五项任务基准测试（全程每项任务均为 `n = 3` 次运行），`aggregate_pass_at_k` 得到 `pass@1 ≈ 0.93`——这一数值与五项任务各自成功率的平均值相近、但并不完全相同，因为只有在 `k = 1` 时，pass@1 才与普通成功率恰好重合（如上文第一个 pytest 用例所核实的那样）——而 `pass@3 = 1.0`：如果可以从全部三次运行中抽取，那么五项任务中的每一项都至少有一次运行通过，包括 `"reverse"` 在内；若只看单次运行，该任务 `2 / 3` 的成功率看起来会远不如在给予智能体完整运行预算后、pass@3 所呈现出的可靠程度。

---

## 8. Reporting: Turning Results Into a Readable Summary

**报告：将结果转化为可读的摘要**

The last piece is a plain-text `report` function that ties [§6](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent) and [§7](#7-aggregation-part-2-applying-passk-in-code) together: a per-task line showing that task's `success_rate` and raw pass count, an overall mean success rate across all tasks, and the aggregate pass@1 figure, all in one function a reader can call after any benchmark run.

最后一部分，是一个把[第 6 节](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent)与[第 7 节](#7-aggregation-part-2-applying-passk-in-code)串联起来的纯文本 `report` 函数：逐行显示每项任务各自的 `success_rate` 与原始通过次数，再给出所有任务的整体平均成功率，以及 pass@1 的聚合数值，全部集中在一个函数中，读者在任意一次基准测试运行之后都可以直接调用它。

```python
def report(results: List[TaskResult], tasks: List[Task]) -> str:
    lines = []
    for task in tasks:
        rate = success_rate(results, task.task_id)
        n = len([r for r in results if r.task_id == task.task_id])
        c = sum(1 for r in results if r.task_id == task.task_id and r.passed)
        lines.append(f"{task.task_id:12s} success_rate={rate:.2f}  ({c}/{n})")
    overall = statistics.mean([success_rate(results, t.task_id) for t in tasks])
    lines.append(f"{'overall':12s} mean_success_rate={overall:.2f}")
    p1 = aggregate_pass_at_k(results, [t.task_id for t in tasks], k=1)
    lines.append(f"{'pass@1':12s} aggregate={p1:.2f}")
    return "\n".join(lines)
```

`report` deliberately returns a string rather than printing directly — the same separation-of-concerns reason a well-designed `check` function in [§4](#4-grading-pass-fail-checks-and-the-boundary-with-scored-grading) only decides pass/fail rather than also printing its own verdict: a function that returns data can be written to a file, compared in a test, or displayed in a different format later, while a function that only prints cannot.

`report` 刻意选择返回一个字符串，而不是直接打印——这与[第 4 节](#4-grading-pass-fail-checks-and-the-boundary-with-scored-grading)中一个设计良好的 `check` 函数只负责判定通过/失败、而不顺带打印自身判决的理由，出于同样的关注点分离考量：一个返回数据的函数，之后既可以被写入文件，也可以在测试中被比对，还可以以不同格式呈现，而一个只负责打印的函数则做不到这些。

**Macro-average, not micro-average — and why the difference stays invisible in this module's own numbers.** The `overall` line above computes a **macro-average**: it takes the five already-computed per-task `success_rate` values and calls `statistics.mean` directly on those five numbers, giving every task equal weight in the average regardless of how many trials contributed to it. The alternative — a **micro-average** — would instead pool every individual trial across every task first and divide the total pass count by the total trial count: `sum(1 for r in results if r.passed) / len(results)`. The two are mathematically identical only when every task contributes the same number of trials to `results`, which is exactly this module's situation (`trials=3` for all five tasks in [§9](#9-assembling-and-running-the-full-harness)) — that uniformity is precisely why the `0.93` `report()` prints matches what a micro-average of the same fifteen results would also give, and why the gap between the two never becomes visible anywhere in this module's own worked example.

They diverge as soon as different tasks run different numbers of trials — a routine situation once a harness lets trial counts vary per task, for instance because an easy, cheap task can afford far more repeated runs than a slow or expensive one. Suppose a two-task benchmark ran an easy task 10 times, all 10 passing, and a hard task twice, with 0 passes. The macro-average is `(10/10 + 0/2) / 2 = 0.50`: the hard task's `0%` and the easy task's `100%` are weighted as equal halves of the average, regardless of how many trials backed each figure. The micro-average is `(10 + 0) / (10 + 2) ≈ 0.83`: dominated by the easy task's larger trial count, since every individual trial counts equally rather than every task. Neither figure is wrong — they answer different questions ("how do tasks perform on average, weighted equally by task?" versus "what fraction of all attempts, across every task, succeed?") — but reporting one without naming which is being computed, as an unlabeled `report()` would, lets a reader silently assume the other.

**宏平均，而非微平均——以及为何这一差异在本模块自身的数字中始终不可见。** 上方 `overall` 这一行计算的是**宏平均**：它直接对五项任务各自已经算好的 `success_rate` 数值调用 `statistics.mean`，无论各项任务背后各贡献了多少次运行，在求平均时都给予每项任务同等的权重。另一种做法——**微平均**——则会先将所有任务的每一次运行汇总到一起，再用总通过次数除以总运行次数：`sum(1 for r in results if r.passed) / len(results)`。只有当每项任务为 `results` 贡献的运行次数完全相同时，二者在数学上才会完全相等——而这恰好正是本模块当下的情形（[第 9 节](#9-assembling-and-running-the-full-harness)中全部五项任务均为 `trials=3`）——正是这种一致性，使得 `report()` 打印出的 `0.93`，与对这同样十五条结果计算微平均所得到的结果恰好相符，也正因如此，二者之间的差异才始终未曾在本模块自身的实例演练中显现出来。

一旦不同任务运行的次数不再相同，二者便会出现分歧——一旦评估框架允许各任务的运行次数各不相同，这便是一种常见情形，例如一项廉价的简单任务负担得起远多于一项缓慢或昂贵任务的重复运行次数。设想一个包含两项任务的基准测试：一项简单任务运行了 10 次，全部通过；一项困难任务运行了 2 次，全部未通过。宏平均为 `(10/10 + 0/2) / 2 = 0.50`——困难任务的 `0%` 与简单任务的 `100%` 被当作平均值中权重相等的两半，而不论各自背后各有多少次运行作为支撑。微平均则为 `(10 + 0) / (10 + 2) ≈ 0.83`——被简单任务更大的运行次数所主导，因为此时是每一次单独运行获得同等权重，而非每一项任务。二者都没有错——它们回答的是两个不同的问题（“各项任务平均而言、且以任务为单位等权重表现如何”，与“在所有任务的全部尝试中，成功的比例是多少”）——但如果只报告其中一个数字、却不注明所计算的究竟是哪一个（就像一个不加标注的 `report()` 那样），便会使读者悄无声息地误以为得到的是另一个。

**Verification: scratch-run.** `report` was executed against the full five-task, `trials=3`, `seed=7` benchmark during authoring; its output is quoted in full in [§9](#9-assembling-and-running-the-full-harness) below, where it is reproduced as part of the complete, assembled script.

**验证方式：暂存脚本试运行。** 撰写本模块期间，`report` 已针对完整的五项任务、`trials=3`、`seed=7` 的基准测试执行过；其输出在下文[第 9 节](#9-assembling-and-running-the-full-harness)中完整转录，作为完整组装脚本的一部分予以呈现。

---

## 9. Assembling and Running the Full Harness

**组装并运行完整的评估框架**

Every piece from [§2](#2-defining-a-task-a-minimal-extensible-record) through [§8](#8-reporting-turning-results-into-a-readable-summary) assembles into one script with no further code: the two record types, the runner, the five-task benchmark and flaky toy agent, the two aggregation functions, and the report function. Running it end to end is the harness's whole reason for existing — one call each to build the agent, run the benchmark, and print the report.

从[第 2 节](#2-defining-a-task-a-minimal-extensible-record)到[第 8 节](#8-reporting-turning-results-into-a-readable-summary)的每一部分，组装起来即构成一个无需再添加任何代码的完整脚本：两种记录类型、运行器、五项任务的基准测试与不稳定的玩具智能体、两个聚合函数，以及报告函数。端到端地运行它，正是这套评估框架存在的全部意义所在——依次调用一次构建智能体、一次运行基准测试、一次打印报告即可。

```python
if __name__ == "__main__":
    agent = make_flaky_agent(seed=7)
    results = run_benchmark(TASKS, agent, trials=3)
    print(report(results, TASKS))
```

**Verification: scratch-run.** The complete script — every code block in [§2](#2-defining-a-task-a-minimal-extensible-record) through this section, concatenated in order — was executed directly (`python3 harness.py`) during authoring. It produced:

**验证方式：暂存脚本试运行。** 完整脚本——即[第 2 节](#2-defining-a-task-a-minimal-extensible-record)至本节的每一个代码块按顺序拼接而成的整体——已在撰写期间直接执行（`python3 harness.py`）。输出如下：

```text
add          success_rate=1.00  (3/3)
multiply     success_rate=1.00  (3/3)
upper        success_rate=1.00  (3/3)
reverse      success_rate=0.67  (2/3)
palindrome   success_rate=1.00  (3/3)
overall      mean_success_rate=0.93
pass@1       aggregate=0.93
```

Four of the five tasks report a perfect `1.00`; `"reverse"` reports exactly the `0.67` derived by hand in [§6](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent); the overall mean success rate and the aggregate pass@1 both round to `0.93`, consistent with [§7](#7-aggregation-part-2-applying-passk-in-code)'s more precise `≈0.933`. A reader who copies every code block above in order, with `seed=7` unchanged, should reproduce this output exactly — the same reproducibility property [§5](#5-two-toy-agents-to-exercise-the-harness) fixed the seed to guarantee.

五项任务中有四项报告出满分 `1.00`；`"reverse"` 所报告的 `0.67`，正与[第 6 节](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent)中手工推导出的结果完全一致；整体平均成功率与 pass@1 聚合值均四舍五入为 `0.93`，这与[第 7 节](#7-aggregation-part-2-applying-passk-in-code)中更精确的 `≈0.933` 相吻合。任何读者若按顺序复制以上每一个代码块、且不改动 `seed=7`，理应能够精确复现这一输出——这正是[第 5 节](#5-two-toy-agents-to-exercise-the-harness)固定随机种子所要保证的那种可复现性。

---

## 10. Common Pitfalls When Building Your Own Harness

**构建自己的评估框架时的常见陷阱**

Three pitfalls recur specifically at the implementation level, beyond the methodological ones [`intermediate/08` §9](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#9-common-methodological-pitfalls-at-this-level) already named (Goodhart's law and leaderboard chasing, which apply unchanged once this harness's numbers start driving a real decision).

除了[`intermediate/08` 第 9 节](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md#9-common-methodological-pitfalls-at-this-level)已经指出的方法论层面的陷阱（古德哈特定律与追逐排行榜，一旦本评估框架所输出的数字开始驱动真实决策，这两者便会原封不动地适用）之外，还有三种陷阱是在实现层面特有的、反复出现的问题。

| Pitfall                                      | EN                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 中文                                                                                                                                                                                                                                                                                                                                                                                     |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Unseeded randomness**                      | building a toy agent (or a real agent-testing setup) with an unseeded random source makes every run's numbers different, defeating reproducibility — [§5](#5-two-toy-agents-to-exercise-the-harness)'s seeded `random.Random(seed)` is the fix, not an optional nicety.                                                                                                                                                                                      | 使用未设种子的随机源来构建玩具智能体（或真实的智能体测试环境），会使每次运行得到的数字都不相同，从而破坏可复现性——[第 5 节](#5-two-toy-agents-to-exercise-the-harness)中带种子的 `random.Random(seed)` 正是解决方案，而非可有可无的锦上添花。                                                                                                                                            |
| **Trials collapsed to one number too early** | overwriting `TaskResult` in place instead of appending, or averaging inside `run_task` instead of keeping the raw per-trial records, throws away exactly the information `success_rate` and `pass_at_k` in [§6](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent)–[§7](#7-aggregation-part-2-applying-passk-in-code) need — aggregate at the reporting layer, never inside the runner.                                      | 就地覆盖 `TaskResult` 而非不断追加，或是在 `run_task` 内部就直接取平均、而不保留各次运行的原始记录，恰恰会丢弃[第 6 节](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent)与[第 7 节](#7-aggregation-part-2-applying-passk-in-code)中 `success_rate` 与 `pass_at_k` 所需要的信息——聚合应当在报告层完成，绝不能在运行器内部就提前完成。                   |
| **Check functions too strict or too loose**  | a `check` that compares output with no normalization at all fails a correct answer over trivial formatting differences (trailing whitespace, case); a `check` that normalizes too aggressively (e.g. stripping all non-alphanumeric characters) can pass a wrong answer by accident — [§5](#5-two-toy-agents-to-exercise-the-harness)'s `.strip()` and `.lower()` calls are the minimum needed for this benchmark's specific tasks, not a universal default. | 一个完全不做任何归一化处理就直接比较输出的 `check`，会因为琐碎的格式差异（尾随空白、大小写）而判定一个正确答案为失败；而一个归一化处理过于激进的 `check`（例如剥离所有非字母数字字符），则可能意外地将一个错误答案判定为通过——[第 5 节](#5-two-toy-agents-to-exercise-the-harness)中的 `.strip()` 与 `.lower()` 调用，只是本基准测试特定任务所需的最低限度处理，而非普遍适用的默认做法。 |

---

## 11. Summary and What's Next

**小结与后续内容**

This module built a complete, minimal evaluation harness in plain Python: a `Task`/`TaskResult` record pair ([§2](#2-defining-a-task-a-minimal-extensible-record)), a runner that executes an agent against a benchmark across multiple trials ([§3](#3-the-task-runner-executing-an-agent-against-a-task-across-multiple-trials)), pass/fail grading via a plain `Callable[[str], bool]` ([§4](#4-grading-pass-fail-checks-and-the-boundary-with-scored-grading)), two aggregation functions implementing [`intermediate/08`](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md)'s success rate and pass@k ([§6](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent)–[§7](#7-aggregation-part-2-applying-passk-in-code)), and a plain-text reporting function ([§8](#8-reporting-turning-results-into-a-readable-summary)) — around 110 lines of code in total, across every fenced code block from [§2](#2-defining-a-task-a-minimal-extensible-record) through [§9](#9-assembling-and-running-the-full-harness), none of it beyond the Python standard library.

本模块用纯 Python 构建了一套完整、最小可行的评估框架：一对 `Task`/`TaskResult` 记录类型（[第 2 节](#2-defining-a-task-a-minimal-extensible-record)）、一个能够针对基准测试跨多次运行执行智能体的运行器（[第 3 节](#3-the-task-runner-executing-an-agent-against-a-task-across-multiple-trials)）、经由普通 `Callable[[str], bool]` 实现的通过/失败评分（[第 4 节](#4-grading-pass-fail-checks-and-the-boundary-with-scored-grading)）、实现了[`intermediate/08`](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md)所述成功率与 pass@k 的两个聚合函数（[第 6](#6-aggregation-part-1-success-rate-and-why-a-single-run-understates-a-flaky-agent)–[7 节](#7-aggregation-part-2-applying-passk-in-code)），以及一个纯文本报告函数（[第 8 节](#8-reporting-turning-results-into-a-readable-summary)）——从[第 2 节](#2-defining-a-task-a-minimal-extensible-record)到[第 9 节](#9-assembling-and-running-the-full-harness)的每一个围栏代码块合计约 110 行代码，且完全没有超出 Python 标准库的范围。

Every reported number in this module traces back to one fixed, seeded scratch-run, and the harness's most statistically delicate piece — the `pass_at_k` estimator — was additionally checked against a five-case `pytest` suite, including a brute-force combinatorial cross-check, before this module was filed. What this module deliberately left as an extension point — scored grading, LLM-as-judge grading with its bias safeguards, and the statistical rigor of confidence intervals and significance testing around success rate and pass@k — is exactly what [`advanced/08` — Rigorous Agent Evaluation: Statistical Methodology](https://anu00.dev/curriculum/advanced/08-rigorous-agent-evaluation-statistical-methodology.md) develops in full; a reader who wants to extend this harness with a confidence interval around its `0.93` overall success rate should look there next.

本模块中报告的每一个数字，都可追溯至一次固定、带种子的暂存脚本试运行；而评估框架中统计学意义上最为精细的部分——`pass_at_k` 估计量——在本模块归档之前，还另外经过了一套包含五个用例的 `pytest` 测试套件的核验，其中包括一次暴力组合枚举式的交叉验证。本模块刻意留作扩展点、未予实现的部分——评分制评分、带有偏差防护措施的 LLM 评判式评分，以及围绕成功率与 pass@k 的置信区间与显著性检验等统计学严谨性——恰恰正是[`advanced/08`——严谨的智能体评估：统计方法论](https://anu00.dev/curriculum/advanced/08-rigorous-agent-evaluation-statistical-methodology.md)所要完整展开的内容；若有读者希望为本评估框架所报告的 `0.93` 整体成功率构建一个置信区间，下一步理应参阅该模块。

---

## References

**参考文献**

### External Sources

- [Chen, M. et al. (2021) — "Evaluating Large Language Models Trained on Code" (Codex / HumanEval / pass@k)](https://arxiv.org/abs/2107.03374)
- [pytest documentation — "Full pytest documentation"](https://docs.pytest.org/en/stable/)
- [Python documentation — `statistics` module (`mean`, `stdev`)](https://docs.python.org/3/library/statistics.html)
- [Python documentation — `dataclasses` module](https://docs.python.org/3/library/dataclasses.html)

### Internal Cross-References

- [`introductory/08` — Why & How We Evaluate Agents](https://anu00.dev/curriculum/introductory/08-why-and-how-we-evaluate-agents.md)
- [`intermediate/08` — Evaluating Agent Systems: Benchmarks & Methodology](https://anu00.dev/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md)
- [`advanced/08` — Rigorous Agent Evaluation: Statistical Methodology](https://anu00.dev/curriculum/advanced/08-rigorous-agent-evaluation-statistical-methodology.md)
- [`practicum/01` — Building a Basic Agent Loop](https://anu00.dev/curriculum/practicum/01-building-a-basic-agent-loop.md)
- [`practicum/02` — Implementing Tool Use & Function Calling](https://anu00.dev/curriculum/practicum/02-implementing-tool-use-and-function-calling.md)
