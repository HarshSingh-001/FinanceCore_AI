from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

import os

load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

print (PINECONE_API_KEY)
extracted_data = load_pdf_file('data/')
text_chunk = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

print("embeddings")
print(embeddings)

pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "financecore-ai"
existing_indexes = [i["name"] for i in pc.list_indexes()]


if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=384,   
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

docsearch = PineconeVectorStore.from_documents(
    documents=text_chunk,
    embedding=embeddings,
    index_name=index_name
    )