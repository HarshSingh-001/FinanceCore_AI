from src.helper import retrieve_context, generate_finance_answer, download_hugging_face_embeddings
from flask import   Flask, request, jsonify, render_template
from langchain_pinecone import PineconeVectorStore
import requests
import os



print("Starting FinanceCore AI Chatbot...")
def finance_bot(query):
    context = retrieve_context(query)
    answer = generate_finance_answer(query, context)
    return answer


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({'answer': 'No message provided'}), 400

    user_query = data['message']
    print(f"User Query: {user_query}")

    answer = finance_bot(user_query)
    print(f"Generated Answer: {answer}")

    return jsonify({'answer': answer})



if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8080 ,debug=True)