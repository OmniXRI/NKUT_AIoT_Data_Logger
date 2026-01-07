from machine import Pin, I2C # 從 machine 導入 Pin, I2C 類別
import utime   # 導入時間相關類別
from bmp280 import BMP280I2C # 從 bmp280 導入 BMP280I2C 類別

# 初始化 I2C 及 BMP280
i2c0_sda = Pin(4) # 設定 SDA 為 GP4
i2c0_scl = Pin(5) # 設定 SCL 為 GP5
# 宣告 I2C0 SDA/SCL 腳位及時脈頻率 400KHz
i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
bmp280_i2c = BMP280I2C(0x76, i2c0) # 預設 BMP280 I2C 位址 0x76
print(bmp280_i2c)

# 每隔一秒從 BMP280 讀取溫度及氣壓值並顯示 
for i in range(3):
    readout = bmp280_i2c.measurements # 讀取 BMP280 量測值
    print(readout)
    # 產生溫度及氣壓值格式化字串，.3f 表限制小數3位
    strBMP280 = f"{readout['t']:.3f} deg. C, {readout['p']:.3f} hPa. " 
    print(strBMP280) # 顯示溫度及氣壓值字串
    utime.sleep(1.0) # 暫停 1 秒