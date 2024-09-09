# LLM-RAG-QnA-Chatbot-for-Documents
## Project Description
### Tech Stack
1. LangChain: A powerful framework for working with Large Language Models (LLMs)
2. Ollama: A tool that allows open-source LLMs to be run locally
3. Groq Cloud: A service that allows running LLMs through their cloud platform
4. ChromaDB: A vector database that allows storage and retrievals of vector embeddings
5. Streamlit: A web framework for data scientists and AI/ML engineers to deliver interactive data apps
### Principles of RAG
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
     
