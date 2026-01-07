from machine import Pin # 從 machine 導入 Pin 類別
import time # 導入時間類別
import network # 導入網路類別
import socket # 導入通訊端點類別

# 初始化 GPIO
led = Pin(2, Pin.OUT)  # 紅色LED(GP2)
sw1 = Pin(9, Pin.IN, Pin.PULL_UP) # SW1(GP9)

# 設定 WIFI 帳號密碼
ssid = '輸入 WIFI SSID'
password = '輸入 WIFI 密碼'

# 設定伺服器
SERVER_PORT = 80 # 標準 HTTP 端口
MAX_CONNECTIONS = 1 # 伺服器一次處理的連線數量

# 連接到 Wi-Fi 網路並返回 WLAN 物件
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    print(f"正在連線到 {ssid}...")
    wlan.connect(ssid, password)
    
    max_wait = 10 # 最多等待 10 秒
    
    while max_wait > 0:
        if wlan.isconnected():
            break
        print(".", end="")
        time.sleep(1)
        max_wait -= 1
        
    if wlan.isconnected(): # 若連線成功
        status = wlan.ifconfig()
        print("\n✅ Wi-Fi 連線成功！")
        print("IP 地址:", status[0])
        return wlan
    else: 
        print("\n❌ Wi-Fi 連線失敗！")
        return None

# 根據 GPIO 狀態生成 HTML 網頁內容
def get_html_response(pin_status):
    # 依按鍵狀態產生對應字串
    status_text = "🟢 HIGH (Released / Idle)" if pin_status == 1 else "🔴 LOW (Pressed / Active)"

    # 配置 html 內容
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="refresh" content="3"> <title>Pico W GPIO 狀態</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; }}
                .status {{ font-size: 1em; margin-top: 50px; padding: 20px; border: 2px solid #ccc; display: inline-block; }}
                .ip-info {{ font-size: 1em; color: #888; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <h1>Raspberry Pi Pico W GPIO 狀態讀取</h1>
            <div class="status">
                <h2>GPIO 9 當前狀態:</h2>
                <p style="font-size: 2em;">{status_text}</p>
                <p>原始值: **{pin_status}**</p>
            </div>
            <p class="ip-info">伺服器 IP: {wlan.ifconfig()[0]}</p>
            <p>上次更新時間: {time.time()}</p>
        </body>
        </html>
        """
        
    # HTTP 回應頭 (必須)
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"
    return response + html

# 連接 Wi-Fi
wlan = connect_wifi(ssid, password)

if wlan is None:
    print("無法啟動伺服器，因為 Wi-Fi 連線失敗。")
else:
    # 建立 Socket 伺服器
    addr = socket.getaddrinfo('0.0.0.0', SERVER_PORT)[0][-1]    
    s = socket.socket()
    # 新增這行：設定 SO_REUSEADDR 屬性
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    s.bind(addr)
    s.listen(MAX_CONNECTIONS) # 監聽端口    
    print(f"Web 伺服器已啟動，正在監聽端口 {SERVER_PORT}...")
    print(f"請在瀏覽器中訪問: http://{wlan.ifconfig()[0]}/")

    while True:
        try:            
            cl, addr = s.accept() # 接受客戶端連線
            print(f"客戶端連線來自: {addr[0]}:{addr[1]}")

            request = cl.recv(1024) # 讀取請求
            # print("請求內容:\n", request)
            
            current_status = sw1.value() # 讀取 GPIO 狀態
            print(f"--- 讀取 SW1 狀態: {current_status} ---")
            
            # 準備並發送 HTTP 回應
            response = get_html_response(current_status)
            cl.send(response)
            
            # 關閉連線
            cl.close()
            
        except OSError as e:
            # 處理可能出現的錯誤，例如連線超時等
            cl.close()
            print('連線錯誤:', e)
        except KeyboardInterrupt:
            # 允許通過 Ctrl+C 退出
            print("\n伺服器停止。")
            break
        
    # 新增這行：確保主監聽 Socket 在程式退出前關閉
    print("正在關閉主監聽 Socket...")
    s.close()