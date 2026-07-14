# Technologies Used

This section catalogues the programming languages, frameworks, libraries, AI models, and software architectures utilized in the development and deployment of the Amaya Operational Intelligence platform.

---

## Programming Languages

### Python 3.11.15
* **What it is**: A high-level, general-purpose, interpreted programming language designed for readability and strong machine learning ecosystems.
* **Why it is used**: It serves as the primary programming runtime for all processing pipelines, libraries integration, and mathematical indexes.
* **Where exactly it appears in the project**: The entire project codebase, including `config.py`, `vector_engine.py`, `generation_engine.py`, `ingestion_engine.py`, `presentation_engine.py`, and `gui.py`.
* **Important implementation details**: Developed using Python 3.11.15. The system leverages multithreading for asynchronous background processing while handling Streamlit GUI reactivity in the main script thread.
* **Things that would be worth mentioning in an internship report**: Used as the primary programming dialect for backend RAG architecture integrations. Addressed specific syntax constraints (e.g., Python 3.11 f-string backslash specifications and platform directory checks) to ensure standard compliance for defense systems installations.
* **Common interview questions related to that technology**:
  * *What are the performance differences between Python 3.11 and prior versions?* (Answer: Python 3.11 is up to 10-60% faster than Python 3.10 depending on workload, featuring a specialized adaptive interpreter and improved speedups for function calls).
  * *How does Python manage memory when passing large vectors or layouts?* (Answer: Automatic reference counting and generational garbage collection. Explicit garbage collections and memory-unloading calls were utilized to release index parameters during data ingestions).

---

## Frameworks

### Streamlit (v1.30+)
* **What it is**: An open-source Python framework designed for constructing rapid, interactive, data-driven web applications directly from code.
* **Why it is used**: Chosen as the primary graphical frontend interface of the Amaya project, exposing backend RAG mechanisms, search queries, and presentation download tools without requiring Javascript/HTML codebases.
* **Where exactly it appears in the project**: [gui.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/gui.py).
* **Important implementation details**:
  * Utilizes `st.session_state` to sync chat databases, loading overlays, and page routing.
  * Employs `@st.cache_resource` on initializations to prevent database connections and tokenizer structures from loading twice.
  * Spins up a parallel background `threading.Thread` to execute docling ingestion tasks, passing logs via a thread-safe Queue to stream live status directly to UI markdown components.
* **Things that would be worth mentioning in an internship report**: Engineered a dual-studio interactive platform (Knowledge Engineering + Strategic Presentation Builder) using Streamlit. Configured custom styling overlays and custom session caching strategies to speed up startup times.
* **Common interview questions related to that technology**:
  * *Explain the execution architecture of a Streamlit app.* (Answer: Whenever a user interacts with a widget, Streamlit re-runs the entire script from the first line to the last. Session state must be used to preserve stateful values across runs).
  * *How would you make a heavy initialization run only once inside Streamlit?* (Answer: Cache it using `@st.cache_resource` for global database handlers, or `@st.cache_data` for calculations/dataframes).

### Docling Document-Converter (IBM Docling v2.x architecture)
* **What it is**: A document parsing framework developed by IBM that structures PDFs, images, and text documents into structured markdown formats.
* **Why it is used**: It replaces traditional line-by-line flat document readers (which break multi-column text flow) by parsing document layouts, detecting reading directions, and preserving tables and headers.
* **Where exactly it appears in the project**: [ingestion_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/ingestion_engine.py).
* **Important implementation details**: Incorporates layout analyzing classification models (`docling-layout-heron`), OCR scanners (`RapidOcr`), and coordinates cells detectors (`TableFormerV2`) to map PDFs into JSON schemas.
* **Things that would be worth mentioning in an internship report**: Successfully implemented and deployed the IBM Docling conversion pipeline on an air-gapped environment. Configured file path overrides and built a tokenizer fallback parameter to allow the system to operate offline.
* **Common interview questions related to that technology**:
  * *Why does a standard RAG system fail when reading multi-column research papers using generic PDF parsers?* (Answer: Generic parsers read horizontally across columns, combining unrelated text blocks. A layout-aware parser like Docling reconstructs column sequences, preserving context readability).

---

## Libraries

### `python-pptx` (v1.0.2)
* **What it is**: A Python library used for programmatically creating and modifying Microsoft PowerPoint (.pptx) presentation files.
* **Why it is used**: Translates parsed LLM slide summaries into fully styled presentations, handling visual layouts, labels, and text overflows automatically.
* **Where exactly it appears in the project**: [presentation_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/presentation_engine.py).
* **Important implementation details**: Directly constructs shape definitions (titles, margins, bulleted lists) using exact coordinates. Includes custom logic to count bullet points and auto-generate continuation slides if bullets exceed 6.
* **Things that would be worth mentioning in an internship report**: Developed a slide generation engine that formats bullet lengths, slide sizes, and draws custom visual themes directly on blank PowerPoint templates.
* **Common interview questions related to that technology**:
  * *How would you programmatically handle text overflow inside a presentation slide using python-pptx?* (Answer: Calculate the height of the text block based on paragraph count and font sizes, or enforce a strict limit on bullet points, programmatically creating a new slide to hold any overflow).

### `xlsxwriter` (v3.2.9)
* **What it is**: A Python module used to write text, formulas, and formatting parameters to Excel spreadsheet files (.xlsx).
* **Why it is used**: Writes complex tables extracted by Docling parser models so users can view and download them.
* **Where exactly it appears in the project**: [ingestion_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/ingestion_engine.py).
* **Important implementation details**: Triggered inside the ingestion workflow to export parsed document tables as standalone Excel books in the process directories.
* **Things that would be worth mentioning in an internship report**: Enabled offline tabular retrieval by extracting embedded PDF tables and exporting them to Excel files for secondary analysis.

### `pydantic` & `pydantic-settings` (v2.14.2)
* **What it is**: A data validation and configuration framework that uses Python type hinting to parse configuration files and environment overrides.
* **Why it is used**: Manages system state variables and paths dynamically, validating details before initializing engines.
* **Where exactly it appears in the project**: [config.py](file:///d:/June%202026%20Internship/project/rag-main/config.py) and [Amaya/config.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/config.py).
* **Important implementation details**: Extends `BaseSettings` to parse configuration parameters, allowing environment variables prefixed with `DOCLING_PRO_` to override hardcoded paths at runtime.
* **Things that would be worth mentioning in an internship report**: Configured configuration schemas to support smooth runtime switches between local model directories and local API servers.
* **Common interview questions related to that technology**:
  * *What is the advantage of using Pydantic Settings over standard os.getenv checks?* (Answer: Pydantic Settings performs validation, enforces types, and raises errors early if values are missing or invalid).

### PyMuPDF (`fitz`)
* **What it is**: A high-performance Python binding for MuPDF, a lightweight PDF rendering and processing library.
* **Why it is used**: Used to render pages from uploaded PDF documents to generate image previews in the Streamlit UI.
* **Where exactly it appears in the project**: [gui.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/gui.py).
* **Important implementation details**: Loads PDF files, renders targets page-by-page to a specified resolution, and exports them as raw bytes for Streamlit rendering.
* **Things that would be worth mentioning in an internship report**: Designed a rapid PDF document viewer inside Streamlit by rendering vector formats directly to PNG on the fly.

### `chromadb`
* **What it is**: An open-source, database-backed vector store optimized for rapid embeddings search.
* **Why it is used**: Serves as the primary metadata and vector embeddings repository, performing Approximate Nearest Neighbor search during query retrieval.
* **Where exactly it appears in the project**: [vector_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/vector_engine.py).
* **Important implementation details**: Runs locally as a persistent client, saving SQLite data to the `chroma_db` folder.
* **Things that would be worth mentioning in an internship report**: Integrated and optimized a local vector database to index and search document metadata offline.
* **Common interview questions related to that technology**:
  * *How does a vector database find semantically similar documents?* (Answer: Computes similarity scores, such as Cosine Similarity or L2 distance, in a multi-dimensional coordinate space using vector clustering indices).

### `rank_bm25`
* **What it is**: A Python library that implements the Okapi BM25 keyword matching scoring algorithm.
* **Why it is used**: Conducts keyword-based lexical searches against document collections, complementing vector search.
* **Where exactly it appears in the project**: [vector_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/vector_engine.py).
* **Important implementation details**: Tokenizes raw document text, builds frequency matrices, and saves indices as pickle files.
* **Things that would be worth mentioning in an internship report**: Implemented a hybrid index architecture merging Vector (dense) and BM25 (lexical) search using Reciprocal Rank Fusion (RRF).

---

## AI Models

### Microsoft Phi-3-Mini (`phi3:mini`)
* **What it is**: A lightweight, open-weight language model (3.8 billion parameters) developed by Microsoft.
* **Why it is used**: Serves as the primary LLM for local inference. It generates natural language responses and structures slide layouts from search results.
* **Where exactly it appears in the project**: Queried via the HTTP REST API in [generation_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/generation_engine.py).
* **Important implementation details**: Runs locally via Ollama. Set to a low temperature config (`0.1`) to ensure factual responses, with context window parameters set to 4,096 tokens.
* **Things that would be worth mentioning in an internship report**: Deployed and queried Microsoft Phi-3-Mini offline. Successfully handled strict format instructions (JSON and XML slide layouts) even with a smaller 3.8B parameters model.
* **Common interview questions related to that technology**:
  * *Why are small language models (SLMs) like Phi-3 preferred in local defense environments?* (Answer: They require minimal memory (under 4GB RAM), run entirely offline, and execute quickly without dependency on cloud access).

### IBM Granite Docling Chunker (`ibm-granite--granite-docling-258M`)
* **What it is**: IBM's optimized document structure transformer model (258M parameters).
* **Why it is used**: Interprets document layout, bounding boxes, and document structures for high-accuracy OCR hierarchy mapping. Its accompanying tokenizer is used as our offline utility.
* **Where exactly it appears in the project**: [ingestion_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/ingestion_engine.py).
* **Important implementation details**: Evaluates page layout regions. Its tokenizer acts as our local fallback engine for document chunking if the main reranking tokenizer is unavailable.
* **Things that would be worth mentioning in an internship report**: Used the IBM Granite tokenizer offline to slice raw document structures into precise chunk lengths based on character layouts.

### Cross-Encoder Reranker (`ms-macro-MiniLM-L6-v2`)
* **What it is**: A pre-trained Transformer model that calculates the exact query-document relevance by feeding both query and document into the attention layer concurrently.
* **Why it is used**: To re-rank the combined search results from BM25 and vector search, improving retrieval accuracy.
* **Where exactly it appears in the project**: [vector_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/vector_engine.py) (referred to by `config.RERANKER_MODEL_PATH`).
* **Important implementation details**: Implemented as an optionalized component. If the folder path is found, it calculates relevance scores; if missing, it falls back to a simpler scoring method.
* **Things that would be worth mentioning in an internship report**: Integrated a local reranking pipeline to improve the relevance of retrieved context before sending it to the LLM.

---

## RAG Components

### Dual-Strategy Hybrid Retriever
* **What it is**: A search pipeline that combines dense vector search with sparse keyword search.
* **Why it is used**: Vector search captures abstract context and synonyms, while BM25 search captures exact keyword matches (like specific file names or numbers).
* **Where exactly it appears in the project**: [vector_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/vector_engine.py) (within `VectorEngine.query`).
* **Important implementation details**:
  * Retrieves top `K` results from ChromaDB and BM25 separately.
  * Normalizes and merges these results to rank the most relevant document chunks.
* **Things that would be worth mentioning in an internship report**: Designed and implemented a hybrid search retriever that combines vector space search with keyword indices.

---

## Embedding Models

### `nomic-embed-text`
* **What it is**: A high-performance text embedding model with a large context window (8,192 tokens).
* **Why it is used**: It converts raw text chunks into 768-dimensional vectors that represent the semantic meaning of the text.
* **Where exactly it appears in the project**: Configured in [config.py](file:///d:/June%202026%20Internship/project/rag-main/config.py) and executed via Ollama.
* **Important implementation details**: Configured as the primary embedding generator for building vector collections in ChromaDB.

---

## Vector Databases

### ChromaDB
* **What it is**: A vector database optimized for storing token embeddings and managing unstructured research vault segments.
* **Why it is used**: Saves documents inside local persistent folders via SQLite index parameters.
* **Where exactly it appears in the project**: [vector_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/vector_engine.py).

---

## APIs

### Ollama REST API
* **What it is**: A local HTTP server that lets you run and query open-weight LLMs on your own machine.
* **Why it is used**: Exposes local endpoints like `/api/chat` and `/api/tags` to generate text and list available models.
* **Where exactly it appears in the project**: [generation_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/generation_engine.py).
* **Important implementation details**: Used Python's `requests` library to stream responses from the `/api/chat` endpoint and process options like `"num_ctx"` and `"temperature"`.

---

## Databases

### SQLite (Embedded)
* **What it is**: A C-language library that implements a small, fast, self-contained, high-reliability, full-featured SQL database engine.
* **Why it is used**: Used by ChromaDB to store documents, index relationships, metadata, and segment IDs locally.
* **Where exactly it appears in the project**: Underneath the persistent directory folder `chroma_db/`.

---

## Backend Technologies

### Streamlit Internal Server (Uvicorn / WebSockets)
* **What it is**: Streamlit's web-server adapter that handles socket sessions and routes client states.
* **Why it is used**: Translates real-time values from the GUI browser views into Python threads.
* **Where exactly it appears in the project**: Streamlit dashboard environment execution.

---

## Frontend Technologies

### Streamlit Components & Custom CSS Injection
* **What it is**: Python utilities to inject styled custom layouts and CSS modifications directly within Streamlit blocks.
* **Why it is used**: Allows customizing the default Streamlit theme, giving the interface a dark-themed visual layout (`brand-container`, citation cards).
* **Where exactly it appears in the project**: [gui.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/gui.py).

---

## Document Processing

### Layout-Aware PDF Parser (IBM Docling Engine)
* **What it is**: A document parsing tool that detects layout elements like headers, columns, tables, and images.
* **Why it is used**: It preserves the structural formatting of complex reports, preventing data tables or columns from getting mixed up during text extraction.
* **Where exactly it appears in the project**: [ingestion_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/ingestion_engine.py).
* **Important implementation details**: Reads PDF files and parses page layout clusters into markdown text and JSON schemas.

---

## Prompt Engineering

### Structured System Prompts (Slide Structuring Template)
* **What it is**: The system prompt used to instruct the LLM to format its output as structured slides.
* **Why it is used**: Ensures the LLM outputs slides using a strict, predictable structure (like `SLIDE: [Title]` followed by bullet points) so the presentation engine can parse it programmatically.
* **Where exactly it appears in the project**: [gui.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/gui.py) (inside the presentation build workflow around lines 960-990).
* **Important implementation details**:
  * Employs few-shot examples (demonstrating correct vs incorrect structures).
  * Injects user-specified custom formatting instructions dynamically into the system definition.

---

## Software Architecture

### Layered RAG Pipeline Architecture
* **What it is**: A design pattern that separates responsibilities into logical layers: interface (Streamlit), search/orchestration (Vector/Retrieval), data storage (ChromaDB), and output formatting (PresentationEngine).
* **Why it is used**: Ensures that changes to one layer (like adding slides styling options) do not affect or break other layers (like parsing or database logic).

---

## Design Patterns

### Singleton Pattern
* **What it is**: A software design pattern that restricts the instantiation of a class to a single, globally shared instance.
* **Why it is used**: Prevents multiple independent instances of heavy database connections (ChromaDB client) or background job managers from conflicting or wasting system memory.
* **Where exactly it appears in the project**:
  * `get_job_manager()` in [gui.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/gui.py) implements a singleton database/state manager class using Streamlit caching.
  * `ModelManager` in [vector_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/vector_engine.py) manages loading/unloading singleton references to active deep-learning models.

---

## Security

### Local-First Network Isolation (Air-Gapped Compliance)
* **What it is**: Enforcing complete offline operation by configuration.
* **Why it is used**: Critical for defense applications (such as at DRDO/TBRL) where computers must remain completely disconnected from the public internet.
* **Where exactly it appears in the project**:
  * Enforced in both `config.py` files via `OFFLINE_MODE = True`.
  * Environment variables `HF_HUB_OFFLINE=1` and `NO_PROXY=*` block any external network connections.
* **Important implementation details**:
  * Restricts libraries from attempting to download weights from the internet during runtime.
  * Tokenization fallbacks ensure the app runs reliably using only locally cached weights.

---

## Deployment

### Python Local Virtual Environment (`amaya_env`)
* **What it is**: An isolated Python runtime directory containing packages and executables.
* **Why it is used**: Ensures the application runs with the exact package versions required (like Python 3.11.15) without conflicts from system-wide Python installations.
* **Where exactly it appears in the project**: The `amaya_env/` directory in the project root.

---

## Infrastructure & Model Configuration (Models Cache Setup)

To execute Amaya successfully in an offline, air-gapped environment (such as TBRL or other secured networks), the local filesystem must contain all necessary dependencies and model files. This section lists these dependencies and outlines the folder structures.

### 1. Offline Environment Dependencies (`amaya_env`)
The project utilizes a pre-configured Python 3.11 virtual environment. For a new deployment, you need to stage package files (wheel `.whl` files) on an internet-enabled PC and install them on the air-gapped system.

**Required Packages (`requirements.txt`):**
* `python-pptx==1.0.2` (Required for building presentation hierarchies programmatically)
* `xlsxwriter==3.2.9` (Required for programmatically building high-fidelity Excel tables from parsed nodes)
* `pydantic-settings==2.14.2` (Required for global settings validations and environmental overrides support)

*Note: The environment also contains the core RAG runtime engines including: `streamlit`, `docling` (with its parser sub-models), `chromadb` (vector storage), `rank_bm25` (lexical indexer), `fitz` (PyMuPDF for PDF preview), and `requests` (for local Ollama communication).*

---

### 2. Large Model Cache Directory Structure
The ingestion parser, chunker, and search-ranking systems require offline deep-learning weights. These files must reside in the directory specified by `config.MODELS_CACHE` (which resolves to `Amaya/models_cache/` in the project root).

Below is the directory structure for `Amaya/models_cache/`:

```
d:\June 2026 Internship\project\rag-main\Amaya\models_cache\
├── RapidOcr/                             # Layout OCR detection libraries
├── docling-project--CodeFormulaV2/       # Mathematical formulas reconstruction models
├── docling-project--TableFormerV2/       # Table structure analyzer and matrix parser
├── docling-project--docling-layout-heron/# Layout classifier and reading order mapper
├── docling-project--docling-models/      # Core Docling structural configurations
├── ds4sd--DocumentFigureClassifier/      # Isolates figure zones and images
├── ibm-granite--granite-docling-258M/    # Lightweight structural parser & falls back tokenizer
└── ms-macro-MiniLM-L6-v2/                # Reranking cross-encoder model folder (Optional)
```

---

### 3. Step-by-Step Operations Guide for a New User
Follow this guide to set up and run the project from scratch:

#### Step A: Pull LLM Models locally via Ollama
Ensure the Ollama service is running on your machine, then pull the LLM models to run them locally:
```powershell
ollama pull phi3:mini
ollama pull nomic-embed-text
```

#### Step B: Launch the Application
Run the Streamlit application using **one** of the methods below:

* **Method 1 (Recommended for PowerShell / terminal command line):**
  Run the application directly using the Python executable inside your virtual environment (no manual activation step needed):
  ```powershell
  .\amaya_env\python.exe -m streamlit run .\Amaya\gui.py
  ```

* **Method 2 (Command Prompt / CMD standard activation):**
  If you are using a standard command window:
  ```cmd
  .\amaya_env\Scripts\activate.bat
  streamlit run .\Amaya\gui.py
  ```

#### Step C: Process and Ingest Documents
1. Open the web interface at `http://localhost:8501`.
2. Navigate to the **Knowledge Engineering Studio** tab in the sidebar.
3. Click "Browse" and upload your target PDF document.
4. Click **Initiate Engineering Workflow** and monitor the progress logs. The system parses the document layout, extracts tables, and saves vector embeddings to ChromaDB.

#### Step D: Generate Boardroom Presentations
1. Navigate to the **Strategic Presentation Suite** tab.
2. Under "Source Material," select the ingested job folder.
3. Choose a styling theme (e.g., **Corporate Navy** or **Emerald Executive**) and input any custom requirements in the **Custom Formatting Instructions** field.
4. Click **🚀 Build Strategic Intelligence Deck**. The system will generate structured slides using the local LLM and build a downloadable styled `.pptx` presentation.

---

# Concepts I Should Learn

## 1. Retrieval-Augmented Generation (RAG)
* **What it is**: An AI system design pattern that retrieves relevant information from a local database and provides it as context to an LLM, helping it generate accurate, factual answers.
* **Why this project needs it**: General LLMs don't know the contents of your local documents. RAG allows the model to answer queries based on custom, local PDFs.
* **Which files/modules use it**:
  * [vector_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/vector_engine.py) (retrieves facts)
  * [generation_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/generation_engine.py) (generates answers based on context)
* **Difficulty**: Intermediate
* **Priority**: **Critical** (This is the core architecture of the project).

## 2. Text Embeddings and Vector Spaces
* **What it is**: Representing the meaning of text as a list of numbers (a vector). Text with similar meanings will have similar mathematical vectors.
* **Why this project needs it**: Enables semantic search (finding chunks of text that match the meaning of a query, even if they don't use the exact same words).
* **Which files/modules use it**: [vector_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/vector_engine.py) (queries ChromaDB collections using text embeddings).
* **Difficulty**: Intermediate
* **Priority**: **High** (Understanding vector spaces is key to tuning retrieval accuracy).

## 3. BM25 Lexical Keyword Search
* **What it is**: A keyword retrieval algorithm that scores document relevance based on term frequency and document length.
* **Why this project needs it**: Helps find exact matches (like serial numbers, acronyms, or specific names) that semantic vector search might skip.
* **Which files/modules use it**: [vector_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/vector_engine.py) (handles hybrid search scoring).
* **Difficulty**: Beginner
* **Priority**: **Medium**

## 4. Cross-Encoder Reranking
* **What it is**: An AI model that compares a search query and a retrieved document chunk together, generating a precise relevance score.
* **Why this project needs it**: Improves search accuracy by re-ranking the combined results of vector search and BM25 search.
* **Which files/modules use it**: [vector_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/vector_engine.py) (uses `ms-macro-MiniLM-L6-v2` for re-ranking).
* **Difficulty**: Advanced
* **Priority**: **Medium**

## 5. Tokenization & LLM Context Limits
* **What it is**: Splitting text into smaller units (tokens) and feeding them to an LLM, which has a maximum capacity (context window) for how many tokens it can process at once.
* **Why this project needs it**: Sending too much retrieved text to the LLM will exceed its limits, causing errors (like the Ollama 400 Bad Request error).
* **Which files/modules use it**:
  * [gui.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/gui.py) (bounds context chunks to 15)
  * [generation_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/generation_engine.py) (configures `num_ctx: 4096`).
* **Difficulty**: Beginner
* **Priority**: **High** (Crucial for debugging API errors).

## 6. Document Layout Trees & OCR Ingestion
* **What it is**: Parsing a document's layout (hierarchies, tables, headers, and columns) instead of reading it as a single block of raw text.
* **Why this project needs it**: Allows the system to capture structure (like keeping tables intact) so the slide builder can format slide content cleanly.
* **Which files/modules use it**: [ingestion_engine.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/ingestion_engine.py).
* **Difficulty**: Advanced
* **Priority**: **High**

## 7. Multithreaded Processing Workers
* **What it is**: Running tasks in a separate background thread so the main application remains responsive.
* **Why this project needs it**: Ingestion is a slow process. Running it in the background keeps the Streamlit UI responsive and allows it to stream progress logs in real-time.
* **Which files/modules use it**: [gui.py](file:///d:/June%202026%20Internship/project/rag-main/Amaya/gui.py) (via `background_worker` threads).
* **Difficulty**: Intermediate
* **Priority**: **High**

---

# Glossary

* **DRDO**: Defence Research and Development Organisation (governing body of TBRL).
* **TBRL**: Terminal Ballistics Research Laboratory (host installation).
* **RAG**: Retrieval-Augmented Generation (context-driven AI generation).
* **LLM**: Large Language Model (the text generator, like Phi-3).
* **SLM**: Small Language Model (optimized, lightweight language model for local deployment).
* **OCR**: Optical Character Recognition (digitizing printed characters from document layout images).
* **Vector स्पेस (Vector Space)**: A mathematical space where text chunks are represented as points based on their semantic meaning.
* **ANN**: Approximate Nearest Neighbor (high-speed vector matching algorithms).
* **ChromaDB**: An open-source vector database used for local storage and retrieval.
* **BM25**: Best Matching 25 (standard keyword-based search ranking algorithm).
* **RRF**: Reciprocal Rank Fusion (an algorithm for combining and ranking search results from multiple search methods).
* **HNSW**: Hierarchical Navigable Small World (fast graph-based vector index).
* **Ollama**: An API server library for running LLMs locally.
* **API**: Application Programming Interface (HTTP communication interfaces between systems).
* **python-pptx**: A Python library used to programmatically generate and edit PowerPoint presentations.
* **docling**: IBM's open-source document parsing library.
* **RapidOCR**: An efficient OCR engine used in Docling for text detection and recognition.
* **TableFormer**: An AI transformer layout block model used to recognize and structure tables in PDFs.
* **pydantic**: A data validation and parsing library using Python type hints.
* **Streamlit**: A Python framework for building local web applications.
* **Session State**: Streamlit variables that persist across page re-runs.
* **Cache Resource**: Caching memory-heavy objects (like database instances) so they don't load twice.
* **Air-gapped**: Computers or networks that are completely isolated from the public internet.
* **WHL (Wheels)**: Pre-compiled ZIP-format packages for installing Python packages without needing to compile from source.
* **NO_PROXY**: An environment variable that forces Python to bypass proxy servers for local requests (like Ollama).
