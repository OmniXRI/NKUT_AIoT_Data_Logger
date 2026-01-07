from machine import Pin, SPI # 從 machine 導入 Pin, SPI 類別
import utime   # 導入時間相關類別
import ili9341 # 導入 ILI9341 LCD相關類別
from xglcd_font import XglcdFont # 從xglcd_font 導入點陣字 XglcdFont 類別
import mySetup # 導入 ili9341 及 xglcd_font 基本設定

color_b = ili9341.color565(0, 0, 255) # 藍

# 建立SPI TFT LCD 實例及引入二種尺寸字形
display = mySetup.createMyDisplay() # LCD 初始化
unispace = XglcdFont('./lib/Unispace12x24.c', 12, 24) # 建立 Unispace 12x24 點陣字形
#arcadepix = XglcdFont('./lib/ArcadePix9x11.c', 9, 11) # 建立 ArcadePix 9x11 點陣字形
display.clear() # 清除畫面(全黑)

# 測試文字顯示，unispace字形的藍色字串於(0, 0)位置
display.draw_text(0, 200, "LCD Image Test !", unispace, color_b)

# 測試影像顯示，BIN/RAW 格式影像(只有RGB565數據，高位在前，沒有檔頭）
# 顯示於(0, 0)位置，影像大小寬80，高80像素
display.draw_image('/Images/omnixri_logo_160.bin', 0, 0, 160, 160)
# display.draw_image('/Images/omnixri_logo_80.bin', 0, 0, 80, 80)
