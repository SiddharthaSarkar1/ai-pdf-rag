# AI PDF RAG with ChromaDB and FLAN-T5

This project is a Retrieval-Augmented Generation (RAG) application that allows you to chat with your PDF and text documents. You can upload a file, and the application will index its content. You can then ask questions, and the application will use the document's content to generate an answer.

This application is built with a Streamlit user interface.

## Features

*   **File Upload:** Supports both PDF and plain text files.
*   **Document Indexing:** Extracts text, splits it into manageable chunks, and stores it in a ChromaDB vector store.
*   **Semantic Search:** Uses `sentence-transformers` to find the most relevant text chunks for your question.
*   **Answer Generation:** Leverages Google's FLAN-T5 model to generate natural language answers based on the retrieved context.
*   **Source Verification:** Displays the exact text chunks that were used to generate the answer, allowing you to verify the information.

## Getting Started

### Prerequisites

*   Python 3.8+

### Installation

1.  **Clone the repository (or download the files):**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

To run the Streamlit application, use the following command in your terminal:

```bash
streamlit run streamlit_app.py
```

This will open a new tab in your web browser with the application interface. 

1.  Upload a PDF or TXT file using the file uploader.
2.  Wait for the application to process and index the document.
3.  Once indexing is complete, type your question into the text box and click "Ask".
4.  The answer and the sources used to generate it will be displayed.

## Core Technologies

*   **UI:** Streamlit
*   **Vector Store:** ChromaDB
*   **Embedding Model:** `all-MiniLM-L6-v2` from `sentence-transformers`
*   **LLM for Answer Generation:** `google/flan-t5-small` from `transformers`
*   **PDF Parsing:** `pdfplumber`
