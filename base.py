from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)
 
@app.route('/')
def home():
    return render_template('home.html')
    

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

if __name__ == '__main__':
   app.run()