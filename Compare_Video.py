import cv2
import numpy as np
import time
import winsound
import serial
import pyautogui
import keyboard
import usb.core
import usb.util

def beep(frequency, duration):
    winsound.Beep(frequency, duration)

# 웹캠/캡처 카드 장치 연결
cap = cv2.VideoCapture(0)

# 카메라의 프레임 설정 및 확인
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)	# 연결된 카메라 프레임의 가로 크기 1024으로 변경
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)	# 연결된 카메라 프레임의 세로 크기 768으로 변경
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)	# 연결된 카메라 프레임의 가로 크기 추출
print('Caputered image width(W) is :', width)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)	# 연결된 카메라 프레임의 세로 크기 추출
print('Caputered image height(H) is :', height)

# 영상 녹화
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('Record_Video.avi', fourcc, 2.0, (640,480))


# 캡처할 영상의 상단 부분 설정
monitor_top = 0
monitor_bottom = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#monitor_bottom = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)  # 상단에서 절반까지만의 화면을 모니터링
print('Half frame of Caputered Image :', monitor_bottom)

# 초기 시간 및 프레임 캡처
start_time = time.time()
ret, prev_frame = cap.read()
ref_prev_frame = prev_frame[monitor_top:monitor_bottom, :]

# -------------- loop -------------------------------------------------- 
while True:
    cv2.imshow('prev_frame', ref_prev_frame)
    time.sleep(1)

    current_time = time.time()
    
    # 프레임 캡처
    ret, current_frame = cap.read()
    # 상단 부분 영상 추출
    current_top_region = current_frame[monitor_top:monitor_bottom, :]
    cv2.imshow('current_top_region', current_top_region)

    # 이전 프레임과 현재 상단 부분 영상 비교
    difference = cv2.absdiff(ref_prev_frame, current_top_region)
    result = np.any(difference)
    print(result)

    # 이미지가 동일한지 확인
    if result:
        # 영상 비교 : 다름 > 기준 시간 및 프레임을 업데이트
        start_time = time.time()
        ref_prev_frame = current_top_region
    else:
        # 영상 비교 : 동일 프레임 > 현재시간을 업데이트 (현재시간 - 기준시간)
        current_time = time.time()

    # 15초 이상 동일프레임이 발생하면 비프음 발생 후 Break
    if current_time - start_time >= 15:
        beep(1000, 1000)
        print("상단 부분이 15초 이상 동일한 화면이 지속되었습니다.")
        break

    # 프로그램 종료를 위한 키 입력 확인
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료
cap.release()
cv2.destroyAllWindows()
