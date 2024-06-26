import openai
import json
import os
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List,Dict

app = FastAPI()


# Load and process files function
def load_and_process_files(file_paths):
    documents = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            documents.append(Document(page_content=content))
    return documents

# File paths
file_paths = [
    "/home/codezeros/Documents/beautifulsoup/output/hdfc_open account.txt",
    "/home/codezeros/Documents/beautifulsoup/output/hdfc_nri_account.txt",
    "/home/codezeros/Documents/beautifulsoup/output/hdfc_loan.txt",
    "/home/codezeros/Documents/beautifulsoup/output/fixed_deposit.txt",
    "/home/codezeros/Documents/beautifulsoup/output/debit_card.txt",
    "/home/codezeros/Documents/beautifulsoup/output/credit_card.txt"
]

# Load and process raw data
raw_data = load_and_process_files(file_paths)

# Split documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0)
documents = text_splitter.split_documents(raw_data)

# Create embeddings for the documents
embeddings = OpenAIEmbeddings()
document_texts = [doc.page_content for doc in documents]
document_embeddings = embeddings.embed_documents(document_texts)

# Store the embeddings in a FAISS vector store
vector_store = FAISS.from_texts(texts=document_texts, embedding=embeddings)

# Function to query the vector store
def query_vector_store(query, k=5):
    retriever = vector_store.as_retriever(k=k)
    results = retriever.invoke(query)
    return results

# Function to get recommendations from the OpenAI API
def get_recommendations(query, retrieved_documents, chathistory, k=3):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
        {"role": "system", "content": f'''
            "You are a HDFC bank customer chatbot." 
            "If the user greets or makes a general statement, respond directly without retrieving documents."
            "For any bank-related questions, first check the retrieved documents and chat history for the answer."
            "when user ask non bank related question then your answer display is i am sorry this question not related to bank. please ask another question regarding to bank."
            "You are smart and intelligent about bank data so please answer based on that."
            "you have search only retrieved document when user ask query."
        '''},
        {"role": "user", "content": f"Retrieved documents are here: {retrieved_documents} \n Chathistory: {chathistory} \n User Question: {query}"}
    ]  
    )
    best_sentence = response['choices'][0]['message']['content']
    return best_sentence

# Function to save conversation to a JSON file
def save_conversation_to_json(conversation, filename='conversation_log.json'):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    # Check if the initial welcome message exists
    initial_message_exists = any(
        isinstance(conv, list) and conv and conv[0].get("role") == "system" and conv[0].get("content") == "Welcome to Customer Support Chatbot!"
        for conv in data
    )

    if not initial_message_exists:
        initial_conversation = [
            {"role": "system", "content": "Welcome to Customer Support Chatbot!"},
            {"role": "assistant", "content": "Hello! How can I assist you?"}
        ]
        data.append(initial_conversation + conversation)
    else:
        # Only append user conversation after the initial greeting
        data.append(conversation)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Pydantic model for request body
class ChatRequest(BaseModel):
    user_input: str
    chathistory: List[Dict[str, str]] = []

# Endpoint for chatbot interaction
@app.post("/Customer Support Chatbot")
async def chat(request: ChatRequest):
    user_input = request.user_input
    chathistory = request.chathistory

    conversation = []
    if user_input.lower() in ['exit']:
        return {"response": "Thank you. Goodbye!"}
    else:
        # Check in chathistory first
        if user_input.lower() in [entry['user_input'].lower() for entry in chathistory]:
            # Retrieve previous response from chathistory
            previous_entry = next(entry for entry in chathistory if entry['user_input'].lower() == user_input.lower())
            response = previous_entry['assistant_response']
            return {"response": response}
        else:
            similar_docs = query_vector_store(user_input)
            retrieved_documents = ""
            valid_documents = ""

            if similar_docs:
                for doc in similar_docs:
                    retrieved_documents += doc.page_content + "\n"
                    if len(doc.page_content) > 20:
                        valid_documents += doc.page_content + "\n"

            if len(valid_documents) >= 50:
                response = get_recommendations(user_input, valid_documents, chathistory)
                conversation.append({"role": "assistant", "content": response})
            else:
                response = "I'm sorry, but I couldn't find any related documents. Please ask another question."
                conversation.append({"role": "assistant", "content": response})

            # Save the user query and assistant response in chathistory
            chathistory.append({
                'user_input': user_input,
                'assistant_response': response
            })

            save_conversation_to_json(conversation)

            return {"response": response}


    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
