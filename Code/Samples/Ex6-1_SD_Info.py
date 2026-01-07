from machine import Pin, SPI
import os
import sdcard

# 初始化 SPI1 及 sdcard
# 預設 SPI baudrate=100KHz, polarity=0, phase=0, bits=8, fristbit=SPI.MSB 
sd_spi = SPI(1, sck = Pin(10, Pin.OUT), mosi = Pin(11, Pin.OUT),
             miso = Pin(12, Pin.OUT))
sd = sdcard.SDCard(sd_spi, Pin(13, Pin.OUT)) # Pin 13 SD_CS

# 掛載 SD card 到 / 資料夾
os.mount(sd, '/') 
print(os.listdir("/")) #列出SD卡的檔案清單
print("Mounted")

# 取得 SD 卡基本資料
# 回傳: (block_size, fragment_size, blocks, bfree,
#        bavail, files, ffree, favail, flag, namemax)
stats = os.statvfs("/") 
print(stats)

# 計算 SD 卡容量
block_size = stats[0] # 區塊大小
total_blocks = stats[2] # 總區塊數
total_size_bytes = block_size * total_blocks # 計算總容量(Byte)
total_size_gb = total_size_bytes / (1024 * 1024 * 1024) #計算總容量(GByte)
print(f"Total Size: {total_size_gb:.2f} GB")