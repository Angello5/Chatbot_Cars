import os
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

local_path = "/home/pibezx/Documents/Proyectos/PaginaWeb_Automoviles/Chatbot_Cars/Toyota/CATALOGO_4RUNNER_PERU_0.pdf"
loader = UnstructuredPDFLoader(local_path)
data = loader.load()

data[0].page_content

text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=100)
chunks = text_splitter.split_documents(data)


embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

persist_directory = "./db_chroma_autos"
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=persist_directory
)

llm = ChatOllama(model="deepseek-r1:8b")

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
    retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
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
