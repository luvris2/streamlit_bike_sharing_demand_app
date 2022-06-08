# Overview
자전거 공유시스템은 시내 곳곳의 키오스크 위치 네트워크를 통해 회원가입, 대여, 자전거 반납 등의 절차가 자동화되는 자전거 대여 수단이다.
이 시스템을 사용하여, 사람들은 한 장소에서 자전거를 빌려서 필요에 따라 다른 곳으로 돌려줄 수 있다. 현재, 전 세계에는 500개 이상의 자전거 공유 프로그램이 있습니다.

# Repository File Structure
![file_dir](https://user-images.githubusercontent.com/105832446/172329301-f29efdcf-2db2-4197-ad78-bb0d201e6444.png)

- app.py : 실행을 위한 메인 파일
    - app_home.py : 앱 실행시 가장 먼저 보여질 홈
    - app_eda.py : 데이터를 분석하여 차트 출력
    - app_ml.py : 분석한 데이터를 이용하여 인공지능 예측
- data 폴더 : 앱 실행시 필요한 추가 파일
    - train.csv : 데이터셋
    - bike_img01.png : 사이드바에 보여질 이미지 파일
    - bike_img02.png : 홈화면에서 보여질 이미지 파일
    
# Dataset
**Kaggle Competitions**  
Bike Sharing Demand - Forecast use of a city bikeshare system  
https://www.kaggle.com/competitions/bike-sharing-demand/data

# Dataset Columns Detail
- datetime : 날짜와 시간
- season : 계절 (1:봄, 2:여름, 3:가을, 4:겨울
- holiday : 공휴일 여부 (0:평일, 1:공휴일)
- workingday : 평일 여부 (0:휴일, 1:평일)
- weather : 날씨 (1:맑음, 2:흐림, 3:이슬비, 4:호우)
- temp : 온도
- atemp : 체감온도
- humidity : 습도
- windspeed : 풍속
- casual : 미등록 회원 대여 횟수
- registered : 등록 회원 대여 횟수
- count : 총 대여 횟수

# Feature Engineering - Datetime
- 세밀한 데이터 분석을 위해 날짜와 시간을 분리
``` python
train['year'] = train['datetime'].dt.year
train['month'] = train['datetime'].dt.month
train['day'] = train['datetime'].dt.day
train['hour'] = train['datetime'].dt.hour
train["dayofweek"] = train["datetime"].dt.dayofweek
def concatenate_year_month(datetime):
    return "{0}-{1}".format(datetime.year, datetime.month)
train["year_month"] = train["datetime"].apply(concatenate_year_month)
```

# Drop Data
  - datetime : 피쳐 엔지니어링을 통해 날짜와 시간을 분리
  - year_month : 연도, 월 컬럼이 단독으로 존재
  -  day : working day, holiday 이용
  - count : 결과값이므로 y 변수에 대입
``` python
X.drop(['year_month','datetime','count','day'], axis=1)
```

# Split Data - X(train data), y(test data)
- X = 학습시킬 데이터
- y = count(대여량) 컬럼
- test size : 25%
``` python
    X = train
    X = X.drop(['year_month','datetime','count','day'], axis=1)
    y = train['count']
    y = y.to_frame()
```

# Feature Scaling
- Using Scaler : Standard Scaler
- Apply Variable : X, y

# Machine Learning
- Using Model : Random Forest Regression