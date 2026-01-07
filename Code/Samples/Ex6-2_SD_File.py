from machine import Pin, SPI
import os
import sdcard

# 初始化 SPI1 及 sdcard
# 預設 SPI baudrate=100KHz, polarity=0, phase=0, bits=8, fristbit=SPI.MSB 
sd_spi = SPI(1, sck = Pin(10, Pin.OUT), mosi = Pin(11, Pin.OUT),
             miso = Pin(12, Pin.OUT))
sd = sdcard.SDCard(sd_spi, Pin(13, Pin.OUT)) # Pin 13 SD_CS

# 掛載 SD card 到 /sd 資料夾
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")
print("Mounted")

# --- 寫入 CSV 範例 ---
def write_csv(filename, data_list):
    # 'a' 代表 append (附加)，如果檔案不存在會自動創建
    with open("/sd/" + filename, "a") as f:
        # 將列表轉為以逗號分隔的字串，並加上換行符
        line = ",".join([str(x) for x in data_list])
        f.write(line + "\n")    
    f.close() # 關閉檔案
    print(data_list)
    print("CSV file has been successfully written.")

# --- 讀取 CSV 範例 ---
def read_csv(filename):
    print("Start read data :")
    with open("/sd/" + filename, "r") as f:
        for line in f:
            # 去除換行符並以逗號分割
            columns = line.strip().split(",")
            print(f"Time: {columns[0]}, Temp.: {columns[1]}°C, pressure: {columns[2]}hPa")
    f.close() # 關閉檔案
    print("CSV file has been successfully read.")
    
# 測試資料
sensor_data = ["2025-12-28 08:00", 25.4, 1013.2]

# 執行寫入與讀取
write_csv("data.csv", sensor_data)
read_csv("data.csv")

# 卸載 (安全移除建議)
os.umount("/sd")