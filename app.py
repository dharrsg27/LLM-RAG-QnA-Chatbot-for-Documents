import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from query import Query
from database_creation import CreateChromaDB

load_dotenv()

# Streamlit app layout
st.set_page_config(page_title="PDF Document Chatbot", page_icon=":book:")
st.title("PDF Document Chatbot")


# Initialize session state
def initialize_session_state():
    if 'db_created' not in st.session_state:
        st.session_state.db_created = False
    if 'db' not in st.session_state:
        st.session_state.db = None
    if 'chroma_path' not in st.session_state:
        st.session_state.chroma_path = None
    if 'pdf_path' not in st.session_state:
        st.session_state.pdf_path = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = []


# Handle PDF upload
def handle_file_upload():
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        if not st.session_state.chroma_path:
            st.session_state.chroma_path = tempfile.mkdtemp()
        if not st.session_state.pdf_path:
            st.session_state.pdf_path = tempfile.mkdtemp()

        tmp_chroma_path = st.session_state.chroma_path
        tmp_pdf_path = st.session_state.pdf_path

        new_files_uploaded = False
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.processed_files:
                new_files_uploaded = True
                save_uploaded_file(uploaded_file, tmp_pdf_path)

        if new_files_uploaded:
            update_database(tmp_pdf_path, tmp_chroma_path)

        return uploaded_files


# Save uploaded file to temporary directory
def save_uploaded_file(uploaded_file, tmp_pdf_path):
    file_path = os.path.join(tmp_pdf_path, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.session_state.processed_files.append(uploaded_file.name)


# Update ChromaDB with new files
def update_database(tmp_pdf_path, tmp_chroma_path):
    status_placeholder = st.empty()
    status_placeholder.write("Adding new files to database...")

    if not st.session_state.db_created:
        create_db = CreateChromaDB(pdf_path=tmp_pdf_path, chroma_path=tmp_chroma_path)
        st.session_state.db_created = True
    else:
        create_db = st.session_state.db

    documents = create_db.load_documents()
    chunks = create_db.split_text(documents)
    create_db.add_to_chroma(chunks)

    st.session_state.db = create_db
    status_placeholder.write("New documents added to ChromaDB!")


# Query processing
def process_query(query_instance):
    if st.session_state.db_created:
        if prompt := st.text_input("Enter your query:", key="query_input"):
            response, sources = query_instance.query(prompt)
            st.session_state.chat_history.insert(0, {"role": "assistant", "content": response['answer']})
            st.session_state.chat_history.insert(0, {"role": "user", "content": prompt})
    else:
        st.error("Please upload and process documents first.")


# Display chat history
def display_chat_history():
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            st.chat_message(message["role"]).markdown(message["content"])


# Main function to run the app
def main():
    initialize_session_state()
    uploaded_files = handle_file_upload()

    if uploaded_files:
        query_instance = Query(pdf_path=st.session_state.pdf_path, chroma_path=st.session_state.chroma_path)
        process_query(query_instance)

    display_chat_history()


# CSS for layout
def set_layout():
    st.markdown("""
        <style>
        .input-container {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 10px;
            z-index: 1000;
        }
        .chat-container {
            margin-top: 70px;
            height: calc(100vh - 70px);
            overflow-y: auto;
        }
        </style>
    """, unsafe_allow_html=True)


# Run the layout and the app
if __name__ == "__main__":
    set_layout()
    main()
