# app.py
from flask import Flask, render_template, request

# 서버 인스턴스 생성
app = Flask(__name__)

# 엔드포인트 1: 입력화면 (/in)
@app.route('/')         # localhost:5000/ 로 요청이 들어오면,
def input_page():       # 이 함수를 실행 하겠다.
    return render_template('in.html')  # in.html 갖다 줘라(응답해라)


# 엔드포인트 2: 출력화면 (/out)
@app.route('/out')
def output_page():
    pass


# 서버 실행
app.run(debug=True)
