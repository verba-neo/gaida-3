"""
청킹 -> 하이브리드(Dense + BM25) 저장/로드
============================================

LangChain 1.0+ 기준 import 경로 (langchain.retrievers는 1.0에서 제거됨):
- EnsembleRetriever: langchain_classic.retrievers (레거시 패키지로 이동)
- BM25Retriever: langchain_community.retrievers (변경 없음)
- Chroma: langchain_chroma (변경 없음)

BM25는 자체 영속화(persist) 기능이 없으므로, 청크 Document 리스트를
pickle로 저장해뒀다가 로드 시점에 BM25 인덱스를 재구성한다.
(BM25 인덱싱은 임베딩 API 호출이 없어 재구성 비용이 매우 낮음)

설치:
    pip install langchain-classic langchain-community langchain-chroma langchain-openai rank_bm25 kiwipiepy

환경변수:
    OPENAI_API_KEY 필요 (Dense 임베딩용)
"""


import pickle
from pathlib import Path

from langchain_chroma import Chroma
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from load_split import process_llamaparse_markdown

try:
    from kiwipiepy import Kiwi

    _kiwi = Kiwi()
    _HAS_KIWI = True
except ImportError:
    _HAS_KIWI = False


# --------------------------------------------------------------------------
# 한국어 형태소 토크나이저 (BM25 전처리용 — 조사/어미 제거 후 핵심 형태소만 추출)
# --------------------------------------------------------------------------


def korean_tokenizer(text: str) -> list[str]:
    if not _HAS_KIWI:
        return text.split()
    return [
        token.form
        for token in _kiwi.tokenize(text)
        if token.tag.startswith(("NN", "VV", "VA", "SL", "SN"))
    ]


# --------------------------------------------------------------------------
# 1. 청킹 -> 하이브리드 저장
# --------------------------------------------------------------------------


def build_and_save_hybrid_store(
    markdown_path: str,
    source_name: str,
    persist_dir: str = "./chroma_db",
    bm25_docs_path: str = "./bm25_docs.pkl",
) -> None:
    with open(markdown_path, encoding="utf-8") as f:
        markdown_text = f.read()

    # 1) 기존 청킹 파이프라인 그대로 사용 (표/다이어그램/텍스트 타입별 분리)
    docs: list[Document] = process_llamaparse_markdown(markdown_text, source_name=source_name)

    # 2) Dense: Chroma에 영속화 (persist_directory 지정 시 자동으로 디스크에 저장됨)
    Chroma.from_documents(
        documents=docs,
        embedding=OpenAIEmbeddings(),
        persist_directory=persist_dir,
    )

    # 3) Sparse(BM25)용 원본 청크를 pickle로 저장
    #    -> BM25는 자체 저장 API가 없어서, 로드 시 이 pickle로 인덱스를 재구성함
    with open(bm25_docs_path, "wb") as f:
        pickle.dump(docs, f)

    print(f"저장 완료: Chroma -> {persist_dir}, BM25용 청크 -> {bm25_docs_path} (총 {len(docs)}개)")


# --------------------------------------------------------------------------
# 2. 저장된 것 로드 -> 하이브리드 리트리버 재구성
# --------------------------------------------------------------------------


def load_hybrid_retriever(
    persist_dir: str = "./chroma_db",
    bm25_docs_path: str = "./bm25_docs.pkl",
    dense_weight: float = 0.5,
    sparse_weight: float = 0.5,
    dense_k: int = 5,
    sparse_k: int = 5,
) -> EnsembleRetriever:
    # Dense: 디스크에서 그대로 로드 (재임베딩 없음 -> 비용/시간 절약)
    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=OpenAIEmbeddings(),
    )
    dense_retriever = vectorstore.as_retriever(search_kwargs={"k": dense_k})

    # Sparse: pickle에서 청크를 불러와 BM25 인덱스 재구성 (API 호출 없어 빠름)
    with open(bm25_docs_path, "rb") as f:
        docs: list[Document] = pickle.load(f)

    sparse_retriever = BM25Retriever.from_documents(docs, preprocess_func=korean_tokenizer)
    sparse_retriever.k = sparse_k

    return EnsembleRetriever(
        retrievers=[sparse_retriever, dense_retriever],
        weights=[sparse_weight, dense_weight],
    )


# --------------------------------------------------------------------------
# 실행 예시
# --------------------------------------------------------------------------

if __name__ == "__main__":
    from 

    markdown_path = Path(__file__).parent / "parsed_data" / "output.md"

    # 최초 1회: 청킹 + 하이브리드 저장
    build_and_save_hybrid_store(
        markdown_path=str(markdown_path),
        source_name="NIA_2026_trends.pdf",
    )

    # 이후: 저장된 것만 로드해서 바로 검색 (재파싱/재임베딩 없음)
    hybrid_retriever = load_hybrid_retriever()

    query = "글로벌 AI 반도체 시장 규모 2026년 전망"
    print(f"\n[질문] {query}")
    for doc in hybrid_retriever.invoke(query)[:3]:
        print("-" * 60)
        print(doc.metadata.get("type"), "|", doc.metadata.get("h2", ""))
        print(doc.page_content[:200])