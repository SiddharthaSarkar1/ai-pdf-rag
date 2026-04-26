import streamlit as st
import os
import shutil
import tempfile
from reader import read_text, chunk_text
from vectorstore import ChromaRAG
from answerGenerator import AnswerGenerator

# Initialize ChromaRAG and AnswerGenerator
@st.cache_resource
def init_rag():
    return ChromaRAG()

@st.cache_resource
def init_answer_generator():
    return AnswerGenerator()

rag = init_rag()
gen = init_answer_generator()

st.title("AI PDF RAG with ChromaDB and FLAN-T5")
st.markdown("## Ask questions about your documents")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF or text file", type=["pdf", "txt"])

if uploaded_file is not None:
    with st.spinner("Processing file..."):
        # Create a temporary directory to store the uploaded file
        temp_dir = tempfile.mkdtemp()
        dest_path = os.path.join(temp_dir, uploaded_file.name)
        with open(dest_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Process the file
        text = read_text(dest_path)
        chunks = chunk_text(text)
        rag.build(chunks)
        st.success(f"Indexed {len(chunks)} chunks. You can now ask questions.")
        shutil.rmtree(temp_dir)

# Question input
question = st.text_input("Ask a question")

if st.button("Ask"):
    if not question:
        st.warning("Please enter a question.")
    elif rag.collection is None:
        st.warning("Please upload a document first.")
    else:
        with st.spinner("Searching for answers..."):
            # Retrieve the top matching chunks
            docs = rag.search(question, top_k=4)

            # Generate answer
            answer = gen.answer(question, docs)

            st.write("### Answer")
            st.write(answer)

            st.write("### Sources")
            for i, doc in enumerate(docs):
                with st.expander(f"Source {i+1}"):
                    st.write(doc)
