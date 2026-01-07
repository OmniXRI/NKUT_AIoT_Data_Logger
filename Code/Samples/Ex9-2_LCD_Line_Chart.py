from machine import Pin, ADC, SPI # 從 machine 導入 Pin, ADC, SPI 類別
import utime   # 導入時間相關類別
import ili9341 # 導入 ILI9341 LCD相關類別
from xglcd_font import XglcdFont # 從xglcd_font 導入點陣字 XglcdFont 類別
import mySetup # 導入 ili9341 及 xglcd_font 基本設定
import array # 導入 array 陣列處理類別

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
#unispace = XglcdFont('./lib/Unispace12x24.c', 12, 24) # 建立 Unispace 12x24 點陣字形
arcadepix = XglcdFont('./lib/ArcadePix9x11.c', 9, 11) # 建立 ArcadePix 9x11 點陣字形
display.clear() # 清除畫面(全黑)

x_begin = 25
x_end = 300
y_begin = 220
y_end = 20

# 繪製y軸刻度及標示數值，0.3 一格
y_scale = 60.0 # 1V = 60pixel
display.draw_line(x_begin, y_begin, x_begin, y_end, color_w) #繪y軸

for i in range(12):
    y_val = i*0.3
    y_text = f"{y_val:.1f}"
    y_pos = round(y_val*y_scale) # 四捨五入轉成整數
    display.draw_text(0, y_begin-y_pos-5, y_text, arcadepix, color_w)
    display.draw_line(x_begin, y_begin-y_pos,
                      x_begin+5, y_begin-y_pos, color_w) #繪x軸刻度
    
# 繪製x軸刻度，每15像素一格
x_scale = 15 # 每筆資料間隔15像素
display.draw_line(x_begin, y_begin, x_end, y_begin, color_w) #繪x軸

for i in range(19):
    display.draw_line(x_begin+i*x_scale, y_begin,
                      x_begin+i*x_scale, y_begin-5, color_w) #繪y軸刻度

float_array = array.array('f') # 宣告一個儲存單精度浮點數的陣列

# 初始化 ADC0
adc = ADC(0) # 設定連接到ADC0(GP26)，亦可寫成ADC(26)
factor = 3.3 / (65535) # 電壓轉換因子

# 每隔1秒讀取 SVR1 (ADC0)，讀60秒後停止
for i in range(60):    
    reading = adc.read_u16() # 讀取類比輸入值16bit無號整數
    volt = reading * factor  # 將輸入值轉成電壓值
    float_array.append(volt) # 將電壓值存入陣列中
    volt_3 = f"Volt: {volt:.3f} V " # 限制小數3位
    display.draw_text(220, 5, volt_3, arcadepix, color_y)
    print(volt_3)
    
    # 繪製折線圖
    display.fill_rectangle(x_begin+5, y_end,
                           x_end-x_begin-5, y_begin-y_end-5,
                           color_k) # 清除折線繪圖區(全部填黑)
    data_len = len(float_array)
    
    if data_len <= 1: # 若資料筆數小於等於1則略過
        pass
    elif data_len <= 18: # 若資料數量小於等於18筆則繪製到目前筆數 
        for i in range(data_len-1): # 繪製資料長度-1個線段              
            display.draw_line(x_begin+x_scale+i*x_scale,
                              round(y_begin-float_array[i]*y_scale),
                              x_begin+x_scale+(i+1)*x_scale,
                              round(y_begin-float_array[i+1]*y_scale),
                              color_c)
    else: # 若資料大於18筆則取最後18筆顯示       
        for i in range(17): # 繪製17個線段
            display.draw_line(x_begin+x_scale+i*x_scale,
                              round(y_begin-float_array[i+data_len-18]*y_scale),
                              x_begin+x_scale+(i+1)*x_scale,
                              round(y_begin-float_array[i+1+data_len-18]*y_scale),
                              color_c)
        
    utime.sleep(0.5) # 暫停0.5秒
    
display.draw_text(100, 5, "Stop Record !", arcadepix, color_r)