from machine import Pin, ADC, SPI # 從 machine 導入 Pin, SPI 類別
import utime   # 導入時間相關類別
import ili9341 # 導入 ILI9341 LCD相關類別
from xglcd_font import XglcdFont # 從xglcd_font 導入點陣字 XglcdFont 類別
import mySetup # 導入 ili9341 及 xglcd_font 基本設定

# LED GPIO 初始化
LED_R = Pin(2, Pin.OUT)  #設定GP2 為輸出腳 (LED1)
LED_G = Pin(3, Pin.OUT)  #設定GP3 為輸出腳 (LED2)
LED_R.off()
LED_G.off()

# SVR1 (ADC0) 初始化
adc = ADC(0) # 設定連接到ADC0(GP26)，亦可寫成ADC(26)
factor = 3.3 / (65535) # 電壓轉換因子

# 建立SPI TFT LCD 實例及引入二種尺寸字形
display = mySetup.createMyDisplay() # LCD 初始化
unispace = XglcdFont('./lib/Unispace12x24.c', 12, 24) # 建立 Unispace 12x24 點陣字形
#arcadepix = XglcdFont('./lib/ArcadePix9x11.c', 9, 11) # 建立 ArcadePix 9x11 點陣字形

display.clear() # 清除畫面(全黑)
FG_Color = ili9341.color565(255, 255, 255) # 文字前景顏色
BG_Color = ili9341.color565(0, 0, 0) # 文字背景顏色
OK_Color = ili9341.color565(0, 255, 0) # OK 文字背景顏色
NG_Color = ili9341.color565(255, 0, 0) # OK 文字背景顏色

while True:  
    reading = adc.read_u16() # 讀取類比輸入值16bit無號整數
    volt = reading * factor  # 將輸入值轉成電壓值
    volt_3 = f"Volt: {volt:.3f} V " # 限制小數3位
#    display.fill_rectangle(0, 90, 320, 24, BG_Color) # 清除文字區
    
    if (volt > 2.0): # 若 ADC 輸入電壓大於 2.0V
        LED_G.off() # 關閉綠色 LED
        LED_R.on() # 開啟紅色LED
        display.draw_text(0, 90, volt_3, unispace, FG_Color, NG_Color)
    else:
        LED_G.on() # 開啟綠色LED
        LED_R.off() # 關閉紅色 LED
        display.draw_text(0, 90, volt_3, unispace, FG_Color, OK_Color)

    utime.sleep(1.0) # 暫停 1 秒