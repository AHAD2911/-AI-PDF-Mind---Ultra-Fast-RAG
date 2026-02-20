# 🧠 AI PDF Mind - Ultra-Fast RAG

A premium, high-performance RAG (Retrieval-Augmented Generation) application built with **LlamaIndex**, **Groq**, and **Streamlit**. Talk to your PDFs with lightning speed and a modern glassmorphism interface.

![Project Demo](rag_demo.mp4)

> **Note:** Watch the `rag_demo.mp4` for a full walkthrough of the application's capabilities.

## 🚀 Key Features
-   **Ultra-Fast Inference**: Uses **Groq LPU™** with Llama 3 70B for near-instant responses.
-   **No-Cost Embeddings**: Local **HuggingFace** embeddings (`BGE-Small`) avoid API costs and quotas.
-   **Premium UI**: Custom CSS with glassmorphism, gradients, and responsive chat interface.
-   **Session Management**: Clear chat history and reset index directly from the sidebar.

## 🛠️ Tech Stack
-   **Core**: Python
-   **Framework**: [Streamlit](https://streamlit.io/)
-   **Orchestration**: [LlamaIndex](https://www.llamaindex.ai/)
-   **LLM Interface**: [Groq](https://groq.com/)
-   **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (via HuggingFace)

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/AHAD2911/-AI-PDF-Mind---Ultra-Fast-RAG.git
    cd RAG-project
    ```

2.  **Set up Virtual Environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## ⚙️ Configuration
The application is pre-configured to use a Groq API key. You can update the `GROQ_API_KEY` in `app.py` for your own production use.

---

