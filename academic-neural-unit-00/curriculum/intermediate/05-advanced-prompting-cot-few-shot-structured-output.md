# Advanced Prompting: Chain-of-Thought, Few-Shot & Structured Output

**进阶提示工程：思维链、少样本与结构化输出**

| Field   | English                      | 中文                                            |
| ------- | ---------------------------- | ----------------------------------------------- |
| Level   | Intermediate                 | 中级                                            |
| Cluster | Prompt & Context Engineering | 提示与上下文工程                                |
| Author  | Dr. Wei-Ling                 | ANU-00 应用人工智能系统研究员 Wei-Ling Tan 博士 |

---

This chapter builds directly on `introductory/05-prompt-engineering-fundamentals.md`, which
defined a prompt's four parts (instruction, context, input data, output indicator), the
system/user/assistant role structure, zero-shot prompting, and temperature. It assumes the reader
already has that vocabulary and does not redefine it. It also assumes the reader has completed
`introductory/06-context-windows-tokens-and-memory-basics.md` for the definitions of token and
context window used throughout Sections 1 and 5 below.

本章直接建立在《提示工程基础》(`introductory/05-prompt-engineering-fundamentals.md`)之上，该章定义了提示词的四个组成部分(指令、上下文、输入数据、输出指示)、系统/用户/助手角色结构、零样本提示以及温度参数。本章假定读者已经掌握了这些词汇，不再重复定义。本章同时假定读者已经学完《上下文窗口、词元与记忆基础》(`introductory/06-context-windows-tokens-and-memory-basics.md`),因为下文第1节与第5节会用到该章对"词元"与"上下文窗口"所下的定义。

Where the introductory module covered prompting techniques that require only a single, direct
instruction, this chapter covers three techniques that ask more of the prompt in exchange for
measurably better performance on harder tasks: few-shot prompting (showing worked examples),
chain-of-thought prompting (asking the model to reason step by step before answering), and strict
structured output (constraining the response to a machine-parseable schema). All three are backed
by peer-reviewed or industry-published research cited in full at the end of this chapter.

如果说入门模块讲授的是那些只需一条直接指令即可完成的提示技巧，本章讲授的则是另外三种对提示词要求更高、但在更难的任务上能带来可测量性能提升的技巧：少样本提示(展示已完成的示例)、思维链提示(要求模型在作答前逐步推理)以及严格的结构化输出(将回答约束在一个可供程序解析的模式之内)。这三种技巧都有经过同行评审或业界正式发布的研究作为支撑，相关引用将在本章末尾完整列出。

## 1. Few-Shot Prompting: In-Context Learning with Examples

**少样本提示：借助示例进行上下文学习**

Few-shot prompting means including, inside the prompt itself, a small number of
worked examples of the task being done correctly, immediately before the actual input the model
must handle. If a zero-shot prompt for sentiment classification simply asks "Is this review
positive or negative?", a few-shot version instead shows two or three example reviews, each
followed by its correct label, before presenting the new review to be classified. The model is
not being retrained on these examples — no parameters change — it is using them purely as
in-context demonstrations of the input-output pattern it should imitate, a capability documented
and named by Brown et al. (2020) in the same GPT-3 paper introduced in the previous module. Their
central empirical finding was that as models scale up in size, few-shot performance — supplying a
handful of examples in the prompt with no gradient updates at all — approaches the performance of
models that were specifically fine-tuned on that task, without any of the cost or delay of
fine-tuning.

少样本提示是指在提示词本身内部，紧挨着模型实际要处理的那个输入之前，给出少量已经正确完成的任务示例。如果一个用于情感分类的零样本提示只是简单地问"这条评论是正面还是负面?",那么它对应的少样本版本则会先展示两三条示例评论、并各自附上正确的标签，然后再呈现需要分类的新评论。模型并没有在这些示例上被重新训练——没有任何参数发生变化——它只是把这些示例纯粹当作上下文中的演示，用来模仿其中的输入-输出模式。这种能力正是 Brown 等人(2020)在上一模块提到的那篇 GPT-3 论文中记录并命名的。他们的核心实证发现是：随着模型规模不断增大，少样本表现——即仅在提示词中提供少量示例、完全不进行任何梯度更新——会逐渐逼近专门针对该任务进行过微调的模型的表现，却无需承担微调所带来的任何成本与延迟。

Two practical design choices affect few-shot performance measurably. First, example selection: the
examples should be representative of the range of inputs the model will actually see in
production, including at least one example near each decision boundary (for sentiment
classification, that means including a genuinely ambiguous or mixed-sentiment example, not just
clear-cut positive and negative ones). Second, example ordering and count: because the prompt
occupies a fixed context window (as defined in `introductory/06`), each example consumes tokens
that are then unavailable for the actual input or for further reasoning, so few-shot prompting
faces a direct trade-off between more guidance and less room for everything else — a trade-off the
advanced module `advanced/05-advanced-context-engineering-long-context-and-budgeting.md` treats
in depth as a special case of a general context-budgeting problem.

有两个实际的设计选择会明显影响少样本提示的效果。第一是示例的选取：示例应当能代表模型在实际生产环境中真正会遇到的输入范围，并且在每一个判断边界附近至少包含一个示例(以情感分类为例，这意味着不能只放正面和负面这类界限清晰的例子，还要包含一个真正模棱两可、褒贬参半的例子)。第二是示例的排列顺序与数量：由于提示词占据的是一个大小固定的上下文窗口(定义见《上下文窗口、词元与记忆基础》),每一个示例都会占用一部分词元，而这部分词元此后就无法再用于真正的输入或进一步的推理，因此少样本提示天然面临着"更多引导"与"为其他内容留出更多空间"之间的直接权衡——这一权衡正是高级模块《高级上下文工程：长上下文与上下文预算》(`advanced/05-advanced-context-engineering-long-context-and-budgeting.md`)所要深入探讨的一般性"上下文预算"问题的一个特例。

## 2. Chain-of-Thought Prompting: Reasoning Before Answering

**思维链提示：先推理，后作答**

Chain-of-thought prompting (often abbreviated CoT) is a technique in which the prompt
asks the model to produce a series of intermediate reasoning steps before stating its final
answer, rather than jumping straight to the answer. Wei et al. (2022), in "Chain-of-Thought
Prompting Elicits Reasoning in Large Language Models," introduced and named this technique,
showing it as a form of few-shot prompting in which the worked examples in the prompt include not
just an input and a correct final answer but also the reasoning that leads from one to the other.
Their headline result was on multi-step arithmetic word problems: on the GSM8K benchmark (a
dataset of grade-school math word problems), a 540-billion-parameter PaLM model's accuracy jumped
from a much lower standard few-shot baseline to a new state of the art when the few-shot examples
included worked-out reasoning steps rather than answers alone — the paper reports this gain is
concentrated in larger models, meaning chain-of-thought's benefit is itself an example of an
emergent capability that becomes more pronounced with model scale.

思维链提示(chain-of-thought prompting,常缩写为 CoT)是一种要求模型在给出最终答案之前，先生成一系列中间推理步骤的提示技巧，而不是直接跳到答案。Wei 等人(2022)在论文《Chain-of-Thought Prompting Elicits Reasoning in Large Language Models》中提出并命名了这一技巧，将其呈现为少样本提示的一种变体：提示词中的示例不仅包含输入与正确的最终答案，还包含从输入推导到答案所经历的推理过程。他们最引人注目的结果出现在多步算术应用题上：在 GSM8K 基准测试(一个由小学数学应用题组成的数据集)上，当少样本示例中包含逐步展开的推理过程、而非只有答案时，一个拥有5400亿参数的 PaLM 模型的准确率，相较于标准的少样本基线有了大幅跃升，达到了当时的最新水平——论文指出，这种收益主要集中在较大规模的模型上，这意味着思维链带来的好处本身，正是"涌现能力"(指随模型规模增大而愈发显著的能力)的一个例证。

A closely related but distinct technique is zero-shot chain-of-thought, introduced by Kojima et
al. (2022) in "Large Language Models are Zero-Shot Reasoners." Rather than including full worked
examples with reasoning, their method simply appends a fixed phrase — "Let's think step by step" —
to the end of the prompt, before the model's answer. Despite requiring no examples at all, this
single addition produced large accuracy gains on the same style of reasoning benchmarks: the paper
reports accuracy on one arithmetic benchmark (MultiArith) rising from 17.7% to 78.7% for one model
when this phrase was added, and similarly large gains on symbolic reasoning tasks. The practical
implication for a prompt engineer is that chain-of-thought reasoning can be elicited two ways —
with worked few-shot examples (higher effort, typically higher reliability, per Wei et al.) or
with a zero-shot trigger phrase (near-zero effort, per Kojima et al.) — and the right choice
depends on how much example-writing effort is justified for the task at hand.

一种与之密切相关但又有所区别的技巧，是由 Kojima 等人(2022)在论文《Large Language Models are Zero-Shot Reasoners》中提出的"零样本思维链"。这种方法不需要包含带推理过程的完整示例，而是仅仅在提示词末尾、模型作答之前，附加一句固定的短语——"让我们一步一步地思考"(Let's think step by step)。尽管完全不需要任何示例，这一处简单的添加却在同类推理基准测试上带来了巨大的准确率提升：论文报告称，在某一算术基准测试(MultiArith)上，加入这句短语后，某个模型的准确率从17.7%跃升至78.7%,在符号推理任务上也观察到了类似幅度的提升。这对提示工程师的实际启示是：思维链推理可以通过两种方式引出——一种是带推理过程的少样本示例(投入更高，据 Wei 等人的研究，通常也更可靠),另一种是零样本触发短语(投入几乎为零，据 Kojima 等人的研究)——具体该选哪一种，取决于当前任务是否值得投入精力去撰写示例。

## 3. Self-Consistency: Sampling Multiple Reasoning Paths

**自洽性：对多条推理路径进行采样**

Because a single chain-of-thought reasoning path can still go wrong at any individual step,
Wang et al. (2022), in "Self-Consistency Improves Chain of Thought Reasoning in Language Models,"
introduced a technique called self-consistency that improves reliability further by exploiting
temperature (defined in `introductory/05`, Section 7). Instead of running the model once at a low
temperature and taking whatever single answer it produces, self-consistency runs the same
chain-of-thought prompt multiple times at a higher, non-zero temperature — deliberately allowing
each run to reason differently — and then takes a majority vote over the multiple final answers
produced, discarding the intermediate reasoning paths themselves. The intuition, stated directly in
the paper, is that a genuinely correct answer tends to be reachable by multiple different valid
lines of reasoning, whereas an incorrect answer is less likely for several independently sampled
reasoning paths to converge on by coincidence. The paper reports this method improved accuracy over
standard chain-of-thought prompting by double-digit percentage points on its arithmetic-reasoning
benchmarks (GSM8K +17.9, SVAMP +11.0, AQuA +12.2) and by smaller, single-digit margins on its
commonsense-reasoning benchmarks (StrategyQA +6.4, ARC-challenge +3.9).

由于单一的思维链推理路径仍可能在任何一个具体步骤上出错，Wang 等人(2022)在论文《Self-Consistency Improves Chain of Thought Reasoning in Language Models》中提出了一种名为"自洽性"(self-consistency)的技巧，通过利用温度参数(定义见《提示工程基础》第7节)进一步提升可靠性。自洽性不是在低温度下只运行一次模型、直接采用它给出的唯一答案，而是在较高、非零的温度下对同一个思维链提示多次运行——有意让每一次运行都可能走出不同的推理路径——然后对多次运行所产生的多个最终答案进行多数投票，并舍弃这些中间推理过程本身。论文中直接阐述的直觉是：一个真正正确的答案，往往可以通过多条不同的、各自有效的推理路线抵达；而一个错误的答案，则不太可能恰好被若干条相互独立采样出的推理路径不约而同地"巧合"得出。论文报告称，该方法在其算术推理基准测试上(GSM8K +17.9、SVAMP +11.0、AQuA +12.2)将准确率提升了两位数的百分点，而在常识推理基准测试上(StrategyQA +6.4、ARC-challenge +3.9)的提升幅度较小，只有个位数百分点。

Self-consistency has a direct, quantifiable cost: running the same prompt N times multiplies the
number of tokens generated (and, in most commercial API pricing, the dollar cost) by roughly N. A
prompt engineer choosing to use self-consistency is making an explicit trade of extra inference
cost for extra reliability, and the technique is best reserved for tasks where a wrong answer is
expensive (e.g., a financial calculation feeding directly into a decision) rather than applied by
default to every prompt.

自洽性有一个直接且可量化的代价：将同一个提示词运行 N 次，生成的词元数量(在大多数商业 API 的计费方式下，也就是实际花费的金额)也会大致相应地增加到 N 倍。选择使用自洽性的提示工程师，实际上是在用额外的推理成本明确换取更高的可靠性，因此这项技巧最好保留给那些答错代价高昂的任务(例如直接影响某项决策的财务计算),而不应作为对每一个提示词都默认采用的做法。

## 4. Combining Structure: Delimiters for Complex Multi-Part Prompts

**组织结构：面向复杂多部分提示词的分隔符**

As a prompt grows to include several few-shot examples, chain-of-thought instructions, and
possibly multiple input documents at once, it becomes important to mark clearly where one part
ends and the next begins — for the model's benefit as much as for a human prompt author's. Building
on the delimiter technique introduced briefly in `introductory/05` (Section 6), Anthropic's
official prompting-best-practices documentation recommends consistently wrapping distinct prompt
components in descriptive XML-style tags — for example `<examples>...</examples>` around the
few-shot block, `<instructions>...</instructions>` around the task description, and
`<document>...</document>` around each piece of input material — precisely because clear
structural boundaries measurably reduce the chance that the model conflates one part of the prompt
with another, such as treating part of a worked example as part of the actual input to be
processed.

随着提示词逐渐扩展，包含了多个少样本示例、思维链指令，乃至可能同时包含多份输入文档，清楚地标明一部分在哪里结束、下一部分从哪里开始就变得非常重要——这既是为了模型着想，也是为了提示词的编写者本人着想。在《提示工程基础》第6节简要介绍的分隔符技巧基础上，Anthropic 官方的提示工程最佳实践文档进一步建议：始终如一地用具有描述性的 XML 风格标签把提示词的各个不同组成部分包裹起来——例如用 `<examples>...</examples>` 包裹少样本示例块，用 `<instructions>...</instructions>` 包裹任务描述，用 `<document>...</document>` 包裹每一份输入材料——之所以如此，正是因为清晰的结构边界能够可测量地降低模型把提示词的某一部分与另一部分相混淆的概率，比如把某个示例的一部分误当作真正要处理的输入内容的一部分。

## 5. Structured Output: Constraining Responses to a Machine-Readable Schema

**结构化输出：将回答约束到机器可读的模式**

`introductory/05` (Section 6) introduced asking the model, via instruction alone, to format its
answer a certain way — for example, to respond with a single line of JSON. That approach is
reliable most of the time with a capable model but is not guaranteed: nothing structurally prevents
the model from adding a stray sentence before the JSON, from omitting a required field, or from
producing a value of the wrong type. Structured output in the strict sense used in
this section refers to a stronger mechanism, offered directly by major LLM providers, that
constrains what the model is allowed to generate at the level of the decoding process itself,
rather than relying on the model choosing to follow a textual instruction.

《提示工程基础》第6节介绍了仅通过指令的方式，要求模型按某种特定格式作答——例如，要求它用一行 JSON 作答。这种做法在使用能力较强的模型时大多数情况下是可靠的，但并不能保证万无一失：结构上没有任何机制能阻止模型在 JSON 前面多加一句无关的话、遗漏某个必填字段，或是给出类型错误的值。本节所使用的严格意义上的"结构化输出",指的是主要大语言模型提供商直接提供的一种更强的机制，它在解码过程本身的层面上，直接约束模型被允许生成的内容，而不是依赖模型"愿意"遵循一条文字指令。

OpenAI's Structured Outputs feature, documented in its API guide, lets a developer supply a JSON
Schema (a formal, machine-readable specification of exactly which fields a JSON object must have
and what type each field's value must be) alongside the prompt; the API then guarantees, at the
level of how the model's output tokens are constrained during generation, that the response will
validate against that schema — the documentation states this is a stronger guarantee than the
provider's earlier, looser "JSON mode," which ensured only that the output was syntactically valid
JSON, not that it matched any particular schema. Anthropic's tool use feature, documented under
"Define tools" in the Claude API docs, achieves a related outcome differently: a developer defines
a "tool" with a `name`, a `description`, and an `input_schema` written in JSON Schema, and can set
`strict: true` so that Claude's tool-call arguments are guaranteed to conform to that schema — a
technique that doubles as both a way to let the model invoke external functions (the mechanism
underlying tool use and function calling, introduced conceptually in
`introductory/04-tool-use-and-function-calling-basics.md`) and a way to force schema-conformant
structured output even when no external function is actually being called.

OpenAI 在其 API 指南中所记录的"结构化输出"(Structured Outputs)功能，允许开发者在提示词之外额外提供一份 JSON Schema(一种正式的、机器可读的规范，精确规定一个 JSON 对象必须包含哪些字段、每个字段的值又必须是什么类型);随后，该 API 会在模型输出词元于生成过程中如何被约束这一层面上加以保证，确保返回的响应能够通过该模式的校验——文档中特别指出，这是比该提供商此前那种较为宽松的"JSON 模式"(JSON mode)更强的保证：后者只能确保输出在语法上是合法的 JSON,却无法保证它符合任何特定的模式。Anthropic 的工具使用功能，记录在 Claude API 文档"定义工具"(Define tools)一节中，以不同的方式达成了类似的效果：开发者用 JSON Schema 定义一个包含 `name`、`description` 与 `input_schema` 的"工具",并可以设置 `strict: true`,从而保证 Claude 生成的工具调用参数一定符合该模式——这项技巧一举两得：既是让模型能够调用外部函数的机制(这正是"工具使用"与"函数调用"背后的原理，已在《工具使用与函数调用基础》〔`introductory/04-tool-use-and-function-calling-basics.md`〕中作了概念性介绍),同时，即便实际上并没有调用任何外部函数，它也可以被用来强制生成符合模式的结构化输出。

The practical rule of thumb this history suggests is: prefer provider-level, schema-enforced
structured output whenever it is available and the downstream consumer is code rather than a
human, since it removes an entire category of parsing failures at the source; fall back to
instruction-based formatting (as in `introductory/05`) only when the schema-enforcement feature is
unavailable for the provider or model in use.

由此可以得出一条实用的经验法则：只要提供商层面的、由模式强制约束的结构化输出功能可用，并且下游的消费者是代码而非人，就应当优先使用它，因为它从源头上就消除了整整一类解析失败的可能性；只有在所使用的提供商或模型不支持这一模式强制功能时，才退而求其次，采用基于指令的格式化方式(如《提示工程基础》所述)。

## 6. Worked Example: Combining All Three Techniques

**实战示例：三种技巧的综合运用**

Consider a harder version of the sentiment-and-feature task from `introductory/05`, Section 9: now
the task is to read a multi-sentence product review that may discuss several features with
different sentiments each, and to return a structured breakdown — because the task now requires
genuine multi-step reasoning (distinguishing which sentence discusses which feature, and each
feature's individual sentiment) rather than a single classification, all three techniques from this
chapter combine naturally.

我们来考虑《提示工程基础》第9节中"情感与特征"任务的一个更困难的版本：现在的任务是阅读一条包含多个句子的产品评论，这条评论可能针对若干个不同的特征分别表达了不同的情感，要求返回一份结构化的拆解结果——由于这项任务现在需要真正的多步推理(判断哪一句话在讨论哪一个特征，以及每个特征各自对应的情感),而不再是单一的分类，本章的三种技巧便可以自然地组合在一起使用。

First, a **system message** establishes the persona and standing rules: "You are a product-review
analysis assistant. Work through the review's sentences one at a time before producing your final
answer." Second, **few-shot examples** (Section 1) show two worked reviews, each followed by
step-by-step reasoning through every sentence, and then a final structured breakdown — teaching the
model both the reasoning style and the exact target format by demonstration rather than description
alone. Third, the **chain-of-thought instruction** (Section 2) is made explicit even beyond what
the examples imply: "Before giving your final answer, list each feature mentioned and the sentence
that discusses it." Fourth, the response is constrained with **provider-level structured output**
(Section 5): a JSON Schema requiring an array called `features`, each entry with a `name` string
and a `sentiment` field restricted to the enum `["positive", "negative", "mixed"]`. For a
high-stakes use of this pipeline — for example, feeding directly into an automated refund-eligibility
decision — an engineer might add **self-consistency** (Section 3): run the whole pipeline three
times at a moderate temperature and keep only the per-feature sentiment values that a majority of
the three runs agree on, flagging any feature without majority agreement for human review rather
than guessing.

首先，一条**系统消息**确立了角色人设与常设规则："你是一名产品评论分析助手。在给出最终答案之前，请逐句处理评论中的每一句话。"其次，**少样本示例**(第1节)展示两条已完成的评论，每一条后面都附有逐句展开的推理过程，最后给出结构化的拆解结果——通过示范而非仅靠文字描述，同时教会模型推理的方式与目标格式的确切样貌。第三，**思维链指令**(第2节)被进一步明确表达出来，超出示例本身所隐含的程度："在给出最终答案之前，请先列出评论中提及的每一个特征，以及讨论该特征的那一句话。"第四，回答通过**提供商层面的结构化输出**(第5节)加以约束：一份 JSON Schema 要求输出一个名为 `features` 的数组，其中每个条目都包含一个字符串类型的 `name` 字段，以及一个取值限定为枚举 `["positive", "negative", "mixed"]` 的 `sentiment` 字段。对于这条流水线中风险较高的用途——例如，直接输入到一个自动化的退款资格判定决策中——工程师或许还会加入**自洽性**(第3节):在中等温度下把整条流水线完整运行三次，只保留三次运行中多数一致同意的每个特征的情感取值，而对没有获得多数一致意见的特征，标记出来交由人工复核，而不是替它作出猜测。

## 7. Common Failure Modes at This Level

**本层级的常见失败模式**

Three failure patterns are specific to the techniques in this chapter, distinct from the beginner
pitfalls already covered in `introductory/05`, Section 8. First, **example leakage bias**: if every
few-shot example happens to share an incidental surface feature with its correct label (for
instance, if every "negative" example in the prompt happens to be long and every "positive" example
happens to be short), the model may learn to key off that surface feature rather than the actual
task, a risk few-shot prompt authors should specifically check for by varying incidental features
independently of the label. Second, **reasoning-answer inconsistency**: because chain-of-thought
reasoning and the final answer are both generated by the same left-to-right token-by-token process,
it is possible for a model's stated reasoning to look sound while its final answer does not
actually follow from it — the reasoning trace should be read as a diagnostic aid for a human
reviewer, not treated as a guarantee that the reasoning caused the answer. Third, **schema
over-constraint**: an excessively rigid or deeply nested JSON Schema can occasionally reduce a
model's task accuracy even while perfectly guaranteeing valid structure, because the fields the
schema demands may force an answer into a shape that does not fit an unusual input well; testing a
schema against a range of realistic edge cases, per the iteration discipline in `introductory/05`
Section 7, remains necessary even when the format itself is now guaranteed to be syntactically
valid.

本章所涉及的这些技巧，还带来了三种与之特有的失败模式，不同于《提示工程基础》第8节已经讲过的那些初学者常见的坑。第一，**示例泄漏偏差**:如果每一个少样本示例恰好都在某个与标签无关的表面特征上与其正确标签相关联(比如，提示词中每一个"负面"示例恰好都篇幅较长，而每一个"正面"示例恰好都篇幅较短),模型就可能学会依据这个表面特征来判断，而非真正依据任务本身来判断——这是少样本提示词的作者应当专门加以检查的风险，做法是让这些无关的表面特征相对于标签独立地变化。第二，**推理与答案不一致**:由于思维链推理过程与最终答案都是由同一个从左到右、逐词元生成的过程产生的，模型陈述出来的推理过程有可能看起来合乎逻辑，而最终答案实际上却并非真正由该推理推导而来——推理轨迹应当被视为供人工审阅者参考的诊断辅助信息，而不应被当作"推理确实导致了这个答案"的保证。第三，**模式过度约束**:一份过于僵化或嵌套层级过深的 JSON Schema,有时会在完美保证结构合法的同时，反而降低模型完成任务的准确率，因为模式所要求的字段可能会强行把答案塞进一种并不适合某个非典型输入的形状里；即便格式本身现在已经能够保证在语法上合法，针对各种贴近真实场景的边界情形对模式本身进行测试，依照《提示工程基础》第7节所述的那套迭代纪律，仍然是必要的。

## 8. Summary

**小结**

This chapter extended the four-part prompt and role structure from `introductory/05` with three
techniques for harder tasks: few-shot prompting, which teaches a task through worked examples
rather than description alone (Brown et al., 2020); chain-of-thought prompting, which elicits
step-by-step reasoning either through worked examples (Wei et al., 2022) or a zero-shot trigger
phrase (Kojima et al., 2022), with self-consistency (Wang et al., 2022) available to trade extra
inference cost for extra reliability; and structured output, which uses provider-level schema
enforcement to guarantee machine-parseable responses. The next module in this cluster,
`advanced/05-advanced-context-engineering-long-context-and-budgeting.md`, picks up directly where
Section 1's context-budget trade-off left off, treating the finite context window itself as a
resource to be actively managed.

本章在《提示工程基础》所讲授的提示词四要素与角色结构基础上，补充了三种应对更困难任务的技巧：少样本提示，通过已完成的示例而非仅凭文字描述来教会模型完成任务(Brown 等人，2020);思维链提示，通过带推理过程的示例(Wei 等人，2022)或零样本触发短语(Kojima 等人，2022)引出逐步推理，并可辅以自洽性(Wang 等人，2022)、以额外的推理成本换取更高的可靠性；以及结构化输出，借助提供商层面的模式强制机制来保证回答可被程序解析。本主题群的下一个模块，《高级上下文工程：长上下文与上下文预算》(`advanced/05-advanced-context-engineering-long-context-and-budgeting.md`),将直接接续第1节末尾提到的"上下文预算"这一权衡问题继续展开，把有限的上下文窗口本身当作一种需要主动管理的资源来对待。

## References

**参考文献**

### External Sources

- [Language Models are Few-Shot Learners (Brown et al., 2020, arXiv:2005.14165)](https://arxiv.org/abs/2005.14165)
- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Wei et al., 2022, arXiv:2201.11903)](https://arxiv.org/abs/2201.11903)
- [Large Language Models are Zero-Shot Reasoners (Kojima et al., 2022, arXiv:2205.11916)](https://arxiv.org/abs/2205.11916)
- [Self-Consistency Improves Chain of Thought Reasoning in Language Models (Wang et al., 2022, arXiv:2203.11171)](https://arxiv.org/abs/2203.11171)
- [Claude Docs — Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Claude Docs — Define Tools (Tool Use)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
- [OpenAI Platform — Structured Outputs Guide](https://developers.openai.com/api/docs/guides/structured-outputs)

### Internal Cross-References

- [`introductory/05-prompt-engineering-fundamentals.md`](../introductory/05-prompt-engineering-fundamentals.md) — direct prerequisite: prompt anatomy, roles, zero-shot prompting, temperature.
- [`introductory/06-context-windows-tokens-and-memory-basics.md`](../introductory/06-context-windows-tokens-and-memory-basics.md) — prerequisite definitions of token and context window used in Sections 1 and 5.
- [`introductory/04-tool-use-and-function-calling-basics.md`](../introductory/04-tool-use-and-function-calling-basics.md) — conceptual background for the tool-use mechanism referenced in Section 5.
- [`advanced/05-advanced-context-engineering-long-context-and-budgeting.md`](../advanced/05-advanced-context-engineering-long-context-and-budgeting.md) — direct continuation: context budgeting as a general resource-management problem.
