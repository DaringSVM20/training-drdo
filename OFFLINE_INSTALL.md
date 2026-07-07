# Offline Dependencies Installation Guide

This document outlines the packages required to install the PowerPoint generation features and run the `Amaya` codebase on an air-gapped machine.

---

## 1. Required Packages & PyPI Download Links

All three packages are **pure Python wheels** (which means they work across all operating systems and architectures without compilation). 

You can download them from the links below on an internet-connected PC, save them to a USB drive/transfer media, and bring them to your air-gapped PC.

| Package Name | Exact Version | PyPI Project Link | Direct Wheel File Name |
| :--- | :--- | :--- | :--- |
| **`python-pptx`** | `1.0.2` | [pypi.org/project/python-pptx/1.0.2](https://pypi.org/project/python-pptx/1.0.2/#files) | `python_pptx-1.0.2-py3-none-any.whl` |
| **`xlsxwriter`** | `3.2.9` | [pypi.org/project/XlsxWriter/3.2.9](https://pypi.org/project/xlsxwriter/3.2.9/#files) | `xlsxwriter-3.2.9-py3-none-any.whl` |
| **`pydantic-settings`** | `2.14.2` | [pypi.org/project/pydantic-settings/2.14.2](https://pypi.org/project/pydantic-settings/2.14.2/#files) | `pydantic_settings-2.14.2-py3-none-any.whl` |

---

## 2. Automated Download (Recommended)

Instead of downloading the files individually through a browser, you can run this command on a machine with internet access. It will automatically download the package wheels:

```bash
# Create a temporary directory for transferring packages
mkdir amaya_packages
cd amaya_packages

# Download the wheels and all their recursive dependencies
pip download python-pptx==1.0.2 pydantic-settings==2.14.2
```

This will save all necessary `.whl` files into the `amaya_packages` folder.

---

## 3. Installation on the Air-Gapped Machine

Transfer the `amaya_packages` directory (or the downloaded `.whl` files) to the offline machine (e.g., in the project root folder) and run:

```bash
pip install --no-index --find-links=./amaya_packages python-pptx pydantic-settings
```

This installs the packages directly utilizing the local wheels without hitting the internet.
