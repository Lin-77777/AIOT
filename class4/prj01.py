
#########################匯入模組#########################
import network
#########################函式與類別定義#########################

#########################宣告與設定#########################
wlan = network.WLAN(network.STA_IF)  # 建立 WLAN 物件，設定為站台模式
ap = network.WLAN(network.AP_IF)    # 建立 WLAN 物件，設定為基地台模式
ap.active(False)#關閉AP模式
wlan.active(True)#開放STA模式

#搜尋WIFI
wifi_list = wlan.scan()  # 掃描附近的無線網路
print("Scan result:")
for i in range(len(wifi_list)):
    print(wifi_list[i])  # 列出掃描結果
#選擇要連線的WIFI
wlSSID = "Singular_AI"
wlPWD = "Singular#1234"
wlan.connect(wlSSID, wlPWD)  # 連接到指定的無線網路
while not (wlan.isconnected()):  # 等待連接成功
    pass
print("connet successfully", wlan.ifconfig())  # 顯示連接資訊
#########################主程式#########################
while True:
    pass