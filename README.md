# 🌠🥇Travel_Project🥇🌠




## 🖥️ 시연 화면
https://youtu.be/jTv9dnZsMHU?si=Wh4IGrgmM7nrS1gb


## 📖실행법

1.프로젝트 의존성 설치 :
- 필요한 라이브러리를 설치하기 위해 터미널에서 pip install -r requirements.txt 명령어를 실행합니다.
- pip install scikit-learn pip install pandas pip install konlpy 3개를 설치합니다.

2.사용자 계정을 만듭니다.
- python manage.py createsuperuser

3.서버 실행
- manage.py 파일이 있는 디렉토리에서 터미널을 열어 다음 명령어를 실행합니다.
- 명령어 : python manage.py runserver

4.웹 페이지 접속:
- 웹 브라우저에서 http://localhost:8000 주소로 접속하여 중남미 여행 타입에 따른 관광지 추천 웹 페이지를 이용할 수 있습니다.


## 😊 프로젝트 소개 및 목적
- AI를 활용한 여행추천 사이트입니다.
- 중남미 권역에 관심있는 여행객들에게 여행 타입별로 다양한 관광지를 추천하여 풍부한 여행 경험을 제공하는 것을 목적으로 합니다.
- 사용자의 여행 선호도를 고려하여 맞춤형 여행 일정과 관광지 정보를 제공하여 사용자의 만족도를 높이는 것을 목표로 합니다.

#
<br>

## 🕰️ 개발 기간
* 23.09.03일 - 23.12.11일

### 🧑‍🤝‍🧑 맴버구성
 - 팀장: 최승호 - 서버 및 AI 개발
 - 팀원: 김성학 - 디자이너 및 UI 개발
 - 팀원: 김도균 - 디자이너 및 UI 개발
 - 팀원: 석재민 - AI 개발 
 - 팀원: 임지현 - 기획
### ⚙️ 개발 환경
- **Language** : `python 3.3`
- **Framework** : Django
- **Database** : MySql
- **AI** : TensorFlow, PyTorch, Keras 
- **IDE** :  Pycharm

## 🌠 시스템 구조
![image](https://github.com/chltmdgh522/Travel_AI/assets/74850409/d53b4c4e-3f11-4860-8cf0-ee36b9fe95f3)


## 📌 주요 기능
#### 로그인/회원가입 -
- DB값 검증
- 비밀번호 찾기 및 변경 
- 로그인 시 쿠키(Cookie) 및 세션(Session) 생성

#### 마이 페이지 
- 프로필, 이름, 소개 변경
  
#### AI 추천 기능 
- 사용자 응답 처리(사전에 설문조사 폼 만들어서 25000개의 데이터 처)
- 데이터 전처리
- 머신러닝 모델 학습
- 사용자 데이터 일치 여부 확인

#### 구글맵 API
- 구글 지도 객체 생성 및 초기화
- 여행지 위치를 마커로 지도에 표시
- 마커 클릭 시 이동 거리 및 이동 시간 계산

  
