import os
import shutil
import tempfile
import gradio as gr

# 1. Upload: Extract Text -> Create Chunk -> Store -> ready to retrieve

def upload_file(uploaded):
    if not uploaded:
        return "Please upload a file."

    src_path = string(uploaded)

    if not os.path.exists(src_path):
        return f"File not found: {src_path}"

    