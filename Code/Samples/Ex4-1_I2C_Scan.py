from machine import Pin, I2C
import time

# 選擇 I2C 編號並設置正確的 I2C 腳位
I2C_SDA_PIN = 14 
I2C_SCL_PIN = 15 
I2C_ID = 1

# 初始化 I2C
i2c = I2C(I2C_ID, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=400000)
print(i2c)

print("--- I2C Start Scan ---")
devices = i2c.scan() # 取得裝置位址

if devices: # 若有找到 
    print(f"Find {len(devices)} I2C Device:")
    for device in devices:
        print(f"  Hex Address: {hex(device)}")
else:
    print("No find any I2C Device !")
    
print("--- I2C Stop Scan ---")