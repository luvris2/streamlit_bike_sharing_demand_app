import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use("ggplot")  #using style ggplot
import joblib

def run_ml() :
    X_s_scaler = joblib.load('data/X_s_scaler.pkl')
    y_s_scaler = joblib.load('data/y_s_scaler.pkl')
    rf_ml = joblib.load('data/rf_ml.pkl')

    train = pd.read_csv('data/train.csv', parse_dates=['datetime'])
    test = pd.read_csv('data/test.csv', parse_dates=['datetime'])
    train['year'] = train['datetime'].dt.year
    train['month'] = train['datetime'].dt.month
    train['day'] = train['datetime'].dt.day
    train['hour'] = train['datetime'].dt.hour
    train["dayofweek"] = train["datetime"].dt.dayofweek
    def concatenate_year_month(datetime):
        return "{0}-{1}".format(datetime.year, datetime.month)
    train["year_month"] = train["datetime"].apply(concatenate_year_month)
    test['year'] = test['datetime'].dt.year
    test['month'] = test['datetime'].dt.month
    test['day'] = test['datetime'].dt.day
    test['hour'] = test['datetime'].dt.hour
    test["dayofweek"] = test["datetime"].dt.dayofweek

    if st.button('데이터 보기') :
        st.text('자전거 대여량 데이터')
        st.write(train.loc[ : , :'count' ])
        st.text('데이터 통계')
        st.write(train.describe())

    X = train
    X = X.drop(['year_month','casual','registered','datetime','count', 'day'], axis=1)
    y = train['count']
    y = y.to_frame()

    X = X_s_scaler.transform(X)
    y = y_s_scaler.transform(y)

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 3)

    rf_y_pred = rf_ml.predict(X_train)
    rf_y_pred = rf_y_pred.reshape(8164,1)
    rf_y_pred = y_s_scaler.inverse_transform(rf_y_pred)
    rf_y_pred = np.around(rf_y_pred)
    y_train = y_s_scaler.inverse_transform(y_train)

    st.subheader('대여량 예측하기')
    st.text(' 예측 데이터 (왼:실제값 / 오:예측값)')
    df = pd.DataFrame(data=y_train)
    df = df.rename(columns={0:'y_test_count'})
    df['rf_y_pred_count'] = rf_y_pred
    st.write(df)
    st.text('실제값과 예측값 차트로 출력')
    st.line_chart(df)