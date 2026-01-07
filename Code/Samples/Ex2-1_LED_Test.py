from machine import Pin # 從 machine 中導入 Pin 類別
import utime # 導入時間相關類別

# 初始化 LED 腳位為輸出 
LED_R = Pin(2, Pin.OUT)  #設定GP2 為輸出腳 (LED1)
LED_G = Pin(3, Pin.OUT)  #設定GP3 為輸出腳 (LED2)

# 初始化 LED 狀態，令 LED 全部熄滅
LED_R.off() # 和 LED_R.value(0) 效果相同
LED_G.off() # 和 LED_G.value(0) 效果相同

# 令 LED1(紅), LED2(綠) 交替閃爍二次
for i in range(2):
    LED_R.on() # 點亮紅色 LED，和 LED_R.value(1) 效果相同
    utime.sleep(0.5) # 延時0.5秒
    
    LED_R.off() # 熄滅紅色 LED，和 LED_R.value(0) 效果相同
    utime.sleep(0.5) # 延時0.5秒
    
    LED_G.toggle() # 令綠色 LED 狀態相反
    utime.sleep(0.5) # 延時0.5秒
    
    LED_G.toggle() # 令綠色 LED 狀態相反
    utime.sleep(0.5) # 延時0.5秒