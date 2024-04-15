import time
import tkinter as tk
from wakeonlan import send_magic_packet

def main(mac_address, duration, times):
    """주요 동작 함수"""
    count = 0
    while times > 0 and not stop_flag:
        
        parsing_mac = mac_address.upper().replace("-", "").replace(":", "")
        print(parsing_mac)

        send_magic_packet(parsing_mac)  # 대상 컴퓨터의 MAC 주소를 입력하세요
        
        times -= 1
        count += 1
        if times == 0:
            break
        
        time.sleep(duration)                    

def start_test():
    """시작 버튼 클릭 시 실행되는 함수"""
    global stop_flag
    stop_flag = False  # 중지 플래그 초기화
    mac_address = mac_entry.get()
#    print(mac_address)
    duration = int(duration_entry.get())
    times = int(times_entry.get())
    main(mac_address, duration, times)

# Tkinter 창 생성
root = tk.Tk()
root.title("Wake On LAN Test")

# MAC 주소 입력 창
mac_label = tk.Label(root, text="MAC Address:")
mac_label.grid(row=0, column=0, padx=20, pady=10)
mac_entry = tk.Entry(root)
mac_entry.grid(row=0, column=1, padx=20, pady=10)

# Duration 입력 창
duration_label = tk.Label(root, text="Interval-delay (sec) :")
duration_label.grid(row=1, column=0, padx=20, pady=10)
duration_entry = tk.Entry(root)
duration_entry.grid(row=1, column=1, padx=20, pady=10)

# Times 입력 창
times_label = tk.Label(root, text="Number of tests (times) :")
times_label.grid(row=2, column=0, padx=20, pady=10)
times_entry = tk.Entry(root)
times_entry.grid(row=2, column=1, padx=20, pady=10)

# 시작 버튼
start_button = tk.Button(root, text="START", command=start_test)
start_button.grid(row=3, column=0, padx=30, pady=20)

stop_flag = False  # 중지 플래그 초기화
root.mainloop()
