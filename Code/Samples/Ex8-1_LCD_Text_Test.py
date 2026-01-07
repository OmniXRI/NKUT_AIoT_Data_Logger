from machine import Pin, SPI # 從 machine 導入 Pin, SPI 類別
import utime   # 導入時間相關類別
import ili9341 # 導入 ILI9341 LCD相關類別
from xglcd_font import XglcdFont # 從xglcd_font 導入點陣字 XglcdFont 類別
import mySetup # 導入 ili9341 及 xglcd_font 基本設定

# 建立SPI TFT LCD 實例及引入二種尺寸字形
display = mySetup.createMyDisplay() # LCD 初始化
unispace = XglcdFont('./lib/Unispace12x24.c', 12, 24) # 建立 Unispace 12x24 點陣字形
arcadepix = XglcdFont('./lib/ArcadePix9x11.c', 9, 11) # 建立 ArcadePix 9x11 點陣字形

# 測試 LCD 畫面色彩切換（色彩填充）
display.fill_rectangle(0, 0, 320, 240, ili9341.color565(255, 0, 0)) # 畫面全紅
utime.sleep(0.5)     # 延時0.5秒
display.fill_rectangle(0, 0, 320, 240, ili9341.color565(0, 255, 0)) # 畫面全綠
utime.sleep(0.5)     # 延時0.5秒
display.fill_rectangle(0, 0, 320, 240, ili9341.color565(0, 0, 255)) # 畫面全藍
utime.sleep(0.5)     # 延時0.5秒
display.clear() # 清除畫面(全黑)

# 測試文字顯示
display.draw_text(0, 0, "Hello World !", unispace,
                  ili9341.color565(0, 0, 255)) # 顯示unispace字形的藍色字串於(0, 0)位置
display.draw_text(0, 25, "LCD Test !", arcadepix,
                  ili9341.color565(255, 0, 0)) # 顯示arcadepix字形的藍色字串於(0, 25)位置