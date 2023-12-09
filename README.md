# Django-registration-and-login-system
This web app has been developed using the popular Django framework and Bootstrap for the frontend. My motivation to build this project is so that I can learn about Django and tighten up my skills. This mini-app can be easily integrated into a bigger system project that needs to have a registration and login system.

### Basic Features of The App
    
* Register – Users can register and create a new profile
* Login - Registered users can login using username and password
* Social Apps Login – Users can login using their GitHub or Google account
* User Profile - Once logged in, users can create and update additional information such as avatar and bio in the profile page
* Update Profile – Users can update their information such as username, email, password, avatar and bio
* Remember me – Cookie Option, users don’t have to provide credentials every time they hit the site
* Forgot Password – Users can easily retrieve their password if they forget it 
* Admin Panel – admin can CRUD users

![ScreenShot](https://user-images.githubusercontent.com/66206865/131695930-648342b0-010b-44b2-a419-15ad54d47869.png)

## Tutorial
[Here](https://dev.to/earthcomfy/series/14274) is a tutorial on how to build this project.

### Quick Start
To get this project up and running locally on your computer follow the following steps.
1. Set up a python virtual environment
2. Run the following commands
```
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```
   
3. Open a browser and go to http://localhost:8000/




#주제 : 중남미 권역 내 여행 타입에 따른 관광지 추천해주는 웹 페이지

용자는 로그인한 후 사용자의 선호도를 조사하고, 이를 기반으로 사용자에게 최적화된 여행 일정과 관광지 정보를 제공합니다.또한 지도를 통해 관광지 위치를 시각적으로 확인할 수 있습니다.

<프로젝트 목적>

- 중남미 권역에 관심있는 여행객들에게 여행 타입별로 다양한 관광지를 추천하여 풍부한 여행 경험을 제공하는 것을 목적으로 합니다.

- 사용자의 여행 선호도를 고려하여 맞춤형 여행 일정과 관광지 정보를 제공하여 사용자의 만족도를 높이는 것을 목표로 합니다.

<프로젝트 용도>

- 사용자는 로그인한 후, 여행 선호도 조사를 통해 자신의 여행 스타일을 선택하고 기록할 수 있습니다.

- 사용자가 선택한 여행 타입에 따라 관광지 추천 알고리즘이 동작하여 사용자에게 맞춤형 여행 일정과 추천 관광지를 제공합니다.

- 웹 페이지에서는 지도를 통해 관광지의 위치를 시각적으로 확인할 수 있습니다.

<프로젝트 설치 및 설정>

1.파이참 설치 :
 프로젝트를 실행하기 위해 파이참을 설치해야 합니다. 추천 버전은PyCharm 2023.2.5입니다.

2.프로젝트 다운 : 
프로젝트 폴더를 다운로드 후 압축 해제합니다. (만약 깃을 이용하여 다운을 받았다면 git clone 프로젝트URL 을 작성)

3.프로젝트 의존성 설치 : 
1. 필요한 라이브러리를 설치하기 위해 터미널에서 pip install -r requirements.txt 명령어를 실행합니다.
2. pip install scikit-learn pip install pandas pip install konlpy 3개를 설치합니다. 


<프로젝트 실행>

1. 사용자 계정을 만듭니다.
python manage.py createsuperuser

2.서버 실행
manage.py 파일이 있는 디렉토리에서 터미널을 열어 다음 명령어를 실행합니다.
명령어 : python manage.py runserver

3.웹 페이지 접속:
웹 브라우저에서 http://localhost:8000 주소로 접속하여 중남미 여행 타입에 따른 관광지 추천 웹 페이지를 이용할 수 있습니다.


