#import machine # 導入Pi Pico硬體參數設定類別
#led = machine.Pin(25, machine.Pin.OUT) # Pi Pico 設定GP25為輸出腳

from machine import Pin # 從 machine 中導入 Pin 類別
import utime # 導入時間相關類別

# Pi Pico W 使用 "LED" 字串會讓 MicroPython 自動尋找 LED 正確的腳位
led = Pin("LED", Pin.OUT) # 設定為輸出腳

while True: # 若真則循環
    led.value(1) # 點亮LED
    utime.sleep(0.5) # 延時0.5秒
    led.value(0) # 熄滅LED
    utime.sleep(0.5) # 延時0.5秒