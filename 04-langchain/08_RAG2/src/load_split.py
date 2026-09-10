"""
LlamaParse 마크다운 출력물 청킹 파이프라인
============================================

대상 문서 특징:
- 표가 마크다운 파이프(|)가 아니라 HTML <table> 태그 (rowspan/colspan 포함)
- 다이어그램이 이미지가 아니라 ```mermaid 코드 블록 (텍스트 그래프 정의)
- "트렌드 N" 단위로 명확한 반복 섹션 구조 (## 헤더로 구분됨)

전략:
1. HTML <table> 블록을 pandas로 파싱 -> 마크다운 표로 재구성, 절대 쪼개지 않음
   (rowspan/colspan은 pandas가 forward-fill로 처리해줌)
2. ```mermaid 블록을 노드/엣지 파싱 -> 자연어 문장으로 변환
   (원본 mermaid 구문은 임베딩 검색에 비효율적이므로 그대로 넣지 않음)
3. 남은 텍스트는 MarkdownHeaderTextSplitter로 헤더 경계를 존중해서 분리
   -> "트렌드 N" 섹션이 쪼개지지 않고 하나의 의미 단위로 유지됨
4. 섹션이 너무 길면 RecursiveCharacterTextSplitter로 2차 분할

설치:
    uv add langchain-text-splitters langchain-core pandas lxml html5lib beautifulsoup4
"""

import io
import re
from pathlib import Path

import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

HTML_TABLE_PATTERN = r"<table>.*?</table>"
MERMAID_PATTERN = r"```mermaid\s*\n(.*?)```"


# --------------------------------------------------------------------------
# 1. HTML 표 추출 -> 마크다운으로 재구성 (rowspan/colspan 보존)
# --------------------------------------------------------------------------


def extract_tables(markdown_text: str, source_name: str) -> tuple[list[Document], str]:
    """
    HTML <table> 블록을 찾아서 pandas로 파싱 후 마크다운 표로 변환.
    pandas.read_html은 colspan/rowspan을 자동으로 forward-fill 처리해줘서
    단순 정규식으로 파이프 표를 만드는 것보다 구조 손실이 적다.
    """
    documents: list[Document] = []
    matches = list(re.finditer(HTML_TABLE_PATTERN, markdown_text, flags=re.DOTALL))

    for idx, match in enumerate(matches):
        html_table = match.group(0)
        try:
            dfs = pd.read_html(io.StringIO(html_table))
            table_md = dfs[0].to_markdown(index=False)
        except Exception:
            # 파싱 실패 시(예: 헤더 없는 표, tabulate 미설치 등) 원본 HTML을 그대로 보존
            # -> LLM이 HTML 표도 어느 정도 이해할 수 있으므로 정보 손실 방지
            table_md = html_table

        documents.append(
            Document(
                page_content=table_md,
                metadata={"source": source_name, "type": "table", "table_index": idx},
            )
        )

    # 표를 제거한 자리에 플레이스홀더를 남겨서, 이후 텍스트 분리 시
    # "표가 있었다"는 문맥이 완전히 끊기지 않도록 함
    table_idx = 0

    def _replace_table(m):
        nonlocal table_idx
        res = f"\n[표 {table_idx}: 아래 참고]\n"
        table_idx += 1
        return res

    remaining = re.sub(
        HTML_TABLE_PATTERN,
        _replace_table,
        markdown_text,
        flags=re.DOTALL,
    )
    return documents, remaining


# --------------------------------------------------------------------------
# 2. Mermaid 다이어그램 추출 -> 자연어 설명으로 변환
# --------------------------------------------------------------------------


def _parse_mermaid_graph(mermaid_code: str) -> str:
    """
    mermaid graph TD/LR 구문에서 노드 라벨과 엣지를 추출해 자연어 문장으로 변환.
    예: node1["인공지능"] --- node2["데이터"]
        -> "인공지능 -- 데이터" 관계로 자연어화
    """
    # 노드 정의 추출: node1["라벨"] 또는 node1[라벨]
    node_pattern = r'(\w+)\["?([^"\]]+)"?\]'
    nodes = dict(re.findall(node_pattern, mermaid_code))

    # 엣지 추출: node1 --- node2, node1 --> node2 등
    edge_pattern = r"(\w+)\s*(?:---|-->|-\.-|\|)+\s*(\w+)"
    edges = re.findall(edge_pattern, mermaid_code)

    if not nodes:
        return mermaid_code.strip()  # 파싱 실패 시 원본 반환

    relations = []
    for src, dst in edges:
        src_label = nodes.get(src, src)
        dst_label = nodes.get(dst, dst)
        relations.append(f"{src_label} - {dst_label}")

    node_list = ", ".join(nodes.values())
    description = f"다이어그램에 포함된 항목: {node_list}."
    if relations:
        description += f" 연결 관계: {'; '.join(relations)}."
    return description


def extract_diagrams(markdown_text: str, source_name: str) -> tuple[list[Document], str]:
    """mermaid 코드 블록을 찾아 자연어 설명 Document로 변환."""
    documents: list[Document] = []
    matches = list(re.finditer(MERMAID_PATTERN, markdown_text, flags=re.DOTALL))

    for idx, match in enumerate(matches):
        mermaid_code = match.group(1)
        description = _parse_mermaid_graph(mermaid_code)
        documents.append(
            Document(
                page_content=description,
                metadata={"source": source_name, "type": "diagram", "diagram_index": idx},
            )
        )

    remaining = re.sub(MERMAID_PATTERN, "\n[다이어그램: 아래 참고]\n", markdown_text, flags=re.DOTALL)
    return documents, remaining


# --------------------------------------------------------------------------
# 3. 나머지 텍스트: 헤더 기준 분리 (트렌드 경계 존중) + 2차 청킹
# --------------------------------------------------------------------------


def split_text_by_headers(
    markdown_text: str,
    source_name: str,
    max_chunk_size: int = 1200,
    chunk_overlap: int = 150,
) -> list[Document]:
    """
    ## 헤더 단위(트렌드 1, 트렌드 2, ...)로 먼저 분리해서 의미 단위를 보존.
    각 섹션이 너무 길면 RecursiveCharacterTextSplitter로 2차 분할하되,
    metadata에 원래 헤더(트렌드명)를 유지해서 어느 트렌드에서 나온 청크인지 추적 가능.
    """
    headers_to_split_on = [
        ("#", "h1"),
        ("##", "h2"),
        ("###", "h3"),
    ]
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False,  # 헤더 텍스트 자체도 청크 안에 남겨서 문맥 유지
    )
    header_sections = header_splitter.split_text(markdown_text)

    sub_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    documents: list[Document] = []
    for section in header_sections:
        content = section.page_content.strip()
        if not content:
            continue

        header_meta = section.metadata  # {"h1": ..., "h2": "트렌드 1 ...", ...}

        if len(content) <= max_chunk_size:
            documents.append(
                Document(
                    page_content=content,
                    metadata={"source": source_name, "type": "text", **header_meta},
                )
            )
        else:
            for chunk in sub_splitter.split_text(content):
                documents.append(
                    Document(
                        page_content=chunk,
                        metadata={"source": source_name, "type": "text", **header_meta},
                    )
                )

    return documents


# --------------------------------------------------------------------------
# 4. 전체 파이프라인
# --------------------------------------------------------------------------


def process_llamaparse_markdown(markdown_text: str, source_name: str) -> list[Document]:
    table_docs, text = extract_tables(markdown_text, source_name)
    diagram_docs, text = extract_diagrams(text, source_name)
    text_docs = split_text_by_headers(text, source_name)

    return table_docs + diagram_docs + text_docs


# 위의 함수들이 잘 동작하는지 테스트하는 코드
if __name__ == "__main__":
    file_path = Path(__file__).parent / "parsed_data" / "output.md"
    with open(file_path, encoding="utf-8") as f:
        markdown_text = f.read()

    docs = process_llamaparse_markdown(markdown_text, source_name="NIA_2026_trends.pdf")

    type_counts: dict[str, int] = {}
    for doc in docs:
        t = doc.metadata["type"]
        type_counts[t] = type_counts.get(t, 0) + 1
    print(f"총 {len(docs)}개 Document / 타입별: {type_counts}")

    for doc in docs[:5]:
        print("-" * 60)
        print(doc.metadata)
        print(doc.page_content[:200])
