# Training Dynamics: Optimization & Generalization

**训练动力学：优化与泛化**

| Field   | English                                                                  | 中文                                              |
| ------- | ------------------------------------------------------------------------ | ------------------------------------------------- |
| Level   | Intermediate                                                             | 中级                                              |
| Cluster | Foundations                                                              | 基础                                              |
| Author  | Dr. Samuel Okonkwo, Research Scientist — Machine Learning Theory, ANU-00 | ANU-00 机器学习理论研究科学家 Samuel Okonkwo 博士 |

---

## 1. Introduction: From a Static Network to a Training Trajectory

**引言：从静态网络到训练轨迹**

`introductory/01` defined a neural network as a parameterized function that maps inputs to
outputs, and described the loss function as a scalar measuring how wrong the network's
predictions are, and backpropagation as the algorithm that computes the gradient of that loss with respect to every parameter. That module stopped at the single-step update
rule: adjust each parameter a small amount in the direction that reduces the loss. This module
picks up exactly where that stopped and asks a different question — not "what is one training
step," but "what happens over the thousands or millions of steps it actually takes to train a real
model, and why does the resulting network work well on data it has never seen."

`introductory/01` 已经把神经网络定义为一个带参数的函数，将输入映射到输出；把损失函数定义为衡量网络预测有多"错"的标量值；把反向传播定义为计算该损失相对于每个参数的梯度的算法。那份材料止步于单步更新规则：把每个参数沿着能降低损失的方向调整一小步。本模块正是从这里接着讲下去，但问的是另一个问题——不是"一步训练做了什么"，而是"训练实际进行的成千上万步里究竟发生了什么，为什么训练出来的网络能在它从未见过的数据上表现良好"。

This is the difference between **optimization** and **generalization**, and the two
are not the same problem even though a single training run touches both. Optimization asks whether
the training procedure actually drives the training loss down — whether the numbers get smaller.
Generalization asks whether a network that has driven its training loss down will also perform well
on new, unseen data drawn from the same underlying distribution. A network can optimize perfectly
and generalize terribly, and understanding why is most of what this module is about.

这正是**优化**与**泛化**之间的区别，尽管同一次训练会同时触及这两者，它们却不是同一个问题。优化问的是训练过程是否真的把训练损失降下去了——数字是否变小了。泛化问的是，一个把训练损失降到很低的网络，能否在来自同一潜在分布、但从未见过的新数据上同样表现良好。一个网络完全可以把优化做到极致却把泛化做得很糟糕，理解这是为什么，正是本模块的核心内容。

---

## 2. Gradient Descent and Its Stochastic Variants

**梯度下降及其随机变体**

Recall the update rule from `introductory/01`: given parameters $\theta$ and a loss function $L(\theta)$, the
gradient-descent step is $\theta \leftarrow \theta - \eta \nabla L(\theta)$, where $\eta$ (eta) is the learning rate
and $\nabla L(\theta)$ is the gradient of the loss with respect to every parameter, computed by backpropagation.
That module computed $\nabla L(\theta)$ using the _entire_ training set on every step — this is called **batch
gradient descent**. In practice, almost no real system trains this way, because
computing the gradient over millions of examples before taking a single step is far too slow, and
because — as we will see — the noise introduced by not doing this turns out to help generalization
rather than only hurting it.

回忆一下 `introductory/01` 中的更新规则：给定参数 $\theta$ 与损失函数 $L(\theta)$，梯度下降步骤为 $\theta \leftarrow \theta - \eta \nabla L(\theta)$，其中 $\eta$（eta，读作"伊塔"）是学习率，$\nabla L(\theta)$ 是损失相对于每个参数的梯度，由反向传播计算得出。那份材料在每一步都用*整个*训练集来计算 $\nabla L(\theta)$——这被称为**批量梯度下降**。而在实践中，几乎没有真实系统会这样训练，因为在迈出一步之前就要在数百万个样本上计算梯度，速度实在太慢；而且——正如我们接下来会看到的——不这样做所引入的噪声，事实证明反而有助于泛化，而不仅仅是有害的。

**Stochastic gradient descent** (SGD) replaces the full-dataset gradient with the
gradient computed on a single randomly sampled training example, or — in the form almost
universally used today — a small **mini-batch** of examples (commonly 32 to a few
thousand, depending on hardware and model size). The foundational theoretical justification for
this idea predates deep learning by decades: Robbins and Monro's 1951 paper on stochastic
approximation showed that an iterative procedure using noisy estimates of a gradient converges to
the same root as the noise-free procedure, provided the step sizes satisfy certain decay conditions
— the mathematical ancestor of every learning-rate schedule discussed in §4 below.

**随机梯度下降（SGD）** 用单个随机抽取的训练样本上计算出的梯度，取代了全数据集梯度；而在如今几乎普遍使用的形式中，是用一个小的**小批量**样本（常见取值在 32 到几千之间，取决于硬件与模型规模）来计算梯度。这一思想的理论根基比深度学习早了几十年：Robbins 与 Monro 在 1951 年关于随机近似的论文中证明，只要步长满足一定的衰减条件，使用带噪声梯度估计的迭代过程会收敛到与无噪声过程相同的根——这正是下文第 4 节将讨论的每一种学习率调度策略的数学源头。

Mini-batch SGD has a second, empirically crucial property beyond speed: the noise in each
mini-batch's gradient estimate acts as an implicit regularizer. Because each step is
computed on a different random subset of the data, the optimization trajectory does not follow the
smooth path that batch gradient descent would take — it jitters, and that jitter tends to push the
parameters out of sharp, narrow minima of the loss landscape and toward flatter regions,
which empirical and theoretical work has repeatedly connected to better generalization. We will
return to this connection between the sharpness of a minimum and generalization when discussing
double descent in §8.

小批量 SGD 除了速度之外，还有第二个在实践中至关重要的性质：每个小批量梯度估计中的噪声，起到了一种隐式正则化的作用。由于每一步都是在数据的一个不同随机子集上计算的，优化轨迹不会像批量梯度下降那样走一条平滑的路径——它会抖动，而这种抖动往往会把参数推离损失曲面中那些尖锐、狭窄的极小值，推向更平坦的区域；大量实证与理论工作反复发现，这种平坦区域与更好的泛化能力相关联。在第 8 节讨论双下降现象时，我们会再次回到"极小值的尖锐程度"与"泛化能力"之间的这层联系。

---

## 3. Adaptive Optimizers: Momentum, RMSProp, and Adam

**自适应优化器：动量法、RMSProp 与 Adam**

Plain SGD treats every parameter identically and uses a single global learning rate, which is a
poor fit for real loss landscapes: some directions in parameter space are steep and others are
nearly flat, and a learning rate small enough to be stable in the steep directions is often far too
small to make progress in the flat ones. **Momentum** addresses part of this by
accumulating a running average of past gradients — an exponentially weighted moving average — and
stepping in that averaged direction rather than the raw current gradient, which damps oscillation
across steep, narrow ravines in the loss surface and accelerates progress along consistently flat
directions, much like a ball rolling downhill accumulates velocity.

普通 SGD 对每个参数一视同仁，使用单一的全局学习率，而这与真实的损失曲面很不匹配：参数空间中有些方向陡峭，有些方向近乎平坦；一个在陡峭方向上足够稳定的学习率，往往在平坦方向上小到几乎无法取得进展。**动量法**部分解决了这个问题：它对过去的梯度做累积——一个指数加权移动平均——并沿着这个被平均过的方向迈步，而不是沿着当前这一步的原始梯度方向迈步。这样一来，损失曲面上那些陡峭狭窄的沟壑中的震荡会被抑制，而在持续平坦的方向上则会加速前进，就像一个球滚下山坡时会不断积累速度一样。

The optimizer most widely used in practice today, **Adam**（Adaptive Moment Estimation，自适应矩估计）,
was introduced by Kingma and Ba (2014) and combines momentum with a second idea: maintaining a
running estimate not just of the gradient's mean but of its variance, and dividing each parameter's
update by the square root of that variance estimate. Concretely, Adam maintains two exponentially
weighted moving averages of the gradient $g_t$ at step t — a first-moment estimate $m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$ and a second-moment estimate $v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$, applies a bias correction
to each (since both are initialized at zero and are therefore biased toward zero early in
training), and updates parameters as $\theta_t \leftarrow \theta_{t-1} - \eta \cdot \hat{m}_t / (\sqrt{\hat{v}_t} + \epsilon)$, where $\epsilon$ is a small
constant added for numerical stability. The practical effect is that parameters whose gradients
have been small and consistent get comparatively larger effective steps, and parameters whose
gradients have been large or noisy get comparatively smaller ones — an automatic, per-parameter
learning-rate adjustment that made Adam dramatically easier to tune than plain SGD across a wide
range of architectures, which is a large part of why it became close to a default choice.

如今实践中最广泛使用的优化器 **Adam**（Adaptive Moment Estimation，自适应矩估计）由 Kingma 与 Ba 于 2014
年提出，它把动量法与另一个想法结合了起来：不仅维护梯度均值的滚动估计，还维护梯度方差的滚动估计，并用每个参数更新量除以该方差估计的平方根。具体来说，Adam
在第 t 步为梯度 $g_t$ 维护两个指数加权移动平均——一阶矩估计 $m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$，以及二阶矩估计 $v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$，并对两者都做偏差修正（因为二者都初始化为零，训练早期会偏向于零），随后按 $\theta_t \leftarrow \theta_{t-1} - \eta \cdot \hat{m}_t / (\sqrt{\hat{v}_t} + \epsilon)$ 更新参数，其中 $\epsilon$ 是为数值稳定性而加入的一个很小的常数。这样做的实际效果是：那些梯度一直较小且稳定的参数会获得相对更大的有效步长，而梯度较大或噪声较多的参数则获得相对更小的步长——这是一种自动的、按参数区分的学习率调整机制，使得
Adam 在各种各样的架构上都比普通 SGD 容易调试得多，这也是它几乎成为默认选择的重要原因之一。

Adam is not, however, a strictly better generalizer than SGD with momentum in every setting — a
substantial body of empirical work has found plain SGD with a well-tuned schedule can generalize
better on some vision tasks, part of why the choice of optimizer is itself an empirical decision,
not a settled one. One specific defect in the original Adam formulation was diagnosed and fixed by
Loshchilov and Hutter (2017): naive L2 regularization (added directly to the loss, which is
mathematically equivalent to weight decay for plain SGD) is _not_ equivalent to weight decay once
Adam's per-parameter rescaling is applied, because the rescaling distorts the effective decay rate
per parameter. Their fix, **AdamW**, decouples the weight-decay term from the gradient-based
update entirely, applying it as a separate multiplicative shrinkage of the weights at each step,
and is now the default optimizer for training most large transformer models.

不过，Adam 在生成模型上并不能在每种情形下都严格优于带动量的 SGD——大量实证研究发现，在某些视觉任务上，配合精心调优的调度策略的普通
SGD 反而泛化得更好，这也是"优化器的选择本身就是一个需要实证验证的决策，而非已有定论"的部分原因。原始 Adam
公式中一个具体的缺陷由 Loshchilov 与 Hutter（2017）诊断并修复：朴素的 L2
正则化（直接加到损失函数中，这在普通 SGD 下在数学上等价于权重衰减）一旦经过 Adam 的按参数缩放，就*不再*等价于权重衰减了，因为这种缩放会扭曲每个参数实际的衰减速率。他们提出的修复方案
**AdamW** 将权重衰减项与基于梯度的更新完全解耦，把它作为每一步中对权重的一次独立的乘性收缩来施加，如今它已成为训练大多数大型
Transformer 模型的默认优化器。

---

## 4. Learning Rate Schedules and Warmup

**学习率调度与预热**

A fixed learning rate throughout training is rarely optimal: early in training, when parameters
are far from any good solution, a larger learning rate lets the network make fast progress; late
in training, when parameters are near a good solution, a large learning rate causes the parameters
to bounce around that solution rather than settling into it, since each step overshoots. A
**learning rate schedule** addresses this by varying $\eta$ over the course of training,
typically starting relatively high and decreasing it — through a linear decay, a step decay, or,
very commonly, a smooth cosine decay.

在整个训练过程中使用固定的学习率很少是最优的：训练早期，参数离任何好的解都还很远，较大的学习率能让网络快速取得进展；训练后期，参数已经接近一个好的解，较大的学习率会导致参数在这个解附近来回震荡而无法真正落定，因为每一步都会"迈过头"。**学习率调度**正是为了解决这个问题，在训练过程中改变 $\eta$
的取值，通常一开始取相对较大的值，随后逐渐降低——可以是线性衰减、阶梯式衰减，或者非常常见的、平滑的余弦衰减。

Loshchilov and Hutter's earlier 2016 paper introduced **SGDR** (Stochastic Gradient Descent with
Warm Restarts), which decays the learning rate along a cosine curve and then periodically resets it
to a high value partway through training — a "restart" — which the authors showed lets the
optimizer escape a local minimum it has settled into and find another, sometimes better one, and
this cosine-decay idea (with or without restarts) is now one of the most common schedule shapes
used for training large models. A second, separate technique — **learning-rate warmup**,
in which the learning rate starts near zero and ramps up over the first few hundred to few
thousand steps before the main decay schedule begins — is used because at initialization, before
Adam's second-moment estimates have accumulated enough gradient history to be reliable, taking a
large step can push the network into a badly conditioned region of the loss landscape from which
it struggles to recover; ramping the learning rate up slowly gives those moment estimates time to
stabilize first.

Loshchilov 与 Hutter 更早在 2016 年的论文中提出了 **SGDR**（Stochastic Gradient Descent with Warm
Restarts，带热重启的随机梯度下降），其学习率沿余弦曲线衰减，并在训练进行到一定阶段后周期性地将其重置为一个较高的值——即所谓的"重启"；作者证明这能让优化器跳出已经陷入的一个局部极小值，去寻找另一个、有时更优的极小值。如今，这种余弦衰减的思路（无论是否带重启）已成为训练大型模型最常用的调度形状之一。另一项独立的技术——**学习率预热**——让学习率从接近零开始，在最初的几百到几千步内逐步爬升，然后再进入主衰减调度；之所以需要它，是因为在初始化阶段，Adam
的二阶矩估计还没有积累足够的梯度历史来变得可靠，此时迈出较大的一步可能把网络推入损失曲面中一个条件数很差的区域，难以从中恢复；让学习率缓慢爬升，能给这些矩估计留出时间先稳定下来。

---

## 5. The Bias–Variance Tradeoff and the Generalization Gap

**偏差–方差权衡与泛化差距**

We now turn from optimization to generalization directly. Define the **generalization gap** as the difference between a model's error on the training set and its error on a held-out
test set drawn from the same distribution but never used for training. A large generalization gap
means the model has, informally, "memorized" patterns specific to the training examples rather
than learning patterns that hold across the whole distribution — this is called
**overfitting**. A model that fails to drive even its training error down, typically
because it is not expressive enough for the task, is **underfitting**.

现在我们把话题从优化直接转向泛化。定义**泛化差距**为模型在训练集上的误差与它在一个留出的测试集上的误差之差——测试集来自与训练集相同的分布，但从未用于训练。泛化差距很大，通俗地说，意味着模型"记住"了训练样本中特有的模式，而不是学到了在整个分布上都成立的规律——这被称为**过拟合**。而一个连训练误差都无法降低的模型，通常是因为它对这个任务而言表达能力不足，这被称为**欠拟合**。

The classical framework for understanding this tradeoff is the **bias–variance
decomposition**, formalized for neural networks in a widely cited 1992 paper by
Geman, Bienenstock, and Doursat. For a model trained to predict a target from noisy data, the
expected squared error on new data decomposes into three terms: **bias**, the error from
the model's hypothesis class being too simple to represent the true underlying pattern; **variance**, the error from the model being highly sensitive to which particular training examples it
happened to see, so that a different training set of the same size would have produced a
meaningfully different model; and irreducible noise inherent to the data itself. A model that is
too simple (underfit) has high bias and low variance; a model that is too flexible (overfit
relative to classical theory) has low bias and high variance. The classical prescription was
therefore to find a "sweet spot" of model capacity in the middle — which, as §8 below describes,
turns out to be an incomplete picture for the very large, heavily overparameterized models used in
modern deep learning.

理解这一权衡的经典框架是**偏差–方差分解**，Geman、Bienenstock 与 Doursat
在 1992 年一篇被广泛引用的论文中将其形式化并应用于神经网络。对于一个从带噪声数据中学习预测目标的模型，它在新数据上的期望平方误差可以分解为三项：**偏差**——由于模型的假设类过于简单、无法表示真实的底层规律而产生的误差；**方差**——由于模型对它恰好见过的那批特定训练样本高度敏感，以至于换一个规模相同但样本不同的训练集就会得到一个明显不同的模型，由此产生的误差；以及数据本身固有的、不可消除的噪声。一个过于简单（欠拟合）的模型具有高偏差、低方差；一个过于灵活（相对于经典理论而言过拟合）的模型则具有低偏差、高方差。因此，经典的处方是在模型容量的两端之间找到一个"甜蜜点"——但正如下文第
8 节所述，这对于现代深度学习中使用的、极大且严重过参数化的模型而言，是一幅并不完整的图景。

A related and striking empirical finding, due to Zhang, Bengio, Hardt, Recht, and Vinyals (2017),
is that state-of-the-art image-classification networks can drive their training error to zero even
when the training labels are replaced with pure random noise — meaning these networks have more
than enough raw capacity to simply memorize an arbitrary training set, with no genuine pattern to
learn at all. The fact that the _same_ networks, trained on real labels with the same optimization
procedure, generalize well despite having this much raw memorization capacity is precisely why
classical capacity-based theory (§9 below) struggles to fully explain deep-learning generalization,
and why the field still treats this as a genuinely open theoretical question rather than a solved
one.

Zhang、Bengio、Hardt、Recht 与 Vinyals（2017）的一项相关且引人注目的实证发现是：即便把训练标签替换成纯粹的随机噪声，最先进的图像分类网络依然能把训练误差降到零——这意味着这些网络的原始容量绰绰有余，足以直接记住一个任意的训练集，其中根本没有任何真正的规律可学。而正是同样的这些网络，在用相同的优化流程训练真实标签时却能很好地泛化，尽管它们拥有如此之大的原始记忆容量——这恰恰是经典的、基于容量的理论（见下文第
9 节）难以完全解释深度学习泛化能力的原因，也是这个领域至今仍将其视为一个真正悬而未决、而非已经解决的理论问题的原因。

---

## 6. Regularization Techniques

**正则化技术**

**Regularization** is the general name for any technique that constrains a model during
training to reduce the generalization gap, typically by discouraging it from fitting training-set
noise too closely. Four techniques recur throughout deep learning practice:

**正则化**是对训练过程中任何用来约束模型、以缩小泛化差距的技术的统称，其做法通常是阻止模型过度贴合训练集中的噪声。深度学习实践中反复出现的技术共有四种：

| Technique               | EN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 中文                                                                                                                                                                                                                                                                                                                                                                                               |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **L2 regularization**   | also called weight decay when applied as a direct multiplicative shrinkage — adds a penalty term proportional to the sum of squared parameter values to the loss, encouraging the model to prefer smaller weights unless the data strongly justifies larger ones — smaller weights typically correspond to smoother, less erratic learned functions.                                                                                                                                                                                                                        | 当以直接的乘性收缩方式施加时也称为权重衰减——在损失函数中加入一个与参数值平方和成正比的惩罚项，鼓励模型在没有数据强有力支持的情况下倾向于使用更小的权重——更小的权重通常对应着更平滑、波动更小的学习到的函数。                                                                                                                                                                                       |
| **Dropout**（随机失活） | introduced by Srivastava, Hinton, Krizhevsky, Sutskever, and Salakhutdinov (2014), takes a different approach: during each training step, it randomly sets a fraction of the network's activations (commonly 20–50%) to zero, forcing the remaining units to produce useful outputs without being able to rely on any specific other unit always being present. This can be understood as training an enormous ensemble of overlapping, thinned sub-networks that share weights, and at test time all units are used together with their outputs scaled down to compensate. | 由 Srivastava、Hinton、Krizhevsky、Sutskever 与 Salakhutdinov（2014）提出，采用了一种不同的思路：在每一次训练步骤中，随机将网络中一部分激活值（通常是 20% 到 50%）置零，迫使剩下的单元在不能依赖任何特定的其他单元始终存在的情况下，也能产生有用的输出。这可以理解为在训练一个由大量相互重叠、共享权重的"变瘦"子网络组成的庞大集成；而在测试阶段，所有单元一起参与计算，输出值按比例缩小以做补偿。 |
| **Early stopping**      | a third, procedurally simple technique: monitor loss on a held-out validation set during training and stop once that validation loss begins to rise even as training loss continues to fall — the point past which the model is beginning to overfit.                                                                                                                                                                                                                                                                                                                       | 第三种、流程上更简单的技术：在训练过程中持续监控模型在留出验证集上的损失，一旦验证损失开始上升——即便训练损失仍在继续下降——就停止训练，这个转折点正是模型开始过拟合的地方。                                                                                                                                                                                                                         |
| **Data augmentation**   | generating synthetic training variations (rotations, crops, paraphrases, and so on, depending on the data modality) — reduces overfitting by effectively enlarging the training distribution the model sees, so that memorizing the augmented set no longer means memorizing the underlying distribution.                                                                                                                                                                                                                                                                   | 即生成训练数据的合成变体（依据数据模态的不同，可以是旋转、裁剪、改写等）——通过有效扩大模型所见的训练分布来减少过拟合，使得"记住增强后的数据集"不再等同于"记住底层的真实分布"。                                                                                                                                                                                                                     |

---

## 7. A Worked Example: Training Dynamics on a Toy Regression Problem

**一个实例：一个玩具回归问题上的训练动力学**

To make §§2–4 concrete, consider the simplest possible learning problem: fitting a single
parameter w to minimize $L(w) = (1/n)\sum_i (w \cdot x_i - y_i)^2$, where each $(x_i, y_i)$ pair is a training example
and the model's prediction is simply $w \cdot x$ (a line through the origin). Suppose our tiny training set
is $(x, y) \in \{(1, 2), (2, 3.9), (3, 6.1)\}$ — approximately $y \approx 2x$ with a little noise. The gradient
of L with respect to w is $\nabla L(w) = (2/n)\sum_i x_i (w \cdot x_i - y_i)$, and starting from $w_0 = 0$ with a learning
rate $\eta = 0.05$, batch gradient descent proceeds as follows:

为了让第 2 至 4 节的内容具体化，考虑最简单的学习问题：拟合单个参数 w，使 $L(w) = (1/n)\sum_i (w \cdot x_i - y_i)^2$ 最小化，其中每个 $(x_i, y_i)$ 都是一个训练样本，模型的预测就是 $w \cdot x$（一条过原点的直线）。假设我们的小训练集是 $(x, y) \in \{(1, 2), (2, 3.9), (3, 6.1)\}$——大致满足 $y \approx 2x$，带有一点噪声。L 相对于 w
的梯度为 $\nabla L(w) = (2/n)\sum_i x_i (w \cdot x_i - y_i)$，从 $w_0 = 0$ 出发，取学习率 $\eta = 0.05$，批量梯度下降的过程如下：

| Step | w     | L(w)   | $\nabla L(w)$ |
| ---- | ----- | ------ | ------------- |
| 0    | 0.000 | 18.007 | −29.267       |
| 1    | 1.463 | 1.719  | −8.671        |
| 2    | 1.897 | 0.163  | −2.517        |
| 3    | 2.023 | 0.024  | −0.694        |
| 4    | 2.058 | 0.014  | −0.170        |
| 5    | 2.066 | 0.014  | −0.021        |

The loss drops sharply in the first few steps and then flattens out near $w \approx 2.07$, close to the
true underlying slope of 2 — the residual gap is exactly the irreducible noise in the three data
points, which no value of w can fit exactly. Now repeat this with $\eta = 0.6$ instead of 0.05: the
first step overshoots to $w_1 = 17.56$, the loss explodes rather than shrinks, and the sequence
diverges — a direct illustration of why §4's warmup and decay schedules matter: too large a
learning rate does not just converge slowly, it can fail to converge at all. If instead we used
**stochastic** gradient descent — computing $\nabla L$ on one randomly chosen example per step rather than
all three — the trajectory of w would not decrease as smoothly as the table above; it would jitter
around the same final neighborhood of $w \approx 2$, illustrating the noise-as-implicit-regularizer effect
described in §2, in miniature.

损失在最初几步中迅速下降，随后在 $w \approx 2.07$ 附近趋于平坦，这非常接近真实的底层斜率
2——剩余的这一点差距，正是这三个数据点中固有的、不可消除的噪声，任何 w 的取值都无法将其完全拟合掉。现在把学习率从 0.05
换成 0.6 重新计算：第一步就会"迈过头"，跳到 $w_1 = 17.56$，损失非但没有缩小反而急剧膨胀，整个序列发散——这正好直观地说明了第 4
节中预热与衰减调度为何重要：学习率太大，不仅仅是收敛得慢，甚至可能根本无法收敛。而如果换用**随机**梯度下降——每一步只用随机抽到的一个样本来计算
$\nabla L$，而不是全部三个样本——w 的变化轨迹就不会像上表那样平滑下降，而会在 $w \approx 2$ 附近的同一个邻域内来回抖动，这正是第 2
节所描述的"噪声作为隐式正则化"效应的一个微缩演示。

---

## 8. Modern Puzzles: Double Descent and the Limits of Classical Theory

**当代的谜题：双下降现象与经典理论的局限**

§5's classical U-shaped picture of generalization — test error falling as capacity grows from
underfit toward a sweet spot, then rising again as the model overfits — describes real behavior in
small models, but Belkin and others, and, in a widely cited large-scale study, Nakkiran, Kaplun,
Bansal, Yang, Barak, and Sutskever (2019), showed that for models trained near the boundary where
they can just barely fit the training data exactly (the **interpolation threshold**),
test error can spike sharply — and then, surprisingly, _fall again_ as model capacity is increased
further past that threshold, sometimes reaching a lower test error than the best point on the
classical curve's "sweet spot" side. This is **double descent**: the test-error curve, as
a function of model size (or of training time, or of dataset size — the authors found analogous
effects along all three axes, unified under a single notion of "effective model complexity"), has
two descending regions separated by a spike, rather than the single classical U-shape.

第 5 节所描述的关于泛化的经典 U
形图景——测试误差随容量从欠拟合增长到某个甜蜜点而下降，随后随着模型过拟合而再度上升——确实描述了小模型中的真实行为，但
Belkin 等人以及 Nakkiran、Kaplun、Bansal、Yang、Barak 与 Sutskever（2019）在一项被广泛引用的大规模研究中发现：当模型训练到恰好能刚好精确拟合训练数据的边界附近（即**插值阈值**）时，测试误差会急剧飙升——然后，令人惊讶的是，当模型容量进一步超过这个阈值时，测试误差竟会*再次下降*，有时甚至能降到比经典曲线"甜蜜点"一侧最优点还要低的水平。这就是**双下降**：测试误差曲线——作为模型规模的函数（或者训练时长、数据集规模的函数——作者发现在这三个轴上都存在类似的效应，可以统一在"有效模型复杂度"这一单一概念之下）——呈现的是被一个尖峰隔开的两段下降区间，而不是经典理论中单一的
U 形曲线。

Why this happens is still an area of active research rather than settled theory, but one
influential intuition connects back to §2's observation about flat versus sharp minima: at the
interpolation threshold there is typically exactly one way to fit the training data exactly, and it
is often a sharp, poorly conditioned solution; once the model has enough capacity to have _many_
different ways of fitting the training data exactly, SGD's implicit bias tends to select flatter,
simpler-in-some-sense solutions among the many available, which generalize better. This is a
genuinely important caveat for how to read §5: raw parameter count alone does not predict
overfitting in modern, heavily overparameterized deep networks the way classical statistical
learning theory would suggest, and practitioners training very large models routinely rely on this
behavior rather than working against it.

为什么会发生这种现象，目前仍是一个活跃的研究方向，而非已有定论的理论，但一种颇具影响力的直觉与第 2
节中"平坦极小值与尖锐极小值"的观察联系了起来：在插值阈值处，通常恰好只有一种方式能精确拟合训练数据，而这种方式往往是一个尖锐、条件数很差的解；一旦模型的容量足够大，能够找到*许多种*不同的方式来精确拟合训练数据，SGD
的隐式偏好就倾向于在这众多可行解中选择更平坦、在某种意义上更"简单"的解，而这类解往往泛化得更好。这对我们该如何理解第
5
节，是一条真正重要的提醒：在现代、严重过参数化的深度网络中，单纯的参数数量并不能像经典统计学习理论所暗示的那样预测过拟合的发生，训练超大模型的实践者通常是在依赖这一行为，而不是在与之对抗。

---

## 9. Formal Generalization Bounds: A Brief Orientation

**形式化泛化界：简要导览**

The classical theoretical machinery for making §5's intuitions precise is rooted in the work of
Vapnik and Chervonenkis, formalized in Vapnik's 1995 book _The Nature of Statistical Learning
Theory_. The central object is the **VC dimension** of a hypothesis class — informally, the
largest number of points that some model in that class can perfectly separate in every possible way
they could be labeled (this property is called "shattering" the points). A hypothesis class
with a larger VC dimension is more expressive but requires proportionally more training data before
its empirical error reliably tracks its true error on the full distribution.

将第 5 节中的直觉精确化的经典理论工具，根植于 Vapnik 与 Chervonenkis 的工作，并在 Vapnik 1995 年的著作《The Nature of
Statistical Learning Theory》中被系统地形式化。其中的核心概念是一个假设类的 **VC 维**——通俗地说，就是该假设类中某个模型能够以所有可能的方式完美分开的最多点数（这种性质被称为"打散"这些点）。VC
维越大的假设类，表达能力越强，但也需要成比例地更多的训练数据，其经验误差才能可靠地反映它在完整分布上的真实误差。

A textbook treatment such as Mohri, Rostamizadeh, and Talwalkar's _Foundations of Machine
Learning_ states generalization bounds of the following schematic shape: with probability at least
$1 - \delta$ over the draw of the training set, the true error of any hypothesis in a class is bounded by
its training error plus a complexity term that grows with the VC dimension (or, in a more modern
and often tighter formulation, the **Rademacher complexity** of the class, a
quantity that measures how well the class can fit random noise) and shrinks as the number of
training examples n grows, roughly as $O(\sqrt{\text{complexity}/n})$. Applying this style of bound literally to
a modern deep network — whose parameter count, and therefore whose VC dimension, vastly exceeds the
number of training examples — would predict essentially vacuous (uninformatively loose) guarantees,
which is exactly the tension §8's double-descent findings and the Zhang et al. (2017)
random-label experiment made concrete: classical capacity-based bounds are mathematically valid but
empirically too pessimistic to explain why real deep networks generalize as well as they do, and
tightening this gap — for instance through bounds based on the flatness of the minimum found, the
implicit bias of SGD itself, or compression-based arguments — remains an active area of the
learning-theory research this module's author works in.

像 Mohri、Rostamizadeh 与 Talwalkar 的《Foundations of Machine Learning》这样的教科书，给出的泛化界大致呈现如下的示意形式：以至少
$1 - \delta$
的概率（这一概率是对训练集抽取过程而言的），某个假设类中任意假设的真实误差，被其训练误差加上一个随复杂度增长的项所界定——这个复杂度项可以是
VC 维，也可以是一种更现代、通常更紧的表述形式——**Rademacher 复杂度**，它衡量的是这个假设类拟合随机噪声的能力有多强——并且这个复杂度项会随着训练样本数量 n
的增大而缩小，大致以 $O(\sqrt{\text{复杂度}/n})$ 的速率下降。如果把这类界直接套用到一个现代深度网络上——它的参数数量、进而它的 VC
维，都远远超过训练样本的数量——得到的保证基本上会是空洞的（松到毫无信息量）；而这恰恰正是第 8 节的双下降发现，与 Zhang
等人（2017）随机标签实验所具体呈现出来的张力：经典的、基于容量的界在数学上是成立的，但在经验上却过于悲观，无法解释真实深度网络为何能泛化得如此之好；而缩小这一差距——例如借助基于所找到极小值平坦程度的界、基于
SGD 本身隐式偏好的界，或者基于压缩论证的界——仍然是本模块作者所从事的学习理论研究中一个活跃的方向。

---

## 10. Summary

**小结**

Training a neural network is a trajectory through parameter space, shaped by an optimizer (§§2–4)
that determines how quickly and stably the trajectory descends the loss landscape, and its
endpoint's quality is judged not by the training loss it reaches but by the generalization gap
between training and test performance (§5), which regularization techniques (§6) exist to narrow.
Modern deep networks routinely violate the intuitions of classical capacity-based theory — most
strikingly through double descent (§8) — which is why formal generalization bounds (§9), while
mathematically sound, remain an open frontier rather than a finished explanation of why deep
learning works as well as it empirically does.

训练一个神经网络，本质上是参数空间中的一条轨迹，其形状由一个优化器（第 2 至 4
节）所塑造——优化器决定了这条轨迹沿着损失曲面下降的速度与稳定性；而这条轨迹终点的好坏，评判标准并非它所达到的训练损失，而是训练性能与测试性能之间的泛化差距（第
5 节）——正则化技术（第 6 节）的存在正是为了缩小这一差距。现代深度网络经常违背经典的、基于容量的理论直觉——双下降现象（第 8
节）是其中最引人注目的例子——这正是为什么形式化的泛化界（第
9 节）尽管在数学上是严谨的，却依然是一片开放的前沿领域，而不是一份对深度学习为何在实践中表现如此出色的、已经完成的解释。

---

## References

**参考文献**

### External Sources

- [Robbins, H. and Monro, S. (1951). A Stochastic Approximation Method. The Annals of Mathematical Statistics, 22, 400–407.](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-22/issue-3/A-Stochastic-Approximation-Method/10.1214/aoms/1177729586.full)
- [Kingma, D. P. and Ba, J. (2014). Adam: A Method for Stochastic Optimization. arXiv:1412.6980.](https://arxiv.org/abs/1412.6980)
- [Loshchilov, I. and Hutter, F. (2017). Decoupled Weight Decay Regularization. arXiv:1711.05101.](https://arxiv.org/abs/1711.05101)
- [Loshchilov, I. and Hutter, F. (2016). SGDR: Stochastic Gradient Descent with Warm Restarts. arXiv:1608.03983.](https://arxiv.org/abs/1608.03983)
- [Geman, S., Bienenstock, E., and Doursat, R. (1992). Neural Networks and the Bias/Variance Dilemma. Neural Computation, 4(1), 1–58.](https://direct.mit.edu/neco/article/4/1/1/5624/Neural-Networks-and-the-Bias-Variance-Dilemma)
- [Zhang, C., Bengio, S., Hardt, M., Recht, B., and Vinyals, O. (2017). Understanding Deep Learning Requires Rethinking Generalization. arXiv:1611.03530.](https://arxiv.org/abs/1611.03530)
- [Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., and Salakhutdinov, R. (2014). Dropout: A Simple Way to Prevent Neural Networks from Overfitting. Journal of Machine Learning Research, 15, 1929–1958.](https://jmlr.org/papers/v15/srivastava14a.html)
- [Nakkiran, P., Kaplun, G., Bansal, Y., Yang, T., Barak, B., and Sutskever, I. (2019). Deep Double Descent: Where Bigger Models and More Data Hurt. arXiv:1912.02292.](https://arxiv.org/abs/1912.02292)
- [Vapnik, V. N. (1995). The Nature of Statistical Learning Theory. Springer, New York.](https://link.springer.com/book/10.1007/978-1-4757-3264-1)
- [Mohri, M., Rostamizadeh, A., and Talwalkar, A. (2018). Foundations of Machine Learning, 2nd Edition. MIT Press.](https://www.penguinrandomhouse.com/books/657853/foundations-of-machine-learning-second-edition-by-mehryar-mohri-afshin-rostamizadeh-and-ameet-talwalkar/)

### Internal Cross-References

- [`introductory/01-neural-networks-and-deep-learning-foundations.md`](../introductory/01-neural-networks-and-deep-learning-foundations.md) — neurons, layers, loss functions, backpropagation, and the basic gradient-descent update rule this module builds directly on.
- [`introductory/02-the-transformer-architecture-and-attention.md`](../introductory/02-the-transformer-architecture-and-attention.md) — the transformer architecture, the model family most modern training-dynamics research (including the scaling-law and double-descent literature cited above) is conducted on.
- [`advanced/01-scaling-laws-and-emergent-capabilities.md`](../advanced/01-scaling-laws-and-emergent-capabilities.md) — extends this module's optimization and generalization discussion to the scale of frontier language models, including a compute-optimal reframing of the capacity questions raised in §§8–9.
