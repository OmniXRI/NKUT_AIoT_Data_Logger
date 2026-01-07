from machine import Pin # 從 machine 中導入 Pin 類別
import utime # 導入時間相關類別

# 初始化輸出腳
LED_R = Pin(2, machine.Pin.OUT)  #設定GP2 為輸出腳 (LED1)
LED_G = Pin(3, machine.Pin.OUT)  #設定GP3 為輸出腳 (LED2)
RELAY = Pin(22, machine.Pin.OUT) #設定GP22為輸出腳 (RELAY)

# 令 紅綠 LED 全部熄滅，繼電器釋放激磁
LED_R.off()
LED_G.off()
RELAY.off()

Relay_State = 0 # 宣告變數儲存繼電器目前狀態，初始值為 0（釋放）

# 初始化 SW1 ~ SW4 輸入腳
SW1 =  Pin(9, Pin.IN, Pin.PULL_UP) # 設定GP9為SW1輸入腳，且自帶pull high電阻
SW2 =  Pin(8, Pin.IN, Pin.PULL_UP) # 設定GP8為SW2輸入腳，且自帶pull high電阻
SW3 =  Pin(7, Pin.IN, Pin.PULL_UP) # 設定GP7為SW3輸入腳，且自帶pull high電阻
SW4 =  Pin(6, Pin.IN, Pin.PULL_UP) # 設定GP6為SW4輸入腳，且自帶pull high電阻

# 測試按鍵 SW1 ~ SW4
# 按下 SW1 紅色 LED 亮，放開則滅。
# 按下 SW2 綠色 LED 亮直到 SW2 再次按下。
# 按下 SW3 繼電器激磁，按下 SW4 繼電器釋放。
  
while True: # 若真則循環
    # 依 SW1 按鍵反相狀態點亮/熄減紅色 LED
    # 當 SW1 按下時接地，讀值為 0
    LED_R.value(SW1.value() == 0)
  
    if (SW2.value() == 0): # 若 SW2 按下
        LED_G.toggle() # 綠色 LED 反轉狀態
        utime.sleep(0.01) # 延時0.01秒(10ms)，去除機械彈跳
    
        while(SW2.value() == 0): # 等待 SW2 放開
            pass
    
    if (SW3.value() == 0): # 若 SW3 按下
        Relay_State = 1 # 繼電器目前狀態設為 1（激磁）
      
    if (SW4.value() == 0): # 若 SW4 按下
        Relay_State = 0 # 繼電器目前狀態設為 0（釋放）
      
    RELAY.value(Relay_State) # 依繼電器目前狀態變更動作
  
    utime.sleep(0.01) # 延時0.01秒(10ms)，去除機械彈跳