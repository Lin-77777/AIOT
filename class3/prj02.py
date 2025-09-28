#########################匯入模組#########################
from machine import Pin,ADC,PWM
from time import sleep
import mcu
#########################函式與類別定義#########################

#########################宣告與設定#########################
gpio=mcu.gpio()
light_sencor=ADC(0)
led=PWM(Pin(gpio.D5),freq=1000,duty=0)
led1=PWM(Pin(gpio.D6),freq=1000,duty=0)
led2=PWM(Pin(gpio.D7),freq=1000,duty=0)
led.duty(0)
led1.duty(0)
led2.duty(0)
#########################主程式#########################
while True:
    light_sencor_reading=light_sencor.read()#讀取類比數位轉換器輸出
    print(f"value:{light_sencor_reading},{round(light_sencor_reading*100/1024)}%")
    sleep(1)
    if light_sencor_reading<700:
        led.duty(0)
    else:
        led.duty(1023)
        