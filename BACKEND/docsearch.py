from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, Docx2txtLoader
from config import EMBEDDING_MODEL, DB_PATH
import os
import faiss
import numpy as np

def load_documents_from_folder(paths):
    docs = []
    for path in paths:
        if path.endswith(".pdf"):
            docs.extend(PyMuPDFLoader(path).load())
        elif path.endswith(".txt"):
            docs.extend(TextLoader(path).load())
        elif path.endswith(".docx"):
            docs.extend(Docx2txtLoader(path).load())
    return docs

def embed_and_save_docs(documents, persist_directory=DB_PATH):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(persist_directory)
    return True

def is_query_doc_relevant_faiss(query, top_k=3):
    faiss_index = faiss.read_index("vectorstore/db_faiss/index.faiss")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    query_vector = embeddings.embed_query(query)

    query_vector = np.array([query_vector], dtype=np.float32)
    D, I = faiss_index.search(query_vector, top_k) 
    max_sim = max(D[0])

    return max_sim


def load_vector_db(persist_directory=DB_PATH):
    index_path = "vectorstore/db_faiss/index.faiss"
    pkl_path = "vectorstore/db_faiss/index.pkl"
    if not (os.path.exists(index_path) and os.path.exists(pkl_path)):
        return None 
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return FAISS.load_local(persist_directory, embeddings, allow_dangerous_deserialization=True)


def retrieve_docs(query, k=3):
    db = load_vector_db()
    if db is None:
        return None
    results = db.similarity_search(query, k=k)
    if not results:
        return None
    return "\n".join([doc.page_content for doc in results])