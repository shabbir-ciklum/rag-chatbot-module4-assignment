# Architecture Components - Detailed Diagrams

This document breaks down the complete architecture into individual components for presentation purposes. Each diagram can be rendered separately in Mermaid.

---

## Component 1: Data Ingestion Pipeline

**Purpose**: Transform raw data (PDFs, Audio) into searchable vector embeddings

```mermaid
graph LR
    subgraph Sources["📥 Data Sources"]
        PDF[📄 PDF Documents<br/>data/pdfs/]
        Audio[🎵 Audio Files<br/>data/audio/]
    end

    subgraph Loaders["🔄 Data Loaders"]
        PDFLoader[PDF Loader<br/>PyMuPDF + pdfplumber]
        AudioLoader[Audio Loader<br/>Whisper base model]
    end

    subgraph Processing["⚙️ Processing"]
        Chunker[Semantic Chunker<br/>500 chars, 100 overlap]
        Embedder[Embeddings Generator<br/>all-MiniLM-L6-v2]
    end

    subgraph Storage["🗄️ Storage"]
        VectorDB[(ChromaDB<br/>Vector Store<br/>384-dim vectors)]
    end

    PDF -->|Extract text| PDFLoader
    Audio -->|Transcribe| AudioLoader

    PDFLoader -->|Raw text| Chunker
    AudioLoader -->|Transcript| Chunker

    Chunker -->|Text chunks| Embedder
    Embedder -->|Vector embeddings| VectorDB

    VectorDB -->|Metadata| Metadata[📋 Metadata<br/>source, page, timestamp]

    classDef source fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef loader fill:#9B59B6,stroke:#6C3483,stroke-width:2px,color:#fff
    classDef process fill:#F39C12,stroke:#B8730D,stroke-width:2px,color:#000
    classDef store fill:#27AE60,stroke:#1E8449,stroke-width:2px,color:#fff

    class PDF,Audio source
    class PDFLoader,AudioLoader loader
    class Chunker,Embedder process
    class VectorDB,Metadata store
```

**Key Technologies**:
- **PDF**: PyMuPDF (text extraction), pdfplumber (table extraction)
- **Audio**: OpenAI Whisper (speech-to-text)
- **Chunking**: LangChain SemanticChunker (overlap for context preservation)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2, 384 dimensions)
- **Storage**: ChromaDB (local SQLite-based vector database)

**Demo Points**:
1. Show input files in `data/pdfs/` and `data/audio/`
2. Run `--rebuild` flag to trigger ingestion
3. Show progress bars for each document
4. Check ChromaDB count: `vector_store.collection.count()`

---

## Component 2: RAG Inference Flow

**Purpose**: Retrieve relevant context and generate answers using LLM

```mermaid
graph TD
    Query[👤 User Query] -->|1. Receive| QueryProcessor[Query Processor]

    QueryProcessor -->|2. Embed query| EmbedQuery[Query Embedding<br/>all-MiniLM-L6-v2]

    EmbedQuery -->|3. Vector search| VectorDB[(ChromaDB<br/>Vector Store)]

    VectorDB -->|4. Top-K results| Retriever[Semantic Retriever<br/>k=5 documents]

    Retriever -->|5. Rerank| Reranker[Score & Filter<br/>Relevance threshold]

    Reranker -->|6. Assemble| ContextBuilder[Context Builder<br/>Docs + Metadata]

    ContextBuilder -->|7. Create prompt| PromptTemplate[Prompt Template<br/>System + Context + Query]

    PromptTemplate -->|8. Generate| LLM[LLM Provider<br/>Ollama/Groq/Gemini]

    LLM -->|9. Parse| ResponseParser[Response Parser<br/>Extract answer + citations]

    ResponseParser -->|10. Format| FinalResponse[✅ Final Response<br/>Answer + Sources]

    FinalResponse --> User[👤 User]

    classDef input fill:#5DADE2,stroke:#2874A6,stroke-width:2px,color:#fff
    classDef embed fill:#F39C12,stroke:#B8730D,stroke-width:2px,color:#000
    classDef retrieve fill:#27AE60,stroke:#1E8449,stroke-width:2px,color:#fff
    classDef llm fill:#E74C3C,stroke:#C0392B,stroke-width:2px,color:#fff
    classDef output fill:#9B59B6,stroke:#6C3483,stroke-width:2px,color:#fff

    class Query,User input
    class QueryProcessor,EmbedQuery embed
    class VectorDB,Retriever,Reranker,ContextBuilder retrieve
    class PromptTemplate,LLM llm
    class ResponseParser,FinalResponse output
```

**Key Features**:
- **Semantic Search**: Cosine similarity in 384-dim space
- **Top-K Retrieval**: Default k=5, configurable
- **Relevance Filtering**: Score threshold to remove low-quality matches
- **Source Citations**: Track document source + page number
- **Multi-Provider**: Same interface for Ollama, Groq, Gemini

**Demo Points**:
1. Ask test question
2. Show retrieved documents (top-3 with scores)
3. Show assembled context sent to LLM
4. Display answer with source citations
5. Compare providers (speed, quality)

---

## Component 3: Agent Orchestration & Reasoning

**Purpose**: Autonomous decision-making, tool selection, and self-reflection

```mermaid
graph TD
    UserQuery[👤 User Query] -->|Input| Agent[🤖 AI Agent<br/>Orchestrator]

    Agent -->|Step 1| Reasoner[💭 Reasoner]

    subgraph Reasoning["🧠 Reasoning Module"]
        Reasoner -->|Analyze| R1[Query Classification<br/>Factual/Analytical/Tool]
        Reasoner -->|Decide| R2[Tool Selection<br/>RAG/Code/Docs/Stats]
        Reasoner -->|Estimate| R3[Confidence Score<br/>0.0 - 1.0]
        Reasoner -->|Plan| R4[Execution Plan<br/>Sequence of actions]
    end

    R4 -->|Step 2| Executor[⚙️ Executor]

    subgraph Execution["🔧 Execution Layer"]
        Executor -->|If RAG| RAG[📚 RAG Retrieval]
        Executor -->|If Tool| Tools[🔨 Agent Tools]
        Executor -->|Always| LLM[🧠 LLM Generation]
    end

    RAG -->|Context| Aggregator[📦 Result Aggregator]
    Tools -->|Tool Output| Aggregator
    LLM -->|Response| Aggregator

    Aggregator -->|Step 3| Reflection[🔍 Self-Reflection]

    subgraph Reflection_Module["💡 Reflection & Quality Control"]
        Reflection -->|Check| Q1[Relevance Check]
        Reflection -->|Check| Q2[Completeness Check]
        Reflection -->|Check| Q3[Accuracy Check]
        Reflection -->|Score| Q4[Quality Score<br/>0-10]
    end

    Q4 -->|If score < 7| Reasoner
    Q4 -->|If score >= 7| FinalResponse[✅ Final Response]

    FinalResponse --> UserOutput[👤 User]

    classDef agent fill:#2E86C1,stroke:#1B4F72,stroke-width:3px,color:#fff
    classDef reasoning fill:#F39C12,stroke:#B8730D,stroke-width:2px,color:#000
    classDef execution fill:#27AE60,stroke:#1E8449,stroke-width:2px,color:#fff
    classDef reflection fill:#E74C3C,stroke:#C0392B,stroke-width:2px,color:#fff
    classDef output fill:#AF7AC5,stroke:#76448A,stroke-width:2px,color:#fff

    class Agent agent
    class Reasoner,R1,R2,R3,R4 reasoning
    class Executor,RAG,Tools,LLM,Aggregator execution
    class Reflection,Q1,Q2,Q3,Q4 reflection
    class FinalResponse,UserOutput output
```

**Key Capabilities**:
- **Query Classification**: Determines question type (factual, analytical, code-based)
- **Tool Selection**: Decides which tools to invoke based on query
- **Confidence Estimation**: Self-awareness of answer reliability
- **Self-Reflection**: Quality gate before response delivery
- **Iterative Refinement**: Re-tries if quality score < threshold

**Demo Points**:
1. Show agent classifying different query types
2. Display tool selection logic
3. Show confidence scores
4. Demonstrate self-reflection (quality check)
5. Show iteration when initial response is low-quality

---

## Component 4: Agent Tools System

**Purpose**: Specialized tools for code analysis, documentation, and content generation

```mermaid
graph TD
    Agent[🤖 AI Agent] -->|Invokes| ToolRegistry[🔧 Tool Registry]

    subgraph Tools["🛠️ Agent Tools"]
        T1[Code Analyzer<br/>AST parsing]
        T2[Architecture Analyzer<br/>Layer detection]
        T3[Stats Collector<br/>Metrics gathering]
        T4[Doc Generator<br/>Technical docs]
        T5[Post Creator<br/>LinkedIn posts]
    end

    ToolRegistry -->|Execute| T1
    ToolRegistry -->|Execute| T2
    ToolRegistry -->|Execute| T3
    ToolRegistry -->|Execute| T4
    ToolRegistry -->|Execute| T5

    subgraph CodeAnalyzer["📊 Code Analyzer"]
        T1 -->|Scan| Files1[Python files]
        Files1 -->|Parse AST| AST[Extract classes<br/>functions, imports]
        AST -->|Output| CodeReport[Code Report<br/>Structure + Metrics]
    end

    subgraph ArchAnalyzer["🏗️ Architecture Analyzer"]
        T2 -->|Scan| Dirs[Directory structure]
        Dirs -->|Detect| Layers[Identify layers<br/>data/agent/api]
        Layers -->|Output| ArchReport[Architecture Report<br/>Pattern + Layers]
    end

    subgraph StatsCollector["📈 Stats Collector"]
        T3 -->|Count| Files2[Total files]
        T3 -->|Count| Lines[Lines of code]
        T3 -->|Count| Tests[Test files]
        Files2 & Lines & Tests -->|Output| StatsReport[Statistics Report<br/>Project metrics]
    end

    subgraph DocGenerator["📝 Doc Generator"]
        T4 -->|Analyze| CodeReport
        T4 -->|Analyze| ArchReport
        CodeReport & ArchReport -->|Generate| Docs[Technical Docs<br/>Markdown]
    end

    subgraph PostCreator["✍️ Post Creator"]
        T5 -->|Analyze| AllReports[All Reports]
        AllReports -->|LLM Generation| Post[LinkedIn Post<br/>Professional summary]
    end

    CodeReport & ArchReport & StatsReport & Docs & Post -->|Return to| Agent

    classDef agent fill:#2E86C1,stroke:#1B4F72,stroke-width:2px,color:#fff
    classDef tools fill:#9B59B6,stroke:#6C3483,stroke-width:2px,color:#fff
    classDef output fill:#27AE60,stroke:#1E8449,stroke-width:2px,color:#fff

    class Agent,ToolRegistry agent
    class T1,T2,T3,T4,T5 tools
    class CodeReport,ArchReport,StatsReport,Docs,Post output
```

**Tool Details**:

| Tool | Implementation | Output |
|------|----------------|--------|
| **Code Analyzer** | Python `ast` module | Classes, functions, docstrings |
| **Arch Analyzer** | Directory pattern matching | Layers, architecture type |
| **Stats Collector** | File system traversal | File count, LOC, test coverage |
| **Doc Generator** | Template-based | Technical documentation |
| **Post Creator** | LLM-powered | LinkedIn post text |

**Demo Points**:
1. Run `--self-analyze` mode
2. Show each tool executing in sequence
3. Display intermediate outputs (code stats, architecture)
4. Show final LinkedIn post generation
5. Open saved reports in `reports/`

---

## Component 5: Performance Evaluation System

**Purpose**: Measure and track system performance across multiple dimensions

```mermaid
graph TD
    Interaction[📝 User Interaction] -->|Capture| Logger[Event Logger]

    Logger -->|Store| InteractionData[Interaction Data<br/>Query + Response + Context]

    InteractionData -->|Evaluate| Evaluator[📊 Evaluator]

    subgraph Metrics["📈 Evaluation Metrics"]
        Evaluator -->|Metric 1| M1[Retrieval Accuracy<br/>Doc relevance score]
        Evaluator -->|Metric 2| M2[Response Relevance<br/>Answer quality score]
        Evaluator -->|Metric 3| M3[Tool Accuracy<br/>Correct tool usage]
        Evaluator -->|Metric 4| M4[Reasoning Quality<br/>Logic coherence]
    end

    subgraph Scoring["🎯 Scoring Methods"]
        M1 -->|Method| S1[Cosine Similarity<br/>Query vs Retrieved]
        M2 -->|Method| S2[Levenshtein Distance<br/>Expected vs Actual]
        M3 -->|Method| S3[Binary Correctness<br/>Right tool used?]
        M4 -->|Method| S4[LLM-as-Judge<br/>Self-evaluation]
    end

    S1 & S2 & S3 & S4 -->|Aggregate| OverallScore[Overall Score<br/>Weighted average]

    OverallScore -->|Store| MetricsDB[(Metrics Storage<br/>JSON logs)]

    MetricsDB -->|Generate| Reports[📄 Reports]

    subgraph ReportTypes["📊 Report Types"]
        Reports -->|Real-time| RTReport[Console Output<br/>Per-query metrics]
        Reports -->|Session| SessionReport[Session Summary<br/>Average scores]
        Reports -->|Historical| HistReport[Historical Analysis<br/>Trends over time]
    end

    RTReport & SessionReport & HistReport -->|Export| Files[💾 Export Files<br/>logs/ & reports/]

    classDef input fill:#5DADE2,stroke:#2874A6,stroke-width:2px,color:#fff
    classDef process fill:#F39C12,stroke:#B8730D,stroke-width:2px,color:#000
    classDef metrics fill:#E74C3C,stroke:#C0392B,stroke-width:2px,color:#fff
    classDef output fill:#27AE60,stroke:#1E8449,stroke-width:2px,color:#fff

    class Interaction,InteractionData input
    class Logger,Evaluator,OverallScore process
    class M1,M2,M3,M4,S1,S2,S3,S4 metrics
    class MetricsDB,Reports,RTReport,SessionReport,HistReport,Files output
```

**Evaluation Dimensions**:

1. **Retrieval Accuracy** (0.0 - 1.0)
   - Measures relevance of retrieved documents
   - Uses cosine similarity between query and doc embeddings
   - Higher = better context for LLM

2. **Response Relevance** (0.0 - 1.0)
   - Measures answer quality vs. question
   - Uses semantic similarity + keyword overlap
   - Higher = more relevant answer

3. **Tool Accuracy** (0.0 - 1.0)
   - Binary: Did agent use correct tool?
   - Tracks tool selection correctness
   - 1.0 = correct tool, 0.0 = wrong/missing

4. **Reasoning Quality** (0 - 10)
   - LLM-as-judge self-evaluation
   - Assesses logical coherence
   - Higher = better reasoning chain

**Demo Points**:
1. Run agent mode with evaluation enabled
2. Show real-time metrics after each question
3. Display session summary (average scores)
4. Open `reports/evaluation_TIMESTAMP.json`
5. Highlight improvements over time (if multiple sessions)

---

## Component 6: Multi-Provider LLM Layer

**Purpose**: Abstract LLM provider interface for flexibility

```mermaid
graph LR
    Agent[🤖 Agent/Chatbot] -->|Request| Interface[🔌 LLM Provider Interface]

    Interface -->|Route to| ProviderFactory[Provider Factory<br/>Based on --provider flag]

    subgraph Providers["🤖 LLM Providers"]
        Ollama[🦙 Ollama<br/>Local deployment]
        Groq[⚡ Groq<br/>Cloud API]
        Gemini[✨ Gemini<br/>Google AI]
    end

    ProviderFactory -->|If ollama| Ollama
    ProviderFactory -->|If groq| Groq
    ProviderFactory -->|If gemini| Gemini

    subgraph OllamaDetails["🦙 Ollama Configuration"]
        Ollama -->|Default| OModel1[llama3.2]
        Ollama -->|Optional| OModel2[mistral]
        Ollama -->|Optional| OModel3[llama3.1]
        OModel1 & OModel2 & OModel3 -->|Local| OEndpoint[http://localhost:11434]
    end

    subgraph GroqDetails["⚡ Groq Configuration"]
        Groq -->|Default| GModel1[llama3-70b-8192]
        Groq -->|Optional| GModel2[mixtral-8x7b]
        GModel1 & GModel2 -->|API Key| GAuth[GROQ_API_KEY]
        GAuth -->|Cloud| GEndpoint[api.groq.com]
    end

    subgraph GeminiDetails["✨ Gemini Configuration"]
        Gemini -->|Default| GemModel[gemini-1.5-flash]
        GemModel -->|API Key| GemAuth[GOOGLE_API_KEY]
        GemAuth -->|Cloud| GemEndpoint[generativelanguage.googleapis.com]
    end

    OEndpoint & GEndpoint & GemEndpoint -->|Response| Interface
    Interface -->|Return| Agent

    classDef interface fill:#2E86C1,stroke:#1B4F72,stroke-width:2px,color:#fff
    classDef provider fill:#27AE60,stroke:#1E8449,stroke-width:2px,color:#fff
    classDef config fill:#F39C12,stroke:#B8730D,stroke-width:2px,color:#000

    class Agent,Interface,ProviderFactory interface
    class Ollama,Groq,Gemini provider
    class OModel1,OModel2,OModel3,GModel1,GModel2,GemModel,OEndpoint,GEndpoint,GemEndpoint,OAuth,GAuth,GemAuth config
```

**Provider Comparison**:

| Feature | Ollama | Groq | Gemini |
|---------|--------|------|--------|
| **Deployment** | Local | Cloud | Cloud |
| **Speed** | Medium | Fast | Fast |
| **Privacy** | High | Medium | Medium |
| **Cost** | Free | Free (limited) | Free (limited) |
| **Setup** | `ollama serve` | API key | API key |
| **Best For** | Privacy, offline | Speed, large models | Low-latency, multimodal |

**Demo Points**:
1. Show switching providers: `--provider ollama` → `--provider groq`
2. Compare response times for same query
3. Show configuration in `.env` file
4. Demonstrate model override: `--model llama3-8b`

---

## System Integration Diagram

**Purpose**: How all components work together end-to-end

```mermaid
graph TB
    Start([Start Application]) -->|main.py| Init[Initialize System]

    Init -->|Load| Config[Configuration<br/>Provider, Model, Flags]
    Init -->|Create| VectorStore[ChromaDB Vector Store]
    Init -->|Check| DBExists{Database<br/>Exists?}

    DBExists -->|No or --rebuild| Ingestion[Data Ingestion Pipeline]
    DBExists -->|Yes| SkipIngestion[Use Existing DB]

    Ingestion -->|Build| VectorStore
    SkipIngestion --> VectorStore

    VectorStore -->|Initialize| LLMProvider[LLM Provider<br/>Ollama/Groq/Gemini]
    LLMProvider -->|Create| Retriever[RAG Retriever]

    Retriever -->|Check| AgentMode{Agent Mode<br/>Enabled?}

    AgentMode -->|Yes| CreateAgent[Create AI Agent<br/>Reasoner + Evaluator + Tools]
    AgentMode -->|No| SkipAgent[Standard RAG Only]

    CreateAgent -->|Initialize| Chatbot[RAG Chatbot]
    SkipAgent -->|Initialize| Chatbot

    Chatbot -->|Check| SelfAnalyze{Self-Analyze<br/>Mode?}

    SelfAnalyze -->|Yes| RunAnalysis[Run Self-Analysis<br/>Tools execution]
    SelfAnalyze -->|No| RunQueries[Run Test Questions]

    RunAnalysis -->|Generate| Reports[Generate Reports<br/>JSON + LinkedIn Post]
    Reports --> End([Exit])

    RunQueries -->|Process| Interactive[Interactive Mode<br/>User Q&A]

    Interactive -->|For each query| Process{Agent Mode?}

    Process -->|Yes| AgentFlow[Agent Orchestration<br/>Reason→Retrieve→Execute→Reflect]
    Process -->|No| RAGFlow[Standard RAG<br/>Retrieve→Generate]

    AgentFlow -->|Evaluate| Metrics[Performance Evaluation]
    RAGFlow --> Response[Generate Response]

    Metrics -->|Return| Response
    Response -->|Display| User[👤 User Output]

    User -->|Continue?| Interactive
    User -->|Exit| FinalReport{Agent Used?}

    FinalReport -->|Yes| ExportReports[Export Performance Reports]
    FinalReport -->|No| SkipReports[No Reports]

    ExportReports --> End
    SkipReports --> End

    classDef start fill:#27AE60,stroke:#1E8449,stroke-width:2px,color:#fff
    classDef init fill:#5DADE2,stroke:#2874A6,stroke-width:2px,color:#fff
    classDef process fill:#F39C12,stroke:#B8730D,stroke-width:2px,color:#000
    classDef agent fill:#9B59B6,stroke:#6C3483,stroke-width:2px,color:#fff
    classDef output fill:#E74C3C,stroke:#C0392B,stroke-width:2px,color:#fff

    class Start,End start
    class Init,Config,VectorStore,LLMProvider,Retriever,Chatbot init
    class Ingestion,RunQueries,Process,RAGFlow,AgentFlow,Response process
    class CreateAgent,RunAnalysis,Metrics agent
    class Reports,ExportReports,User output
```

---