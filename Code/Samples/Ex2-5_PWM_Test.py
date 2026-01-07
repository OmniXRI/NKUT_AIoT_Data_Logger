from machine import Pin, PWM # 從 machine 導入 Pin, PWM 類別
import utime # 導入時間相關類別

# 初始化 PWM
pwm = PWM(Pin(2)) # 紅色 LED
pwm.freq(1000) # 設定 PWM 工作頻率 1KHz

# 令紅色 LED 產生呼吸燈(漸明漸暗)數次效果
duty = 0 # 目前亮度值
direction = 1 # 數值遞增方向

for _ in range(8 * 256): # 遞增遞減次數
    duty += direction # 亮度值遞加或遞減
    
    if duty > 255: # 若目前亮度值大於 255
        duty = 255 # 則亮度值設為 255
        direction = -1 # 並使遞增方向為負
    elif duty < 0: # 若目前亮度值小於 0 
        duty = 0 # 則亮度值設為 0
        direction = 1 # 並使遞增方向為正
        
    pwm.duty_u16(duty * duty) # 設定工作週期
    utime.sleep(0.005) # 停止 0.005 (5ms) 秒 