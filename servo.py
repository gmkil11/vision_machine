import pigpio # pigpio 라이브러리를 가져온다.
import time # time 라이브러리를 가져온다.

# 서보모터 컨트롤 함수
def servo(is_passed): # servo() 함수를 만든다.
    servo = 18 # 18번 핀에 서보모터를 연결
    pwm = pigpio.pi() # pigpio에서 pi(pwm 조정 함수)를 pwm 변수에 넣는다.
    pwm.set_mode(servo, pigpio.OUTPUT) # 서보모터를 출력모드로 바꾼다.

    if is_passed == True: # 만약 camruler에서 리턴받은 값이 True라면
        pwm.set_servo_pulsewidth( servo,800) # 서보 모터의 펄스값을 800으로 설정 (60도)
        time.sleep(1.0) # 1초간 정지

    else: # 만약 camruler에서 리턴받은 값이 False라면
        pwm.set_servo_pulsewidth( servo,2200) # 서보 모터의 펄스값을 2200으로 설정 (120도)
        time.sleep(1.0) # 1초간 정지

# 서보모터 리셋 함수
def servo_0(): # servo_0() 함수를 만든다.
    print("서보모터 중립") # 서보모터 중립이라는 텍스트를 터미널에 표시
    servo = 18 # 18번 핀에 서보모터를 연결
    pwm = pigpio.pi() # pigpio에서 pi(pwm 조정 함수)를 pwm 변수에 넣는다.
    pwm.set_mode(servo, pigpio.OUTPUT) # 서보모터를 출력모드로 바꾼다.
    pwm.set_servo_pulsewidth( servo,1500); # 서보 모터의 펄스값을 1500으로 설정 (90도)
    time.sleep(1.0) # 1초간 정지






