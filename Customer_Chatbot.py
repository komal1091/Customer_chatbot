import os
import openai
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import json
import streamlit
from dotenv import load_dotenv



load_dotenv()
openai.api_key = "sk-proj-5HIMqYMAxjsJDdPmxzm7T3BlbkFJifATym3GXlDPYSmS2AMu"


def get_recommendations(query, db, k=3):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    best_sentence = response['choices'][0]['message']['content']
    return best_sentence

def save_conversation_to_json(conversation, filename='conversation_log.json'):
    with open(filename, 'r') as file:
        data = json.load(file)

    #new = conv
    data.append(conversation)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def chatbot():
    conversation = []
    print("Welcome to Customer Support Chatbot")
    print("Chatbot: Hello! How can I assist you?")
    conversation.append({"role": "system", "content": "Welcome to Customer Support Chatbot!"})
    conversation.append({"role": "assistant", "content": "Hello! How can I assist you?"})
    save_conversation_to_json(conversation)
    
    while True:
        user_input = input("User: ")
        conversation.append({"role": "user", "content": user_input})
        
        if user_input.lower() in ['exit']:
            print("User: Thank you. Goodbye!")
            conversation.append({"role": "user", "content": "Thank you. Goodbye!"})
            save_conversation_to_json(conversation)
            break
        elif user_input.lower() == 'hello':
            print("User: Hello")
            print("Chatbot: How can I help you?")
            conversation.append({"role": "assistant", "content": "How can I help you?"})
        else:
            response = get_recommendations(user_input, db={})
            print(f"User: {user_input}")
            print(f"Chatbot: {response}")
            conversation.append({"role": "assistant", "content": response})
        
        save_conversation_to_json(conversation)

# Run the chatbot
if __name__ == "__main__":
    chatbot()




