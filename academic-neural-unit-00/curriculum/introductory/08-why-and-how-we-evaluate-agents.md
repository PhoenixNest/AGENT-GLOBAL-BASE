# Why & How We Evaluate Agents

**为什么以及如何评估智能体**

| Field   | English                                                       | 中文                                       |
| ------- | ------------------------------------------------------------- | ------------------------------------------ |
| Level   | Introductory                                                  | 入门                                       |
| Cluster | Multi-Agent Systems & Evaluation                              | 多智能体系统与评估                         |
| Author  | Dr. Mireille Dubois, Research Scientist — LLM Systems, ANU-00 | ANU-00 LLM 系统研究员 Mireille Dubois 博士 |

---

## 1. The Problem: "It Worked When I Tried It" Is Not Evidence

**问题所在："我试过，它成功了"并不能算作证据**

`introductory/03` defined an AI agent as an LLM wrapped in a loop that perceives, thinks, acts, and
observes, and `introductory/04` showed that loop calling real tools. Once you have built or are
using such an agent, a natural next question arises: does it actually work? A common but weak way
to answer this is to try the agent on two or three questions, watch it succeed, and conclude "it
works." This module explains why that is not good enough, and gives you the vocabulary and basic
method to do better. The core problem with a handful of hand-picked tries is **selection bias**: if you unconsciously pick easy examples, or stop testing as soon as you see a
success, you learn almost nothing about how the agent behaves on the full range of things it will
actually be asked to do. A system that got lucky twice is indistinguishable, from two data points
alone, from a system that is reliably good — and the two are very different systems to actually
rely on.

`introductory/03`将 AI 智能体定义为被包裹在一个"感知—思考—行动—观察"循环中的 LLM，`introductory/04`
则展示了该循环如何调用真实工具。一旦你构建或使用了这样的智能体，一个自然而然的问题便随之而来：它
真的有效吗？一种常见却薄弱的回答方式，是用两三个问题去试探智能体，看到它成功，便断言"它有效"。本
模块将解释为什么这远远不够，并为你提供更好方法所需的基本词汇与方法。仅凭少数几个精挑细选的尝试，
其核心问题在于**选择偏差**：如果你不自觉地挑选了简单的例子，或者一看到成功就
停止测试，那么你几乎无法了解该智能体在其实际将被要求完成的全部任务范围内的表现。仅凭两个数据点，
一个恰好走运两次的系统，与一个真正可靠、始终表现良好的系统是无法区分的——而这二者作为真正可依赖的
系统，其实相差甚远。

The discipline of systematically answering "does this actually work, and how well" is called
**evaluation**. Evaluation is not a single technique but a whole practice: choosing what
"working" means for a given task, assembling a fair and representative set of test cases,
measuring performance on them in a way that cannot be gamed by accident, and being honest about
what the resulting numbers do and do not show. This module walks through that practice at an
introductory level, building directly on the agent concepts from `introductory/03`, `04`, and the
multi-agent concepts from `introductory/07`.

系统性地回答"这东西究竟有没有效、效果如何"，这门学问被称为**评估**。评估并非单一
技巧，而是一整套实践：为某项任务确定"有效"意味着什么，组建一个公平且具有代表性的测试用例集合，以一
种不会被无意间"作弊"利用的方式测量其表现，并对由此得出的数字究竟说明了什么、又没能说明什么保持诚实。
本模块将在入门层面梳理这套实践，直接建立在`introductory/03`、`04`所讲的智能体概念，以及
`introductory/07`所讲的多智能体概念之上。

---

## 2. Defining "Evaluate": Tasks, Metrics, and Ground Truth

**定义"评估"：任务、指标与标准答案**

To evaluate anything precisely, three things must be defined first. A **task** is a
specific, concrete instance of work given to the agent — not "can it answer questions about
weather" in general, but the exact input "what's the weather in Tokyo right now, and should I
bring an umbrella?" from `introductory/03`'s worked example. A **metric** is a rule for
turning the agent's output on a task into a number or category that says how good that output was
— for example, "1 if the final answer correctly states both the weather condition and gives
sensible umbrella advice, 0 otherwise." **Ground truth** is the independently
known correct answer or correct behavior against which the metric compares the agent's output — in
the weather example, ground truth would be the real weather in Tokyo at the time the question was
asked, obtained from a source you trust that is separate from the agent itself. Without all three
— a concrete task, a metric, and ground truth to compare against — "evaluation" is really just an
opinion.

要精确地评估任何事物，必须先定义三样东西。**任务**是交给智能体完成的一项具体、明确的工作
实例——不是泛泛而言的"它能否回答关于天气的问题"，而是`introductory/03`实例演练中那个确切的输入："东京
现在天气如何？我要不要带伞？"。**指标**是一条规则，用于把智能体在某项任务上的输出转化
为一个数字或类别，说明该输出的好坏——例如："若最终答案既正确说明了天气状况，又给出了合理的带伞建议，
则记 1，否则记 0"。**标准答案**是独立已知的正确答案或正确行为，指标据此与智能体的
输出进行比较——在天气示例中，标准答案就是提问那一刻东京的真实天气，来自一个你信任、且独立于智能体
本身的来源。若缺少这三者中的任何一个——具体的任务、指标，以及可供比对的标准答案——所谓"评估"其实
不过是一种主观意见。

A collection of many tasks, together with their metric and ground truth, assembled specifically to
measure a capability, is called a **benchmark**. One well-known early example outside
the agent world is **MMLU（大规模多任务语言理解基准）**, introduced by Dan Hendrycks and colleagues,
which tests a language model with 57 different subjects' worth of multiple-choice exam questions —
each question is a task, "did it pick the labeled correct choice" is the metric, and the exam's
official answer key is the ground truth. The same three-part structure — tasks, metric, ground
truth — applies whether you are evaluating a plain LLM's knowledge or, as this module is concerned
with, a full agent's ability to complete multi-step work.

将许多任务连同其指标与标准答案一起收集起来、专门用于衡量某种能力的集合，称为**基准测试**。智能体领域之外一个著名的早期例子是 **MMLU（大规模多任务语言理解基准）**，由 Dan
Hendrycks 及其合作者提出，它用涵盖 57 个不同学科的选择题来测试语言模型——每道题就是一项任务，"是否
选中了标注的正确选项"就是指标，考试的官方答案便是标准答案。无论是评估一个纯语言模型的知识水平，
还是如本模块所关注的、评估一个完整智能体完成多步骤工作的能力，"任务—指标—标准答案"这套三段式结构
都同样适用。

---

## 3. Two Different Questions: Did It Work, and Did It Work Well?

**两个不同的问题：它有没有成功，以及它做得好不好**

Evaluating an agent can ask two different kinds of question, and it matters which one you are
asking. **Outcome-based evaluation** asks only whether the agent's final result
was correct, ignoring how it got there — for the weather agent, did the final sentence correctly
report rain and correctly advise bringing an umbrella? This is usually the easier kind of
evaluation to automate, because it only needs to check a final answer. **Process-based evaluation**, sometimes called trajectory evaluation, instead looks at the sequence of
steps the agent took in its loop — did it call the right tool, in a sensible order, without wasted
or hallucinated actions (the failure mode named in `introductory/03` §8)? Process-based evaluation
can catch a problem that outcome-based evaluation misses entirely: an agent that reaches the right
final answer by luck, through a badly reasoned or even nonsensical path, passes outcome-based
evaluation but should fail process-based evaluation, and such an agent's apparent success is
unlikely to generalize to a slightly different task. A thorough evaluation of a real agent system
typically checks both.

评估智能体可以提出两种不同类型的问题，而搞清楚自己问的是哪一种至关重要。**基于结果的评估**只关心智能体的最终结果是否正确，而不关心它是如何得到这个结果的——对
天气智能体而言，就是最终那句话是否正确报告了下雨、是否正确建议带伞？这通常是较容易自动化的一类评估，
因为它只需检查最终答案。**基于过程的评估**，有时也称为轨迹评估，则关注智能体在其循环中所采取的一系列步骤——它是否调用了正确的工具、
顺序是否合理、有没有出现`introductory/03`第 8 节所述的浪费或幻觉行动？基于过程的评估能够发现基于
结果的评估完全遗漏的一类问题：一个智能体可能凭运气、通过一条推理糟糕甚至毫无道理的路径，恰好得到了
正确的最终答案——这样的智能体能通过基于结果的评估，却理应无法通过基于过程的评估，而这种表面上的
成功也不太可能推广到略有不同的任务上。对真实智能体系统的全面评估，通常需要二者兼顾。

---

## 4. Building a Fair Test Set: Held-Out Tasks and Why Order Matters

**构建公平的测试集：留出任务及其顺序为何重要**

A single test question is not enough to know how an agent behaves in general — it might succeed
or fail on that one question for reasons that have nothing to do with its typical performance.
Real evaluation therefore uses a **test set**: a collection of many tasks meant to
represent the range of things the agent will actually be asked to do, ideally chosen to include
easy cases, hard cases, and edge cases (unusual inputs that stress a particular weak point). A
critical discipline, easy to violate by accident, is keeping the test set **held out** —
meaning it must not be used to tune the agent's prompt or instructions. If you keep adjusting the
agent's instructions until it passes the same five questions you have been testing with, you have
not measured how well the agent performs in general; you have overfit the prompt to those five
questions specifically, a problem directly analogous to a student who has memorized the answer key
to a practice exam rather than learning the underlying subject. The fix is simple in principle: set
the test tasks aside before you start tuning, and only run them once tuning is finished, ideally
by someone other than the person who did the tuning.

单单一道测试题不足以了解智能体的一般行为——它在那一道题上成功或失败，原因可能与它的典型表现毫无
关系。因此，真正的评估会使用**测试集**：由许多任务组成的集合，旨在代表智能体实际将被
要求完成的各类任务范围，理想情况下应包含简单案例、困难案例，以及边缘案例（对某个特定弱点施加压力
的异常输入）。一条至关重要、却很容易在不知不觉间被违反的准则，是保持测试集**留出**
的状态——也就是说，它不能被用来调整智能体的提示词或指令。如果你不断调整智能体的指令，直到它通过
你一直在用来测试的那五道题，那么你测量到的并不是智能体的一般表现；你实际上是把提示词过拟合到了
那五道特定的题目上，这一问题与一个死记硬背练习题答案、而非真正掌握所学科目的学生如出一辙。原则上
解决方法很简单：在开始调整之前先把测试任务搁置一旁，只在调整完成之后运行一次，理想情况下应由调整
工作的执行者之外的人来运行。

---

## 5. Automated Grading: Exact Match, and the Newer Idea of LLM-as-Judge

**自动化评分：精确匹配，以及较新的"以 LLM 作为评判者"理念**

Once you have a test set, something has to actually check each output against ground truth — this
is called **grading**. The simplest form is **exact match**: the agent's answer
is compared, character-for-character or by a simple rule, against the known correct answer, which
works well when there is exactly one correct form of the answer (a numeric result, a specific
tool call). Many real tasks, however, have answers that are correct in more than one valid
phrasing — "it's raining, bring an umbrella" and "expect rain — an umbrella is a good idea" should
both be graded correct, but exact match would fail the second one. One newer approach to this
problem, made practical only once LLMs themselves became capable graders, is **LLM-as-judge
（LLM 评判 / 以 LLM 作为评判者）**: a separate LLM call is given the task, the agent's output, and
(when available) the ground truth, and asked to judge whether the output is correct or how good it
is. Lianmin Zheng and colleagues' 2023 study of this approach found that a strong LLM judge (GPT-4
in their study) agreed with human judgments over 80% of the time — comparable to the agreement
rate between two different human judges — but the same study also found real weaknesses:
**position bias**, where the judge's verdict can shift depending on which order two
answers being compared are shown in, and **verbosity bias**, where the judge tends to
prefer a longer answer even when it is not actually better. This module names LLM-as-judge only at
an introductory level; `intermediate/08` covers the methodology — including these specific
biases — in full depth, and shows how to use LLM-as-judge more carefully.

有了测试集之后，还需要有某种机制来实际检查每一份输出是否符合标准答案——这个过程称为**评分**。最简单的形式是**精确匹配**：将智能体的答案逐字符或按简单规则与已知
正确答案进行比对，这在答案只有唯一正确形式时（如一个数值结果、一次特定的工具调用）效果良好。然而，
许多真实任务的答案存在不止一种正确的表述方式——"下雨了，带把伞"和"预计有雨——带伞是个好主意"都应
被判为正确，但精确匹配会判定后者为错误。针对这一问题，一种较新的方法——只有当 LLM 本身具备了足够
的评判能力后才变得切实可行——是 **LLM 评判（LLM-as-judge）**：另外发起一次独立的 LLM 调用，向其
提供任务、智能体的输出，以及（若有）标准答案，请它判断该输出是否正确、或有多好。Lianmin Zheng 及其
合作者 2023 年的研究发现，一个强大的 LLM 评判者（他们研究中使用的是 GPT-4）与人类判断的一致率超过
80%——与两位不同人类评判者之间的一致率相当——但同一项研究也发现了确实存在的弱点：**位置
偏差**，即评判者的判决会随着被比较的两份答案展示顺序的不同而发生变化；以及**冗长
偏差**，即评判者倾向于偏爱更长的答案，即便它实际上并不更好。本模块仅在入门层面
提及 LLM 评判；`intermediate/08`将全面深入探讨这一方法论——包括这些具体的偏差——并展示如何更
审慎地使用 LLM 评判。

---

## 6. Evaluating More Than One Agent at Once

**同时评估多个智能体**

`introductory/07` introduced the multi-agent system (MAS) and named **emergent behavior** — a pattern in overall behavior that no single agent's instructions explicitly produced.
Evaluation gets a genuinely new wrinkle once more than one agent is involved: because a MAS's
agents may act in a different order from run to run, or a message may be phrased slightly
differently each time even when nothing is meaningfully "wrong," running the exact same task twice
can produce two different outputs from the exact same system. This means a single run of a
multi-agent task tells you even less than a single run of a single-agent task does, and it is
tempting — but a mistake — to treat one lucky run as proof the system works. The correct response,
covered rigorously in `advanced/08`, is to run the same task multiple times and look at the spread
of outcomes, not just one outcome; this module simply flags that the need exists. `introductory/07`
§5's Coder-and-Reviewer example is worth revisiting here: to properly evaluate that two-agent
system, you would want to run it on many different function specifications, not just the one
`is_prime` example, and check whether the Reviewer reliably catches the same class of bug across
different code, not just that one time.

`introductory/07`介绍了多智能体系统（MAS），并为**涌现行为**命名——即整体
行为中出现的、并非任何单个智能体指令明确产生的某种模式。一旦涉及多个智能体，评估就会遇到一个真正
全新的复杂之处：由于 MAS 中的智能体每次运行的行动顺序可能不同，或者即便没有出现任何实质性"错误"，
每次消息的措辞也可能略有差异，同一项任务运行两次，同一个系统也可能产生两个不同的输出。这意味着，
多智能体任务的单次运行所能告诉你的信息，甚至比单智能体任务的单次运行还要少，而把一次幸运的运行
当作系统有效的证明，是一种很有诱惑力、却也是错误的做法。正确的做法——将在`advanced/08`中严谨展开
——是对同一任务多次运行，观察结果的分布情况，而不仅仅是单一结果；本模块在此只是指出这一需求确实
存在。`introductory/07`第 5 节中"编码智能体与审查智能体"的示例，在此值得重新审视：要恰当地评估
这一双智能体系统，你会希望在许多不同的函数规格说明上运行它，而不仅仅是那一个 `is_prime` 示例，并
检验审查智能体是否在不同代码上都能可靠地发现同一类漏洞，而不只是那一次侥幸发现。

---

## 7. Common Pitfalls for a First Evaluation

**首次评估中的常见陷阱**

Three mistakes recur often enough among people new to evaluation that they are worth naming
plainly. **Cherry-picking** is presenting only the successful runs
while quietly discarding failures — whether done deliberately or, more often, by unconsciously
remembering the wins better than the losses. **Testing on the tuning set** is
the overfitting problem from §4: judging the agent by its performance on the very examples you
used to write or adjust its prompt. **Benchmark leakage / contamination**
is a related but distinct problem specific to LLM-based systems: because the underlying LLM was
trained on a huge amount of text, it is possible that a benchmark's exact questions and answers
appeared somewhere in that training data, so a high score reflects memorization rather than genuine
capability — Shahriar Golchin and Mihai Surdeanu's 2023 research developed concrete methods for
detecting this kind of contamination in an LLM, confirming it is a real, measurable risk and not
just a theoretical worry. None of these three pitfalls require bad intentions to happen; they are
easy to fall into by default, which is exactly why evaluation needs deliberate discipline rather
than being left to instinct.

在评估初学者中反复出现的三种错误，值得在此明确指出。**挑选样本**是指只展示
成功的运行结果，而悄悄丢弃失败的结果——无论是有意为之，还是（更常见地）因为人们无意中对成功的记忆
比对失败的记忆更深刻。**在调优集上测试**就是第 4 节所述的过拟合
问题：用你曾经用来撰写或调整提示词的那些例子来评判智能体的表现。**基准污染 / 数据污染**是一个相关但不同的问题，为基于 LLM 的系统所特有：由于底层 LLM 是在
海量文本上训练而成的，某个基准测试的确切题目与答案有可能恰好出现在那些训练数据之中，于是高分反映
的其实是记忆而非真正的能力——Shahriar Golchin 与 Mihai Surdeanu 在 2023 年的研究开发出了检测 LLM
中此类污染的具体方法，证实这是一种真实、可测量的风险，而非仅仅是理论上的担忧。这三种陷阱都无需
恶意即可发生；它们很容易在不知不觉中被踏入，这正是评估需要刻意的纪律、而不能仅凭直觉行事的原因。

---

## 8. Worked Example: Evaluating the Weather Agent on Five Tasks

**实例演练：在五项任务上评估天气智能体**

Return once more to `introductory/03`'s weather agent, with its one tool `get_weather(city)`.
Instead of trying it on one question, assemble a small held-out test set of five varied tasks, and
grade each with a simple metric ("1" if the final answer correctly reflects both the weather
condition and gives advice consistent with it, "0" otherwise), using exact-match against a real
weather lookup as ground truth:

再次回到`introductory/03`中带有单一工具 `get_weather(city)` 的天气智能体。这一次，不再仅用一个
问题来试探它，而是组建一个包含五项不同任务的小型留出测试集，并用一个简单的指标为每一项打分
（若最终答案既正确反映了天气状况、又给出了与之相符的建议，则记"1"，否则记"0"），以对真实天气查询
结果的精确匹配作为标准答案：

```text
Task 1: "Weather in Tokyo, bring an umbrella?"       -> Correct (rain correctly identified)   -> 1
Task 2: "Weather in a city that doesn't exist: Zzyx"  -> Tool call fails; agent should say so   -> 1
Task 3: "Compare Tokyo and Osaka weather"             -> Only checked Tokyo, ignored Osaka      -> 0
Task 4: "Weather in Tokyo tomorrow"                   -> Tool only supports "right now"; agent
                                                          correctly explained the limitation     -> 1
Task 5: "Weather in Tokyo, in French"                 -> Correct data, but answered in English   -> 0

Success rate: 3 / 5 = 60%
```

```text
任务一："东京天气如何，要不要带伞？"          -> 正确识别出下雨                          -> 1
任务二："查询一个不存在的城市 Zzyx 的天气"     -> 工具调用失败，智能体正确说明了这一点     -> 1
任务三："比较东京与大阪的天气"                 -> 只查了东京，忽略了大阪                  -> 0
任务四："明天东京的天气"                       -> 工具只支持"当前"天气；智能体正确说明了
                                                  这一限制                                  -> 1
任务五："用法语回答东京天气"                   -> 数据正确，但用英文作答                  -> 0

成功率：3 / 5 = 60%
```

A single question ("what's the weather in Tokyo?") would have suggested the agent works perfectly.
The five-task test set instead reveals two genuine, specific weaknesses — it does not reliably
handle multi-city comparisons (Task 3) and does not respect a requested output language (Task 5) —
that a developer can now go fix, and can re-test against the same held-out set afterward to confirm
the fix actually worked without accidentally breaking Tasks 1, 2, or 4. This is the entire point of
evaluation: not a verdict of "good" or "bad," but a specific, actionable map of where a system
works and where it does not.

若只用一个问题（"东京天气如何？"）来测试，会让人误以为该智能体表现完美。而这个包含五项任务的测试集
则揭示出两个真实、具体的弱点——它无法可靠地处理多城市比较（任务三），也没有遵守所要求的输出语言
（任务五）——开发者现在可以着手修复这两个问题，之后再用同一份留出测试集重新测试，以确认修复确实
生效，且没有意外破坏任务一、二、四的表现。这正是评估的全部意义所在：它给出的不是"好"或"坏"这样
笼统的判词，而是一幅具体、可付诸行动的地图，标明系统在何处有效、在何处无效。

---

## 9. Summary and What's Next

**小结与后续内容**

Evaluating an agent means precisely defining tasks, a metric, and ground truth, then measuring
performance on a held-out test set rather than trusting a handful of hand-picked tries. Outcome-
based evaluation checks the final answer; process-based evaluation checks the path taken to get
there, catching lucky-but-badly-reasoned successes that outcome-based evaluation misses. Grading
can be automated by exact match or, for answers with more than one valid phrasing, by LLM-as-judge
— a genuinely useful but bias-prone technique. Multi-agent systems add run-to-run variance on top
of everything single-agent evaluation must already handle, and cherry-picking, tuning-set testing,
and benchmark contamination are three common ways an evaluation can quietly mislead its own author.

评估一个智能体，意味着精确地定义任务、指标与标准答案，然后在一个留出测试集上测量表现，而不是仅仅
信赖少数几个精挑细选的尝试。基于结果的评估检查最终答案；基于过程的评估则检查得出答案所经过的路径，
从而能够发现那些基于结果的评估会遗漏的、"侥幸成功但推理糟糕"的情形。评分既可以通过精确匹配实现
自动化，也可以针对存在多种有效表述方式的答案，采用 LLM 评判——一种确实有用、但也容易产生偏差的
技术。多智能体系统在单智能体评估本已必须处理的一切之上，又增添了运行间的方差；而挑选样本、在调优集
上测试，以及基准污染，则是评估会在不知不觉间误导其作者自身的三种常见方式。

The next module in this cluster, `intermediate/08`, formalizes everything introduced here: it
covers named agent benchmarks such as SWE-bench and WebArena, the LLM-as-judge methodology in full
depth, and the specific challenges of evaluating multi-agent systems raised in §6. `advanced/08`
then goes further, covering the statistical machinery — confidence intervals, significance
testing — needed to state an evaluation result rigorously rather than just descriptively.

本主题群的下一个模块`intermediate/08`将把本模块所引入的一切加以形式化：它将介绍 SWE-bench 与
WebArena 等具名的智能体基准测试、LLM 评判方法论的全部深度，以及第 6 节所提出的多智能体系统评估
所特有的挑战。`advanced/08`则会更进一步，介绍陈述评估结果所需的统计工具——置信区间、显著性
检验——使结论能够被严谨地表述，而不仅仅是描述性的。

---

## References

**参考文献**

### External Sources

- [Hendrycks, D. et al. (2020) — "Measuring Massive Multitask Language Understanding" (MMLU)](https://arxiv.org/abs/2009.03300)
- [Zheng, L. et al. (2023) — "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"](https://arxiv.org/abs/2306.05685)
- [Golchin, S. & Surdeanu, M. (2023) — "Time Travel in LLMs: Tracing Data Contamination in Large Language Models"](https://arxiv.org/abs/2308.08493)
- [Liang, P. et al. (2022) — "Holistic Evaluation of Language Models" (HELM)](https://arxiv.org/abs/2211.09110)

### Internal Cross-References

- [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](./03-what-is-an-ai-agent-concepts-and-the-agent-loop.md)
- [`introductory/04` — Tool Use & Function Calling Basics](./04-tool-use-and-function-calling-basics.md)
- [`introductory/07` — Introduction to Multi-Agent Systems](./07-introduction-to-multi-agent-systems.md)
- [`intermediate/08` — Evaluating Agent Systems: Benchmarks & Methodology](../intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md)
- [`advanced/08` — Rigorous Agent Evaluation: Statistical Methodology](../advanced/08-rigorous-agent-evaluation-statistical-methodology.md)
