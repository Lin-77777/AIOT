#########################匯入模組#########################
from machine import Pin,I2C
import dht
import time
import mcu
import ssd1306
#########################函式與類別定義#########################

#########################宣告與設定#########################
gpio = mcu.gpio()
wi = mcu.wifi("SingularClass", "Singular#1234")
wi.setup(ap_active=False, sta_active=True)
if wi.connect():
    print(f"IP={wi.ip}")
mqClient0 = mcu.MQTT(
    "a", "mqtt.singularinnovation-ai.com", "singular", "Singular#1234", 60
)
mqClient0.connect()
i2c = I2C(scl=Pin(gpio.D1), sda=Pin(gpio.D2))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
d = dht.DHT11(Pin(gpio.D0,Pin.IN))

#########################主程式#########################
while True:
    d.measure()#讀取溫度與濕度
    temp = d.temperature()#取得溫度
    hum = d.humidity()#取得濕度
    oled.fill(0)  # 清除顯示
    oled.text(f"Humidity:{hum:02d}%", 0, 0)#顯示文字，X=0,Y=0
    oled.text(f"Temperature:{temp:02d}C", 0, 8)#顯示文字，X=0,Y=0
    oled.show()  # 更新顯示
    msg = f"Humidity:{hum:02d}, Temperature:{temp:02d}{'\u00b0'}C"#\u00b0C為攝氏符號
    mqClient0.publish("kinntama", msg)#mqtt發布訊息
    time.sleep(1)#DHT11讀取間隔須大於1秒