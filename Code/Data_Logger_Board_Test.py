"""
資料收集器開發板測試程式
by Jack OmniXRI, 2025/12/12, version 1.0

測試項目：

1. SPI ILI9341 LCD 點亮測試，畫面依序全紅、全綠、全藍、全白、全黑，再出現待測試項目文字。
2. 測試 SW1 ~ SW4，依序按下時 LCD 上對應的紅字變綠字。
3. 測試 LED1(紅), LED2(綠), 交替閃爍兩次，間隔 0.5秒。
4. 測試 RELAY，交替開關兩次，間隔 0.5秒。
5. 讀取 SVR1 ADC0 讀值並顯示在 LCD，3秒內可任意調整旋鈕 。
6. 讀取 RTC 數值並顯示在 LCD 上，停留3秒觀測數值變化。。
7. 插入 SD 卡讀取容量並顯示在 LCD 。
8. J5 插入 360度舵機，依序正轉、反轉1秒後停止。
9. J4 插入 UART 測試線，TX, RX 短路，發出測試字串“UART OK\n\r"並顯示在 LCD 上。
10. J7 插入 BMP280 溫度氣壓模組，將讀值顯示在 LCD 上。
11. 開啟手機 WIFI 分享，SSID 設為 OmniXRI, 密碼 abcd1234，將工作位址 IP 顯示在 LCD 上。
12. 完成開發板基本功能測試，在 LCD 上顯示結束字串。

"""
from machine import Pin, ADC, PWM, I2C, SPI, UART
from sys import implementation
from os import uname
import utime   # 導入時間相關類別
from bmp280 import BMP280I2C 
import ili9341
from xglcd_font import XglcdFont
import mySetup
import RTC_DS3231
import sdcard
import os
import socket
import network

# 初始化 GPIO 
# LED_B = Pin(25, Pin.OUT) #設定GP25為輸出腳 (Pi Pico LED)

# Pi Pico W 使用 "LED" 字串會讓 MicroPython 自動尋找 LED 正確的腳位
LED_B = Pin("LED", Pin.OUT) # 設定為輸出腳
LED_R = Pin(2, Pin.OUT)  #設定GP2 為輸出腳 (LED1)
LED_G = Pin(3, Pin.OUT)  #設定GP3 為輸出腳 (LED2)
RELAY = Pin(22, Pin.OUT) #設定GP22為輸出腳 (RELAY)

LED_B.off()
LED_R.off()
LED_G.off()
RELAY.off()

SW1 =  Pin(9, Pin.IN, Pin.PULL_UP) # 設定GP9為SW1輸入腳，且自帶pull high電阻
SW2 =  Pin(8, Pin.IN, Pin.PULL_UP) # 設定GP8為SW2輸入腳，且自帶pull high電阻
SW3 =  Pin(7, Pin.IN, Pin.PULL_UP) # 設定GP7為SW3輸入腳，且自帶pull high電阻
SW4 =  Pin(6, Pin.IN, Pin.PULL_UP) # 設定GP6為SW4輸入腳，且自帶pull high電阻

# print(implementation.name) # micropython
# print(uname()[3]) # UF2 Version
# print(uname()[4]) # Board Name
# print(SPI(0)) # for LCD
# print(SPI(1)) # for SD

print('Board Inital Start ...\n')

# 建立SPI TFT LCD 實例及引入二種尺寸字形
display = mySetup.createMyDisplay()
unispace = XglcdFont('./lib/Unispace12x24.c', 12, 24)
arcadepix = XglcdFont('./lib/ArcadePix9x11.c', 9, 11)

# 1. 測試 LCD 畫面色彩切換
display.fill_rectangle(0, 0, 320, 240, ili9341.color565(255, 0, 0)) # 畫面全紅
utime.sleep(0.5)     # 延時0.5秒
display.fill_rectangle(0, 0, 320, 240, ili9341.color565(0, 255, 0)) # 畫面全綠
utime.sleep(0.5)     # 延時0.5秒
display.fill_rectangle(0, 0, 320, 240, ili9341.color565(0, 0, 255)) # 畫面全藍
utime.sleep(0.5)     # 延時0.5秒
display.clear() # 清除畫面(全黑)

# 顯示開始測試字串
display.draw_text(0, 216, "== Data Logger Board Test ==", unispace,
                  ili9341.color565(255, 255, 255))

# 顯示 LOGO
display.draw_image('/Images/omnixri_logo_80.bin', 240, 0, 80, 80)

# 顯示 LCD 名稱、執行程式名稱及版本
print(implementation.name) # micropython
print(uname()[3]) # UF2 Version
print(uname()[4]) # Board Name
print(ili9341.__name__) # LCD Name

display.draw_text(0, 0, ili9341.__name__, arcadepix,
                  ili9341.color565(255, 255, 255))
display.draw_text(60, 0, ili9341.implementation.name, arcadepix,
                  ili9341.color565(255, 255, 255))
display.draw_text(150, 0, str(ili9341.implementation.version), arcadepix,
                  ili9341.color565(255, 255, 255))
display.draw_text(0, 18, "LCD Inital Done !", arcadepix,
                  ili9341.color565(0, 255, 0))

print('LCD Inital Done !\n')

# 2. 測試按鍵 SW1 ~ SW4，未按顯示紅色文字，依序按下顯示綠色文字
display.fill_rectangle(0, 36, 240, 12, ili9341.color565(0, 0, 0)) # 清除文字區
display.draw_text(0, 36, "SW1", arcadepix,
                  ili9341.color565(255, 0, 0))
display.draw_text(60, 36, "SW2", arcadepix,
                  ili9341.color565(255, 0, 0))
display.draw_text(120, 36, "SW3", arcadepix,
                  ili9341.color565(255, 0, 0))
display.draw_text(180, 36, "SW4", arcadepix,
                  ili9341.color565(255, 0, 0))
    
while (SW1.value() == 1): # 等待 SW1 按下(輸入為 Low)
    pass

display.draw_text(0, 36, "SW1", arcadepix,
                  ili9341.color565(0, 255, 0))
        
while (SW2.value() == 1): # 等待 SW2 按下(輸入為 Low)
    pass

display.draw_text(60, 36, "SW2", arcadepix,
                  ili9341.color565(0, 255, 0))
        
while (SW3.value() == 1): # 等待 SW3 按下(輸入為 Low)
    pass

display.draw_text(120, 36, "SW3", arcadepix,
                  ili9341.color565(0, 255, 0))
        
while (SW4.value() == 1): # 等待 SW4 按下(輸入為 Low)
    pass

display.draw_text(180, 36, "SW4", arcadepix,
                  ili9341.color565(0, 255, 0))
    
display.fill_rectangle(0, 36, 240, 12, ili9341.color565(0, 0, 0)) # 清除文字區
display.draw_text(0, 36, "SW Test Done !", arcadepix,
                  ili9341.color565(0, 255, 0))    
print('SW Test Done !\n')

# 3. 測試 LED1(紅), LED2(綠) 交替閃爍二次
for i in range(2):
    LED_R.on()
    display.draw_text(0, 54, "R ON  ", arcadepix,
                  ili9341.color565(255, 255, 255))
    utime.sleep(0.5)
    
    LED_R.off()
    display.draw_text(0, 54, "R OFF ", arcadepix,
                  ili9341.color565(255, 255, 255))
    utime.sleep(0.5)
    
    LED_G.on()
    display.draw_text(0, 54, "G ON  ", arcadepix,
                  ili9341.color565(255, 255, 255))
    utime.sleep(0.5)
    
    LED_G.off()
    display.draw_text(0, 54, "G OFF ", arcadepix,
                  ili9341.color565(255, 255, 255))
    utime.sleep(0.5)

display.fill_rectangle(0, 54, 240, 12, ili9341.color565(0, 0, 0)) # 清除文字區
display.draw_text(0, 54, "LED Test Done !", arcadepix,
                  ili9341.color565(0, 255, 0))    
print('LED Test Done !\n')

# 4. 測試 RELAY 開關兩次
for i in range(2):
    RELAY.on()
    display.draw_text(0, 72, "RELAY ON  ", arcadepix,
                  ili9341.color565(255, 255, 255))
    utime.sleep(0.5)
    
    RELAY.off()
    display.draw_text(0, 72, "RELAY OFF ", arcadepix,
                  ili9341.color565(255, 255, 255))
    utime.sleep(0.5)

display.fill_rectangle(0, 72, 240, 12, ili9341.color565(0, 0, 0)) # 清除文字區
display.draw_text(0, 72, "RELAY Test Done !", arcadepix,
                  ili9341.color565(0, 255, 0))    
print('RELAY Test Done !\n')

# 5. 測試 SVR1 (ADC0) 數值 3 秒
adc = ADC(0) # 設定連接到ADC0(GP26)，亦可寫成ADC(26)
factor = 3.3 / (65535) # 電壓轉換因子
display.fill_rectangle(0, 90, 320, 12, ili9341.color565(0, 0, 0)) # 清除文字區
    
for i in range(30):    
    reading = adc.read_u16() # 讀取類比輸入值16bit無號整數
    volt = reading * factor  # 將輸入值轉成電壓值
    volt_3 = f"Volt: {volt:.3f} V " # 限制小數3位
    display.draw_text(0, 90, volt_3, arcadepix,
                  ili9341.color565(255, 255, 255))    
    utime.sleep(0.1)         # 延時0.1秒

display.fill_rectangle(0, 90, 320, 12, ili9341.color565(0, 0, 0)) # 清除文字區
display.draw_text(0, 90, "SVR1 (ADC0) Test Done ! " + volt_3, arcadepix,
                  ili9341.color565(0, 255, 0))
print(volt_3)
print('SVR1 (ADC0) Test Done !\n')

# 6. 測試 RTC 讀值並更新3秒
rtc = RTC_DS3231.RTC()
display.fill_rectangle(0, 108, 320, 12, ili9341.color565(0, 0, 0)) # 清除文字區
display.draw_text(0, 108, "Date / Time : ", arcadepix,
                  ili9341.color565(255, 255, 255)) 

for i in range(6):
    curr_t = rtc.DS3231_ReadTime(1)  # 讀取 RTC 數值並以：號格式化 (Mode 1)
    display.draw_text(100, 108, curr_t, arcadepix,
                  ili9341.color565(255, 255, 255))
    utime.sleep(0.5)
    
display.fill_rectangle(0, 108, 320, 12, ili9341.color565(0, 0, 0)) # 清除文字區
display.draw_text(0, 108, "RTC Test Done ! " + curr_t, arcadepix,
                  ili9341.color565(0, 255, 0))
print(curr_t)
print('RTC Test Done !\n')

# 7. 測試 SD 卡讀取容量並顯示
# FAT16 Sector Size 2048 Byte
# FAT32 Sector Size 4096 Byte

# 建立 SPI1 及 SD 實例
sd_spi = SPI(1, sck = Pin(10, Pin.OUT), mosi = Pin(11, Pin.OUT),
            miso = Pin(12, Pin.OUT))
sd = sdcard.SDCard(sd_spi, Pin(13, Pin.OUT)) # Pin 13 SD_CS

# 掛載 SD card 到 / 資料夾
os.mount(sd, '/')
print(os.listdir("/"))  #列出SD卡的檔案清單
print("Mounted")

SD_Size = "Size: {} MB".format(sd.sectors/4096)

print(SD_Size)
display.fill_rectangle(0, 126, 320, 12, ili9341.color565(0, 0, 0)) # 清除文字區
display.draw_text(0, 126, "SD Test Done ! " + SD_Size, arcadepix,
                  ili9341.color565(0, 255, 0))
print('SD Test Done !\n')

# 8. 測試 PWM 控制 360度舵機
pwm = PWM(Pin(28)) # 設定 GP28 為 PWM 輸出腳
pwm.freq(50) # 設定PWM頻率為50 Hz

for i in range(2):
    pwm.duty_ns(1000 * 1000) # 1ms PWM 脈波寬度，正方向高速旋轉
    display.draw_text(0, 144, "CW   ", arcadepix,
                  ili9341.color565(255, 255, 255))
    utime.sleep(1.0)
    
    pwm.duty_ns(1500 * 1000) # 1.5ms PWM 脈波寬度，停止
    display.draw_text(0, 144, "STOP ", arcadepix,
                  ili9341.color565(255, 255, 255))
    utime.sleep(1.0)
    
    pwm.duty_ns(2000 * 1000) # 2ms PWM 脈波寬度，反方向高速旋轉
    display.draw_text(0, 144, "CCW  ", arcadepix,
                  ili9341.color565(255, 255, 255))    
    utime.sleep(1.0)
    
    pwm.duty_ns(1500 * 1000) # 1.5ms PWM 脈波寬度，停止
    display.draw_text(0, 144, "STOP ", arcadepix,
                  ili9341.color565(255, 255, 255))
    utime.sleep(1.0)

display.fill_rectangle(0, 144, 320, 12, ili9341.color565(0, 0, 0)) # 清除文字區
display.draw_text(0, 144, "PWM Test Done !", arcadepix,
                  ili9341.color565(0, 255, 0))
print('PWM Test Done !\n')

# 9. 測試 UART0
uart = UART(0,baudrate=115200,tx=Pin(0),rx=Pin(1)) # 指定使用 UART0, TX Pin 0, RX Pin 1

uart.write("UART OK") # 從 UART0 輸出字串
uart_result_string = "UART Test Fail ! "
uart_result_color = ili9341.color565(255, 0, 0) 

if uart.any() > 0: # 若有接收到任何資料
    print(uart.any())
    raw_string = uart.read(7)
    decoded_string = raw_string.decode('utf-8')
    print(decoded_string)  
    
    if (decoded_string == "UART OK"):
        uart_result_string = "UART Test Done ! " + decoded_string
        uart_result_color = ili9341.color565(0, 255, 0)
  
display.fill_rectangle(0, 162, 320, 12, ili9341.color565(0, 0, 0)) # 清除文字區
display.draw_text(0, 162, uart_result_string, arcadepix, uart_result_color)        
print('UART Test Done !\n')

# 10. 測試 I2C 感測器 BMP280，讀出溫度及氣壓值，讀3秒
i2c0_sda = Pin(4)
i2c0_scl = Pin(5)
i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
bmp280_i2c = BMP280I2C(0x76, i2c0)
print(bmp280_i2c)

for i in range(3):
    readout = bmp280_i2c.measurements
    strBMP280 = f"{readout['t']:.3f} deg. C, {readout['p']:.3f} hPa. "# 限制小數3位
    display.draw_text(0, 180, strBMP280, arcadepix,
                  ili9341.color565(255, 255, 255))
    print(strBMP280)
    utime.sleep(1.0)

display.fill_rectangle(0, 180, 320, 12, ili9341.color565(0, 0, 0)) # 清除文字區
display.draw_text(0, 180, "I2C (BMP280) Test Done ! " + f"{readout['t']:.3f} deg. C", arcadepix,
                  ili9341.color565(0, 255, 0))
print('I2C (BMP280) Test Done !\n')

# 11. 測試 WIFI ，顯示 IP
ssid = 'OmniXRI'
password = 'abcd1234'
wifi_result_string = "WIFI Test FAIL !"
wifi_result_color = ili9341.color565(255, 0, 0)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# 若 3 秒內沒連上就判定失敗
for i in range(6):
    if wlan.isconnected() :
        print('IP: ', wlan.ifconfig()[0])  # 顯示開發板的IP位址
        wifi_result_string = "WIFI Test Done ! IP : " + wlan.ifconfig()[0]
        wifi_result_color = ili9341.color565(0, 255, 0)
        break
    utime.sleep(0.5)

display.fill_rectangle(0, 198, 320, 12, ili9341.color565(0, 0, 0)) # 清除文字區
display.draw_text(0, 198, wifi_result_string, arcadepix, wifi_result_color)
print('WIFI Test Done !\n')

# 12. 顯示測試結束字串
display.draw_text(0, 216, "Data Logger Board Test Done ", unispace,
                  ili9341.color565(255, 255, 0))
print("Data Logger Board Test Done !")