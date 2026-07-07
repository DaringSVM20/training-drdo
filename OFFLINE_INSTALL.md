# Offline Dependencies Installation Guide

This document outlines the steps to deploy the updated `Amaya` codebase and install its dependencies on an air-gapped machine.

---

## Method A: Manual Browser-Only Download (For Maya OS/Hardened Systems)

If your internet-connected PC runs **Maya OS** and you cannot run CLI commands or code editors to pull dependencies, you can download all files directly using any standard web browser.

### 1. Download the Codebase (Zip)
1. Open your web browser on the internet PC and go to your GitHub repository:
   `https://github.com/DaringSVM20/training-drdo`
2. Click the green **Code** button on the top right.
3. Select **Download ZIP**.
4. Transfer this `.zip` file to your USB drive.

### 2. Download the Python Wheels (Web Browser)
Download the `.whl` files directly from PyPI (Python Package Index) using your browser from the following URLs:

1. **`python-pptx` (v1.0.2):**
   * **URL:** [https://pypi.org/project/python-pptx/1.0.2/#files](https://pypi.org/project/python-pptx/1.0.2/#files)
   * **Download File:** `python_pptx-1.0.2-py3-none-any.whl` (Click the link to download the wheel)
2. **`xlsxwriter` (v3.2.9):**
   * **URL:** [https://pypi.org/project/XlsxWriter/3.2.9/#files](https://pypi.org/project/XlsxWriter/3.2.9/#files)
   * **Download File:** `xlsxwriter-3.2.9-py3-none-any.whl`
3. **`pydantic-settings` (v2.14.2):**
   * **URL:** [https://pypi.org/project/pydantic-settings/2.14.2/#files](https://pypi.org/project/pydantic-settings/2.14.2/#files)
   * **Download File:** `pydantic_settings-2.14.2-py3-none-any.whl`

*Move all three downloaded `.whl` files into a folder named `offline_packages/` on your USB drive.*

---

## Method B: Command-Line Staging (Standard Internet PC)

If you have a standard command-line capable internet PC, you can automate wheel downloads:

```bash
# Create staging directory
mkdir offline_packages

# Download target wheels only (no-dependencies, as the base env satisfies others)
pip download --no-deps -d ./offline_packages -r requirements.txt
```

---

## Installation on the Air-Gapped Machine

Transfer the `training-drdo` folder (unzipped) and the `offline_packages/` directory from your USB to the air-gapped machine and run:

1. **Start Ollama:**
   ```cmd
   ollama serve
   ```
   *(Ensure model `phi3:mini` is loaded by verifying `ollama list` output)*

2. **Activate your environment & install wheels offline:**
   Open a command prompt in the unzipped folder:
   ```cmd
   # (Optional) If using virtual environment
   python -m venv .venv
   .venv\Scripts\activate

   # Install the wheels
   pip install --no-index --find-links=./offline_packages -r requirements.txt
   ```

3. **Launch the application:**
   ```cmd
   streamlit run Amaya/gui.py
   ```
