import os
import shutil
import tempfile
import gradio as gr
from reader import read_text, chunk_text
from vectorstore import ChromaRAG
from answerGenerator import AnswerGenerator

rag = ChromaRAG()
gen = AnswerGenerator()

# 1. Upload: Extract Text -> Create Chunk -> Store -> ready to retrieve

def upload_file(uploaded):
    if not uploaded:
        return "Please upload a file."

    src_path = string(uploaded)

    if not os.path.exists(src_path):
        return f"File not found: {src_path}"

    temp_dir = tempfile.mkdtemp()
    dest_path = os.path.join(temp_dir, os.path.basename(src_path))
    shutil.copy(src_path, dest_path)

    text = read_text(dest_path)
    chunks = chunk_text(text)
    rag.build(chunks)

    return f"Indexed {len(chunks)} chunks. You can now ask questions."
    
# 2. Answer a question

def ask_question(question):
    if not question:
        return "Please enter a question."

    if rag.collection is None:
        return "Please upload a document first."

# Retrieve the top matching chunks
    docs = rag.search(question, top_k=4)
    return results

    # Extract only the text parts
    contexts = [d for d in docs]

    # Generate answer
    answer = gen.answer(question, contexts)

    src_list = "\n".join([f"- {d[:120]}..." for d in contexts])

    return answer + "\n\nSources:\n" + src_list

# 3. Build APP UI with Gradio

with gr.Blocks(title="AI PDF RAG with ChromaDB") as demo:
    gr.Markdown("## AI PDF RAG with ChromaDB and FLAN-T5")


    with gr.Row():
        with gr.Column():
            file_in = gr.File(label="Upload PDF or txt file")
            upload_btn = gr.Button("Index Document")
            status = gr.Textbox(label="Status")

        with gr.Column():
            question_in = gr.Textbox(label="Ask a question")
            ask_btn = gr.Button("Ask")
            answer_out = gr.Textbox(label="Answer", lines=10)
            upload_btn.click(upload_file, inputs=file_in, outputs=status)

        ask_btn.click(ask_question, inputs=question_in, outputs=answer_out)
        upload_btn.click(upload_file, inputs=question_in, outputs=status)

# Run app

if __name__ == "__main__":
    demo.launch()

