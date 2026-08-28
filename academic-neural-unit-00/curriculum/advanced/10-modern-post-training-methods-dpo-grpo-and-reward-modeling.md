# Modern Post-Training Methods: DPO, GRPO & Reward Modeling

**现代后训练方法：DPO、GRPO 与奖励建模**

| Field   | English                                                                     | 中文                                                  |
| ------- | --------------------------------------------------------------------------- | ----------------------------------------------------- |
| Level   | Advanced                                                                    | 高级                                                  |
| Cluster | Post-Training (S2, Amendment 5)                                             | 后训练（S2，第 5 号修正案）                           |
| Author  | Dr. Aditi Bhandari, Staff Research Scientist — Foundational AI Lead, ANU-00 | ANU-00 基础人工智能首席研究科学家 Aditi Bhandari 博士 |

---

## 1. Introduction: From RLHF to Direct and Group-Relative Post-Training

**导论：从 RLHF 到直接偏好优化与群体相对的后训练方法**

This module builds directly on [`advanced/09` — Reinforcement Learning from Human Feedback](https://anu00.dev/curriculum/advanced/09-reinforcement-learning-from-human-feedback.md)
(Reinforcement Learning from Human Feedback), which is this chapter's named prerequisite and
establishes the three-stage RLHF pipeline this chapter takes as its starting point: a base language
model is first fine-tuned on human demonstrations (supervised fine-tuning), human annotators then
rank several model outputs for the same prompt by preference, a separate **reward model** is trained
to predict those rankings, and finally the base policy is optimized with reinforcement learning —
specifically Proximal Policy Optimization (PPO) — to maximize the learned reward model's score,
subject to a penalty that keeps the policy from drifting too far from its starting point. Because
this module and `advanced/09` — Reinforcement Learning from Human Feedback were authored in parallel under the same S2 curriculum-extension
charter (`README.md` Amendment 5), this section restates only the minimum of that pipeline needed for
this chapter to stand on its own; the full treatment of the RLHF pipeline, its reward model, and PPO
belongs to `advanced/09` — Reinforcement Learning from Human Feedback. This exact three-stage pipeline is the one Long Ouyang and co-authors
describe for InstructGPT, the model that established RLHF as the standard alignment recipe for
instruction-following language models.

本章直接建立在[`advanced/09` — Reinforcement Learning from Human Feedback](https://anu00.dev/curriculum/advanced/09-reinforcement-learning-from-human-feedback.md)（基于人类反馈的强化学习）之上——这是本章明确指定的前置模块，也是本章讨论的出发点：该模块确立了 RLHF 的三阶段流程——首先在人类示范数据上对基础语言模型做有监督微调，随后由人类标注者对同一提示下的多个模型输出按偏好排序，再训练一个独立的**奖励模型**来预测这些排序，最后用强化学习——具体而言是近端策略优化（PPO）——对基础策略进行优化，使其最大化学得的奖励模型给出的分数，同时施加一个约束，防止策略偏离其起点太远。由于本模块与 `advanced/09` — 基于人类反馈的强化学习 是在同一份 S2 课程扩展章程（`README.md` 第 5 号修正案）下并行撰写的，本节仅复述本章能够独立成立所需的最小限度的流程回顾；关于 RLHF 流程、其奖励模型以及 PPO 的完整讲解属于 `advanced/09` — 基于人类反馈的强化学习 的范畴。这套三阶段流程正是 Long Ouyang 及其合著者为 InstructGPT 所描述的流程——该模型确立了 RLHF 作为指令跟随语言模型标准对齐方案的地位。

This chapter is about what changed after 2023: two methods that keep the same underlying preference
data RLHF uses, but restructure how that data turns into an updated policy, for different engineering
reasons and with different trade-offs. **Direct Preference Optimization (DPO)**, introduced by Rafael
Rafailov and co-authors, removes the reward model and the reinforcement-learning loop entirely,
converting preference learning into a single closed-form classification loss computed directly on the
policy being trained. **Group Relative Policy Optimization (GRPO)**, introduced by Zhihong Shao and
co-authors as part of the DeepSeekMath project, keeps reinforcement learning but removes the separate
value-function network PPO requires, replacing it with a statistic computed directly from a group of
sampled outputs to the same prompt. Both methods are grounded in a real, verifiable engineering
complaint about the standard RLHF pipeline — a separately-trained reward model and a PPO value network
are expensive to train, easy to misconfigure, and add failure surface — and this chapter derives both
from first principles rather than presenting them as black-box recipes to be dropped into a training
script.

本章要讲的，是 2023 年之后发生的变化：两种方法都沿用了 RLHF 所依赖的同一类偏好数据，但出于不同的工程动机、以不同的权衡方式，重新组织了这些数据转化为更新后策略的方式。**直接偏好优化（Direct Preference Optimization，DPO）**由 Rafael Rafailov 及其合著者提出，它彻底去掉了奖励模型和强化学习循环，把偏好学习转化为一个直接作用于待训练策略之上、具有闭式解的单一分类损失。**群体相对策略优化（Group Relative Policy Optimization，GRPO）**由 Zhihong Shao 及其合著者在 DeepSeekMath 项目中提出，它保留了强化学习，但去掉了 PPO 所需要的独立价值函数网络，代之以一个直接从针对同一提示采样出的一组输出中计算得到的统计量。这两种方法都源于对标准 RLHF 流程一个真实、可验证的工程层面的抱怨——独立训练的奖励模型和 PPO 的价值网络训练成本高、极易配置错误、并且增加了系统的失效面——本章将从第一性原理出发推导这两种方法，而不是把它们当作可以直接套用到训练脚本中的黑盒配方来介绍。

The chapter proceeds in three movements. [§2](#2-the-bradley-terry-model-a-formal-foundation-for-preference)
through [§3](#3-reward-modeling-objective-training-procedure-and-overoptimization) formalize the
preference model both reward modeling and DPO are built on, and name a real failure mode —
overoptimization — that motivates looking past reward models at all. [§4](#4-deriving-direct-preference-optimization-dpo)
through [§6](#6-beyond-dpo-ipo-kto-and-simpo) derive DPO from that same preference model and survey
its direct successors. [§7](#7-from-ppo-to-group-relative-policy-optimization) through
[§9](#9-grpo-in-production-deepseekmath-deepseek-r1-and-the-length-and-difficulty-bias-critique)
derive GRPO and trace its use, and its own documented biases, into a real production reasoning model.
[§10](#10-contested-ground-and-open-questions) is deliberately not a tidy resolution — several of the
questions this chapter raises are genuinely unsettled in the published literature, and this chapter
says so rather than picking a winner to keep the narrative clean.

本章分三个部分展开。[第 2 节](#2-the-bradley-terry-model-a-formal-foundation-for-preference)到[第 3 节](#3-reward-modeling-objective-training-procedure-and-overoptimization)先形式化奖励建模与 DPO 二者共同依赖的偏好模型，并指出一个真实存在的失败模式——过度优化——它正是促使人们越过奖励模型另寻他法的动机所在。[第 4 节](#4-deriving-direct-preference-optimization-dpo)到[第 6 节](#6-beyond-dpo-ipo-kto-and-simpo)从同一个偏好模型出发推导出 DPO，并考察它的几个直接后继方法。[第 7 节](#7-from-ppo-to-group-relative-policy-optimization)到[第 9 节](#9-grpo-in-production-deepseekmath-deepseek-r1-and-the-length-and-difficulty-bias-critique)推导 GRPO，追溯它的实际应用及其自身有据可查的偏差，一直到一个真实的生产级推理模型。[第 10 节](#10-contested-ground-and-open-questions)刻意没有给出一个整洁的定论——本章提出的若干问题，在已发表的文献中确实尚无定论，本章选择如实说明，而不是为了叙事的整洁而武断地选出一个“赢家”。

---

## 2. The Bradley-Terry Model: A Formal Foundation for Preference

**Bradley-Terry 模型：偏好建模的形式化基础**

Both reward modeling ([§3](#3-reward-modeling-objective-training-procedure-and-overoptimization)) and
DPO ([§4](#4-deriving-direct-preference-optimization-dpo)) rest on the same statistical model of how a
preference between two options arises from an underlying scalar quality score. That model is the
**Bradley-Terry model（Bradley-Terry 模型，布拉德利-特里模型）**, introduced by Ralph Bradley and
Milton Terry in a 1952 _Biometrika_ paper on ranking objects from paired comparisons — for example,
ranking sports teams from a set of pairwise match results, the original paper's own motivating
application. Nothing about the model is specific to language models; RLHF and DPO import it wholesale
because it is exactly the tool statisticians built decades earlier for "given many pairwise judgments,
recover an underlying ranking."

奖励建模（[第 3 节](#3-reward-modeling-objective-training-procedure-and-overoptimization)）与 DPO（[第 4 节](#4-deriving-direct-preference-optimization-dpo)）都建立在同一个统计模型之上，用来描述两个选项之间的偏好是如何从一个潜在的标量质量分数中产生的。这个模型就是 **Bradley-Terry 模型（Bradley-Terry model，布拉德利-特里模型）**，由 Ralph Bradley 与 Milton Terry 在 1952 年发表于《Biometrika》期刊的一篇论文中提出，该论文研究的是如何从成对比较结果中对若干对象进行排序——例如根据一系列两两对阵的比赛结果，对体育队伍进行排名，这正是原论文自身的应用场景。这个模型本身与语言模型毫无关系；RLHF 与 DPO 之所以直接照搬这个模型，正是因为它恰好是统计学家几十年前就已经打造好的工具，专门用来解决“给定大量成对判断，还原出其背后的潜在排序”这一问题。

Assume each option $y$ has a latent, unobserved scalar score $r(y)$ — in the RLHF setting, $r(x,y)$ is
the quality of response $y$ to prompt $x$. The Bradley-Terry model states that the probability a human
judge prefers $y_w$ ("winner") over $y_l$ ("loser") is a logistic function of the difference between
their scores:

假设每个选项 $y$ 都有一个潜在的、不可直接观测的标量分数 $r(y)$——在 RLHF 场景下，$r(x,y)$ 表示响应 $y$ 针对提示 $x$ 的质量。Bradley-Terry 模型指出，人类评判者更偏好 $y_w$（“获胜者”）而非 $y_l$（“落败者”）的概率，是二者分数之差的逻辑斯谛函数：

$$
P(y_w \succ y_l \mid x) = \frac{\exp\big(r(x,y_w)\big)}{\exp\big(r(x,y_w)\big) + \exp\big(r(x,y_l)\big)} = \sigma\big(r(x,y_w) - r(x,y_l)\big)
$$

Here $\sigma(z) = 1/(1+e^{-z})$ is the logistic sigmoid function, and the equality on the right follows
from dividing numerator and denominator by $\exp(r(x,y_w))$. Two properties of this formula matter for
everything that follows. First, only the _difference_ $r(x,y_w) - r(x,y_l)$ determines the preference
probability — adding any constant $c(x)$ to both scores leaves the predicted probability unchanged,
because $c(x)$ cancels in the subtraction. This single fact is what later lets the reference-policy
partition function cancel out of the DPO derivation in [§4](#4-deriving-direct-preference-optimization-dpo).
Second, the model is symmetric and well-calibrated by construction: if $r(x,y_w) = r(x,y_l)$, the
model predicts a 50/50 coin flip, matching the intuition that equally good responses should be equally
likely to be preferred by chance.

其中 $\sigma(z) = 1/(1+e^{-z})$ 是逻辑斯谛 sigmoid 函数，右边的等式是把分子和分母同时除以 $\exp(r(x,y_w))$ 得到的。这个公式有两条性质对后文的一切推导都至关重要。第一，决定偏好概率的只是**差值** $r(x,y_w) - r(x,y_l)$——如果给两个分数同时加上任意一个常数 $c(x)$，预测出的概率完全不变，因为在做减法时 $c(x)$ 会被消去。正是这一点，使得后文[第 4 节](#4-deriving-direct-preference-optimization-dpo)推导 DPO 时，参考策略的配分函数才能够被消去。第二，这个模型在构造上就是对称且校准良好的：如果 $r(x,y_w) = r(x,y_l)$，模型预测的就是一个五五开的抛硬币结果，这与直觉相符——两个同样好的响应，理应有相同的概率被偶然选中。

Worked example: suppose two candidate responses to the same prompt have latent scores $r(x,y_w) = 2.0$
and $r(x,y_l) = 0.5$. The Bradley-Terry model predicts $P(y_w \succ y_l \mid x) = \sigma(2.0 - 0.5) =
\sigma(1.5) \approx 0.818$ — an 81.8% chance a human judge prefers the higher-scored response, not
certainty, because the model treats preference judgments as noisy rather than deterministic. If the
score gap widens to $r(x,y_w) - r(x,y_l) = 4.0$, the predicted probability rises to $\sigma(4.0) \approx
0.982$ — clearly-better responses are predicted to win almost every comparison, but the model never
outputs exactly 1.0 for a finite score gap, which is precisely the property [§6](#6-beyond-dpo-ipo-kto-and-simpo)'s
discussion of Identity Preference Optimization (IPO) revisits as a potential weakness.

举一个具体例子：假设针对同一个提示的两个候选响应，其潜在分数分别为 $r(x,y_w) = 2.0$ 和 $r(x,y_l) = 0.5$。Bradley-Terry 模型预测 $P(y_w \succ y_l \mid x) = \sigma(2.0 - 0.5) = \sigma(1.5) \approx 0.818$——也就是说，人类评判者偏好得分更高那个响应的概率约为 81.8%，而不是必然如此，因为该模型把偏好判断视为带噪声的，而不是确定性的。如果分数差距进一步拉大到 $r(x,y_w) - r(x,y_l) = 4.0$，预测概率会上升到 $\sigma(4.0) \approx 0.982$——明显更优的响应在几乎每一次比较中都会“获胜”，但只要分数差距是有限值，模型就永远不会输出恰好等于 1.0 的概率，而这一点正是[第 6 节](#6-beyond-dpo-ipo-kto-and-simpo)在讨论恒等偏好优化（Identity Preference Optimization，IPO）时，重新审视的一个潜在弱点。

---

## 3. Reward Modeling: Objective, Training Procedure, and Overoptimization

**奖励建模：目标函数、训练流程与过度优化**

A **reward model** is a neural network $r_\phi(x,y)$ — typically the same transformer architecture as
the policy being trained, with its final unembedding layer replaced by a single scalar output head —
that is trained to approximate the latent score $r(x,y)$ the Bradley-Terry model of
[§2](#2-the-bradley-terry-model-a-formal-foundation-for-preference) assumes exists. Given a dataset
$\mathcal{D}$ of human preference judgments, each a triple $(x, y_w, y_l)$ recording that a human judge
preferred $y_w$ over $y_l$ for prompt $x$, the reward model is trained by maximum likelihood under the
Bradley-Terry model — equivalently, by minimizing the negative log-likelihood of the observed
preferences:

**奖励模型**是一个神经网络 $r_\phi(x,y)$——通常与待训练的策略采用相同的 Transformer 架构，只是把最后的反嵌入层替换为单一的标量输出头——其训练目标是逼近[第 2 节](#2-the-bradley-terry-model-a-formal-foundation-for-preference)中 Bradley-Terry 模型所假设存在的那个潜在分数 $r(x,y)$。给定一个人类偏好判断数据集 $\mathcal{D}$，其中每一条记录都是一个三元组 $(x, y_w, y_l)$，表示人类评判者在提示 $x$ 下更偏好 $y_w$ 而非 $y_l$，奖励模型的训练方式就是在 Bradley-Terry 模型下做极大似然估计——等价地，最小化观测到的偏好数据的负对数似然：

$$
\mathcal{L}_R(\phi) = -\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\Big[\log \sigma\big(r_\phi(x,y_w) - r_\phi(x,y_l)\big)\Big]
$$

This is exactly the loss described in Ouyang and co-authors' InstructGPT paper's reward-modeling
stage: the reward model is initialized from the supervised-fine-tuned policy, then fine-tuned on this
pairwise classification objective. Once trained, $r_\phi$ is frozen and used as the reward signal that
drives PPO in the RLHF pipeline [`advanced/09` — Reinforcement Learning from Human Feedback](https://anu00.dev/curriculum/advanced/09-reinforcement-learning-from-human-feedback.md)
covers in full.

这正是 Ouyang 及其合著者在 InstructGPT 论文中所描述的奖励建模阶段的损失函数：奖励模型从有监督微调后的策略初始化而来，随后在这个成对分类目标上做微调。训练完成后，$r_\phi$ 就被冻结下来，作为驱动 [`advanced/09` — Reinforcement Learning from Human Feedback](https://anu00.dev/curriculum/advanced/09-reinforcement-learning-from-human-feedback.md) 全文所讲解的 RLHF 流程中 PPO 阶段的奖励信号。

Worked example: given a preference triple where the current reward model scores $r_\phi(x,y_w) = 1.2$
and $r_\phi(x,y_l) = 1.0$ (a narrow gap, since the model has not yet learned to separate this pair
well), the per-example loss is $-\log\sigma(1.2-1.0) = -\log\sigma(0.2) \approx -\log(0.550) \approx
0.598$ nats. Gradient descent on this loss pushes $r_\phi(x,y_w)$ up and $r_\phi(x,y_l)$ down until the
gap — and hence the predicted preference probability — grows, exactly the direction that reduces the
loss toward zero.

举一个具体例子：假设某个偏好三元组中，当前奖励模型给出的分数为 $r_\phi(x,y_w) = 1.2$ 和 $r_\phi(x,y_l) = 1.0$（差距很小，因为模型尚未学会很好地区分这一对样本），那么该样本的损失为 $-\log\sigma(1.2-1.0) = -\log\sigma(0.2) \approx -\log(0.550) \approx 0.598$ 纳特（nats）。对该损失做梯度下降，会把 $r_\phi(x,y_w)$ 推高、把 $r_\phi(x,y_l)$ 压低，直到二者的差距——从而预测出的偏好概率——不断增大，这正是能让损失趋向于零的方向。

Because the reward model is only an approximation of true human preference — trained on a finite,
noisy sample of human judgments — optimizing a policy against it too aggressively runs into
**overoptimization**, also called **reward hacking**: the policy learns to produce outputs that score
highly under $r_\phi$ without actually being higher-quality by the standard $r_\phi$ was meant to
approximate. Leo Gao, John Schulman, and Jacob Hilton study this directly, framing it as an instance of
**Goodhart's Law（古德哈特定律）** — informally, "when a measure becomes a target, it ceases to be a
good measure" — applied to reward models specifically. Their paper studies how the true, gold-standard
reward and the proxy reward model's score diverge as optimization pressure (measured by KL divergence
from the reference policy) increases, and reports that this proxy-versus-gold relationship follows
different functional forms depending on the optimization method (RL fine-tuning versus best-of-$n$
resampling), with the divergence's severity scaling smoothly, and predictably, with reward-model size
and dataset size.

由于奖励模型终究只是对真实人类偏好的一种近似——它是在有限、带噪声的人类判断样本上训练出来的——如果针对它过于激进地优化策略，就会遇到**过度优化**问题，也称为**奖励黑客**：策略学会了生成在 $r_\phi$ 下得分很高、但按照 $r_\phi$ 本应逼近的那个标准来看，实际质量却并未真正提升的输出。Leo Gao、John Schulman 与 Jacob Hilton 直接研究了这一现象，将其归纳为**古德哈特定律（Goodhart's Law）**——通俗地说，“一旦一项指标变成了优化目标，它就不再是一个好指标”——在奖励模型这一具体场景下的一个体现。他们的论文研究了随着优化压力（以相对参考策略的 KL 散度衡量）不断增大，真实的“黄金标准”奖励与代理奖励模型给出的分数是如何逐渐背离的，并报告称：这种“代理指标 vs. 黄金标准”的关系，会因优化方法（强化学习微调 vs. best-of-$n$ 重采样）不同而呈现出不同的函数形态，而且这种背离的严重程度，会随着奖励模型规模和训练数据规模的变化平滑、可预测地变化。

The overoptimization problem is the direct engineering motivation for [§4](#4-deriving-direct-preference-optimization-dpo):
if a separately-trained reward model is both expensive to build and structurally vulnerable to being
gamed by the very policy it is meant to supervise, a method that never trains a standalone reward model
at all removes an entire class of failure by construction — which is exactly DPO's pitch, examined
next.

过度优化问题正是[第 4 节](#4-deriving-direct-preference-optimization-dpo)背后直接的工程动机所在：如果一个独立训练出来的奖励模型，既训练成本高昂，又在结构上容易被它本应监督的那个策略“钻空子”，那么一种压根不训练独立奖励模型的方法，就从构造上直接消除了这整整一类失败模式——这正是接下来要考察的 DPO 的核心卖点。

---

## 4. Deriving Direct Preference Optimization (DPO)

**直接偏好优化（DPO）的推导**

The standard RLHF objective [`advanced/09` — Reinforcement Learning from Human Feedback](https://anu00.dev/curriculum/advanced/09-reinforcement-learning-from-human-feedback.md) covers
in full is a KL-regularized reward maximization problem: find a policy $\pi_\theta$ that maximizes
expected reward under the trained reward model $r_\phi$, while staying close (in KL divergence) to a
fixed reference policy $\pi_{ref}$ (typically the supervised-fine-tuned model before RL):

[`advanced/09` — Reinforcement Learning from Human Feedback](https://anu00.dev/curriculum/advanced/09-reinforcement-learning-from-human-feedback.md) 全文所讲的标准 RLHF 目标，是一个带 KL 正则化的奖励最大化问题：寻找一个策略 $\pi_\theta$，使其在训练好的奖励模型 $r_\phi$ 下期望奖励最大化，同时（以 KL 散度衡量）与一个固定的参考策略 $\pi_{ref}$（通常是尚未经过强化学习的、有监督微调后的模型）保持接近：

$$
\max_{\pi_\theta} \; \mathbb{E}_{x\sim\mathcal{D},\, y\sim\pi_\theta(\cdot\mid x)}\big[r_\phi(x,y)\big] - \beta\, D_{KL}\big[\pi_\theta(\cdot\mid x)\,\|\,\pi_{ref}(\cdot\mid x)\big]
$$

Rafailov and co-authors do not merely assert this solution — they derive it in their paper's own
Appendix A.1, using the same constrained-optimization argument that produces the Gibbs/Boltzmann policy
throughout maximum-entropy reinforcement learning and soft Q-learning more generally. The derivation is
worth carrying out explicitly here, because the resulting closed form is exactly what makes the
partition function $Z(x)$ cancel later in this section. Fix a prompt $x$ — everything below is
implicitly conditioned on this fixed $x$ — and expand the KL-divergence term in the objective above by
its definition, $D_{KL}\big[\pi(\cdot\mid x)\,\|\,\pi_{ref}(\cdot\mid x)\big] = \sum_y \pi(y\mid
x)\log\dfrac{\pi(y\mid x)}{\pi_{ref}(y\mid x)}$. This turns the maximization into an explicit
optimization over the distribution $\pi(\cdot\mid x)$ itself:

Rafailov 及其合著者并不是凭空断言这个解，而是在论文自身的附录 A.1 中给出了推导，所用的正是最大熵强化学习与软 Q 学习中，用来推出吉布斯-玻尔兹曼（Gibbs/Boltzmann）策略形式的那一套约束优化论证。这个推导值得在此完整地展示一遍，因为正是由此得到的闭式解，才使得配分函数 $Z(x)$ 能够在本节后文中被消去。固定一个提示 $x$——以下推导中的所有量都隐含地以这个固定的 $x$ 为条件——并按定义把上面目标函数中的 KL 散度项展开：$D_{KL}\big[\pi(\cdot\mid x)\,\|\,\pi_{ref}(\cdot\mid x)\big] = \sum_y \pi(y\mid x)\log\dfrac{\pi(y\mid x)}{\pi_{ref}(y\mid x)}$。这就把原来的最大化问题，转化成了一个直接针对分布 $\pi(\cdot\mid x)$ 本身的显式优化问题：

$$
\max_{\pi(\cdot\mid x)} \;\; \sum_{y} \pi(y\mid x)\, r(x,y) \;-\; \beta \sum_{y} \pi(y\mid x) \log\frac{\pi(y\mid x)}{\pi_{ref}(y\mid x)}
$$

This maximization is subject to $\pi(\cdot\mid x)$ being a valid probability distribution over
responses, i.e. $\sum_y \pi(y\mid x) = 1$. Non-negativity, $\pi(y\mid x)\geq 0$, does not need to be
imposed as a separate active constraint — it holds automatically for the solution found below, since
that solution turns out to be a positive multiple of $\pi_{ref}(y\mid x) \geq 0$. This leaves a single
equality constraint, so the standard method of Lagrange multipliers applies: introducing a multiplier
$\lambda(x)$ for the normalization constraint gives the Lagrangian

这个最大化问题的约束条件，是 $\pi(\cdot\mid x)$ 必须是响应集合上的一个合法概率分布，即 $\sum_y \pi(y\mid x) = 1$。非负性约束 $\pi(y\mid x)\geq 0$ 不需要单独作为一个有效约束来处理——下面求得的解自然就会满足它，因为这个解本身就是 $\pi_{ref}(y\mid x) \geq 0$ 的一个正数倍。这样一来就只剩下一个等式约束，因此可以直接套用标准的**拉格朗日乘子法（method of Lagrange multipliers）**：为归一化约束引入一个拉格朗日乘子 $\lambda(x)$，得到拉格朗日函数

$$
\mathcal{L}\big(\pi(\cdot\mid x),\, \lambda(x)\big) = \sum_{y} \pi(y\mid x)\, r(x,y) \;-\; \beta \sum_{y} \pi(y\mid x) \log\frac{\pi(y\mid x)}{\pi_{ref}(y\mid x)} \;+\; \lambda(x)\left(1 - \sum_{y} \pi(y\mid x)\right)
$$

The objective being maximized is strictly concave in $\pi(\cdot\mid x)$: the first term $\sum_y
\pi(y\mid x)\,r(x,y)$ is linear in $\pi$, and the second term equals $-\beta\, D_{KL}\big[\pi(\cdot\mid
x)\,\|\,\pi_{ref}(\cdot\mid x)\big]$, which is strictly concave because KL divergence is strictly convex
in its first argument and $\beta > 0$; a linear function plus a strictly concave function is strictly
concave. Over a convex feasible set — the probability simplex defined by the constraint above — a
strictly concave objective has at most one stationary point, and that point is automatically its unique
global maximum, so finding the stationary point of $\mathcal{L}$ is sufficient to solve the problem.
Because $y$ ranges over a discrete (if very large) set of possible responses, $\pi(\cdot\mid x)$ is a
vector indexed by $y$ rather than a continuous function, so no calculus of variations is required here:
each $\pi(y\mid x)$ can be treated as an ordinary independent variable, and $\mathcal{L}$ differentiated
with respect to one of them at a time. Using $\dfrac{\partial}{\partial \pi(y\mid x)}\big[\pi(y\mid
x)\log\pi(y\mid x)\big] = \log\pi(y\mid x) + 1$, the partial derivative of $\mathcal{L}$ with respect to
$\pi(y\mid x)$, for one fixed response $y$, is

被最大化的目标函数关于 $\pi(\cdot\mid x)$ 是**严格凹的**：第一项 $\sum_y \pi(y\mid x)\,r(x,y)$ 关于 $\pi$ 是线性的，第二项则等于 $-\beta\, D_{KL}\big[\pi(\cdot\mid x)\,\|\,\pi_{ref}(\cdot\mid x)\big]$——由于 KL 散度关于其第一个自变量是严格凸的，且 $\beta > 0$，这一项本身就是严格凹的；线性函数加上严格凹函数，其结果仍然是严格凹函数。在一个凸可行集——也就是上面约束条件所定义的概率单纯形——上，严格凹的目标函数至多只有一个驻点，而这个驻点自动就是唯一的全局最大值点，因此只需要求出 $\mathcal{L}$ 的驻点，即可解出整个问题。由于 $y$ 取值于一个离散（尽管规模可能极大）的响应集合，$\pi(\cdot\mid x)$ 本质上是一个以 $y$ 为下标的向量，而不是一个连续函数，因此这里并不需要用到变分法：可以把每一个 $\pi(y\mid x)$ 都当作一个普通的独立变量，逐一对 $\mathcal{L}$ 求偏导。利用 $\dfrac{\partial}{\partial \pi(y\mid x)}\big[\pi(y\mid x)\log\pi(y\mid x)\big] = \log\pi(y\mid x) + 1$，固定某一个响应 $y$，$\mathcal{L}$ 关于 $\pi(y\mid x)$ 的偏导数为

$$
\frac{\partial \mathcal{L}}{\partial \pi(y\mid x)} \;=\; r(x,y) \;-\; \beta\left(\log\frac{\pi(y\mid x)}{\pi_{ref}(y\mid x)} + 1\right) \;-\; \lambda(x)
$$

Setting this partial derivative to zero — the first-order stationarity condition — and solving for the
log-ratio between $\pi$ and $\pi_{ref}$:

令这个偏导数等于零——也就是一阶驻点条件——并解出 $\pi$ 与 $\pi_{ref}$ 之间的对数比值：

$$
\log\frac{\pi(y\mid x)}{\pi_{ref}(y\mid x)} \;=\; \frac{r(x,y)}{\beta} \;-\; 1 \;-\; \frac{\lambda(x)}{\beta}
$$

Exponentiating both sides isolates $\pi(y\mid x)$:

对等式两边取指数，解出 $\pi(y\mid x)$：

$$
\pi(y\mid x) \;=\; \pi_{ref}(y\mid x)\, \exp\!\left(\frac{r(x,y)}{\beta}\right) \cdot \exp\!\left(-1 - \frac{\lambda(x)}{\beta}\right)
$$

The second exponential factor does not depend on $y$ at all — the stationarity condition ties it only
to the single multiplier $\lambda(x)$, which is shared across every response $y$ to the same prompt $x$
— so write it as $1/Z(x)$ for some function $Z(x)$ of $x$ alone, and pin down its exact value using
precisely the normalization constraint that was set aside above:

第二个指数因子根本不依赖于 $y$——驻点条件把它仅仅系于同一个乘子 $\lambda(x)$，而对同一个提示 $x$ 下的每一个响应 $y$ 而言，这个乘子都是共享、不变的——因此可以把它记作 $1/Z(x)$，其中 $Z(x)$ 是一个只依赖于 $x$ 的函数，并且恰好可以利用上面被暂时搁置的归一化约束，来确定它的具体取值：

$$
\sum_{y} \pi(y\mid x) = 1 \;\;\Longrightarrow\;\; \frac{1}{Z(x)} \sum_{y} \pi_{ref}(y\mid x)\, \exp\!\left(\frac{r(x,y)}{\beta}\right) = 1 \;\;\Longrightarrow\;\; Z(x) = \sum_{y} \pi_{ref}(y\mid x)\, \exp\!\left(\frac{r(x,y)}{\beta}\right)
$$

Substituting $1/Z(x)$ back in for the constant factor gives the unique maximizer $\pi^*$ — the
closed-form optimal policy Rafailov and co-authors state, now derived rather than merely asserted, for
_any_ fixed reward function $r$:

把 $1/Z(x)$ 代回这个常数因子的位置，就得到了唯一的最大化解 $\pi^*$——也就是 Rafailov 及其合著者所给出的那个闭式最优策略，对**任意**给定的固定奖励函数 $r$ 都成立，而此刻它是被推导出来的，不再只是被断言的：

$$
\pi^*(y\mid x) = \frac{1}{Z(x)}\,\pi_{ref}(y\mid x)\, \exp\!\left(\frac{1}{\beta} r(x,y)\right)
$$

As the derivation above shows, $Z(x)$ is exactly the normalizing sum required to make $\pi^*(\cdot\mid
x)$ a valid probability distribution — but it remains, in general, computationally intractable to
evaluate directly, since it sums over every possible generated sequence $y$. Rearranging this closed
form to solve for the reward as a function of the optimal policy gives:

正如上面的推导所示，$Z(x)$ 恰好就是让 $\pi^*(\cdot\mid x)$ 成为一个合法概率分布所需要的那个归一化求和项——但一般而言，它在计算上仍然是不可行的，因为它需要对每一个可能生成的序列 $y$ 求和。把这个闭式解反过来整理，把奖励表示为最优策略的函数，就得到：

$$
r(x,y) = \beta \log\frac{\pi^*(y\mid x)}{\pi_{ref}(y\mid x)} + \beta \log Z(x)
$$

This is the pivotal step: it says the reward function implied by any optimal policy $\pi^*$ is fully
determined (up to the intractable, prompt-only-dependent term $\beta\log Z(x)$) by the log-ratio between
that policy and the reference policy. Substituting this expression for $r(x,y_w)$ and $r(x,y_l)$ back
into the Bradley-Terry preference model from [§2](#2-the-bradley-terry-model-a-formal-foundation-for-preference)
is where the trick pays off: because $Z(x)$ depends only on $x$, not on $y$, it is identical for
$y_w$ and $y_l$ under the same prompt, and cancels exactly in the subtraction $r(x,y_w) - r(x,y_l)$ the
Bradley-Terry model requires:

这正是整个推导的关键一步：它说明，任何最优策略 $\pi^*$ 所隐含的奖励函数，完全由该策略与参考策略之间的对数比值所决定（只差一个难以计算、且只依赖于提示本身的项 $\beta\log Z(x)$）。把这个表达式代入[第 2 节](#2-the-bradley-terry-model-a-formal-foundation-for-preference)中 Bradley-Terry 偏好模型里的 $r(x,y_w)$ 和 $r(x,y_l)$，正是这个技巧真正发挥作用的地方：由于 $Z(x)$ 只依赖于 $x$、与 $y$ 无关，在同一个提示下，它对 $y_w$ 和 $y_l$ 而言完全相同，因此会在 Bradley-Terry 模型所要求的差值 $r(x,y_w) - r(x,y_l)$ 中被恰好消去：

$$
P(y_w \succ y_l \mid x) = \sigma\!\left(\beta\log\frac{\pi^*(y_w\mid x)}{\pi_{ref}(y_w\mid x)} - \beta\log\frac{\pi^*(y_l\mid x)}{\pi_{ref}(y_l\mid x)}\right)
$$

The intractable $Z(x)$ has vanished entirely, leaving a preference probability expressed purely in
terms of the policy's and the reference model's log-probabilities of the two responses. Replacing the
unknown optimal $\pi^*$ with the trainable policy $\pi_\theta$ and fitting it by maximum likelihood on
the human preference dataset $\mathcal{D}$ — exactly as [§3](#3-reward-modeling-objective-training-procedure-and-overoptimization)
fit the reward model — gives the **DPO loss**:

原本难以计算的 $Z(x)$ 就此完全消失，只剩下一个纯粹用策略与参考模型对两个响应的对数概率来表达的偏好概率。把未知的最优策略 $\pi^*$ 替换为可训练的策略 $\pi_\theta$，并像[第 3 节](#3-reward-modeling-objective-training-procedure-and-overoptimization)拟合奖励模型那样，在人类偏好数据集 $\mathcal{D}$ 上对其做极大似然拟合，就得到了 **DPO 损失**：

$$
\mathcal{L}_{DPO}(\pi_\theta;\pi_{ref}) = -\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\left[\log\sigma\!\left(\beta\log\frac{\pi_\theta(y_w\mid x)}{\pi_{ref}(y_w\mid x)} - \beta\log\frac{\pi_\theta(y_l\mid x)}{\pi_{ref}(y_l\mid x)}\right)\right]
$$

Rafailov and co-authors summarize this result in their paper's own title: the language model being
trained is "secretly a reward model" — the quantity $\beta\log\big(\pi_\theta(y\mid x)/\pi_{ref}(y\mid
x)\big)$ _is_ an implicit reward, and minimizing $\mathcal{L}_{DPO}$ by ordinary gradient-based
supervised learning (no sampling from the policy during training, no separate reward model, no PPO
rollouts) provably converges, under their derivation, to the same optimal policy the full RLHF pipeline
targets. This is what "direct" in Direct Preference Optimization（直接偏好优化）names: preference data
maps straight onto a policy-gradient-free classification loss, skipping the reward-modeling and
RL-optimization stages entirely.

Rafailov 及其合著者在论文的标题中就已概括了这一结果：正在被训练的语言模型“本身秘密地就是一个奖励模型”——量 $\beta\log\big(\pi_\theta(y\mid x)/\pi_{ref}(y\mid x)\big)$ **本身就是**一个隐式奖励，而通过普通的基于梯度的有监督学习来最小化 $\mathcal{L}_{DPO}$（训练过程中无需从策略中采样，无需独立的奖励模型，也无需 PPO 式的轨迹采样），按照他们的推导，可以被证明会收敛到与完整 RLHF 流程所追求的同一个最优策略。这正是“直接偏好优化”中“直接”二字的含义：偏好数据被直接映射为一个无需策略梯度的分类损失，完全跳过了奖励建模与强化学习优化这两个阶段。

---

## 5. DPO Worked Example and Practical Considerations

**DPO 实例演算与实践考量**

Worked example: suppose $\beta = 0.1$, and for a given prompt $x$ the reference model assigns
log-probabilities $\log\pi_{ref}(y_w\mid x) = -12.0$ and $\log\pi_{ref}(y_l\mid x) = -10.0$ (the
reference model happens to slightly prefer the human-dispreferred response), while the policy currently
being trained, after some updates, assigns $\log\pi_\theta(y_w\mid x) = -11.0$ and
$\log\pi_\theta(y_l\mid x) = -10.5$. The implicit reward margin is:

举一个具体例子：设 $\beta = 0.1$，对于给定的提示 $x$，参考模型给出的对数概率为 $\log\pi_{ref}(y_w\mid x) = -12.0$ 和 $\log\pi_{ref}(y_l\mid x) = -10.0$（恰好参考模型本身更偏好人类不喜欢的那个响应），而当前正在训练、已经经过若干次更新的策略给出的对数概率为 $\log\pi_\theta(y_w\mid x) = -11.0$ 和 $\log\pi_\theta(y_l\mid x) = -10.5$。此时隐式奖励差值为：

$$
\beta\big[(\log\pi_\theta(y_w\mid x)-\log\pi_{ref}(y_w\mid x)) - (\log\pi_\theta(y_l\mid x)-\log\pi_{ref}(y_l\mid x))\big] = 0.1\big[(-11.0-(-12.0)) - (-10.5-(-10.0))\big]
$$

which simplifies to $0.1\big[(1.0) - (-0.5)\big] = 0.1 \times 1.5 = 0.15$. The per-example loss is
$-\log\sigma(0.15) \approx -\log(0.537) \approx 0.622$ nats, and the gradient of this loss with respect
to $\theta$ pushes $\log\pi_\theta(y_w\mid x)$ up and $\log\pi_\theta(y_l\mid x)$ down relative to their
reference-model values — the policy is being taught to diverge from the reference specifically in the
direction the human preference indicates, and by no more than the KL penalty (controlled by $\beta$)
allows.

化简后为 $0.1\big[(1.0) - (-0.5)\big] = 0.1 \times 1.5 = 0.15$。该样本的损失为 $-\log\sigma(0.15) \approx -\log(0.537) \approx 0.622$ 纳特，这个损失对 $\theta$ 的梯度，会把 $\log\pi_\theta(y_w\mid x)$（相对参考模型的取值）推高、把 $\log\pi_\theta(y_l\mid x)$ 压低——策略正被引导着，朝人类偏好所指示的方向偏离参考模型，而偏离的幅度不会超过（由 $\beta$ 控制的）KL 惩罚所允许的限度。

Three practical properties follow directly from the derivation in [§4](#4-deriving-direct-preference-optimization-dpo)
and matter for anyone implementing DPO. First, $\pi_{ref}$ is fixed throughout training — it is
evaluated once per batch (or its log-probabilities are precomputed) and never updated, so DPO needs two
copies of the model resident (policy and frozen reference) but never runs generation from the policy
during training, unlike PPO's rollout phase. Second, $\beta$ plays exactly the same role it plays in
the RLHF objective of [§4](#4-deriving-direct-preference-optimization-dpo) — a small $\beta$ permits the
policy to move further from $\pi_{ref}$ per unit of preference signal, which can improve fit to the
preference data at the cost of larger divergence from the reference (and a higher risk of the
degenerate, off-distribution behavior a KL penalty exists to prevent). Third, because $\mathcal{L}_{DPO}$
is fit entirely on a fixed, offline preference dataset with no exploration, DPO can only ever push the
policy toward preferences that were actually represented in $\mathcal{D}$ — it has no mechanism, unlike
online RL, for discovering and evaluating novel responses the reference model never sampled during data
collection, a limitation [§10](#10-contested-ground-and-open-questions) returns to when comparing DPO
against online methods.

从[第 4 节](#4-deriving-direct-preference-optimization-dpo)的推导中可以直接得出三条实践性质，对任何要实现 DPO 的人都很重要。第一，$\pi_{ref}$ 在整个训练过程中保持固定——它每个批次只需评估一次（或者预先计算好其对数概率），此后就不再更新，所以 DPO 需要同时驻留两份模型（策略模型与冻结的参考模型），但训练过程中从不需要从策略中做生成，这与 PPO 需要“轨迹采样”阶段不同。第二，$\beta$ 所扮演的角色与它在[第 4 节](#4-deriving-direct-preference-optimization-dpo) RLHF 目标函数中的角色完全一致——较小的 $\beta$ 允许策略在单位偏好信号下偏离 $\pi_{ref}$ 更远，这可以让模型更好地拟合偏好数据，但代价是与参考模型的偏离更大（也更容易出现 KL 惩罚原本要防止的那种退化、偏离训练分布的行为）。第三，由于 $\mathcal{L}_{DPO}$ 完全是在一个固定的、离线的偏好数据集上拟合的，不涉及任何探索，DPO 只能把策略推向 $\mathcal{D}$ 中实际出现过的偏好方向——不像在线强化学习那样，它没有任何机制去发现并评估参考模型在数据收集阶段从未采样过的新响应，这一局限性会在[第 10 节](#10-contested-ground-and-open-questions)比较 DPO 与在线方法时再次被提及。

---

## 6. Beyond DPO: IPO, KTO, and SimPO

**DPO 之外：IPO、KTO 与 SimPO**

DPO's derivation in [§4](#4-deriving-direct-preference-optimization-dpo) makes a specific modeling
choice worth stating explicitly: it assumes pairwise human preferences can always be reduced to a
_pointwise_ scalar reward difference passed through the Bradley-Terry sigmoid — the same assumption
standard reward modeling makes in [§3](#3-reward-modeling-objective-training-procedure-and-overoptimization).
Mohammad Gheshlaghi Azar and co-authors examine this assumption directly, arguing that both RLHF and
DPO "heavily rely" on this pointwise-substitution approximation, and propose a more general framework,
$\Psi\text{PO}$, that operates on pairwise preferences without first reducing them to pointwise rewards.
Setting $\Psi$ to the identity function yields **Identity Preference Optimization (IPO,
恒等偏好优化)**, for which the authors derive an efficient training procedure and report empirical
advantages over DPO on illustrative examples — in particular, IPO adds an explicit regularization term
that keeps the learned preference gap finite even when preference data is noise-free or deterministic,
addressing the concern [§2](#2-the-bradley-terry-model-a-formal-foundation-for-preference) raised about
the Bradley-Terry sigmoid never reaching exactly 1.0: DPO, fit on deterministic preference data with no
regularization on the _magnitude_ of the log-ratio, can in principle drive that log-ratio toward
infinity chasing a probability the sigmoid can only approach, not reach, which IPO's added term is
designed to prevent.

[第 4 节](#4-deriving-direct-preference-optimization-dpo)对 DPO 的推导，做出了一个值得明确指出的建模选择：它假设成对的人类偏好，总能被约化为一个通过 Bradley-Terry sigmoid 函数传递的**逐点式**标量奖励差——这与[第 3 节](#3-reward-modeling-objective-training-procedure-and-overoptimization)中标准奖励建模所做的假设完全相同。Mohammad Gheshlaghi Azar 及其合著者直接审视了这一假设，指出 RLHF 与 DPO 都“严重依赖”这种逐点式替代近似，并提出了一个更一般化的框架 $\Psi\text{PO}$，它直接作用于成对偏好之上，而不先把它们约化为逐点式奖励。将 $\Psi$ 设为恒等函数，就得到了**恒等偏好优化（Identity Preference Optimization，IPO）**，作者为此推导出一套高效的训练方法，并在若干示例上报告了相对 DPO 的实证优势——具体而言，IPO 增加了一个显式的正则化项，即便偏好数据是无噪声、确定性的，也能让学到的偏好差距保持有限，这正是针对[第 2 节](#2-the-bradley-terry-model-a-formal-foundation-for-preference)中提出的那个担忧：Bradley-Terry sigmoid 函数永远无法恰好取值 1.0；而 DPO 在拟合确定性偏好数据、又没有对对数比值的**幅度**做任何正则化的情况下，原则上可能会不断把这个对数比值推向无穷大，去追逐一个 sigmoid 函数只能无限逼近、却永远无法达到的概率值——IPO 新增的正则项，正是为了防止这种情况而设计的。

A second line of critique targets DPO's dependence on _paired_ preference data specifically — two
responses to the same prompt, one marked preferred. Kawin Ethayarajh and co-authors' **Kahneman-Tversky
Optimization (KTO, 卡尼曼-特沃斯基优化)** instead learns from unpaired binary desirability labels — "this
single response was good" or "this single response was bad" — grounding the training objective in
**prospect theory（前景理论）**, the behavioral-economics model of human decision-making under
uncertainty developed by Daniel Kahneman and Amos Tversky, rather than in the Bradley-Terry pairwise
model. The paper reports KTO matches or exceeds DPO's downstream performance across model scales from
1 billion to 30 billion parameters, despite requiring a strictly weaker and often cheaper-to-collect
form of feedback.

第二条批评路线，则针对 DPO 对**成对**偏好数据这一具体形式的依赖——即针对同一提示的两个响应，其中一个被标记为更受偏好。Kawin Ethayarajh 及其合著者提出的**卡尼曼-特沃斯基优化（Kahneman-Tversky Optimization，KTO）**则转而从非成对的二元“可取性”标签中学习——即“这一个响应是好的”或“这一个响应是不好的”——并将训练目标建立在**前景理论（prospect theory）**之上，而不是 Bradley-Terry 成对模型；前景理论是 Daniel Kahneman 与 Amos Tversky 提出的、描述人类在不确定条件下如何决策的行为经济学模型。该论文报告称，在参数规模从 10 亿到 300 亿不等的多种模型上，KTO 都能达到或超过 DPO 的下游表现，尽管它所需要的反馈形式严格更弱、且往往采集成本更低。

A third line simplifies DPO's machinery rather than its data assumptions. Yu Meng, Mengzhou Xia, and
Danqi Chen's **Simple Preference Optimization (SimPO, 简单偏好优化)** removes the reference model
$\pi_{ref}$ from the objective entirely — eliminating the second resident model copy [§5](#5-dpo-worked-example-and-practical-considerations)
noted DPO requires — by using the _length-normalized average log-probability_ of a response under the
policy itself as the implicit reward, rather than a log-ratio against a reference, and adds an explicit
target margin between preferred and dispreferred response scores on top of the Bradley-Terry objective.
The authors report SimPO outperforming DPO by up to 6.4 points on AlpacaEval 2 and up to 7.5 points on
Arena-Hard across the model families they test, and a Gemma-2-9B model trained with SimPO reaching a
72.4% length-controlled win rate on AlpacaEval 2 — the strongest result among sub-10B models on Chatbot
Arena at the time of the paper's writing.

第三条路线简化的不是 DPO 的数据假设，而是它本身的机制。Yu Meng、Mengzhou Xia 与 Danqi Chen 提出的**简单偏好优化（Simple Preference Optimization，SimPO）**，把参考模型 $\pi_{ref}$ 从目标函数中彻底移除——从而省去了[第 5 节](#5-dpo-worked-example-and-practical-considerations)中提到 DPO 所需要驻留的第二份模型——其做法是用响应在策略自身之下、经过长度归一化的**平均对数概率**作为隐式奖励，而不是相对参考模型的对数比值，并在 Bradley-Terry 目标之上额外加入一个偏好响应与非偏好响应得分之间的显式目标间隔。作者报告称，在他们测试的多个模型系列上，SimPO 在 AlpacaEval 2 上最多领先 DPO 6.4 个百分点，在 Arena-Hard 上最多领先 7.5 个百分点；用 SimPO 训练的 Gemma-2-9B 模型在 AlpacaEval 2 上达到了 72.4% 的长度受控胜率——是论文写作当时，Chatbot Arena 上参数规模低于 100 亿的模型中表现最强的。

The table below summarizes the four methods along the dimensions that actually differ.

下表按照这四种方法真正存在差异的几个维度做了归纳总结。

| Method                         | Data required                       | Reference model needed? | Core change vs. DPO                                                        |
| ------------------------------ | ----------------------------------- | ----------------------- | -------------------------------------------------------------------------- |
| **DPO**（直接偏好优化）        | Paired preferences $(y_w,y_l)$      | Yes, frozen             | Baseline — derived in [§4](#4-deriving-direct-preference-optimization-dpo) |
| **IPO**（恒等偏好优化）        | Paired preferences $(y_w,y_l)$      | Yes, frozen             | Regularizes preference-gap magnitude; drops pointwise-reward approximation |
| **KTO**（卡尼曼-特沃斯基优化） | Unpaired binary desirability labels | Yes, frozen             | Prospect-theory objective; no paired data required                         |
| **SimPO**（简单偏好优化）      | Paired preferences $(y_w,y_l)$      | No                      | Reference-free, length-normalized implicit reward + target margin          |

None of these four methods is a strict, universal replacement for the others across every reported
benchmark — this table names their mechanisms, not a ranking, and [§10](#10-contested-ground-and-open-questions)
returns to why a ranking would be premature.

这四种方法之中，没有哪一种能在所有已报告的基准测试上，构成对其他方法严格、普适的替代——上表列出的是它们各自的机制，而不是一个高下排名，[第 10 节](#10-contested-ground-and-open-questions)会回过头来说明，为什么现在给出一个排名还为时过早。

---

## 7. From PPO to Group-Relative Policy Optimization

**从 PPO 到群体相对策略优化**

Where [§4](#4-deriving-direct-preference-optimization-dpo) through [§6](#6-beyond-dpo-ipo-kto-and-simpo)
moved away from reinforcement learning entirely, GRPO moves in the opposite direction: it keeps
reinforcement learning but restructures the specific piece of standard PPO that turns out to be
disproportionately expensive for large language models. John Schulman and co-authors' **Proximal
Policy Optimization (PPO, 近端策略优化)**, the algorithm `advanced/09` — 基于人类反馈的强化学习 covers as the RL stage of the
standard RLHF pipeline, optimizes a _clipped surrogate objective_ that lets the policy take several
gradient steps on the same batch of sampled data without the update straying so far from the
data-collecting policy that the objective's approximation breaks down — clipping the probability
ratio between new and old policy to a small range around 1 is what gives PPO "proximal" in its name,
and is what lets it reuse each batch of rollouts for multiple epochs of updates instead of the single
update classical policy-gradient methods require.

如果说[第 4 节](#4-deriving-direct-preference-optimization-dpo)到[第 6 节](#6-beyond-dpo-ipo-kto-and-simpo)是彻底离开了强化学习的路线，那么 GRPO 走的则是相反的方向：它保留了强化学习，但重新组织了标准 PPO 中那个对大语言模型而言开销格外高昂的具体环节。John Schulman 及其合著者提出的**近端策略优化（Proximal Policy Optimization，PPO）**——`advanced/09` — 基于人类反馈的强化学习 将其作为标准 RLHF 流程中强化学习阶段所讲授的算法——优化的是一个**剪切代理目标**，它允许策略在同一批采样数据上迈出多步梯度更新，而不会让更新偏离采集数据时所用的策略太远、以至于目标函数的近似失效——把新旧策略之间的概率比值剪切到 1 附近的一个小区间内，正是 PPO 名字中“近端（proximal）”一词的由来，也正是它能够对同一批轨迹数据复用多个训练轮次、而不像经典策略梯度方法那样每批数据只能更新一次的原因。

Computing PPO's advantage estimate — how much better a given action was than the policy's average
action in that state, the quantity that actually multiplies the clipped ratio in the objective — requires
a **value function** (or "critic"): a second neural network, typically the same size as the policy
itself, trained to predict expected future reward from any given partial state. For LLM fine-tuning,
this means training and holding in memory a second copy of the language model throughout RL training,
purely to estimate a baseline — roughly doubling the compute and memory footprint of the RL stage on
top of the policy model itself. This cost is compounded in a specific way for reasoning-focused
training: when the reward is sparse and terminal (e.g., a rule-based verifier checks only whether the
final numeric answer to a math problem is correct, assigning reward only at the very last token), a
per-token value function has very little signal to learn to predict against, making it both expensive
and a poor estimator in exactly the setting where verifiable, terminal rewards are most attractive to
use in the first place.

计算 PPO 的优势估计——即某个具体动作相对该状态下策略平均动作而言好了多少，也就是目标函数中真正与剪切比值相乘的那个量——需要一个**价值函数**（或称“评论家”，critic）：这是第二个神经网络，通常与策略本身规模相当，其训练目标是根据任意给定的部分状态预测未来的期望奖励。对大语言模型微调而言，这意味着在整个强化学习训练过程中，都要额外训练并在内存中保留第二份语言模型的副本，而其唯一目的仅仅是估计一个基线——这大致会让强化学习阶段在策略模型本身之外的计算与显存开销再翻上一倍。这一成本在面向推理能力的训练中，还会以一种特定的方式被进一步放大：当奖励是稀疏且仅在终点给出时（例如，一个基于规则的验证器只检查数学题最终的数值答案是否正确，只在最后一个词元处给出奖励），逐词元的价值函数几乎没有什么信号可供学习预测——而恰恰正是在这种可验证的、终点式奖励最具吸引力的场景下，价值函数变得既昂贵又难以准确估计。

Zhihong Shao and co-authors' GRPO, introduced as part of the DeepSeekMath project, replaces the value
function with a much cheaper baseline: instead of training a critic to predict expected reward, GRPO
samples a _group_ of several complete outputs for the same prompt, scores each with the same reward
signal used elsewhere, and uses the group's own reward statistics — mean and standard deviation — as
the baseline for every member of that group. The paper describes GRPO explicitly as a variant of PPO
that "enhances mathematical reasoning abilities while concurrently optimizing the memory usage of
PPO" — the elimination of a same-sized critic network is exactly where that memory saving comes from.

Zhihong Shao 及其合著者提出的 GRPO，是 DeepSeekMath 项目的一部分，它用一个成本低得多的基线取代了价值函数：GRPO 不再训练一个评论家来预测期望奖励，而是针对同一个提示采样出一整**组**完整的输出，用与其他环节相同的奖励信号给每个输出打分，再用这一组自身的奖励统计量——均值与标准差——作为组内每个成员的基线。论文明确将 GRPO 描述为 PPO 的一个变体，它“在提升数学推理能力的同时，也优化了 PPO 的内存占用”——而省去一个与策略同等规模的评论家网络，正是这份内存节省的来源所在。

---

## 8. The GRPO Objective: Formulation and Worked Example

**GRPO 目标函数：形式化表述与实例演算**

For a prompt (in the reasoning setting, a math or coding question) $q$, GRPO samples a group of $G$
complete responses $\{o_1,\dots,o_G\}$ from the policy version being used for rollouts,
$\pi_{\theta_{old}}$, and scores each with a reward function $r_i$ — a rule-based verifier for a
math answer, a reward model, or any other scalar signal. The group-relative advantage for response
$i$ is the reward's **z-score within the group**:

对于一个提示（在推理场景下，是一道数学题或编程题）$q$，GRPO 会从用于生成轨迹的那一版策略 $\pi_{\theta_{old}}$ 中，针对同一个提示采样出一组共 $G$ 个完整响应 $\{o_1,\dots,o_G\}$，并用某个奖励函数 $r_i$（可以是针对数学答案的基于规则的验证器、一个奖励模型，或任何其他标量信号）为每个响应打分。响应 $i$ 的群体相对优势，就是该奖励在这一组内的 **z 分数**：

$$
\hat{A}_i = \frac{r_i - \mathrm{mean}(r_1,\dots,r_G)}{\mathrm{std}(r_1,\dots,r_G)}
$$

Every token in response $o_i$ is assigned the same advantage $\hat{A}_i$ (written $\hat{A}_{i,t}$ for
token $t$ of response $i$, since the group-level statistic does not vary within a single response).
The GRPO objective then applies PPO's own clipped surrogate machinery — the probability ratio between
the policy being updated and the rollout-time policy, clipped to $[1-\epsilon, 1+\epsilon]$ — to this
group-relative advantage, averaged first within each response's tokens and then across the group, and
adds an explicit KL-divergence penalty against a reference policy directly inside the objective (rather
than folding it into the reward, as standard PPO-based RLHF does):

响应 $o_i$ 中的每一个词元都被赋予相同的优势值 $\hat{A}_i$（对响应 $i$ 的第 $t$ 个词元记作 $\hat{A}_{i,t}$，因为这个群体层面的统计量在同一个响应内部并不发生变化）。GRPO 的目标函数随后套用 PPO 自身的剪切代理机制——即待更新策略与轨迹采样时所用策略之间的概率比值，被剪切到 $[1-\epsilon, 1+\epsilon]$ 区间内——作用于这个群体相对优势之上，先在每个响应内部对各词元取平均，再在组内取平均，并且直接在目标函数中显式加入相对参考策略的 KL 散度惩罚项（而不是像标准的基于 PPO 的 RLHF 那样，把它折算进奖励本身）：

$$
\mathcal{J}_{GRPO}(\theta) = \mathbb{E}\left[\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_i|}\sum_{t=1}^{|o_i|}\min\!\Big(\rho_{i,t}(\theta)\,\hat{A}_{i,t},\ \mathrm{clip}\big(\rho_{i,t}(\theta),\,1-\epsilon,\,1+\epsilon\big)\hat{A}_{i,t}\Big) - \beta\, D_{KL}\big[\pi_\theta \,\|\, \pi_{ref}\big]\right]
$$

where $\rho_{i,t}(\theta) = \pi_\theta(o_{i,t}\mid q, o_{i,<t}) \,/\, \pi_{\theta_{old}}(o_{i,t}\mid q,
o_{i,<t})$ is the token-level probability ratio PPO's clipping mechanism operates on. Two
normalization terms are doing distinct jobs here and are worth naming individually, because
[§9](#9-grpo-in-production-deepseekmath-deepseek-r1-and-the-length-and-difficulty-bias-critique) shows
each one has a documented, separate failure mode: the $1/|o_i|$ term averages the per-token surrogate
objective over each response's own length, and the $1/\mathrm{std}(r_1,\dots,r_G)$ term inside
$\hat{A}_i$ normalizes the advantage's scale by how spread out the group's rewards happen to be.

其中 $\rho_{i,t}(\theta) = \pi_\theta(o_{i,t}\mid q, o_{i,<t}) \,/\, \pi_{\theta_{old}}(o_{i,t}\mid q, o_{i,<t})$ 就是 PPO 剪切机制所作用的那个逐词元概率比值。这里有两个归一化项各自承担着不同的作用，值得单独点名，因为[第 9 节](#9-grpo-in-production-deepseekmath-deepseek-r1-and-the-length-and-difficulty-bias-critique)会说明，二者各自都有一个有据可查、彼此独立的失败模式：$1/|o_i|$ 项是把逐词元的代理目标，按每个响应自身的长度取平均；而 $\hat{A}_i$ 内部的 $1/\mathrm{std}(r_1,\dots,r_G)$ 项，则是按这一组奖励碰巧呈现出的离散程度，对优势值的尺度做归一化。

Worked example: suppose $G = 4$ and a rule-based verifier assigns binary rewards $r_1=1, r_2=0, r_3=1,
r_4=0$ for a math problem where two of the four sampled responses reached the correct final answer.
The group mean is $\mathrm{mean}(1,0,1,0) = 0.5$ and the group standard deviation is
$\mathrm{std}(1,0,1,0) = 0.5$. The resulting advantages are $\hat{A}_1 = (1-0.5)/0.5 = 1.0$,
$\hat{A}_2 = (0-0.5)/0.5 = -1.0$, $\hat{A}_3 = 1.0$, $\hat{A}_4 = -1.0$ — correct responses receive a
positive advantage and are reinforced, incorrect ones a negative advantage and are suppressed, with no
value-function forward pass anywhere in the computation. If instead all four responses had been correct
($r_i = 1$ for all $i$), $\mathrm{std}(1,1,1,1) = 0$ and every advantage is undefined (division by
zero) — a degenerate case implementations must guard against, and one that foreshadows the
difficulty-bias critique in [§9](#9-grpo-in-production-deepseekmath-deepseek-r1-and-the-length-and-difficulty-bias-critique).

举一个具体例子：设 $G = 4$，对于某道数学题，一个基于规则的验证器给出的二元奖励为 $r_1=1, r_2=0, r_3=1, r_4=0$，即四个采样响应中有两个得出了正确的最终答案。这一组的均值为 $\mathrm{mean}(1,0,1,0) = 0.5$，标准差为 $\mathrm{std}(1,0,1,0) = 0.5$。由此得到的优势值为 $\hat{A}_1 = (1-0.5)/0.5 = 1.0$，$\hat{A}_2 = (0-0.5)/0.5 = -1.0$，$\hat{A}_3 = 1.0$，$\hat{A}_4 = -1.0$——正确的响应获得正的优势值、因而被强化，错误的响应获得负的优势值、因而被抑制，整个计算过程中没有任何一次价值函数的前向计算。反过来，如果四个响应全部正确（对所有 $i$ 都有 $r_i = 1$），那么 $\mathrm{std}(1,1,1,1) = 0$，每个优势值都会因除以零而变得未定义——这是实现时必须防范的一种退化情形，也预示了[第 9 节](#9-grpo-in-production-deepseekmath-deepseek-r1-and-the-length-and-difficulty-bias-critique)将要讨论的难度偏差批评。

---

## 9. GRPO in Production: DeepSeekMath, DeepSeek-R1, and the Length and Difficulty Bias Critique

**GRPO 的生产实践：DeepSeekMath、DeepSeek-R1 与长度和难度偏差批评**

GRPO was first introduced and validated in Shao and co-authors' DeepSeekMath paper, where it was used
to train a model specifically on verifiable mathematical reasoning problems — exactly the sparse,
terminal-reward setting [§7](#7-from-ppo-to-group-relative-policy-optimization) identified as
particularly costly for a PPO-style value function to handle well. DeepSeek-AI's later DeepSeek-R1,
covered publicly first as an arXiv preprint and subsequently published in _Nature_, used GRPO as the
reinforcement-learning algorithm behind its central claim: that a base language model, trained with
large-scale reinforcement learning against verifiable rewards and comparatively little supervised
fine-tuning, can develop advanced reasoning behaviors — self-reflection, verification of its own
intermediate steps, and dynamic strategy adaptation — as an emergent property of the RL training
process rather than something explicitly taught by demonstration.

GRPO 最早是在 Shao 及其合著者的 DeepSeekMath 论文中被提出并得到验证的，该论文用它来专门训练一个针对可验证数学推理问题的模型——这正是[第 7 节](#7-from-ppo-to-group-relative-policy-optimization)所指出的、对 PPO 式价值函数而言格外昂贵、难以妥善处理的稀疏终点式奖励场景。DeepSeek-AI 后来的 DeepSeek-R1——最初以 arXiv 预印本形式公开，随后正式发表于《Nature》——用 GRPO 作为强化学习算法，支撑起其核心主张：一个基础语言模型，如果针对可验证奖励进行大规模强化学习训练、而只搭配相对较少的有监督微调，就能够发展出高级的推理行为——自我反思、对自身中间步骤的验证、以及动态的策略调整——这些行为是强化学习训练过程中涌现出的性质，而不是通过示范被显式教授的。

GRPO's group-relative baseline is not, however, a free lunch, and Zichen Liu and co-authors' "Dr.
GRPO" paper identifies an optimization bias built into exactly the two normalization terms
[§8](#8-the-grpo-objective-formulation-and-worked-example) named. The response-length normalization
term $1/|o_i|$ systematically favors longer incorrect responses over shorter correct ones: because the
per-token surrogate objective is averaged over the response's own length before being combined across
the group, a longer response dilutes any given token's individual contribution to the gradient, which
Liu and co-authors show creates a net incentive for the model to lengthen incorrect responses — an
observable failure mode independent of whether length itself is ever explicitly rewarded. The
group-level standard-deviation normalization inside $\hat{A}_i$ produces a second, separate bias: for
prompts where the sampled responses happen to have low reward variance — questions the model finds
uniformly easy or uniformly hard, exactly the near-degenerate case the worked example in
[§8](#8-the-grpo-objective-formulation-and-worked-example) previewed — dividing by a small
$\mathrm{std}(r_1,\dots,r_G)$ inflates the resulting advantage magnitude, so the training signal
systematically overweights low-variance-difficulty questions relative to ones where the group's
responses are more evenly split between correct and incorrect. Dr. GRPO's proposed fix removes both
normalization terms — computing the advantage from the raw reward difference without dividing by the
group's standard deviation, and aggregating the surrogate objective across all tokens in the group
without dividing by each response's individual length — which the authors report yields an unbiased
policy-gradient estimator that improves token efficiency while preserving reasoning performance.

然而，GRPO 的群体相对基线并不是没有代价的，Zichen Liu 及其合著者的“Dr. GRPO”论文，恰恰在[第 8 节](#8-the-grpo-objective-formulation-and-worked-example)提到的这两个归一化项中，各自找到了一种内生的优化偏差。响应长度归一化项 $1/|o_i|$，会系统性地偏向更长的错误响应、而不利于更短的正确响应：因为逐词元的代理目标先在响应自身长度上取平均、再在组内做综合，更长的响应会稀释每个词元对梯度的个体贡献，Liu 及其合著者证明，这会形成一种净的激励，促使模型把错误的响应变得更长——这是一种可观测的失败模式，与“长度本身是否曾被显式奖励”无关。$\hat{A}_i$ 内部的组内标准差归一化，则产生了第二种、彼此独立的偏差：对于那些采样出的响应恰好奖励方差较低的提示——也就是模型觉得整体一致地简单、或整体一致地困难的问题，正是[第 8 节](#8-the-grpo-objective-formulation-and-worked-example)实例演算中预先展示过的那种近似退化情形——除以一个很小的 $\mathrm{std}(r_1,\dots,r_G)$ 会放大由此得到的优势值幅度，从而使训练信号系统性地过度加权那些低方差难度的问题，相对于那些组内响应在正确与错误之间分布更均衡的问题而言。Dr. GRPO 提出的修正方案，是把这两个归一化项都去掉——计算优势值时直接使用原始奖励差、不再除以组内标准差，聚合代理目标时对组内所有词元求和、不再除以每个响应各自的长度——作者报告称，这样得到的是一个无偏的策略梯度估计器，能够在保持推理性能的同时提升词元使用效率。

---

## 10. Contested Ground and Open Questions

**尚存争议的领域与开放问题**

This chapter closes by naming, rather than resolving, four points where the published literature has
not converged, per this curriculum's standing rule that unsettled questions are stated as unsettled
rather than smoothed into false consensus.

本章最后要指出、而不是去强行解决四个已发表文献尚未达成共识的问题，这也是本课程一贯坚持的原则：对于尚无定论的问题，应如实说明其尚无定论，而不是为了表面的整齐一致而将其抹平。

**Is DPO actually equivalent in practice to PPO-based RLHF, or only in theory?** Shusheng Xu and
co-authors' comprehensive empirical study reports that a carefully-tuned PPO can _surpass_ DPO and
other offline alignment methods across dialogue and, notably, competitive coding tasks, and argues DPO
has "fundamental limitations" stemming from exactly the offline, fixed-dataset property
[§5](#5-dpo-worked-example-and-practical-considerations) named — DPO cannot explore or evaluate
responses outside its training distribution the way an online RL loop that samples fresh rollouts can.
This directly complicates any blanket claim that DPO "is" RLHF in a cheaper package: the theoretical
equivalence [§4](#4-deriving-direct-preference-optimization-dpo) derives holds for the optimal policy
under _exact_ optimization of both objectives, not necessarily for the policies that finite,
imperfectly-tuned training actually reaches, and the two methods' practical rankings appear to depend
on task type, data quality, and tuning effort in ways the field has not fully mapped.

**DPO 在实践中真的等价于基于 PPO 的 RLHF，还是仅仅在理论上等价？** Shusheng Xu 及其合著者的一项综合性实证研究报告称，一个经过精心调优的 PPO，在对话任务、尤其是竞赛级编程任务上，其表现可以**超过** DPO 及其他离线对齐方法，并指出 DPO 存在“根本性局限”，其根源正是[第 5 节](#5-dpo-worked-example-and-practical-considerations)所指出的那个离线、固定数据集的特性——DPO 无法像在线强化学习循环那样，通过采样全新的轨迹来探索或评估训练分布之外的响应。这直接对“DPO 本质上就是一种更廉价版本的 RLHF”这类笼统说法提出了质疑：[第 4 节](#4-deriving-direct-preference-optimization-dpo)所推导出的理论等价性，成立的前提是对两个目标函数都做**精确**优化所得到的最优策略，并不必然适用于有限的、调优并不完美的实际训练所真正收敛到的策略；这两种方法在实践中孰优孰劣，似乎取决于任务类型、数据质量与调优投入等因素，而目前学界尚未对此形成完整的认识图景。

**Which DPO variant is actually best?** [§6](#6-beyond-dpo-ipo-kto-and-simpo) deliberately presented
IPO, KTO, and SimPO as addressing different, specific concerns with DPO — theoretical soundness of the
Bradley-Terry approximation, data-collection cost, and computational overhead, respectively — rather
than as three competing bids for the same crown. Each paper reports favorable results on its own
chosen benchmarks against its own chosen baselines; this chapter has not attempted, and the published
literature does not yet offer, a single head-to-head study covering all four methods under identical
data, compute, and evaluation conditions, so a reader should treat "SimPO beats DPO by 6.4 points"
as a real, verified result on the specific benchmarks and models the SimPO paper reports, not as a
general law that SimPO dominates DPO everywhere.

**在这些 DPO 变体中，究竟哪一种才是最好的？**[第 6 节](#6-beyond-dpo-ipo-kto-and-simpo)刻意把 IPO、KTO 和 SimPO 呈现为分别针对 DPO 的不同、具体问题——依次是 Bradley-Terry 近似的理论合理性、数据采集成本、以及计算开销——而不是三个争夺同一顶“王冠”的竞争者。每一篇论文都在各自选定的基准测试上、针对各自选定的基线方法报告了有利的结果；本章并未尝试、目前已发表的文献也尚未提供一项在完全相同的数据、算力与评估条件下，同时覆盖这四种方法的正面对比研究，因此读者应当把“SimPO 领先 DPO 6.4 个百分点”视为在 SimPO 论文所报告的特定基准和模型上真实、经过验证的结果，而不应将其当作“SimPO 在任何场景下都全面优于 DPO”这样一条普适规律。

**Does the Dr. GRPO critique mean production systems should stop using original GRPO?** DeepSeek-R1's
publicly reported training used the original, biased-per Liu and co-authors' analysis, GRPO
formulation, and still produced the reasoning capabilities the paper documents. This is a genuine
tension this chapter does not resolve: either the length and difficulty biases [§9](#9-grpo-in-production-deepseekmath-deepseek-r1-and-the-length-and-difficulty-bias-critique)
describes matter less in practice than the theoretical analysis suggests, or DeepSeek-R1's specific
training recipe (data mixture, reward design, model scale) happened to be robust to them, or the
biases are real and DeepSeek-R1's reported results would have been further improved by Dr. GRPO's
correction — the published record as of this writing does not settle which.

**Dr. GRPO 的批评，是否意味着生产系统应当停止使用原始版本的 GRPO？** DeepSeek-R1 公开报告的训练过程，使用的正是原始的、按 Liu 及其合著者的分析存在偏差的 GRPO 形式，却依然产出了论文中所记录的那些推理能力。这是本章并未加以解决的一个真实张力：究竟是[第 9 节](#9-grpo-in-production-deepseekmath-deepseek-r1-and-the-length-and-difficulty-bias-critique)所描述的长度偏差与难度偏差，在实践中的影响其实小于理论分析所暗示的程度；还是 DeepSeek-R1 具体的训练方案（数据配比、奖励设计、模型规模）恰好对这些偏差具有一定的鲁棒性；抑或这些偏差确实真实存在，只是 DeepSeek-R1 已报告的结果如果采用 Dr. GRPO 的修正方案，本可以进一步提升——截至本文写作之时，已发表的记录尚无法对此给出定论。

**Is reward modeling itself obsolete?** [§3](#3-reward-modeling-objective-training-procedure-and-overoptimization)'s
overoptimization problem and [§4](#4-deriving-direct-preference-optimization-dpo)'s elimination of the
standalone reward model might suggest reward models are being phased out in favor of direct or
group-relative methods. This is not accurate as a general claim: GRPO, as [§8](#8-the-grpo-objective-formulation-and-worked-example)
shows, still requires _some_ scalar reward signal per sampled response, whether that comes from a
rule-based verifier (as in DeepSeekMath's and DeepSeek-R1's math and code domains, where a ground-truth
checker is available) or from a trained reward model (necessary wherever no automatic verifier exists —
open-ended writing, subjective helpfulness, and most real-world instruction-following). Reward
modeling and the overoptimization risk [§3](#3-reward-modeling-objective-training-procedure-and-overoptimization)
documents remain a live concern precisely wherever GRPO's own reward signal is itself a learned reward
model rather than a rule-based verifier — the methods in this chapter change how preference data
becomes a policy update, not whether a scalar reward signal is needed at all.

**奖励建模本身是否已经过时？**[第 3 节](#3-reward-modeling-objective-training-procedure-and-overoptimization)所讨论的过度优化问题，以及[第 4 节](#4-deriving-direct-preference-optimization-dpo)对独立奖励模型的取消，或许会让人觉得，奖励模型正在被直接式或群体相对式方法逐步淘汰。作为一个普遍性断言，这并不准确：如[第 8 节](#8-the-grpo-objective-formulation-and-worked-example)所示，GRPO 仍然需要为每一个采样出的响应提供**某种**标量奖励信号，无论这个信号来自基于规则的验证器（如 DeepSeekMath 与 DeepSeek-R1 所面对的数学和代码领域，那里存在可用的标准答案检查器），还是来自一个训练出来的奖励模型（在任何不存在自动验证器的场景下都是必需的——开放式写作、主观意义上的“有帮助程度”，以及绝大多数现实世界中的指令跟随任务）。只要 GRPO 自身所用的奖励信号，仍然是一个学习得到的奖励模型、而不是基于规则的验证器，[第 3 节](#3-reward-modeling-objective-training-procedure-and-overoptimization)所记录的奖励建模与过度优化风险，就依然是一个现实存在的隐患——本章所讲的这些方法，改变的是偏好数据如何转化为策略更新，而不是“是否还需要一个标量奖励信号”这件事本身。

---

## 11. Summary

**小结**

This chapter derived two post-2023 alternatives to the standard PPO-based RLHF pipeline
[`advanced/09` — Reinforcement Learning from Human Feedback](https://anu00.dev/curriculum/advanced/09-reinforcement-learning-from-human-feedback.md) established, both grounded in the
same Bradley-Terry preference model ([§2](#2-the-bradley-terry-model-a-formal-foundation-for-preference))
underlying standard reward modeling ([§3](#3-reward-modeling-objective-training-procedure-and-overoptimization)).
Direct Preference Optimization eliminates the reward model and the RL loop by algebraically folding a
KL-constrained reward-maximization objective's closed-form optimal policy back into the Bradley-Terry
likelihood, producing a single classification loss ([§4](#4-deriving-direct-preference-optimization-dpo)–[§5](#5-dpo-worked-example-and-practical-considerations)),
and its own assumptions were in turn refined or challenged by IPO, KTO, and SimPO
([§6](#6-beyond-dpo-ipo-kto-and-simpo)). Group Relative Policy Optimization keeps reinforcement
learning but eliminates PPO's value-function network by estimating a baseline from a sampled group's
own reward statistics ([§7](#7-from-ppo-to-group-relative-policy-optimization)–[§8](#8-the-grpo-objective-formulation-and-worked-example)),
a design that powered DeepSeekMath and DeepSeek-R1's reasoning results but carries its own documented
length and difficulty biases, which Dr. GRPO's analysis traces to GRPO's two normalization terms
specifically ([§9](#9-grpo-in-production-deepseekmath-deepseek-r1-and-the-length-and-difficulty-bias-critique)).
[§10](#10-contested-ground-and-open-questions)'s four open questions are not loose ends to be tidied
up in a future revision of this chapter — they are an accurate description of where the published
literature currently stands, and a reader entering this field should expect the ranking among DPO,
its variants, PPO, and GRPO to keep shifting as more head-to-head studies are published.

本章推导了两种在 2023 年之后出现的、替代 [`advanced/09` — Reinforcement Learning from Human Feedback](https://anu00.dev/curriculum/advanced/09-reinforcement-learning-from-human-feedback.md) 所确立的标准“基于 PPO 的 RLHF”流程的方法，二者都建立在与标准奖励建模（[第 3 节](#3-reward-modeling-objective-training-procedure-and-overoptimization)）相同的 Bradley-Terry 偏好模型（[第 2 节](#2-the-bradley-terry-model-a-formal-foundation-for-preference)）之上。直接偏好优化通过代数手段，把一个带 KL 约束的奖励最大化目标的闭式最优策略解，重新代入 Bradley-Terry 似然之中，从而消去了奖励模型与强化学习循环，得到一个单一的分类损失（[第 4 节](#4-deriving-direct-preference-optimization-dpo)–[第 5 节](#5-dpo-worked-example-and-practical-considerations)），而它自身的假设，又分别被 IPO、KTO 与 SimPO 进一步细化或质疑（[第 6 节](#6-beyond-dpo-ipo-kto-and-simpo)）。群体相对策略优化保留了强化学习，但通过从一组采样结果自身的奖励统计量中估计基线，消去了 PPO 的价值函数网络（[第 7 节](#7-from-ppo-to-group-relative-policy-optimization)–[第 8 节](#8-the-grpo-objective-formulation-and-worked-example)），这一设计支撑起了 DeepSeekMath 与 DeepSeek-R1 的推理成果，但也带有其自身有据可查的长度偏差与难度偏差，Dr. GRPO 的分析将其具体归因于 GRPO 的两个归一化项（[第 9 节](#9-grpo-in-production-deepseekmath-deepseek-r1-and-the-length-and-difficulty-bias-critique)）。[第 10 节](#10-contested-ground-and-open-questions)提出的四个开放问题，并不是本章未来修订时需要收尾的松散线头——它们是对已发表文献现状的如实描述，初入这一领域的读者应当预期，随着更多正面对比研究的发表，DPO、其各种变体、PPO 与 GRPO 之间的优劣排名还会持续变化。

---

## References

**参考文献**

### External Sources

- [Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons — Bradley & Terry, Biometrika, 1952](https://www.jstor.org/stable/2334029)
- [Training language models to follow instructions with human feedback — Ouyang et al., arXiv:2203.02155](https://arxiv.org/abs/2203.02155)
- [Proximal Policy Optimization Algorithms — Schulman, Wolski, Dhariwal, Radford & Klimov, arXiv:1707.06347](https://arxiv.org/abs/1707.06347)
- [Scaling Laws for Reward Model Overoptimization — Gao, Schulman & Hilton, arXiv:2210.10760](https://arxiv.org/abs/2210.10760)
- [Direct Preference Optimization: Your Language Model is Secretly a Reward Model — Rafailov, Sharma, Mitchell, Ermon, Manning & Finn, arXiv:2305.18290](https://arxiv.org/abs/2305.18290)
- [A General Theoretical Paradigm to Understand Learning from Human Preferences — Azar, Rowland, Piot, Guo, Calandriello, Valko & Munos, arXiv:2310.12036](https://arxiv.org/abs/2310.12036)
- [KTO: Model Alignment as Prospect Theoretic Optimization — Ethayarajh, Xu, Muennighoff, Jurafsky & Kiela, arXiv:2402.01306 (ICML 2024)](https://arxiv.org/abs/2402.01306)
- [SimPO: Simple Preference Optimization with a Reference-Free Reward — Meng, Xia & Chen, arXiv:2405.14734 (NeurIPS 2024)](https://arxiv.org/abs/2405.14734)
- [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models — Shao et al., arXiv:2402.03300](https://arxiv.org/abs/2402.03300)
- [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning — DeepSeek-AI, arXiv:2501.12948](https://arxiv.org/abs/2501.12948)
- [Understanding R1-Zero-Like Training: A Critical Perspective (Dr. GRPO) — Liu, Chen, Li, Qi, Pang, Du, Lee & Lin, arXiv:2503.20783](https://arxiv.org/abs/2503.20783)
- [Is DPO Superior to PPO for LLM Alignment? A Comprehensive Study — Xu, Fu, Gao, Ye, Liu, Mei, Wang, Yu & Wu, arXiv:2404.10719 (ICML 2024)](https://arxiv.org/abs/2404.10719)

### Internal Cross-References

- [`advanced/09` — Reinforcement Learning from Human Feedback](https://anu00.dev/curriculum/advanced/09-reinforcement-learning-from-human-feedback.md)
- [`intermediate/01` — Training Dynamics: Optimization & Generalization](https://anu00.dev/curriculum/intermediate/01-training-dynamics-optimization-and-generalization.md)
- [`advanced/01` — Scaling Laws & Emergent Capabilities](https://anu00.dev/curriculum/advanced/01-scaling-laws-and-emergent-capabilities.md)
- [`advanced/08` — Rigorous Agent Evaluation: Statistical Methodology](https://anu00.dev/curriculum/advanced/08-rigorous-agent-evaluation-statistical-methodology.md)
