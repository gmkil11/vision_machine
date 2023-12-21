import servo            # servo.py를 가져온다.
import conveyer         # conveyer.py를 가져온다.
import data             # data.py를 가져온다
import camera        # camruler3.py를 가져온다.

counter_1 = 0           # counter_1 에 0을 넣는다.
counter_2 = 0           # counter_2에 1을 넣는다.
data.default()          # data.py 에서 default 함수를 사용해 파이어베이스 데이터를 리셋


# loop문

while 1: # 계속 루프시킴
    print(data.read()) # data.py 에서 read 함수를 사용해 True/False 값을 받아와 출력한다.
    if data.read() == '"true"': # 파이어베이스에서 ON/OFF 값을 구별해 True일 시 함수를 실행시킨다.
        conveyer.detact()   # convayer.py 에서 detact() 함수를 가져온다.
        if data.read() == '"true"': # 파이어베이스에서 OFF 기능을 사용하기 위해서 False 값이 들어올 시 모터를 정지킴
            servo.servo_0()     # servo.py 에서 servo_0() 함수를 가져온다
            give = camera.cam() # camruler3.py 에서 cam() 함수에서 나오는 리턴값 (양품/불량품) 을 give라는 변수에 넣는다.
            good, bad = data.write(give,counter_1,counter_2) # data.py 에서 write() 함수 에서 나오는 리턴값을 (양품/불량 개수)를 good과 bad에 넣는다.
            counter_1 = good # counter_1 변수에 good을 넣는다.
            counter_2 = bad # counter_2 변수에 bad를 넣는다. 
            servo.servo(give) # servo.py 에 servo(x) 함수에 a의 값을 넣는다.
    
            