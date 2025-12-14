#########################匯入模組#########################
import mcu
from machine import Pin, I2C
import ssd1306


#########################函式與類別定義#########################
def on_message(topic, msg):
    global msg_received
    msg_received = msg.decode("utf-8")  # Byte to String
    topic = topic.decode("utf-8")
    print(f"my subscribe topic is:{topic},msg:{msg_received}")


#########################宣告與設定#########################
msg_received = ""  # 初始化，避免未收到訊息時使用到未定義變數

gpio = mcu.gpio()

i2c = I2C(scl=Pin(gpio.D1), sda=Pin(gpio.D2))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
wi = mcu.wifi()
wi.setup(ap_active=False, sta_active=True)
if wi.connect("SingularClass", "Singular#1234"):
    print(f"IP={wi.ip}")
else:
    print("WiFi connect failed")

mqClient0 = mcu.MQTT(
    "a", "mqtt.singularinnovation-ai.com", "singular", "Singular#1234", 60
)
mqClient0.connect()
mqClient0.subscribe("bakayarou", on_message)  # 設定想訂閱的主題

#########################主程式#########################
while True:

    msg_num = len(msg_received)
    # 查看是否有訂閱主題發布的資料
    mqClient0.check_msg()  # 等待已訂閱的主題發送資料
    oled.fill(0)  # 清除顯示
    oled_high = 0
    for i in range(0, msg_num, 16):
        msg = msg_received[i : i + 16]
        oled_high += 9
        oled.text(msg, 0, oled_high)

    oled.show()
