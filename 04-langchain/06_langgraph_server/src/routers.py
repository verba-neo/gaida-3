# src/routers.py
from src.state import EmailAgentState


# 의도 분류기
def intent_router(state: EmailAgentState):
    intent = state['classification']['intent']
    urgecy = state['classification']['urgency']
    # intent 가 billing. or 긴급도가 'critical' 이면, 'human_review' 리턴
    if intent == 'billing' or urgecy == 'critical':
        return 'human_review'
    # intent가 'question' 이나 'feature' 면, 'search_document' 리턴
    elif intent in ('question', 'feature'):
        return 'search_document'
    # intent 가 bug 면,  'bug_tracking' 리턴
    elif intent == 'bug':
        return 'bug_tracking'
    # 나머지는, 'draft_response' 리턴
    else:
        return 'draft_response'


# 생성한 응답을 1. 보낼지 / 2. 인간에게 검사받을지 결정하는 라우터
def send_or_hitl_router(state: EmailAgentState):
    c = state['classification']
    # 긴급도가 high, critical 이거나 의도가 'complex' 면 인간 리뷰
    if c['urgency'] in ('high', 'critical') or c['intent'] == 'complex':
        return 'human_review'
    # 아니면 메일 발송
    else:
        return 'send_reply'
