import pyrebase # pyrebase 라이브러리를 넣는다. (Firebase API 파이썬 용 라이브러리)
 
# 데이터 베이스 초기화 함수
def default(): # default() 라는 함수를 만들어준다.
    config = { # 파이어베이스 통신 설정을 config이라는 변수에 넣는다.
        "apiKey": "cknchqy6wHWxrCzHJAYZXgBJ0TM8jHTn38b8C800",
        "authDomain": "vision-machine-8f1fd.firebaseapp.com",
        "databaseURL": "https://vision-machine-8f1fd-default-rtdb.firebaseio.com/",
        "projectId": "vision-machine-8f1fd",
        "storageBucket": "https://vision-machine-8f1fd.appspot.com/"
    }

    
    firebase = pyrebase.initialize_app(config) # pyerbase 라이브러리에서 initialize_app() 함수에 config 변수를 넣고 firebase 변수에 넣는다.

    db = firebase.database() # firebase.database() 메소드를 db라는 변수에 넣는다.
    db.child("data").update({"양품 개수 :": 0}) # db.child().update 메소드를 사용해 data 라는 키에 "양품 개수 : 0" 값을 저장한다. 
    db.child("data").update({"불량품 개수 :": 0}) # db.child().update 메소드를 사용해 data 라는 키에 "불량품 개수 : 0" 값을 저장한다. 

# 데이터 베이스 저장 함수
def write(given, good, bad): #write() 라는 함수를 만들고 given, good, bad라는 매개변수를 준다.
    config = { # 파이어베이스 통신 설정을 config이라는 변수에 넣는다.
        "apiKey": "cknchqy6wHWxrCzHJAYZXgBJ0TM8jHTn38b8C800",
        "authDomain": "vision-machine-8f1fd.firebaseapp.com",
        "databaseURL": "https://vision-machine-8f1fd-default-rtdb.firebaseio.com/",
        "projectId": "vision-machine-8f1fd",
        "storageBucket": "https://vision-machine-8f1fd.appspot.com/"
    }


    firebase = pyrebase.initialize_app(config) # pyerbase 라이브러리에서 initialize_app() 함수에 config 변수를 넣고 firebase 변수에 넣는다.

    db = firebase.database() # firebase.database() 메소드를 db라는 변수에 넣는다.

    if given == True: # camruler3.py에서 나온 리턴값(give)값이 True 라면
        good = good + 1 # good 이라는 변수에 1을 추가한다. (초기값 = 0)
        db.child("data").update({"양품 개수 :": good}) # db.child().update 메소드를 사용해 data 라는 키에 "양품 개수 : good" 값을 저장한다. 

    else : # camruler3.py에서 나온 리턴값(give)값이 False 라면
        bad = bad + 1 # bad 라는 변수에 1을 추가한다. (초기값 = 0)
        db.child("data").update({"불량품 개수 :": bad}) # db.child().update 메소드를 사용해 data 라는 키에 "불량품 개수 : bad" 값을 저장한다. 
        
    return good, bad # good과 bad 값을 리턴시킨다.

# 데이터베이스 읽기 함수
def read(): # read() 라는 함수를 만든다.
    config = { # 파이어베이스 통신 설정을 config이라는 변수에 넣는다.
        "apiKey": "cknchqy6wHWxrCzHJAYZXgBJ0TM8jHTn38b8C800",
        "authDomain": "vision-machine-8f1fd.firebaseapp.com",
        "databaseURL": "https://vision-machine-8f1fd-default-rtdb.firebaseio.com/",
        "projectId": "vision-machine-8f1fd",
        "storageBucket": "https://vision-machine-8f1fd.appspot.com/"
    }

    firebase = pyrebase.initialize_app(config) # pyerbase 라이브러리에서 initialize_app() 함수에 config 변수를 넣고 firebase 변수에 넣는다.

    db = firebase.database() # firebase.database() 메소드를 db라는 변수에 넣는다.
    power = db.child("Power").get() # 데이터베이스의 Power라는 데이터를 가져와 power 변수에 넣는다.
    
    for power in power.each(): # power 안의 value 값을 추출하는 함수
        is_on = power.val() # power 안의 value 값을 is_on 변수에 넣는다.
        
    return is_on # is_on 값을 리턴시킨다.