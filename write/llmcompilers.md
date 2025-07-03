# LLMs as compilers
2025/7/2 by Kadhir
https://resync-games.com/blog/engineering/llms-as-compiler


So far, I've only used LLMs as an assistant, where I'm doing something, and an LLM helps me along the way. Code autocomplete feels like a great example of how useful it can be when it gets it right. I don't doubt that over time this will improve, but I'm excited to see a more significant transition from this assistant mode to a compiler mode, at least for coding.

It will be exciting when we focus solely on the context we fed the LLM, then test the features it generates rather than the code. And importantly, we let the LLM handle integrating new features into the existing codebase. That means we no longer examine the code. Our time as engineers will be spent handling context, testing features, and iterating on them.

The consequence of that seems to be:

    - Democratize access to engineering
        - You don't need as specialized skillsets to build complex apps, you just need to know how to put context together and iterate
    - Increase the velocity of feature development
        - My gut says dealing with context will result in a better ratio of engineering time into features shipped than dealing with code directly
The obvious pushback here is, well, compilers are provable. There's a straightforward mapping between inputs and outputs, and we can prove the outputs are the same each time. We can also write tests to ensure the outputs are optimized.

But if we squint, a compiler transforms an input into an output. If we treat the code as an intermediate layer, viewing the input as context and the output as features, then we can demonstrate that the compiler is reliable through evaluations and testing. And importantly, we don't have to get the output right in the first go, we can let it iterate over and over until it gets it right. A new kind of compiler.

So I propose that if we get LLM-as-a-compiler, as a software engineer, I will go through this cycle:

1. Put together the context
    - Which includes a series of tests for the final behavior (perhaps I use an LLM for this)
2. I put it through the LLM compiler
    - Which is probably a system composed of several things
3. Which continually iterates on the output until all the tests pass
    - Ideally, as the LLM compiler gets better, the latency gets lower and lower
4. We cache the output (code) for performance improvements
5. I decide how I need to edit the context, and go back to step 1

SWE agents feel like they're the right abstraction on this path; they convert context into features, iterating in the background. They feel like they'll be an integral part of the LLM compiler system, which I think will have the following pieces:

- A way to specify the context of my app
    - And a way to specify which part of my context to focus on
- Mechanism for specifying my reward signal (my tests)
- A system for monitoring the changes happening
    - And a way to redirect parts of the compiler if it's not doing what I expect
    - Over time, I'd expect this part to evolve and the need to see the code to reduce

# Resources

1. Vivek Haldar - LLMs are compilers
Vivek Haldar
Feb 26, 2023

LLMs are compilers
I’ve been thinking about a fruitful way to frame the act of writing code in the age of Copilot/Codex, and I don’t think “autocomplete on steriods” is it. Prompt-driven programming with an LLM is better thought of as a compiler. Just like what we understand as a compiler today translates from a high-level programming language like C++ or Java to machine code (actually, assembly language), you could view an LLM as a compiler that translates from English to a high-level language.

The hottest new programming language is English

— Andrej Karpathy (@karpathy) January 24, 2023
Programming in assembly language used to be a skill. That skill became irrelevant when good optimizing compilers could translate high-level languages to performant assembly (and when whatever tiny difference remained got swamped by gains in CPU speed). Nobody argues today that programming should be done in assembly.

Today we’re living through a similar transition to a higher level of abstraction. Code in HLLs is becoming the output of an even higher-level language– the natural language prompt to an LLM.

Here are a few examples to drive the point home:

Copilot easily passes “Intro to CS” courses: In this paper, the authors found that on a set of CS101-level programming problems, Copilot solved half of them right away (just feeding it the problem description itself), and solved 60% of the rest with only changes to the problem description.

Other observations have shown that when the output from tools like Copilot is wrong, developers avoid debugging the generated code, and either fiddle with the prompt until it works, or rewrite the code from scratch.


And here is Prof. Crista Lopes (1, 2, 3, 4) trying to grab the CS education community by the shoulders and shake them, after getting surprisingly good results with ChatGPT when implementing a lexer and parser for a toy programming language– a problem common in graduate-level compilers courses.

The neural network was able to understand the concrete symbolic reasoning of a Lox tokenizer purely by examples; it was able to generalize well beyond the examples; it was able to correct my specification mistakes; … bottom line: it is able to tokenize Lox programs without a single line of code being written.

Obviously, I am “programming” it by teaching it the rules using a combination of natural language and examples. But this is not programming as we know it. This is a blend of old ideals such as “do what I mean” and programming by example, but on steroids. While I am very familiar with these old ideals, I never thought I would live to see the day where they were a reality!

Taking the compiler analogy even further are systems like Parsel, which takes in a spec that mimics the way human programmers think, in that the spec decomposes the problem to be solved into smaller sub-problems, along with function signatures and a few input-output examples (i.e. unit tests), and produces code for that higher-level problem. The authors have recently made advances that let you omit the input-output examples, and even omit the function signatures, generating code from a natural language breakdown of the problem!

Parsel🐍 update: you now don't need to write function names/args at all - it's literally just indented natural language!

Images show 4 lines of Parsel and the generated 114-line Python code
Try or contribute here! https://t.co/vZ33rNFzuX
Last thread: https://t.co/SAJzbD9lKL pic.twitter.com/LsASh6OBhI

— Eric Zelikman (@ericzelikman) February 14, 2023
 
Of course, Copilot is not perfect. It still generates incorrect code, even though the hit-rate is pretty good. The question is: do you think it’ll get better or worse in the future? Programmers today never have to peel back the curtain to debug the assembly language generated by modern compilers (unless you’re a compiler writer). Sooner or later, code LLMs will achieve the same level of reliability, truly making them compilers from English to working code.


2. Dave Hoover - LLM as Compiler

LLM as Compiler
Dave Hoover
Dave Hoover

Follow
5 min read
·
Oct 3, 2023
68




I have a strong hunch that we are fast approaching the next revolution in programming languages.

A little history
In 1972, we were suddenly able to write programs in C, a watershed moment for the software industry. In 1987, we were suddenly able to write programs in Perl, followed by Python, Ruby, JavaScript, Java, and then C#. When C was released, it was considered a “high level” programming language. But when Perl and friends were released, they were considered “high level”, and interestingly, they were all written in C. The C programming language was expressive enough to allow a generation of language designers to use it to invent even more expressive and powerful languages.

Now, in 2023, we’re seeing the emergence of a technology that could reframe “Perl and friends” in the same way that they reframed C. After paying close attention to software engineering for 23 years, along with some recent conversations, I cannot shake the feeling that a specialized Large Language Model (LLM) will power the next programming language revolution.

Incepting conversations
I have two friends who got excited about AI early while I’ve been a bit of a laggard, too busy to dive deeply into the tech or implications.

The first is Kevin Solorio, who’s been in my ear since 2020 about machine learning, followed by AI and LLMs more recently. At a dinner together back in June, Kevin mentioned that he thought something like Cucumber could be a good way to communicate to an LLM what sort of application it should then generate. My summer has been a bit of a disaster, so I immediately forgot what Kevin suggested as I had bigger fish to fry in the present than to think about the future.

The second is Ryan Prinz, a software engineer with a product management background. Ryan and I took a walk together in September when he told me about his explorations into test-driven development and LLMs. This time it started to click for me, especially as Ryan asked me about the decade that spawned everything from JUnit to Selenium to RSpec, and finally Cucumber in 2008. I wasn’t heavily involved in any of those specific projects, but I’ve spent time with all of their creators. Through Ryan’s explanations, I started to see the possibility that a specialized LLM could generate code while a product developer used a natural-language-based technology like Cucumber to specify in enough detail to help the LLM understand the desired behavior.

Ryan and I considered a few people who we should talk to next, and I suggested Ward Cunningham. Ward was kind enough to write the forward to my book, Apprenticeship Patterns, so I had his contact information. He quickly agreed to chat with us. Ward is a recently-retired software pioneer. He invented and contributed to many highly influential things over his career, including the wiki, which then, incredibly, gave rise to the emergence of Wikipedia. Ryan and I had two wide-ranging discussions with Ward over the course of a week. We wanted to run these ideas past him to see what he thought. At the end of our first discussion, after he had listened for a while, he gave us a wonderful bit of encouragement:

“Nobody asked for the wiki.”

Get Dave Hoover’s stories in your inbox
Join Medium for free to get updates from this writer.

Enter your email
Subscribe
At the beginning of our second conversation, Ward said he’d been thinking about what we were describing and thought it made sense. We learned a lot from our conversations with Ward, but our biggest takeaway was that he wasn’t telling us we were off track.

Disclaimer
What I’m imagining is purely conceptual. Kevin and Ryan have both actively worked with AI-assisted technologies as well as learned far more than I have about the tech behind them. I hope that we, with a community of others, can keep discussing this and do some more thorough experimentation.

The vision
Some programming languages are compiled (C and Java) and some are interpreted (Python and JavaScript). A compiled language generates an intermediate artifact that is then interpreted by a runtime. An interpreted language has no intermediate artifact. The interpreter directly executes the specified code.

My vision for this next revolution is that we will initially have a compiled language, though it could eventually evolve to become interpreted. The programming language will be compiled via the following steps:

Specify the high-level behavior using something like Cucumber’s Gherkin.
Specify in more technical detail, using programming by wishful thinking, using something like Cucumber’s Step Definitions. A GitHub-Copilot-like tool could assist in writing these step definitions in one’s preferred “Perl and friends” language.
Feed steps 1 & 2 to the specialized LLM, which acts as a compiler and generates the resulting codebase.
The resulting codebase can be executed by the appropriate “Perl and friends” runtime.
Manually verify the behavior of the code. If the behavior needs to change, goto step 1.
The implications
To the extent that we achieve “LLM as Compiler”, we are once again going to have an incredible boost in developer productivity, similar to the boosts with C in 1972 and Perl in 1987. A C programmer is an order of magnitude more productive than a programmer writing in Assembly. A “Perl and friends” programmer is an order of magnitude more productive than a programmer writing in C. And soon, someone who can specify the behavior of a software system in something like Cucumber, will be an order of magnitude more productive than someone writing in “Perl and friends”.

Now, there are still specific problems that can only be solved with low-level languages, and they will always be with us. People still have to be able to work completely up and down the stack. People learn and use Assembly and C/C++ every day. “LLM as Compiler” won’t eradicate the current programming languages, but it will, once again, make it easier for people to tell computers what to do.

“LLM as Compiler” is a different way of using AI to boost programmer productivity. The typical way that people are boosting their productivity is “LLM as Teammate”, which already works via tools like GitHub Copilot and ChatGPT. The Compiler vs Teammate approaches are not mutually exclusive, and are actually quite complementary.

Today, a cross-functional product development team tends to consist of a product manager, a UX designer, a UI designer, and multiple software engineers. An “LLM as Compiler” could mean that team has a single software engineer. I don’t believe that means we’ll need 80% fewer software engineers. I believe that means we’ll have 5x as many product development teams. Why do I believe that? I’ll share more in my next post.



3. Avik Das - LLMs are like compilers, sort of
LLMs are like compilers, sort of
May 5, 2025 • Avik Das

An AI-generate image of two monitor-like things, one displaying text, the other displaying binary and other incomprehensible text. To the left of the first monitor are some speech bubbles.

An AI-generated image, appropriate for this post. The machine on the left is like an LLM, taking in prompts and producing code. The machine on the right is like a compiler, producing binaries. I tried really hard to generate a good image with AI, but my needs seem too esoteric. That's been my experience with AI coding too.
I’m no expert on LLMs and coding with AI. In fact, I feel like I’ve fallen behind. I’m still in the initial phases of trying out AI-augmented coding. This blog post is my attempt at addressing my own reservations about this new world by comparing current AI to early compilers. The audience is myself, but maybe it’ll help someone who’s hesitant to use AI in their day-to-day coding.

Whenever I have a gut reaction against AI coding, I remind myself: compilers faced the same backlash, but eventually, compilers (and high-level languages) enabled solving more complex problems faster, to the point of becoming indispensable tools. With that in mind, I shouldn’t dismiss AI coding.

As I sat down to write this blog post, I found someone else had already written a version of it: When Compilers Were the ‘AI’ That Scared Programmers. I’ll rehash some of Vivek’s arguments, but Vivek is definitely pro-AI. I additionally want to explore another angle in my post.

The complaints against are overblown
My initial reaction to AI coding could apply almost point-by-point to early compilers:

LLMs produce bad code. “Bad” can mean inefficient, or even buggy. Early compilers also produced bad code. But compilers got better, and so will AI.

You’re giving up control. Same with (high-level) compilers, where you no longer decide exactly how your code maps to the actual execution on your machine. In exchange, you get to think about problems at a higher level, not worrying about… the execution on your machine.

You lose out on understanding the fundamentals of your software, so when things go wrong, you can’t fix it. For many people, being able to solve complex problems is more valuable than the few times when things go catastrophically wrong. Think scientists who are just trying to model something, and they don’t actually care about being expert programmers or computer scientists. Meanwhile, for those of us whose core job is writing software, compilers haven’t changed the fact that learning computer science and understanding low-level programming is still useful, hence the utility of a solid computer science degree.

In my time as a programmer, when the end goal was solving a problem, and writing code was just a means to an end, I reached for a high-level language. (Sometimes the constraints, such as writing for a specific hardware target, made that impossible, but I’m talking about software I’ll run on my own computer or similar.) It’s just more productive. Maybe I’ll get to the point where I reach for an LLM.

As a side note: a lot of these same arguments apply to modern IDEs, with their fancy GUIs and auto-completion!

The problem with LLMs: code is a liability
There is one fundamental difference I see with LLMs that I haven’t seen addressed. The way AI coding works today is the LLM spits out code that you have to maintain. The original prompts are no longer the source of truth, the generated code is. When you fix a bug, the generated code is an input to the LLM, and the next iteration changes that code incrementally.

That’s like saying the binary output of a compiler is what you check into source control. The binary is what you edit and the machine code is what you debug. But that’s not how things work today. Today, the original source code is the source of truth. As compilers improve, you recompile the source code to produce a better binary. When you have a bug, you look for logical errors in the source code and modify that until the produced binary does what you want. This would be as if you stored only the LLM prompts, and you evolved the prompts incrementally, running the LLM from a blank slate each time you want to execute your software. (I’m ignoring incremental builds, but in general, a clean build is always possible with a compiler.)

One day, AI may become deterministic enough that we would indeed just store the prompts as our source of truth. Even compilers can be non-deterministic when performing optimizations, but as long as they preserve the semantics of the source code, we’re okay with giving up full control over the machine code.

Coding for fun
Given all this, you’d think I’m convinced I have to use LLMs all the time. After all, I wouldn’t use a barebones text editor and start writing in assembly, right? I guess I’ll always be an odd one out, because that’s exactly something I like to do for fun! I’ve been writing a compiler for over a decade, and there’s a lot of assembly. In fact, there’s a lot of hand-assembled machine code, and I like it that way. I typically use Vim, with minimal auto-completion and no “go to definition”. Earlier in my career, I made it a point to make one of my work projects “Vim-friendly”: if you couldn’t keep the program in your head and navigate around the codebase by hand, the codebase was too complex.

So even in the 2020’s, when you’d think compilers and IDEs are a given, I enjoy artisanal, hand-crafted code after all. Still, a tool is a tool, and I should learn how to use LLMs to enhance my code. I’m not ready to be left behind.

