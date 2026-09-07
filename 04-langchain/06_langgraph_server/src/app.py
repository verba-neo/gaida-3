# app.py -> 우리 서비스의 최종 그래프가 조립되는 곳
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import InMemorySaver

from src.state import EmailAgentState
from src.nodes import (
    classify_intent_node,
    search_document_node,
    bug_tracking_node,
    draft_response_node,
    human_review_node,
    send_reply_node
)
from src.routers import intent_router, send_or_hitl_router


builder = StateGraph(EmailAgentState)
builder.add_node(classify_intent_node)
builder.add_node(search_document_node)
builder.add_node(bug_tracking_node)
builder.add_node(draft_response_node)
builder.add_node(human_review_node)
builder.add_node(send_reply_node)

builder.add_edge(START, 'classify_intent_node')
builder.add_conditional_edges(
    'classify_intent_node',
    intent_router,
    {
        'human_review': 'human_review_node',
        'search_document': 'search_document_node',
        'bug_tracking': 'bug_tracking_node',
        'draft_response': 'draft_response_node',
    }
)
builder.add_edge('bug_tracking_node', 'draft_response_node')
builder.add_edge('search_document_node', 'draft_response_node')
builder.add_conditional_edges(
    'draft_response_node',
    send_or_hitl_router,
    {
        'human_review': 'human_review_node',
        'send_reply': 'send_reply_node'
    }
)

# email_graph = builder.compile(checkpointer=InMemorySaver())
email_graph = builder.compile()
