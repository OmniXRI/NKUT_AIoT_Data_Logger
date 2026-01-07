from machine import Pin, SPI # 從 machine 導入 Pin, SPI 類別
import utime   # 導入時間相關類別
import ili9341 # 導入 ILI9341 LCD相關類別
from xglcd_font import XglcdFont # 從xglcd_font 導入點陣字 XglcdFont 類別
import mySetup # 導入 ili9341 及 xglcd_font 基本設定

color_k = ili9341.color565(0, 0, 0) # 黑
color_r = ili9341.color565(255, 0, 0) # 紅
color_y = ili9341.color565(255, 255, 0) # 黃
color_g = ili9341.color565(0, 255, 0) # 綠
color_c = ili9341.color565(0, 255, 255) # 洋青
color_b = ili9341.color565(0, 0, 255) # 藍
color_m = ili9341.color565(255, 0, 255) # 洋紅
color_w = ili9341.color565(255, 255, 255) # 白

# 建立SPI TFT LCD 實例及引入二種尺寸字形
display = mySetup.createMyDisplay() # LCD 初始化
unispace = XglcdFont('./lib/Unispace12x24.c', 12, 24) # 建立 Unispace 12x24 點陣字形
#arcadepix = XglcdFont('./lib/ArcadePix9x11.c', 9, 11) # 建立 ArcadePix 9x11 點陣字形
display.clear() # 清除畫面(全黑)

# 測試文字顯示，unispace字形的藍色字串於(0, 0)位置
display.draw_text(0, 0, "LCD Graphic Test !", unispace, color_b) 

display.draw_pixel(160, 120, color_w) # 繪白點在 (160,120)
display.draw_line(100, 60, 220, 180, color_y) #繪黃線從(100,60)到(220,180)
display.draw_circle(160, 120, 50, color_r) # 繪紅圓圓心(160,120)半徑50
display.draw_ellipse(160, 120, 100, 80, color_g) # 繪綠色橢圓圓心(160,120)長軸100短軸80
display.draw_rectangle(100, 60, 120, 120, color_c) # 繪青色矩形從(100,60)寬120高120
display.draw_polygon(5, 160,120, 30, color_b, 15) # 繪藍色五邊形圓心(160,120)半徑30旋轉15度
utime.sleep(1.0) # 暫停1秒

display.fill_circle(50, 50, 20, color_r) # 繪紅實心圓圓心(50,50)半徑20
display.fill_ellipse(270, 50, 20, 10, color_y) # 繪綠色實心橢圓圓心(270,500)長軸20短軸10
display.fill_rectangle(50, 180, 20, 20, color_c) # 繪青色實心矩形從(50,180)寬20高20
display.fill_polygon(5, 270, 190, 10, color_b, 15) # 繪藍色五邊形圓心(270,190)半徑10旋轉15度
utime.sleep(1.0) # 暫停1秒

# 繪製灰階條分成32段
for i in range(32):
    color_step = 8 # 256/32
    color_gray = ili9341.color565(i*color_step, i*color_step, i*color_step)
    display.fill_rectangle(i*color_step, 220, color_step, 20, color_gray)