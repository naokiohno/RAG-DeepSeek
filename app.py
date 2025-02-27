
'''
This script was written in Python version 3.12. For best reproducibility, create a fresh virtual environment (venv)
specifically for this project, and install requirements.txt using pip.
'''

# Load libraries
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
import os
import openai

def check_for_api_key():
    if os.environ["DEEPSEEK_API_KEY"] == "":
        api_key = input("API key not found in environmental variables. Please enter your DeepSeek API key: ")
        os.environ["DEEPSEEK_API_KEY"] = api_key
    else:
        print("API Key found")

def authenticate_api_key():
    client = openai.OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
    client.models.list()
    try:
        client.models.list()
    except openai.AuthenticationError:
        raise ValueError("Authentication error. Make sure you're using a valid API key")
    else:
        print("Successful authentication")

def create_file_paths(folder_path):
    dir_list = os.listdir(folder_path)
    full_dir_list = []
    for i in range(len(dir_list)):
        full_dir_list.append(folder_path + dir_list[i])
    return full_dir_list

def load_and_split_multiple_files(list_of_file_paths):
    output = []
    for i in range(len(list_of_file_paths)):
        loader = PyPDFLoader(list_of_file_paths[i])
        pages = loader.load_and_split()
        output.extend(pages)
    return output

def make_query(query_string):
    result = conversation_chain({"question": query_string})
    answer = result["answer"]
    print("The answer is:\n" + answer)


# Check, set, and authenticate API key
check_for_api_key()
# authenticate_api_key()

# Load and process data.
pdf_file_path = 'data/cv_pdf_files/'
full_pdf_file_paths = create_file_paths(pdf_file_path)
final_pages = load_and_split_multiple_files(full_pdf_file_paths)

# We're still using an OPENAI embedding.
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(final_pages, embedding=embeddings)

# Langchain DeepSeek API documentation
# https://python.langchain.com/api_reference/deepseek/chat_models/langchain_deepseek.chat_models.ChatDeepSeek.html

# Create model
llm = ChatDeepSeek(model_name="deepseek-chat")
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    memory=memory
)

# Make example queries
make_query('Are you a deepseek model?')
make_query('Who in the context is best qualified for a Java programmer role?')
make_query('Who in the context has more Python experience?')
make_query('Who in the context has the most management experience?')
make_query('Who in the context has the most data science experience?')
