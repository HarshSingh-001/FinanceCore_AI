# FinanceCore-AI

FinanceCore-AI is a domain-specific AI assistant focused on answering finance-related questions using retrieval-augmented generation (RAG).  
The project is designed to explore how large language models can be integrated with embeddings and contextual retrieval to produce accurate and grounded responses.


## Project Objective

The primary objective of this project is to:
- Build a finance-focused AI assistant
- Implement context-aware question answering
- Understand retrieval-augmented generation (RAG)
- Design a backend API for AI workflows
- Integrate frontend and backend in an AI-driven system



## Key Features

- Finance-specific question answering  
- Retrieval-Augmented Generation (RAG) pipeline  
- Embedding-based semantic search  
- Flask-based backend API  
- Simple and clean web chat interface  
- Modular and extensible architecture  



## Tech Stack

### Backend
- Python  
- Flask  
- LangChain  
- OPENROUTER 
- Sentence Transformers  

### Frontend
- HTML  
- CSS  
- JavaScript  



## How It Works

1. User submits a finance-related query  
2. Relevant context is retrieved using embeddings  
3. Context is combined with the user query  
4. Google Gemini generates a response based on retrieved data  
5. Response is returned through the Flask API  


## Installation & Setup

### Setup 
```bash
git clone https://github.com/your-username/FinanceCore-AI.git
cd FinanceCore-AI

conda create financebot
cont activate financebot

pip install -r requirements.txt

python app.py

```

### youtube video
https://www.youtube.com/watch?v=TxWXbK1uUuk





