import os
import pandas as pd
from flask import Flask, send_from_directory, render_template, request, jsonify
from LLM import rag_chain

# static_folder를 프론트엔드 빌드 결과물 폴더인 'templates/dist'로 지정합니다.
app = Flask(__name__, static_folder='templates/dist')

@app.route('/')
def home():
    # 기본 경로 접속 시 dist/index.html 반환
    return send_from_directory(app.static_folder, 'index.html')

# 정적 파일(js, css, 이미지 등) 및 React Router를 위한 라우트 설정
@app.route('/<path:path>')
def serve_static(path):
    # 요청된 파일이 dist 폴더 내에 존재하는지 확인
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    
    # 그 외의 모든 경로는 index.html로 보내어 React Router가 처리하도록 함
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/classify', methods=['POST'])
def classify():
    # 클라이언트로부터 데이터 받기
    data_from_client = request.get_json()
    my_test_data = data_from_client.get('my_test_data')

    df = pd.read_excel('data/waste_train.xlsx')

    x = df['data']
    y = df['category']

    # 데이터 전처리
    # 인코딩(문자열->숫자)
    x = pd.get_dummies(x)

    # 데이터 준비
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # 모델 학습
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier()
    model.fit(x_train, y_train)

    # 입력받은 데이터를 리스트로 감싸서 DataFrame 생성
    test_df = pd.DataFrame({'data': [my_test_data]})
    new_x = pd.get_dummies(test_df['data'])
    new_x = new_x.reindex(columns=x.columns, fill_value=0)

    # 결과 예측
    predictions = model.predict(new_x)

    # JSON 형태로 예측 결과 반환
    return jsonify({'result': str(predictions[0])})

@app.route('/classify_llm', methods=['POST'])
def classify_llm():
    # 클라이언트로부터 데이터 받기
    data_from_client = request.get_json()
    my_test_data = data_from_client.get('my_test_data')

    # LLM을 사용하여 분류
    query = f"{my_test_data}의 category는 무엇인가요?"
    result = rag_chain.invoke(query)

    # 결과에서 "Assistant:" 이후의 텍스트만 추출
    if "Assistant:" in result:
        answer = result.split("Assistant:", 1)[-1].strip()
    else:
        answer = result.strip()

    # JSON 형태로 예측 결과 반환
    return jsonify({'result': answer})

if __name__ == '__main__':
    app.run()