from machine import Pin, UART # 從 machine 導入 Pin, UART 類別
import utime   # 導入時間相關類別
import sys
import select

# 初始化 LED 腳位為輸出 
LED_R = Pin(2, Pin.OUT)  #設定GP2 為輸出腳 (LED1)
# 初始化 SW 1
# 設定GP9為SW1輸入腳，且自帶pull high電阻
SW1 =  Pin(9, Pin.IN, Pin.PULL_UP) 
# 初始化 UART0 為 115200 bps, 無同位元(N), 8Bit 資料(8), 1 停止位元(1)
# 指定使用 UART0, TX Pin 0, RX Pin 1
uart0 = UART(0,baudrate=115200,tx=Pin(0),rx=Pin(1)) 

rxData = bytes() # 宣告接收字串空間

while True:
    # 若實體 UART 有接收到任何字元
    if uart0.any() > 0: 
        while uart0.any() > 0: # 若接收區還有任何字元
            rxData += uart0.read(1) # 從 UART 讀取一字元並累加到 rxData 中

        if (rxData == "LED_ON"):
            LED_R.on() # 點亮紅色 LED
        elif (rxData == "LED_OFF"):
            LED_R.off() # 熄滅紅色 LED
        else:
            print(rxData.decode('utf-8')) # 列印出接收到的字串，以 utf-8 格式顯示
    
    # 若透過虛擬串列埠有收到資料
    if select.select([sys.stdin], [], [], 0)[0]:
        # 讀取一行輸入並移除換行符號
        cmd = sys.stdin.readline().strip()
        
        if cmd == "LED_ON":
            LED_R.on() # 點亮紅色 LED
        elif cmd == "LED_OFF":
            LED_R.off() # 熄滅紅色 LED
        
        if cmd != "":           
            print(f"cmd: {cmd}") # 列印出接收到的原始字串（含換行字元）
    
    if(SW1.value() == 0): # 等待 SW1 按下(輸入為 Low)
        rxData = b'' # 清除 rxData 內容
        uart0.write(b'SW1 Pressed') # 從 UART0 輸出(寫入)字串
        utime.sleep(0.01) # 等待 10ms，消除機械彈跳
        
        while(SW1.value() == 0): # 等待 SW1 放開
            pass