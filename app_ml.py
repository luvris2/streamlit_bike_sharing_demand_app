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
    rf_wind_ml = joblib.load('data/rf_wind_ml.pkl')

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

    st.subheader('풍속이 0인 값 확인하기')
    st.write(train['windspeed'].value_counts())

    # 풍속이 0인 값과 아닌 값 나누기
    trainWind0 = train.loc[train['windspeed'] == 0]
    trainWindNot0 = train.loc[train['windspeed'] != 0]
    testWind0 = test.loc[test['windspeed'] == 0]
    testWindNot0 = test.loc[test['windspeed'] != 0]

    st.subheader('풍속이 0인 값 데이터 예측하기')
    wCol = ["season", "weather", "humidity", "month", "temp", "year", "atemp"]
    trainWindNot0["windspeed"] = trainWindNot0["windspeed"].astype("str") # 풍속이 0이 아닌 값들 스트링으로 타입 변환
    testWindNot0["windspeed"] = testWindNot0["windspeed"].astype("str") # 풍속이 0이 아닌 값들 스트링으로 타입 변환
    rf_wind_ml.fit(trainWindNot0[wCol], trainWindNot0["windspeed"])
    trainWind0_pred = rf_wind_ml.predict(X = trainWind0[wCol])
    testWind0_pred = rf_wind_ml.predict(X = testWind0[wCol])

    # 풍속 0인 값 대입전 차트 출력
    st.text('풍속이 0인 값 정리 전 차트')
    fig1, ax1 = plt.subplots()
    fig1.set_size_inches(25,10)
    plt.sca(ax1)
    plt.xticks(rotation=30, ha='right')
    ax1.set(ylabel='Count',title="train windspeed")
    sns.countplot(data=train, x="windspeed", ax=ax1)
    st.pyplot(fig1)

    # 풍속이 0인 값에 예측한 풍속 값 대입
    trainWind0['windspeed'] = trainWind0_pred
    train = trainWind0.append(trainWindNot0)
    train['windspeed'] = train['windspeed'].astype('float')

    testWind0['windspeed'] = testWind0_pred
    test = testWind0.append(testWindNot0)
    test['windspeed'] = test['windspeed'].astype('float')

    #0 값을 조정한 이후 차트 확인
    st.text('풍속이 0인 값 예측 후 차트')
    fig2, ax2 = plt.subplots()
    fig2.set_size_inches(25,10)
    plt.sca(ax2)
    plt.xticks(rotation=30, ha='right')
    ax2.set(ylabel='Count',title="test windspeed")
    sns.countplot(data=test, x="windspeed", ax=ax2)
    st.pyplot(fig2)

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