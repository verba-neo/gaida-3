# src/nodes.py
from langchain.chat_models import init_chat_model
from langgraph.types import interrupt, Command
from langgraph.graph import END

from src.state import EmailAgentState, EmailClassification

llm = init_chat_model('openai:gpt-4.1-mini')


def classify_intent_node(state: EmailAgentState):
    '''LLM으로 이메일 분류: 의도와 긴급정도에 따라서 다음 노드가 결정되야함'''
    # 위에서 작성한 스키마 주입

    structured_llm = llm.with_structured_output(EmailClassification)
    prompt = f"""
    Analyze this customer email and classify it:

    Email: {state['email_content']}
    From: {state['sender_email']}

    Provide classification including intent, urgency, topic, and summary.
    """
    classification = structured_llm.invoke(prompt)

    # state의 classification을 갱신
    return {'classification': classification}


# RAG로 문서 찾는 노드
def search_document_node(state: EmailAgentState):
    classification = state['classification']
    # RAG에 사용할 가짜 쿼리
    query = f'{classification['intent']} - {classification['topic']}'
    print(f'----{query} 를 사용해 DB 검색중입니다...----')
    # 실제로는 vectorstore.search(query) 같은 코드를 실행하고
    search_result = [
        "Reset password via Settings > Security > Change Password",
        "Password must be at least 12 characters",
        "Include uppercase, lowercase, numbers, and symbols"
    ]
    return {'search_result': search_result}


# Github Issue 에서 해당하는 버그 찾아오는 노드
def bug_tracking_node(state: EmailAgentState):
    # github에서 issue 보고 대응하는 버그 issue id 가져오기를 가정
    issue_ids = ['BUG-123', 'BUG-456', 'BUG-789']
    return {'search_result': issue_ids}


# 이메일 초안 작성 노드
def draft_response_node(state: EmailAgentState):
    classification = state['classification']

    context_sections = []

    # 여러 문자열 데이터를 하나로 합치는 코드
    if state.get('search_results'):
        # list 안에 각 str을 '- ' 붙여서 엔터로 연결한 하나의 문자열
        formatted_docs = "\n".join([f"- {doc}" for doc in state['search_results']])
        context_sections.append(f"Relevant documentation:\n{formatted_docs}")

    # 여러 문자열 데이터를 하나로 합치는 코드
    if state.get('customer_history'):
        # Format customer data for the prompt
        context_sections.append(f"Customer tier: {state['customer_history'].get('tier', 'standard')}")

    prompt = f'''Draft a response to this customer email:
    원본 이메일 내용: {state['email_content']}

    Email intent: {classification.get('intent', 'unknown')}
    Urgency level: {classification.get('urgency', 'medium')}

    참고 문서:
        {'\n'.join(context_sections)}

    Guidelines:
    - Be professional and helpful
    - Address their specific concern
    - Use the provided documentation when relevant
    '''

    # 위에서 만든 context_sections 에 있는 내용을 싹다 프롬프트에 넣고 LLM에게 초안 만들어달라고 함
    result = llm.invoke(prompt)

    return {'draft_response': result.content}


def human_review_node(state: EmailAgentState):
    classification = state['classification']

    # human_decision에 저장된 데이터는 -> 인간이 Command(reusme=) 으로 재개명령할때, 보내는 데이터
    human_decision = interrupt({  # interrupt 내부의 데이터는 -> 인간에게 바톤터치할 때, 추가로 넘길 데이터
        "email_id": state.get('email_id',''),
        "original_email": state.get('email_content',''),
        "draft_response": state.get('draft_response',''),
        "urgency": classification.get('urgency'),
        "intent": classification.get('intent'),
        "action": "Please review and approve/edit this response"
    })

    # 사람이 승인을하면 이어짐
    if human_decision.get('approved'):  # 인간이 {'approved': True} 라고 보냈다면
        return Command(update={
            'draft_response': human_decision.get('edited_response') or state.get('draft_response')
        }, goto='send_reply_node')
    else:
        # 인간이 {'approved': True} 아님. -> 승인안함 -> 인간이 알아서 하겠다는 뜻 -> 종료
        return Command(update={}, goto=END)


# 이메일 답장 보내기
def send_reply_node(state: EmailAgentState) -> dict:
    # Integrate with email service
    print('-----------------이메일 답장 전송중------------------')
    print(f"Sending reply: {state['draft_response'][:100]}...")
    print('-----------------Agent 종료------------------')
    return {}
