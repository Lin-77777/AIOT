import network


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
