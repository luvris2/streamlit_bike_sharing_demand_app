import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("ggplot")  #using style ggplot
import joblib

def run_ml() :
    # 미리 학습시킨 표준화 스케일러와 RandomForest Regression모델 호출
    X_s_scaler = joblib.load('data/X_s_scaler.pkl')
    y_s_scaler = joblib.load('data/y_s_scaler.pkl')
    rf_ml = joblib.load('data/rf_ml.pkl')


    # csv 파일 호출
    train = pd.read_csv('data/train.csv', parse_dates=['datetime'])


    # 피쳐 엔지니어링
    train['year'] = train['datetime'].dt.year
    train['month'] = train['datetime'].dt.month
    train['day'] = train['datetime'].dt.day
    train['hour'] = train['datetime'].dt.hour
    train["dayofweek"] = train["datetime"].dt.dayofweek
    def concatenate_year_month(datetime):
        return "{0}-{1}".format(datetime.year, datetime.month)
    train["year_month"] = train["datetime"].apply(concatenate_year_month)


    if st.button('데이터 보기') :
        st.text('자전거 대여량 데이터')
        st.write(train.loc[ : , :'count' ])
        st.text('데이터 통계')
        st.write(train.describe())


    # 학습할 데이터 X와 결과값 y 분리
    X = train
    X = X.drop(['year_month', 'datetime','count', 'day'], axis=1)
    y = train['count']
    y = y.to_frame()


    # X,y 값 표준화 피쳐스케일링
    X = X_s_scaler.transform(X)
    y = y_s_scaler.transform(y)


    # 학습용, 테스트용 데이터 분리
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 3)


    # 결과값 예측 후 스케일링된 데이터 원복
    rf_y_pred = rf_ml.predict(X_test)
    rf_y_pred = rf_y_pred.reshape(2722,1)
    rf_y_pred = y_s_scaler.inverse_transform(rf_y_pred)
    rf_y_pred = np.around(rf_y_pred)
    y_test = y_s_scaler.inverse_transform(y_test)


    # 예측한 데이터 수치 출력
    st.subheader('대여량 예측하기')
    st.write('- 예측 데이터 (왼:실제값 / 오:예측값)')
    df = pd.DataFrame(data=y_test)
    df = df.rename(columns={0:'y_test_count'})
    df['rf_y_pred_count'] = rf_y_pred
    st.write(df)


    # 예측한 데이터 차트로 비교
    st.write(' ')
    st.write('- 실제값과 예측값 차트로 출력')
    st.line_chart(df)