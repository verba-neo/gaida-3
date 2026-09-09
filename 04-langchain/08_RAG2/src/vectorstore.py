# src/vectorstore.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

print('***********Vectore Setting************')
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True  # 쪼개진 chunk 의 시작 index를 기록
)

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
# Google 
loader = PyPDFLoader('src/pdfs/GOOG-10-K-2025.pdf')
docs = loader.load()

chunks = text_splitter.split_documents(docs)
googl_vectorstore = InMemoryVectorStore(embedding=embeddings)

ids = googl_vectorstore.add_documents(documents=chunks)
print(len(ids))
print('**************************************')