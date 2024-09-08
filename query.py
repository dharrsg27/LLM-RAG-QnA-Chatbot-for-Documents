from langchain.vectorstores.chroma import Chroma
from langchain.prompts import PromptTemplate
from database_creation import CreateChromaDB
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


class Query:
    def __init__(self, pdf_path=None, chroma_path=None):
        self.CHROMA_PATH = chroma_path
        self.PDF_PATH = pdf_path

        self.promptTemplate = """
        You are a highly knowledgeable assistant tasked with answering questions based on the 
        following context:
        
        {context}
        
        Guidelines:
        1. If the answer to the question is directly found in the context, respond based only 
        on the content of the document.
        2. If the question is related to the document but not directly answered within it, use 
        your broader knowledge to provide an informed response, while indicating that the document 
        does not directly provide the answer.
        3. If the question is unrelated to the document, respond by saying: "I am unable to answer 
        this question based on the provided document."
        
        Now, based on the document above, please answer the following question:
        
        Question: {question}
        """

        createDB = CreateChromaDB(pdf_path=self.PDF_PATH, chroma_path=self.CHROMA_PATH)

        self.embedding_function = createDB.get_embedding_function()

        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def query(self, queryText: str):

        db = Chroma(persist_directory=self.CHROMA_PATH, embedding_function=self.embedding_function)

        results = db.similarity_search_with_score(queryText, k=5)
        retriever = db.as_retriever()

        prompt_template = PromptTemplate.from_template(self.promptTemplate)

        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={'prompt': prompt_template})

        textResponse = conversation_chain({"question": queryText})

        sources = [doc.metadata.get("id", None) for doc, _score in results]

        return textResponse, sources


if __name__ == "__main__":
    query = Query()