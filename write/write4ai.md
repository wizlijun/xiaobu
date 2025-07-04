# Writing documentation for AI: best practices

Retrieval-Augmented Generation (RAG) systems like Kapa rely on your documentation to provide accurate, helpful information. When documentation serves both humans and machines well, it creates a self-reinforcing loop of content quality: clear documentation improves AI answers, and those answers help surface gaps that further improve the docs.

This guide provides best practices for creating documentation that works effectively for both human readers and AI/LLM consumption in RAG systems. Many best practices benefit both simultaneously, often in complementary ways.

## Why documentation quality matters

Documentation quality has always been important for helping users understand and use your product effectively. And it becomes even more important when AI systems use that same content to answer user questions. Poor documentation doesn't just frustrate human readers, it directly degrades the quality of AI responses, creating a compounding problem where bad content leads to bad answers.

Understanding how AI systems process and use your documentation reveals why content quality is non-negotiable for good AI performance.

## How AI systems process your documentation

Kapa works by finding relevant pieces of your content and using them to construct answers. The process involves three main components:

- **Retriever**: Searches through your knowledge sources to find content that matches the user's question
- **Vector database**: Stores your content in a searchable format that enables fast and accurate retrieval
- **Generator**: A Large Language Model (LLM) that uses the retrieved content to create helpful responses

Information flows through a specific process once you connect knowledge sources to Kapa:

1. **Ingestion**: Content is divided into chunks (smaller, focused sections) and stored in the vector database
2. **Query processing**: When users ask questions, the system converts their question into a searchable format
3. **Retrieval**: The system finds the most relevant chunks from your documentation
4. **Answer generation**: The LLM uses these chunks as context to generate a response

In the steps that an AI takes to consume your content, there are some writing and structural patterns worth highlighting that can negatively impact how well your content is understood:

- **AI systems work with chunks**: They process documentation as discrete, independent pieces rather than reading it as a continuous narrative
- **They rely on content matching**: They find information by comparing user questions with your content, not by following logical document structure
- **They lose implicit connections**: Relationships between sections may not be preserved unless explicitly stated
- **They cannot infer unstated information**: Unlike humans who can make reasonable assumptions, AI systems can only work with explicitly documented information

Documentation optimized for AI systems should ideally be explicit, self-contained, and contextually complete. The more a chunk can stand alone while maintaining clear relationships to related content, the better it can be understood by the AI. The more explicit and less ambiguous the information is, the better the retrieval accuracy is and the better equipped the AI becomes at answering questions confidently.

While AI does work remarkably well with unstructured content, it's also true that information written and structured for with retrieval in mind can greatly improve the quality of an "Ask AI" interface to your knowledge sources.

## Why chunking is necessary

Ideally, chunking would not be necessary, and the AI could continuously keep your entire knowledge base in context, all the time. Unfortunately, this is impractical. Not only due to token limits but also because LLMs perform significantly better when provided with optimized, focused contexts. A large or overly broad context increases the likelihood that the model overlooks or misinterprets critical information, resulting in reduced accuracy and less coherent outputs.

Dividing documents into smaller, semantically coherent chunks enables retrieval systems to present the most relevant content to the LLM. This targeted approach significantly improves model comprehension, retrieval precision, and overall response quality.

## Quick tips to optimize your content

Optimizing content for AI is similar in principle to optimizing content for accessibility and screen readers: the clearer, more structured, and more machine-readable your content is, the better it performs. Just as clear semantic structure helps accessibility tools parse content effectively, a clear structure significantly improves AI accuracy. This section outlines some actionable, practical improvements you can apply today to make your docs more machine-readable.

Prioritizing these adjustments sets a strong foundation for addressing more nuanced content challenges, as discussed in the section **Content design challenges for AI**.

### 1. Use standardized semantic HTML

For website sources, ensure correct and semantic use of HTML elements like headings (`<h1>`, `<h2>`), lists (`<ul>`, `<ol>`), and tables (`<table>`). Semantic HTML ensures clear document structure, improving how accurately content is chunked and retrieved.

**Example:**
```html
<h2>How to enable webhooks</h2>
<ol>
  <li>Log in to your CloudSync dashboard.</li>
  <li>Navigate to Settings &gt; Webhooks.</li>
  <li>Toggle webhooks to "Enabled".</li>
</ol>
```

More importantly, avoid incorrect use of elements. An incorrectly placed `<h2>` element, for example, can have dire consequences for how a machine parses your content.

### 2. Avoid PDFs, prefer HTML or Markdown

PDF documents often have complex visual layouts that make machine parsing difficult. Migrating content from PDFs to HTML or Markdown drastically improves text extraction and retrieval quality.

### 3. Create crawler-friendly content

Simplify page structures by reducing or eliminating custom UI elements, JavaScript-driven dynamic content, and complex animations. Clear, predictable HTML structure facilitates easier indexing and parsing.

Replace complex JavaScript widgets with plain-text alternatives or simple interactive elements.

### 4. Ensure semantic clarity

Use descriptive headings and meaningful URLs reflecting the content hierarchy. Semantic clarity helps the AI correctly infer content relationships, greatly enhancing retrieval accuracy.

**Example of a meaningful URL:**
- ✅ Good: `/docs/cloudsync/setup-webhooks`
- ❌ Poor: `/docs/page12345`

### 5. Provide text equivalents for visuals

Always include clear text descriptions for critical visual information such as diagrams, charts, and screenshots. This ensures crucial details remain accessible to machines and screen readers alike.

**Example:**
```markdown
![System architecture diagram](architecture.png)

**Figure 1:** Diagram illustrating the CloudSync integration workflow,
detailing authentication, data upload, and confirmation steps.
```

### 6. Keep layouts simple

Avoid layouts where meaning is derived heavily from visual positioning or formatting. Layout is lost during conversion, and any meaning it was designed to convey with it. Content structured simply with clear headings, lists, and paragraphs translates effectively into plain text.

## Content design challenges for AI

This section takes a closer look at common content design anti-patterns that can create challenges for AI systems. These challenges often arise from how information is organized, contextualized, or assumed rather than how it's formatted. Each example highlights a specific problem pattern, why it causes issues for AI, and how to rewrite or restructure your content to avoid it.

### Contextual dependencies

**The problem:** Documentation that scatters key details and definitions across multiple sections or paragraphs creates problems when content is divided into chunks. When critical information is separated from its context, individual chunks can become ambiguous or incomplete.

Understanding how chunking works in practice reveals why proximity matters. Kapa attempts to preserve document structure by keeping sections intact when possible, but practical constraints often force splits:

- Sections that are too long get divided at paragraph or sentence boundaries
- Sections that are too short get combined with neighboring content
- Chunk sizes must be balanced for optimal retrieval performance

Since chunk boundaries can't be perfectly predicted, the closer related information appears in your source content, the more likely it stays together after chunking. This proximity principle becomes critical for maintaining meaning.

Consider this (simplified) problematic example:

> Authentication tokens expire after 24 hours by default.
> 
> The system provides several configuration options for different environments.
> 
> When implementing the login flow, ensure you handle this appropriately.

When this content gets chunked, the middle sentence about configuration options might cause the chunking algorithm to separate the token expiration detail from the implementation guidance. The resulting chunk containing "When implementing the login flow, ensure you handle this appropriately" loses crucial context about what "this" refers to and the specific 24-hour timeframe.

**The remedy:** Keep related information together within close proximity. When introducing a concept that has important constraints or context, include those details in the same paragraph or immediately adjacent paragraphs.

> Authentication tokens expire after 24 hours by default. When implementing the
> login flow, ensure you handle token expiration by refreshing tokens before the
> 24-hour limit or implementing proper error handling for expired token
> responses.
> 
> The system provides several configuration options for different environments,
> including custom token expiration periods.

By keeping the constraint (24-hour expiration) close to its implementation guidance, they're much more likely to remain in the same chunk, regardless of where the boundaries fall.

Look for sections that become unclear when read in isolation, especially where section headings are generic and multi-step processes that reference context from earlier paragraphs.

### Semantic discoverability gaps

**The problem:** Kapa finds information based on semantic similarity between queries and content. If important terms or concepts aren't present in a chunk, that chunk won't be retrieved for relevant queries, even if it contains exactly the information needed.

```markdown
## Configure timeouts

Configure custom timeout settings and retry logic for improved reliability in
production environments. Access these options through the admin panel.
```

If a user asks "How do I configure CloudSync timeouts?", this chunk might not be retrieved because "CloudSync" doesn't appear in the text.

**The remedy:** Establish consistent terminology for your product's unique concepts and use them systematically. Include specific product or feature names when documenting functionality.

```markdown
## Configure CloudSync timeouts

Configure custom CloudSync timeout settings and retry logic for improved
reliability in production environments. Access these options through the
CloudSync admin panel.
```

Your product's unique terminology won't be well-represented in the model's training data. Explicit, consistent usage helps establish what content relates to which product features.

**A note of balance:** This doesn't mean you should repeat the product name in every sentence or heading. Kapa also uses document structure, URLs, and parent headings to infer context. The important thing is that for any given chunk, there's a clear and consistent signal that connects it to your product or feature. See **Hierarchical information architecture** for how structural metadata supports this.

### Implicit knowledge assumptions

**The problem:** Kapa operates on a simple principle: if information isn't explicitly documented, it doesn't exist in the system's knowledge base. Unlike human readers who can draw on external knowledge or make reasonable inferences, Kapa only works with the information provided.

When documentation assumes user knowledge, these become dangerous gaps. Well-designed RAG systems should choose uncertainty over inaccuracy, but this only works when documentation explicitly addresses the topics users ask about.

**The remedy:** Include prerequisite steps within procedural content rather than assuming prior setup. When referencing external tools or concepts, provide brief context or links to detailed explanations.

**Before:**
```markdown
## Setting up webhooks

Configure your endpoint URL in the dashboard and test the connection.
```

**After:**
```markdown
## Setting up CloudSync webhooks

Before configuring webhooks, ensure you have:

- A publicly accessible HTTPS endpoint
- Valid SSL certificate
- CloudSync API credentials

Configure your endpoint URL in the CloudSync dashboard under Settings >
Integrations, then use the "Test connection" button to verify setup.
```

Look for instructions that assume familiarity with tools or interfaces, or reference "standard" configurations without explanation.

### Visual information dependencies

**The problem:** Critical information embedded in images, diagrams, and videos create problems for the ingestion processes that parse your documentation. When key information appears only in visual elements, users may receive incomplete answers.

**Example:** Information that completely depends on a graphical element
```markdown
See the diagram below for the complete API workflow:
![Complex flowchart showing 8-step process](workflow.png)

Follow these steps to implement the integration.
```

Instructions that depend on visual elements become inaccessible to automated systems, making the instruction meaningless.

**The remedy:** Provide text-based alternatives that capture the essential information. Represent workflow diagrams as numbered step lists while keeping visual elements as supplements.

```markdown
## CloudSync API workflow

The CloudSync integration follows this workflow:

1. **Authentication**: Send API credentials to `/auth/token` endpoint
2. **Validation**: System validates credentials and returns access token
3. **Data preparation**: Format your data according to CloudSync schema
4. **Upload request**: POST data to `/sync/upload` with access token
5. **Processing**: CloudSync validates and processes the data
6. **Status check**: Poll `/sync/status/{job_id}` for processing updates
7. **Completion**: Receive confirmation when sync completes
8. **Error handling**: Handle any validation or processing errors

![API workflow diagram](workflow.png)
_Visual representation of the workflow steps above_
```

### Layout-dependent information

**The problem:** Information that depends on visual layout, positioning, or table structure often loses meaning when processed as text by machines. While humans can interpret visual relationships and grouped content, AI systems struggle to maintain these connections.

Complex or poorly structured comparison tables with merged headers and visual groupings become ambiguous when converted to plain text:

```
Pricing		
Basic Plan	Standard Plan	Enterprise Plan
5 users	25 users	Unlimited users
1GB storage	10GB storage	Unlimited storage
Email support	Phone support	24/7 dedicated support
API Limits		
100 requests/hour	1,000 requests/hour	No rate limit
Basic endpoints only	All endpoints	All endpoints + webhooks
```

**The remedy:** If a tabular representation is preferable, ensure that the headers and rows are semantically correct. However, tabular representation is not always appropriate or necessary. You may also consider alternatives that preserve relationships in text form. Use structured lists or repeated context that maintains the connections. For example:

```markdown
## CloudSync pricing plans

### Basic Plan

- 5 users
- 1GB storage
- Email support
- API limits: 100 requests/hour, basic endpoints only

### Standard Plan

- 25 users
- 10GB storage
- Phone support
- API limits: 1,000 requests/hour, all endpoints

### Enterprise Plan

- Unlimited users
- Unlimited storage
- 24/7 dedicated support
- API limits: No rate limit, all endpoints plus webhooks
```

Keep simple reference tables where each row is self-contained, but supplement or replace complex tables where relationships between cells convey important meaning.

## Content organization

The following techniques help create content that can be effectively retrieved, without sacrificing readability.

### Hierarchical information architecture

When your content gets ingested into Kapa, preprocessing steps extract metadata that helps preserve context and boost retrieval accuracy. One of the most valuable pieces of data extracted is the hierarchical position of each document or section.

This hierarchy includes multiple layers of context: URL paths, document titles, and headings. These elements work together to build contextual understanding for content chunks after they're separated from their original location.

Design your content hierarchy so that each section carries sufficient context to be understood independently, while maintaining clear relationships to parent and sibling content.

When planning content structure, consider how users would find any given section without search. Ensure each section includes enough context to be understood independently:

- **Product family**: Which product or service area
- **Product name**: Specific product or feature name
- **Version information**: When applicable
- **Component specificity**: Subfeatures or modules
- **Functional context**: What the user is trying to accomplish

This hierarchical clarity helps AI systems understand relationships between concepts and provides richer context when retrieving information for user queries.

### Self-contained sections

Documentation sections that depend on readers following a linear path or remembering details from previous sections become problematic when processed as independent chunks. Sections are retrieved based on relevance and document order is not preserved, so sections should ideally make sense when encountered in isolation.

Compare these two approaches to the same information:

**Context-dependent:**
```markdown
## Updating webhook URLs

Now change the endpoint to your new URL and save the configuration.
```

**Self-contained:**
```markdown
## Updating webhook URLs

To update webhook endpoints in CloudSync:

1. Navigate to Settings > Webhooks in your CloudSync dashboard
2. Select the webhook you want to modify
3. Change the endpoint URL to your new address, and click Save
```

The self-contained version works when retrieved as an isolated chunk because it includes the essential context: what system (CloudSync), where to find the setting (Settings > Webhooks), and complete steps. The context-dependent version assumes the reader knows what "endpoint" refers to and where they are in the interface.

Front-load essential context and include complete information within each section boundary. This doesn't mean repeating everything everywhere, but ensuring sections remain actionable when encountered independently.

Consider starting each section with brief context about its scope and prerequisites, using descriptive headings that indicate what the section accomplishes, and including essential background information without assuming prior reading. Look for sections that reference "as mentioned above," "now that you've," or "with everything configured" as signals that context needs to be made explicit.

### Error context with solutions

Troubleshooting documentation deserves special attention because users often search by copying exact error messages they encounter. When your documentation includes the specific error text alongside solutions, it creates direct matches between user queries and helpful content.

When documenting troubleshooting steps, quote exact error messages and describe observable symptoms alongside solutions.

**Generic troubleshooting:**
```markdown
## Connection problems

If the connection fails, check your network settings and firewall configuration.
```

**Specific troubleshooting:**
```markdown
## CloudSync connection problems

### Error: "Connection timeout after 30 seconds"

This error occurs when CloudSync cannot reach the…

### Error: "Authentication failed (401)"

This indicates invalid or expired credentials…
```

Including exact error text ensures users can find help when searching with the specific messages they're seeing. To identify which error messages to prioritize in your documentation, review the Common Questions analytics in the Kapa platform. This shows you the actual error messages and problems users are asking about most frequently.

## Conclusion

Creating documentation that serves both human readers and AI effectively centers on a fundamental principle: explicit, self-contained content that maintains clear relationships between concepts. Eliminating contextual dependencies, ensuring discoverability, filling knowledge gaps, and providing text alternatives for visual content help mitigate inherent limitations in how machines consume your docs.

Documentation that works for AI is, at its core, just great documentation: clear, structured, explicit, and user-focused. The better your docs serve your users, the better your AI serves them, too.

Review and analyze user conversations, particularly conversations with uncertain or downvoted answers. Start with immediate fixes to frequently asked questions, then gradually restructure scattered information into coherent, complete sections. The goal is documentation where every section stands alone while maintaining logical connections to related concepts.