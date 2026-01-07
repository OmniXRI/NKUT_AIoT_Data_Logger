from machine import Pin, SPI # 從 machine 導入 Pin, SPI 類別
import ili9341 # 導入 ILI9341 LCD相關類別
from xglcd_font import XglcdFont # 從xglcd_font 導入點陣字 XglcdFont 類別
import mySetup # 導入 ili9341 及 xglcd_font 基本設定

# 建立SPI TFT LCD 實例
display = mySetup.createMyDisplay() # LCD 初始化
display.clear() # 清除畫面(全黑)

# 顯示人機介面所需 BIN/RAW 格式影像(只有RGB565數據，高位在前，沒有檔頭）
display.draw_image('/Images/page0-title.bin', 0, 0, 320, 20) # 繪製主畫面抬頭
display.fill_rectangle(0, 20, 320, 200, ili9341.color565(204, 255, 204)) # 主畫面底色
display.draw_image('/Images/page0-main.bin', 40, 40, 240, 160) # 繪製主畫面主圖示
display.draw_image('/Images/page0-pb1.bin', 0, 220, 80, 20) # 繪製主畫面按鍵一
display.draw_image('/Images/page0-pb2.bin', 80, 220, 80, 20) # 繪製主畫面按鍵二
display.draw_image('/Images/page0-pb3.bin', 160, 220, 80, 20) # 繪製主畫面按鍵三
display.draw_image('/Images/page0-pb4.bin', 240, 220, 80, 20) # 繪製主畫面按鍵四