from machine import Pin, PWM # 從 machine 導入 Pin, PWM 類別
import utime   # 導入時間相關類別

# 初始化 PWM
pwm = PWM(Pin(28)) # 設定 GP28 為 PWM 輸出腳
pwm.freq(50) # 設定PWM頻率為50 Hz

# 測試 PWM 控制 360度舵機， 令舵機正反轉兩次
for i in range(2):
    pwm.duty_ns(1000 * 1000) # 1ms PWM 脈波寬度，正方向高速旋轉
    utime.sleep(1.0) # 停止1秒    
    pwm.duty_ns(1500 * 1000) # 1.5ms PWM 脈波寬度，停止旋轉
    utime.sleep(1.0) # 停止1秒    
    pwm.duty_ns(2000 * 1000) # 2ms PWM 脈波寬度，反方向高速旋轉 
    utime.sleep(1.0) # 停止1秒    
    pwm.duty_ns(1500 * 1000) # 1.5ms PWM 脈波寬度，停止旋轉
    utime.sleep(1.0) # 停止1秒

