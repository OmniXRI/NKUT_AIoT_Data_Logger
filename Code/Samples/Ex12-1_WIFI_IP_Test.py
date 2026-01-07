from machine import Pin # 從 machine 導入 Pin 類別
import socket # 導入 socket 類別
import network # 導入 network 類別

led = Pin(2, Pin.OUT)  # 指定控制開發板紅色LED(GP2)

ssid = '輸入 WIFI SSID'
password = '輸入 WIFI 密碼'

# 首頁的 HTML 碼，顯示 "Hello World !"
html = """<!DOCTYPE html>
<html>
  <head>
    <title>Pico W</title>
  </head>
  <body>
    <h1>Hello World!</h1>
  </body>
</html>
"""

# 初始化 network 並連線（Pi Pico 只能連線 2.4GHz WIFI）
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected() : # 等待連線成功
    pass

print('IP: ', wlan.ifconfig()[0])  # 顯示開發板的 IP 位址

# 初始化 socket 並指定 port 80 最多五人排隊
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# 偵聽用戶端連線
while True:
    try:
        client, addr = s.accept()
        req = client.recv(1024).decode('UTF-8')
        client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')

        if req.find('/led/on') == 4:  # 若連線請求字串包含'/led/on'
            client.send('<h1>LED ON!</h1>') # 顯示 LED ON! 字串
            led.value(1)  # 點亮 LED ，接腳設為高電位
        elif req.find('/led/off') == 4: # 若連線請求字串包含'/led/off'
            client.send('<h1>LED OFF!</h1>') # 顯示 LED OFF! 字串
            led.value(0) # 熄滅 LED ，接腳設為低電位
        else:
            client.send(html) # 回到首頁

        client.close() # 關閉連線

    except OSError as e:
        client.close()
        print('connection closed')
