The New Skill in AI is Not Prompting, It's Context Engineering
June 30, 2025
5 minute read
Context Engineering is new term gaining traction in the AI world. The conversation is shifting from "prompt engineering" to a broader, more powerful concept: Context Engineering. Tobi Lutke describes it as "the art of providing all the context for the task to be plausibly solvable by the LLM.” and he is right.

With the rise of Agents it becomes more important what information we load into the “limited working memory”. We are seeing that the main thing that determines whether an Agents succeeds or fails is the quality of the context you give it. Most agent failures are not model failures anyemore, they are context failures.

What is the Context?
To understand context engineering, we must first expand our definition of "context." It isn't just the single prompt you send to an LLM. Think of it as everything the model sees before it generates a response.

Context

Instructions / System Prompt: An initial set of instructions that define the behavior of the model during a conversation, can/should include examples, rules ….
User Prompt: Immediate task or question from the user.
State / History (short-term Memory): The current conversation, including user and model responses that have led to this moment.
Long-Term Memory: Persistent knowledge base, gathered across many prior conversations, containing learned user preferences, summaries of past projects, or facts it has been told to remember for future use.
Retrieved Information (RAG): External, up-to-date knowledge, relevant information from documents, databases, or APIs to answer specific questions.
Available Tools: Definitions of all the functions or built-in tools it can call (e.g., check_inventory, send_email).
Structured Output: Definitions on the format of the model's response, e.g. a JSON object.
Why It Matters: From Cheap Demo to Magical Product
The secret to building truly effective AI agents has less to do with the complexity of the code you write, and everything to do with the quality of the context you provide.

Building Agents is less about the code you write or framework you use. The difference between a cheap demo and a “magical” agent is about the quality of the context you provide. Imagine an AI assistant is asked to schedule a meeting based on a simple email:

Hey, just checking if you’re around for a quick sync tomorrow.

The "Cheap Demo" Agent has poor context. It sees only the user's request and nothing else. Its code might be perfectly functional—it calls an LLM and gets a response—but the output is unhelpful and robotic:

Thank you for your message. Tomorrow works for me. May I ask what time you had in mind?

The "Magical" Agent is powered by rich context. The code's primary job isn't to figure out how to respond, but to gather the information the LLM needs to full fill its goal. Before calling the LLM, you would extend the context to include

Your calendar information (which shows you're fully booked).
Your past emails with this person (to determine the appropriate informal tone).
Your contact list (to identify them as a key partner).
Tools for send_invite or send_email.
Then you can generate a response.

Hey Jim! Tomorrow’s packed on my end, back-to-back all day. Thursday AM free if that works for you? Sent an invite, lmk if it works.

The magic isn't in a smarter model or a more clever algorithm. It’s in about providing the right context for the right task. This is why context engineering will matter. Agent failures aren't only model failures; they are context failures.

From Prompt to Context Engineering
What is context engineering? While "prompt engineering" focuses on crafting the perfect set of instructions in a single text string, context engineering is a far broader. Let's put it simply:

Context Engineering is the discipline of designing and building dynamic systems that provides the right information and tools, in the right format, at the right time, to give a LLM everything it needs to accomplish a task.

Context Engineering is

A System, Not a String: Context isn't just a static prompt template. It’s the output of a system that runs before the main LLM call.
Dynamic: Created on the fly, tailored to the immediate task. For one request this could be the calendar data for another the emails or a web search.
About the right information, tools at the right time: The core job is to ensure the model isn’t missing crucial details ("Garbage In, Garbage Out"). This means providing both knowledge (information) and capabilities (tools) only when required and helpful.
where the format matters: How you present information matters. A concise summary is better than a raw data dump. A clear tool schema is better than a vague instruction.
Conclusion
Building powerful and reliable AI Agents is becoming less about finding a magic prompt or model updates. It is about the engineering of context and providing the right information and tools, in the right format, at the right time. It’s a cross-functional challenge that involves understanding your business use case, defining your outputs, and structuring all the necessary information so that an LLM can “accomplish the task."

Acknowledgements
This overview was created with the help of deep and manual research, drawing inspiration and information from several excellent resources, including:
---

- [Tobi Lutke tweet](https://x.com/tobi/status/1935533422589399127) 

tobi lutke

@tobi
I really like the term “context engineering” over prompt engineering. 

It describes the core skill better: the art of providing all the context for the task to be plausibly solvable by the LLM.
---
- [Karpathy tweet](https://x.com/karpathy/status/1937902205765607626) 

Andrej Karpathy
@karpathy
+1 for "context engineering" over "prompt engineering".

People associate prompts with short task descriptions you'd give an LLM in your day-to-day use. When in every industrial-strength LLM app, context engineering is the delicate art and science of filling the context window with just the right information for the next step. Science because doing this right involves task descriptions and explanations, few shot examples, RAG, related (possibly multimodal) data, tools, state and history, compacting... Too little or of the wrong form and the LLM doesn't have the right context for optimal performance. Too much or too irrelevant and the LLM costs might go up and performance might come down. Doing this well is highly non-trivial. And art because of the guiding intuition around LLM psychology of people spirits.

On top of context engineering itself, an LLM app has to:
- break up problems just right into control flows
- pack the context windows just right
- dispatch calls to LLMs of the right kind and capability
- handle generation-verification UIUX flows
- a lot more - guardrails, security, evals, parallelism, prefetching, ...

So context engineering is just one small piece of an emerging thick layer of non-trivial software that coordinates individual LLM calls (and a lot more) into full LLM apps. The term "ChatGPT wrapper" is tired and really, really wrong.
---
- [The rise of "context engineering"](https://blog.langchain.com/the-rise-of-context-engineering/) 

The rise of "context engineering"
5 min read
Jun 23, 2025
Header image from Dex Horthy on Twitter.

Context engineering is building dynamic systems to provide the right information and tools in the right format such that the LLM can plausibly accomplish the task.

Most of the time when an agent is not performing reliably the underlying cause is that the appropriate context, instructions and tools have not been communicated to the model.

LLM applications are evolving from single prompts to more complex, dynamic agentic systems. As such, context engineering is becoming the most important skill an AI engineer can develop.

What is context engineering?
Context engineering is building dynamic systems to provide the right information and tools in the right format such that the LLM can plausibly accomplish the task.

This is the definition that I like, which builds upon recent takes on this from Tobi Lutke, Ankur Goyal, and Walden Yan. Let’s break it down.

Context engineering is a system

Complex agents likely get context from many sources. Context can come from the developer of the application, the user, previous interactions, tool calls, or other external data. Pulling these all together involves a complex system.

This system is dynamic

Many of these pieces of context can come in dynamically. As such, the logic for constructing the final prompt needs to be dynamic as well. It is not just a static prompt.

You need the right information

A common reason agentic systems don’t perform is they just don’t have the right context. LLMs cannot read minds - you need to give them the right information. Garbage in, garbage out.

You need the right tools

It may not always be the case that the LLM will be able to solve the task just based solely on the inputs. In these situations, if you want to empower the LLM to do so, you will want to make sure that it has the right tools. These could be tools to look up more information, take actions, or anything in between. Giving the LLM the right tools is just as important as giving it the right information.

The format matters

Just like communicating with humans, how you communicate with LLMs matters. A short but descriptive error message will go a lot further a large JSON blob. This also applies to tools. What the input parameters to your tools are matters a lot when making sure that LLMs can use them.

Can it plausibly accomplish the task?

This is a great question to be asking as you think about context engineering. It reinforces that LLMs are not mind readers - you need to set them up for success. It also helps separate the failure modes. Is it failing because you haven’t given it the right information or tools? Or does it have all the right information and it just messed up? These failure modes have very different ways to fix them.

Why is context engineering important
When agentic systems mess up, it’s largely because an LLM messes. Thinking from first principles, LLMs can mess up for two reasons:

The underlying model just messed up, it isn’t good enough
The underlying model was not passed the appropriate context to make a good output
More often than not (especially as the models get better) model mistakes are caused more by the second reason. The context passed to the model may be bad for a few reasons:

There is just missing context that the model would need to make the right decision. Models are not mind readers. If you do not give them the right context, they won’t know it exists.
The context is formatted poorly. Just like humans, communication is important! How you format data when passing into a model absolutely affects how it responds
How is context engineering different from prompt engineering?
Why the shift from “prompts” to “context”? Early on, developers focused on phrasing prompts cleverly to coax better answers. But as applications grow more complex, it’s becoming clear that providing complete and structured context to the AI is far more important than any magic wording.

I would also argue that prompt engineering is a subset of context engineering. Even if you have all the context, how you assemble it in the prompt still absolutely matters. The difference is that you are not architecting your prompt to work well with a single set of input data, but rather to take a set of dynamic data and format it properly.

I would also highlight that a key part of context is often core instructions for how the LLM should behave. This is often a key part of prompt engineering. Would you say that providing clear and detailed instructions for how the agent should behave is context engineering or prompt engineering? I think it’s a bit of both.

Examples of context engineering
Some basic examples of good context engineering include:

Tool use: Making sure that if an agent needs access to external information, it has tools that can access it. When tools return information, they are formatted in a way that is maximally digestable for LLMs
Short term memory: If a conversation is going on for a while, creating a summary of the conversation and using that in the future.
Long term memory: If a user has expressed preferences in a previous conversation, being able to fetch that information.
Prompt Engineering: Instructions for how an agent should behave are clearly enumerated in the prompt.
Retrieval: Fetching information dynamically and inserting it into the prompt before calling the LLM.
How LangGraph enables context engineering
When we built LangGraph, we built it with the goal of making it the most controllable agent framework. This also allows it to perfectly enable context engineering.

With LangGraph, you can control everything. You decide what steps are run. You decide exactly what goes into your LLM. You decide where you store the outputs. You control everything.

This allows you do all the context engineering you desire. One of the downsides of agent abstractions (which most other agent frameworks emphasize) is that they restrict context engineering. There may be places where you cannot change exactly what goes into the LLM, or exactly what steps are run beforehand.

Side note: a very good read is Dex Horthy's "12 Factor Agents". A lot of the points there relate to context engineering ("own your prompts", "own your context building", etc). The header image for this blog is also taken from Dex. We really enjoy the way he communicates about what is important in the space.

How LangSmith helps with context engineering
LangSmith is our LLM application observability and evals solution. One of the key features in LangSmith is the ability to trace your agent calls. Although the term "context engineering" didn't exist when we built LangSmith, it aptly describes what this tracing helps with.

LangSmith lets you see all the steps that happen in your agent. This lets you see what steps were run to gather the data that was sent into the LLM.

LangSmith lets you see the exact inputs and outputs to the LLM. This lets you see exactly what went into the LLM - the data it had and how it was formatted. You can then debug whether that contains all the relevant information that is needed for the task. This includes what tools the LLM has access to - so you can debug whether it's been given the appropriate tools to help with the task at hand

Communication is all you need
A few months ago I wrote a blog called "Communication is all you need". The main point was that communicating to the LLM is hard, and not appreciated enough, and often the root cause of a lot of agent errors. Many of these points have to do with context engineering!

Context engineering isn't a new idea - agent builders have been doing it for the past year or two. It's a new term that aptly describes an increasingly important skill. We'll be writing and sharing more on this topic. We think a lot of the tools we've built (LangGraph, LangSmith) are perfectly built to enable context engineering, and so we're excited to see the emphasis on this take off.
---
- [Own your context window](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-03-own-your-context-window.md) 

3. Own your context window
You don't necessarily need to use standard message-based formats for conveying context to an LLM.

At any given point, your input to an LLM in an agent is "here's what's happened so far, what's the next step"
Everything is context engineering. LLMs are stateless functions that turn inputs into outputs. To get the best outputs, you need to give them the best inputs.

Creating great context means:

The prompt and instructions you give to the model
Any documents or external data you retrieve (e.g. RAG)
Any past state, tool calls, results, or other history
Any past messages or events from related but separate histories/conversations (Memory)
Instructions about what sorts of structured data to output
image

Don't take it from me
I heard these folks are pretty smart too.

Screenshot 2025-06-25 at 4 11 45 PM

Screenshot 2025-06-25 at 4 12 59 PM

on context engineering
This guide is all about getting as much as possible out of today's models. Notably not mentioned are:

Changes to models parameters like temperature, top_p, frequency_penalty, presence_penalty, etc.
Training your own completion or embedding models
Fine-tuning existing models
Again, I don't know what's the best way to hand context to an LLM, but I know you want the flexibility to be able to try EVERYTHING.

Standard vs Custom Context Formats
Most LLM clients use a standard message-based format like this:

[
  {
    "role": "system",
    "content": "You are a helpful assistant..."
  },
  {
    "role": "user",
    "content": "Can you deploy the backend?"
  },
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "1",
        "name": "list_git_tags",
        "arguments": "{}"
      }
    ]
  },
  {
    "role": "tool",
    "name": "list_git_tags",
    "content": "{\"tags\": [{\"name\": \"v1.2.3\", \"commit\": \"abc123\", \"date\": \"2024-03-15T10:00:00Z\"}, {\"name\": \"v1.2.2\", \"commit\": \"def456\", \"date\": \"2024-03-14T15:30:00Z\"}, {\"name\": \"v1.2.1\", \"commit\": \"abe033d\", \"date\": \"2024-03-13T09:15:00Z\"}]}",
    "tool_call_id": "1"
  }
]
While this works great for most use cases, if you want to really get THE MOST out of today's LLMs, you need to get your context into the LLM in the most token- and attention-efficient way you can.

As an alternative to the standard message-based format, you can build your own context format that's optimized for your use case. For example, you can use custom objects and pack/spread them into one or more user, system, assistant, or tool messages as makes sense.

Here's an example of putting the whole context window into a single user message:

[
  {
    "role": "system",
    "content": "You are a helpful assistant..."
  },
  {
    "role": "user",
    "content": |
            Here's everything that happened so far:
        
        <slack_message>
            From: @alex
            Channel: #deployments
            Text: Can you deploy the backend?
        </slack_message>
        
        <list_git_tags>
            intent: "list_git_tags"
        </list_git_tags>
        
        <list_git_tags_result>
            tags:
              - name: "v1.2.3"
                commit: "abc123"
                date: "2024-03-15T10:00:00Z"
              - name: "v1.2.2"
                commit: "def456"
                date: "2024-03-14T15:30:00Z"
              - name: "v1.2.1"
                commit: "ghi789"
                date: "2024-03-13T09:15:00Z"
        </list_git_tags_result>
        
        what's the next step?
    }
]
The model may infer that you're asking it what's the next step by the tool schemas you supply, but it never hurts to roll it into your prompt template.

code example
We can build this with something like:

class Thread:
  events: List[Event]

class Event:
  # could just use string, or could be explicit - up to you
  type: Literal["list_git_tags", "deploy_backend", "deploy_frontend", "request_more_information", "done_for_now", "list_git_tags_result", "deploy_backend_result", "deploy_frontend_result", "request_more_information_result", "done_for_now_result", "error"]
  data: ListGitTags | DeployBackend | DeployFrontend | RequestMoreInformation |  
        ListGitTagsResult | DeployBackendResult | DeployFrontendResult | RequestMoreInformationResult | string

def event_to_prompt(event: Event) -> str:
    data = event.data if isinstance(event.data, str) \
           else stringifyToYaml(event.data)

    return f"<{event.type}>\n{data}\n</{event.type}>"


def thread_to_prompt(thread: Thread) -> str:
  return '\n\n'.join(event_to_prompt(event) for event in thread.events)
Example Context Windows
Here's how context windows might look with this approach:

Initial Slack Request:

<slack_message>
    From: @alex
    Channel: #deployments
    Text: Can you deploy the latest backend to production?
</slack_message>
After Listing Git Tags:

<slack_message>
    From: @alex
    Channel: #deployments
    Text: Can you deploy the latest backend to production?
    Thread: []
</slack_message>

<list_git_tags>
    intent: "list_git_tags"
</list_git_tags>

<list_git_tags_result>
    tags:
      - name: "v1.2.3"
        commit: "abc123"
        date: "2024-03-15T10:00:00Z"
      - name: "v1.2.2"
        commit: "def456"
        date: "2024-03-14T15:30:00Z"
      - name: "v1.2.1"
        commit: "ghi789"
        date: "2024-03-13T09:15:00Z"
</list_git_tags_result>
After Error and Recovery:

<slack_message>
    From: @alex
    Channel: #deployments
    Text: Can you deploy the latest backend to production?
    Thread: []
</slack_message>

<deploy_backend>
    intent: "deploy_backend"
    tag: "v1.2.3"
    environment: "production"
</deploy_backend>

<error>
    error running deploy_backend: Failed to connect to deployment service
</error>

<request_more_information>
    intent: "request_more_information_from_human"
    question: "I had trouble connecting to the deployment service, can you provide more details and/or check on the status of the service?"
</request_more_information>

<human_response>
    data:
      response: "I'm not sure what's going on, can you check on the status of the latest workflow?"
</human_response>
From here your next step might be:

nextStep = await determine_next_step(thread_to_prompt(thread))
{
  "intent": "get_workflow_status",
  "workflow_name": "tag_push_prod.yaml",
}
The XML-style format is just one example - the point is you can build your own format that makes sense for your application. You'll get better quality if you have the flexibility to experiment with different context structures and what you store vs. what you pass to the LLM.

Key benefits of owning your context window:

Information Density: Structure information in ways that maximize the LLM's understanding
Error Handling: Include error information in a format that helps the LLM recover. Consider hiding errors and failed calls from context window once they are resolved.
Safety: Control what information gets passed to the LLM, filtering out sensitive data
Flexibility: Adapt the format as you learn what works best for your use case
Token Efficiency: Optimize context format for token efficiency and LLM understanding
Context includes: prompts, instructions, RAG documents, history, tool calls, memory

Remember: The context window is your primary interface with the LLM. Taking control of how you structure and present information can dramatically improve your agent's performance.

Example - information density - same message, fewer tokens:

Loom Screenshot 2025-04-22 at 09 00 56

Recurring theme here: I don't know what's the best approach, but I know you want the flexibility to be able to try EVERYTHING.


- [context engineering by Simon Willison](https://simonwillison.net/2025/Jun/27/context-engineering/) 

Simon Willison’s Weblog
Subscribe
The term context engineering has recently started to gain traction as a better alternative to prompt engineering. I like it. I think this one may have sticking power.

Here's an example tweet from Shopify CEO Tobi Lutke:

I really like the term “context engineering” over prompt engineering.

It describes the core skill better: the art of providing all the context for the task to be plausibly solvable by the LLM.

Recently amplified by Andrej Karpathy:

+1 for "context engineering" over "prompt engineering".

People associate prompts with short task descriptions you'd give an LLM in your day-to-day use. When in every industrial-strength LLM app, context engineering is the delicate art and science of filling the context window with just the right information for the next step. Science because doing this right involves task descriptions and explanations, few shot examples, RAG, related (possibly multimodal) data, tools, state and history, compacting [...] Doing this well is highly non-trivial. And art because of the guiding intuition around LLM psychology of people spirits. [...]

I've spoken favorably of prompt engineering in the past - I hoped that term could capture the inherent complexity of constructing reliable prompts. Unfortunately, most people's inferred definition is that it's a laughably pretentious term for typing things into a chatbot!

It turns out that inferred definitions are the ones that stick. I think the inferred definition of "context engineering" is likely to be much closer to the intended meaning.

Posted 27th June 2025 at 11:42 pm
---
- [Context Engineering for Agents](https://rlancemartin.github.io/2025/06/23/context_engineering/)

Context Engineering for Agents
Jun 23, 2025

Lance Martin

Context Engineering
As Andrej Karpathy puts it, LLMs are like a new kind of operating system. The LLM is like the CPU and its context window is like RAM, representing a “working memory” for the model.

Context enters an LLM in several ways, including prompts (e.g., user instructions), retrieval (e.g., documents), and tool calls (e.g., APIs).

Just like RAM, the LLM context window has limited “communication bandwidth” to handle these various sources of context.

And just as an operating system curates what fits into a CPU’s RAM, we can think about “context engineering” the art and science of filling the context window with the information needed to perform a task.


The Rise of Context Engineering
Context engineering is an umbrella discipline that captures a few different focus areas:

Instructions – prompts (see: prompt engineering), memories, few‑shot examples
Knowledge – retrieval or memories to extend the model’s world‑knowledge (see: RAG)
Tool feedback – context flowing in from the environment via tools
As LLMs get better at tool calling, agents are now feasible. Agents interleave LLM and tool calls for long-running tasks, and motivate the need for engineering across all three types of context.


Cognition called out the importance of context engineering when building agents:

“Context engineering” … is effectively the #1 job of engineers building AI agents.

Anthropic also laid it out clearly:

Agents often engage in conversations spanning hundreds of turns, requiring careful context management strategies.

This post is aims to break down some common strategies — compress, persist, and isolate — for agent context engineering.

Context Engineering for Agents
The agent context is populated with feedback from tool calls, which can exceed the size of the context window and balloon the cost / latency.


I’ve been bitten by this many times. One incarnation of a deep research agent that I built used token-heavy search API tool calls, resulting in > 500k token and several dollars per run!

Long context may also degrade agent performance. Google and Percy Liang’s group have described different types of “context degradation syndrome” since a long context can limit an LLMs ability to recall facts or follow instructions.

There are many ways to combat this problem, which I group into 3 buckets and describe below: compressing, persisting, and isolating context.


Compressing Context
Compressing context involves keeping only the highest-value tokens at each turn.

Context Summarization

Agent interactions can span hundreds of turns and may have token-heavy tool calls. Context summarization is one common way to manage this.

If you’ve used Claude Code, you’ve seen this in action. Claude Code runs “auto-compact” after you exceed 95% of the context window.

Summarization can be used in different places, such as the full agent trajectory with methods such as recursive or hierarchical summarization.


It’s also common to summarize tool call feedback (e.g., a token-heavy search tool) or specific steps (e.g., Anthropic’s multi-agent researcher applies summarization on completed work phases).

Cognition called out that summarization can be tricky if specific events or decisions from agent trajectories are needed. They use a fine-tuned model for this in Devin, which underscores how much work can go into refining this step.

Persisting Context
Persisting context involves systems to store, save, and retrieve context over time.

Storing context

Files are a simple way to store context. Many popular agents use this: Claude Code uses CLAUDE.md. Cursor and Windsurf use rules files, and some plugins (e.g., Cursor Memory Bank) / MCP servers manage collections of memory files.

Some agents need to store information that can’t be easily be captured in a few files. For example, we may want to store large collections of facts and / or relationships. A few tools emerged to support this and showcase some common patterns.

Letta, Mem0, and LangGraph / Mem store embedded documents. Zep and Neo4J use knowledge graphs for continuous / temporal indexing of facts or relationships.

Saving context

Claude Code entrusts the user to create / update memories (e.g., the # shortcut). But there are many cases where we want agents to autonomously create / update memories.

The Reflexion paper introduced the idea of reflection following each agent turn and re-using these self-generated hints. Generative Agents created memories as summaries synthesized from collections of past feedback.

These concepts made their way into popular products like ChatGPT, Cursor, and Windsurf, which all have mechanisms to auto-generate memories based on user-agent interactions.


Memory creation can also be done at specific points in an agent’s trajectory. One pattern I like: update memories based upon user feedback.

For example, human-in-the-loop review of tool calls is a good way to build confidence in your agent. But if you pair this with memory updating, then the agent can learn from your feedback over time. My email assistant does this with file based memory.

Retrieving context

The simplest approach is just to pull all memories into the agent’s context window. For example, Claude Code just reads all CLAUDE.md files into context at the start of each session. In my email assistant, I always load a set memories that provide email triage and response instructions into context.

But, mechanisms to fetch select memories are important if the collection is large. The store will help determine the approach (e.g., embedding-based search or graph retrieval).

In practice this is a deep topic. Retrieval can be tricky. For example, Generative Agents scored memories on similarity, recency, and importance. Simon Willison shared an example of memory retrieval gone wrong. GPT-4o injected location into an image based upon his memories, which was not desired. Poor memory retrieval can make users feel like the context window “doesn’t belong to them”!

Isolating Context
Isolating context involves approaches to partition it across agents or environments.

Context Schema

Oftentimes, messages are used to structure agent context. Tool feedback is appended to a message list. The full list is then passed to the LLM at each agent turn.

The problem is that a list can get bloated with token-heavy tool calls. A structured runtime state - defined via a schema (e.g., a Pydantic model) - can often be more effective.

Then, you can better control what the LLM sees at each agent turn. For example, in one version of a deep research agent, my schema both messages and sections. messages is passed to the LLM at each turn, but I isolate token-heavy sections in sections and fetch them selectively.

Multi-agent

One popular approach is to split context across sub-agents. A motivation for the OpenAI Swarm library was “separation of concerns”, where a team of agents can handle sub-tasks and each agent has its own instructions and context window.


Anthropic’s multi-agent researcher makes a clear case for this: multi-agent with isolated context outperformed single-agent by 90.2%, largely due to token usage. As the blog said:

[Subagents operate] in parallel with their own context windows, exploring different aspects of the question simultaneously.

The problems with multi-agent include token use (e.g., 15× more tokens than chat), the need for careful prompting and context for sub-agent planning, and sub-agent coordination. Cognition argues against multi-agent for these reasons.

I’ve also been bitten by this: one iteration of my deep research agent had a team of agents write sections of the report. Sometimes the final report was disjointed because the agents did not communicate with one another while writing.

One way to reconcile this is to ensure the task is parallelizable. A subtle point is that Anthropic’s deep research multi-agent system applied parallelization to research. This is easier than writing, which requires tight cohesion across the sections of a report to achieve strong overall flow.

Context Isolation with Environments

HuggingFace’s deep researcher is another good example of context isolation. Most agents use tool calling APIs, which return JSON objects (arguments) that can be passed to tools (e.g., a search API) to get tool feedback (e.g., search results).


HuggingFace uses a CodeAgent, which outputs code to execute tools. The code runs in a sandbox and select tool feedback from code execution is passed back to the LLM.

[Code Agents allow for] a better handling of state … Need to store this image / audio / other for later use? No problem, just assign it as a variable in your state and you [use it later].

The sandbox stores objects generated during execution (e.g., images), isolating them from the LLM context window, but the agent can still reference these objects with variables later.

Lessons
General principles for building agents are still in their infancy. Models are changing quickly and the Bitter Lesson warns us to avoid context engineering that will become irrelevant as LLMs improve.

For example, continual learning may let LLMs to learn from feedback, limiting some of the need for external memory. With this and the patterns above in mind, here are some general lessons ordered roughly by the amount of effort required to use them.

Instrument first: Always look at your data. Ensure you have a way to track tokens when building agents. This has allowed me to catch various cases of excessive token-usage and isolate token-heavy tool calls. It sets the stage for any context engineering efforts.
Think about your agent state: Anthropic called out the idea of “thinking like your agent.” One way to do this is to think through the information your agent needs to collect and use at runtime. A well defined state schema is an easy way to better control what is exposed to the LLM during the agent’s trajectory. I use this with nearly every agent I build, rather than just saving all context to a message list. [Anthropic] also called this out in their researcher where they save the research plan for future use.
Compress at tool boundaries: Tools boundaries are a natural place to add compression, if needed. The output of token-heavy tool calls can be summarized, for example, using a small LLM with straightforward prompting. This lets you quickly limit runaway context growth at the source without the need for compression over the full agent trajectory.
Start simple with memory: Memory can be a powerful way to personalize an agent. But, it can be challenging to get right. I often use simple, file-based memory that tracks a narrow set of agent preferences that I want to save and improve over time. I load these preferences into context every time my agent runs. Based upon human-in-the-loop feedback, I use an LLM to update these preferences (see here). This is a simple but effective way to use memory, but obviously the complexity of memory can be increased significantly if needed.
Consider multi-agent for easily parallelizable tasks: Agent-agent communication is still early, and it’s hard to coordinate multi-agent teams. But that doesn’t mean you should abandon the idea of multi-agent. Instead, consider multi-agent in cases where the problem can be easily parallelized and tight coordination between sub-agents is not strictly required, as shown in the case of Anthropic’s multi-agent researcher.


