from machine import Pin, ADC # 從 machine 中導入 Pin, ADC 類別
import utime # 導入時間相關類別

adc = ADC(0) # 設定連接到ADC0(GP26)，亦可寫成ADC(26)
factor = 3.3 / (65535) # 電壓轉換因子
    
while True:    
    reading = adc.read_u16() # 讀取類比輸入值16bit無號整數
    vlot = reading * factor  # 將輸入值轉成電壓值
    volt_3 = f"Volt: {vlot:.3f} V " # 限制小數3位
    print(volt_3) # 列印電壓值到電腦
    utime.sleep(1.0) # 延時0.1秒
