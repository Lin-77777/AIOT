# PC執行
#########################匯入模組#########################
import socket

#########################函式與類別定義#########################

#########################宣告與設定#########################
HOST = "localhost"  # IP
PORT = 5438  # Port，可自行更改但需與客戶端相同
server_socket = socket.socket()  # 建立Socket
server_socket.bind((HOST, PORT))  # 綁定IP與Port
server_socket.listen(5)  # 開始監聽，括號內數字為最大連線數
print(f"server:{HOST} port:{PORT} start")  # 接受客戶端連接，返回客戶端socket與位址
client, addr = server_socket.accept()  # 接受連線
print(f"client address:{addr[0]} port:{addr[1]} connected")  # 顯示連接資訊
#########################主程式#########################
while True:
    msg = client.recv(1024).decode(
        "utf-8"
    )  # 接收客戶端訊息，100為接收訊息的最大長度，utf8為解碼方式
    print(f"Receive Message:{msg}")  # 顯示接收到的訊息
    reply = ""  # 建立伺服器回應字串

    if msg == "Hi":
        reply = "Hello to nice to fuck you"
        client.send(reply.encode("utf-8"))  # 回傳訊息給客戶端，utf8為編碼方式
    elif msg == "bye":
        client.send(
            b"get away form the fucking server"
        )  # b"字串"的效果和encode("utf-8")一樣
        break
    else:
        reply = "what fuck are you doing"
        client.send(
            reply.encode("utf-8")
        )  # 回傳訊息給客戶端，utf8為編碼方式(encode("utf-8")的效果和b"字串"一樣
        break
client.close()  # 關閉與客戶端的溝通
server_socket.close()  # 關閉伺服器
