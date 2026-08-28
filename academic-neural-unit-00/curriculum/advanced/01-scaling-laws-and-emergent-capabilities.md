# Scaling Laws & Emergent Capabilities

**规模法则与涌现能力**

| Field   | English                                                                  | 中文                                              |
| ------- | ------------------------------------------------------------------------ | ------------------------------------------------- |
| Level   | Advanced                                                                 | 高级                                              |
| Cluster | Foundations                                                              | 基础                                              |
| Author  | Dr. Samuel Okonkwo, Research Scientist — Machine Learning Theory, ANU-00 | ANU-00 机器学习理论研究科学家 Samuel Okonkwo 博士 |

---

## 1. Introduction: From One Model's Training Run to a Family of Models at Every Scale

**引言：从单个模型的训练过程到覆盖各种规模的一整个模型家族**

[`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) studied training dynamics for a single model of fixed size — how it descends the
loss landscape, and why it generalizes or fails to. This module asks a different kind of question,
one that only makes sense once you have trained not one model but _many_ models of systematically
varying size, varying amounts of training data, and varying amounts of compute: is there a
predictable relationship between how large a model is, how much data and compute it was trained
with, and how well it performs?

[`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) 研究的是单个固定规模模型的训练动力学——它如何沿着损失曲面下降，又为什么能够泛化或者泛化失败。本模块所问的是另一类问题，这类问题只有在你不是训练了一个模型、而是训练了系统性变化规模、变化训练数据量、变化训练算力的*许多*模型之后才有意义：一个模型的规模有多大、用了多少数据和算力来训练、最终表现有多好，这三者之间是否存在一种可预测的关系？

If there is such a relationship, it would let a lab predict the performance of a model it has not
yet trained — including models far larger than anything trained so far — from the performance of
smaller, cheaper experiments. This turns out to be true to a remarkable degree, and the resulting
relationships are called **scaling laws**.

如果确实存在这样的关系，一个实验室就可以从规模较小、成本较低的实验结果中，预测出一个尚未训练过的模型——包括比迄今训练过的任何模型都大得多的模型——的表现。事实证明，这种关系在惊人的程度上是成立的，由此得到的关系被称为**规模法则**。

A second, closely related question this module addresses is whether model capability changes
_smoothly_ with scale, or whether some capabilities appear suddenly, in a way that a smooth
extrapolation from smaller models would not have predicted — a phenomenon studied under the name
**emergent capabilities**. As you will see in [§§6–7](#6-emergent-capabilities-the-claim), whether this second phenomenon is real in the
strong sense originally claimed, or is instead an artifact of how it was measured, is a genuinely
open and actively contested question in the field, and this module presents both sides rather than
picking a winner.

本模块所探讨的第二个、与之密切相关的问题是：模型的能力是随规模**平滑**变化，还是有些能力会突然出现——以一种仅凭对小模型的平滑外推根本无法预测的方式突然出现——这种现象被称为**涌现能力**。正如你将在第 6 至 7 节中看到的，这第二种现象在最初被提出的那种强意义上是否真实存在，还是仅仅是测量方式所造成的假象，在这个领域中至今仍是一个真正悬而未决、且被激烈争论的问题；本模块会呈现双方的观点，而不会替你选定一个“赢家”。

---

## 2. The Kaplan et al. Power-Law Picture

**Kaplan 等人的幂律图景**

In 2020, Kaplan, McCandlish, Henighan, Brown, Chess, Child, Gray, Radford, Wu, and Amodei published
"Scaling Laws for Neural Language Models," training a large family of transformer language models of
systematically varying size on varying amounts of data, and fitting the resulting test-loss
measurements to power-law curves.

2020 年，Kaplan、McCandlish、Henighan、Brown、Chess、Child、Gray、Radford、Wu 与 Amodei 发表了《Scaling Laws for Neural Language Models》一文，训练了一大批规模系统性变化的 Transformer 语言模型，并配以不同数量的训练数据，将得到的测试损失结果拟合成幂律曲线。

A **power law** is a relationship of the form $y = a \cdot x^b$; on a log–log plot, a power law
appears as a straight line, which is exactly the pattern the authors found across more than six
orders of magnitude of model size, dataset size, and compute — an unusually clean and wide-ranging
empirical regularity for a system as complex as a trained neural network.

**幂律**是形如 $y = a \cdot x^b$ 的关系；在对数–对数坐标图上，幂律呈现为一条直线，这正是作者在跨越六个数量级以上的模型规模、数据集规模与算力上所发现的模式——对于一个像训练好的神经网络这样复杂的系统而言，这是一种异常干净、覆盖范围异常宽广的经验规律。

Specifically, holding the other two factors from being the bottleneck, the paper reports three
separate power-law relationships between the cross-entropy test loss L and, respectively, the number
of non-embedding model parameters N, the dataset size D (in tokens), and the amount of training
compute $C_{\min}$: $L(N) = (N_c/N)^{\alpha_N}$ with $\alpha_N \approx 0.076$ and $N_c \approx 8.8
\times 10^{13}$; $L(D) = (D_c/D)^{\alpha_D}$ with $\alpha_D \approx 0.095$ and $D_c \approx 5.4
\times 10^{13}$ tokens; and $L(C_{\min}) = (C_c/C_{\min})^{\alpha_{C_{\min}}}$ with
$\alpha_{C_{\min}} \approx 0.050$.

具体而言，在保持另外两个因素不成为瓶颈的前提下，该论文报告了交叉熵测试损失 L 分别与非嵌入模型参数数量 N、数据集规模 D（以词元数计）、训练算力量 $C_{\min}$ 之间的三条独立的幂律关系：$L(N) = (N_c/N)^{\alpha_N}$，其中 $\alpha_N \approx 0.076$，$N_c \approx 8.8 \times 10^{13}$；$L(D) = (D_c/D)^{\alpha_D}$，其中 $\alpha_D \approx 0.095$，$D_c \approx 5.4 \times 10^{13}$ 个词元；以及 $L(C_{\min}) = (C_c/C_{\min})^{\alpha_{C_{\min}}}$，其中 $\alpha_{C_{\min}} \approx 0.050$。

A second, equally important finding of the paper is that other architectural choices — network depth
versus width, the number of attention heads (introduced in [`introductory/02`](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md)), and similar details —
have comparatively minor effects on loss within a wide range, as long as total parameter count is
held fixed; scale, in other words, dominates architectural fine-tuning as a lever for improving
performance.

该论文同样重要的第二项发现是：只要总参数量保持固定，其他架构选择——网络的深度与宽度之比、注意力头的数量（在 [`introductory/02`](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md) 中已经介绍过）等类似细节——在相当宽的范围内对损失的影响都相对较小；换句话说，作为提升性能的杠杆，规模本身要比架构上的精细调整更为主导。

---

## 3. A Worked Example: Extrapolating Loss from the Power Law

**一个实例：从幂律外推损失**

Consider the model-size relationship $L(N) = (N_c/N)^{\alpha_N}$ with $\alpha_N \approx 0.076$.
Suppose a lab has trained a model with $N_1$ parameters and measured its test loss $L_1$, and wants
to predict the loss $L_2$ of a second model with ten times as many parameters, $N_2 = 10 \cdot N_1$
(holding data and compute large enough not to bottleneck either model).

考虑模型规模关系 $L(N) = (N_c/N)^{\alpha_N}$，其中 $\alpha_N \approx 0.076$。假设某实验室训练了一个参数量为 $N_1$ 的模型，测得其测试损失为 $L_1$，现在想要预测第二个参数量为原来十倍（$N_2 = 10 \cdot N_1$）的模型的损失 $L_2$（假设数据量与算力都足够大，不会成为瓶颈）。

Because $L_1/L_2 = (N_2/N_1)^{\alpha_N} = 10^{0.076}$, we get $L_2 = L_1 / 10^{0.076}$. Computing
$10^{0.076} = e^{0.076 \cdot \ln 10} = e^{0.076 \times 2.3026} = e^{0.175} \approx 1.191$, so $L_2
\approx L_1 / 1.191 \approx 0.840 \cdot L_1$ — a ten-fold increase in parameter count is predicted
to reduce the test loss by roughly 16%, all else held equal.

由于 $L_1/L_2 = (N_2/N_1)^{\alpha_N} = 10^{0.076}$，可得 $L_2 = L_1 / 10^{0.076}$。计算 $10^{0.076} = e^{0.076 \cdot \ln 10} = e^{0.076 \times 2.3026} = e^{0.175} \approx 1.191$，因此 $L_2 \approx L_1 / 1.191 \approx 0.840 \cdot L_1$——也就是说，参数量增加十倍，预计能使测试损失降低约 16%，其他条件不变。

This small exponent ($\alpha_N \approx 0.076$, far less than 1) is exactly why frontier labs need to
increase model size by very large multiplicative factors — not by 10% or 50% — to achieve visibly
better performance, and it directly foreshadows the question [§4](#4-the-chinchilla-correction-compute-optimal-scaling) asks next: given that both more
parameters _and_ more data each individually reduce loss following their own power law, and given
that a real training run has a fixed total compute budget to split between the two, what is the best
way to split it?

正是因为这个指数很小（$\alpha_N \approx 0.076$，远小于 1），前沿实验室才需要把模型规模成倍地、大幅度地扩大——而不是仅仅增加 10% 或 50%——才能获得肉眼可见的性能提升，而这也直接引出了[第 4 节](#4-the-chinchilla-correction-compute-optimal-scaling)接下来要问的问题：既然更多的参数*和*更多的数据各自都能按照它们各自的幂律降低损失，而一次真实的训练运行只有固定的总算力预算需要在两者之间分配，那么该如何分配才是最优的？

---

## 4. The Chinchilla Correction: Compute-Optimal Scaling

**Chinchilla 的修正：算力最优的规模分配**

Kaplan et al.'s original paper, when used to derive a compute-optimal split between model size and
data, implied that as compute grows, model size should grow substantially faster than dataset size —
motivating a wave of very large models trained on comparatively modest amounts of data.

Kaplan 等人最初的论文，若被用来推导模型规模与数据量之间算力最优的分配方式，会得出一个结论：随着算力的增长，模型规模应当比数据集规模增长得快得多——这一结论催生了一波在相对有限的数据量上训练超大模型的浪潮。

In 2022, Hoffmann, Borgeaud, Mensch, Buchatskaya, Cai, Rutherford, and colleagues at DeepMind
revisited this question directly, training over 400 language models ranging from 70 million to over
16 billion parameters on data ranging from 5 billion to 500 billion tokens, and fitting a
compute-optimal frontier to the results.

2022 年，Hoffmann、Borgeaud、Mensch、Buchatskaya、Cai、Rutherford 以及 DeepMind 的其他几位同事直接重新审视了这个问题，训练了 400 多个语言模型，规模从 7000 万到超过 160 亿参数不等，训练数据从 50 亿到 5000 亿个词元不等，并将结果拟合出一条算力最优的前沿曲线。

Their central finding reversed the earlier implication: for compute-optimal training, model size N
and dataset size D should each scale at _equal_ rates with compute — for every doubling of model
size, the number of training tokens should also be doubled — meaning the large models trained under
the earlier scaling picture had, in the authors' words, been **significantly undertrained** relative
to their size.

他们的核心发现推翻了此前的推论：在算力最优的训练中，模型规模 N 与数据集规模 D 应当以*相同*的速率随算力增长——模型规模每翻一倍，训练词元数量也应当翻一倍——这意味着，按照此前那种规模法则的图景所训练出的大模型，用作者自己的话说，相对于其规模而言，是**严重训练不足的**。

To demonstrate this, the authors trained **Chinchilla**（龙猫模型）, a 70-billion-parameter model trained
on the same total compute budget as an existing 280-billion-parameter model called Gopher, but on
roughly four times as much data — about 1.4 trillion tokens, which works out to approximately 20
training tokens for every model parameter, now widely cited as the "Chinchilla-optimal" ratio.

为验证这一点，作者训练了 **Chinchilla（龙猫模型）**——一个 700 亿参数的模型，使用与一个已有的、名为 Gopher 的 2800 亿参数模型相同的总算力预算进行训练，但用了大约四倍的数据——约 1.4 万亿个词元，折算下来大约是每个模型参数配 20 个训练词元，如今这一比例被广泛称为“Chinchilla 最优”比例。

Despite having a quarter of Gopher's parameter count, Chinchilla outperformed it substantially
across standard benchmarks, including reaching a then-state-of-the-art average accuracy of 67.5% on
the MMLU benchmark — direct empirical confirmation that, for a fixed compute budget, a smaller model
trained on proportionally more data can beat a larger model trained on proportionally less.

尽管参数量只有 Gopher 的四分之一，Chinchilla 在标准基准测试上的表现却大幅超越了它，包括在 MMLU 基准上达到了当时最先进的 67.5% 平均准确率——这是“在固定算力预算下，用相对更多数据训练的较小模型可以击败用相对更少数据训练的较大模型”这一结论的直接实证。

---

## 5. A Worked Example: Compute-Optimal Allocation as a Budget Grows

**一个实例：算力预算增长时的最优分配**

Suppose, following [§4](#4-the-chinchilla-correction-compute-optimal-scaling)'s roughly 20-tokens-per-parameter heuristic, a lab starts with a
compute-optimal model of $N_1$ = 1 billion parameters trained on $D_1$ = 20 billion tokens.

沿用[第 4 节](#4-the-chinchilla-correction-compute-optimal-scaling)中“每参数约 20 个词元”这一经验法则，假设某实验室最初有一个算力最优的模型，参数量 $N_1$ = 10 亿，训练数据量 $D_1$ = 200 亿词元。

Because the Chinchilla finding says compute-optimal N and D should each scale at the _same_ rate
with compute — both roughly as the square root of the compute budget, $N \propto C^{0.5}$ and $D
\propto C^{0.5}$, since doubling one without the other would violate the "double both together" rule
— a 100-fold increase in available compute ($C_2 = 100 \cdot C_1$) implies both N and D should scale
by $100^{0.5} = 10$, giving a new compute-optimal model of $N_2$ = 10 billion parameters trained on
$D_2$ = 200 billion tokens.

由于 Chinchilla 的发现指出，算力最优的 N 与 D 应当以*相同*的速率随算力增长——二者都大致按算力预算的平方根增长，即 $N \propto C^{0.5}$、$D \propto C^{0.5}$（因为只增大其中一个而不增大另一个，就会违反"两者同步翻倍"这条规则）——因此，可用算力增加 100 倍（$C_2 = 100 \cdot C_1$）意味着 N 与 D 都应按 $100^{0.5} = 10$ 的倍数增长，得到一个新的算力最优模型：参数量 $N_2$ = 100 亿，训练数据量 $D_2$ = 2000 亿词元。

Notice that the ratio $D_2/N_2 = 200/10 = 20$ is unchanged from $D_1/N_1 = 20/1 = 20$ — this is
exactly what "N and D scale at equal rates" means concretely: the _ratio_ between them stays roughly
constant across a compute-optimal frontier, even as their absolute values grow by an order of
magnitude. This is the calculation, in miniature, that determined the specific size Hoffmann et al.
chose for Chinchilla itself, and it is why "roughly 20 tokens per parameter" became a practical rule
of thumb for planning a compute-optimal training run, rather than a coincidence specific to one
model.

注意，$D_2/N_2 = 200/10 = 20$ 这一比例与 $D_1/N_1 = 20/1 = 20$ 完全一致——这正是“N 与 D 以相同速率增长”这句话的具体含义：即便二者的绝对数值都增长了一个数量级，它们之间的*比例*在整条算力最优前沿上大致保持不变。这正是 Hoffmann 等人为 Chinchilla 本身确定具体规模时所做的计算（这里只是把它缩微重现了一遍），这也是为什么“每参数约 20 个词元”会成为规划算力最优训练时的一条实用经验法则，而不是某一个模型身上的偶然巧合。

---

## 6. Emergent Capabilities: The Claim

**涌现能力：这一说法本身**

[§§2–5](#2-the-kaplan-et-al-power-law-picture) described loss as a smooth power-law function of scale.

[第 2 至 5 节](#2-the-kaplan-et-al-power-law-picture)所描述的，是语言建模目标（预测下一个词元）上的损失作为规模的一个平滑幂律函数。

But loss on the language-modeling objective (predicting the next token) is not the same thing as
performance on a specific downstream task a user actually cares about — arithmetic, multi-step
reasoning, following an unusual instruction — and in 2022, Wei, Tay, Bommasani, Raffel, Zoph,
Borgeaud, Yogatama, Bosma, Zhou, Metzler, Chi, Hashimoto, Vinyals, Liang, Dean, and Fedus surveyed a
range of such downstream tasks and reported a striking pattern: on many of them, performance stayed
flat at essentially random-chance level as model scale increased, until a certain scale threshold,
past which performance rose sharply — a pattern the authors defined as an **emergent ability**: one
that "is not present in smaller models but is present in larger models," and specifically one whose
presence "cannot be predicted by simply extrapolating the performance of smaller models."

但语言建模目标上的损失，与用户真正关心的某个下游任务上的表现——算术运算、多步推理、遵循某种不寻常的指令——并不是同一回事；2022 年，Wei、Tay、Bommasani、Raffel、Zoph、Borgeaud、Yogatama、Bosma、Zhou、Metzler、Chi、Hashimoto、Vinyals、Liang、Dean 与 Fedus 考察了一系列这样的下游任务，报告了一个引人注目的模式：在其中许多任务上，随着模型规模的增长，性能基本停留在与随机猜测相当的水平，直到达到某个规模阈值之后，性能才会急剧攀升——作者将这种模式定义为**涌现能力**：一种“在较小模型中不存在、只在较大模型中出现”的能力，具体而言，是一种其出现“无法仅凭对较小模型性能的外推来预测”的能力。

The examples the authors surveyed span tasks such as multi-step arithmetic, certain word-manipulation puzzles, and — of particular relevance to agent development — the effectiveness of **chain-of-thought prompting**（思维链提示，which a later module, `intermediate/05-advanced-prompting-cot-few-shot-structured-output.md`, covers in depth): asking a model to reason step by step before answering provides little to no benefit on many reasoning tasks below a certain model scale, and a large benefit above it.

作者所考察的例子涵盖了诸如多步算术运算、某些文字操作类谜题，以及——与智能体开发尤为相关的——**思维链提示（chain-of-thought prompting，后续模块 `intermediate/05-advanced-prompting-cot-few-shot-structured-output.md` 会对此深入讲解）**的效果：要求模型在回答前逐步进行推理，在许多推理任务上，当模型规模低于某个阈值时几乎没有效果，而一旦超过这个阈值，效果就会大幅提升。

If this pattern is real in the strong sense the term "emergence" implies, it has a significant
practical consequence: capabilities a lab wants may simply not exist yet at the scale it can
currently afford to train, no matter how the training data or prompting strategy is tuned, and may
appear suddenly and somewhat unpredictably at some future scale.

如果这种模式在“涌现”一词所暗示的那种强意义上确实真实存在，它就会带来一个重要的实践后果：一个实验室想要的某些能力，可能在它当前负担得起的训练规模下根本还不存在，无论怎样调整训练数据或提示策略都无济于事,而这些能力却可能在未来的某个规模节点上突然地、且在某种程度上不可预测地出现。

---

## 7. The Mirage Critique: Is Emergence in the Metric, Not the Model?

**“海市蜃楼”式的批评：涌现究竟在模型里，还是在度量方式里？**

In 2023, Schaeffer, Miranda, and Koyejo published "Are Emergent Abilities of Large Language Models a
Mirage?", directly challenging the interpretation in [§6](#6-emergent-capabilities-the-claim). Their central argument is that emergence,
as reported by Wei et al. and similar work, arises primarily from the _choice of evaluation metric_
rather than from a genuine, sudden change in the underlying model.

2023 年，Schaeffer、Miranda 与 Koyejo 发表了《Are Emergent Abilities of Large Language Models a Mirage?》一文，直接挑战了[第 6 节](#6-emergent-capabilities-the-claim)的解读。他们的核心论点是：Wei 等人及类似工作所报告的涌现现象，主要源自*评估度量方式的选择*，而不是底层模型本身发生了真正的、突然的变化。

Many of the tasks showing sharp "emergent" jumps were scored with **nonlinear or discontinuous
metrics** — most commonly exact-match accuracy on a multi-token answer, which scores an answer as
entirely right or entirely wrong even when the model's underlying token-level probabilities are
shifting gradually and continuously.

许多表现出尖锐“涌现”式跃升的任务，所使用的都是**非线性或不连续的度量指标**——最常见的是对多词元答案采用精确匹配准确率，即便模型底层的、逐词元的概率正在平滑而连续地变化，这种指标也只会把一个答案判为“完全正确”或“完全错误”。

A model whose per-token probability of producing each correct token in a long answer is improving
smoothly with scale can, under an exact-match metric that requires every single token to be correct,
show a test score that stays near zero for a long stretch and then rises sharply — not because the
underlying model changed discontinuously, but because the scoring rule amplifies smooth, continuous
improvement into an apparently discontinuous jump once a threshold of per-token accuracy is crossed.

一个模型生成一段较长答案中每个正确词元的逐词元概率，随规模增长而平滑提升，但在要求每一个词元都必须正确的精确匹配度量下，测试得分可能在很长一段区间内都接近于零，随后才急剧上升——这并非因为底层模型发生了不连续的变化，而是因为一旦跨过某个逐词元准确率的阈值，这种评分规则就会把平滑而连续的改进放大成一次看似不连续的跃升。

The authors' proposed test is to re-score the same model outputs on the same tasks using a smooth,
continuous metric — such as token-level log-likelihood or a partial-credit score — instead of the
original discontinuous one, and to check whether the "emergent" jump disappears. Where it does
disappear under a smoother metric, the authors argue, the underlying capability was actually
improving predictably all along, and what looked like emergence was a property of how success was
being counted, not of the model.

作者提出的检验方法是：用一种平滑、连续的度量方式——例如逐词元的对数似然，或者某种部分给分的评分方式——而不是原来那种不连续的指标，对同一批任务上的同一批模型输出重新打分，并检验那个“涌现式”的跃升是否会消失。作者认为，在换用更平滑的度量后跃升确实消失的情形下，说明底层能力其实一直在以可预测的方式提升，看起来像涌现的现象，其实是“成功如何被计数”这一度量方式的属性，而不是模型本身的属性。

This is a genuinely significant methodological challenge, and per this curriculum's standing rule on
unsettled claims (`curriculum/README.md` [§5](#5-a-worked-example-compute-optimal-allocation-as-a-budget-grows)), it should not be read as having fully replaced Wei et
al.'s account: the debate is not closed.

这是一项确实很有分量的方法论挑战；但按照本课程对悬而未决的说法所遵循的一贯原则（见 `curriculum/README.md` § 5），不应把它解读为已经完全取代了 Wei 等人的论述：这场争论并未落定。

Defenders of the original emergence framing have pointed out that some tasks and some real-world
capability thresholds are genuinely discontinuous by their nature — a model either can or cannot
reliably execute a multi-step plan without a single mistake, for instance, in a way a smoother
metric cannot fully paper over — and that a metric-artifact explanation, even where it applies, does
not necessarily generalize to every reported case of emergence. A reader entering this field should
treat "are emergent abilities real, or a measurement artifact" as an open empirical and
methodological question under active investigation, not as one this module — or the field — has
settled.

原始涌现说法的支持者也指出，有些任务、有些现实世界中的能力门槛，就其本质而言确实是不连续的——例如，一个模型要么能够不出一丝差错地可靠执行一项多步计划，要么不能，这种不连续性并不是换一种更平滑的度量方式就能完全抹平的；而且，即便“度量假象”这一解释在某些情形下成立，也未必能推广到每一个被报告为涌现的案例上。初入这一领域的读者，应当把“涌现能力究竟是真实存在，还是一种测量假象”视为一个仍在被积极研究、悬而未决的实证与方法论问题,而不是本模块——乃至整个学界——已经盖棺定论的结论。

---

## 8. Summary

**小结**

Scaling laws ([§§2–5](#2-the-kaplan-et-al-power-law-picture)) are among the most robust and practically consequential empirical findings in
modern deep learning: test loss falls as a clean power law in model size, dataset size, and compute,
and the Chinchilla correction to the original Kaplan et al. picture showed that compute-optimal
training splits a fixed compute budget between model size and data at equal rates — a finding with
direct, dollar-and-GPU-hour consequences for how every frontier lab plans a training run.

规模法则（[第 2 至 5 节](#2-the-kaplan-et-al-power-law-picture)）是现代深度学习中最为稳健、也最具实践意义的经验发现之一：测试损失随模型规模、数据集规模和算力呈现干净的幂律下降；而 Chinchilla 对 Kaplan 等人最初图景的修正表明，算力最优的训练需要把固定的算力预算以相同的速率分配给模型规模与数据量——这一发现直接关系到每一个前沿实验室在规划一次训练运行时,实实在在的资金与 GPU 工时投入。

Whether specific downstream capabilities appear smoothly or emerge discontinuously with scale
([§§6–7](#6-emergent-capabilities-the-claim)) is a genuinely less settled question, and this module has deliberately presented Wei et
al.'s original claim and Schaeffer et al.'s metric-artifact critique side by side, as the current
state of an active, unresolved scientific debate rather than a closed textbook fact — exactly the
caveat this curriculum's citation policy requires when the literature itself has not settled.

至于具体的下游能力究竟是随规模平滑出现,还是不连续地“涌现”出来（[第 6 至 7 节](#6-emergent-capabilities-the-claim)），则是一个真正远未有定论的问题；本模块特意将 Wei 等人最初的说法与 Schaeffer 等人提出的“度量假象”批评并列呈现，把它作为一场仍在进行中、尚未有定论的科学争论的现状，而不是一条已经写进教科书、盖棺定论的事实来呈现——这正是本课程的引用规范在文献本身尚无定论时所要求的那种审慎态度。

---

## References

**参考文献**

### External Sources

- [Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J., and Amodei, D. (2020). Scaling Laws for Neural Language Models. arXiv:2001.08361.](https://arxiv.org/abs/2001.08361)
- [Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E., Cai, T., Rutherford, E., et al. (2022). Training Compute-Optimal Large Language Models. arXiv:2203.15556.](https://arxiv.org/abs/2203.15556)
- [Wei, J., Tay, Y., Bommasani, R., Raffel, C., Zoph, B., Borgeaud, S., Yogatama, D., Bosma, M., Zhou, D., Metzler, D., Chi, E. H., Hashimoto, T., Vinyals, O., Liang, P., Dean, J., and Fedus, W. (2022). Emergent Abilities of Large Language Models. arXiv:2206.07682.](https://arxiv.org/abs/2206.07682)
- [Schaeffer, R., Miranda, B., and Koyejo, S. (2023). Are Emergent Abilities of Large Language Models a Mirage? arXiv:2304.15004.](https://arxiv.org/abs/2304.15004)
- [Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., et al. (2020). Language Models Are Few-Shot Learners. arXiv:2005.14165.](https://arxiv.org/abs/2005.14165)

### Internal Cross-References

- [`introductory/02-the-transformer-architecture-and-attention.md`](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md) — the transformer architecture every model in every scaling-law study cited above was built on.
- [`intermediate/01-training-dynamics-optimization-and-generalization.md`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) — optimization and generalization, including the observation that classical capacity-based theory undershoots real deep-network behavior, a theme this module extends to the scale of frontier models.
- [`intermediate/05-advanced-prompting-cot-few-shot-structured-output.md`](https://anu00.dev/curriculum/intermediate/05-advanced-prompting-cot-few-shot-structured-output.md) — covers chain-of-thought prompting in depth; [§6](#6-emergent-capabilities-the-claim) above references its scale-dependent effectiveness as a specific example in the emergent-capabilities literature.
