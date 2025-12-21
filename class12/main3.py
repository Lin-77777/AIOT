#########################匯入模組#########################
import mcu
import time
from machine import Pin, ADC, PWM

#########################函式與類別定義#########################

#########################宣告與設定#########################
gpio = mcu.gpio()
light_sencor = ADC(0)
wi = mcu.wifi()
wi.setup(ap_active=False, sta_active=True)
if wi.connect("SingularClass", "Singular#1234"):
    print(f"IP={wi.ip}")
mqClient0 = mcu.MQTT(
    "a", "mqtt.singularinnovation-ai.com", "singular", "Singular#1234", 60
)
mqClient0.connect()

#########################主程式#########################

while True:
    msg = light_sencor.read()  # 讀取類比數位轉換器輸出
    msg = str(msg)
    mqClient0.publish("kinntama", msg)
    time.sleep(1)
