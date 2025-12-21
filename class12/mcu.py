import sys
import network
from machine import PWM, Pin
from umqtt.simple import MQTTClient


class gpio:
    def __init__(self):
        self._D0 = 16
        self._D1 = 5
        self._D2 = 4
        self._D3 = 0
        self._D4 = 2
        self._D5 = 14
        self._D6 = 12
        self._D7 = 13
        self._D8 = 15
        self._SDD3 = 10
        self._SDD2 = 9

    @property  # 讓指令變數變的樣子(讓指令變不可改)
    def D0(self):
        return self._D0

    @property
    def D1(self):
        return self._D1

    @property
    def D2(self):
        return self._D2

    @property
    def D3(self):
        return self._D3

    @property
    def D4(self):
        return self._D4

    @property
    def D5(self):
        return self._D5

    @property
    def D6(self):
        return self._D6

    @property
    def D7(self):
        return self._D7

    @property
    def D8(self):
        return self._D8

    @property
    def SDD3(self):
        return self._SDD3

    @property
    def SDD2(self):
        return self._SDD2


class wifi:
    def __init__(self, ssid=None, password=None):
        """
        初始化WIFI模組
        ssid: WIFI名稱
        password: WIFI密碼
        """

        self.sta = network.WLAN(network.STA_IF)  # 建立 WLAN 物件，設定為站台模式
        self.ap = network.WLAN(network.AP_IF)  # 建立 WLAN 物件，設定為基地台模式
        self.ssid = ssid
        self.password = password
        self.ap_active = False
        self.sta_active = False
        self.ip = None

    def setup(self, ap_active=False, sta_active=False):
        """
        設定WIFI模組
        ap_active: 是否開放AP模式
        sta_active: 是否開放STA模式

        使用方法:
        wi.setup(ap_active=True|False,sta_active=True|False)
        """
        self.ap_active = ap_active
        self.sta_active = sta_active
        self.ap.active(ap_active)
        self.sta.active(sta_active)

    def scan(self):
        """
        掃描附近的WIFI
        返回:WIFI列表
        使用方法:
        wi.scan()
        """
        if self.sta_active:
            wifi_list = self.sta.scan()
            print("Scan result:")
            for i in range(len(wifi_list)):
                print(wifi_list[i][0])
        else:
            print("STA模式未啟用")

    def connect(self, ssid=None, password=None) -> bool:
        """
        連接WIFI
        ssid: WIFI名稱
        password: WIFI密碼
        返回:是否連接成功
        使用方法:
        wi.connect(ssid="WIFI名稱",password="WIFI密碼")
        """
        if self.sta_active:
            if ssid is None:
                ssid = self.ssid
            if password is None:
                password = self.password
            self.sta.connect(ssid, password)
            while not self.sta.isconnected():
                pass
            if self.sta.isconnected():
                self.ip = self.sta.ifconfig()[0]
                print("Connected, IP address:", self.ip)
                return True
            print("Failed to connect to WiFi")
            return False
        else:
            print("STA模式未啟用")
            return False


class LED:
    def __init__(self, r_pin, g_pin, b_pin, pwm: bool = False):
        """
        LED 類別用於管理 RGB LED

        屬性:
            RED(Pin):紅色LED
            GREEN(Pin):綠色LED
            BLUE(Pin):藍色LED
        方法:__init__(r_pin,g_pin,b_pin,pwm: bool = False):初始化LED。
            當pwm=False時，使用 Pin控制LED。
            當pwm=True時，使用 PWM控制LED亮度。
            RED.value(value):設定紅色LED狀態或亮度。
            GREEN.value(value):設定綠色LED狀態或亮度。
            BLUE.value(value):設定藍色LED狀態或亮度。
            RED.duty(duty):設定紅色LED PWM佔空比。
            GREEN.duty(duty):設定綠色LED PWM佔空比。
            BLUE.duty(duty):設定藍色LED PWM佔空比。
        """
        self.pwm = pwm
        if pwm == False:
            self.RED = Pin(r_pin, Pin.OUT)
            self.GREEN = Pin(g_pin, Pin.OUT)
            self.BLUE = Pin(b_pin, Pin.OUT)
        else:
            frequency = 1000
            duty_cycle = 0
            self.RED = PWM(Pin(r_pin), freq=frequency, duty=duty_cycle)
            self.GREEN = PWM(Pin(g_pin), freq=frequency, duty=duty_cycle)
            self.BLUE = PWM(Pin(b_pin), freq=frequency, duty=duty_cycle)

    def LED_open(self, RED_value, GREEN_value, BLUE_value):
        """
        LED開啟方法
        LED_open(RED_value,GREEN_value,BLUE_value)
        例如:


        led = LED(r_pin=5, g_pin=4, b_pin=0, pwm=False)
        led.LED_open(1, 0, 0)  # 設定紅色LED開啟，綠色和藍色LED關閉

        led = LED(r_pin=5, g_pin=4, b_pin=0, pwm=True)
        led.LED_open(512, 0, 0)  # 設定紅色LED亮度為512，綠色和藍色LED關閉
        """
        if self.pwm == False:
            self.RED.value(RED_value)
            self.GREEN.value(GREEN_value)
            self.BLUE.value(BLUE_value)
        else:
            self.RED.duty(RED_value)
            self.GREEN.duty(GREEN_value)
            self.BLUE.duty(BLUE_value)


class MQTT:
    def __init__(self, Client_id, sever, user, password, keepalive):
        """
        抓取MQTTClient物件
        連接MQTT伺服器
        訂閱主題
        等待以訂閱之主題發送資料
        使用方法:
        1.import mcu
        2.mcu.MQTT
        """
        """
        使用方式:
        mqClient(MQTT伺服器名稱,使用者名稱,密碼,保持連線時間)要是str
        """
        self.mqClient = MQTTClient(
            Client_id, sever, user=user, password=password, keepalive=keepalive
        )
        """
        MQTT.connect()
        """

    def connect(self):
        try:
            self.mqClient.connect()
        except:
            sys.exit()
        finally:
            print("connected MQTT server")

    """
    MQTT.subscribe(主題)
    """

    def subscribe(self, topic: str, callback: function):
        self.mqClient.set_callback(callback)  # 設定接收訊息的時候要呼叫的函式
        self.mqClient.subscribe(topic)  # 設定想訂閱的主題

    """
    MQTT.check_msg()
    """

    def check_msg(self):
        self.mqClient.check_msg()  # 等待已訂閱的主題發送資料
        self.mqClient.ping()  # 持續確認是否還保持連線

    def publish(self, topic: str, msg: str):
        topic = topic.encode("utf-8")
        msg = msg.encode("utf-8")
        self.mqClient.publish(topic, msg)
