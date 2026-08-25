# Prompt Engineering Fundamentals

**提示词工程基础**

| Field   | English                                                           | 中文                                            |
| ------- | ----------------------------------------------------------------- | ----------------------------------------------- |
| Level   | Introductory                                                      | 入门                                            |
| Cluster | Prompt & Context Engineering                                      | 提示与上下文工程                                |
| Author  | Dr. Wei-Ling Tan, Research Scientist — Applied AI Systems, ANU-00 | ANU-00 应用人工智能系统研究员 Wei-Ling Tan 博士 |

---

This chapter is the reader's first hands-on encounter with the single most important skill in
working with large language models: writing the text that tells the model what to do. Everything
here assumes no prior background in machine learning, statistics, or programming — every term is
defined before it is used.

本章是读者第一次真正动手接触与大语言模型打交道时最重要的一项技能：写出告诉模型该做什么的那段文字。本章的写作前提是读者没有任何机器学习、统计学或编程方面的背景知识——每一个术语在使用之前都会先给出定义。

## 1. What Is a Large Language Model, and What Is a Prompt?

**什么是大语言模型？什么是提示词？**

A large language model (LLM) is a computer program trained on enormous amounts of text — books,
websites, code, conversations — so that, given some text as input, it can predict what text is
likely to come next. It does this not by "looking up" answers the way a search engine does, but by
having learned statistical patterns of language: which words, phrases, and ideas typically follow
which others, across billions of examples. When you give an LLM some text and it produces more text
in response, that response is called a completion or a generation.

大语言模型是一种在海量文本——书籍、网页、代码、对话记录——上训练出来的计算机程序，它的能力在于：给定一段输入文字，预测接下来最可能出现的文字。它并不像搜索引擎那样“查找”答案，而是从数十亿个例子中学习到了语言的统计规律——哪些词语、短语和概念通常会跟在哪些词语、短语和概念之后。当你给大语言模型一段文字、它据此生成新的文字作为回应时，这段回应就被称为“补全”或“生成”。

A prompt is the text you give the model as input — the instructions, questions, or material you want
it to act on. Prompt engineering is the practice of deliberately designing that input text so the
model's output is accurate, useful, and in the form you need. It is called "engineering" rather than
"writing" because, as this chapter will show, small and seemingly cosmetic changes to a prompt's
wording, structure, or ordering can produce large, measurable differences in output quality — the
same disciplined, testable mindset used in other kinds of engineering.

提示词是你提供给模型作为输入的文字——你希望模型据以行动的指令、问题或素材。提示工程就是有意识地设计这段输入文字，使模型的输出准确、有用，并且符合你所需要的形式。之所以称为“工程”而非“写作”，是因为本章将会展示：提示词措辞、结构或顺序上看似微小的改动，往往会在输出质量上带来巨大且可测量的差异——这正是其他工程学科所共有的那种严谨、可验证的思维方式。

It is worth being explicit about what prompt engineering is _not_. It is not training or fine-tuning
the model — that is, it does not change the model's internal parameters (the numbers the model
learned during training that encode its knowledge and behavior).

有必要明确说明提示工程“不是”什么。它不是在训练或微调模型——也就是说，它并不会改变模型内部的参数(模型在训练过程中学到的、编码了其知识与行为方式的一组数值)。

A prompt only shapes what the already-trained model does with a single input; the model itself is
unchanged after the conversation ends. This distinction matters because it explains both prompt
engineering's biggest strength (no computing cluster or machine-learning expertise required — anyone
can iterate on a prompt in seconds) and its biggest limitation (a prompt cannot teach the model a
fact or skill it fundamentally does not have).

提示词只是在塑造一个已经训练完成的模型如何处理某一次具体的输入；对话结束后，模型本身并不会发生变化。这一区别之所以重要，是因为它同时解释了提示工程最大的优势(不需要计算集群或机器学习专业知识——任何人都能在几秒钟内反复调整提示词)和它最大的局限(提示词无法让模型学会它原本根本不具备的知识或能力)。

## 2. The Anatomy of a Prompt

**提示词的构成**

A well-formed prompt is rarely just a bare question. It typically combines up to four
distinguishable parts, and naming them separately makes it much easier to reason about what a prompt
is doing and to fix it when it fails.

一个组织良好的提示词很少只是一句孤零零的问题。它通常由最多四个可以区分开来的部分组成，把它们分别命名出来，能让我们更容易分析提示词在做什么、并在它失效时加以修正。

| #   | Part                             | EN                                                                                                                                                                                 | 中文                                                                                                                 |
| --- | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| 1   | **Instruction**（指令）          | the task itself, stated as an imperative: "Summarize the following article in three sentences," "Translate this paragraph into French," "Classify this email as spam or not spam." | 任务本身，以祈使句给出：“用三句话概括下面这篇文章”“把这段文字翻译成法语”“判断这封邮件是否属于垃圾邮件”。             |
| 2   | **Context**（上下文）            | background information the model needs but was not trained specifically to know: a company's style guide, a customer's order history, the rules of a game you have invented.       | 模型完成任务所需、但并非专门在训练中学到的背景信息：某公司的风格指南、某位顾客的历史订单、你自己发明的一套游戏规则。 |
| 3   | **Input data**（输入数据）       | the actual material the instruction should be applied to: the article to summarize, the paragraph to translate, the email to classify.                                             | 指令实际要作用的材料：待概括的文章、待翻译的段落、待判断的邮件正文。                                                 |
| 4   | **Output indicator**（输出指示） | a description of the form the answer should take: "Answer in a single word," "Return valid JSON with keys `label` and `confidence`," "Write no more than 100 words."               | 对答案应呈现形式的说明：“只用一个词回答”“返回带有 `label` 和 `confidence` 两个字段的有效 JSON”“字数不超过 100 字”。  |

Not every prompt needs all four parts — a casual question needs only an instruction — but as tasks
become more specific, leaving a part out is the single most common cause of a disappointing answer.
Consider the bare prompt "Summarize this," pasted above a long news article, with nothing else. The
model has no length target, no audience, and no sense of what to emphasize, so it will guess — and
different runs may guess differently.

并非每一个提示词都需要包含全部四个部分——一句随意的提问只需要一条指令即可——但随着任务变得越来越具体，遗漏某个部分正是导致答案令人失望的最常见原因。设想一个只写着“概括一下”的提示词，上面粘贴着一整篇长新闻，别无其他。模型不知道概括应该多长、面向什么样的读者、该突出哪些重点，于是只能靠猜测——而不同的运行之间，猜测的结果也可能不一样。

Compare that with: "Instruction: Summarize the following news article for a reader who has no
background in the topic. Output indicator: three plain-language sentences, no jargon. Input data:
[article text]." The second version removes almost all of the model's guesswork, and that reduction
in ambiguity is the practical core of prompt engineering.

再对比这样一个版本：“指令：请为一位对该话题毫无背景知识的读者概括下面这篇新闻报道。输出指示：用三句通俗易懂的话，不使用专业术语。输入数据：[文章正文]。”第二个版本几乎消除了模型所有的猜测空间，而正是这种对歧义的消除，构成了提示工程实践中最核心的部分。

## 3. Roles: System, User, and Assistant

**角色：系统、用户与助手**

Most modern LLM interfaces — including the ones used to build production applications — organize a
conversation into messages, each tagged with a role. The three roles a beginner will encounter first
are system, user, and assistant.

大多数现代大语言模型接口——包括用于构建生产级应用的接口——都会把一次对话组织成一条条带有“角色”标签的消息。初学者最先会接触到的三种角色是：系统、用户和助手。

| Role                  | EN                                                                                                                                                                                                                                                                                                                                            | 中文                                                                                                                                                                                                         |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **System**（系统）    | sets standing instructions that apply for the whole conversation — the model's persona, its general behavior rules, and any constraints that should hold no matter what the user asks next: "You are a customer support assistant for a bicycle rental company. Always be polite. Never quote a price outside the official price list below." | 设定的是贯穿整场对话的常设指令——模型的人设、总体行为规则，以及无论用户接下来问什么都必须遵守的各种约束条件，例如：“你是一家自行车租赁公司的客服助手。请始终保持礼貌。除下方官方价目表外，不得报出任何价格。” |
| **User**（用户）      | is where the specific request or question is placed — this is what a person (or another program) actually typed.                                                                                                                                                                                                                              | 用来放置具体的请求或问题——也就是一个人(或另一个程序)实际输入的内容。                                                                                                                                         |
| **Assistant**（助手） | holds the model's own previous responses when a conversation has more than one turn, which lets the model refer back to what it already said.                                                                                                                                                                                                 | 当一次对话包含多个回合时，会保存模型此前自己给出的回应，使模型能够回顾自己已经说过的话。                                                                                                                     |

Anthropic's official prompt engineering documentation and OpenAI's own guide both organize their
recommended techniques around exactly this system/user split, treating the system message as the
place for durable role and policy framing and the user message as the place for the task at hand.

Anthropic 官方的提示工程文档与 OpenAI 自身的指南，都正是围绕这套系统/用户的划分来组织各自推荐的技巧的：系统消息用来承载长期不变的角色设定和策略框架，用户消息则用来承载当下要处理的具体任务。

Getting the role right matters because it changes how firmly the model treats an instruction. A
constraint stated in the system message ("never reveal internal pricing") is generally treated as a
standing rule that should survive the rest of the conversation, while a constraint buried inside a
long user message competes for attention with everything else in that message. A beginner's most
common early mistake is putting everything — persona, rules, and the actual question — into one
undivided block of user text; separating durable instructions into the system role, when the
interface offers one, is one of the simplest reliability improvements available.

角色设置是否恰当，会直接影响模型对待某条指令的坚定程度。写在系统消息里的约束(例如“绝不透露内部定价”)通常会被当作一条应当贯穿整场对话的常设规则来遵守，而埋在一大段用户消息里的约束，则要与该消息中其他所有内容争夺模型的“注意力”。初学者最常犯的早期错误，就是把人设、规则和真正要问的问题全部塞进同一段不加区分的用户文字里；只要接口提供了系统角色，把长期有效的指令单独放进系统消息中，就是能获得的最简单、也最立竿见影的可靠性改进之一。

## 4. Zero-Shot Prompting

**零样本提示**

Zero-shot prompting means asking the model to perform a task by describing it in words alone,
without showing the model any worked examples of the task being done correctly. "Is the sentiment of
this review positive or negative?" followed by a review, with no example reviews and labels shown
first, is a zero-shot prompt.

零样本提示是指仅用文字描述任务，让模型据此执行任务，而不向模型展示任何“任务应如何正确完成”的示例。比如“这条评论的情感是正面还是负面？”后面直接跟着一条评论正文，前面不给出任何带标签的示例评论——这就是一个零样本提示。

Large language models are able to do this at all — follow a task description they have never seen
phrased exactly that way before — because of a property called in-context learning: the ability of a
sufficiently large model to infer what is wanted from the immediate prompt text alone, without any
update to its parameters.

大语言模型之所以能够做到这一点——遵循一段它此前从未以完全相同措辞见过的任务描述——依赖于一种被称为“上下文学习”的特性：一个规模足够大的模型，仅凭当前提示词本身的文字，就能推断出用户想要什么，而无需对其参数做任何更新。

Brown et al.'s 2020 paper introducing GPT-3, "Language Models are Few-Shot Learners," is the paper
that first documented this capability at scale and gave the field the vocabulary of "zero-shot,"
"one-shot," and "few-shot" evaluation that is now standard (see References).

Brown 等人于 2020 年发表的论文《Language Models are Few-Shot Learners》(该论文首次公开了 GPT-3)最早在大规模上记录了这种能力，并为这一领域确立了“零样本”“单样本”“少样本”评测这套如今已成为标准的术语(见“参考文献”)。

Zero-shot prompting is the natural starting point for almost any task because it requires the least
prompt-construction effort, and modern instruction-tuned models — models specifically trained to
follow natural-language task descriptions, which is what virtually every commercial LLM product is
today — are often good enough at zero-shot performance that no examples are needed at all. The
intermediate module `05-advanced-prompting-cot-few-shot-structured-output.md` builds directly on
this idea, introducing few-shot prompting (showing the model worked examples) and chain-of-thought
prompting (asking the model to reason step by step) as techniques for the cases where zero-shot
alone is not reliable enough.

零样本提示几乎是所有任务最自然的起点，因为它所需的提示词构造成本最低，而现代的“指令微调模型”(即专门训练用来遵循自然语言任务描述的模型，如今几乎所有商用大语言模型产品都属于此类)在零样本表现上往往已经足够出色，根本无需示例。中级模块《进阶提示工程：思维链、少样本与结构化输出》(`05-advanced-prompting-cot-few-shot-structured-output.md`)正是在这一基础之上展开的，它引入了少样本提示(向模型展示已完成的示例)和思维链提示(要求模型逐步推理)这两种技巧，用于应对仅靠零样本还不够可靠的情形。

## 5. Clarity and Specificity

**清晰与具体**

The single highest-leverage habit in prompt engineering is stating exactly what you want, in
concrete rather than vague terms, and removing information the model would otherwise have to guess.
This sounds obvious, but it is violated constantly because natural language allows vague requests
that a human listener could resolve using shared context the model does not have.

提示工程中收益最高的一个习惯，就是用具体而非笼统的措辞，准确说出你想要什么，并去掉那些原本要靠模型自行猜测的信息。这听起来是常识，但在实践中却常常被违背，因为自然语言允许模糊的表达方式，而人类听者可以借助双方共享的背景知识去化解这种模糊，模型却没有这份共享背景。

Consider the instruction "Write something about dogs." This is ambiguous along at least four
independent dimensions: length (a tweet or a textbook chapter?), tone (playful or scientific?),
audience (a child or a veterinarian?), and purpose (to entertain, to inform, to persuade someone to
adopt one?). Each unresolved dimension is a place where the model must guess, and a guess that does
not match what the requester actually wanted looks, from the outside, like the model "failing" —
when in fact the prompt simply under-specified the task.

以指令“写点关于狗的东西”为例，它至少在四个相互独立的维度上是含糊不清的：篇幅(是一条推文，还是一整章教材？) 、语气(俏皮还是严肃？) 、受众(儿童还是兽医？) 以及目的(娱乐、科普，还是劝说别人领养一只狗？) 。每一个未被明确的维度，都是模型必须靠猜测来填补的空白，而一旦猜测的结果与提问者真正想要的不一致，从外部看就像是模型“失败”了——但实际上，问题出在提示词本身对任务的界定不足。

A better version resolves each dimension explicitly: "Write a 150-word, upbeat paragraph aimed at a
general adult audience, encouraging them to consider adopting a shelter dog. Mention that shelter
dogs are usually already house-trained." OpenAI's and Anthropic's official prompt engineering guides
both list "be specific and descriptive" and "give the model the context it needs" among their first
recommended techniques for exactly this reason (see References).

一个更好的版本会把每个维度都明确交代清楚：“请写一段约150字、语气积极的段落，面向普通成年读者，鼓励他们考虑领养一只收容所里的狗。请提及收容所的狗通常已经完成了如厕训练。” OpenAI 和 Anthropic 各自官方的提示工程指南，都把“具体而详尽”以及“为模型提供它所需要的背景信息”列为最优先推荐的技巧之一，原因正在于此(见“参考文献”)。

Specificity also means telling the model what _not_ to do when a failure mode is predictable. If a
customer-support prompt has previously produced answers that promise refunds the company cannot
actually give, adding an explicit negative constraint — "Do not promise a refund under any
circumstances; direct the customer to a human agent instead" — is often more effective than hoping a
positive instruction alone will prevent the behavior, because it removes the specific failure from
the space of things the model considers acceptable.

具体性同样包括在某种失败模式可以预见时，明确告诉模型“不要做什么”。如果某个客服提示词此前生成过承诺公司实际上无法兑现的退款的回答，那么加入一条明确的否定性约束——“在任何情况下都不得承诺退款；应引导顾客转接人工客服”——往往比仅靠一条正面指令、寄望于它能自然避免这种行为更为有效，因为这条约束把这一具体的失败情形直接从模型认为可接受的选项范围中排除了出去。

## 6. Controlling Output Format

**控制输出格式**

Beyond telling the model _what_ to say, a prompt can — and often should — tell the model _how_ to
say it. This matters enormously once a prompt's output is meant to be read by another piece of
software rather than a person: a program that expects a number cannot handle "The answer is
approximately forty-two, though it could be a bit higher."

除了告诉模型“要说什么”，提示词还可以——而且往往应该——告诉模型“该怎么说”。一旦提示词的输出是要交给另一段软件读取，而不是给人看的，这一点就变得极其重要：一个期望拿到一个数字的程序，是无法处理“答案大约是四十二左右，不过也可能略高一些”这样的表述的。

The simplest format controls are direct instructions: "Answer with only the number, no other text,"
"Respond in exactly one sentence," "Use a numbered list." A more structured technique, recommended
in Anthropic's prompting-best-practices documentation, is to use clearly delimited tags to separate
different parts of a prompt and to specify the exact output shape, for example wrapping the input
text in `<document>...</document>` tags and asking the model to place its answer inside
`<answer>...</answer>` tags — the visual delimiters make it unambiguous, both to the model and to
any code parsing the response afterward, where one part ends and the next begins.

最简单的格式控制方式是直接给出指令：“只用数字回答，不要有其他文字”“用恰好一句话回答”“用带编号的列表呈现”。 Anthropic 提示工程最佳实践文档中推荐的一种更结构化的技巧，是使用界限清晰的标签来分隔提示词的不同部分，并明确规定输出的具体形态——例如用 `<document>...</document>` 标签把输入文本包裹起来，并要求模型把答案放进 `<answer>...</answer>` 标签之中。

The intermediate module in this cluster (`05-advanced-prompting-cot-few-shot-structured-output.md`)
goes further into this idea with strict, schema-validated structured output (for example, JSON that
conforms to a fixed set of fields) — a technique that requires understanding tokens and context,
covered in `06-context-windows-tokens-and-memory-basics.md`, and is best introduced after this
foundation is in place.

这种可视化的分隔符，无论对模型本身、还是对之后解析该回应的代码而言，都能清楚地标明一部分在哪里结束、下一部分从哪里开始，不留歧义。本主题群中的中级模块(《进阶提示工程：思维链、少样本与结构化输出》,`05-advanced-prompting-cot-few-shot-structured-output.md`)会在这一思路上进一步展开，介绍具备严格模式校验的结构化输出(例如符合固定字段集合的 JSON)——这项技巧需要理解词元与上下文的相关知识，这部分内容由《上下文窗口、词元与记忆基础》(`06-context-windows-tokens-and-memory-basics.md`)讲授，最好在打好本章这一基础之后再学习。

## 7. Iteration: Prompting as a Design Process

**迭代：把提示词写作当作一个设计过程**

A prompt that works well is very rarely the first draft. Prompt engineering, practiced seriously,
looks less like writing a single sentence and more like an iterative design loop: write a prompt,
run it, inspect the output, identify exactly what went wrong or what was ambiguous, revise, and run
it again. This loop matters because language models are not fully deterministic in general use
(their outputs can vary between runs even on the same input, particularly at higher randomness
settings — see the note on temperature below) and because a prompt that works on one example may
silently fail on a slightly different one.

一个效果良好的提示词，几乎从来都不是一稿而就的。认真实践提示工程，与其说是在写一句话，不如说更像是一个迭代式的设计循环：写出提示词、运行它、检查输出结果、准确找出哪里出了问题或存在歧义、修改、再次运行。这个循环之所以重要，是因为大语言模型在一般使用场景下并非完全确定性的(即便输入完全相同，不同运行之间的输出也可能有所差异，尤其是在随机性设置较高的情况下——参见下文关于“温度”参数的说明)，也因为一个在某个例子上表现良好的提示词，换到一个略有不同的例子上，可能会悄无声息地失效。

A practical iteration workflow for a beginner looks like this: (1) write a first-draft prompt
covering instruction, context, input, and output indicator; (2) test it against several different
realistic inputs, not just the one you had in mind while writing it; (3) for every output that is
wrong or oddly formatted, ask specifically _which_ of the four prompt parts was ambiguous or
missing, rather than vaguely rewriting the whole prompt; (4) fix that one part; (5) re-test against
the full set of inputs again, since a fix for one case can sometimes break another.

一个适合初学者的实用迭代流程大致如下：(1)写出涵盖指令、上下文、输入数据、输出指示这四个部分的初稿；(2)用若干个不同的、贴近真实场景的输入来测试它，而不只是用你写提示词时脑子里想着的那一个例子；(3)对于每一个错误或格式怪异的输出，要具体追问四个部分中“哪一个”存在歧义或缺失，而不是笼统地把整个提示词推倒重写；(4)只修正这一个部分；(5)再次针对全部输入集合重新测试，因为针对某一种情况的修正，有时会破坏另一种情况下原本正确的结果。

This same discipline scales up directly into the practice, common at organizations building
production LLM systems, of maintaining a small test set of representative inputs and expected
behaviors that every prompt revision is checked against before being deployed — a lightweight
version of what software engineers call regression testing, applied to prompts.

这套纪律可以直接扩展为构建生产级大语言模型系统的机构中普遍采用的做法：维护一个由代表性输入和预期行为组成的小型测试集，每一次提示词的修改在上线部署前都要在这个测试集上过一遍——这本质上是软件工程中“回归测试”概念的一个轻量版本，应用在了提示词上。

One parameter worth defining here, because it directly affects how iteration should be interpreted,
is temperature. Temperature is a setting, typically a number from 0 upward, that controls how much
randomness the model uses when choosing its next word: a temperature near 0 makes the model
consistently pick its single most likely next word, producing very similar output across repeated
runs on the same prompt, while a higher temperature allows less-likely words to be chosen more
often, producing more varied and sometimes more creative — but also less predictable — output.

这里有一个值得专门定义的参数，因为它直接影响我们该如何看待“迭代”这件事，那就是“温度”。温度是一个设置项，通常取值从 0 起往上，用来控制模型在选择下一个词时所使用的随机程度：温度接近 0 时，模型会稳定地选择它认为最可能出现的下一个词，因而在同一提示词下反复运行时，输出会非常相似；温度较高时，一些原本可能性较低的词被选中的概率会提高，输出因此更加多样、有时也更具创造性——但也相应地更难预测。

Historically, both OpenAI's and Anthropic's API documentation exposed this as an adjustable request
parameter, and it remains so for most current models — but this is no longer universal: as of this
writing, Anthropic's own migration documentation states that its newest model releases (Claude Opus
4.7 and later, and Claude Sonnet 5) reject a non-default `temperature` (along with `top_p` and
`top_k`) with a request error, on the stated rationale that well-crafted system and user
instructions are a more reliable behavior lever than sampling-layer tuning for these models.

历史上，OpenAI 和 Anthropic 各自的 API 文档都把温度作为一个可调节的请求参数开放给使用者，对大多数当前模型而言依然如此——但这已不再是普遍适用的规则：截至本文写作时，Anthropic 官方的迁移文档指出，其最新发布的一批模型（Claude Opus 4.7 及更新版本、Claude Sonnet 5）会拒绝非默认值的 `temperature`（以及 `top_p`、`top_k`）参数并返回请求错误，官方给出的理由是：对于这些模型而言，精心设计的系统消息与用户指令，是比采样层面的参数调节更可靠的行为调控手段。

The underlying _concept_ taught in this section — that sampling randomness exists and shapes output
variability — still applies to every model; only whether a given model's API lets you _adjust_ it
directly is provider- and model-specific and changes over time, so check the current API reference
for the exact model you are calling before assuming this parameter is available. For tasks where
consistency matters (classification, data extraction, following a strict format), a low temperature
(on models that still expose it) is usually preferable; for open-ended creative writing, a higher
temperature is often desirable.

本节所讲授的底层*概念*——采样过程中存在随机性、并会影响输出的多样程度——依然适用于每一个模型；唯一会因服务商与具体模型而异、且会随时间变化的，是该模型的 API 是否允许你*直接调节*这个参数，因此在假定这个参数一定可用之前，请查阅你实际调用的那个模型的最新 API 参考文档。对于需要一致性的任务(分类、数据抽取、遵循严格格式)，在仍然开放该参数的模型上，通常更适合使用较低的温度；而对于开放式的创意写作任务，较高的温度往往更受欢迎。

## 8. Common Pitfalls for Beginners

**初学者常见的坑**

Five mistakes account for most of the frustration beginners report when a model's output seems
"wrong" for no clear reason, and recognizing them is often faster than any amount of general
rewriting.

初学者在遇到模型输出“莫名其妙就是不对”时所感到的挫败，大多可以归因于以下五种错误，识别出这些错误，往往比漫无目的地反复重写整段提示词要快得多。

| #   | Pitfall                                                                      | EN                                                                                                                                                                                                                                                                                                       | 中文                                                                                                                                                                                             |
| --- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | **Conflating what you meant with what you wrote**                            | assuming the model shares context that only exists in your head, such as an unstated house style, an abbreviation specific to your team, or an implicit assumption about the reader.                                                                                                                     | 误以为模型和你共享着只存在于你脑海中的背景信息，比如未曾言明的行文风格、团队内部专用的缩写，或是关于读者是谁的隐含假设。                                                                         |
| 2   | **Overloading a single prompt with too many unrelated instructions at once** | this increases the odds that the model satisfies some instructions at the expense of others; breaking a complex request into smaller, sequential prompts is often more reliable than one dense paragraph trying to do everything.                                                                        | 这会增加模型顾此失彼、满足了某些指令却牺牲了另一些指令的概率；把一个复杂的请求拆分成多个更小、按顺序执行的提示词，往往比写一大段试图面面俱到的密集文字更为可靠。                                 |
| 3   | **Omitting the output format entirely**                                      | when the answer will be consumed by code, leading to responses that are individually reasonable but impossible to parse reliably.                                                                                                                                                                        | 当答案要交给代码处理时，却完全没有规定输出格式，导致每一次单独看都还算合理的回应，却无法被稳定地解析。                                                                                           |
| 4   | **Treating a single good or bad run as representative**                      | when a handful of test inputs across plausible edge cases is needed before trusting a prompt.                                                                                                                                                                                                            | 而实际上在信任一个提示词之前，需要用若干个覆盖各种可能边界情形的测试输入来加以验证。                                                                                                             |
| 5   | **Not separating instructions from data**                                    | pasting user-supplied text directly into an instruction without a clear delimiter, which can cause the model to interpret part of the data as an instruction; this is also the root of a security concern (prompt injection) that later modules in the Agent Architecture cluster examine in more depth. | 把用户提供的文本不加清晰分隔地直接粘贴进指令中，这可能导致模型把数据的一部分误当作指令来执行；这也是“提示词注入”这一安全隐患的根源所在，该主题将在“智能体架构”主题群的后续模块中作更深入的探讨。 |

## 9. Worked Example: Building a Prompt from Scratch

**实战示例：从零构建一个提示词**

Suppose the task is: given a customer's free-text product review, decide whether the review is
positive, negative, or mixed, and extract the specific product feature the customer mentions most.
This section walks through four successive drafts to show the iteration process concretely.

假设任务是这样的：给定一位顾客对产品的自由文本评论，判断这条评论是正面、负面还是褒贬不一，并抽取出顾客提及最多的具体产品特征。本节将通过连续四个版本的草稿，具体展示这一迭代过程。

**Draft 1 (bare instruction).** "What does this review say?" — This fails immediately: it does not
ask for sentiment or a feature, and gives the model no output format, so the answer will be an
unstructured paraphrase of unpredictable length.

**草稿一(裸指令)**:“这条评论说了什么？”——这个版本一开始就会失败：它既没有要求判断情感，也没有要求抽取特征，更没有给模型任何输出格式，因此得到的答案只会是一段长度难以预料、结构混乱的复述。

**Draft 2 (adds instruction and output indicator, still zero-shot).** "Instruction: Read the
following product review. Determine whether its overall sentiment is Positive, Negative, or Mixed.
Also identify the single product feature mentioned most. Output indicator: respond in the format
`Sentiment: <value> | Feature: <value>`. Input data: [review text]." This is a large improvement —
the shape of the answer is now fully specified — but it is still zero-shot, so unusual reviews
(sarcasm, reviews about multiple products at once) may still confuse the model about the exact label
boundaries.

**草稿二(加入指令与输出指示，仍为零样本)**:“指令：阅读下面这条产品评论。判断其整体情感是正面、负面还是褒贬不一。同时找出评论中提及最多的那一个产品特征。输出指示：按 `Sentiment: <值> | Feature: <值>` 的格式作答。输入数据：[评论正文]。”这是一个很大的进步——答案的形态已经被完全规定了下来——但它仍然是零样本的，因此一些不寻常的评论(反讽、同时评价多个产品的评论)仍可能让模型在标签的确切边界上产生困惑。

**Draft 3 (adds a negative constraint and an explicit tie-break rule).** Building on Draft 2, add:
"If the review expresses both praise and criticism in roughly equal measure, use Mixed rather than
guessing Positive or Negative. If two features are mentioned an equal number of times, choose the
one mentioned first." This closes two specific ambiguities the author noticed while testing Draft 2
against real reviews — exactly the iteration process described in Section 7.

**草稿三(加入否定约束与明确的平局判定规则)**：在草稿二的基础上补充：“如果评论中褒扬与批评的分量大致相当，请判定为'褒贬不一'，而不要在正面与负面之间随意猜测。如果有两个特征被提及的次数相同，则选择先被提及的那一个。”这补上了作者在用真实评论测试草稿二时发现的两处具体歧义——正是[第 7 节](#7-iteration-prompting-as-a-design-process)所描述的那种迭代过程。

**Draft 4 (final, for machine consumption).** For a prompt whose output will be read by code rather
than a person, the format is tightened further: "Output indicator: respond with only a single line
of valid JSON in the exact form `{"sentiment": "positive"|"negative"|"mixed", "feature": "<short
phrase>"}`, with no text before or after it." This draft is now unambiguous about content, format,
and edge cases — the three axes that Sections 5, 6, and 8 introduced separately are now working
together in one finished prompt.

**草稿四(定稿，供程序读取)**：如果提示词的输出要交给代码而非人来读取，格式还需要进一步收紧：“输出指示：只用一行合法的 JSON 作答，格式严格为 `{"sentiment": "positive"|"negative"|"mixed", "feature": "<简短短语>"}`，前后不得有任何其他文字。”至此，这份草稿在内容、格式和边界情形三个方面都已经不再含糊——第5、6、8节分别引入的这三个维度，如今在这一份完成的提示词中协同发挥了作用。

## 10. Summary and What Comes Next

**小结与后续内容**

This chapter defined prompts, prompt engineering, and in-context learning; walked through the four
parts of a well-formed prompt and the system/user/assistant role structure; introduced zero-shot
prompting and temperature; and practiced the iterative discipline of testing and revising a prompt
against realistic inputs. None of the techniques here required showing the model worked examples or
asking it to reason step by step — those two techniques, few-shot prompting and chain-of-thought
prompting, along with strict schema-validated structured output, are the subject of the intermediate
module that follows directly from this one.

本章定义了提示词、提示工程与上下文学习这几个概念；讲解了一个组织良好的提示词的四个组成部分，以及系统/用户/助手这套角色结构；介绍了零样本提示与温度参数；并练习了针对真实输入不断测试与修改提示词这一迭代纪律。本章的技巧都还没有涉及向模型展示已完成的示例、或要求模型逐步推理——这两项技巧，也就是少样本提示与思维链提示，连同具备严格模式校验的结构化输出，正是紧接本章之后的中级模块所要讲授的内容。

## References

**参考文献**

### External Sources

- [Language Models are Few-Shot Learners (Brown et al., 2020, arXiv:2005.14165)](https://arxiv.org/abs/2005.14165)
- [Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing (Liu et al., 2021, arXiv:2107.13586)](https://arxiv.org/abs/2107.13586)
- [OpenAI Platform — Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Claude Docs — Prompt Engineering Overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
- [Claude Docs — Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

### Internal Cross-References

- [`introductory/02-the-transformer-architecture-and-attention.md`](/academic-neural-unit-00/curriculum/introductory/02-the-transformer-architecture-and-attention.md) — background on how the underlying model processes text (referenced for the reader's general orientation; consult that module directly for its content).
- [`introductory/06-context-windows-tokens-and-memory-basics.md`](/academic-neural-unit-00/curriculum/introductory/06-context-windows-tokens-and-memory-basics.md) — tokens and context windows, needed before structured-output and long-prompt techniques.
- [`intermediate/05-advanced-prompting-cot-few-shot-structured-output.md`](/academic-neural-unit-00/curriculum/intermediate/05-advanced-prompting-cot-few-shot-structured-output.md) — the direct continuation of this chapter: few-shot prompting, chain-of-thought, and structured output.
