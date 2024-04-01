import cv2
import numpy as np
import time
from datetime import datetime
import winsound
import serial
import pyautogui
import keyboard
import usb.core
import usb.util

def beep(frequency, duration):
    winsound.Beep(frequency, duration)

# 웹캠 연결
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)	# 연결된 카메라 프레임의 가로 크기 640으로 변경
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)	# 연결된 카메라 프레임의 세로 크기 480으로 변경
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)	# 연결된 카메라 프레임의 가로 크기 추출
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)	# 연결된 카메라 프레임의 세로 크기 추출
print('Caputered image width(W) is :', width)
print('Caputered image height(H) is :', height)

# 영상 녹화
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('Record_Video.avi', fourcc, 2.0, (1024,768))

# 캡처할 영상의 상단 부분 설정
monitor_top = 0
monitor_bottom = 368
#monitor_bottom = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)  # 상단 반쪽만 모니터링
#monitor_bottom = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 상단 반쪽만 모니터링
print('Half frame of Caputered Image :', monitor_bottom)

# 초기 프레임 캡처
ret, prev_frame = cap.read()
ref_prev_frame = prev_frame[monitor_top:monitor_bottom, :]

# 초기 시간 설정
start_time = time.time()

# -------------- loop -------------------------------------------------- 
while True:
    cv2.imshow('ref_prev_frame', ref_prev_frame)

    time.sleep(1)

    current_time = time.time()
    
    # 프레임 캡처
    ret, current_frame = cap.read()
    cv2.imshow('current_frame', current_frame)
    # 상단 부분 영상 추출
    current_top_region = current_frame[monitor_top:monitor_bottom, :]
    cv2.imshow('current_top_region', current_top_region)

    # 이전 프레임과 현재 상단 부분 영상 비교
    #difference = cv2.subtract(ref_prev_frame, current_top_region)
    difference = cv2.absdiff(ref_prev_frame, current_top_region)
    result = np.any(difference)

    # 이미지가 동일한지 확인
    if result:
        # 현재 상단 부분 영상이 이전과 다르면 이전 상단 부분 영상 업데이트
        start_time = time.time()
        ref_prev_frame = current_top_region
        print('OK')
    else:
        # 현재 상단 부분 영상이 이전과 같으면 시간 갱신
        current_time = time.time()
        print(datetime.now().strftime('%Y-%m-%d  %H:%M:%S'), 'Top Frame(50%) is not changed')

    # 10초 이상 동일한 화면이 지속되었는지 확인
    if current_time - start_time >= 15:
        beep(1000, 1000)

        print("상단 부분이 15초 이상 동일한 화면이 지속되었습니다.")
        #break

    # 프로그램 종료를 위한 키 입력 확인
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료
cap.release()
cv2.destroyAllWindows()
