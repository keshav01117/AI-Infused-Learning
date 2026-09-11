# AI-Infused-Learning

## Class 1: Short Revision Notes

### What we learned

- Use the `openai` Python package to call an LLM from Python.
- Keep API keys in `.env`; never hardcode or commit them.
- Use `python-dotenv` to load environment variables at runtime.
- Groq provides an OpenAI-compatible API. Change `base_url`, API key, and model to use it.
- Use `requests` and `BeautifulSoup` to fetch and clean website content.
- Send the cleaned content to an LLM with a clear system prompt to generate a summary.
- Use Gradio to turn a Python function into a simple shareable web app.

### Core API pattern

```python
from openai import OpenAI

client = OpenAI(api_key="...", base_url="https://api.groq.com/openai/v1")

response = client.chat.completions.create(
	model="your-model",
	messages=[
		{"role": "system", "content": "You are a helpful assistant."},
		{"role": "user", "content": "Your question"},
	],
)
print(response.choices[0].message.content)
```

### Class 1 flow

`fetch website -> clean HTML -> summarize content -> display with Gradio`

### Setup and run

```bash
pip install python-dotenv openai requests beautifulsoup4 gradio
python "class 1/first_class.py"
```

Add the required provider key to `.env`, for example `GROQ_API_KEY=your-key`.

## Class 2: LangChain and Agents

### What we learned

- LangChain separates prompts, models, and output parsers into reusable steps.
- The `|` operator composes those steps into a runnable chain.
- Conversation memory sends previous `HumanMessage` and `AIMessage` objects with each request.
- An agent lets an LLM decide when to call a Python function, then uses the tool result to answer.
- Function tools need a name, description, parameter schema, and a result linked by `tool_call_id`.
- A shared provider factory keeps API keys, model names, and API endpoints in one place.
- The same OpenAI-compatible client can use OpenAI or Groq by changing the key, endpoint, and model.
- Gradio turns the agent function into a browser-based chat interface.
- Website summarization combines the Class 1 scraper with a LangChain prompt/model/parser chain.

### Class 2 flow

`prompt -> model -> parser`  |  `agent -> tool call -> tool result -> final answer`

### Setup and run

```bash
pip install -r "Class2/requirements.txt"
python "Class2/summarizer_langchain.py"
python "Class2/agent.py"
```

Class 2 prefers `OPENAI_API_KEY` in `Class2/.env` and falls back to
`GROQ_API_KEY` in `class 1/.env`. Never commit `.env` files.


# AI-Infused-Learning

## Class 3: RAG — Talk to Your Own Documents

### What we learned

* RAG stands for **Retrieval-Augmented Generation**.
* RAG allows an LLM to answer questions using your own documents/data without retraining or fine-tuning the model.
* RAG helps solve **knowledge cutoff, private data, hallucinations, and missing citations**.
* The basic RAG pipeline is: **Question -> Search -> Stuff -> LLM -> Answer**.
* RAG has two phases: **Indexing (offline)** and **Querying (online)**.
* Embeddings convert text into vectors that represent semantic meaning.
* Similar meanings produce vectors that are close together in vector space.
* Chunking splits large documents into smaller pieces before creating embeddings.
* Vector databases store embeddings and perform semantic similarity search.
* Reranking improves retrieval by using a fast first-stage search followed by a more accurate second-stage ranking.
* Hybrid search combines **BM25 keyword search** with **vector semantic search**.
* A practical RAG system can be built using **LangChain, HuggingFace embeddings, Chroma, OpenAI, and Gradio**.
* Metadata such as page numbers can be used to provide citations in answers.
* The Class 3 project is **Chat with your PDF**.

### Why does RAG exist?

RAG mainly solves four problems:

* **Knowledge cutoff** -> retrieve fresh information from external documents.
* **Private / internal data** -> search company documents, PDFs, wikis, policies, etc.
* **Hallucinations** -> ground the answer in retrieved text.
* **No citations** -> return the source/page used to generate the answer.

### The 1-line definition

**RAG = Retrieval-Augmented Generation.**

Before the model answers, retrieve the most relevant snippets from your own data and add them to the prompt. The LLM then generates the answer using those snippets.

**No retraining. No fine-tuning.**

RAG is essentially an **open-book exam** for an LLM instead of a closed-book exam.

### RAG in one simple picture

RAG works like a **smart librarian** between the user and the LLM.

Imagine a question about an 800-page book. Instead of asking someone to guess the answer, first find the most relevant pages, give those pages to the person, and then ask them to answer.

### The 5-box pipeline

`Question -> Search -> Stuff -> LLM -> Answer + source citation`

* **Question** -> user asks a question.
* **Search** -> find relevant chunks.
* **Stuff** -> add retrieved chunks to the prompt.
* **LLM** -> generate an answer using the provided context.
* **Answer** -> return the answer along with the source citation.

### Two phases · don't confuse them

**Phase 1 — Indexing (offline, once)**

`Documents -> Chunks -> Embeddings -> Vector DB`

* Read the documents.
* Split them into chunks.
* Convert each chunk into an embedding/vector.
* Store the chunks and vectors in a vector database.
* Repeat when documents change.

**Phase 2 — Querying (online, every question)**

`Question -> Query Embedding -> Similarity Search -> Relevant Chunks -> Prompt -> LLM -> Answer`

The important point is that **RAG does not retrain the model**. It changes what information is provided in the prompt.

### Embeddings: words become coordinates

An **embedding** is a list of numbers, called a **vector**, that represents the meaning of a piece of text.

`Similar meaning -> similar vectors -> nearby points`

`Different meaning -> different vectors -> points farther apart`

Real embeddings can have dimensions such as **384, 768, or 3072**.

### The aha: embedding math actually works

A famous example is:

`king - man + woman ≈ queen`

Embeddings can capture relationships between words through their position and direction in vector space.

The key idea for RAG is:

**Search by meaning = find the nearest point in vector space.**

### The score we use: cosine similarity

Cosine similarity measures how similar two vectors are based on the angle between them.

* Range: **-1 to +1**
* Larger value -> more similar
* Smaller value -> less similar

Simple interview line:

> **Cosine similarity tells us how close two embeddings are in terms of meaning.**

### How do we actually get an embedding? One function call.

Example using `sentence-transformers`:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

vec = model.encode("A cat is sleeping on the couch")

print(vec.shape)
```

`all-MiniLM-L6-v2` produces a **384-dimensional embedding**.

To compare two texts:

```python
from numpy import dot
from numpy.linalg import norm

v1 = model.encode("A cat is sleeping on the couch")
v2 = model.encode("A kitten is napping on the sofa")

similarity = dot(v1, v2) / (norm(v1) * norm(v2))

print(similarity)
```

### Vectors = coordinates

Every chunk of text gets represented as a point/vector in a high-dimensional space.

### Cosine similarity

`-1 -> opposite`

`0 -> unrelated`

`+1 -> very similar`

Remember:

**Bigger similarity score = more similar meaning.**

### One function call

`.encode(text)` -> converts text into an embedding vector.

### Chunking: cut the book into snippets

Before generating embeddings, large documents need to be divided into smaller pieces called **chunks**.

A 200-page PDF should not normally be represented by one vector because important meaning can get averaged together.

Chunking directly affects RAG quality.

### The 4 chunking strategies worth knowing

**Fixed size**

Split every N characters or tokens.

* Simple and fast.
* Good for prototypes.
* Can split in the middle of sentences or words.

**Recursive**

Try to split using a hierarchy such as:

`paragraph -> sentence -> word`

* Preserves boundaries better.
* Default approach in LangChain.
* Good for most real applications.

**Semantic**

Group sentences that discuss the same topic.

* Chunks follow meaning rather than fixed size.
* Useful for long flowing prose.

**Structure-aware**

Use the document's existing structure:

* Markdown headings
* Code blocks
* HTML sections
* Document sections

Useful for documentation, code, and wikis.

### the recall vs precision tradeoff · keep this in mind

**Big chunks**

`High recall + Low precision`

The answer is more likely to be present, but there may be lots of irrelevant information.

**Small chunks**

`High precision + Low recall`

The retrieved chunk can be very focused, but relevant information may be split across multiple chunks.

### One line of real code

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

chunks = splitter.split_text(your_long_document)
```

### Why `chunk_overlap`?

Suppose the answer is located exactly at the boundary between two chunks.

Without overlap, the relevant information may be split.

With overlap:

`Chunk 1: A B C D E`

`Chunk 2: D E F G H`

The overlapping section provides **context glue** and reduces boundary loss.

### Vector databases: a search engine for meaning

A **vector database** stores embeddings and allows us to find the vectors closest to a query vector.

Instead of:

`Find documents containing this word`

we ask:

`Find documents whose meaning is closest to this query`

### The three names you'll hear all the time

**Chroma**

* Open-source.
* Easy to run.
* Good for prototypes.
* Used in the Class 3 project.

**Pinecone**

* Fully managed SaaS.
* Designed for large-scale production workloads.
* Minimal infrastructure management.

**Qdrant**

* Open-source.
* Production-grade.
* Can be self-hosted or used through cloud.

### Picking one (don't overthink)

* Prototyping -> **Chroma**
* Managed production service -> **Pinecone**
* Self-hosted production -> **Qdrant / Weaviate**

### What it actually does — three operations

A vector DB essentially performs:

**1. Add**

```text
db.add(documents, embeddings)
```

Store chunks and their vectors.

**2. Query**

```text
db.query(query_vector, k=3)
```

Retrieve the nearest chunks.

**3. Delete**

```text
db.delete(ids)
```

Remove chunks when documents are deleted.

### HNSW — the trick behind every vector DB

**HNSW = Hierarchical Navigable Small World**

It is an approximate nearest-neighbor search technique used by vector databases to search large numbers of vectors efficiently.

You normally don't implement HNSW yourself. Vector databases provide it internally.

### Build a real RAG in 30 lines

The basic pattern is:

`Load -> Chunk -> Embed -> Store -> Retrieve -> Answer`

### Step 1 — Index your documents (once)

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

docs = [
    "Our return policy allows refunds within 30 days of purchase.",
    "Shipping is free for orders above ₹999 across India.",
    "For corporate orders above 50 units, contact sales@example.com.",
    "Our office is in Indiranagar, Bangalore. Open Mon-Fri 10am-7pm.",
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.create_documents(docs)

embedder = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    chunks,
    embedder,
    persist_directory="./chroma_db"
)

print(f"Indexed {len(chunks)} chunks")
```

### Step 2 — Ask a question (every time)

```python
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

embedder = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedder
)

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
Answer the question using ONLY the context below.
If the context doesn't contain the answer, say "I don't know."

Context:
{context}

Question: {question}
""")

def rag_answer(question):
    chunks = db.similarity_search(question, k=3)

    context = "\n\n".join(
        c.page_content for c in chunks
    )

    chain = prompt | model

    return chain.invoke({
        "context": context,
        "question": question
    }).content
```

### the 8 numbered steps

**① Your data**

PDFs, web pages, Notion exports, documents, etc.

**② Chunk it**

Split the documents into smaller pieces.

**③ Pick an embedder**

Convert each chunk into a vector.

**④ Build the vector store**

Store chunks and embeddings in Chroma/vector DB.

**⑤ Reopen the database**

Reuse previously generated embeddings instead of generating them again.

**⑥ Build the prompt**

Give the LLM the retrieved context and instruct it to answer from that context.

**⑦ Retrieve**

`similarity_search(question, k=3)`

Find the top 3 relevant chunks.

**⑧ Generate**

`prompt | model`

Send the context and question to the LLM.

### Take a moment — this is the canonical pattern

The core RAG pattern is:

`Documents -> Chunk -> Embed -> Store -> Retrieve -> Prompt -> LLM -> Answer`

Everything else is an improvement around retrieval, ranking, prompting, and evaluation.

### Make it better: rerank + hybrid search

A basic RAG system works, but retrieval can be improved using:

* **Reranking**
* **Hybrid search**

### Problem 1: the top-5 from vector search isn't the best 5

Vector similarity is fast, but the first retrieved results are not always the most relevant.

A common solution is **two-stage retrieval**.

`Fast retrieval -> candidates -> accurate reranking -> final results`

### Bi-encoder like a resume scan

A bi-encoder processes the query and document separately.

```text
Query -> Vector
Document -> Vector
```

Then the vectors are compared using similarity.

Advantages:

* Fast.
* Can pre-compute document embeddings.
* Suitable for retrieving many candidates.

Use it to retrieve approximately **top 50–100 candidates**.

### Cross-encoder like a 30-min interview

A cross-encoder receives the query and document together.

```text
(Query + Document) -> Transformer -> Relevance Score
```

Advantages:

* More accurate.
* Understands query-document interactions better.

Disadvantage:

* Slower because every query-document pair must be processed.

Use it to rerank the initial candidates and keep the **top 3–5**.

### remember this — the two-stage pattern is universal

**Stage 1 — Bi-encoder**

`Vector DB -> Top 50–100 candidates`

Fast retrieval.

**Stage 2 — Cross-encoder**

`Candidates -> Rerank -> Top 3–5`

More accurate but slower.

### Problem 2: sometimes you need the exact word

Semantic search is not always good at exact identifiers.

Examples:

* SKU
* Product code
* Version number
* Date
* Legal reference
* Technical jargon

For these cases, **keyword search** can outperform semantic search.

### Two librarians, very different superpowers

There are two complementary retrieval approaches:

**BM25 -> exact words**

**Vector search -> semantic meaning**

Using both gives **hybrid search**.

### Librarian A · BM25 the literalist

BM25 is good at exact keyword matching.

Good for:

* Product codes
* SKUs
* Model numbers
* Version strings
* Proper nouns
* Dates
* Legal references
* Technical jargon

Weak at:

* Synonyms
* Paraphrases
* Intent

### Librarian B · Vector the philosopher

Vector search focuses on semantic meaning.

Good for:

* Natural-language questions
* Fuzzy queries
* Paraphrases
* Similar meanings
* Multilingual matching

Weak at:

* Exact codes
* IDs
* Technical strings

### Hybrid = both librarians on the case

Run both BM25 and vector search.

Then merge their rankings.

The technique used in the class is:

**Reciprocal Rank Fusion (RRF)**

### Reciprocal Rank Fusion in one line

```text
Final Score =
1 / (60 + BM25 rank)
+
1 / (60 + Vector rank)
```

Documents ranked highly by both retrieval methods get a stronger combined ranking.

### Why this works so well in practice

Real-world queries often contain both:

* Natural language
* Exact technical terms

Hybrid search covers both.

```text
Natural language -> Vector Search
Exact keywords -> BM25
Both results -> RRF -> Final ranking
```

### Mini-Project: Chat with your PDF

The project builds a chatbot that can:

* Accept a PDF.
* Read the PDF.
* Split it into chunks.
* Generate embeddings.
* Store them in Chroma.
* Retrieve relevant chunks.
* Ask an LLM to answer.
* Return page citations.
* Provide a Gradio chat interface.

### The full app — 4 files

`PDF -> Chunk -> Embed + Store -> Retrieve -> Chat`

### Step 1 — Load the PDF & index it once

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def build_index(pdf_path):
    pages = PyPDFLoader(pdf_path).load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(pages)

    embedder = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = Chroma.from_documents(
        chunks,
        embedder
    )

    return db
```

### Step 2 — Answer with retrieval + citations

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
You are a helpful PDF assistant.
Answer the question using ONLY the context below.

If the context doesn't contain the answer,
say "I couldn't find that in the document."

After your answer, list the page numbers used as:
Sources: page X, page Y.

Context:
{context}

Question: {question}
""")

def ask(db, question):
    chunks = db.similarity_search(question, k=4)

    context = "\n\n".join(
        f"[page {c.metadata['page']+1}] {c.page_content}"
        for c in chunks
    )

    chain = prompt | model

    return chain.invoke({
        "context": context,
        "question": question
    }).content
```

### Step 3 — Give it a face with Gradio

```python
import gradio as gr

state = {"db": None}

def upload(pdf):
    state["db"] = build_index(pdf.name)
    return "PDF indexed! Ask me anything about it."

def chat(message, history):
    if state["db"] is None:
        return "Please upload a PDF first."

    return ask(state["db"], message)

with gr.Blocks(title="Chat with your PDF") as demo:
    gr.Markdown("## Chat with your PDF (powered by RAG)")

    pdf = gr.File(
        label="Upload a PDF",
        file_types=[".pdf"]
    )

    status = gr.Markdown()

    pdf.upload(
        upload,
        inputs=pdf,
        outputs=status
    )

    gr.ChatInterface(fn=chat)

demo.launch(share=True)
```

### the 3 small choices that matter

**① State**

```python
state = {"db": None}
```

The vector database is kept across Gradio events.

Without this, the PDF could be indexed again for every chat message.

**② Re-indexing**

The PDF is indexed when a new PDF is uploaded.

Chat messages then reuse the existing index.

**③ Metadata**

Page metadata is passed into the prompt.

This allows the LLM to provide page citations.

### Run it

```bash
python pdf_chat.py
```

Gradio starts a local application and can optionally provide a public share link using:

```python
demo.launch(share=True)
```

### Upload any PDF

Examples:

* Resume
* Research paper
* Company HR policy
* Earnings report
* College notes
* Textbook

### Ask 3 questions

Try:

* A factual question.
* A summary question.
* A comparison/tricky question.

Then check the citations.

### Try a question that's NOT in the doc

The system should respond with something like:

`I couldn't find that in the document.`

This is important because the system should **refuse to hallucinate when the required information is not available in the retrieved context**.

### Ship it to LinkedIn — today

Class 3 also focuses on shipping the project publicly.

### The 3-step ship checklist

**Record a 20-second clip**

Show:

`Upload PDF -> Ask question -> Show answer + citation`

Also demonstrate a question that is not present in the document.

**Use the caption template**

Mention:

* What you built.
* Which PDF you tested.
* RAG architecture.
* Retrieval and embeddings.
* Page citations.

**Post + reply**

Share the project and engage with comments.

### Want a variation? Pick a flavour, swap the PDF

Possible projects:

**Chat with the Constitution**

Upload the Indian Constitution and ask questions with citations.

**Chat with an earnings call**

Upload a quarterly earnings transcript and ask about:

* Revenue
* Margins
* Guidance
* Hiring

**Chat with your textbook**

Upload a chapter and ask exam-style questions.

**Chat with company HR policy**

Upload HR policy documents and ask questions about policies.

### Where this is going

The next step is to make RAG smarter.

### Agentic RAG — when retrieval becomes a decision

Normal RAG retrieves information for every query.

**Agentic RAG** combines the agent loop from Class 2 with the retrieval system from Class 3.

The agent can decide:

* Do I need retrieval?
* Is the retrieved information sufficient?
* Should I rewrite the query?
* Should I search again?
* Should I ask the user for clarification?

### The loop you'll meet next class

`Query -> Retrieve -> Grade chunks -> Rewrite query if needed -> Search again -> Clarify if needed -> Answer`

This combines:

`Class 2 Agent + Class 3 RAG`

### Advanced RAG — the tricks the senior engineers use

**HyDE**

**Hypothetical Document Embeddings**

The LLM generates a hypothetical answer/document first and uses it to improve retrieval.

**Step-back prompting**

Generalize the question before retrieval.

Example:

```text
Specific question
        ↓
General concept
        ↓
Better retrieval
```

**Graph RAG**

Build a knowledge graph containing:

* Entities
* Relationships

Useful for questions involving relationships between entities.

**RAG evaluation**

Measure the quality of the RAG system using:

* **Relevance**
* **Faithfulness**
* **Correctness**

### Where you are right now

The four important pieces learned across the first classes are:

`Model + Prompt + Tool + Retrieval`

Class 3 adds retrieval to the previous LLM and agent concepts.

### Embeddings

`Text -> Vectors`

Similar meaning = nearby vectors.

### Chunking

Split documents into useful pieces.

Chunking is one of the most important quality-tuning parameters in RAG.

### Vector DB

Three core operations:

`Add -> Query -> Delete`

### You shipped

A real:

**"Chat with your PDF"**

application using RAG.

### You shipped class 3 🎉

You now understand the core RAG architecture:

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector DB
    ↓
Retrieval
    ↓
Prompt + Context
    ↓
LLM
    ↓
Answer + Citations
```

### For next class

Index a PDF that is useful to you and prepare **3 questions** where the RAG system produced an interesting or unexpected result.

These examples can be used to understand **Agentic RAG** in the next class.
