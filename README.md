# LLM-RAG-QnA-Chatbot-for-Documents
## Project Description
### Tech Stack
![Static Badge](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=ffffff&link=https%3A%2F%2Fwww.langchain.com%2F)
![Static Badge](https://img.shields.io/badge/Ollama-34363b?style=for-the-badge&logo=ollama&logoColor=ffffff&link=https%3A%2F%2Follama.com%2F)
![Static Badge](https://img.shields.io/badge/GroqCloud-d17021?style=for-the-badge&link=https%3A%2F%2Fconsole.groq.com%2Flogin)
![Static Badge](https://img.shields.io/badge/ChromaDB-0378a6?style=for-the-badge&link=https%3A%2F%2Fwww.trychroma.com%2F)
![Static Badge](https://img.shields.io/badge/Streamlit-%23FF4B4B?style=for-the-badge&logo=streamlit&logoColor=ffffff&link=https%3A%2F%2Fstreamlit.io%2F)
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
     
