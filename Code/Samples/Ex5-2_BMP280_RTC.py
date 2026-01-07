from machine import Pin, I2C # 從 machine 導入 Pin, I2C 類別
import utime   # 導入時間相關類別
import RTC_DS3231 # 導入 RTC DS3231 自定義類別
from bmp280 import BMP280I2C # 從 bmp280 導入 BMP280I2C 類別

# 初始化 DS3231 RTC 模組
# I2C1, SDA(GP14), SCL(GP15), 時脈頻率 100KHz, 位址 0x68
rtc = RTC_DS3231.RTC()

# 初始化 I2C0 及 BMP280 模組
i2c0_sda = Pin(4) # 設定 SDA 為 GP4
i2c0_scl = Pin(5) # 設定 SCL 為 GP5
i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl, freq=400000) # 時脈頻率 400KHz
bmp280_i2c = BMP280I2C(0x76, i2c0) # 預設 BMP280 I2C 位址 0x76

# 每隔一秒從 DS3231 RTC 讀出目前時間值及 BMP280 溫度及氣壓值並顯示 
while True:
    # 讀取 RTC 數值陣列 (Mode 0)
    # 輸出為[秒, 分, 時, 星期, 日, 月, 年]
    curr_t = rtc.DS3231_ReadTime(0)

    # 讀取 BMP280 量測值
    # 輸出為 't_adc' 溫度原始類比值, 't' 溫度值，'p' 氣壓值, 'p_adc' 氣壓原始類比值
    readout = bmp280_i2c.measurements

    # 產生溫度及氣壓值 CSV 格式化字串，.3f 表限制小數3位
    strBMP280 = (f"{curr_t[6]}/{curr_t[5]}/{curr_t[4]},{curr_t[2]}:{curr_t[1]}:{curr_t[0]}," 
                 f"{readout['t']:.3f},{readout['p']:.3f}") 
    print(strBMP280) # 顯示溫度及氣壓值字串
    utime.sleep(1.0) # 暫停 1 秒