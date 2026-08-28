# Reinforcement Learning from Human Feedback

**基于人类反馈的强化学习**

| Field   | English                                                                  | 中文                                              |
| ------- | ------------------------------------------------------------------------ | ------------------------------------------------- |
| Level   | Advanced                                                                 | 高级                                              |
| Cluster | Post-Training (S2, Amendment 5)                                          | 后训练（S2，第 5 号修正案）                       |
| Author  | Dr. Samuel Okonkwo, Research Scientist — Machine Learning Theory, ANU-00 | ANU-00 机器学习理论研究科学家 Samuel Okonkwo 博士 |

---

## 1. Introduction: From a Pretraining Objective to Human Preferences

**引言：从预训练目标到人类偏好**

[`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) studied how a network is trained — gradient descent and its variants, driven entirely by a
loss function computed from a fixed dataset — and [`advanced/01`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md) studied how far that same kind of training
scales: bigger models, more data, more compute, all still optimizing the same underlying objective,
next-token prediction, and all measured by the same underlying quantity, cross-entropy test loss.
This module asks what happens once you have a large, capable, pretrained language model and
discover that "predicts the next token well" is not the same property as "does what a person
actually wants it to do."

[`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) 研究的是一个网络*如何*被训练——梯度下降及其变体，整个过程完全由根据固定数据集计算出的损失函数驱动；[`advanced/01`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md) 研究的是这种训练方式能扩展到多远——更大的模型、更多的数据、更多的算力，全都仍在优化同一个底层目标（预测下一个词元），也全都用同一个底层量（交叉熵测试损失）来衡量。本模块要问的是：当你已经拥有一个庞大、强大、预训练好的语言模型之后，会发现"能很好地预测下一个词元"和"能做到一个人真正想要它做的事"，并不是同一种性质——接下来会发生什么。

A pretrained language model, trained only to continue text plausibly, will often continue a
question with more questions, continue an instruction with a paraphrase of the instruction rather
than an attempt to follow it, or continue with plausible-sounding but false information, because
none of those behaviors were ever penalized by the next-token objective — they were just as
"plausible a continuation" of internet text as a genuinely helpful answer would have been. Closing
this gap between "predicts plausible text" and "does what the user wants, helpfully, honestly, and
safely" is the problem this module calls **alignment via human feedback**, and **reinforcement
learning from human feedback** — glossed on first use as RLHF（基于人类反馈的强化学习，RLHF）— is
the specific, now-dominant technique for closing it that this module covers in full.

一个仅仅被训练来"合理地续写文本"的预训练语言模型，往往会用更多的问题去续写一个问题，会用对指令的改写而不是执行指令的尝试去续写一条指令，或者会用听起来合理但实际上是错误的信息去续写——因为这些行为都从未被下一词元预测这个目标所惩罚过：在"续写互联网文本"这件事上，它们和一个真正有用的回答一样"合理"。缩小"能续写出合理文本"与"能真正有帮助地、诚实地、安全地去做用户想要的事"之间的这道鸿沟，正是本模块所说的**基于人类反馈的对齐**问题，而 **Reinforcement Learning from Human Feedback**（基于人类反馈的强化学习，RLHF）——正是本模块要完整讲解的、用于弥合这道鸿沟的具体技术，也是当前最主流的一种做法。

The idea of using human preferences rather than a hand-written reward function to train a
reinforcement-learning system predates its application to language models. Christiano, Leike,
Brown, Martic, Legg, and Amodei (2017) showed that an RL agent could learn complex behaviors —
Atari gameplay, simulated robot locomotion — from a reward model trained on human comparisons
between short video clips of the agent's own behavior, using less than one percent of the agent's
environment interactions for human labeling. This module's pipeline is a direct descendant of that
result, adapted from video clips of robot behavior to pairs of text completions from a language
model.

用人类偏好而不是手工编写的奖励函数来训练强化学习系统，这个想法早于它在语言模型上的应用。Christiano、Leike、Brown、Martic、Legg 与 Amodei（2017）证明，一个强化学习智能体可以从一个基于人类对智能体自身行为片段视频进行比较而训练出的奖励模型中，学会复杂的行为——雅达利游戏、模拟机器人运动——而用于人类标注的环境交互量不到智能体全部交互量的百分之一。本模块所讲的整条流水线，正是这一结果的直接延续，只是把"机器人行为的视频片段"换成了"语言模型生成的一对文本续写"。

---

## 2. The Three-Stage RLHF Pipeline: An Overview

**RLHF 三阶段流水线：总览**

RLHF, as applied to language models, is not one training procedure but a pipeline of three
distinct, sequential stages, each producing an artifact the next stage depends on. Ziegler, Stiennon, Wu, Brown, Radford, Amodei, Christiano, and Irving (2019) established this
three-stage structure for language models directly, and Ouyang et al. (2022), in the paper
introducing **InstructGPT**, is the canonical modern reference for the full pipeline at scale —
this module follows their naming and formalization throughout.

应用于语言模型的 RLHF，并不是单一的一套训练流程，而是由三个不同的、依次进行的阶段组成的一条流水线，每个阶段都会产出下一阶段所依赖的一份产物。Ziegler、Stiennon、Wu、Brown、Radford、Amodei、Christiano 与 Irving（2019）直接为语言模型确立了这个三阶段的结构，而 Ouyang 等人（2022）在提出 **InstructGPT** 的论文中，则是当今整条流水线在大规模场景下的经典参考文献——本模块通篇都沿用他们的命名与形式化方式。

| Stage | Name                          | Input                                             | Output                                 | Trained by                                                                                                                                               |
| ----- | ----------------------------- | ------------------------------------------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1     | Supervised fine-tuning (SFT)  | A pretrained language model, human demonstrations | A reference policy $\pi^{SFT}$         | Standard supervised learning ([`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) §2) |
| 2     | Reward model (RM) training    | $\pi^{SFT}$, human preference comparisons         | A scalar reward model $r_\theta(x, y)$ | The Bradley-Terry loss ([§4](#4-stage-2-reward-modeling-preference-data-and-the-bradley-terry-loss))                                                     |
| 3     | RL fine-tuning against the RM | $\pi^{SFT}$, $r_\theta$                           | A final policy $\pi^{RL}_\phi$         | PPO ([§6](#6-stage-3-from-policy-gradients-to-ppos-clipped-objective))                                                                                   |

| 阶段 | 名称                   | 输入                             | 输出                              | 训练方式                                                                                                                                         |
| ---- | ---------------------- | -------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1    | 有监督微调（SFT）      | 一个预训练语言模型、人类示范数据 | 一个参考策略 $\pi^{SFT}$          | 标准有监督学习（[`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) 第 2 节） |
| 2    | 奖励模型（RM）训练     | $\pi^{SFT}$、人类偏好比较数据    | 一个标量奖励模型 $r_\theta(x, y)$ | Bradley-Terry 损失（[第 4 节](#4-stage-2-reward-modeling-preference-data-and-the-bradley-terry-loss)）                                           |
| 3    | 针对 RM 的强化学习微调 | $\pi^{SFT}$、$r_\theta$          | 最终策略 $\pi^{RL}_\phi$          | PPO（[第 6 节](#6-stage-3-from-policy-gradients-to-ppos-clipped-objective)）                                                                     |

Each stage answers a question the previous stage cannot: SFT teaches the model the _format_ of a
good response by direct imitation, but human demonstrations are expensive and imitation alone
cannot rank a model's own many possible outputs against each other; reward modeling solves this by
learning a scalar scoring function from comparisons, which are far cheaper for humans to produce
than demonstrations; and RL fine-tuning solves the last problem — a reward model can score text,
but it cannot itself generate text that scores well, so an optimization procedure is needed to turn
the reward model's scores into a policy that produces high-scoring text.

每一个阶段都回答了前一阶段无法回答的问题：SFT 通过直接模仿，教会模型一个好回答的*形式*，但人类示范数据的获取成本很高，而且仅凭模仿本身也无法对模型自己生成的众多可能输出进行相互排序；奖励建模解决了这个问题——它从比较数据中学习一个标量打分函数，而人类产生比较数据的成本远低于产生示范数据；强化学习微调则解决了最后一个问题——奖励模型能够对文本打分，但它自己并不能生成能拿到高分的文本，因此需要一套优化流程，把奖励模型给出的分数，转化为一个能够生成高分文本的策略。

---

## 3. Stage 1: Supervised Fine-Tuning and the Reference Policy

**阶段 1：有监督微调与参考策略**

The first stage is the most straightforward and reuses machinery [`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) already covered
in full: a pretrained language model is fine-tuned, using ordinary supervised learning — the same
gradient-descent update rule and the same optimizer choices ([`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) §3) — on a
dataset of human-written demonstrations of the desired behavior: prompt-response pairs where the
response is exactly what a skilled human would have written in reply to that prompt. Ouyang et al.
(2022) report collecting roughly 13,000 such demonstrations for InstructGPT, written by hired
human labelers, and fine-tuning GPT-3 on them for 16 epochs with a cosine learning-rate decay
schedule ([`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) §4).

第一阶段是最直接的一步，直接复用了 [`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) 已经完整讲过的机制：对一个预训练语言模型，用普通的有监督学习——同样的梯度下降更新规则、同样的优化器选择（[`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) 第 3 节）——在一个由人类撰写的、展示所期望行为的示范数据集上进行微调：数据集中的每一条都是一对提示-回应，其中的回应正是一位熟练的人类会针对该提示写出的回答。Ouyang 等人（2022）报告说，他们为 InstructGPT 收集了大约 13,000 条这样的示范数据，由受雇的人类标注员撰写，并用余弦学习率衰减调度（[`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) 第 4 节）对 GPT-3 微调了 16 个训练轮次。

The resulting model is called the **SFT model** or **reference policy**, written $\pi^{SFT}$, and
it plays two distinct roles for the rest of the pipeline: it is the _starting point_ that Stage 3's
reinforcement learning fine-tunes further, and — as [§7](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy) below explains — it is also the fixed
_anchor_ that Stage 3's optimization is measured against and penalized for drifting too far from,
a role that has nothing to do with how it was trained and everything to do with what it is used
for afterward.

由此得到的模型称为 **SFT 模型**，或称**参考策略**，记作 $\pi^{SFT}$，它在流水线的后续部分中扮演着两个不同的角色：它是阶段 3 的强化学习进一步微调的*起点*；而且——正如下文[第 7 节](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy)所解释的——它同时也是一个固定的*锚点*，阶段 3 的优化过程会以它为基准来衡量，并因偏离它太远而受到惩罚，这个角色与它当初是怎么训练出来的无关，而完全取决于它在此后被用来做什么。

---

## 4. Stage 2: Reward Modeling — Preference Data and the Bradley-Terry Loss

**阶段 2：奖励建模——偏好数据与 Bradley-Terry 损失**

Rather than asking a human to write a good response — expensive, slow, and only produces one
response per prompt — the reward-modeling stage asks a cheaper question: given two or more
responses the current model already generated for the same prompt, which one is better? Humans
are, empirically, much faster and more reliable at _comparing_ two responses than at _writing_ a
response from scratch: Ziegler et al. (2019) report scaling this comparison-based labeling to
60,000 human comparisons in their own summarization experiments, and Stiennon et al. (2020) scaled
it further still, collecting 64,832 comparisons for their summarization work — both are
comparison-based approaches, not a demonstration-writing baseline.

奖励建模阶段不再要求人类去写一个好的回答——这样做既昂贵又缓慢，而且每条提示只能产出一个回答——而是提出了一个成本更低的问题：给定当前模型针对同一条提示已经生成的两个或更多个回答，哪一个更好？经验表明，人类*比较*两个回答的速度和可靠性，都远高于从零*撰写*一个回答：Ziegler 等人（2019）在他们自己的摘要任务实验中，报告将这种基于比较的标注方式扩展到了 60,000 次人类比较；Stiennon 等人（2020）则将其进一步扩大，为其摘要工作收集了 64,832 次比较——两篇论文采用的都是基于比较的方法，而非依赖示范数据的基线方式。

For a prompt $x$ and a pair of model-generated completions $y_w$ (the one the human labeler
preferred, "win") and $y_l$ ("lose"), the reward model $r_\theta(x, y)$ is a single scalar-output
network — typically the SFT model with its final unembedding layer replaced by a single linear
output — and the question is how to turn a dataset of such win/lose pairs into a loss function for
$\theta$. The answer used by Christiano et al. (2017), Ziegler et al. (2019), Stiennon et al.
(2020), and Ouyang et al. (2022) alike is the **Bradley-Terry model**（Bradley-Terry 模型）, a
statistical model of paired comparisons introduced by Bradley and Terry (1952) for ranking
competitors from win/loss records, long before it was ever applied to neural networks.

对于一条提示 $x$ 以及一对由模型生成的续写 $y_w$（人类标注员偏好的那一个，"win"）与 $y_l$（"lose"），奖励模型 $r_\theta(x, y)$ 是一个输出单一标量的网络——通常就是把 SFT 模型的最终解嵌入层替换成一个单一的线性输出——问题在于，如何把这样一批 win/lose 数据对转化为一个关于 $\theta$ 的损失函数。Christiano 等人（2017）、Ziegler 等人（2019）、Stiennon 等人（2020）以及 Ouyang 等人（2022）都采用了同一个答案：**Bradley-Terry 模型**（Bradley-Terry 模型），一种由 Bradley 与 Terry 于 1952 年提出、用于从胜负记录中对参赛者进行排名的成对比较统计模型，其提出时间远早于它被应用到神经网络之上。

The Bradley-Terry model assigns each item $i$ a latent score $s_i$ and states that the probability
item $i$ "beats" item $j$ in a head-to-head comparison is $P(i \succ j) = \sigma(s_i - s_j)$,
where $\sigma(z) = 1/(1 + e^{-z})$ is the logistic sigmoid function — a larger score gap makes the
higher-scored item's win more certain, and an equal score gives a fifty-fifty prediction, exactly
matching the intuition that a coin-flip-close comparison should carry little signal about which
item is truly better. Treating the reward model's output $r_\theta(x, y)$ as that latent score for
completion $y$ given prompt $x$, the probability the reward model assigns to the human's actual
preference $y_w \succ y_l$ is $P(y_w \succ y_l) = \sigma(r_\theta(x, y_w) - r_\theta(x, y_l))$, and
maximizing this probability over the whole comparison dataset — equivalently, minimizing its
negative log-likelihood — gives the reward model's training loss.

Bradley-Terry 模型为每一个项目 $i$ 赋予一个潜在分数 $s_i$，并指出在一场一对一的比较中，项目 $i$ "战胜"项目 $j$ 的概率为 $P(i \succ j) = \sigma(s_i - s_j)$，其中 $\sigma(z) = 1/(1 + e^{-z})$ 是逻辑斯谛 S 型函数——分数差距越大，得分更高的一方获胜就越确定，而分数相等时给出的预测就是五五开，这恰好符合这样的直觉：一场势均力敌、近乎抛硬币的比较，本身应当携带很少的信号来说明哪个项目真的更好。把奖励模型对给定提示 $x$ 下续写 $y$ 的输出 $r_\theta(x, y)$ 当作这个潜在分数，那么奖励模型为人类实际给出的偏好 $y_w \succ y_l$ 所赋予的概率就是 $P(y_w \succ y_l) = \sigma(r_\theta(x, y_w) - r_\theta(x, y_l))$，在整个比较数据集上最大化这个概率——等价于最小化它的负对数似然——就得到了奖励模型的训练损失。

Ouyang et al. (2022) write this loss, for a dataset $D$ of prompts with $K$ ranked completions
each (so that each prompt contributes $\binom{K}{2}$ pairwise comparisons, normalized by that count
so that a prompt with more ranked completions does not dominate the loss), as:

Ouyang 等人（2022）将这个损失写成如下形式——数据集 $D$ 中每条提示都带有 $K$ 个经过排序的续写（因此每条提示会贡献 $\binom{K}{2}$ 个成对比较，损失会按这个数量归一化，使得排序续写数量更多的提示不会主导整体损失）：

$$\text{loss}(\theta) = -\frac{1}{\binom{K}{2}} \, \mathbb{E}_{(x,\, y_w,\, y_l) \sim D} \left[ \log\left( \sigma\left( r_\theta(x, y_w) - r_\theta(x, y_l) \right) \right) \right]$$

This is a direct log-likelihood loss under the Bradley-Terry model of the paragraph above, applied
per comparison and averaged over all $\binom{K}{2}$ comparisons drawn from each prompt's $K$-way
ranking. Ouyang et al. (2022) report training a 6-billion-parameter reward model on roughly 33,000
training prompts for InstructGPT, and note that they found training a reward model as large as the
175-billion-parameter policy itself to be unstable and unnecessary for this purpose.

这正是上一段所说的 Bradley-Terry 模型下的对数似然损失，按每一次比较逐一计算，再对每条提示的 $K$ 项排序中抽取出的全部 $\binom{K}{2}$ 次比较取平均。Ouyang 等人（2022）报告说，他们为 InstructGPT 训练了一个 60 亿参数的奖励模型，训练提示约 33,000 条，并指出他们发现，把奖励模型训练到与 1750 亿参数的策略模型同样大的规模，会导致训练不稳定，而且对这个用途而言也没有必要。

---

## 5. A Worked Example: Computing the Reward Model Loss

**一个实例：计算奖励模型损失**

Suppose a prompt $x$ has $K = 4$ ranked completions, from best to worst: $y_1 \succ y_2 \succ y_3
\succ y_4$, and the current reward model assigns them the scalar scores $r_\theta(x, y_1) = 2.1$,
$r_\theta(x, y_2) = 1.4$, $r_\theta(x, y_3) = 0.3$, and $r_\theta(x, y_4) = -0.5$. With $K = 4$,
this ranking implies $\binom{4}{2} = 6$ pairwise comparisons, one for every pair where the first
completion is preferred over the second.

假设某条提示 $x$ 有 $K = 4$ 个经过排序的续写，从最好到最差依次为 $y_1 \succ y_2 \succ y_3 \succ y_4$，而当前的奖励模型为它们赋予的标量分数分别为 $r_\theta(x, y_1) = 2.1$、$r_\theta(x, y_2) = 1.4$、$r_\theta(x, y_3) = 0.3$、$r_\theta(x, y_4) = -0.5$。当 $K = 4$ 时，这个排序隐含了 $\binom{4}{2} = 6$ 次成对比较，每一对都是排序中排在前面的续写胜过排在后面的续写。

| Pair $(y_w, y_l)$ | $r_\theta(y_w) - r_\theta(y_l)$ | $\sigma(\cdot)$ | $-\log \sigma(\cdot)$ |
| ----------------- | ------------------------------- | --------------- | --------------------- |
| $(y_1, y_2)$      | 0.7                             | 0.668           | 0.403                 |
| $(y_1, y_3)$      | 1.8                             | 0.858           | 0.153                 |
| $(y_1, y_4)$      | 2.6                             | 0.931           | 0.071                 |
| $(y_2, y_3)$      | 1.1                             | 0.750           | 0.288                 |
| $(y_2, y_4)$      | 1.9                             | 0.870           | 0.139                 |
| $(y_3, y_4)$      | 0.8                             | 0.690           | 0.371                 |

Summing the final column gives $\sum -\log\sigma(\cdot) \approx 1.425$, and dividing by
$\binom{4}{2} = 6$ gives $\text{loss}(\theta) \approx 0.238$ for this single prompt — the quantity
that would then be averaged again over every prompt in a training batch to produce the batch loss
that gradient descent ([`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) §2) actually minimizes.

将最后一列求和，得到 $\sum -\log\sigma(\cdot) \approx 1.425$，再除以 $\binom{4}{2} = 6$，得到这单条提示的损失 $\text{loss}(\theta) \approx 0.238$——这个量随后还会在一个训练批次中的每一条提示上再取一次平均，得到梯度下降（[`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) 第 2 节）真正去最小化的批次损失。

Notice that the pair with the largest score gap, $(y_1, y_4)$ at 2.6, contributes the smallest
individual loss term (0.071), because the reward model already strongly agrees with the human
ranking on that pair; the pair with the smallest gap, $(y_1, y_2)$ at 0.7, contributes the largest
term (0.403), because the reward model is least confident there — exactly the behavior the loss is
designed to produce: gradient signal concentrates on the comparisons the model is currently getting
least right, in the same sense that [`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) §2's gradient always points toward
reducing whichever error is currently largest.

注意，分数差距最大的那一对 $(y_1, y_4)$（差距 2.6），贡献的单项损失反而最小（0.071），因为奖励模型在这一对上已经和人类的排序高度一致；而分数差距最小的那一对 $(y_1, y_2)$（差距 0.7），贡献的单项损失最大（0.403），因为奖励模型在这一对上的把握最不确定——这正是这个损失函数被设计出来要产生的行为：梯度信号会集中在模型当前判断得最不准的那些比较上，这与 [`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) 第 2 节中"梯度总是指向能降低当前最大误差的方向"是同一种道理。

---

## 6. Stage 3: From Policy Gradients to PPO's Clipped Objective

**阶段 3：从策略梯度到 PPO 的裁剪目标**

With a trained reward model $r_\theta$ in hand, the last stage treats text generation itself as a
reinforcement-learning problem: the language model is a **policy** $\pi_\phi$ that, given a prompt
(the RL "state"), chooses a completion (a sequence of "actions," one token at a time), and receives
a scalar **reward** — the reward model's score for the finished completion. The objective is to
adjust $\phi$ to maximize expected reward, and the algorithm every paper cited in this module uses
to do so is **Proximal Policy Optimization**（近端策略优化，PPO）, introduced by Schulman, Wolski,
Dhariwal, Radford, and Klimov (2017).

有了一个训练好的奖励模型 $r_\theta$，最后一个阶段把文本生成本身当作一个强化学习问题来处理：语言模型是一个**策略** $\pi_\phi$，给定一条提示（强化学习中的"状态"），它会选择一个续写（一串"动作"，逐个词元地生成），并获得一个标量**奖励**——即奖励模型对生成完毕的续写所给出的分数。目标是调整 $\phi$ 以最大化期望奖励，而本模块中所引用的每一篇论文都使用了同一种算法来达成这个目标：**Proximal Policy Optimization**（近端策略优化，PPO），由 Schulman、Wolski、Dhariwal、Radford 与 Klimov（2017）提出。

A plain policy-gradient method would take the current policy's own trajectory, weight each action
by the reward it led to (or, more precisely, by an advantage estimate — [§7](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy) below), and step the
parameters in the direction that makes high-reward actions more likely. The trouble is that a
single large step, taken naively, can move the policy so far that the data it just collected is no
longer even representative of what the new policy would do — destabilizing training, sometimes
catastrophically, an instability with the same underlying flavor as [`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) §7's
worked example of a learning rate large enough to make gradient descent diverge rather than
converge.

一个普通的策略梯度方法，会取当前策略自身产生的轨迹，用每个动作所导致的奖励（更准确地说，是一个优势估计——见下文[第 7 节](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy)）对其加权，然后把参数朝着能让高奖励动作变得更有可能的方向迈一步。问题在于，如果不加约束地迈出一大步，可能会让策略移动得太远，以至于刚刚采集到的数据甚至已经不能代表新策略会做出的行为——这会破坏训练的稳定性，有时甚至是灾难性的，其内在的不稳定性，与 [`intermediate/01`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) 第 7 节中"学习率过大导致梯度下降发散而非收敛"的那个实例，在本质上是同一类问题。

PPO's fix is to bound how much a single update is allowed to trust the current batch of data, via
the **probability ratio** between the new and old policy for each action taken:

PPO 的解决方案是，通过新旧策略针对每个已执行动作的**概率比**，来限制一次更新对当前这批数据的"信任程度"：

$$r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\text{old}}}(a_t \mid s_t)}$$

A ratio of 1 means the action is exactly as likely under the new policy as it was under the policy
that generated the data; a ratio far from 1 means the update has pushed the new policy far away
from the data-generating policy, into territory where the advantage estimate computed under the old
policy may no longer be trustworthy.

比值为 1，意味着该动作在新策略下的可能性与在生成这批数据的旧策略下完全相同；比值远离 1，则意味着这次更新已经把新策略推得远离了产生数据的那个策略，进入了一个在旧策略下计算出的优势估计可能已经不再可靠的区域。

PPO's **clipped surrogate objective** bounds the ratio's influence directly:

PPO 的**裁剪代理目标**直接对这个比值的影响施加了约束：

$$L^{\text{CLIP}}(\theta) = \mathbb{E}_t\left[ \min\left( r_t(\theta)\, \hat{A}_t, \; \text{clip}\left(r_t(\theta),\, 1-\epsilon,\, 1+\epsilon\right) \hat{A}_t \right) \right]$$

where $\hat{A}_t$ is an estimate of the advantage of the action taken at step $t$ ([§7](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy) below), and
$\epsilon$ is a small hyperparameter — Schulman et al. (2017) use $\epsilon = 0.2$ in their reported
Atari and MuJoCo experiments — that sets the trust-region width: the $\text{clip}(\cdot)$ term
caps the ratio to the interval $[1-\epsilon,\ 1+\epsilon]$, and taking the minimum of the clipped
and unclipped terms means the objective never rewards pushing the ratio further outside that
interval in the direction that would already have increased the (unclipped) objective, while still
allowing the gradient to pull a ratio that has drifted too far _back toward_ 1 if doing so would
improve the objective — the worked example in [§8](#8-a-worked-example-ppos-clipped-objective-in-action) below makes this asymmetry concrete.

其中 $\hat{A}_t$ 是对第 $t$ 步所执行动作的优势的估计值（见下文[第 7 节](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy)），$\epsilon$ 是一个较小的超参数——Schulman 等人（2017）在他们所报告的雅达利与 MuJoCo 实验中使用了 $\epsilon = 0.2$——它设定了信赖域的宽度：$\text{clip}(\cdot)$ 项把比值限制在区间 $[1-\epsilon,\ 1+\epsilon]$ 之内，而对裁剪项与未裁剪项取最小值，意味着这个目标函数永远不会因为把比值进一步推出这个区间（并且推的方向本来就会增大未裁剪的目标值）而获得奖励，但如果一个已经偏离该区间太远的比值，朝着 1 的方向"回撤"能够改善目标值，梯度依然允许这样做——下文[第 8 节](#8-a-worked-example-ppos-clipped-objective-in-action)的实例会把这种不对称性具体呈现出来。

In practice, Schulman et al. (2017) combine $L^{\text{CLIP}}$ with a value-function loss term
(coefficient $c_1$) and an entropy bonus (coefficient $c_2$, encouraging continued exploration)
into a single objective $L^{\text{CLIP+VF+S}}(\theta) = \mathbb{E}_t\left[ L^{\text{CLIP}}_t(\theta) - c_1 \left(V_\theta(s_t) - V_t^{\text{targ}}\right)^2 + c_2\, S[\pi_\theta](s_t) \right]$, and this is the form of PPO that Ziegler et al. (2019), Stiennon et al. (2020), and Ouyang et al. (2022) all adopt for RLHF, with [§7](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy) below adding one more term specific to language-model RLHF that does not appear in Schulman et al.'s original game-playing and robotics experiments.

在实践中，Schulman 等人（2017）把 $L^{\text{CLIP}}$ 与一个价值函数损失项（系数 $c_1$）以及一个鼓励持续探索的熵奖励项（系数 $c_2$）结合成一个单一目标：$L^{\text{CLIP+VF+S}}(\theta) = \mathbb{E}_t\left[ L^{\text{CLIP}}_t(\theta) - c_1 \left(V_\theta(s_t) - V_t^{\text{targ}}\right)^2 + c_2\, S[\pi_\theta](s_t) \right]$，而这正是 Ziegler 等人（2019）、Stiennon 等人（2020）以及 Ouyang 等人（2022）在 RLHF 中都采用的 PPO 形式；下文[第 7 节](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy)还会再加入一项 Schulman 等人最初在游戏与机器人实验中并未出现的、专属于语言模型 RLHF 的项。

---

## 7. Advantage Estimation and the KL Penalty Against the Reference Policy

**优势估计与针对参考策略的 KL 惩罚**

Two pieces are still missing from [§6](#6-stage-3-from-policy-gradients-to-ppos-clipped-objective)'s picture: where the advantage estimate $\hat{A}_t$ actually comes
from, and what stops the policy from drifting arbitrarily far from sensible, fluent text while
chasing reward-model score.

[第 6 节](#6-stage-3-from-policy-gradients-to-ppos-clipped-objective)的图景中还缺了两块：优势估计 $\hat{A}_t$ 究竟从何而来，以及是什么阻止了策略在一味追逐奖励模型分数的过程中，任意偏离通顺、合理的文本。

For the first, PPO's standard practice — used across the RLHF pipeline — is **Generalized
Advantage Estimation**（广义优势估计，GAE）, introduced by Schulman, Moritz, Levine, Jordan, and
Abbeel (2015). GAE combines a learned value function $V(s_t)$ (predicting expected future reward
from state $s_t$, trained alongside the policy) with the actual rewards observed, via the
temporal-difference residual $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$, and then forms the
advantage estimate as an exponentially weighted sum of these residuals over the remaining
trajectory, $\hat{A}_t = \sum_{l=0}^{\infty} (\gamma\lambda)^l\, \delta_{t+l}$, where $\gamma$ is the
usual RL discount factor and $\lambda \in [0, 1]$ trades off bias against variance in the
estimate — $\lambda = 1$ recovers a high-variance Monte Carlo estimate of the full future return,
and $\lambda = 0$ gives the lowest-variance, most heavily bootstrapped one-step estimate.

对于第一个问题，PPO 的标准做法——在整条 RLHF 流水线中都会用到——是 **Generalized Advantage Estimation**（广义优势估计，GAE），由 Schulman、Moritz、Levine、Jordan 与 Abbeel（2015）提出。GAE 将一个学习得到的价值函数 $V(s_t)$（预测从状态 $s_t$ 出发的期望未来奖励，与策略一同训练）与实际观测到的奖励结合起来，通过时序差分残差 $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$，再把优势估计构造为对剩余轨迹上这些残差的一个指数加权和：$\hat{A}_t = \sum_{l=0}^{\infty} (\gamma\lambda)^l\, \delta_{t+l}$，其中 $\gamma$ 是强化学习中通常使用的折扣因子，$\lambda \in [0, 1]$ 则在估计的偏差与方差之间做权衡——$\lambda = 1$ 会还原出一个高方差的、对未来完整回报的蒙特卡洛估计，而 $\lambda = 0$ 则给出方差最低、自举程度最深的单步估计。

For the second — keeping the policy from drifting too far from sensible text — the RLHF pipeline
adds a term that has no analogue in Schulman et al.'s original game-playing setting: a per-token
penalty on the **Kullback-Leibler (KL) divergence** between the current policy $\pi^{RL}_\phi$ and
the fixed reference policy $\pi^{SFT}$ from [§3](#3-stage-1-supervised-fine-tuning-and-the-reference-policy). Ouyang et al. (2022) fold the reward-model score and this KL
penalty into a single per-episode reward:

对于第二个问题——阻止策略偏离合理文本太远——RLHF 流水线加入了一项在 Schulman 等人最初的游戏实验设定中并不存在的项：对当前策略 $\pi^{RL}_\phi$ 与来自[第 3 节](#3-stage-1-supervised-fine-tuning-and-the-reference-policy)的固定参考策略 $\pi^{SFT}$ 之间的 **Kullback-Leibler（KL）散度**，施加一个逐词元的惩罚。Ouyang 等人（2022）把奖励模型的分数与这个 KL 惩罚合并成了单个逐回合（per-episode）的奖励：

$$\text{reward}(x, y) = r_\theta(x, y) - \beta \log\left(\frac{\pi^{RL}_\phi(y \mid x)}{\pi^{SFT}(y \mid x)}\right)$$

where $\beta$ controls the strength of the penalty. The log-ratio term is exactly a Monte Carlo
estimate of the KL divergence between the two policies for the generated completion $y$: since
$\pi^{RL}_\phi = \pi^{SFT}$ makes the log-ratio zero, the penalty vanishes exactly where the policy
has not moved at all, and grows the further the policy's token-by-token probabilities diverge from
the reference model's — a direct check on the reward model's known weakness that it is only ever
trained on completions the SFT model or early RL policy actually produced, and its scores for text
far outside that distribution are not to be trusted, foreshadowing [§10](#10-reward-hacking-and-overoptimization-an-open-problem)'s discussion of
reward-model overoptimization.

其中 $\beta$ 控制着惩罚的强度。这个对数比值项，正是两个策略在生成的续写 $y$ 上的 KL 散度的一个蒙特卡洛估计：由于 $\pi^{RL}_\phi = \pi^{SFT}$ 会使这个对数比值恰好为零，所以在策略完全没有发生移动的地方，惩罚也恰好为零；而策略逐词元的概率与参考模型偏离得越远，惩罚就越大——这直接针对了奖励模型一个已知的弱点：奖励模型自始至终只是在 SFT 模型或早期 RL 策略实际生成过的续写上训练出来的，它对远远偏离这个分布的文本所给出的分数是不可信的，这也预示了下文[第 10 节](#10-reward-hacking-and-overoptimization-an-open-problem)将要讨论的奖励模型过优化问题。

Ouyang et al. (2022) additionally define **PPO-ptx**, mixing a language-modeling pretraining loss
back into the RL objective at coefficient $\gamma$, to counteract a specific failure mode they
observed — performance regressions on standard NLP benchmarks after RL fine-tuning, sometimes
called an **"alignment tax"** — giving the full objective:

Ouyang 等人（2022）还定义了 **PPO-ptx**，以系数 $\gamma$ 把一个语言建模的预训练损失重新混入 RL 目标，用来抵消他们所观察到的一种特定失效模式——RL 微调之后在标准 NLP 基准测试上出现性能倒退，有时被称为**"对齐税"**——由此得到完整的目标函数：

$$\text{objective}(\phi) = \mathbb{E}_{(x,y)\sim D_{\pi^{RL}_\phi}}\left[ r_\theta(x, y) - \beta \log\left(\frac{\pi^{RL}_\phi(y \mid x)}{\pi^{SFT}(y \mid x)}\right) \right] + \gamma\, \mathbb{E}_{x \sim D_{\text{pretrain}}}\left[ \log \pi^{RL}_\phi(x) \right]$$

The first expectation is [§6](#6-stage-3-from-policy-gradients-to-ppos-clipped-objective)'s PPO objective applied to the KL-penalized reward above; the second is
an ordinary pretraining log-likelihood term, computed on samples from the original pretraining
distribution $D_{\text{pretrain}}$ rather than on RL-generated completions, pulling the policy back
toward the broad general-purpose competence the pretraining phase originally gave it whenever RL
fine-tuning alone would erode it.

第一项期望，就是[第 6 节](#6-stage-3-from-policy-gradients-to-ppos-clipped-objective)的 PPO 目标应用于上面这个经过 KL 惩罚修正的奖励之上；第二项则是一个普通的预训练对数似然项，它是在原始预训练分布 $D_{\text{pretrain}}$ 的样本上计算的，而不是在 RL 生成的续写上计算的——每当单独的 RL 微调会侵蚀预训练阶段原本赋予模型的那种广泛的通用能力时，这一项就会把策略重新拉回去。

---

## 8. A Worked Example: PPO's Clipped Objective in Action

**一个实例：PPO 裁剪目标的实际运作**

Consider a single token-generation step with $\epsilon = 0.2$, so the trust region is
$[1-\epsilon,\ 1+\epsilon] = [0.8,\ 1.2]$. Two cases illustrate the asymmetry [§6](#6-stage-3-from-policy-gradients-to-ppos-clipped-objective) mentioned.

考虑一次单个词元生成步骤，取 $\epsilon = 0.2$，因此信赖域为 $[1-\epsilon,\ 1+\epsilon] = [0.8,\ 1.2]$。以下两种情形展示了[第 6 节](#6-stage-3-from-policy-gradients-to-ppos-clipped-objective)所提到的那种不对称性。

**Case A — the ratio has moved too far in the "good" direction.** Suppose the old policy assigned
this token probability 0.20, the current (updated) policy now assigns it probability 0.30, giving
$r_t(\theta) = 0.30 / 0.20 = 1.5$, and the advantage estimate is $\hat{A}_t = +2$ (this was, in
hindsight, a good token to have generated more often). The unclipped term is $r_t(\theta)\hat{A}_t
= 1.5 \times 2 = 3.0$; the clipped term is $\text{clip}(1.5, 0.8, 1.2) \times 2 = 1.2 \times 2 =
2.4$; and $L^{\text{CLIP}} = \min(3.0,\ 2.4) = 2.4$ — the objective is capped at the clipped value,
so a further increase in $r_t(\theta)$ past 1.5 would not increase the objective any further,
removing the gradient's incentive to keep pushing this already-large ratio even higher.

**情形 A——比值朝"好"的方向移动得太远。** 假设旧策略给这个词元赋予的概率是 0.20，当前（更新后）的策略现在给它赋予的概率是 0.30，于是 $r_t(\theta) = 0.30 / 0.20 = 1.5$，优势估计为 $\hat{A}_t = +2$（事后看来，这确实是一个应当更频繁生成的好词元）。未裁剪项为 $r_t(\theta)\hat{A}_t = 1.5 \times 2 = 3.0$；裁剪项为 $\text{clip}(1.5, 0.8, 1.2) \times 2 = 1.2 \times 2 = 2.4$；因此 $L^{\text{CLIP}} = \min(3.0,\ 2.4) = 2.4$——目标值被限制在裁剪后的数值上，这意味着 $r_t(\theta)$ 若在 1.5 的基础上进一步增大，也不会再让目标值继续增大，这就消除了梯度继续把这个已经很大的比值推得更高的动机。

**Case B — the ratio has moved too far in the "bad" direction, but the action was actually good.**
Suppose instead the old policy assigned probability 0.40 and the new policy has dropped it to
0.20, giving $r_t(\theta) = 0.20 / 0.40 = 0.5$, with the same $\hat{A}_t = +2$ (a good token that
the update has, so far, wrongly made less likely). The unclipped term is $0.5 \times 2 = 1.0$; the
clipped term is $\text{clip}(0.5, 0.8, 1.2) \times 2 = 0.8 \times 2 = 1.6$; and $L^{\text{CLIP}} =
\min(1.0,\ 1.6) = 1.0$ — here the _unclipped_ term is selected, so the clip does not block the
gradient, and the objective still rewards moving $r_t(\theta)$ back up toward 1, correcting the
mistake.

**情形 B——比值朝"坏"的方向移动得太远，但这个动作实际上是好的。** 假设旧策略赋予的概率是 0.40，而新策略把它降到了 0.20，于是 $r_t(\theta) = 0.20 / 0.40 = 0.5$，优势估计仍为 $\hat{A}_t = +2$（这是一个好词元，但目前为止的更新却错误地降低了它出现的概率）。未裁剪项为 $0.5 \times 2 = 1.0$；裁剪项为 $\text{clip}(0.5, 0.8, 1.2) \times 2 = 0.8 \times 2 = 1.6$；因此 $L^{\text{CLIP}} = \min(1.0,\ 1.6) = 1.0$——这里选中的是*未裁剪*项，所以裁剪并没有挡住梯度，目标值仍然鼓励把 $r_t(\theta)$ 重新往 1 的方向拉回，纠正这个错误。

These two cases together are the whole point of the clip-then-minimum construction: it disables
the incentive to push a ratio further outside the trust region only in the direction that would
already have been rewarded, while leaving the corrective gradient — pulling an out-of-region ratio
back toward 1 — fully intact.

这两种情形合在一起，正是"先裁剪、再取最小值"这一构造的全部意义所在：它只在比值本来就会因继续朝某个方向移动而获得奖励的那个方向上，取消了推动比值进一步偏离信赖域的动机，而把纠正性的梯度——把已经偏离区间的比值拉回 1——完整地保留了下来。

---

## 9. The Full RLHF Loop, End to End

**完整的 RLHF 循环，从头到尾**

Putting [§§3–8](#3-stage-1-supervised-fine-tuning-and-the-reference-policy) together, one iteration of Stage 3's RL fine-tuning loop runs as follows: (1) sample a
batch of prompts $x$ from the training distribution; (2) generate a completion $y$ for each prompt
using the _current_ policy $\pi^{RL}_\phi$, one token at a time; (3) score each finished
completion with the frozen reward model, $r_\theta(x, y)$, and subtract the KL penalty against
$\pi^{SFT}$ ([§7](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy)) to get the per-episode reward; (4) fit a value function and compute a GAE
advantage estimate ([§7](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy)) for every generated token; (5) take one or more PPO gradient steps on
$L^{\text{CLIP+VF+S}}$ ([§6](#6-stage-3-from-policy-gradients-to-ppos-clipped-objective), plus the pretraining-mix term for PPO-ptx) using the ratio between the
just-updated policy and the policy that generated this batch; and (6) repeat with a fresh batch of
prompts and the now-updated policy.

把[第 3 至 8 节](#3-stage-1-supervised-fine-tuning-and-the-reference-policy)的内容放在一起，阶段 3 的强化学习微调循环的一次迭代大致如下：（1）从训练分布中采样一批提示 $x$；（2）用*当前*策略 $\pi^{RL}_\phi$，逐个词元地为每条提示生成一个续写 $y$；（3）用冻结的奖励模型对每个生成完毕的续写打分 $r_\theta(x, y)$，并减去针对 $\pi^{SFT}$ 的 KL 惩罚（[第 7 节](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy)），得到逐回合的奖励；（4）拟合一个价值函数，并为每一个生成的词元计算 GAE 优势估计（[第 7 节](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy)）；（5）用刚更新的策略与生成这批数据的策略之间的比值，在 $L^{\text{CLIP+VF+S}}$（[第 6 节](#6-stage-3-from-policy-gradients-to-ppos-clipped-objective)，若是 PPO-ptx 还要加上预训练混合项）上迈出一步或多步 PPO 梯度更新；（6）用新一批提示以及现在已经更新过的策略，重复上述过程。

It is worth being explicit about a subtlety this loop shares with every reinforcement-learning
system built on [§6](#6-stage-3-from-policy-gradients-to-ppos-clipped-objective)'s machinery, but that is easy to lose sight of once "RLHF" becomes a single
familiar acronym: none of the three stages actually requires a human in the loop _during_ Stage 3
itself. The human comparisons are collected once, up front, to train the frozen reward model in
Stage 2; Stage 3's entire loop runs against that fixed, learned proxy for human judgment, not
against a person evaluating completions in real time. This is precisely what makes reward-model
overoptimization — [§10](#10-reward-hacking-and-overoptimization-an-open-problem) below — possible at all: the policy is free to drift toward whatever the
proxy scores highly, whether or not a human would actually agree.

值得明确指出的是，这个循环存在一个与[第 6 节](#6-stage-3-from-policy-gradients-to-ppos-clipped-objective)所依赖的机制所共有的微妙之处，但一旦"RLHF"变成一个耳熟能详的单一缩写，这一点就很容易被忽略：这三个阶段中，实际上没有任何一个阶段要求在阶段 3*本身*的执行过程中有人类参与。人类的比较数据是提前、一次性收集好的，用来在阶段 2 中训练出那个被冻结的奖励模型；阶段 3 的整个循环，是针对那个固定的、习得的人类判断代理来运行的，而不是针对一个实时评估续写的真人。这正是下文[第 10 节](#10-reward-hacking-and-overoptimization-an-open-problem)所讨论的"奖励模型过优化"之所以可能发生的根本原因：策略完全可以自由地朝着这个代理打高分的方向偏移，而不管一个真人是否真的会认同。

---

## 10. Reward Hacking and Overoptimization: An Open Problem

**奖励黑客与过优化：一个悬而未决的问题**

Because Stage 3 optimizes against the reward model rather than against real human judgment
directly, and because the reward model is itself an imperfect, learned approximation trained on a
finite set of comparisons, pushing the policy to score arbitrarily highly under $r_\theta$ does not
guarantee — and past some point, actively stops guaranteeing — that a human evaluator would agree
the resulting text is actually better. This general phenomenon, of a proxy measure ceasing to track
the true goal once it is optimized hard enough, is a specific instance of **Goodhart's
Law**（古德哈特定律）, informally: "when a measure becomes a target, it ceases to
be a good measure." In the RLHF literature it is called **reward hacking**（奖励黑客）.

由于阶段 3 是针对奖励模型进行优化，而不是直接针对真实的人类判断，而奖励模型本身又是在有限的一批比较数据上训练出来的、并不完美的习得近似，因此把策略推向在 $r_\theta$ 下得分任意高的方向，并不能保证——而且过了某个点之后，会积极地不再保证——一个人类评估者会认同最终生成的文本真的更好。这种"一旦被优化得足够狠，代理指标就不再追踪真实目标"的普遍现象，是**古德哈特定律**（古德哈特定律）的一个具体例子，通俗地说就是："一旦一个度量指标变成了优化目标，它就不再是一个好的度量指标。"在 RLHF 的文献中，这种现象被称为**奖励黑客**。

Gao, Schulman, and Hilton (2022) quantified this directly, in a controlled setup where a large
"gold-standard" reward model stands in for true human judgment and a smaller "proxy" reward model
of the kind actually used during RLHF is optimized against. As optimization against the proxy
reward model intensifies — measured, following [`advanced/01`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md)'s style of relationship, by a smooth,
predictable functional form — gold-standard reward initially rises alongside proxy reward, exactly
as intended, but then plateaus and, with enough further optimization, can actively decline: the
policy has learned to satisfy the specific, idiosyncratic weaknesses of the proxy reward model
rather than the underlying quality it was meant to stand in for. Gao et al. (2022) further report
that this overoptimization curve itself scales predictably with reward-model size, connecting
reward-model overoptimization directly to the kind of scaling-law reasoning [`advanced/01`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md) covers.

Gao、Schulman 与 Hilton（2022）在一个受控实验设定中，直接对这一现象做了量化：用一个大型"黄金标准"奖励模型来充当真实人类判断的替身，再对一个较小的、与 RLHF 中实际使用的类似的"代理"奖励模型进行优化。随着针对代理奖励模型的优化不断加强——按照 [`advanced/01`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md) 所描述的那种关系风格来衡量，呈现出一种平滑、可预测的函数形式——黄金标准奖励一开始会随着代理奖励一起上升，完全符合预期，但随后会趋于平台，而如果继续大幅优化，甚至会开始实际下降：策略学会了去满足代理奖励模型那些特有的、古怪的弱点，而不是它本应代表的那种真实质量。Gao 等人（2022）进一步报告说，这条过优化曲线本身也会随奖励模型规模的变化而可预测地伸缩，这就把奖励模型的过优化问题，直接与 [`advanced/01`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md) 所讲的那种规模法则式的推理联系了起来。

[§7](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy)'s KL penalty against $\pi^{SFT}$ is, in this light, best understood not as an incidental
regularizer but as the pipeline's primary defense against reward hacking: it directly limits how
far the policy is allowed to drift from the distribution the reward model was actually trained on
and can be trusted on, at the cost — via the "alignment tax" [§7](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy) described — of also limiting how
much genuine improvement the policy is allowed to make. Choosing $\beta$ is therefore a real
trade-off, not a settled default, and per this curriculum's standing rule on unsettled claims
(`curriculum/README.md` [§5](#5-a-worked-example-computing-the-reward-model-loss)), this module states plainly that neither a single correct value of $\beta$
nor a general solution to reward hacking beyond stronger reward models, better KL control, and more
extensive human oversight currently exists in the published literature — it remains an active
research area, not a closed textbook fact.

由此来看，[第 7 节](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy)中针对 $\pi^{SFT}$ 的 KL 惩罚，最好不要被理解成一种附带的正则化手段，而应被理解成整条流水线抵御奖励黑客的主要防线：它直接限制了策略被允许偏离"奖励模型真正训练过、因而可以信任"的那个分布有多远，但代价是——正如[第 7 节](#7-advantage-estimation-and-the-kl-penalty-against-the-reference-policy)所描述的"对齐税"——也限制了策略被允许做出多大程度的真实改进。因此，$\beta$ 的选择是一个真实存在的权衡，而不是一个已有定论的默认值；按照本课程对悬而未决的说法所遵循的一贯原则（`curriculum/README.md` 第 5 节），本模块在此明确指出：在已发表的文献中，目前既不存在一个唯一正确的 $\beta$ 取值，也不存在除了"更好的奖励模型、更好的 KL 控制、更充分的人类监督"之外，一个能够彻底解决奖励黑客问题的通用方案——这仍然是一个活跃的研究方向，而不是一条已经盖棺定论的教科书事实。

---

## 11. Summary

**小结**

RLHF closes the gap between a pretrained model's next-token objective and what a person actually
wants from it, through a three-stage pipeline ([§2](#2-the-three-stage-rlhf-pipeline-an-overview)): supervised fine-tuning on human
demonstrations produces a reference policy ([§3](#3-stage-1-supervised-fine-tuning-and-the-reference-policy)); a reward model learns a scalar scoring function
from human preference comparisons via the Bradley-Terry loss ([§§4–5](#4-stage-2-reward-modeling-preference-data-and-the-bradley-terry-loss)); and PPO's clipped
surrogate objective, combined with GAE advantage estimation and a KL penalty against the reference
policy, fine-tunes the policy to score well under the reward model without collapsing into
incoherent, reward-model-gaming text ([§§6–9](#6-stage-3-from-policy-gradients-to-ppos-clipped-objective)). That last safeguard is necessary rather than
decorative precisely because the reward model is only ever a proxy for human judgment, and
optimizing any proxy hard enough eventually produces reward hacking ([§10](#10-reward-hacking-and-overoptimization-an-open-problem)) — a genuinely open
problem this module has deliberately presented as such, in keeping with this curriculum's rule that
an unsettled question stays unsettled on the page.

RLHF 通过一条三阶段的流水线（[第 2 节](#2-the-three-stage-rlhf-pipeline-an-overview)），弥合了预训练模型的下一词元目标与一个人真正想要的东西之间的鸿沟：在人类示范数据上进行有监督微调，得到一个参考策略（[第 3 节](#3-stage-1-supervised-fine-tuning-and-the-reference-policy)）；一个奖励模型通过 Bradley-Terry 损失，从人类偏好比较数据中学会一个标量打分函数（[第 4 至 5 节](#4-stage-2-reward-modeling-preference-data-and-the-bradley-terry-loss)）；而 PPO 的裁剪代理目标，结合 GAE 优势估计以及针对参考策略的 KL 惩罚，把策略微调到能在奖励模型下得高分，同时又不至于崩坏成不连贯的、专门迎合奖励模型漏洞的文本（[第 6 至 9 节](#6-stage-3-from-policy-gradients-to-ppos-clipped-objective)）。最后这道防线之所以是必要的、而非装饰性的，正是因为奖励模型终究只是人类判断的一个代理，而任何代理一旦被优化得足够狠，最终都会产生奖励黑客现象（[第 10 节](#10-reward-hacking-and-overoptimization-an-open-problem)）——这是一个真正悬而未决的问题，本模块特意如实地将其呈现出来，遵循的正是本课程"悬而未决的问题就应在文中原样保留其悬而未决状态"这一原则。

---

## References

**参考文献**

### External Sources

- [Christiano, P., Leike, J., Brown, T. B., Martic, M., Legg, S., and Amodei, D. (2017). Deep Reinforcement Learning from Human Preferences. arXiv:1706.03741.](https://arxiv.org/abs/1706.03741)
- [Bradley, R. A. and Terry, M. E. (1952). Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons. Biometrika, 39(3/4), 324–345.](https://academic.oup.com/biomet/article-abstract/39/3-4/324/326091)
- [Schulman, J., Moritz, P., Levine, S., Jordan, M., and Abbeel, P. (2015). High-Dimensional Continuous Control Using Generalized Advantage Estimation. arXiv:1506.02438.](https://arxiv.org/abs/1506.02438)
- [Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. (2017). Proximal Policy Optimization Algorithms. arXiv:1707.06347.](https://arxiv.org/abs/1707.06347)
- [Ziegler, D. M., Stiennon, N., Wu, J., Brown, T. B., Radford, A., Amodei, D., Christiano, P., and Irving, G. (2019). Fine-Tuning Language Models from Human Preferences. arXiv:1909.08593.](https://arxiv.org/abs/1909.08593)
- [Stiennon, N., Ouyang, L., Wu, J., Ziegler, D. M., Lowe, R., Voss, C., Radford, A., Amodei, D., and Christiano, P. (2020). Learning to Summarize from Human Feedback. arXiv:2009.01325.](https://arxiv.org/abs/2009.01325)
- [Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C. L., Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A., Schulman, J., Hilton, J., Kelton, F., Miller, L., Simens, M., Askell, A., Welinder, P., Christiano, P., Leike, J., and Lowe, R. (2022). Training Language Models to Follow Instructions with Human Feedback. arXiv:2203.02155.](https://arxiv.org/abs/2203.02155)
- [Gao, L., Schulman, J., and Hilton, J. (2022). Scaling Laws for Reward Model Overoptimization. arXiv:2210.10760.](https://arxiv.org/abs/2210.10760)

### Internal Cross-References

- [`intermediate/01-training-dynamics-optimization-and-generalization.md`](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md) — gradient descent, optimizers, and learning-rate schedules this module's PPO and reward-model training both build on directly.
- [`advanced/01-scaling-laws-and-emergent-capabilities.md`](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md) — scaling laws this module's discussion of reward-model overoptimization ([§10](#10-reward-hacking-and-overoptimization-an-open-problem)) extends to reward-model size.
- [`advanced/10-modern-post-training-methods-dpo-grpo-and-reward-modeling.md`](https://anu00.dev/curriculum/advanced/10-modern-post-training-methods-dpo-grpo-and-reward-modeling.md) — covers post-training methods developed as alternatives to this module's PPO-based pipeline, including approaches that remove the separate reward-model stage entirely.
