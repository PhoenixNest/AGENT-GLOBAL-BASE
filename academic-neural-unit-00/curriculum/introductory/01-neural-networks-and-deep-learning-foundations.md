# Neural Networks & Deep Learning Foundations

**神经网络与深度学习基础**

| Field   | English                                                          | 中文                                    |
| ------- | ---------------------------------------------------------------- | --------------------------------------- |
| Level   | Introductory                                                     | 入门                                    |
| Cluster | Foundations                                                      | 基础                                    |
| Author  | Dr. Yuna Baek, Research Scientist — AI / Neural Networks, ANU-00 | ANU-00 AI/神经网络研究员 Yuna Baek 博士 |

---

This chapter assumes no prior exposure to machine learning, artificial intelligence, or programming
beyond basic arithmetic and algebra (variables, functions, summation). Every term is defined at
first use. Read it in full before moving to the next module in the sequence — later introductory,
intermediate, and advanced modules build directly on the vocabulary and mechanics introduced here.

本章不假设读者具备任何机器学习、人工智能或编程背景，仅要求掌握基础的算术与代数知识（变量、函数、求和）。所有术语均在首次出现时给出定义。请在进入课程序列的下一模块之前完整阅读本章——后续的入门、中级与高级模块都将直接建立在本章引入的词汇与机制之上。

---

## 1. What This Chapter Covers and Why It Matters

**本章内容与意义**

A neural network is, at its core, nothing mystical: it is a mathematical function — a rule that
takes numbers in and produces numbers out — built by chaining together many small, simple
mathematical operations.

神经网络本质上并不神秘：它就是一个数学函数——一条把若干数字作为输入、产出若干数字作为输出的规则——由许多微小而简单的数学运算连接而成。

What makes neural networks powerful is not that any single piece is complicated, but that stacking
thousands or billions of simple pieces together, and tuning their internal numbers automatically
from data, lets the resulting function approximate extraordinarily complex relationships:
recognizing a face in a photograph, translating a sentence, or predicting the next word in a
paragraph. This chapter builds that function from the ground up: one neuron, then a layer, then a
network, then the learning procedure that adjusts it.

神经网络之所以强大，并不是因为其中任何一个环节很复杂，而是因为将成千上万乃至数十亿个简单环节堆叠起来，并通过数据自动调节其内部数值，最终得到的函数就能够逼近极其复杂的关系：识别照片中的人脸、翻译一句话，或预测一段文字中的下一个词。本章将从零开始搭建这个函数：先是一个神经元，再到一层，再到一整个网络，最后是调整网络的学习过程。

Every module after this one — the Transformer architecture in [`introductory/02`](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md), attention mechanics
in [`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md), and mixture-of-experts variants in [`advanced/02`](https://anu00.dev/curriculum/advanced/02-mixture-of-experts-and-modern-architecture-variants.md) — is a refinement or
extension of the same core idea introduced here: numbers flow through layers of simple operations,
and a learning procedure adjusts the operations' internal numbers so that the output gets closer to
what is desired. Understanding this chapter thoroughly is the single highest -leverage investment in
the entire curriculum.

本模块之后的每一个模块——[`introductory/02`](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md) 中的 Transformer 架构、[`intermediate/02`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) 中的注意力机制细节，以及 [`advanced/02`](https://anu00.dev/curriculum/advanced/02-mixture-of-experts-and-modern-architecture-variants.md) 中的专家混合变体——都是对本章所引入这一核心思想的细化或扩展：数字流经一层层简单的运算，而学习过程会调整这些运算的内部数值，使输出逐渐逼近期望的结果。透彻理解本章，是整个课程体系中回报率最高的一项投入。

---

## 2. What Is a Neural Network? From Biological Inspiration to Mathematical Function

**什么是神经网络：从生物学启发到数学函数**

The name "neural network" comes from a loose analogy to biological brains, where neurons (nerve
cells) receive electrical/chemical signals from other neurons, combine them, and fire a signal
onward if the combined input is strong enough. Frank Rosenblatt's 1958 perceptron (感知机) — the first
precisely specified, computationally implemented artificial neuron model — was directly inspired by
this picture of biological signal combination and thresholding (Rosenblatt, 1958).

“神经网络”这一名称源自与生物大脑的一种松散类比：在大脑中，神经元接收来自其他神经元的电化学信号，将它们汇总，并在汇总后的输入足够强时向外发出信号。 Frank Rosenblatt 于 1958 年提出的感知机（perceptron）——第一个被精确定义并以计算方式实现的人工神经元模型——正是直接受到这种生物信号汇总与阈值判断图景的启发（Rosenblatt, 1958）。

The analogy should not be taken too literally: modern artificial neural networks are simplified
mathematical abstractions, not biologically accurate brain simulations. What survives from the
analogy, and what matters for this course, is the core computational pattern: combine several
numeric inputs, weight them by importance, and produce an output.

但这一类比不应被过度字面化理解：现代人工神经网络是经过简化的数学抽象，而非对大脑的生物学精确模拟。这一类比中真正延续下来、并且与本课程相关的，是其核心计算模式：将若干数值输入按重要程度加权组合，并产生一个输出。

A neural network, stripped of biological metaphor, is a parameterized function — a function whose
exact behavior is controlled by a large set of adjustable numbers called parameters, commonly split
into weights and biases.

抛开生物学隐喻，神经网络本质上是一个参数化函数——其具体行为由一大批可调节的数值控制，这些数值被称为参数，通常分为权重与偏置两类。

Given an input (for example, the pixel values of an image, or the numeric encoding of a word), the
network computes an output (for example, a probability that the image contains a cat, or a
probability distribution over the next word) by passing the input through a sequence of simple
mathematical transformations. "Training" a network means searching for parameter values that make
the function's outputs match desired outputs on example data, using a procedure covered in [§7](#7-how-a-network-learns-loss-functions)–[§9](#9-backpropagation-computing-gradients-efficiently) of
this chapter.

给定一个输入（例如一张图像的像素值，或一个词的数值编码），网络会通过一系列简单的数学变换，计算出一个输出（例如图像中包含猫的概率，或下一个词的概率分布）。“训练”一个网络，就是利用示例数据搜索能使函数输出与期望输出相匹配的参数取值，其具体过程将在本章第 7 至[第 9 节](#9-backpropagation-computing-gradients-efficiently)中介绍。

---

## 3. The Single Neuron: Weights, Bias, and Activation

**单个神经元：权重、偏置与激活函数**

The smallest building block of a neural network is a single artificial neuron, also called a unit.

神经网络最小的构成单元是单个人工神经元，也称为单元。

A neuron takes a fixed number of numeric inputs, $x_1, x_2, \ldots, x_n$, and computes a weighted
sum: it multiplies each input $x_i$ by a corresponding weight $w_i$ (a number representing how
important that input is to this neuron), adds all the products together, and adds one more
adjustable number called the bias $b$ (which shifts the result up or down independent of the inputs,
similar to the intercept in a line equation $y = mx + b$). This weighted sum is usually written $z =
w_1 x_1 + w_2 x_2 + \ldots + w_n x_n + b$, or more compactly using a dot product, $z = w \cdot x +
b$.

一个神经元接收固定数量的数值输入 $x_1, x_2, \ldots, x_n$，并计算它们的加权和：将每个输入 $x_i$ 乘以对应的权重 $w_i$（表示该输入对这个神经元的重要程度的数值），把所有乘积相加，再加上一个额外的可调数值——偏置 $b$（它与输入无关地整体上移或下移结果，类似直线方程 $y = mx + b$ 中的截距）。这个加权和通常写作 $z = w_1 x_1 + w_2 x_2 + \ldots + w_n x_n + b$，或用点积更简洁地表示为 $z = w \cdot x + b$。

The weighted sum $z$ alone is just a linear function of the inputs — and stacking linear functions
on top of each other produces only another linear function, no matter how many layers are used,
which severely limits what the network can represent. To give the network the ability to represent
curved, complex relationships, the weighted sum $z$ is passed through a nonlinear activation
function, producing the neuron's final output $a = f(z)$. [§4](#4-activation-functions-why-nonlinearity-matters) covers activation functions in depth;
for now, the essential shape of a single neuron is: **weighted sum, then nonlinearity**.

单独的加权和 $z$ 只是输入的一个线性函数——而无论叠加多少层，线性函数叠加线性函数得到的仍然只是另一个线性函数，这严重限制了网络的表达能力。为了让网络具备表达曲线型、复杂关系的能力，加权和 $z$ 会被送入一个非线性的激活函数，产生神经元的最终输出 $a = f(z)$。[第 4 节](#4-activation-functions-why-nonlinearity-matters)将深入介绍激活函数；目前只需记住单个神经元的基本形态是：**先加权求和，再做非线性变换**。

---

## 4. Activation Functions: Why Nonlinearity Matters

**激活函数：为何非线性至关重要**

An activation function $f$ takes the weighted sum $z$ and squashes, reshapes, or gates it into the
neuron's output $a$. Three activation functions recur throughout this curriculum.

激活函数 $f$ 接收加权和 $z$，将其压缩、重塑或“门控”为神经元的输出 $a$。本课程体系中会反复出现三种激活函数。

| Activation Function                                                           | EN                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 中文                                                                                                                                                                                                                                                                                |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sigmoid**（Sigmoid 函数）, $\sigma(z) = \dfrac{1}{1 + e^{-z}}$              | smoothly maps any real number into the open interval $(0, 1)$, making it a natural choice when an output should be interpreted as a probability; it was the default nonlinearity in the earliest multi-layer networks trained with backpropagation (Rumelhart, Hinton, and Williams, 1986).                                                                                                                                                                  | 能将任意实数平滑地映射到开区间 $(0, 1)$ 内，因此当输出需要被解释为概率时，它是自然的选择；在最早使用反向传播训练的多层网络中，它是默认的非线性函数（Rumelhart, Hinton, and Williams, 1986）。                                                                                       |
| **ReLU**（ReLU 函数, Rectified Linear Unit）, $\mathrm{ReLU}(z) = \max(0, z)$ | simply passes positive values through unchanged and clips negative values to zero; despite its simplicity, ReLU and its variants became the dominant activation function in deep networks because they are cheap to compute and avoid a problem called "vanishing gradients" that severely slows learning in very deep sigmoid-based networks (a problem that will make more concrete sense after [§9](#9-backpropagation-computing-gradients-efficiently)). | 的做法则更为直接：正值原样通过，负值一律裁剪为零；尽管形式简单，ReLU 及其变体已成为深度网络中占主导地位的激活函数，因为它计算成本低廉，并且能够避免一种被称为“梯度消失”的问题——这一问题会严重拖慢基于 sigmoid 的深层网络的学习速度（在第 9 节之后，这一问题的含义会更加具体清晰）。 |
| **Softmax**（Softmax 函数）                                                   | turns a whole vector of numbers into a probability distribution — every entry becomes a value between 0 and 1, and all entries sum to 1 — and is used when a network must choose among several discrete categories (for example, which of 10 digit classes an image shows, or which word in a vocabulary comes next).                                                                                                                                        | 则将一整个数值向量转化为一个概率分布——每个元素都变为 0 到 1 之间的值，且所有元素之和为 1——常用于网络需要在若干个离散类别中做出选择的场合（例如判断一张图像属于 10 个数字类别中的哪一个，或判断词表中下一个词是什么）。                                                              |

---

## 5. From One Neuron to a Network: Layers and Forward Propagation

**从单个神经元到网络：层与前向传播**

A single neuron can only represent a narrow class of functions. Real capability comes from arranging
many neurons into layers and stacking layers on top of each other.

单个神经元只能表达一类非常有限的函数。真正的表达能力来自于将大量神经元组织成层，并将多层依次堆叠起来。

| #   | Layer / Stage                              | EN                                                                                                                                                                                                         | 中文                                                                                                                 |
| --- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| 1   | **Input layer**（输入层）                  | simply holds the raw input numbers (for example, pixel intensities).                                                                                                                                       | 仅仅承载原始输入数值（例如像素强度）。                                                                               |
| 2   | One or more **hidden layers**（隐藏层）    | each contain several neurons; every neuron in a hidden layer typically receives the outputs of every neuron in the previous layer as its inputs — this is called a **fully connected** or **dense** layer. | 各自包含若干神经元；隐藏层中的每个神经元通常都以前一层所有神经元的输出作为自己的输入——这被称为**全连接层**或稠密层。 |
| 3   | **Output layer**（输出层）                 | produces the network's final answer, shaped to match the task (a single probability for a yes/no question, or a vector of probabilities for a multi-way classification).                                   | 产生网络的最终答案，其形态取决于具体任务（对于是/否问题输出单个概率值，对于多分类问题输出一个概率向量）。            |
| 4   | **Forward pass**（前向传播，也叫前向计算） | the process of computing outputs by pushing an input through the input layer, then each hidden layer in order, then the output layer.                                                                      | 将输入依次推送经过输入层、各个隐藏层、直至输出层来计算输出的过程。                                                   |

A network with at least one hidden layer between its input and output is often called a
**multi-layer perceptron** (MLP), and a network with many hidden layers is called "deep" — this is
the origin of the term **deep learning**: learning with networks that are deep, i.e., composed of
many stacked layers, rather than just one layer of weights.

在输入层和输出层之间至少包含一个隐藏层的网络，通常被称为**多层感知机**（MLP）；拥有很多隐藏层的网络则被称为“深层”网络——这正是**深度学习**这一术语的由来：使用“深”的网络进行学习，也就是由许多层堆叠而成的网络，而不仅仅是单层权重的网络。

---

## 6. A Worked Example: Forward Pass by Hand

**手算示例：前向传播**

To make [§3](#3-the-single-neuron-weights-bias-and-activation)–[§5](#5-from-one-neuron-to-a-network-layers-and-forward-propagation) concrete, consider the smallest possible network: a single neuron with two inputs,
sigmoid activation, and known numeric weights. This is a toy example — real networks have thousands
to billions of parameters — but the arithmetic is identical in kind, just repeated many more times.

为了让第 3 至[第 5 节](#5-from-one-neuron-to-a-network-layers-and-forward-propagation)的内容更加具体，来看一个最小规模的网络：一个拥有两个输入、使用 sigmoid 激活函数、权重已知的单一神经元。这只是一个玩具示例——真实的网络拥有成千上万乃至数十亿个参数——但其中的算术运算在本质上完全相同，只是被重复了更多次。

Suppose the inputs are $x_1 = 1.0$ and $x_2 = 0.5$, the weights are $w_1 = 0.4$ and $w_2 = -0.6$,
and the bias is $b = 0.1$. The weighted sum is:

假设输入为 $x_1 = 1.0$ 和 $x_2 = 0.5$，权重为 $w_1 = 0.4$ 和 $w_2 = -0.6$，偏置为 $b = 0.1$。加权和为：

$$z = w_1 x_1 + w_2 x_2 + b = (0.4)(1.0) + (-0.6)(0.5) + 0.1 = 0.4 - 0.3 + 0.1 = 0.2$$

Passing $z = 0.2$ through the sigmoid activation gives the neuron's output:

将 $z = 0.2$ 代入 sigmoid 激活函数，可得该神经元的输出：

$$a = \sigma(0.2) = \frac{1}{1 + e^{-0.2}} \approx 0.5498$$

This single number, $a \approx 0.5498$, is the neuron's forward-pass output — for example, if this
neuron were the entire network and the task were a yes/no classification, `0.5498` could be
interpreted as "54.98% confident the answer is yes." [§7](#7-how-a-network-learns-loss-functions) continues this exact example to show how the
network's parameters get adjusted when this output is wrong.

这个数字 $a \approx 0.5498$ 就是该神经元前向传播的输出——例如，如果这个神经元就是整个网络，任务是一个是/否分类问题，那么 `0.5498` 可以被解释为“有 54.98% 的把握认为答案是'是'”。[第 7 节](#7-how-a-network-learns-loss-functions)将继续沿用这个例子，说明当这一输出出现偏差时，网络的参数是如何被调整的。

---

## 7. How a Network Learns: Loss Functions

**网络如何学习：损失函数**

A freshly initialized network — one whose weights and biases are set to small random numbers before
any training — produces essentially useless outputs. Learning is the process of adjusting weights
and biases so that the network's outputs get closer to correct answers on a set of example inputs
whose correct answers ("labels" or "targets") are already known — this collection of labeled
examples is called the **training data**. To adjust parameters in a principled direction, the
network needs a single number that measures "how wrong" its current output is; this number is
produced by a **loss function**, also called a cost function or objective function.

一个刚刚初始化的网络——即在训练开始之前，权重和偏置被设置为较小的随机数——所产生的输出基本上是无用的。学习就是不断调整权重和偏置，使网络在一组输入示例上的输出逐渐逼近已知的正确答案（这些正确答案被称为“标签”或“目标值”）的过程——这一批带有标签的示例集合被称为**训练数据**。为了以有原则的方式调整参数，网络需要一个单一的数值来衡量当前输出“错得有多离谱”；这个数值由**损失函数**产生，也称为代价函数或目标函数。

Continuing the worked example from [§6](#6-a-worked-example-forward-pass-by-hand): suppose the true target for this input is $y = 1$ (meaning
the correct answer is "yes"), but the network's output was $a \approx 0.5498$. A common loss
function for this kind of problem is the **squared error** loss, $L = \tfrac{1}{2}(y - a)^2$, which
is small when $a$ is close to `y` and grows quadratically as $a$ moves away from `y`. Plugging in
the numbers:

延续[第 6 节](#6-a-worked-example-forward-pass-by-hand)中的示例：假设该输入的真实目标为 $y = 1$（即正确答案是“是”），而网络的输出为 $a \approx 0.5498$。针对此类问题，常用的损失函数是**平方误差**损失 $L = \tfrac{1}{2}(y - a)^2$——当 $a$ 接近 `y` 时该值很小，而当 $a$ 偏离 `y` 时则以平方的速度增大。代入数值：

$$L = \tfrac{1}{2}(1 - 0.5498)^2 = \tfrac{1}{2}(0.4502)^2 \approx 0.1014$$

A loss of `0.1014` is the network's "score" for this one example — the goal of training is to adjust
$w_1$, $w_2$, and $b$ so that this score gets smaller. [§8](#8-gradient-descent-finding-the-downhill-direction) and [§9](#9-backpropagation-computing-gradients-efficiently) explain exactly how that adjustment
is computed.

`0.1014` 这个损失值就是网络在这一个示例上的“得分”——训练的目标就是不断调整 $w_1$、$w_2$ 和 $b$，使这个得分不断减小。[第 8 节](#8-gradient-descent-finding-the-downhill-direction)与[第 9 节](#9-backpropagation-computing-gradients-efficiently)将具体说明这一调整过程是如何计算出来的。

---

## 8. Gradient Descent: Finding the Downhill Direction

**梯度下降：寻找下坡方向**

Imagine the loss $L$ as a landscape — a surface whose height at any point is determined by the
current values of all the network's weights and biases. Training seeks the lowest point (or a
sufficiently low point) of this landscape, since low loss means accurate predictions.

可以把损失 $L$ 想象成一片地形——地形上任意一点的高度由网络当前所有权重与偏置的取值决定。训练的目标是寻找这片地形的最低点（或足够低的点），因为损失越低意味着预测越准确。

**Gradient descent** is the standard algorithm for finding a low point: at the network's current
parameter values, compute the **gradient** — the direction in which the loss increases fastest,
formally the vector of partial derivatives of the loss with respect to each parameter — and then
take a small step in the _opposite_ direction (downhill), since moving opposite to the direction of
steepest increase decreases the loss fastest. This step is repeated many times.

**梯度下降**是寻找低点的标准算法：在网络当前的参数取值处，计算**梯度**——损失增长最快的方向，形式上是损失相对于每个参数的偏导数所构成的向量——然后朝其*相反*方向（即下坡方向）迈出一小步，因为沿最陡上升方向的反方向移动能最快地降低损失。这一步骤会被反复重复执行。

Formally, each parameter $\theta$ (a stand-in for any weight or bias) is updated by the rule $\theta
\leftarrow \theta - \eta \cdot (\partial L/\partial \theta)$, where $\partial L/\partial \theta$ is
the partial derivative of the loss with respect to that parameter (how much the loss would change
for a tiny change in that parameter, holding all others fixed), and $\eta$ (eta) is the **learning
rate** — a small positive number, typically set by the practitioner, that controls how large each
step is.

形式上，每个参数 $\theta$（代表任意一个权重或偏置）都按照规则 $\theta \leftarrow \theta - \eta \cdot (\partial L/\partial \theta)$ 进行更新，其中 $\partial L/\partial \theta$ 是损失相对于该参数的偏导数（表示在保持其他参数不变的前提下，该参数发生微小变化时损失会如何变化），而 $\eta$（希腊字母 eta）则是**学习率**——一个通常由使用者设定的较小正数，用于控制每一步迈出的幅度大小。

A learning rate that is too large can overshoot the low point and fail to converge; one that is too
small makes training impractically slow. [§9](#9-backpropagation-computing-gradients-efficiently) explains how $\partial L/\partial \theta$ is actually
computed for every parameter in a network, however deep.

学习率过大可能会越过最低点而无法收敛；学习率过小则会使训练过程慢得不切实际。[第 9 节](#9-backpropagation-computing-gradients-efficiently)将说明，无论网络有多深，$\partial L/\partial \theta$ 究竟是如何针对每一个参数计算出来的。

---

## 9. Backpropagation: Computing Gradients Efficiently

**反向传播：高效计算梯度**

For a network with millions or billions of parameters spread across many layers, computing the
gradient $\partial L/\partial \theta$ for every parameter one at a time, from scratch, would be
computationally infeasible. **Backpropagation**, short for "backward propagation of errors," is the
algorithm that makes this efficient.

对于一个参数分布在众多层中、数量可达数百万乃至数十亿的网络而言，若要逐个从头计算每个参数的梯度 $\partial L/\partial \theta$，在计算上是不可行的。 **反向传播**（“误差反向传播”的简称）正是使这一计算变得高效的算法。

It works by applying the **chain rule** from calculus (the rule for differentiating a function
composed of other functions) systematically, layer by layer, starting from the output layer and
working backward toward the input layer — hence the name. Rumelhart, Hinton, and Williams's 1986
paper popularized this algorithm for training multi-layer networks and showed that it lets hidden
layers automatically discover useful internal representations of the task, rather than requiring a
human to hand-design them (Rumelhart, Hinton, and Williams, 1986).

它系统性地运用微积分中的**链式法则**（即对由若干函数复合而成的函数求导的法则），从输出层开始，逐层向输入层方向反向推进——这也是该算法名称的由来。 Rumelhart、Hinton 和 Williams 于 1986 年发表的论文推广了这一用于训练多层网络的算法，并证明了它能让隐藏层自动发现对任务有用的内部表示，而无需人工手动设计这些表示（Rumelhart, Hinton, and Williams, 1986）。

Continuing the worked example from [§6](#6-a-worked-example-forward-pass-by-hand)–[§7](#7-how-a-network-learns-loss-functions): to update weight $w_1$, backpropagation applies the chain
rule to decompose $\partial L/\partial w_1$ into three factors — how the loss changes with the
output $a$, how the output changes with the weighted sum $z$, and how the weighted sum changes with
$w_1$:

延续第 6 至[第 7 节](#7-how-a-network-learns-loss-functions)中的示例：为了更新权重 $w_1$，反向传播运用链式法则将 $\partial L/\partial w_1$ 分解为三个因子——损失相对于输出 $a$ 的变化率、输出相对于加权和 $z$ 的变化率，以及加权和相对于 $w_1$ 的变化率：

$$\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial a} \cdot \frac{\partial a}{\partial z} \cdot \frac{\partial z}{\partial w_1}$$

The first factor, the derivative of $\tfrac{1}{2}(y-a)^2$ with respect to $a$:

第一个因子，$\tfrac{1}{2}(y-a)^2$ 对 $a$ 的偏导数：

$$\frac{\partial L}{\partial a} = -(y - a) = -(1 - 0.5498) = -0.4502$$

The second factor, the derivative of the sigmoid:

第二个因子，sigmoid 函数的导数：

$$\frac{\partial a}{\partial z} = a(1 - a) = 0.5498 \times 0.4502 \approx 0.2475$$

The third factor, the derivative of $w_1 x_1 + w_2 x_2 + b$ with respect to $w_1$:

第三个因子，$w_1 x_1 + w_2 x_2 + b$ 对 $w_1$ 的偏导数：

$$\frac{\partial z}{\partial w_1} = x_1 = 1.0$$

Multiplying the three factors together:

将这三个因子相乘：

$$\frac{\partial L}{\partial w_1} = (-0.4502)(0.2475)(1.0) \approx -0.1114$$

With a learning rate $\eta = 0.1$, the update rule from [§8](#8-gradient-descent-finding-the-downhill-direction) gives a new value for $w_1$:

取学习率 $\eta = 0.1$，代入[第 8 节](#8-gradient-descent-finding-the-downhill-direction)中的更新规则，即可得到 $w_1$ 的新取值：

$$w_1^{\text{new}} = w_1 - \eta \cdot \frac{\partial L}{\partial w_1} = 0.4 - (0.1)(-0.1114) \approx 0.4111$$

$w_1$ increased slightly, from `0.4` to approximately `0.4111`. Intuitively this makes sense: since
$x_1$ was positive and the network under-predicted (output `0.5498` was less than target `1`),
increasing the weight on $x_1$ pushes the output slightly higher, toward the target — exactly the
correction gradient descent is designed to make. The same chain-rule mechanics apply to $w_2$, $b$,
and to every parameter in every layer of a much larger network; backpropagation is simply this same
computation, organized layer by layer, reusing intermediate results so the whole gradient can be
computed in roughly the same amount of work as one forward pass.

$w_1$ 从 `0.4` 略微增大到约 `0.4111`。这在直觉上是合理的：由于 $x_1$ 为正值，且网络的预测偏低（输出 `0.5498` 小于目标值 `1`），增大 $x_1$ 对应的权重会使输出略微升高，向目标值靠拢——这正是梯度下降所要做出的修正。同样的链式法则运算同样适用于 $w_2$、$b$，以及一个规模大得多的网络中每一层的每一个参数；反向传播不过是把这同一种计算按层组织起来，并复用中间结果，从而使整个梯度的计算量大致与一次前向传播相当。

---

## 10. The Training Loop, Epochs, and Batches

**训练循环、轮次与批次**

Real training repeats the forward pass, loss computation, backpropagation, and parameter update
across the entire training dataset, many times over. One full pass through the entire training
dataset is called an **epoch** (轮次/回合).

真正的训练过程会在整个训练数据集上反复执行前向传播、损失计算、反向传播与参数更新，如此循环往复多次。完整遍历一次训练数据集的过程被称为一个**轮次**（epoch）。

In practice, parameters are usually not updated after every single example (which is noisy and slow)
nor only after the entire dataset (which is memory-intensive and updates too infrequently); instead,
the training data is split into small groups called **batches** or **mini-batches** (批/小批量), and one
parameter update is performed per batch, using the average gradient across the examples in that
batch. This approach — **mini-batch gradient descent** — balances computational efficiency with
stable, frequent learning progress, and is the default in essentially all modern deep learning
training.

在实践中，参数通常既不会在每处理一个样本后就更新一次（这样噪声太大且速度过慢），也不会等到遍历完整个数据集后才更新一次（这样对内存要求过高，且更新频率过低）；取而代之的是，训练数据会被划分为若干个小组，称为**批次**或**小批量**（batch / mini-batch），每处理完一个批次就执行一次参数更新，更新时使用该批次内所有样本梯度的平均值。这种方法——**小批量梯度下降**（mini-batch gradient descent）——在计算效率与稳定、频繁的学习进展之间取得了平衡，也是当今几乎所有深度学习训练的默认做法。

---

## 11. Overfitting, Underfitting, and Generalization

**过拟合、欠拟合与泛化**

The ultimate goal of training is not to make the network perform well only on the exact examples it
was trained on, but to make it perform well on new, previously unseen examples — this ability is
called **generalization** (泛化). To measure generalization honestly, practitioners set aside a
portion of labeled data, called the **validation set** or **test set**, that the network never
trains on, and periodically check performance on it.

训练的最终目标并不是让网络仅仅在训练时所见过的确切样本上表现良好，而是要让它在全新的、此前从未见过的样本上也表现良好——这种能力被称为**泛化**（generalization）。为了客观地衡量泛化能力，实践者通常会预留出一部分带标签的数据，称为**验证集**（validation set）或**测试集**（test set），网络在训练过程中从不接触这部分数据，并会定期在其上检查性能。

**Overfitting** (过拟合) occurs when a network becomes so finely tuned to the specific training examples — including their noise and idiosyncrasies — that its performance on the training set keeps improving while its performance on the held-out validation set stalls or gets worse; the network has essentially memorized the training data rather than learning generalizable patterns. **Underfitting** (欠拟合) is the opposite failure: the network is too simple, or was not trained long enough, to capture even the patterns present in the training data, so performance is poor on both training and validation data.

**过拟合**（overfitting）指的是网络过度贴合特定的训练样本——包括其中的噪声与个别特性——以至于训练集上的表现不断提升，而在预留出的验证集上的表现却停滞不前甚至变差；此时网络实际上是在死记硬背训练数据，而没有学到可泛化的规律。 **欠拟合**（underfitting）则是相反的失败模式：网络过于简单，或训练时间不足，甚至无法捕捉训练数据中本就存在的规律，因此在训练集和验证集上的表现都很差。

---

## 12. Deep Learning: Why "Deep"?

**深度学习：为何是“深”**

A landmark theoretical result — often called the **universal approximation theorem** — shows that
even a network with just a single hidden layer can, in principle, approximate any continuous
function to arbitrary accuracy, given enough neurons in that layer. This might suggest depth (many
layers) is unnecessary.

一项具有里程碑意义的理论结果——通常被称为**通用逼近定理**（universal approximation theorem）——表明，只要隐藏层中神经元数量足够多，即便是仅含单个隐藏层的网络，原则上也能以任意精度逼近任何连续函数。这似乎意味着深度（即多层结构）并非必要。

In practice, however, deep networks — many layers, each learning increasingly abstract features
built on the previous layer's features — tend to represent complex functions far more compactly
(with far fewer total parameters) and learn more effectively from data than shallow-but-wide
networks that try to achieve the same accuracy with a single very large hidden layer, which is a
central motivation for the field being called "deep" learning rather than simply "neural network"
learning.

然而在实践中，深层网络——由许多层构成，每一层都在前一层特征的基础上学习更加抽象的特征——往往能够以远为紧凑的方式（即使用远少得多的参数总量）表示复杂函数，其从数据中学习的效果也往往优于试图用单个极大的隐藏层达到同等精度的“浅而宽”的网络，这正是该领域被称为“深度”学习而非仅仅是“神经网络”学习的核心原因之一。

Deep learning practice, discussed in detail in Goodfellow, Bengio, and Courville's textbook, treats
depth itself — not just raw parameter count — as a resource that shapes what a network can
efficiently learn (Goodfellow, Bengio, and Courville, 2016).

Goodfellow、Bengio 与 Courville 所著教材对深度学习实践有详细论述，该书将深度本身——而不仅仅是参数总量——视为一种决定网络能够高效学到什么的资源（Goodfellow, Bengio, and Courville, 2016）。

---

## 13. Summary and What Comes Next

**小结与后续内容**

This chapter built a neural network from its smallest piece upward: a single neuron (weighted sum
plus nonlinear activation), assembled into layers, assembled into a full network, evaluated with a
loss function, and improved through gradient descent driven by gradients computed with
backpropagation. It also introduced the vocabulary — training data, epochs, batches, overfitting,
generalization, depth — used throughout the rest of this curriculum. Every one of these mechanics
carries forward unchanged into more advanced architectures; what changes going forward is not the
learning procedure itself, but the internal structure of the function being learned.

本章从最小的构成单元开始，逐步搭建起一个完整的神经网络：单个神经元（加权求和加非线性激活）、组装成层、组装成完整网络，用损失函数进行评估，并通过反向传播计算梯度、经梯度下降不断改进。本章还引入了贯穿本课程体系其余部分的词汇——训练数据、轮次、批次、过拟合、泛化、深度。这些机制中的每一项都会原封不动地延续到更高级的架构之中；真正发生变化的并非学习过程本身，而是所学函数的内部结构。

`introductory/02-the-transformer-architecture-and-attention.md` picks up exactly where this chapter
leaves off, introducing the Transformer — the specific layered architecture, built from the neurons,
layers, activations, and training procedure defined here, that underlies essentially every modern
large language model.

`introductory/02-the-transformer-architecture-and-attention.md` 将紧接本章内容继续展开，介绍 Transformer——一种基于本章所定义的神经元、层、激活函数与训练流程构建而成的特定层级架构，也是当今几乎所有大型语言模型的基础。

---

## References

**参考文献**

### External Sources

- [Rosenblatt, F. (1958). The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain. _Psychological Review_, 65(6), 386–408.](https://pubmed.ncbi.nlm.nih.gov/13602029/)
- [Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). Learning representations by back-propagating errors. _Nature_, 323, 533–536.](https://www.nature.com/articles/323533a0)
- [Goodfellow, I., Bengio, Y., & Courville, A. (2016). _Deep Learning_. MIT Press.](https://www.deeplearningbook.org/)
- [Nielsen, M. (2015). _Neural Networks and Deep Learning_ (free online book).](http://neuralnetworksanddeeplearning.com/)

### Internal Cross-References

- [`introductory/02-the-transformer-architecture-and-attention.md`](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md) — builds directly on the neuron/layer/training vocabulary defined here.
- [`intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md`](https://anu00.dev/curriculum/intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) — extends the attention mechanism introduced in [`introductory/02`](https://anu00.dev/curriculum/introductory/02-the-transformer-architecture-and-attention.md).
- [`advanced/02-mixture-of-experts-and-modern-architecture-variants.md`](https://anu00.dev/curriculum/advanced/02-mixture-of-experts-and-modern-architecture-variants.md) — extends the layer/network vocabulary from this chapter into sparse architectures.
