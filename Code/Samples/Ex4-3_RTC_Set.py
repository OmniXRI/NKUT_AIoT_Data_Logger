from machine import I2C # 從 machine 導入 I2C 類別
import utime   # 導入時間相關類別
import RTC_DS3231 # 導入 RTC DS3231 自定義類別

# 初始化 DS3231 RTC 模組
# I2C1, SDA(GP14), SCL(GP15), 100KHz, Address: 0x68
rtc = RTC_DS3231.RTC()

# 同步系統時間到 RTC
def sync_time():
    # 獲取電腦時間，格式為 (年, 月, 日, 時, 分, 秒, 星期(0週一), 當年第幾天)
    t = utime.localtime()
    print("目前電腦時間:", t)
    
    # 十進制轉 BCD 格式，年只保留後兩位數即可
    year = rtc.dec2bcd(t[0]%100)
    month = rtc.dec2bcd(t[1])
    date = rtc.dec2bcd(t[2])
    day = rtc.dec2bcd(t[6])
    hour = rtc.dec2bcd(t[3])
    minite = rtc.dec2bcd(t[4])
    second = rtc.dec2bcd(t[5])
    
    # 寫入 DS3231 格式為 (秒, 分鐘, 小時, 星期, 日, 月, 年)
    NowTime = bytes([second, minite, hour, day, date, month, year])
    print("NowTIme:", " ".join([f"\\x{b:02x}" for b in NowTime])) # 顯示16進制數值   
    rtc.DS3231_SetTime(NowTime) # 寫入時間到 RTC
    print("時間已同步！")    

# 讀取 RTC 目前時間
def read_rtc():
    curr_t = rtc.DS3231_ReadTime(1)  # 讀取 RTC 時間並以：號格式化 (Mode 1)
    print("DS3231 當前時間:", curr_t)

# 執行同步並回讀顯示
sync_time()
read_rtc()