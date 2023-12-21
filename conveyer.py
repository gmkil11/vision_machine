import RPi.GPIO as GPIO # RPi.GPIO 라이브러리를 가져오고 GPIO로 선언해 사용한다.
import time # time 라이브러리를 가져온다.
from multiprocessing import Process, Queue # multiprocessing 라이브러리에서 Process와 Queue를 가져온다.
import data

def detact(): # 물체 감지 

    def motor(q): # motor()라는 함수를 만들고 Queue를 이용하기 위해서 매개변수 q를 선언한다.
        # 모터 상태
        STOP = 0 # 0을 STOP이라는 변수에 넣는다.
        FORWARD  = 1 # 1을 FORWARD라는 변수에 넣는다.
        BACKWORD = 2 # 2를 BACKWORD라는 변수에 넣는다.

        # 2개의 모터를 이용하기 위해 채널 2개를 만듦
        CH1 = 0 # CH1이라는 변수에 0을 넣는다.
        CH2 = 1 # CH2라는 변수에 1을 넣는다.

        # PIN 입출력 설정
        OUTPUT = 1 # OUTPUT이라는 변수에 1을 넣는다.
        INPUT = 0 # INPUT이라는 변수에 0을 넣는다.

        # PIN 설정
        HIGH = 1 # HIGH라는 변수에 1을 넣는다.
        LOW = 0 # LOW라는 변수에 0을 넣는다.

        # 실제 핀 정의
        #PWM PIN 
        ENA = 26  #37 pin (A모터의 PWM 신호를 enables 시킨다. 즉, 모터의 속도)
        ENB = 0   #27 pin (B모터의 PWM신호를 enables 시킨다. 즉, 모터의 속도)  

        #GPIO PIN
        IN1 = 19  #35 pin (A모터를 enable시킴)
        IN2 = 13  #33 pin (A모터를 enable시킴)
        IN3 = 6   #31 pin (B모터를 enable시킴)
        IN4 = 5   #29 pin (B모터를 enable시킴)

        # 핀 설정 함수
        def setPinConfig(EN, INA, INB):  # setPinConfig()라는 함수를 만든다.
            GPIO.setup(EN, GPIO.OUT) # 모터 드라이버의 EN핀을 출력으로 만든다. 
            GPIO.setup(INA, GPIO.OUT) # 모터드라이버의 INA핀을 출력으로 만든다.
            GPIO.setup(INB, GPIO.OUT) # 모터드라이버의 INB핀을 출력으로 만든다.
 
            pwm = GPIO.PWM(EN, 100)  # 100khz 로 PWM 동작 시킴   
            pwm.start(0)   # 우선 PWM 멈춤.
            return pwm # pwm값을 리턴시킴

        # 모터 제어 함수
        def setMotorContorl(pwm, INA, INB, speed, stat): # setMotorControl() 함수를 만들어준다

            pwm.ChangeDutyCycle(speed)  #모터 속도 제어 PWM
            
            if stat == FORWARD: # 만약 stat이 FORWARD라면 
                GPIO.output(INA, HIGH) # INA핀을 HIGH로 설정한다.
                GPIO.output(INB, LOW) # INB핀을 LOW로 설정한다.
                
            #뒤로
            elif stat == BACKWORD: #만약 stat이 BACKWORD라면
                GPIO.output(INA, LOW) # INA핀을 LOW로 설정한다.
                GPIO.output(INB, HIGH) # INB핀을 HIGH로 설정한다.
            
            #정지
            elif stat == STOP: #만약 stat이 STOP이라면
                GPIO.output(INA, LOW) # INA핀을 LOW로 설정한다.
                GPIO.output(INB, LOW) # INB핀을 LOW로 설정한다.

                
        # 모터 제어함수 간단하게 사용하기 위해 한번더 감싼다
        def setMotor(ch, speed, stat): # setMoter라는 함수를 만든다
            if ch == CH1: # 만약 ch가 CH1과 같다면
                setMotorContorl(pwmA, IN1, IN2, speed, stat) #pwmA는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
            else: # 나머지는
                setMotorContorl(pwmB, IN3, IN4, speed, stat)  #pwmB는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
          

        # GPIO 모드 설정 
        GPIO.setmode(GPIO.BCM) # 핀번호를 브로드컴칩(BCM)의 번호를 참조하는 모드로 설정
              
        #모터 핀 설정
        #핀 설정후 PWM 핸들 얻어옴 
        pwmA = setPinConfig(ENA, IN1, IN2) # setPinConfig()함수에 ENA, IN1, IN2 변수를 선언하고 pwmA 변수에 넣는다.
        pwmB = setPinConfig(ENB, IN3, IN4) # setPinConfig()함수에 ENB, IN3, IN4 변수를 선언하고 pwmB 변수에 넣는다.
        

        #제어 시작
        time.sleep(2)  # 모터를 안정화 시키기 위해서 2초 정지 
        setMotor(CH1, 20, FORWARD) # CH1 모터를 20의 pwm으로 앞으로 회전시킨다.
        setMotor(CH2, 20, FORWARD) # CH2 모터를 20의 pwm으로 앞으로 회전시킨다.
        
        #queue 설정
        stop = q.get() # stop이라는 변수에 초음파 센서의 Queue(a) 를 가져오는 함수를 사용한다.
        
        # 초음파 센서에서 물체 인식 시
        if stop == 1: # 만약 stop 이라는 변수에 1 이 들어온다면
            time.sleep(0.8) # 초음파 센서 인식 후 카메라 아래서 멈추게 0.8초를 기다렸다가 모터를 정지시킨다.
            setMotor(CH1, 0, FORWARD) # CH1 모터를 정지시킨다.
            setMotor(CH2, 0, FORWARD) # CH2 모터를 정지시킨다.
            GPIO.cleanup() # GPIO 신호를 초기화 시킨다.
        
    def sonic(a, q): # sonic() 이라는 함수를 만들고 a라는 변수와 Queue를 사용하기 위해 q를 선언한다.
        time.sleep (2) # 초음파 센서를 안정화 시키기 위해서 2초 정지
        GPIO.setmode(GPIO.BCM) # GPIO.setmode(GPIO.BCM) # 핀번호를 브로드컴칩(BCM)의 번호를 참조하는 모드로 설정
        GPIO.setwarnings(False) # GPIO 경고를 표시하지 않는다.

        TRIG = 23 # TRIG 핀을 23번 핀에 연결
        ECHO = 24 # ECHO 핀을 24번 핀에 연결
        print("초음파 거리 측정기 활성화") # 초음파 센서가 활성화 되었는지 표시하기 위한 문구

        GPIO.setup(TRIG, GPIO.OUT) # TRIG 핀을 출력 신호로 설정한다.
        GPIO.setup(ECHO, GPIO.IN) # ECHO 핀을 입력 신호로 설정한다.

        GPIO.output(TRIG, False) # TRIG 출력 신호를 끈다.
        # loop문
        while True: # 계속 루프시킨다. 
            GPIO.output(TRIG,True) # TRIG 출력 신호를 킨다.
            time.sleep(0.1)        # 10uS의 펄스 발생을 위한 딜레이
            GPIO.output(TRIG, False) # TRIG 출력 신호를 끈다.
            
            while GPIO.input(ECHO)==0: # 만약 ECHO 핀이 0이라는 신호가 들어오면 (초음파가 수신이 안 되면 start 변수에 시간을 입력한다.)
                start = time.time()     # Echo핀 상승 시간값 저장
                
            while GPIO.input(ECHO)==1: # 만약 ECHO 핀이 1이라는 신호가 들어오면 (초음파가 수신되면 stop 변수에 시간을 입력한다.)
                stop = time.time()      # Echo핀 하강 시간값 저장
                
            check_time = stop - start # stop 시간 값에서 start 시간 값을 뺀 값을 check_time 값에 넣는다. 
            distance = check_time * 34300 / 2 # check_time에 34300을 2로 나눈 값을 곱해 distance 변수에 넣는다. (거리 = 시간 * 속도)이고, 소리의 속도는 34300cm/s 인데
                                              # 초음파 센서는 송신부에서 나갔다가 수신부로 들어오기 때문에 2를 나눈다.) 
            if distance < 9: # 만약 distance가 5cm 보다 작으면 (물체가 인식 되었을 때)
                a = 1 # a 라는 변수에 1을 넣는다.
                q.put(a) # Queue 변수에 a를 넣는다.
                GPIO.cleanup() # GPIO 신호를 초기화 시킨다.
                break # while 문을 빠져나간다.
            
            elif data.read() == '"false"': # 만약 파이어베이스의 power 값이 OFF(false)라면
                a = 1 # a 라는 변수에 1을 넣는다.
                q.put(a) # Queue 변수에 a를 넣는다.
                GPIO.clenup() # GPIO 신호를 초기화 시킨다.    
                break # while 문을 빠져나간다.             
                
            
            print("Distance : %.1f cm" % distance) # 거리를 표시한다.

            
            

    q = Queue() # Queue() 함수를 q라는 변수에 넣는다.
    a = 0 # 0 이라는 값을 a 변수에 넣는다.
    
    # 초음파 센서와 컨베이어 벨트 모터를 동시에 사용하기 위해서 multiprocessing를 이용
    p1 = Process(target = sonic , args=(a,q)) # Process() 함수를 이용해 sonic 함수를 p1이라는 변수에 넣는다.
    p2 = Process(target = motor, args=(q,)) # Process() 함수를 이용해 motor 함수를 p2라는 변수에 넣는다.
        
    p1.start() # p1 함수를 시작 
    p2.start() # p2 함수를 시작
        
    q.close() # Queue 통로를 닫는다.
    q.join_thread() # 백그라운드 스레드에 넣는다.
      
    p1.join() # p1 프로세스가 종료 될 때 까지 대기시킴
    p2.join() # p2 프로세스가 종료 될 때 까지 대기시킴


