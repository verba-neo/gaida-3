# src/state.py
from typing import TypedDict, Literal
from langgraph.graph import MessagesState


# 1. 아래 State 형태를 결정할 때 사용
# 2. llm_with_output에서 스키마로 사용
class EmailClassification(TypedDict):
    intent: Literal['question', 'bug', 'billing', 'feature', 'complex']
    urgency: Literal['low', 'medium', 'high', 'critical']
    topic: str
    summary: str


class EmailAgentState(MessagesState):
    # messages 포함

    sender_email: str
    email_content: str

    classification: EmailClassification

    search_result = list[str] | None  # search_result 는 있으면 list[str], 없을 수도 있다.
    customer_history: dict | None

    draft_response: str | None