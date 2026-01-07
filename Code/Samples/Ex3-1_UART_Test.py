from machine import Pin, UART # 從 machine 導入 Pin, UART 類別
import utime   # 導入時間相關類別

# 初始化 UART0 為 115200 bps, 無同位元(N), 8Bit 資料(8), 1 停止位元(1)
# 指定使用 UART0, TX Pin 0, RX Pin 1
uart0 = UART(0,baudrate=115200,tx=Pin(0),rx=Pin(1)) 

# 測試 UART0 發射及接收功能，將 Tx(GP0) / Rx(GP1) 短路
uart0.write("UART OK\n\r") # 從 UART0 輸出(寫入)字串
utime.sleep(0.1) # 等待0.1秒
rxData = bytes() # 宣告接收字串空間

if uart0.any() > 0: # 若有接收到任何字元
    while uart0.any() > 0: # 若接收區還有任何字元
        rxData += uart0.read(1) # 從 UART 讀取一字元並累加到 rxData 中

    print(rxData) # 列印出接收到的原始字串（含換行字元）
    print(rxData.decode('utf-8')) # 列印出接收到的字串，以 utf-8 格式顯示
else:
    print("No data received !"); # 列印沒收到資料訊息