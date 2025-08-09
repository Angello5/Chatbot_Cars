import os
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

#local_path = "/home/pibezx/Documents/Proyectos/PaginaWeb_Automoviles/Chatbot_Cars/Volkswagen/FichaTecnica-Teramont-2024.txt"

loader = TextLoader(local_path, encoding = "utf-8")
data = loader.load()

#loader = UnstructuredPDFLoader(local_path)
#data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=100)
chunks = text_splitter.split_documents(data)


embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

persist_directory = "./db_chroma_autos"
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=persist_directory
)

llm = ChatOllama(model="mistral")

prompt_template = """Eres un asistente experto en vehículos. Responde la pregunta usando exclusivamente el contexto proporcionado.
Contexto:
{context}

Pregunta: {question}
Respuesta en español:"""


prompt = ChatPromptTemplate.from_template(prompt_template)

# Configurar cadena de RAG (retrieval-augmented generation)
chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(search_kwargs={"k": 4}),
    chain_type_kwargs={"prompt": prompt}
)

while True:

    user_prompt = input('Pibinho: ')
    if user_prompt.lower() == 'gudbai':
        print("Chau")
        break
    resultado = chain.invoke(user_prompt)
    print(resultado)

print("CHAUUUUU")
