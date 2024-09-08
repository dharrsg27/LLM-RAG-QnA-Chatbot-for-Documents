from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma


class CreateChromaDB:
    def __init__(self, pdf_path=None, chroma_path=None):
        self.PDF_PATH = pdf_path
        self.CHROMA_PATH = chroma_path

    def load_documents(self):
        document_loader = PyPDFDirectoryLoader(self.PDF_PATH)
        documents = document_loader.load()
        print("Documents Loaded Successfully")
        return documents

    def split_text(self, documents: list[Document]):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True,
        )

        chunks = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

        return chunks

    def get_embedding_function(self):
        embeddings = OllamaEmbeddings(
            model='nomic-embed-text'
        )
        return embeddings

    def create_chunk_ids(self, chunks):

        # Creates ids of chunks in the format "fileName:page:chunkIndex"
        last_page_id = None
        current_chunk_index = 0

        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"

            # If the page ID is the same as the last one, increment the index.
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            # Calculate the chunk ID.
            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id

            # Add it to the page meta-data.
            chunk.metadata["id"] = chunk_id

        return chunks

    def add_to_chroma(self, chunks: list[Document]):

        # Load the existing database.
        db = Chroma(
            persist_directory=self.CHROMA_PATH, embedding_function=self.get_embedding_function()
        )

        # Calculate Page IDs.
        chunks_with_ids = self.create_chunk_ids(chunks)

        # Add or Update the documents.
        existing_items = db.get(include=[])  # IDs are always included by default
        existing_ids = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")

        # Only add documents that don't exist in the DB.
        new_chunks = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks) > 0:
            print(f"Adding {len(new_chunks)} new documents to the Chroma vectorstore.")
            db.add_documents(new_chunks, ids=[chunk.metadata["id"] for chunk in new_chunks])
            db.persist()
            existing_items = db.get(include=[])  # IDs are always included by default
            existing_ids = set(existing_items["ids"])
            print(f"Number of existing documents in DB: {len(existing_ids)}")
        else:
            print("No new documents to add.")


if __name__ == "__main__":
    createDB = CreateChromaDB()