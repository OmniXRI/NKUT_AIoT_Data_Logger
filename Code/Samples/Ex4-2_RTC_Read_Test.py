from machine import I2C # 從 machine 導入 I2C 類別
import utime   # 導入時間相關類別
import RTC_DS3231 # 導入 RTC DS3231 自定義類別

# 初始化 DS3231 RTC 模組
# I2C1, SDA(GP14), SCL(GP15), 100KHz, Address: 0x68
rtc = RTC_DS3231.RTC()

# 每隔 0.5秒 列印目前時間，共 6 次(3.0秒)
for i in range(6):
    curr_t = rtc.DS3231_ReadTime(1)  # 讀取 RTC 數值並以：號格式化 (Mode 1)
    utime.sleep(0.5)   
    print(curr_t)