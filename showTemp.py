#!/bin/python3
import time
import os
from RPi import GPIO
from gpiozero import CPUTemperature
from datetime import datetime

channel=18
start_fan_temperature=60
stop_fan_temperature=45
shutdown_temperature=70

def record_and_show():
    max_temperature=0
    max_time = ''
    last_start_time=''
    cpu = CPUTemperature()
    while True:
        now=datetime.now()
        s = now.strftime('%Y-%m-%d %H:%M:%S')
        t = cpu.temperature
        if t > max_temperature:
            max_temperature =t 
            max_time = s
        if t>start_fan_temperature:
            switch_fan(True)
            last_start_time=s
        elif t<stop_fan_temperature:
            switch_fan(False)
        if t>shutdown_temperature:
            os.system('sudo shutdown now') 
        #print('%s temperature is:%s, last start fan:%s'%(s,t,last_start_time))
        time.sleep(10)


def switch_fan(t):
    on = GPIO.LOW if t else GPIO.HIGH
    GPIO.output(channel,on)

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(channel,GPIO.OUT,initial=GPIO.HIGH)

if __name__ == '__main__':
    try:
        init_gpio()
        record_and_show()
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
