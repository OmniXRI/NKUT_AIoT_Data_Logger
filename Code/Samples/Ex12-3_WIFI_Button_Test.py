from machine import Pin # 從 machine 導入 Pin 類別
import network # 導入網路類別
import socket # 導入通訊端點類別

# 初始化 GPIO
led = Pin(2, Pin.OUT)  # 紅色LED(GP2)

# 設定 WIFI 帳號密碼
ssid = '輸入 WIFI SSID'
password = '輸入 WIFI 密碼'

# 生成包含 LED 狀態和控制按鈕的 HTML 網頁
def get_html_with_buttons(led_state_value):   
    # 判斷 LED 狀態文字
    led_status_text = "🟢 ON" if led_state_value == 1 else "🔴 OFF"

    # 使用 GET 請求建立按鈕，這是最簡單的方式
    html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Pico W LED 控制</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; }}
                .status {{ font-size: 2em; margin-bottom: 30px; }}
                .button-container button {{ 
                    padding: 15px 30px; 
                    font-size: 1.5em; 
                    margin: 10px; 
                    cursor: pointer;
                    border: none;
                    border-radius: 5px;
                }}
                #on-btn {{ background-color: #4CAF50; color: white; }}
                #off-btn {{ background-color: #f44336; color: white; }}
            </style>
        </head>
        <body>
            <h1>Pico W LED 控制面板</h1>
            <div class="status">
                <h2>LED 狀態: {led_status_text}</h2>
            </div>
            <div class="button-container">
                <a href="/led/on">
                    <button id="on-btn">開啟 LED</button>
                </a>
                
                <a href="/led/off">
                    <button id="off-btn">關閉 LED</button>
                </a>
            </div>
        </body>
        </html>
        """
        
    # HTTP 回應頭
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"
    return response + html_content

# 初始化網路設定
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected() : # 等待網路連接 
    pass

print('IP: ', wlan.ifconfig()[0])  # 顯示開發板的IP位址

# 初始化 socket 並指定 port 80 最多五人排隊
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# 進入伺服器主循環
while True:
    try:
        cl, addr = s.accept()
        request = cl.recv(1024).decode('utf-8')
        
        # 解析請求路徑
        # 請求的第一行通常是 'GET /path/to/resource HTTP/1.1'
        request_line = request.split('\r\n')[0]
        try:
            url = request_line.split(' ')[1]
        except IndexError:
            # 處理空請求或格式錯誤
            url = "/" 

        # 執行命令邏輯
        command_executed = False
        
        if url == "/led/on":
            led.value(1) # 設定 LED 為 HIGH (開啟)
            print(">>> 執行命令: LED ON")
            command_executed = True
        elif url == "/led/off":
            led.value(0) # 設定 LED 為 LOW (關閉)
            print(">>> 執行命令: LED OFF")
            command_executed = True
        
        # 準備回應        
        # 獲取當前 LED 狀態
        current_led_state = led.value()
        
        # 如果是控制命令，需要導向回主頁面
        if command_executed:
             # HTTP 303 See Other: 告訴瀏覽器重導向到主頁，避免重複提交
             response = "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n"
        else:
             # 發送帶有按鈕的主頁面
             response = get_html_with_buttons(current_led_state)

        cl.send(response.encode())
        cl.close()
            
    except OSError as e:
        print('連線錯誤:', e)
        cl.close()
    except KeyboardInterrupt:
        print("\n伺服器停止。")
        s.close()
        break