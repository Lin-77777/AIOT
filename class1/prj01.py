from machine import Pin,PWM
from time import sleep

frequency=1000
duty_cycle=0
led = PWM(Pin(2),freq=frequency,duty=duty_cycle)
while True:
    for i in range(1023):
        led.duty(i)#value只能用0，1，duty是0~1023
        sleep(0.01)
        