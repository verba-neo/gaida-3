"""
하이브리드 검색 결과 재랭킹 (Cross-Encoder Reranker)
========================================================

LangChain 1.0+ 기준 import 경로:
- ContextualCompressionRetriever: langchain_classic.retrievers.contextual_compression
- CrossEncoderReranker: langchain_classic.retrievers.document_compressors
- HuggingFaceCrossEncoder: langchain_community.cross_encoders (변경 없음)

왜 재랭킹이 필요한가:
- EnsembleRetriever(BM25 + Dense)는 RRF로 "순위"만 융합할 뿐, 실제 질문과
  문서 간의 세밀한 관련성을 직접 비교하지 않는다.
- Cross-Encoder는 (질문, 문서) 쌍을 함께 입력받아 관련성 점수를 직접 계산하므로
  훨씬 정밀하다. 다만 느려서, "1차로 넓게 뽑고(BM25+Dense) 2차로 정밀하게
  줄 세우는(rerank)" 2단계 구조로 쓰는 게 정석.

모델 선택: 이 문서가 한국어이므로 한국어를 지원하는 멀티링구얼 리랭커 필요.
BAAI/bge-reranker-v2-m3 (다국어 지원, 한국어 포함)를 사용.

설치:
    uv add langchain-classic langchain-community sentence-transformers torch
"""

from langchain_classic.retrievers.contextual_compression import (
    ContextualCompressionRetriever,
)
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

try:
    from src.hybrid_retriever import load_hybrid_retriever
except ModuleNotFoundError:
    from hybrid_retriever import load_hybrid_retriever


def build_reranked_retriever(
    top_n: int = 5,
    reranker_model: str = "BAAI/bge-reranker-v2-m3",
) -> ContextualCompressionRetriever:
    """
    1단계: EnsembleRetriever(BM25 + Dense)로 넓게 후보를 뽑고 (예: 각 5~10개)
    2단계: Cross-Encoder가 (질문, 문서) 쌍을 직접 비교해서 top_n개로 압축
    """
    hybrid_retriever = load_hybrid_retriever(dense_k=10, sparse_k=10)  # 1단계: 넉넉히 후보 확보

    cross_encoder = HuggingFaceCrossEncoder(model_name=reranker_model)
    reranker = CrossEncoderReranker(model=cross_encoder, top_n=top_n)

    reranked_retriever = ContextualCompressionRetriever(
        base_compressor=reranker,
        base_retriever=hybrid_retriever,
    )
    return reranked_retriever


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    retriever = build_reranked_retriever(top_n=3)

    query = "AI 반도체 시장에서 엔비디아 점유율은 어느 정도야?"
    print(f"[질문] {query}\n")

    results = retriever.invoke(query)
    for rank, doc in enumerate(results, start=1):
        print(f"[{rank}위] type={doc.metadata.get('type')} | {doc.metadata.get('h2', '')}")
        print(doc.page_content[:200])
        print("-" * 60)