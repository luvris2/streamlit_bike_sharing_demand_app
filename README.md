# 오버뷰
자전거 공유시스템은 시내 곳곳의 키오스크 위치 네트워크를 통해 회원가입, 대여, 자전거 반납 등의 절차가 자동화되는 자전거 대여 수단이다.
이 시스템을 사용하여, 사람들은 한 장소에서 자전거를 빌려서 필요에 따라 다른 곳으로 돌려줄 수 있다. 현재, 전 세계에는 500개 이상의 자전거 공유 프로그램이 있습니다.

# 데이터셋
**Kaggle Competitions**  
Bike Sharing Demand - Forecast use of a city bikeshare system  
https://www.kaggle.com/competitions/bike-sharing-demand/data

# 데이터셋 각 컬럼 설명
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
``` python
    X = train
    X = X.drop(['year_month','datetime','count','day'], axis=1)
    y = train['count']
    y = y.to_frame()
```

# Feature Scaling
- User Scaler : Standard Scaler
- Apply Variable : X, y

# Machine Learning
- Using Model : Random Forest Regression
