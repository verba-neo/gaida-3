from langchain_core.tools import tool

from src.vectorstore import googl_vectorstore

@tool
def search_google_10k(query: str):
    """Retrieve info from GOOGLE 10-k report 2025 to help answer a query about """
    docs = googl_vectorstore.similarity_search(query, k=5)
    result = '----------------------\n\n'.join(map(lambda doc: doc.page_content, docs))
    return result
