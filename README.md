# 🍸 TTB Alcoholic Beverage Label Compliance Verifier

An automated compliance auditing prototype for the **Alcohol and Tobacco Tax and Trade Bureau (TTB)**. This application uses multimodal vision LLMs (`Gemma-4-12B`) served via `llama-server` to inspect uploaded beverage front/back labels against statutory standards (**27 CFR Parts 4, 5, and 7**).

---

## 🛠️ Architecture Overview

The system consists of two primary components:
1. **Frontend / Audit Engine:** A Streamlit application (`app.py`) that handles payload formatting, regulatory rule resolution, Base64 image encoding, and live SSE stream parsing.
2. **Local Multimodal Inference Server:** `llama-server` (from `llama.cpp`) running `Gemma-4-12B` with multimodal projection (`mmproj`) support.

---

## 📋 Prerequisites

- **Docker & Docker Desktop** installed and running.
- **Git** installed.
- **System Memory:** Minimum 16 GB RAM / Unified Memory (8–10 GB allocated for model weights).
- **32 GB to run a good response time
---

## 🚀 Quickstart Guide

Choose the method that matches your host hardware setup:

### Method A: Native `llama-server` + Docker Streamlit (Recommended for macOS / Apple Silicon)

Running `llama-server` natively on Apple Silicon allows `llama.cpp` to leverage Apple Metal GPU acceleration directly via Unified Memory Architecture (UMA), while Streamlit runs isolated in Docker.

#### 1. Clone the Repositories
```bash
# Clone this repository
git clone [https://github.com/your-username/gemma-vision-app.git](https://github.com/your-username/gemma-vision-app.git)
cd gemma-vision-app

# Clone and build llama.cpp (if not already built)
git clone [https://github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) ~/llama.cpp
cd ~/llama.cpp
cmake -B build -DGGML_METAL=ON
cmake --build build --config Release -j

