import os
import shutil
import tempfile
import gradio as gr
from reader import read_text, chunk_text


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
    