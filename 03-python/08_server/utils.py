import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

load_dotenv()


def extract_naver_news_content(url):
    '''url 을 통해 naver news의 본문만 추출'''
    
    if 'n.news.naver.com' not in url:
        raise Exception('네이버 뉴스가 아닙니다') 

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    news_text = soup.select_one('#dic_area').text.strip()
    return news_text


def make_gpt_comment(news_content, mood):
    '''들어온 뉴스 기사 내용에 따라, 원하는 분위기의 댓글 생성'''

    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )

    system_msg = f'''
    너는 매우 착한 댓글을 만들어주는 AI야. 
    기사 내용을 보고 {mood} 분위기의 댓글을 만들어줘
    '''
    # 기사내용은 이미 추출해 놨음! 그걸 사용

    gpt_res = client.responses.create(
        model='gpt-4.1-mini',
        # system message
        instructions=system_msg,
        input=news_content
    )

    return gpt_res.output_text
