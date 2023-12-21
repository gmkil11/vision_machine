import cv2 # openCV 라이브러리를 가져온다.
import numpy as np # numpy 라이브러리를 np라는 이름으로 가져온다.

def cam():
    cap = cv2.VideoCapture(0) # cap 이라는 변수에 cv2 라이브러리에서 VideoCapture() 함수를 가져온다.
    progress = True # a라는 변수에 True라는 Bool값을 저장
    is_passed = None # is_passed라는 변수에 null값을 저장 
    cap.set(3, 1620) # 카메라 가로 프레임의 1620픽셀로 설정
    cap.set(4, 1080) # 카메라 세로 프레임의 1080픽셀로 설정

    # 메인 loop
    while True: # 계속 루프시킨다.
        _, frame = cap.read() # VideoCapture() 함수에서 frame을 받아온다. read() 함수는 카메라, 동영상에서 프레임을 받아올 수 있다. (_은 값을 무시하고 싶을 때 사용)
        
        # 벨트 크기
        belt = frame[1:1080 , 0 : 1620] # 벨트 프레임의 크기를 지정해준다. [y1, y2 : x1, x2]             # x1 =  , y1 = # 화면 보고 왼쪽 상단 끝 좌표
        gray_belt = cv2.cvtColor(belt, cv2.COLOR_BGR2GRAY ) # gray_belt 프레임의 배경을 회색으로 한다.   # x2 =  , y2 =  화면 보고 오른쪽 하단 끝 좌표
        _, threshold = cv2.threshold(gray_belt, 110, 255, cv2.THRESH_BINARY) # threshold 프레임에 110의 임계값을 설정하고, 이를 넘었을 시 255(흑백)으로 표시
        
        # 측정 함수
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)              # contours 변수에 cv2.findcontours를 이용해 threshold 프레임에서
        for cnt in contours:  # contours 리스트에서 요소를 꺼내 cnt에 저장하고 꺼낼 때 마다 코드를 반복한다.    # 흰 물체의 바깥 외곽선만 검출 후 꼭지점 좌표를 리스트 형태로 반환해 넣어준다.
            (x, y, w, h) = cv2.boundingRect(cnt) # cnt에서 받아온 꼭지점 좌표를 boundingRect() 함수를 이용해 사각형을 그리고 x,y,w,h 변수에 넣어준다.
            
            # 측정 구역
            area = cv2.contourArea(cnt) / 5 # cnt에서 받아온 좌표를 contourArea 함수를 통해 넓이를 구한 뒤 area라는 변수에 넣어준다. 
            carea = round(area) # area를 round라는 함수를 사용해 반올림시켜 carea 라는 변수에 넣는다.
            
            # 양품/불량 분류
            if (carea > 90000 and carea < 300000 ) or (carea > 1000 and carea < 50000)  : # carea가 90000보다 크거나 300000보다 작을시, 그리고 1000보다 크거나 50000 보다 작을시 불량
                cv2.rectangle(belt, (x, y), (x + w, y+ h), (0, 0, 255), 2) # x,y,w,h 값에 넣은 꼭짓점 좌표값을 연결시켜 빨간색 사각형을 만든다.
                cv2.putText(belt, str(area), (x, y), 1, 1, (0, 255, 0)) # 사각형 아래쪽에 carea를 표시한다.
                print ("측정된 불량품 물체의 너비 = %s" %carea) # 측정한 물체의 넓이를 터미널에 출력한다.
                progress = False # progress 변수에 False 값을 넣는다.
                is_passed = False # is_passed 변수에 True 값을 넣는다.

            elif carea >= 50000 and carea < 90000: # 50000 보다 크거나 같다 & 90000보다 작으면 양품
                cv2.rectangle(belt, (x, y), (x + w, y+ h), (255, 0, 0), 2) # x,y,w,h 값에 넣은 꼭짓점 좌표값을 연결시켜 파란색 사각형을 만든다.
                cv2.putText(belt, str(carea), (x, y), 1, 1, (0, 255, 0)) # 사각형 아래쪽에 carea를 표시한다
                print ("측정된 양품 물체의 너비 = %s" %carea) # 측정한 물체의 넓이를 터미널에 출력한다.
                progress = False # prgress 변수에 False 값을 넣는다.
                is_passed = True # is_passed 변수에 False 값을 넣는다.

            else: # 아무것도 측정되지 않았을 시 
                continue # 반복한다.
        
        if progress == False: # progress가 False일 시 
            break # while 문을 빠져나간다.
        
    cap.release() # 카메라를 끈다.
    return is_passed # is_passed 라는 값을 리턴시킨다.