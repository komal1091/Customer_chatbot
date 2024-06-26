import openai
import json
import os
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings



# Function to load and process files
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
embeddings = OpenAIEmbeddings(openai_api_key = OPENAI_API_KEY)
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
            {"role": "system", "content": (
                "You are a HDFC bank customer chatbot."
                "when user some question about bank related then retrieved documents search first then display related answer to user ask question."
                "when user ask non bank related question then your answer display is i am sorry this question not related to bank. please ask another question regarding to bank."
                "when sometimes bank server down then use ask query You display that query answer is i am sorry bank server unavailable. please try again later."
                "You are smart and intelligent about bank data so please answer display only bank related question."
                "you have search only retrieved document when user ask query."
                "when retrieved documents are not found some user query answer that you display answer as simple i am sorry. i don't get this type of question."
                "when second time user ask query then first check chathistory and after check retrived documents then display answer."
                "user ask another question that is not related bank that time you should change your answer and display answer is This is not a banking retaled question please ask only banking related question."
                "when user ask any question then check conversion data and also chathistory check and then after assistant display answer on user query."

                
            )},
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

# Main chatbot function
def chatbot():
    conversation = []
    chathistory = []  # Initialize chat history
    user_name = None  # Initialize user's name
    
    print("Welcome to Customer Support Chatbot!")
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
            break
        elif user_name is None and "my name is " in user_input.lower():
            user_name = user_input.split("my name is ", 1)[1].strip()
            print(f"User: {user_input}")
            print(f"Chatbot: Welcome {user_name}! How can I assist you?")
            conversation.append({"role": "assistant", "content": f"Welcome {user_name}! How can I assist you?"})
        elif "what is my name" in user_input.lower():
            if user_name:
                print(f"User: {user_input}")
                print(f"Chatbot: Your name is {user_name}. How else can I help?")
                conversation.append({"role": "assistant", "content": f"Your name is {user_name}. How else can I help?"})
            else:
                print(f"User: {user_input}")
                print(f"Chatbot: I'm sorry, I don't know your name yet. How can I assist you?")
                conversation.append({"role": "assistant", "content": "I'm sorry, I don't know your name yet. How can I assist you?"})
        elif user_input.lower() == 'hello':
            print("User: Hello")
            print("Chatbot: How can I help you?")
            conversation.append({"role": "assistant", "content": "How can I help you?"})
        else:
            # Check in chathistory first
            if user_input.lower() in [entry['user_input'].lower() for entry in chathistory]:
                # Retrieve previous response from chathistory
                previous_entry = next(entry for entry in chathistory if entry['user_input'].lower() == user_input.lower())
                response = previous_entry['assistant_response']
                print(f"User: {user_input}")
                print(f"Chatbot: {response}")
                conversation.append({"role": "assistant", "content": response})
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
                    print(f"User: {user_input}")
                    print(f"Chatbot: {response}")
                    conversation.append({"role": "assistant", "content": response})
                else:
                    print("Query Results: no related documents found")
                    response = "I'm sorry, but I couldn't find any related documents. Please ask another question."
                    print(f"Chatbot: {response}")
                    conversation.append({"role": "assistant", "content": response})
                
                # Save the user query and assistant response in chathistory
                chathistory.append({
                    'user_input': user_input,
                    'assistant_response': response
                })

    save_conversation_to_json(conversation)

# Run the chatbot
if __name__ == "__main__":
    chatbot()
