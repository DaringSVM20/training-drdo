# Amaya RAG & Presentation Pipeline Rebuild Setup Guide

This guide describes how to configure, run, and troubleshoot the Amaya RAG (Retrieval-Augmented Generation) and themed slide presentation pipeline from scratch on a fresh offline Windows environment.

---

## 1. Prerequisites & Environment Setup

This project is built and optimized for **Python 3.11** (specifically virtual environments targeting Python 3.11.15).

### Set Up Python 3.11 Environment
To set up a fresh environment from scratch:
1. **Install Python 3.11**: Download and run the Python 3.11 Windows installer (ensure "Add Python to PATH" is checked).
2. **Create a Virtual Environment**:
   Open PowerShell/Command Prompt at the project root folder (`rag-main`) and run:
   ```powershell
   python -m venv amaya_env
   ```
3. **Activate the Environment**:
   ```powershell
   # In PowerShell:
   .\amaya_env\Scripts\Activate.ps1
   
   # In CMD:
   .\amaya_env\Scripts\activate.bat
   ```

---

## 2. Offline Dependency Installation

For air-gapped or offline Windows machines, packages can be staged and installed without internet access.

### Step 1: Stage packages on an internet-connected PC
Run the following command on a machine with internet access to download all required packages as packages wheels:
```powershell
# Create folder to hold downloaded wheels
mkdir offline_packages

# Download all required wheels (non-recursive, to save only target packages)
pip download --no-deps -d ./offline_packages -r requirements.txt
```
*Note: If PyPI requires downloading dependencies not already in the base Python installation, remove `--no-deps` or download them manually into `offline_packages/`.*

### Step 2: Install offline on the air-gapped PC
Transfer the project directory and the `offline_packages` folder to your target Windows machine, activate your virtual environment, and run:
```powershell
pip install --no-index --find-links=offline_packages -r requirements.txt
```

---

## 3. Large Model Configuration (Cache Setup)

The ingestion pipeline (Docling OCR and table extractors) and the search-ranking system require offline neural network weights. 

### Where Model Files Must Live
All local model files must reside in the directory specified by `config.MODELS_CACHE` (which maps to `Amaya/models_cache/` in the project root):
```
d:\June 2026 Internship\project\rag-main\Amaya\models_cache\
```

Ensure the following subfolders are present under `models_cache/`:
1. **Docling Layout/OCR Models** (obtained from your coworker):
   - `RapidOcr`
   - `docling-project--CodeFormulaV2`
   - `docling-project--TableFormerV2`
   - `docling-project--docling-layout-heron`
   - `docling-project--docling-models`
   - `ds4sd--DocumentFigureClassifier`
   - `ibm-granite--granite-docling-258M`
2. **Reranker Model (Optionalized)**:
   - `ms-macro-MiniLM-L6-v2` *(If this folder is missing, the system will fall back to using the Granite model's tokenizer to initialize chunking offline, and will bypass search reranking)*

### How to Verify Correct Placement
You can verify the cache folders exist by running this command in PowerShell:
```powershell
Get-ChildItem -Path ".\Amaya\models_cache"
```
It should display all 7-8 model names in the directory directory list.

---

## 4. Run Ollama Server (Local LLM & Embedding)

Ollama handles prompt synthesis and vector generation.

1. **Verify Ollama is Running**:
   On the Windows taskbar, locate the Ollama icon or run:
   ```powershell
   ollama list
   ```
2. **Ensure Required Models are Pulled**:
   The presentation generation requires the following models loaded:
   - **LLM Model**: `phi3:mini` (2.2 GB)
   - **Embedding Model**: `nomic-embed-text` (or another model set in config)
   
   If `phi3:mini` is missing from `ollama list`, run:
   ```powershell
   ollama pull phi3:mini
   ollama pull nomic-embed-text
   ```

---

## 5. Launch the Streamlit Application

Run the application inside the virtual environment:
```powershell
# Ensure your environment is active:
.\amaya_env\Scripts\Activate.ps1

# Start the Streamlit server:
streamlit run .\Amaya\gui.py
```
This will automatically open the browser interface at `http://localhost:8501`.

---

## 6. How to Run a Test Presentation Gen

To verify the pipeline functions correctly:
1. Open the UI browser tab.
2. Select the **Knowledge Engineering Studio** tab.
3. Upload a sample document PDF (e.g. `Amaya Research Paper.pdf`). Click **Initiate Engineering Workflow** to ingest it. You should see live logs streamed to confirm chunking.
4. Go to the **Strategic Presentation Suite** tab.
5. In the *Presentation Controls* column:
   - Select a visual theme (e.g., **Corporate Navy**, **Emerald Executive**).
   - Enter **Custom Formatting Instructions** (e.g., `"Focus on business metrics and key statistics only"`).
6. Click **🚀 Build Strategic Intelligence Deck**.
7. The system will synthesize the slides, construct the PPTX with backgrounds and bounding margins, and render a download button to save `Presentation_xxxxxx.pptx`.

---

## 7. Common Issues & Troubleshooting

| Issue / Error | Root Cause | Fix |
|---|---|---|
| **`ImportError: cannot import name ...`** | Python is picking up script files from the root folder instead of the `Amaya/` subfolder. | Always run Streamlit using the command `streamlit run .\Amaya\gui.py` from the project root directory. Do not run it from inside `Amaya/` without setting `PYTHONPATH`. |
| **`OSError: Repo id must use alphanumeric chars...`** | The offline chunker could not locate the tokenizers folder on disk. | Ensure the model cache directory folders (specifically the Granite model folder `ibm-granite--granite-docling-258M`) exist inside `Amaya\models_cache\`. |
| **`Ollama Generation Error: 400 Client Error: Bad Request`** | The document context window was overloaded, or the context exceeded default Ollama limits. | Clean or reduce your context files. We have optimized `gui.py` to limit context to 15 chunks and increased the API request window to `num_ctx: 4096` to resolve this. |
| **`ConnectionError: Could not reach Ollama server`** | The Ollama desktop service is stopped. | Start Ollama client from your Start Menu or execute `ollama serve` in a background terminal. |
| **`ImportError: DLL load failed` (PyTorch/CUDA)** | The Python environment contains binary mismatch for Windows (often happens if transferring packages between different OS architectures). | Reinstall the PyTorch/dependencies inside the virtual environment using the correct Windows wheel version. |
