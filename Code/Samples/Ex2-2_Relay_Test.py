from machine import Pin # 從 machine 中導入 Pin 類別
import utime # 導入時間相關類別

# 初始化 RELAY 腳位為輸出 
RELAY = Pin(22, machine.Pin.OUT) #設定GP22為輸出腳 (RELAY)

# 初始化 RELAY 狀態，令 RELAY 不激磁
RELAY.off() # 和 RELAY.value(0) 效果相同

# 令 RELAY 交替開關二次
for i in range(2):
    RELAY.on() # 激磁繼電器，和 RELAY.value(1) 效果相同
    utime.sleep(0.5) # 延時0.5秒
    
    RELAY.off() # 釋放繼電器 LED，和 RELAY.value(0) 效果相同
    utime.sleep(0.5) # 延時0.5秒