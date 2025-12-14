#########################匯入模組#########################
from umqtt.simple import MQTTClient
import sys
import time
import mcu
from machine import ADC

global msg_received
msg_received = ""


#########################函式與類別定義#########################
def on_message(topic, msg):
    global msg_received
    msg_received = msg.decode("utf-8")  # Byte to String
    topic = topic.decode("utf-8")
    print(f"my subscribe topic is:{topic},msg:{msg_received}")


#########################宣告與設定#########################
wi = mcu.wifi()
wi.setup(ap_active=False, sta_active=True)
if wi.connect("SingularClass", "Singular#1234"):
    print(f"IP={wi.ip}")
mqClient0 = mcu.MQTT(
    "a", "mqtt.singularinnovation-ai.com", "singular", "Singular#1234", 60
)
mqClient0.connect()
mqClient0.subscribe("bakayarou", on_message)  # 設定想訂閱的主題


gpio = mcu.gpio()
LED = mcu.LED(gpio.D5, gpio.D6, gpio.D7, pwm=True)
LED.LED_open(0, 0, 0)
light_sencor = ADC(0)
#########################主程式#########################

while True:
    # 查看是否有訂閱主題發布的資料
    mqClient0.check_msg()  # 等待已訂閱的主題發送資料
    light_sencor_reading = light_sencor.read()  # 讀取類比數位轉換器輸出
    if msg_received == "on":
        LED.LED_open(1023, 1023, 1023)
    elif msg_received == "off":
        LED.LED_open(0, 0, 0)
    elif msg_received == "auto":
        print(f"value:{light_sencor_reading},{round(light_sencor_reading*100/1024)}%")
        if light_sencor_reading < 400:
            light_sencor_reading = 0

        LED.LED_open(light_sencor_reading, light_sencor_reading, light_sencor_reading)
    time.sleep(0.3)
