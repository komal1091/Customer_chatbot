import os
import openai
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

os.environ["OPENAI_API_KEY"] = "sk-proj-5HIMqYMAxjsJDdPmxzm7T3BlbkFJifATym3GXlDPYSmS2AMu"

def load_and_process_files(file_paths):
    all_documents = []
    for file_path in file_paths:
        loader = TextLoader(file_path)
        documents = loader.load()
        all_documents.extend(documents)
    return all_documents

file_paths = [
    "/home/codezeros/Documents/beautifulsoup/output/output.txt",
    "/home/codezeros/Documents/beautifulsoup/output/ai_for_ecommerce.txt", 
    "/home/codezeros/Documents/beautifulsoup/output/ai_ticketing.txt"
    ]
raw_data = load_and_process_files(file_paths)

print("Loaded document content:", raw_data)

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)  
documents = text_splitter.split_documents(raw_data)

print(f"Number of documents: {len(documents)}")

embedding = OpenAIEmbeddings()
db = FAISS.from_documents(documents, embedding)

def get_recommendations(query, db, k=3):
    docs = db.similarity_search(query, k=k)  

    print(f"Retrieved {len(docs)} documents for query: {query}")

    relevant_sentences = []
    for doc in docs:
        content = doc.page_content
        sentences = content.split('.')  
        for sentence in sentences:
            if query.lower() in sentence.lower():
                relevant_sentences.append(sentence.strip())

    if relevant_sentences:
        best_sentence = max(relevant_sentences, key=lambda s: len(s)) 
    else:
        best_sentence = "No relevant sentence found."

    return best_sentence

def chatbot():
    print("Welcome to the Personalized Content Recommendation System!")
    print("Chatbot: How can I assist you?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit']:
            print("Chatbot: Goodbye!")
            break
        
        elif user_input.lower() == 'hello':
            print("Chatbot: How can I help you?")
        else:
            response = get_recommendations(user_input, db)
            print(f"Chatbot: {response}.")

if __name__ == "__main__":
    chatbot()
