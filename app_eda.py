import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 한글 출력
import platform
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system... sorry~~~~')

train = pd.read_csv('data/train.csv', parse_dates=['datetime'])
train['year'] = train['datetime'].dt.year
train['month'] = train['datetime'].dt.month
train['day'] = train['datetime'].dt.day
train['hour'] = train['datetime'].dt.hour
train["dayofweek"] = train["datetime"].dt.dayofweek
def concatenate_year_month(datetime):
    return "{0}-{1}".format(datetime.year, datetime.month)
train["year_month"] = train["datetime"].apply(concatenate_year_month)

def run_eda() :
    st.subheader('데이터 분석')
    st.text(platform.system())

    if st.button('데이터 보기') :
        st.write(train.loc[ : , :'count' ])

    with st.expander('데이터프레임 컬럼 상세 설명') :
        st.subheader('데이터프레임 컬럼 상세 설명')
        st.text('datetime : 날짜와 시간')
        st.text('season : 계절 (1:봄, 2:여름, 3:가을, 4:겨울')
        st.text('holiday : 공휴일 여부 (0:평일, 1:공휴일')
        st.text('workingday : 평일 여부 (0:휴일, 1:평일')
        st.text('weather : 날씨 (1:맑음, 2:흐림, 3:이슬비, 4:호우)')
        st.text('temp : 온도')
        st.text('atemp : 체감온도')
        st.text('humidity : 습도')
        st.text('windspeed : 풍속')
        st.text('casual : 미등록 회원 대여 횟수')
        st.text('registered : 등록 회원 대여 횟수')
        st.text('count : 총 대여 횟수')

    st.text('')
    st.subheader('날짜/시간별 대여량 분석')
    figure, (ax1,ax2) = plt.subplots(nrows=1, ncols=2)
    figure.set_size_inches(15,5)
    sns.barplot(data=train, x='year' , y= 'count' , ax=ax1)
    sns.barplot(data=train, x='month' , y= 'count' , ax=ax2)
    ax1.set_title("연도별 대여량", fontsize=30)
    ax1.set_xlabel("연도", fontsize=20)
    ax1.set_ylabel("대여량", fontsize=20)
    ax2.set_title("월별 대여량", fontsize=30)
    ax2.set_xlabel("월", fontsize=20)
    ax2.set_ylabel("대여량", fontsize=20)   
    st.pyplot(figure)
    
    figure, (ax3,ax4) = plt.subplots(nrows=1, ncols=2)
    figure.set_size_inches(15,5)
    sns.barplot(data=train, x='day' , y= 'count' , ax=ax3)
    sns.barplot(data=train, x='hour' , y= 'count' , ax=ax4)
    ax3.set_title("일별 대여량", fontsize=30)
    ax3.set_xlabel("일", fontsize=20)
    ax3.set_ylabel("대여량", fontsize=20)
    ax4.set_title("시간별 대여량", fontsize=30)
    ax4.set_xlabel("시간", fontsize=20)
    ax4.set_ylabel("대여량", fontsize=20)
    st.pyplot(figure)    

    fig, ax5 = plt.subplots(nrows=1, ncols=1)
    fig.set_size_inches(18, 4)
    sns.barplot(data=train, x="year_month", y="count", ax=ax5)
    ax5.set_title("연도/월별 대여량", fontsize=40)
    ax5.set_xlabel("연도-월", fontsize=25)
    ax5.set_ylabel("대여량", fontsize=25)
    st.pyplot(fig)

    st.text('')
    st.subheader('계절별, 휴일/평일별 대여량 분석')
    fig, axes = plt.subplots(ncols=2)
    fig.set_size_inches(10, 5)
    sns.boxplot(data=train,y="count",x="season",orient="v",ax=axes[0])
    sns.boxplot(data=train,y="count",x="workingday",orient="v",ax=axes[1])

    axes[0].set_title('계절별 대여량', fontsize=25)
    axes[0].set_xlabel('계절(1:봄, 2:여름, 3:가을, 4:겨울)', fontsize=15)
    axes[0].set_ylabel('대여량', fontsize=15)
    axes[1].set_title('휴일/평일별 대여량', fontsize=25)
    axes[1].set_xlabel('휴일/평일(0:휴일, 1:평일', fontsize=15)
    axes[1].set_ylabel('대여량', fontsize=15)
    st.pyplot(fig)

    st.text('')
    st.subheader('시간별 대여량 심화 분석')
    fig,ax1 = plt.subplots(nrows=1)
    fig.set_size_inches(10, 3)
    sns.pointplot(data=train, x="hour", y="count", ax=ax1)
    ax1.set_title("시간별 대여량", fontsize=25)
    ax1.set_xlabel("시간", fontsize=15)
    ax1.set_ylabel("대여량", fontsize=15)
    st.pyplot(fig)
    fig,ax2 = plt.subplots(nrows=1)
    fig.set_size_inches(10, 3)
    sns.pointplot(data=train, x="hour", y="count", hue="workingday", ax=ax2)
    ax2.set_title("휴일/평일에 따른 시간별 대여량", fontsize=25)
    ax2.set_xlabel("휴일/평일(0:휴일, 1:평일)", fontsize=15)
    ax2.set_ylabel("대여량", fontsize=15)
    st.pyplot(fig)
    fig,ax3 = plt.subplots(nrows=1)
    fig.set_size_inches(10, 3)
    sns.pointplot(data=train, x="hour", y="count", hue="dayofweek", ax=ax3)
    ax3.set_title("요일에 따른 시간별대여량", fontsize=25)
    ax3.set_xlabel("요일(1:월, 2:화, 3:수, 4:목, 5:금, 6:토, 7:일)", fontsize=15)
    ax3.set_ylabel("대여량", fontsize=15)
    st.pyplot(fig)
    fig,ax4 = plt.subplots(nrows=1)
    fig.set_size_inches(10, 3)
    sns.pointplot(data=train, x="hour", y="count", hue="weather", ax=ax4)
    ax4.set_title("날씨에 따른 시간별 대여량", fontsize=25)
    ax4.set_xlabel("날씨(1:맑음, 2:흐림, 3:이슬비, 4:호우))", fontsize=15)
    ax4.set_ylabel("대여량", fontsize=15)
    st.pyplot(fig)
    fig,ax5 = plt.subplots(nrows=1)
    fig.set_size_inches(10, 3)
    sns.pointplot(data=train, x="hour", y="count", hue="season", ax=ax5)
    ax5.set_title("계절에 따른 시간별 대여량", fontsize=25)
    ax5.set_xlabel("계절(1:봄, 2:여름, 3:가을, 4:겨울)", fontsize=15)
    ax5.set_ylabel("대여량", fontsize=15)
    st.pyplot(fig)

    st.text('')
    st.subheader('상관계수 표현')
    corrMatt = train[["temp", "atemp", "casual", "registered", "humidity", "windspeed", "count"]]
    corrMatt = corrMatt.corr()
    st.text(corrMatt)

    import numpy as np
    mask = np.array(corrMatt)
    mask[np.tril_indices_from(mask)] = False

    fig, ax = plt.subplots()
    fig.set_size_inches(20,10)
    sns.heatmap(corrMatt, mask=mask,vmax=.8, square=True,annot=True)
    st.pyplot(fig)


    fig,(ax1,ax2,ax3) = plt.subplots(ncols=3)
    fig.set_size_inches(12, 5)
    sns.regplot(x="temp", y="count", data=train,ax=ax1)
    sns.regplot(x="windspeed", y="count", data=train,ax=ax2)
    sns.regplot(x="humidity", y="count", data=train,ax=ax3)