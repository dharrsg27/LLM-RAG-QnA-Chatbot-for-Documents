# LLM-RAG-QnA-Chatbot-for-Documents
## Project Description
### Tech Stack
![Static Badge](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=ffffff)
![Static Badge](https://img.shields.io/badge/Ollama-34363b?style=for-the-badge&logo=ollama&logoColor=ffffff)
![Static Badge](https://img.shields.io/badge/GroqCloud-d17021?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/ChromaDB-0378a6?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/Streamlit-%23FF4B4B?style=for-the-badge&logo=streamlit&logoColor=ffffff)
### Introduction to RAG
Retrieval-Augmented Generation (RAG) is an AI architecture that combines the strengths of information retrieval and generative language models. The main problem with traditional language models is that it generates text based on its training data which means that they may struggle when asked for domain-specific or recent information. By augmenting these models with a retrieval mechanism, RAG enhances the quality and accuracy of responses by fetching relevant documents or facts from given external sources.

### RAG Project Workflow
The workflow of a general RAG pipeline can be seen below:
![image](https://github.com/user-attachments/assets/889fd5db-cc35-434b-b3cc-5229a1bc4775)
<p align="center">Source: https://blog.griddynamics.com/retrieval-augmented-generation-llm/</p>

A. Vector Database Creation
1. Loading Documents

   - PDF documents can be uploaded to the streamlit app
   - LangChain provides convenient functions such as PyPDFDirectoryLoader to easily load PDF documents from a given directory and extract the texts as well

2. Chunking

   - Chunking is the process of dividing the documents to be retrieved, into smaller, manageable segments or chunks.
   - Chunking allows for more efficient retrieval algorithms by focusing on smaller, more relevant parts of the document. Instead of searching through an entire document, the retrieval mechanism can look for the most relevant chunk, improving the accuracy and relevance of the retrieved context.
   - In this project, LangChain's RecursiveCharacterTextSplitter can be used to split the documents into chunks with a specified size and overlap

3. Vector Embeddings of Chunks

   - After chunking, each chunk is converted into a vector embedding, which is a numerical representation of the text. These embeddings capture the meaning, context, and relationships between words within a chunk.
   - By converting chunks into embeddings, similar chunks can be quickly found during queries using techniques like cosine similarity, which is significantly faster than performing direct text searches.
   - In this project, Ollama's embedding model, 'nomic-embed-text', was used for vector embeddings.

4. Storing Embeddings in a Vector Database

   - Vector databases like ChromaDB are optimized to store and retrieve high-dimensional vector embeddings. Once text chunks are converted into vector embeddings, these databases can efficiently perform similarity searches using metrics like cosine similarity. This is crucial for tasks like information retrieval, where we want to find chunks of text similar to a user's query.
   - Each chunk has a unique ID so it can be easily tracked and retrieved later, such as in this project, the IDs were formatted as "file_name:page:chunk_ids"

B. Document Retrieval from Query and Answer Generation
1. Vectorize Question
   
   - When a user submits a question, it is also vectorized, meaning it’s transformed into an embedding using the same embedding model that was used for the document chunks.

2. Retrieve Most Relevant Document Chunks from Question Embedding
   
   - Similarity search is performed in the vector database, comparing the question embedding with the stored document chunk embeddings.
   - It retrieves the document chunks most similar to the query, identified by their unique IDs.

3. Document Chunk IDs to Retrieve Document Chunks from Storage:

   - Using the retrieved chunk IDs, the corresponding document chunks are fetched from storage. These chunks contain the textual content that is semantically relevant to the question.

4. Answer Generation

   - A prompt was previously defined and given the LLM on what to do when given the context and question
   - The system combines the retrieved document chunks as context and the user’s question to formulate a response based on the context provided.

## Setup
1. Clone this repository
2. Create a Python virtual environment
   ```
   python3 -m venv .venv
   ```
3. Activate the virtual environment
   - For MacOS users:
     ```
     source .venv/bin/activate
     ```
   - For Windows users:
     ```
     .\venv\Scripts\activate
     ```
4. Install `onnxruntime` for `chromadb` dependency:
   - For MacOS users:
     ```
     conda install onnxruntime -c conda-forge
     ```
   - For Window users: Install the Microsoft C++ Build Tools and follow this guide
5. Install dependenies in the `requirements.txt` file:
   ```
   pip install -r requirements.txt
   ```
6. Install markdown depenendies:
   ```
   pip install "unstructured[md]"
   ```
7. Set up a Groq Cloud account:
   - Create an account in their [website](https://console.groq.com/login)
   - Go to the API Keys sections
   - Press "Create API Key"
   - Copy the API key and paste it to the .env file
8. Download [Ollama](ollama.com)
   - Pull the embedding model in terminal
     ```
     ollama pull nomic-embed-text
     ```
## Running the Streamlit Application
`cd` into the directory where you clone this repository and input the following code in your terminal
```
streamlit run app.py
```
     
