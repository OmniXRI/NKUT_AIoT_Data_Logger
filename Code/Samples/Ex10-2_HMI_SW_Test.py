from machine import Pin, SPI # 從 machine 導入 Pin, SPI 類別
import ili9341 # 導入 ILI9341 LCD相關類別
from xglcd_font import XglcdFont # 從xglcd_font 導入點陣字 XglcdFont 類別
import mySetup # 導入 ili9341 及 xglcd_font 基本設定

page_num = 0 # 0:main, 1:Page1, 2:Page2, 3:Page3

SW1 =  Pin(9, Pin.IN, Pin.PULL_UP) # 設定GP9為SW1輸入腳，且自帶pull high電阻
SW2 =  Pin(8, Pin.IN, Pin.PULL_UP) # 設定GP8為SW2輸入腳，且自帶pull high電阻
SW3 =  Pin(7, Pin.IN, Pin.PULL_UP) # 設定GP7為SW3輸入腳，且自帶pull high電阻
SW4 =  Pin(6, Pin.IN, Pin.PULL_UP) # 設定GP6為SW4輸入腳，且自帶pull high電阻

# 建立SPI TFT LCD 實例
display = mySetup.createMyDisplay() # LCD 初始化
unispace = XglcdFont('./lib/Unispace12x24.c', 12, 24)
display.clear() # 清除畫面(全黑)

# 顯示人機介面所需 BIN/RAW 格式影像(只有RGB565數據，高位在前，沒有檔頭）
display.draw_image('/Images/page0-title.bin', 0, 0, 320, 20) # 繪製主畫面抬頭
display.fill_rectangle(0, 20, 320, 200, ili9341.color565(204, 255, 204)) # 主畫面底色
display.draw_image('/Images/page0-main.bin', 40, 40, 240, 160) # 繪製主畫面主圖示
display.draw_image('/Images/page0-pb1.bin', 0, 220, 80, 20) # 繪製主畫面按鍵一
display.draw_image('/Images/page0-pb2.bin', 80, 220, 80, 20) # 繪製主畫面按鍵二
display.draw_image('/Images/page0-pb3.bin', 160, 220, 80, 20) # 繪製主畫面按鍵三
display.draw_image('/Images/page0-pb4.bin', 240, 220, 80, 20) # 繪製主畫面按鍵四

while True:
    if SW1.value() == 0: # SW1 被按下(輸入為 Low)
        page_num = 0
        display.fill_rectangle(0, 20, 320, 200, ili9341.color565(204, 255, 204)) # 主畫面底色
        display.draw_image('/Images/page0-main.bin', 40, 40, 240, 160) # 繪製主畫面主圖示
    elif SW2.value() == 0: # SW2 被按下(輸入為 Low)
        page_num = 1
        display.fill_rectangle(0, 20, 320, 200, ili9341.color565(255, 255, 255)) # 主畫面底色
        display.draw_text(120, 100, "PAGE 1", unispace, ili9341.color565(255, 0, 0))
    elif SW3.value() == 0: # SW3 被按下(輸入為 Low)
        page_num = 2
        display.fill_rectangle(0, 20, 320, 200, ili9341.color565(255, 255, 255)) # 主畫面底色
        display.draw_text(120, 100, "PAGE 2", unispace, ili9341.color565(0, 255, 0))  
    elif SW4.value() == 0: # SW4 被按下(輸入為 Low)
        page_num = 3
        display.fill_rectangle(0, 20, 320, 200, ili9341.color565(255, 255, 255)) # 主畫面底色
        display.draw_text(120, 100, "PAGE 3", unispace, ili9341.color565(0, 0, 255))