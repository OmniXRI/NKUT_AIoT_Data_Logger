from machine import Pin, ADC # 從 machine 中導入 Pin, ADC 類別
import network # 導入網路類別
import time # 導入時間類別
from umqtt.simple import MQTTClient # 從 umqtt.simple 導入 MQTT_Client 類別 

# 初始化 ADC0(SVR1) 及電壓轉換因子
adc = ADC(0) # 設定連接到ADC0(GP26)，亦可寫成ADC(26)
factor = 3.3 / (65535) # 電壓轉換因子

# 設定 WIFI 帳號密碼
ssid = '輸入 WIFI SSID'
password = '輸入 WIFI 密碼'

# MQTT Broker 設定 (以 HiveMQ 為例)
MQTT_BROKER = "輸入 HiveMQ Cluster，例：xxxxxxx.s1.eu.hivemq.cloud"
MQTT_USER = "輸入已授權使用者名稱（非個人帳號）"
MQTT_PASS = "輸入已授權密碼（非個人密碼）"
MQTT_CLIENT_ID = "輸入任何身份名稱字串，例：PicoW_Sensor_01"

# 連接 WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)

while not wlan.isconnected():
    print("連線中...")
    time.sleep(1)
print("WiFi 已連線:", wlan.ifconfig())

# 連接 MQTT Broker (HiveMQ 雲端通常需要 SSL)
def connect_mqtt():
    # 使用 8883 埠進行 SSL 加密連線
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=8883, 
                        user=MQTT_USER, password=MQTT_PASS, ssl=True,
                        ssl_params={'server_hostname': MQTT_BROKER} )
    client.connect()
    return client

try:
    client = connect_mqtt()
    print("已成功連接至雲端 Broker")
    
    while True:
        # 讀取 ADC0(SVR1) 數據
        reading = adc.read_u16() # 讀取類比輸入值16bit無號整數
        vlot = reading * factor  # 將輸入值轉成電壓值
        volt_3 = f"Volt: {vlot:.3f} V " # 限制小數3位
        print(f"發布數據: {volt_3}") 
        client.publish("pico/sensor", str(vlot)) # 發布訊息到主題 (Topic)        
        time.sleep(3) # 每 3 秒上傳一次
except Exception as e:
    print("發生錯誤:", e)