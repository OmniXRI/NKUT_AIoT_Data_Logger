from machine import Pin, SPI # 從 machine 導入 Pin, SPI 類別
import utime   # 導入時間相關類別
import ili9341 # 導入 ILI9341 LCD相關類別
from xglcd_font import XglcdFont # 從xglcd_font 導入點陣字 XglcdFont 類別
import mySetup # 導入 ili9341 及 xglcd_font 基本設定

SW1 =  Pin(9, Pin.IN, Pin.PULL_UP) # 設定GP9為SW1輸入腳，且自帶pull high電阻
SW2 =  Pin(8, Pin.IN, Pin.PULL_UP) # 設定GP8為SW2輸入腳，且自帶pull high電阻
SW3 =  Pin(7, Pin.IN, Pin.PULL_UP) # 設定GP7為SW3輸入腳，且自帶pull high電阻
SW4 =  Pin(6, Pin.IN, Pin.PULL_UP) # 設定GP6為SW4輸入腳，且自帶pull high電阻

# 建立SPI TFT LCD 實例及引入二種尺寸字形
display = mySetup.createMyDisplay() # LCD 初始化
unispace = XglcdFont('./lib/Unispace12x24.c', 12, 24) # 建立 Unispace 12x24 點陣字形
#arcadepix = XglcdFont('./lib/ArcadePix9x11.c', 9, 11) # 建立 ArcadePix 9x11 點陣字形

display.clear() # 清除畫面(全黑)
FG_Color = ili9341.color565(255, 0, 0) # 文字前景顏色
BG_Color = ili9341.color565(255, 255, 0) # 文字背景顏色
Inv_FG_Color = ili9341.color565(0, 0, 255) # 文字前景反相顏色
Inv_BG_Color = ili9341.color565(0, 255, 255) # 文字背景反相顏色

# 測試按鍵 SW1 ~ SW4，未按顯示紅色文字黃色背景，依序按下顯示藍色文字青色背景
display.fill_rectangle(0, 216, 320, 24, BG_Color) # 清除文字區(填文字背景色)
display.draw_text( 22, 216, "SW1", unispace, FG_Color, BG_Color)
display.draw_text(102, 216, "SW2", unispace, FG_Color, BG_Color)
display.draw_text(182, 216, "SW3", unispace, FG_Color, BG_Color)
display.draw_text(262, 216, "SW4", unispace, FG_Color, BG_Color)
    
while True:   
    if (SW1.value() == 0): # 等待 SW1 按下(輸入為 Low)
#        display.fill_rectangle(0, 216, 80, 24, Inv_BG_Color) # 清除 SW1 文字區成背景反相色
        display.draw_text(22, 216, "SW1", unispace, Inv_FG_Color, Inv_BG_Color)
    else:
#        display.fill_rectangle(0, 216, 80, 24, BG_Color) # 清除 SW1 文字區成背景色
        display.draw_text( 22, 216, "SW1", unispace, FG_Color, BG_Color)
        
#     if (SW1.value() == 0): # 等待 SW1 按下(輸入為 Low)
#         display.fill_rectangle(0, 216, 80, 24, Inv_BG_Color) # 清除 SW1 文字區成背景反相色
#         display.draw_text(22, 216, "SW1", unispace, Inv_FG_Color, Inv_BG_Color) # 繪反相字串
#         utime.sleep(0.01) # 等待機械彈跳結束
#         
#         while (SW1.value() == 0): # 等待 SW1 放開(輸入為 High)
#             pass
#         
#         display.fill_rectangle(0, 216, 80, 24, BG_Color) # 清除 SW1 文字區成背景色
#         display.draw_text( 22, 216, "SW1", unispace, FG_Color, BG_Color) # 繪正常字串