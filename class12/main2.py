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


def desplay_massage(init_y, msg):
    """
    在OLED上顯示訊息，自動換行
    每個字元佔用8x8像素，OLED寬度128像素，高度64像素
    參數:
     init_y: 起始y座標
     msg: 要顯示的訊息
     迴圈變數m從init_y開始，每次增加16，直到msg長度結束
     取得當前行的訊息為line=[m:m+16]
     y座標為(m//16)*8
     透過oled.text(line, 0, y)顯示訊息

    """
    max_char_per_line = 16  # 每行最大字元數
    for m in range(0, len(msg), max_char_per_line):
        line = msg[m : m + max_char_per_line]  # 取得當前行的字串
        y_position = init_y + (m // max_char_per_line) * 8
        oled.text(line, 0, y_position + init_y)


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
    desplay_massage(16, f"msg:{msg_received}")
    # # 根據接收到的訊息長度決定顯示行數

    oled.show()
