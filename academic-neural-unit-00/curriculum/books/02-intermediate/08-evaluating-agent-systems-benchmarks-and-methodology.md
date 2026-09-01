# Evaluating Agent Systems: Benchmarks & Methodology

**评估智能体系统：基准测试与方法论**

| Field   | English                                                       | 中文                                       |
| ------- | ------------------------------------------------------------- | ------------------------------------------ |
| Level   | Intermediate                                                  | 中级                                       |
| Cluster | Multi-Agent Systems & Evaluation                              | 多智能体系统与评估                         |
| Author  | Dr. Mireille Dubois, Research Scientist — LLM Systems, ANU-00 | ANU-00 LLM 系统研究员 Mireille Dubois 博士 |

---

## 0. Where This Module Fits

**本模块的定位**

[`introductory/08` — Why & How We Evaluate Agents](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md) established the vocabulary of agent evaluation at an informal level: a task, a
metric, ground truth, held-out test sets, outcome- versus process-based grading, a first mention of
LLM-as-judge, and the specific evaluation challenge multi-agent systems raise once
[`introductory/07` — Introduction to Multi-Agent Systems](https://anu00.dev/curriculum/books/01-introductory/07-introduction-to-multi-agent-systems.md)'s emergent behavior enters the picture. This module takes every one of those
threads and formalizes it — naming real, published benchmarks by name, deriving the actual metrics
used in production evaluation practice, and treating LLM-as-judge and multi-agent evaluation as
methodologies in their own right rather than as informal cautions. Nothing here assumes coursework
outside this curriculum; every named algorithm and formula is grounded in a verified citation, per
`curriculum/README.md` [§5](#5-llm-as-judge-methodology-in-full-prompting-bias-and-calibration).

[`introductory/08` — Why & How We Evaluate Agents](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md)在非正式的层面上确立了智能体评估的词汇：任务、指标、标准答案、留出测试集、基于结果与基于过程的评分之分、对 LLM 评判的初步提及，以及一旦引入[`introductory/07` — Introduction to Multi-Agent Systems](https://anu00.dev/curriculum/books/01-introductory/07-introduction-to-multi-agent-systems.md)所述的涌现行为后，多智能体系统所带来的特有评估挑战。本模块将这一切线索加以形式化——具名地介绍真实、已发表的基准测试，推导生产实践中实际使用的具体指标，并把 LLM 评判与多智能体评估当作真正意义上的方法论来处理，而不再仅仅是非正式的提醒。本模块的内容不假定读者具备本课程之外的任何背景知识；按照`curriculum/README.md` [第 5 节](#5-llm-as-judge-methodology-in-full-prompting-bias-and-calibration)的要求，此处出现的每一个具名算法与公式都有可核实的引用作为依据。

---

## 1. From an Informal Test Set to a Formal Benchmark

**从非正式测试集到正式基准测试**

[`introductory/08` — Why & How We Evaluate Agents §2](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#2-defining-evaluate-tasks-metrics-and-ground-truth) defined a benchmark loosely as "many tasks, plus a metric and ground truth,
assembled to measure a capability." A rigorous benchmark adds three further requirements that
distinguish it from an ad-hoc test set a developer assembles alone.

[`introductory/08` — 为什么以及如何评估智能体 第 2 节](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#2-defining-evaluate-tasks-metrics-and-ground-truth)将基准测试宽泛地定义为“许多任务，加上指标与标准答案，专门用于衡量某种能力”。一个严谨的基准测试还需满足另外三项要求，从而区别于开发者独自拼凑的临时测试集。

| #   | Requirement                                               | EN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 中文                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| --- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Task diversity**（任务多样性）                          | the tasks must be sampled to represent a genuine distribution of real difficulty and real use cases, not just whatever cases happened to be easy to write.                                                                                                                                                                                                                                                                                                                                                                                                                                             | 任务的抽样必须能够代表真实难度与真实使用场景的实际分布，而不能仅仅是恰好容易编写的那些案例。                                                                                                                                                                                                                                                                                                                                                                           |
| 2   | **Fixed, published protocol**（固定且公开的评测协议）     | exactly how the agent is prompted, how many attempts it gets, and how outputs are graded must be specified precisely enough that two different research groups running the same benchmark on the same system get comparable numbers — without this, a reported score is not reproducible and cannot be trusted for comparison.                                                                                                                                                                                                                                                                         | 智能体究竟如何被提示、能获得多少次尝试机会、输出又如何被评分，都必须被精确规定到足以让两个不同的研究团队在同一系统上运行同一基准测试时得到可比较的数字——若无此项，报告出的分数便无法复现，也就无法用于可信的比较。                                                                                                                                                                                                                                                     |
| 3   | **Public availability of the task set**（任务集公开可用） | or at minimum a held-out portion kept private specifically to prevent the contamination problem named in [`introductory/08` — Why & How We Evaluate Agents §7](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#7-common-pitfalls-for-a-first-evaluation) — a benchmark whose entire task set is public is easiest to trust for reproducibility but easiest to contaminate; one that keeps a private held-out split (as several benchmarks discussed in [§3](#3-a-tour-of-named-agent-benchmarks) do) trades some reproducibility for contamination resistance. | 或者至少保留一部分专门私藏、以防止[`introductory/08` — 为什么以及如何评估智能体 第 7 节](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#7-common-pitfalls-for-a-first-evaluation)所述污染问题的留出部分——一个任务集完全公开的基准测试，最便于复现验证，却也最容易被污染；而保留私有留出部分的基准测试（[第 3 节](#3-a-tour-of-named-agent-benchmarks)将讨论的几个基准测试正是如此）则是以牺牲一部分可复现性来换取抗污染能力。 |

A benchmark that satisfies all three is what allows a claim like "Agent X solves 40% of SWE-bench"
to mean the same thing to every reader, rather than being an artifact of one team's private test
setup.

同时满足这三项要求的基准测试，才能让“智能体 X 解决了 SWE-bench 中 40% 的问题”这样的说法，对每一位读者而言含义都一致，而不是某个团队私有测试环境所特有的产物。

---

## 2. Designing an Agent Benchmark: What Makes It Different from an LLM Benchmark

**设计智能体基准测试：它与 LLM 基准测试有何不同**

A benchmark like MMLU ([`introductory/08` — Why & How We Evaluate Agents §2](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#2-defining-evaluate-tasks-metrics-and-ground-truth)) tests a language model on a single-turn question with
one correct answer chosen from a fixed set of options — the model's whole "action" is producing text
once. An agent, per the loop defined in [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md), may take many steps, call tools, and
interact with a changing environment before producing a final result, so an agent benchmark must
additionally decide: what counts as the environment the agent acts in, how success is checked
against that environment's actual final state (rather than against a single fixed text string), and
how many steps or how much cost the agent is allowed to spend.

像 MMLU 这样的基准测试（见[`introductory/08` — 为什么以及如何评估智能体 第 2 节](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#2-defining-evaluate-tasks-metrics-and-ground-truth)）在单轮问答上测试语言模型，正确答案是从固定选项集中选出的一个——模型的全部“行动”就是生成一次文本。而按照[`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md)所定义的循环，智能体在给出最终结果之前，可能会采取多个步骤、调用工具，并与一个不断变化的环境交互，因此智能体基准测试还必须额外确定：智能体所作用的环境究竟是什么，成功与否应如何依据该环境实际的最终状态来判定（而非依据某个固定的文本字符串），以及允许智能体消耗多少步骤或多少成本。

This last point connects directly to [`introductory/07` — Introduction to Multi-Agent Systems §8](https://anu00.dev/curriculum/books/01-introductory/07-introduction-to-multi-agent-systems.md#8-risks-unique-to-multi-agent-systems)'s naming of cost multiplication as a
genuine risk of agentic and multi-agent systems — an agent benchmark that reports only success rate,
with no accounting for the number of tool calls or tokens spent to achieve it, hides exactly the
cost information a real deployment decision needs. A well-designed agent benchmark therefore
typically reports at least two numbers together: how often the agent succeeded, and how much it cost
to get there.

最后这一点，与 [`introductory/07` — 多智能体系统导论 第 8 节](https://anu00.dev/curriculum/books/01-introductory/07-introduction-to-multi-agent-systems.md#8-risks-unique-to-multi-agent-systems)将成本倍增列为智能体系统与多智能体系统真实风险的论述直接相关——一个只报告成功率、却不核算达成该成功所耗费工具调用次数或词元数量的智能体基准测试，恰恰隐藏了真实部署决策所需要的成本信息。因此，一个设计良好的智能体基准测试通常至少会同时报告两个数字：智能体成功的频率，以及为达成该成功所付出的代价。

---

## 3. A Tour of Named Agent Benchmarks

**具名智能体基准测试巡礼**

Several published benchmarks now anchor the field, and knowing them by name is part of the working
vocabulary of anyone doing agent evaluation.

如今已有若干已发表的基准测试成为该领域的支柱，熟悉它们的名称，是从事智能体评估者工作词汇的一部分。

| Benchmark               | EN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 中文                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SWE-bench**           | introduced by Carlos Jimenez and colleagues in 2023, tests an agent's ability to resolve real, previously filed GitHub issues by editing real code repositories, checking success by running the repository's actual test suite after the agent's edit — grounding "correctness" in genuine software-engineering behavior rather than a hand-written answer key.                                                                                                                                                                                                                                                                                                          | 由 Carlos Jimenez 及其合作者于 2023 年提出，测试智能体解决真实的、此前已提交的 GitHub issue 的能力，做法是让智能体修改真实的代码仓库，再运行该仓库真正的测试套件来检验修改是否成功——从而把“正确性”锚定在真实的软件工程行为上，而非某份手写的标准答案。                                                                                                                                                                                                                                  |
| **WebArena**            | introduced by Shuyan Zhou and colleagues in 2023, places an agent in a realistic, self-hosted set of websites (a Reddit-like forum, a GitLab-like code host, a shopping site, and others) with 812 tasks, and checks success by inspecting the resulting functional state of the website (did the right item end up in the cart, was the right issue actually closed) rather than by comparing the agent's literal sequence of clicks to one fixed "correct" trace — an important design choice, since two different valid sequences of actions can both correctly complete the same real task.                                                                           | 由 Shuyan Zhou 及其合作者于 2023 年提出，将智能体置于一套逼真、可自行部署的网站集合中（类似 Reddit 的论坛、类似 GitLab 的代码托管平台、购物网站等），共设 812 项任务，并通过检验网站最终的功能性状态（正确的商品是否进入了购物车、正确的 issue 是否真的被关闭）来判定成功与否，而不是将智能体逐次点击的实际序列与某条固定的“正确”轨迹相比对——这是一项重要的设计选择，因为两条不同、但都有效的行动序列都可能正确完成同一项真实任务。                                                     |
| **AgentBench**          | introduced by Xiao Liu and colleagues in 2023, deliberately spans eight quite different environments (including operating-system command lines, databases, and games) in one benchmark, specifically to test whether an agent's competence transfers across environment types rather than being narrow to one domain.                                                                                                                                                                                                                                                                                                                                                     | 由 Xiao Liu 及其合作者于 2023 年提出，在同一个基准测试中特意涵盖了八种颇为不同的环境（包括操作系统命令行、数据库与游戏），专门用于检验智能体的能力能否跨环境类型迁移，而非局限于单一领域。                                                                                                                                                                                                                                                                                              |
| **GAIA**                | introduced by Grégoire Mialon and colleagues in 2023, poses 466 real-world assistant questions that require combining web search, tool use, and multi-step reasoning, deliberately designed to be easy for a resourceful human (the paper reports 92% human accuracy) but hard for an agent without genuinely general tool-use ability.                                                                                                                                                                                                                                                                                                                                   | 由 Grégoire Mialon 及其合作者于 2023 年提出，设置了 466 道真实世界的助理型问题，需要综合运用网络搜索、工具使用与多步推理，其刻意设计为对一位善于利用资源的人类而言并不困难（论文报告人类准确率为 92%），但对不具备真正通用工具使用能力的智能体而言却很困难。                                                                                                                                                                                                                            |
| **τ-bench (tau-bench)** | introduced by Shunyu Yao and colleagues in 2024, is structurally different from the other four: it places the agent in a live, multi-turn conversation with a simulated user plus a set of domain-specific tools (retail and airline customer-service scenarios) and a written policy document the agent must actually follow, checking success by comparing the resulting database state to an annotated goal state — this benchmark's reliability metric, pass^k, is developed further in [`advanced/08` — Rigorous Agent Evaluation: Statistical Methodology](https://anu00.dev/curriculum/books/04-advanced/08-rigorous-agent-evaluation-statistical-methodology.md). | 由 Shunyu Yao 及其合作者于 2024 年提出，在结构上与前四者不同：它让智能体与一个模拟用户进行实时的多轮对话，并配以一组特定领域的工具（零售与航空客服场景）以及一份智能体必须切实遵循的书面政策文件，通过比较最终的数据库状态与标注的目标状态来判定成功与否——该基准测试的可靠性指标 pass^k，将在[`advanced/08` — Rigorous Agent Evaluation: Statistical Methodology](https://anu00.dev/curriculum/books/04-advanced/08-rigorous-agent-evaluation-statistical-methodology.md)中进一步展开。 |

---

## 4. Metrics for Agent Evaluation: Success Rate and pass@k

**智能体评估指标：成功率与 pass@k**

The simplest agent metric is plain **success rate**: the fraction of tasks in the benchmark on which
the agent's single attempt met the success criterion. Success rate alone, however, hides an
important distinction for tasks where an agent is allowed multiple independent attempts — a pattern
directly analogous to the self-consistency technique from [`intermediate/05` — Advanced Prompting: Chain-of-Thought, Few-Shot & Structured Output §3](https://anu00.dev/curriculum/books/02-intermediate/05-advanced-prompting-cot-few-shot-structured-output.md#3-self-consistency-sampling-multiple-reasoning-paths), where the same
prompt is sampled multiple times at non-zero temperature rather than run once.

最简单的智能体指标是普通的**成功率**：基准测试中智能体单次尝试满足成功标准的任务所占比例。然而，对于允许智能体进行多次独立尝试的任务而言，成功率单独一项会掩盖一个重要区别——这与[`intermediate/05` — 进阶提示词工程：思维链、少样本与结构化输出 第 3 节](https://anu00.dev/curriculum/books/02-intermediate/05-advanced-prompting-cot-few-shot-structured-output.md#3-self-consistency-sampling-multiple-reasoning-paths)所述的自洽性技巧直接类似，即在非零温度下对同一提示词多次采样，而非只运行一次。

Mark Chen and colleagues, introducing this idea in their 2021 Codex paper (the same paper behind the
HumanEval coding benchmark referenced informally in [`introductory/08` — Why & How We Evaluate Agents §7](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#7-common-pitfalls-for-a-first-evaluation)), defined **pass@k （pass@k
指标）**: the probability that at least one of k independently sampled attempts at a task succeeds.
Naively estimating this by generating exactly k samples and checking whether any succeeded is a
biased, high-variance estimator when k is small relative to the number of samples actually drawn;
Chen et al.'s paper instead gives an unbiased estimator that generates n ≥ k samples per task,
counts the number c of samples that pass, and computes

Mark Chen 及其合作者在其 2021 年的 Codex 论文（[`introductory/08` — 为什么以及如何评估智能体 第 7 节](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#7-common-pitfalls-for-a-first-evaluation)非正式提及的 HumanEval 编程基准测试正出自同一篇论文）中提出了 **pass@k 指标**：即对某项任务独立采样 k 次尝试中，至少有一次成功的概率。若朴素地通过恰好生成 k 个样本、检查是否有任一成功来估计这一概率，当 k 相对于实际抽取的样本数较小时，这种估计是有偏且高方差的；Chen 等人的论文转而给出了一个无偏估计量：对每项任务生成 n ≥ k 个样本，统计其中通过的样本数 c，并计算

```text
pass@k := E[1 - C(n - c, k) / C(n, k)]
```

where `C(n, k)` is the binomial coefficient "n choose k." Practically, this formula is computed by
generating a larger number of samples (say n = 200) once per task, so that pass@k for several
different values of k can all be estimated from the same set of samples without having to re-run the
agent — an efficiency point that matters directly for the cost concern raised in [§2](#2-designing-an-agent-benchmark-what-makes-it-different-from-an-llm-benchmark), since
generating n samples per task across a large benchmark is itself expensive. [`advanced/08` — Rigorous Agent Evaluation: Statistical Methodology](https://anu00.dev/curriculum/books/04-advanced/08-rigorous-agent-evaluation-statistical-methodology.md) returns to
this formula to examine its statistical properties — its variance, and how it can be misused — in
full rigor.

其中 `C(n, k)` 是二项式系数“n 选 k”。在实践中，这个公式的计算方式是对每项任务一次性生成较多数量的样本（例如 n = 200），这样便可以从同一批样本中估计出多个不同 k 值对应的 pass@k，而无需为每个 k 值重新运行智能体——这一效率考量与[第 2 节](#2-designing-an-agent-benchmark-what-makes-it-different-from-an-llm-benchmark)所提出的成本关切直接相关，因为在大型基准测试中为每项任务生成 n 个样本本身就代价高昂。[`advanced/08` — Rigorous Agent Evaluation: Statistical Methodology](https://anu00.dev/curriculum/books/04-advanced/08-rigorous-agent-evaluation-statistical-methodology.md)将回到这一公式，以完全严谨的方式考察其统计性质——包括其方差，以及它可能被误用的方式。

---

## 5. LLM-as-Judge Methodology in Full: Prompting, Bias, and Calibration

**LLM 评判方法论全解：提示词设计、偏差与校准**

[`introductory/08` — Why & How We Evaluate Agents §5](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#5-automated-grading-exact-match-and-the-newer-idea-of-llm-as-judge) introduced LLM-as-judge and named two of its known weaknesses; the source study
deserves fuller treatment here, since it is now a standard evaluation tool in agent research.
Lianmin Zheng and colleagues' 2023 paper "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
studied exactly how well a strong LLM judge's verdicts track human preference judgments, using two
complementary evaluation setups: MT-Bench, a curated set of multi-turn questions graded by both
human annotators and LLM judges, and Chatbot Arena, a crowdsourced platform where real users compare
pairs of model responses.

而是能够在大规模场景下真正替代昂贵人类评估的有用代理。

The paper's central finding was that GPT-4 as a judge agreed with human preference judgments over
80% of the time, matching the agreement rate typically seen between two independent human judges on
the same task — evidence that a well-designed LLM judge is not simply noise, but a genuinely useful
proxy for expensive human evaluation at scale. The same paper, however, documents three specific
bias patterns any practitioner using this method must guard against.

然而，同一篇论文也记录了三种特定的偏差模式，任何使用这一方法的实践者都必须加以防范。

| Bias                      | EN                                                                                                                                                                                                                                                                                                                                    | 中文                                                                                                                                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Position bias**         | when a judge is shown two candidate answers side by side and asked which is better, the verdict can shift depending on which position (first or second) an answer is placed in — the standard mitigation is to run the comparison twice with positions swapped and treat a verdict that flips as a tie rather than a real preference. | 当评判者被并排展示两份候选答案、并被要求判断哪一份更好时，其判决可能会随着答案所处位置（第一位或第二位）的不同而发生变化——标准的缓解方法是交换位置再比较一次，若判决发生翻转，则视为平局而非真实偏好。 |
| **Verbosity bias**        | judges tend to rate longer answers as better independent of actual quality, requiring evaluators to either control for length explicitly or accept this as a genuine limitation of the method.                                                                                                                                        | 评判者倾向于将较长的答案评为更好，而与其实际质量无关，这要求评估者要么明确控制篇幅这一变量，要么将其作为该方法的一项真实局限性加以接受。                                                               |
| **Self-enhancement bias** | a model used as its own judge tends to rate its own outputs more favorably than an independent judge would, which is why rigorous evaluation practice avoids using the same model family as both the system under test and the judge wherever practical.                                                                              | 当一个模型被用来评判自己的输出时，往往会比独立评判者给出更有利的评价，这正是严谨的评估实践在条件允许时，会避免让被测系统与评判者出自同一模型系列的原因。                                               |

---

## 6. Human Evaluation and Measuring Whether Human Raters Agree

**人工评估与人类评分者一致性的度量**

LLM-as-judge does not eliminate the need for human evaluation; rather, human judgments remain the
reference LLM judges are validated against (as in the Zheng et al. study in [§5](#5-llm-as-judge-methodology-in-full-prompting-bias-and-calibration)), and human
evaluation is still the standard for the highest-stakes evaluation decisions. Once more than one
human rater grades the same outputs, however, a new question arises that pure automated grading
never faces: do the raters actually agree with each other?

LLM 评判并不能消除对人工评估的需求；恰恰相反，人类判断依然是 LLM 评判者据以校验的参照标准（如[第 5 节](#5-llm-as-judge-methodology-in-full-prompting-bias-and-calibration) Zheng 等人的研究所示），而对于风险最高的评估决策，人工评估仍然是标准做法。然而，一旦有不止一位人类评分者对同一批输出进行评分，一个纯自动化评分从未遇到过的新问题便随之出现：这些评分者彼此之间真的一致吗？

Simple **percent agreement** — the fraction of items on which two raters gave the same verdict — is
misleading because it does not account for agreement that would occur purely by chance even if the
raters were guessing randomly. Jacob Cohen's 1960 paper "A Coefficient of Agreement for Nominal
Scales" introduced **Cohen's kappa（Cohen's kappa 系数）** to correct for exactly this:

简单的**一致率**——两位评分者给出相同判决的项目所占比例——具有误导性，因为它没有扣除即便评分者纯属随机猜测也会碰巧出现的一致情况。 Jacob Cohen 在其 1960 年的论文《A Coefficient of Agreement for Nominal Scales》中提出了 **Cohen's kappa 系数（Cohen's kappa）**，正是为了修正这一点：

$$\kappa = \frac{p_0 - p_e}{1 - p_e}$$

where $p_0$ is the observed proportion of agreement between the two raters, and $p_e$ is the
proportion of agreement that would be expected if both raters were assigning verdicts independently
at random, given each rater's own marginal rate of each verdict. J. Richard Landis and Gary Koch's
1977 paper proposed a widely used, though explicitly informal, scale for interpreting the resulting
number: values above roughly 0.81 are considered "almost perfect" agreement, 0.61–0.80
"substantial," 0.41–0.60 "moderate," and lower values progressively weaker, down to values at or
below zero indicating agreement no better than (or worse than) chance.

其中 $p_0$ 是两位评分者之间观察到的一致比例，$p_e$ 则是假设两位评分者都是根据各自对每种判决的边际比率独立随机做出判决时，所预期出现的一致比例。 J. Richard Landis 与 Gary Koch 1977 年的论文提出了一套被广泛使用、但明确带有非正式性质的解释量表，用于解读所得数值：约 0.81 以上被视为“近乎完美”的一致；0.61–0.80 为“高度一致”；0.41–0.60 为“中度一致”；数值越低，一致程度依次递减，直至等于或低于零，表示一致程度不优于（甚至劣于）随机水平。

For agent evaluation specifically, computing Cohen's kappa between two human raters, or between a
human rater and an LLM judge, is the correct way to state "how much can this grading method be
trusted" as a number, rather than as an unquantified impression.

就智能体评估而言，计算两位人类评分者之间、或某位人类评分者与某个 LLM 评判者之间的 Cohen's kappa 系数，正是把“这种评分方法究竟有多可信”表述为一个具体数字、而非一种未经量化的印象的正确方式。

---

## 7. Evaluating Multi-Agent Systems: Formalizing the §6 Concern from `introductory/08`

**评估多智能体系统：将[`introductory/08` — 为什么以及如何评估智能体 第 6 节](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#6-evaluating-more-than-one-agent-at-once)的关切加以形式化**

[`introductory/08` — Why & How We Evaluate Agents §6](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#6-evaluating-more-than-one-agent-at-once) flagged that a MAS can produce different outputs on identical repeated runs
because of [`introductory/07` — Introduction to Multi-Agent Systems](https://anu00.dev/curriculum/books/01-introductory/07-introduction-to-multi-agent-systems.md)'s emergent behavior, and that evaluating with a single run therefore
tells you even less than it does for a single agent. Formalizing this: a multi-agent system's
performance on a task is not a single number but a **distribution** of outcomes across repeated
runs, and a rigorous evaluation must report that distribution's spread, not merely its average — a
point developed with the actual statistical machinery in [`advanced/08` — Rigorous Agent Evaluation: Statistical Methodology](https://anu00.dev/curriculum/books/04-advanced/08-rigorous-agent-evaluation-statistical-methodology.md).

[`introductory/08` — 为什么以及如何评估智能体 第 6 节](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#6-evaluating-more-than-one-agent-at-once)曾指出，由于[`introductory/07` — Introduction to Multi-Agent Systems](https://anu00.dev/curriculum/books/01-introductory/07-introduction-to-multi-agent-systems.md)所述的涌现行为，MAS 在完全相同的重复运行中也可能产生不同的输出，因此仅凭单次运行进行评估，其所能告诉你的信息甚至比单智能体的情形还要少。将这一点形式化：一个多智能体系统在某项任务上的表现，并非单一数字，而是重复运行所形成结果的一个 **分布**，而严谨的评估必须报告这一分布的离散程度，而非仅仅报告其均值——这一点将在[`advanced/08` — Rigorous Agent Evaluation: Statistical Methodology](https://anu00.dev/curriculum/books/04-advanced/08-rigorous-agent-evaluation-statistical-methodology.md)中借助真正的统计工具加以展开。

Practically, this means running each benchmark task multiple times (a common choice is somewhere
between 3 and 10 repetitions, depending on cost budget) and reporting the range or spread of success
rates observed, not a single success/fail per task.

在实践中，这意味着需要对每项基准测试任务重复运行多次（常见的选择是 3 到 10 次之间，具体取决于成本预算），并报告观察到的成功率的范围或离散程度，而非每项任务只给出单一的成功/失败结果。

A second, MAS-specific complication [`introductory/08` — Why & How We Evaluate Agents](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md) did not have room to cover: because a MAS's
agents interact through message passing or shared state ([`introductory/07` — Introduction to Multi-Agent Systems §6](https://anu00.dev/curriculum/books/01-introductory/07-introduction-to-multi-agent-systems.md#6-communication-messages-protocols-and-shared-state)), a single failure can
be attributed to more than one plausible cause — did the Coder agent from [`introductory/07` — Introduction to Multi-Agent Systems §5](https://anu00.dev/curriculum/books/01-introductory/07-introduction-to-multi-agent-systems.md#5-a-worked-example-two-agents-writing-and-reviewing-code) write
bad code, or did the Reviewer agent fail to catch a bug it should have caught? Evaluating a
multi-agent system well therefore usually requires grading not just the final outcome but also each
agent's individual contribution along the way — a return, at the level of a whole system, to the
outcome-versus-process distinction [`introductory/08` — Why & How We Evaluate Agents §3](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#3-two-different-questions-did-it-work-and-did-it-work-well) introduced for a single agent.

[`introductory/08` — Why & How We Evaluate Agents](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md)篇幅有限、未能覆盖的第二个 MAS 特有的复杂之处是：由于 MAS 中的智能体通过消息传递或共享状态相互交互（见[`introductory/07` — 多智能体系统导论 第 6 节](https://anu00.dev/curriculum/books/01-introductory/07-introduction-to-multi-agent-systems.md#6-communication-messages-protocols-and-shared-state)），单次失败往往可以归因于不止一个可能的原因——是[`introductory/07` — 多智能体系统导论 第 5 节](https://anu00.dev/curriculum/books/01-introductory/07-introduction-to-multi-agent-systems.md#5-a-worked-example-two-agents-writing-and-reviewing-code)中的编码智能体写出了错误的代码，还是审查智能体未能发现本应发现的漏洞？因此，要恰当地评估一个多智能体系统，通常不仅需要为最终结果评分，还需要沿途为每个智能体各自的贡献评分——这在整个系统的层面上，重新回到了 [`introductory/08` — 为什么以及如何评估智能体 第 3 节](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#3-two-different-questions-did-it-work-and-did-it-work-well)为单个智能体所引入的“结果 vs. 过程”这一区分。

---

## 8. Worked Example: An Evaluation Harness for the Coder/Reviewer System

**实例演练：为编码/审查双智能体系统构建评估工具链**

Take [`introductory/07` — Introduction to Multi-Agent Systems §5](https://anu00.dev/curriculum/books/01-introductory/07-introduction-to-multi-agent-systems.md#5-a-worked-example-two-agents-writing-and-reviewing-code)'s Coder-and-Reviewer MAS and design a proper benchmark for it, applying
everything above.

以[`introductory/07` — 多智能体系统导论 第 5 节](https://anu00.dev/curriculum/books/01-introductory/07-introduction-to-multi-agent-systems.md#5-a-worked-example-two-agents-writing-and-reviewing-code)中的编码/审查双智能体 MAS 为例，运用上文的一切要点，为其设计一套恰当的基准测试。

| #   | Element                                                                                                 | EN                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 中文                                                                                                                                                                                                                                                      |
| --- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Task diversity**（[§1](#1-from-an-informal-test-set-to-a-formal-benchmark)）                          | instead of one function specification (`is_prime`), assemble ten varied specifications spanning easy (`is_even`), medium (`is_prime` with an efficiency requirement), and deliberately tricky cases (a function whose natural first-draft implementation has an off-by-one error).                                                                                                                                                                                        | 不再只用一份函数规格说明（`is_prime`），而是组建十份不同的规格说明，涵盖简单情形（`is_even`）、中等情形（带效率要求的 `is_prime`）以及刻意设置的陷阱情形（其最自然的初稿实现存在差一错误）。                                                              |
| 2   | **Fixed protocol**                                                                                      | each specification is given to the Coder once, the Coder's output is shown to the Reviewer once, and the Coder is allowed exactly one revision based on the Reviewer's feedback — no unlimited back-and-forth, so results are comparable across runs.                                                                                                                                                                                                                     | 每份规格说明只交给编码智能体一次，编码智能体的输出只展示给审查智能体一次，编码智能体只被允许根据审查智能体的反馈修订恰好一次——不允许无限次往返，从而使各次运行的结果具有可比性。                                                                          |
| 3   | **Metrics**                                                                                             | an outcome metric (does the final revised code pass a held-out unit-test suite the agents never see) and a process metric (does the Reviewer's feedback correctly identify the actual bug present, graded by an LLM judge per [§5](#5-llm-as-judge-methodology-in-full-prompting-bias-and-calibration), checked against a human-labeled sample per [§6](#6-human-evaluation-and-measuring-whether-human-raters-agree) to confirm the judge is trustworthy for this task). | 一项结果指标（最终修订后的代码是否通过一套两个智能体都从未见过的留出单元测试套件），以及一项过程指标（审查智能体的反馈是否正确识别出了实际存在的漏洞，按第 5 节所述由 LLM 评判者评分，并按第 6 节所述对照一份人工标注样本核实该评判者对此任务是否可信）。 |
| 4   | **Repetition**（[§7](#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08)） | run each of the ten specifications three times at non-zero temperature and report the range of outcome-metric success across runs, not a single number.                                                                                                                                                                                                                                                                                                                   | 对十份规格说明中的每一份，在非零温度下各运行三次，并报告各次运行中结果指标成功率的取值范围，而非单一数字。                                                                                                                                                |

```text
Spec: "off-by-one trap" function, run 1: outcome = fail (Reviewer missed the bug)
Spec: "off-by-one trap" function, run 2: outcome = pass (Reviewer caught it, Coder fixed it)
Spec: "off-by-one trap" function, run 3: outcome = pass (Reviewer caught it, Coder fixed it)

Reported result for this task: success rate 2/3, not a single "pass" or "fail"
```

```text
规格说明："差一错误陷阱"函数，运行一：结果 = 失败（审查智能体未发现该漏洞）
规格说明："差一错误陷阱"函数，运行二：结果 = 成功（审查智能体发现了漏洞，编码智能体做出了修复）
规格说明："差一错误陷阱"函数，运行三：结果 = 成功（审查智能体发现了漏洞，编码智能体做出了修复）

该任务报告的结果：成功率 2/3，而非单一的"成功"或"失败"
```

Reporting 2/3 rather than picking whichever run happened to run last is precisely the discipline [§7](#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08)
requires, and it reveals something a single run would have hidden entirely: the Reviewer's
bug-catching ability on this particular trap is inconsistent, not reliable — exactly the kind of
specific, actionable finding evaluation exists to produce, echoing [`introductory/08` — Why & How We Evaluate Agents §8](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#8-worked-example-evaluating-the-weather-agent-on-five-tasks)'s weather-
agent example at the level of a full multi-agent system.

报告"2/3"而非仅仅采用恰好最后运行的那一次结果，正是[第 7 节](#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08)所要求的那种严谨态度，并且它揭示出了单次运行本会完全掩盖的信息：审查智能体在这一特定陷阱上发现漏洞的能力并不稳定、并不可靠——这正是评估存在的意义所要产出的那种具体、可付诸行动的发现，与[`introductory/08` — 为什么以及如何评估智能体 第 8 节](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#8-worked-example-evaluating-the-weather-agent-on-five-tasks)天气智能体示例在整个多智能体系统层面上遥相呼应。

---

## 9. Common Methodological Pitfalls at This Level

**本层级的常见方法论陷阱**

Beyond [`introductory/08` — Why & How We Evaluate Agents §7](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#7-common-pitfalls-for-a-first-evaluation)'s three pitfalls, two further failure modes recur once evaluation
becomes formal enough to drive real decisions like model selection or a go/no-go release call.

除[`introductory/08` — 为什么以及如何评估智能体 第 7 节](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#7-common-pitfalls-for-a-first-evaluation)的三种陷阱之外，一旦评估变得足够正式、足以驱动模型选择或“是否发布”这类真实决策，还会反复出现另外两种失效模式。

**Goodhart's law（古德哈特定律）**, an idea most often quoted in the phrasing given by anthropologist Marilyn Strathern in her 1997 paper generalizing economist Charles Goodhart's original 1975 observation about monetary policy — "when a measure becomes a target, it ceases to be a good measure" — describes what happens when a benchmark score stops being a neutral measurement and starts being optimized against directly: a team that tunes an agent specifically to maximize its SWE-bench score risks producing an agent that is good at SWE-bench's particular style of task rather than genuinely good at software engineering, a formal version of the tuning-set overfitting problem from [`introductory/08` — Why & How We Evaluate Agents §4](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#4-building-a-fair-test-set-held-out-tasks-and-why-order-matters) applied to an entire published benchmark rather than a private test set.

**古德哈特定律（Goodhart's law）**——这一观点最常被引用的表述来自人类学家 Marilyn Strathern 1997 年的论文，她在其中将经济学家 Charles Goodhart 1975 年关于货币政策的原始论述加以推广，提出“当一项测量成为目标时，它就不再是一项好的测量”——描述的正是当基准测试分数不再是一种中立的测量、而开始被直接作为优化对象时会发生什么：一个专门为最大化其 SWE-bench 分数而调优智能体的团队，冒着的风险是产出一个擅长应付 SWE-bench 特定任务风格、而非真正擅长软件工程本身的智能体——这是[`introductory/08` — 为什么以及如何评估智能体 第 4 节](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md#4-building-a-fair-test-set-held-out-tasks-and-why-order-matters)所述调优集过拟合问题的一种正式版本，只不过对象从私有测试集变成了整个已发表的基准测试。

**Leaderboard chasing** is the practical symptom: optimizing a system's benchmark number as the
primary goal, rather than as one signal among several (real-world pilot deployment feedback,
process-metric quality per [§7](#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08)'s Reviewer-attribution example, cost per [§2](#2-designing-an-agent-benchmark-what-makes-it-different-from-an-llm-benchmark)) about whether the system
is actually good. Neither pitfall has a purely technical fix; the defense is organizational
discipline — treating any single benchmark number as one input to a decision, never as the decision
itself.

**追逐排行榜**是其实践中的症状：把优化系统的基准测试分数当作首要目标，而不是把它当作判断系统是否真正优秀的多项信号之一（真实世界试点部署的反馈、按[第 7 节](#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08)审查智能体归因示例衡量的过程指标质量、按[第 2 节](#2-designing-an-agent-benchmark-what-makes-it-different-from-an-llm-benchmark)衡量的成本）。这两种陷阱都没有纯技术性的解决办法；防范之道在于组织层面的自律——把任何单一的基准测试分数当作决策的一项输入，而绝不能当作决策本身。

---

## 10. Summary and What's Next

**小结与后续内容**

A rigorous agent benchmark formalizes [`introductory/08` — Why & How We Evaluate Agents](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md)'s informal task/metric/ground-truth
structure with task diversity, a fixed published protocol, and a defined stance on contamination
resistance. Named benchmarks — SWE-bench, WebArena, AgentBench, GAIA, τ-bench — each probe a
different slice of agentic capability, using metrics from plain success rate to the unbiased pass@k
estimator from the same paper that introduced HumanEval.

一个严谨的智能体基准测试，以任务多样性、固定且公开的评测协议，以及对抗污染能力的明确立场，将 [`introductory/08` — Why & How We Evaluate Agents](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md)非正式的“任务/指标/标准答案”结构加以形式化。 SWE-bench、WebArena、AgentBench、 GAIA、τ-bench 等具名基准测试各自探测智能体能力的不同侧面，所用指标从普通成功率，到源自 HumanEval 同一篇论文的无偏 pass@k 估计量不等。

LLM-as-judge, validated against human agreement rates around 80% but subject to position, verbosity,
and self-enhancement biases, complements rather than replaces human evaluation, and Cohen's kappa
gives a precise number for how much any grading method — human or LLM — can be trusted. Multi-agent
evaluation requires treating outcomes as a distribution across repeated runs and attributing failure
to specific agents, and Goodhart's law is the formal name for what happens when a benchmark score is
optimized for its own sake.

LLM 评判虽然经验证与人类一致率约达 80%，却仍受位置偏差、冗长偏差与自我偏好偏差的影响，它是对人工评估的补充而非替代，而 Cohen's kappa 系数则为任何评分方法——无论人工还是 LLM——的可信程度给出了一个精确的数字。多智能体评估要求把结果视为重复运行所形成的一个分布，并将失败归因于具体的智能体，而古德哈特定律正是基准测试分数一旦被当作目标本身来优化时所发生现象的正式名称。

[`advanced/08` — Rigorous Agent Evaluation: Statistical Methodology](https://anu00.dev/curriculum/books/04-advanced/08-rigorous-agent-evaluation-statistical-methodology.md) takes the distributional and multiple-run concerns raised in [§7](#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08) and [§8](#8-worked-example-an-evaluation-harness-for-the-coderreviewer-system) and gives them
full statistical rigor: confidence intervals for a success rate, formal significance testing for
comparing two systems, and the statistical properties of pass@k and Cohen's kappa developed further
than this module's introductory treatment allows.

[`advanced/08` — Rigorous Agent Evaluation: Statistical Methodology](https://anu00.dev/curriculum/books/04-advanced/08-rigorous-agent-evaluation-statistical-methodology.md)将把[第 7 节](#7-evaluating-multi-agent-systems-formalizing-the-6-concern-from-introductory08)与[第 8 节](#8-worked-example-an-evaluation-harness-for-the-coderreviewer-system)所提出的分布性与多次运行相关的关切，赋予完全的统计学严谨性：成功率的置信区间、比较两个系统的正式显著性检验，以及对 pass@k 与 Cohen's kappa 系数统计性质的进一步展开，超出本模块入门层面所能处理的深度。

---

## References

**参考文献**

### External Sources

- [Chen, M. et al. (2021) — "Evaluating Large Language Models Trained on Code" (Codex / HumanEval / pass@k)](https://arxiv.org/abs/2107.03374)
- [Jimenez, C. E. et al. (2023) — "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"](https://arxiv.org/abs/2310.06770)
- [Zhou, S. et al. (2023) — "WebArena: A Realistic Web Environment for Building Autonomous Agents"](https://arxiv.org/abs/2307.13854)
- [Liu, X. et al. (2023) — "AgentBench: Evaluating LLMs as Agents"](https://arxiv.org/abs/2308.03688)
- [Mialon, G. et al. (2023) — "GAIA: A Benchmark for General AI Assistants"](https://arxiv.org/abs/2311.12983)
- [Yao, S. et al. (2024) — "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains"](https://arxiv.org/abs/2406.12045)
- [Zheng, L. et al. (2023) — "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"](https://arxiv.org/abs/2306.05685)
- [Cohen, J. (1960) — "A Coefficient of Agreement for Nominal Scales"](https://journals.sagepub.com/doi/10.1177/001316446002000104)
- [Landis, J. R. & Koch, G. G. (1977) — "The Measurement of Observer Agreement for Categorical Data"](https://pubmed.ncbi.nlm.nih.gov/843571/)
- [Strathern, M. (1997) — "'Improving Ratings': Audit in the British University System"](https://www.cambridge.org/core/journals/european-review/article/abs/improving-ratings-audit-in-the-british-university-system/FC2EE640C0C44E3DB87C29FB666E9AAB)

### Internal Cross-References

- [`introductory/03` — What Is an AI Agent? Concepts & the Agent Loop](https://anu00.dev/curriculum/books/01-introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md)
- [`introductory/07` — Introduction to Multi-Agent Systems](https://anu00.dev/curriculum/books/01-introductory/07-introduction-to-multi-agent-systems.md)
- [`introductory/08` — Why & How We Evaluate Agents](https://anu00.dev/curriculum/books/01-introductory/08-why-and-how-we-evaluate-agents.md)
- [`intermediate/05` — Advanced Prompting: Chain-of-Thought, Few-Shot & Structured Output](https://anu00.dev/curriculum/books/02-intermediate/05-advanced-prompting-cot-few-shot-structured-output.md)
- [`advanced/08` — Rigorous Agent Evaluation: Statistical Methodology](https://anu00.dev/curriculum/books/04-advanced/08-rigorous-agent-evaluation-statistical-methodology.md)
