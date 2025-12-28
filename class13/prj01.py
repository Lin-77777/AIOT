#########################匯入模組#########################
from machine import Pin
import dht
import time
import mcu

#########################函式與類別定義#########################

#########################宣告與設定#########################
gpio = mcu.gpio()
d = dht.DHT11(Pin(gpio.D0,Pin.IN))
#########################主程式#########################
while True:
    d.measure()#讀取溫度與濕度
    temp = d.temperature()#取得溫度
    hum = d.humidity()#取得濕度
    print(f"Humidity:{hum:02d}, Temperature:{temp:02d}{'\u00b0'}C")#\u00b0C為攝氏符號
    time.sleep(1)#DHT11讀取間隔須大於1秒