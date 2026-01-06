import os
import requests
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Set Pinecone API key
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


# Set OpenRouter API key
OPEN_ROUTER_KEY = os.environ.get("OPEN_ROUTER_KEY")
os.environ["OPEN_ROUTER_KEY"] = OPEN_ROUTER_KEY



embeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')
index_name = "financecore-ai"
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(index_name)


def load_pdf_file(data):
    loader = DirectoryLoader(data,
                            glob="*.pdf", 
                            loader_cls=PyPDFLoader)
    
    documents = loader.load()
    return documents



def text_split(extracted_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks



def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')
    return embeddings



#----------------------------------------------------------

def retrieve_context(query, top_k=4):

    # change the text "query" to embedding vector
    query_vector = embeddings.embed_query(query)
    
    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )
    print(results)

    if not results["matches"]:
        return ""

    context = "\n\n".join(
        match["metadata"].get("text", "")
        for match in results["matches"]
    )

    return context



#----------------------------------------------------------


def generate_finance_answer(query, context):

    URL = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPEN_ROUTER_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "xiaomi/mimo-v2-flash:free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an educational finance assistant. "
                    "Answer ONLY using the provided context. "
                    "If not found, say 'Not found in documents'."
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{query}"
            }
        ],
        "temperature": 0.2
    }

    response = requests.post(URL, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]


