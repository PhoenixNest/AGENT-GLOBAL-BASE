# Advanced Context Engineering: Long-Context & Context Budgeting

**高级上下文工程：长上下文与上下文预算**

| Field   | English                      | 中文                                            |
| ------- | ---------------------------- | ----------------------------------------------- |
| Level   | Advanced                     | 高级                                            |
| Cluster | Prompt & Context Engineering | 提示与上下文工程                                |
| Author  | Dr. Wei-Ling Tan,            | ANU-00 应用人工智能系统研究员 Wei-Ling Tan 博士 |

---

This chapter builds strictly on three earlier curriculum modules and names each explicitly
wherever it depends on them. From `introductory/06-context-windows-tokens-and-memory-basics.md`
it assumes the reader already has working definitions of token and context window. From
`intermediate/05-advanced-prompting-cot-few-shot-structured-output.md` §1 it
assumes the reader already understands that few-shot examples consume a share of a fixed context
window, and picks up directly from the "context-budget trade-off" that section named but did not
develop. From `intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md` it
assumes, without re-deriving, the $O(n^2)$ computational cost of self-attention (§4), the KV cache
mechanism and its memory formula $2 \times L \times H \times d_h \times n \times p$ (§7), and the rotary position embedding
(RoPE) and ALiBi positional schemes (§9) — that module's own §4 explicitly named this chapter as
the place where "architectural mitigations for long-context processing" would be covered in depth,
and this chapter is that continuation.

本章严格建立在三个此前的课程模块之上，并在依赖它们之处逐一明确点名。本章假定读者已经从《上下文窗口、词元与记忆基础》(`introductory/06-context-windows-tokens-and-memory-basics.md`)中掌握了词元与上下文窗口的基本定义。本章假定读者已经从《进阶提示工程：思维链、少样本与结构化输出》(`intermediate/05-advanced-prompting-cot-few-shot-structured-output.md`)第1节中理解了少样本示例会占用固定上下文窗口的一部分份额，并直接接续该节提到但未展开的"上下文预算权衡"问题继续讲授。本章还假定读者已经从《注意力机制深入解析：多头注意力、KV 缓存与位置编码》(`intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md`)中掌握了自注意力 $O(n^2)$ 的计算成本(第4节)、KV 缓存机制及其内存公式 $2 \times L \times H \times d_h \times n \times p$(第7节)、以及旋转位置编码(RoPE)与 ALiBi 这两种位置编码方案(第9节)，本章不再重新推导这些内容——该模块第4节中明确点名，"应对长上下文处理的架构层面缓解方案"将由本章深入讲解，本章正是这一延续。

This chapter has two parts. Sections 2 through 6 examine long context as a hard engineering and
scientific problem: why the underlying architecture resists naive extension, what actually happens
to a model's accuracy as context grows, and how the field measures that empirically — including
where the standard measurement itself is contested. Sections 7 through 9 then turn to context
budgeting: the practical discipline, used daily by anyone building a production LLM application, of
treating a finite context window as a resource to be actively allocated and managed rather than
filled passively.

本章分为两个部分。第2至第6节将长上下文视为一个真正棘手的工程与科学问题来考察：底层架构为何会抵抗简单粗暴的扩展、随着上下文增长模型的准确率究竟会发生什么、以及这一领域如何对此进行实证测量——其中也包括标准测量方法本身存在争议的地方。第7至第9节随后转向上下文预算：这是任何构建生产级大语言模型应用的人日常都要用到的实践纪律——把有限的上下文窗口当作一种需要主动分配和管理的资源，而不是被动地被填满。

## 1. Recap and Scope

**回顾与范围**

Three facts from the prerequisite modules set up everything that follows. First,
`introductory/06` established that every model has a fixed maximum context window measured in
tokens, and that both the prompt and the model's own generated output must fit inside it together.
Second, `intermediate/02` §4 established that the compute and memory required by self-attention
grow quadratically, $O(n^2)$, with sequence length `n` — doubling the input length quadruples the
attention computation. Third, `intermediate/02` §7 established that autoregressive generation
additionally requires a KV cache whose memory grows linearly with `n`, following the formula
$2 \times L \times H \times d_h \times n \times p$. Put together, these three facts mean that "just make the context window
bigger" is never a free engineering choice — it has a compute cost that grows worse than linearly,
a memory cost that grows linearly and multiplies across every concurrent request a server handles,
and, as this chapter's Sections 5–6 show, no guarantee that a model actually uses everything inside
a larger window equally well.

前置模块中的三点事实，构成了本章后续内容的基础。第一，《上下文窗口、词元与记忆基础》确立了：每个模型都有一个以词元数衡量的固定最大上下文窗口，提示词本身与模型自己生成的输出必须共同容纳在这个窗口之内。第二，《注意力机制深入解析》第4节确立了：自注意力所需的计算量与内存量都随序列长度 `n` 呈平方级增长，即 $O(n^2)$——输入长度翻倍，注意力计算量就变为原来的四倍。第三，该模块第7节确立了：自回归生成还额外需要一个 KV 缓存，其内存开销随 `n` 线性增长，遵循公式 $2 \times L \times H \times d_h \times n \times p$。综合这三点可以看出："干脆把上下文窗口做大一点"从来都不是一个没有代价的工程选择——它带来的计算成本增长快于线性，内存成本随线性增长、并会在服务器同时处理的每一个并发请求上成倍累加，而且正如本章第5至第6节将会展示的那样，窗口变大也并不能保证模型能够同样好地利用窗口内的所有内容。

## 2. The Position-Extrapolation Problem

**位置外推问题**

`intermediate/02` §9 described RoPE as encoding a token's position by rotating its query and key
vectors by an angle that depends on that token's position index, and noted that Su et al. (2021)
prove the resulting attention score depends only on the _relative_ distance between two positions.
This relative-distance property is what makes RoPE, in principle, applicable to sequences of any
length. In practice, however, a model trained with RoPE only ever sees position indices up to some
maximum length `L_train` during training — its attention layers never learn what to do with the
rotation angles that correspond to positions beyond `L_train`. Chen et al. (2023), in "Extending
Context Window of Large Language Models via Positional Interpolation," describe directly evaluating
a RoPE-based model at position indices beyond its training length and finding that attention scores
at those unseen, "extrapolated" positions can become anomalously large, degrading the model's
output quality catastrophically rather than gracefully — the model does not merely get somewhat
worse beyond `L_train`, it can effectively break.

《注意力机制深入解析》第9节曾介绍，RoPE 是通过一个取决于 token 位置索引的角度，对查询向量和键向量进行旋转，以此编码位置信息，并指出 Su 等人(2021)证明了由此得到的注意力得分只取决于两个位置之间的*相对*距离。正是这一相对距离特性，使得 RoPE 在原理上可以适用于任意长度的序列。然而在实践中，一个用 RoPE 训练出来的模型，在训练过程中所见过的位置索引最多只到某个上限 `L_train`——它的注意力层从未学习过该如何处理超出 `L_train` 所对应的那些旋转角度。Chen 等人(2023)在论文《Extending Context Window of Large Language Models via Positional Interpolation》中，直接评估了一个基于 RoPE 的模型在超出其训练长度的位置索引上的表现，发现这些从未见过的"外推"位置上的注意力得分可能会异常增大，导致模型输出质量出现灾难性的、而非渐进式的下降——模型在超出 `L_train` 之后，并不只是"稍微变差一点"，而是有可能实际上直接失效。

Chen et al.'s proposed fix, **Position Interpolation (PI)**, is deliberately simple: instead of
letting a token's position index run up to the new, longer target length directly, PI linearly
rescales every position index by the ratio `L_train / L_target` before it enters the RoPE rotation,
so that even a token near the end of a much longer sequence is presented to the rotation
mathematics with an index that stays within the range the model saw during training. Because this
interpolated range was seen during training, the paper reports that a model needs only a small
amount of additional fine-tuning — within 1,000 steps in their experiments — to adapt cleanly to
the new, longer effective context length, in contrast to the catastrophic quality loss of naive
extrapolation. Chen et al. demonstrate extending LLaMA models to context windows up to 32,768
tokens using this method.

Chen 等人提出的解决方案——**位置插值(Position Interpolation, PI)**——刻意设计得很简单：与其让 token 的位置索引直接一路增长到新的、更长的目标长度，PI 会先按比例 `L_train / L_target` 对每一个位置索引做线性缩放，再将其送入 RoPE 的旋转计算，这样一来，即便是位于一个长得多的序列末尾附近的 token，呈现给旋转计算的位置索引，依然落在模型训练时所见过的范围之内。由于这个经过插值缩放的范围在训练时已经被模型见过，论文报告称，模型只需要少量额外的微调——在他们的实验中不超过1000步——就能干净利落地适应新的、更长的有效上下文长度，这与朴素外推所带来的灾难性质量下降形成了鲜明对比。Chen 等人展示了用这一方法将 LLaMA 系列模型的上下文窗口扩展到最多 32,768 个 token。

## 3. YaRN: Combining Interpolation with Attention Scaling

**YaRN：插值与注意力缩放的结合**

Peng et al. (2023), in "YaRN: Efficient Context Window Extension of Large Language Models," build
on the interpolation idea in two ways. First, rather than rescaling every RoPE dimension by the
same uniform ratio as plain Position Interpolation does, YaRN applies what the paper calls
"NTK-by-parts" interpolation: different dimensions of the rotation are rescaled by different
amounts, because — as the paper's analysis shows — the dimensions of RoPE that rotate fastest
(encoding fine-grained, short-range position information) and those that rotate slowest (encoding
coarse-grained, long-range position information) are not equally harmed by naive interpolation, so
treating them uniformly wastes some of the model's existing positional resolution. Second, YaRN
adds a temperature-like scaling adjustment to the attention computation itself to compensate for a
subtle side effect of interpolation on the distribution of attention scores. Peng et al. report
that YaRN reaches state-of-the-art context-extension results using only about 0.1% of the original
pretraining corpus and roughly 400 training steps — substantially less additional training than
prior extension methods required, while extrapolating beyond even the interpolated training range
better than Position Interpolation alone.

Peng 等人(2023)在论文《YaRN: Efficient Context Window Extension of Large Language Models》中，从两个方面在插值这一思路的基础上做了改进。第一，YaRN 并不像朴素的位置插值那样对 RoPE 的每一个维度都采用同一个统一的缩放比例，而是采用了论文中所称的"分部 NTK"(NTK-by-parts)插值：旋转的不同维度会按不同幅度分别缩放，因为——正如论文的分析所显示的——RoPE 中旋转最快的维度(编码精细的短距离位置信息)与旋转最慢的维度(编码粗粒度的长距离位置信息)，受朴素插值的损害程度并不相同，若对它们一视同仁地处理，就会浪费模型原本已经具备的部分位置分辨能力。第二，YaRN 还对注意力计算本身加入了一个类似"温度"的缩放调整，用以补偿插值对注意力得分分布所带来的一种细微副作用。Peng 等人报告称，YaRN 仅使用约0.1%的原始预训练语料、大约400个训练步骤，就达到了当时最先进的上下文扩展效果——所需的额外训练量远小于此前的扩展方法，同时在超出插值训练范围之外的外推表现上，也优于单纯的位置插值。

For a prompt engineer rather than a model trainer, the practical takeaway from Sections 2 and 3 is
not that these techniques must be implemented directly — they are applied by the organizations that
train and release long-context models — but that a model's advertised maximum context length is
not a free architectural fact; it is the product of a specific extension technique applied during
or after training, and different techniques trade off differently between extension size, the
amount of additional training required, and how gracefully performance degrades near and beyond the
advertised limit. This is why Sections 5–6 evaluate long-context claims empirically rather than
taking an advertised window size at face value.

对于提示工程师(而非模型训练者)而言，第2节与第3节带来的实际启示，并不是说这些技术必须由使用者亲自实现——它们是由训练并发布长上下文模型的机构应用的——而是说，一个模型所宣称的最大上下文长度，并不是一个凭空存在的架构事实；它是训练期间或训练之后所应用的某种特定扩展技术的产物，而不同的技术在"能扩展多长""需要多少额外训练"以及"在宣称的极限附近及之外性能会以多平滑的方式下降"这几个方面，各有不同的权衡取舍。这正是为什么第5至第6节要用实证的方式来评估长上下文的相关宣称，而不是对宣称的窗口大小照单全收。

## 4. Distributing Attention Across Devices: Ring Attention

**跨设备分布式注意力：环形注意力**

Sections 2–3 addressed making a trained model's positional encoding work correctly at longer
lengths. A separate problem is purely computational: `intermediate/02` §4's $O(n^2)$ cost means
that, for a sufficiently long sequence, the attention score matrix alone may not fit in a single
device's memory regardless of positional encoding. Liu, Zaharia, and Abbeel (2023), in "Ring
Attention with Blockwise Transformers for Near-Infinite Context," address this by distributing the
sequence itself across multiple devices arranged in a logical ring: each device holds only a block
of the full sequence's queries, keys, and values, computes attention for its own block, and then
passes its block of keys and values to the next device in the ring while simultaneously receiving
the previous device's block — overlapping this communication with the ongoing attention computation
so that, ideally, the communication cost is hidden behind computation rather than adding to it. The
paper reports that this blockwise, ring-communicated approach enables training and inference on
sequences whose length scales with the _number of devices_ used, rather than being capped by any
single device's memory — a mechanism the paper's title calls "near-infinite context" specifically
because the practical limit becomes cluster size rather than a fixed architectural ceiling.

第2至第3节讨论的是如何让一个已经训练好的模型的位置编码，在更长的长度下依然正确工作。另一个独立的问题则纯粹是计算层面的：《注意力机制深入解析》第4节所述的 $O(n^2)$ 开销意味着，对于足够长的序列，无论采用何种位置编码，单单是注意力得分矩阵本身就可能装不进单个设备的内存。Liu、Zaharia 与 Abbeel(2023)在论文《Ring Attention with Blockwise Transformers for Near-Infinite Context》中，通过将序列本身分布到以逻辑环状排列的多个设备上来解决这一问题：每个设备只持有完整序列中查询、键、值的其中一个分块，为自己的分块计算注意力，同时将自己的键值分块传递给环中的下一个设备，并同步接收上一个设备传来的分块——这一通信过程与正在进行的注意力计算相互重叠，理想情况下，通信开销会被隐藏在计算过程之后，而不会成为额外的负担。论文报告称，这种以分块、环状通信为基础的方法，使得训练与推理所能处理的序列长度可以随所使用的*设备数量*而扩展，而不再受限于任何单一设备的内存上限——论文标题之所以称之为"近乎无限的上下文"(near-infinite context)，正是因为实际的限制变成了集群规模，而非某个固定的架构上限。

Ring Attention is included here not because a prompt engineer implements it directly, but because
it clarifies an important distinction for anyone reasoning about a vendor's advertised context
window: a very large advertised window (hundreds of thousands to millions of tokens) is evidence
that the serving organization has solved the _computational_ distribution problem this section
describes — it says nothing on its own about whether the model's positional scheme extrapolates
gracefully (Section 2) or whether the model's accuracy actually stays high across that entire
window (Sections 5–6). These are three separate engineering problems that happen to be solved
together in a shipped product.

之所以在本章中纳入环形注意力，并不是因为提示工程师需要亲自实现它，而是因为它能够帮助我们厘清一个重要的区分，供任何在思考厂商所宣称的上下文窗口时参考：一个非常庞大的宣称窗口(几十万乃至上百万个 token)，说明了提供该服务的机构已经解决了本节所描述的*计算层面*的分布式问题——但这本身并不能说明该模型的位置编码方案是否能够平滑地外推(第2节)，也不能说明该模型的准确率是否真的能在整个窗口范围内保持稳定(第5至第6节)。这是三个各自独立的工程问题，只是恰好在某个已发布的产品中被一并解决了而已。

## 5. The Empirical Shape of Long-Context Performance: "Lost in the Middle"

**长上下文性能的实证形态："迷失在中间"**

Even when a model's context window is architecturally sound at a given length, Liu, Lin, Hewitt,
Paranjape, Bevilacqua, Petroni, and Liang (2023), in "Lost in the Middle: How Language Models Use
Long Contexts," ask a different, purely empirical question: given that a piece of relevant
information is somewhere inside a long prompt, how does the model's accuracy at using it change
depending on _where_ in the prompt it is placed? Their experiments — including a multi-document
question-answering task where one document contains the answer and the rest are distractors, with
the answer-containing document's position systematically varied — find a consistent
**U-shaped performance curve**: accuracy is highest when the relevant information is at the very
beginning of the context or the very end of it, and is substantially lower when the same
information is placed in the middle of a long context, even though the model's stated context
window comfortably contains the entire input. The paper additionally finds that this
middle-of-context degradation gets worse as the total context length grows, and that it occurs
across multiple model families the authors tested, not just one.

即便一个模型在某个给定长度下，其上下文窗口在架构层面是健全的，Liu、Lin、Hewitt、Paranjape、Bevilacqua、Petroni 与 Liang(2023)在论文《Lost in the Middle: How Language Models Use Long Contexts》中，提出了一个不同的、纯粹实证性的问题：假设一段相关信息位于一段长提示词内部的某处，模型使用这段信息的准确率，会如何随着它在提示词中所处的*位置*而变化？他们的实验——包括一项多文档问答任务，其中一份文档包含答案，其余文档均为干扰项，而包含答案的那份文档的位置被系统性地加以变化——发现了一条一致的**U 形性能曲线**：当相关信息位于上下文的最开头或最结尾时，准确率最高；而当同样的信息被放在一段长上下文的中间部分时，准确率则明显更低，即便模型所宣称的上下文窗口完全能够容纳整段输入。论文还发现，这种"迷失在中间"的性能下降，会随着总上下文长度的增长而愈发严重，并且在作者们测试的多个模型家族中都普遍存在，而不只是个别模型才有的现象。

This finding has an immediate, practical consequence for context budgeting (developed further in
Section 7): the position of content inside a prompt is not a neutral formatting choice — where you
place the single most important piece of information can measurably change whether the model uses
it correctly, independent of whether that information is present in the context at all. Anthropic's
own official long-context prompting guidance, discussed further in Section 7, recommends placing
long-form reference material near the top of a prompt, above the specific query and instructions,
partly for this reason.

这一发现，对于上下文预算(将在第7节进一步展开)有着直接的实际影响：内容在提示词中的位置，并非一个中立无关的排版选择——你把最重要的那一条信息放在哪里，会实实在在地影响模型能否正确使用它，而这与该信息是否已经存在于上下文中是两回事。Anthropic 官方自身的长上下文提示指南(将在第7节进一步讨论)，之所以建议把长篇参考材料放在提示词靠前的位置、置于具体问题和指令之上，原因之一正在于此。

## 6. Evaluating Long-Context Claims: Needle-in-a-Haystack and Its Limits

**评估长上下文相关宣称：大海捞针测试及其局限**

Given that longer context windows can fail both architecturally (Sections 2–4) and behaviorally
(Section 5), the field needed a standard, repeatable way to measure whether a model actually uses
its full advertised window. Kamradt's **Needle in a Haystack** test, published as an open-source
evaluation methodology, does this directly: a specific, distinctive statement (the "needle") is
inserted at a controlled depth (a percentage position, e.g. 10%, 50%, 90% of the way through) inside
a long body of unrelated filler text (the "haystack") of a controlled total length, and the model is
prompted to retrieve the needle's content; repeating this across a grid of context lengths and
depths and plotting the resulting accuracy produces a heatmap that visualizes exactly where, across
length and position, a model's retrieval starts to fail. This methodology was quickly adopted
across the industry as a standard diagnostic precisely because it turns "does this model really use
its whole context window" from an anecdotal impression into a reproducible, visual measurement.

鉴于更长的上下文窗口既可能在架构层面出问题(第2至第4节)，也可能在行为层面出问题(第5节)，这一领域需要一套标准、可重复的方法，来衡量一个模型是否真的能够用好它所宣称的整个窗口。Kamradt 提出的**大海捞针测试**(Needle in a Haystack)作为一套开源发布的评测方法，正是直接针对这一问题：将一句具体而独特的陈述(即"针")插入到一段长度可控的、由不相关填充文本组成的正文(即"草垛")中某个受控的深度位置(即某个百分比位置，例如整体长度的10%、50%、90%处)，然后要求模型检索出这根"针"的内容；在一系列不同的上下文长度与深度组合上重复这一过程，并将得到的准确率绘制出来，就能得到一张热力图，直观地呈现出模型的检索能力究竟在长度与位置的哪个组合上开始失效。这套方法之所以能被业界迅速采纳为一项标准诊断手段，正是因为它把"这个模型是否真的用好了它整个上下文窗口"这个问题，从一种轶事式的主观印象，变成了一项可复现的、可视化的测量。

The needle-in-a-haystack test is not, however, the last word on long-context evaluation, and this
is a case where the literature is genuinely unsettled rather than settled in the test's favor. Hsieh
et al. (2024), in "RULER: What's the Real Context Size of Your Long-Context Language Models?",
argue explicitly that the standard needle-in-a-haystack test measures only a superficial form of
long-context ability — pure verbatim retrieval of one isolated fact — and does not test whether a
model can trace connections across multiple pieces of information, aggregate information scattered
across the context, or handle multiple needles at once. Their RULER benchmark extends the basic
needle test with these harder task categories, and their headline empirical result is sobering:
across 17 long-context models they evaluated, most models that score nearly perfectly on the
standard needle-in-a-haystack test at their claimed maximum context length still show large
performance drops on RULER's harder tasks well before that claimed length, and among models
claiming context windows of 32K tokens or more, only about half actually maintained satisfactory
performance at 32K on RULER's fuller task suite. The honest conclusion a prompt
engineer should draw is that passing a needle-in-a-haystack test is necessary evidence of long-context
capability but is not, on its own, sufficient evidence — a vendor's needle-in-a-haystack score and a
model's true reliability at complex, multi-fact reasoning over a long context are related but
distinct claims, and the two are not always aligned.

不过，大海捞针测试并不是长上下文评测方法的终点，这也是文献中确实存在争议、而非一边倒地支持该测试的一个案例。Hsieh 等人(2024)在论文《RULER: What's the Real Context Size of Your Long-Context Language Models?》中明确指出，标准的大海捞针测试只测量了长上下文能力中较为表层的一种形式——对单条孤立事实的逐字检索——并未测试模型能否在多条信息之间建立联系、能否聚合散布在上下文各处的信息，或能否同时处理多根"针"。他们提出的 RULER 基准测试，用这些更困难的任务类别对基础的大海捞针测试做了扩展，而他们最引人注目的实证结果令人警醒：在他们评测的17个长上下文模型中，大多数在其宣称的最大上下文长度下、标准大海捞针测试几乎能拿到满分的模型，在 RULER 更困难的任务上，远远不到宣称长度就出现了明显的性能下降；而在那些宣称上下文窗口达到32K个 token 或更长的模型中，在 RULER 更完整的任务集上，能在32K长度真正保持令人满意表现的模型大约只占一半。提示工程师应当从中得出的诚实结论是：通过大海捞针测试，是长上下文能力的必要证据，但单凭它本身并不充分——厂商给出的大海捞针得分，与模型在长上下文上进行复杂、多事实推理时的真实可靠程度，是相关但并不等同的两件事，二者并不总是一致的。

## 7. Context Budgeting as an Engineering Discipline

**上下文预算：一门工程纪律**

Sections 2–6 established that a context window's usable capacity is neither unlimited nor uniform
across its length. **Context budgeting** is the practice, given that reality, of
treating the context window as a finite resource to be deliberately allocated across categories of
content rather than filled greedily. A useful way to enumerate the categories competing for that
budget extends the four-part prompt anatomy from `introductory/05` §2 and the few-shot trade-off
named in `intermediate/05` §1:

第2至第6节确立了这样一个事实：上下文窗口的可用容量，既不是无限的，在窗口内部各处也并非均等分布。**上下文预算**正是在这一现实之下形成的一种实践：把上下文窗口当作一种有限的资源，在不同类别的内容之间有意识地加以分配，而不是贪婪地一味填满。要枚举争夺这份预算的各个类别，一种有效的方式，是在《提示工程基础》第2节所讲的提示词四要素以及《进阶提示工程》第1节所提到的少样本权衡基础上加以扩展：

| #   | Category                                                                                                                              | 类别                                                                                                                                        |
| --- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | the system prompt and standing instructions                                                                                           | 系统提示词与常设指令                                                                                                                        |
| 2   | tool and function schemas, when the application uses tool use as covered in `introductory/04-tool-use-and-function-calling-basics.md` | 工具与函数模式，适用于像《工具使用与函数调用基础》(`introductory/04-tool-use-and-function-calling-basics.md`)所讲那样使用工具调用的应用场景 |
| 3   | few-shot examples (`intermediate/05` §1)                                                                                              | 少样本示例(《进阶提示工程》第1节)                                                                                                           |
| 4   | retrieved or reference documents                                                                                                      | 检索得到的或作为参考的文档                                                                                                                  |
| 5   | conversation history                                                                                                                  | 对话历史                                                                                                                                    |
| 6   | a reserved allowance for the model's own output, since output tokens share the same window as input tokens on most current APIs       | 为模型自身输出预留的额度，因为在目前大多数 API 中，输出词元与输入词元共享同一个窗口                                                         |

Every token spent on one category is a token unavailable to every other category, and Section 5's
finding means the _placement_ of what remains matters as much as the total count.

花在某一类别上的每一个词元，都意味着其他每一类别都少了一个可用的词元，而第5节的发现意味着：剩下的这些内容被*放在哪里*，与它们的总数量同样重要。

Three concrete techniques put this discipline into practice.

有三种具体的技巧，能把这一纪律落到实处。

| Technique                                     | EN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 中文                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Placement discipline**                      | Anthropic's official long-context prompting guidance recommends placing long reference documents near the top of a prompt, above the specific query and instructions that follow, reporting this ordering can measurably improve response quality on complex, multi-document tasks — a direct, actionable response to the Section 5 finding, since it deliberately keeps the query (which the model must always attend to correctly) out of the "lost in the middle" zone. The same guidance also recommends, for long-document tasks, asking the model to first quote the specific passages it will rely on before producing its final answer, which the documentation frames as helping the model filter signal from the surrounding noise of a large document. | Anthropic 官方的长上下文提示指南建议，把长篇参考文档放在提示词靠前的位置、置于随后的具体问题和指令之上，并报告称，这种排布方式能够在复杂的多文档任务上带来可测量的回答质量提升——这是对第5节发现的一种直接、可操作的回应，因为它有意让查询本身(模型必须始终正确关注的部分)避开了"迷失在中间"的那个区域。同一份指南还建议，在长文档任务中，要求模型先引用它将要依赖的具体段落原文、再给出最终答案，文档中将这一做法描述为有助于模型从一份大型文档周围的噪声中过滤出真正的信号。                                                                                     |
| **Prompt caching**                            | Anthropic's documented prompt-caching mechanism lets an application mark a prefix of a prompt (for example, a large, unchanging system prompt or reference document) with a cache breakpoint; on a subsequent request that reuses the identical cached prefix, the documentation reports cache-read tokens cost roughly 10% of the price of ordinary input tokens and reduce time-to-first-token substantially, though writing to the cache initially costs about 25% more than an ordinary input token and the cached entry has a limited lifetime (a documented minimum of 5 minutes for the standard cache, or 1 hour for an extended-lifetime cache) before it must be rewritten.                                                                             | Anthropic 官方记录的提示词缓存机制，允许应用程序为提示词的某个前缀(例如一段庞大且不变的系统提示词，或某份参考文档)标记一个缓存断点；在后续请求中，如果复用了完全相同的已缓存前缀，文档报告称，缓存读取的词元成本大约只是普通输入词元价格的10%，并能大幅缩短首个词元的返回时间，不过首次写入缓存的成本比普通输入词元高出约25%，且缓存条目的存活时间有限(文档记录的标准缓存最短为5分钟，若使用延长存活时间的缓存则为1小时)，超过这一时限后就必须重新写入。                                                                                                          |
| **Compaction and retrieval as escape valves** | when the content competing for budget exceeds what fits acceptably — particularly long-running conversation history — an engineer can either compress it (summarizing older turns rather than keeping them verbatim, a technique developed further in `core-component-00/engineering/context-engineering/`-style production systems this curriculum does not duplicate here) or avoid loading it into context at all and instead fetch only the currently relevant slice on demand — which is precisely the retrieval-augmented generation approach that `advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md` develops as this chapter's direct continuation.                                                                                     | 当争夺预算的内容超出了能够合理容纳的范围时——尤其是运行时间很长的对话历史——工程师既可以选择对其进行压缩(对较早的对话轮次进行摘要，而非逐字保留；这一技巧在本课程体系不重复展开的、`core-component-00/engineering/context-engineering/` 这类生产系统中有进一步发展)，也可以干脆完全不把它加载进上下文，而是按需只取出当前真正相关的那一小部分——这正是检索增强生成(retrieval-augmented generation)的做法，而这正是本章的直接后续——《规模化 RAG：混合检索、重排序与评估》(`advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`)——将要展开讲授的内容。 |

## 8. Worked Example: Budgeting a Long Context Window for a Support Agent

**实战示例：为一个客服智能体规划长上下文预算**

Consider an application built on a model with a documented 200,000-token context window (the size
Anthropic's own context-window documentation reports for its Claude 3 model family), serving a
customer-support agent that must answer questions using a 40,000-token product manual, up to 20
few-shot examples of well-answered support tickets, and a running conversation that can grow long
over a multi-turn session. Table 1 below shows one reasonable budget allocation, chosen by applying
the six categories from Section 7.

设想有这样一个应用：构建在一个文档记录的上下文窗口为200,000个 token 的模型之上(这正是 Anthropic 自身的上下文窗口文档中，针对其 Claude 3 模型系列所报告的窗口大小)，用于服务一个客服智能体，该智能体必须依据一份40,000个 token 的产品手册来回答问题，还要用到最多20条已妥善解答的客服工单作为少样本示例，并且要处理一段在多轮会话中可能不断变长的对话历史。下面的表1展示了一种合理的预算分配方案，依据的正是第7节所述的六个类别。

| Category                       | Allocation                          | Rationale                                                                                                                                                                     |
| ------------------------------ | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| System prompt + standing rules | ~1,000 tokens                       | Small, fixed; cached (Section 7) since it never changes between requests.                                                                                                     |
| Product manual (reference)     | 40,000 tokens                       | Placed at the _top_ of the prompt per Section 5/7's placement discipline; cached, since it is shared across every user's request and rarely changes.                          |
| Few-shot examples              | ~4,000 tokens                       | 8–10 well-chosen examples (per `intermediate/05` §1's guidance on representative, boundary-covering selection) rather than all 20 — trading example count for room elsewhere. |
| Conversation history           | up to 30,000 tokens, then compacted | Kept verbatim while short; older turns summarized once the running total exceeds this ceiling.                                                                                |
| Reserved for model output      | 4,000 tokens                        | Guarantees the model is never truncated mid-answer.                                                                                                                           |
| Unallocated headroom           | remainder (~121,000 tokens)         | Kept free rather than filled, since Section 5–6 give no guarantee that stuffing more content in improves — and may degrade — accuracy.                                        |

以模型的一个应用实例为例来考虑上述场景：该模型文档记录的上下文窗口为200,000个 token(这正是 Anthropic 自身的上下文窗口文档中，针对其 Claude 3 模型系列所报告的窗口大小)，用于服务一个客服智能体，该智能体必须依据一份40,000个 token 的产品手册来回答问题，还要用到最多20条已妥善解答的客服工单作为少样本示例，并且要处理一段在多轮会话中可能不断变长的对话历史。下面的表1展示了一种合理的预算分配方案，依据的正是第7节所述的六个类别。

The deliberate decision worth highlighting is the last row: rather than treating the unused 121,000
tokens as free space to fill with more examples or more history "just in case," this budget leaves
it unallocated. This is a direct, practical consequence of Sections 5–6 — since more content in the
middle of a long context is not guaranteed to be used correctly, and since even models with large
advertised windows have been shown (Section 6) to degrade well before their claimed limit on
harder, multi-fact tasks, an engineer following this chapter's evidence treats headroom as a safety
margin, not an invitation to add content indiscriminately. Combined with placing the large, static
product manual first and marking both it and the system prompt as cached, this budget also minimizes
cost: on a multi-turn session, every request after the first pays the roughly 10% cache-read price
(Section 7) for the 41,000 tokens of system prompt and manual, rather than the full input price on
every single turn.

值得特别强调的，是最后一行体现出的那个有意为之的决定：这份预算并没有把未使用的121,000个 token 当作"以防万一"的自由空间，拿更多的示例或更多的历史记录去填满它，而是让它保持未分配的状态。这是第5至第6节发现的一个直接、实际的推论——因为长上下文中间部分的更多内容，并不保证能被模型正确使用，而且即便是那些宣称拥有庞大窗口的模型，也已经被证明(第6节)会在远未达到其宣称上限之前，就在更困难的多事实任务上出现性能下降；一名遵循本章证据行事的工程师，会把这部分余量当作安全边际，而不是一个可以不加节制往里塞内容的邀请。再加上把庞大而静态的产品手册放在最前面、并将它与系统提示词一并标记为缓存，这份预算方案同时也把成本降到了最低：在一个多轮会话中，第一轮之后的每一次请求，针对那41,000个 token 的系统提示词与产品手册，支付的都是大约10%的缓存读取价格(第7节)，而不是每一轮都按全额的输入价格计费。

## 9. Common Pitfalls at This Level

**本层级的常见坑**

Three failure patterns are specific to long-context engineering, distinct from the beginner
pitfalls in `introductory/05` §8 and the intermediate-level failure modes in `intermediate/05` §7.

有三种失败模式是长上下文工程所特有的，不同于《提示工程基础》第8节所讲的初学者常见坑，也不同于《进阶提示工程》第7节所讲的中级层面的失败模式。

| Pitfall                                                       | EN                                                                                                                                                                                                                                                                                                                                                               | 中文                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Trusting an advertised window size as a quality guarantee** | Sections 4 and 6 showed that a very large advertised context window is evidence a vendor has solved a _computational_ distribution problem, not evidence that accuracy stays flat across that entire window; RULER's findings (Section 6) mean this must be checked, not assumed, for any task involving multi-fact reasoning rather than single-fact retrieval. | 第4节与第6节表明，一个非常庞大的宣称上下文窗口，说明的是厂商已经解决了一个*计算层面*的分布式问题，而不能说明准确率在整个窗口范围内都能保持平稳；RULER 的发现(第6节)意味着，对于任何涉及多事实推理、而非单一事实检索的任务，这一点都必须加以核实，而不能想当然地假设成立。 |
| **Burying the query**                                         | placing a user's actual question after a very long block of reference material, rather than following the placement discipline in Section 7, needlessly moves the query itself into the degraded middle region that Section 5 identified, even when the reference material's _content_ is well-placed.                                                           | 将用户真正的问题放在一大段参考材料之后，而不遵循第7节所述的位置排布纪律，即便参考材料本身的*内容*放置得当，也会无谓地把查询本身推入第5节所指出的那个性能下降的中间区域。                                                                                                  |
| **Paying full price for repeated static content**             | sending the same large system prompt or reference document on every request without using the caching mechanism in Section 7 wastes both money and latency on content that has not changed since the previous request.                                                                                                                                           | 在每一次请求中都发送同样庞大的系统提示词或参考文档，却不使用第7节所述的缓存机制，会在自上一次请求以来根本没有变化的内容上，白白浪费金钱与延迟。                                                                                                                           |

## 10. Summary and What Comes Next

**小结与后续内容**

This chapter extended `intermediate/02`'s architectural picture of attention with the specific
problems and techniques of long-context engineering: the position-extrapolation problem RoPE-based
models face beyond their training length and two solutions, Position Interpolation (Chen et al., 2023) and YaRN (Peng et al., 2023); Ring Attention (Liu et al., 2023) as a solution to the separate,
purely computational problem of distributing $O(n^2)$ attention across devices; the empirical
"lost in the middle" degradation pattern (Liu et al., 2023) that shows position within a context
matters independently of total window size; and the needle-in-a-haystack diagnostic together with
RULER's (Hsieh et al., 2024) evidence that it measures only a superficial slice of true long-context
capability. It then turned these findings into the practical discipline of context budgeting:
allocating a finite window across competing categories of content, applying placement discipline
and prompt caching, and — when content genuinely does not fit a budget an engineer is willing to
pay for — reaching for retrieval instead of ever-larger context. That last escape valve is exactly
where the next module in this cluster,
`advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`, begins: rather than loading
every potentially relevant document into context, retrieval-augmented generation selects only what
is likely to matter for a given query, at scale.

本章在《注意力机制深入解析》所建立的注意力架构图景基础上，进一步讲授了长上下文工程特有的问题与技巧：基于 RoPE 的模型在超出训练长度之后所面临的位置外推问题，以及两种解决方案——位置插值(Chen 等人，2023)与 YaRN(Peng 等人，2023)；环形注意力(Liu 等人，2023)作为解决另一个独立的、纯计算层面问题——即如何将 $O(n^2)$ 的注意力计算分布到多个设备上——的方案；"迷失在中间"这一实证性的性能下降规律(Liu 等人，2023)，它表明内容在上下文中的位置，其重要性独立于窗口总大小；以及大海捞针诊断方法，连同 RULER(Hsieh 等人，2024)所提供的证据——表明该诊断方法只测量了真正长上下文能力中较为表层的一小部分。随后，本章把这些发现转化为上下文预算这一实用纪律：在相互竞争的各类内容之间分配有限的窗口、运用位置排布纪律与提示词缓存，并且——当内容确实超出了工程师愿意承担的预算时——转而求助于检索，而不是一味追求更大的上下文。而这最后一道泄压阀，正是本主题群下一个模块——《规模化 RAG：混合检索、重排序与评估》(`advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`)——的起点：检索增强生成不会把每一份可能相关的文档都塞进上下文，而是在规模化的场景下，只挑选出对给定查询很可能真正重要的内容。

## References

**参考文献**

### External Sources

- [Attention Is All You Need (Vaswani et al., 2017, arXiv:1706.03762)](https://arxiv.org/abs/1706.03762)
- [RoFormer: Enhanced Transformer with Rotary Position Embedding (Su et al., 2021, arXiv:2104.09864)](https://arxiv.org/abs/2104.09864)
- [Extending Context Window of Large Language Models via Positional Interpolation (Chen et al., 2023, arXiv:2306.15595)](https://arxiv.org/abs/2306.15595)
- [YaRN: Efficient Context Window Extension of Large Language Models (Peng et al., 2023, arXiv:2309.00071)](https://arxiv.org/abs/2309.00071)
- [Ring Attention with Blockwise Transformers for Near-Infinite Context (Liu, Zaharia & Abbeel, 2023, arXiv:2310.01889)](https://arxiv.org/abs/2310.01889)
- [Lost in the Middle: How Language Models Use Long Contexts (Liu et al., 2023, arXiv:2307.03172)](https://arxiv.org/abs/2307.03172)
- [RULER: What's the Real Context Size of Your Long-Context Language Models? (Hsieh et al., 2024, arXiv:2404.06654)](https://arxiv.org/abs/2404.06654)
- [gkamradt/LLMTest_NeedleInAHaystack — Needle In A Haystack evaluation methodology (GitHub)](https://github.com/gkamradt/LLMTest_NeedleInAHaystack)
- [Claude Docs — Context Windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Claude Docs — Long Context Prompting Tips](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/long-context-tips)
- [Claude Docs — Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

### Internal Cross-References

- [`introductory/06-context-windows-tokens-and-memory-basics.md`](../introductory/06-context-windows-tokens-and-memory-basics.md) — prerequisite definitions of token and context window.
- [`introductory/05-prompt-engineering-fundamentals.md`](../introductory/05-prompt-engineering-fundamentals.md) — prerequisite: the four-part prompt anatomy extended in Section 7.
- [`introductory/04-tool-use-and-function-calling-basics.md`](../introductory/04-tool-use-and-function-calling-basics.md) — prerequisite background for the tool-schema budget category in Section 7.
- [`intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md`](../intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md) — direct prerequisite: $O(n^2)$ attention complexity, KV cache mechanism and memory formula, RoPE and ALiBi.
- [`intermediate/05-advanced-prompting-cot-few-shot-structured-output.md`](../intermediate/05-advanced-prompting-cot-few-shot-structured-output.md) — direct prerequisite: the context-budget trade-off introduced in its §1, continued here.
- [`advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`](./06-rag-at-scale-hybrid-search-reranking-and-evaluation.md) — direct continuation: retrieval as an alternative to context stuffing.
