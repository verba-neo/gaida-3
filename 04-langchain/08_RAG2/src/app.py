from langgraph.graph import StateGraph, MessagesState, START, END

from src.vectorstore import googl_vectorstore


builder = StateGraph(MessagesState)  # 추후에 실제 사용할 State로 교체
builder.add_edge(START, END)
graph = builder.compile()