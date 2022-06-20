from ws2812 import WS2812
import utime
import machine
from time import sleep

shutDown = machine.Pin(7,machine.Pin.OUT)

power = machine.Pin(11,machine.Pin.OUT)
power.value(1)

OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

 
led = WS2812(12,1)#WS2812(pin_num,led_count)
battery = machine.ADC(26)

#Above 7.3 High Voltage - Green
#7.3 - 6.4 Mid Voltage - Yellow
#6.4 - 5.5 Low Voltage - Red
#below 5.5 - Turn off Voltage - White
"""
The voltage read by ADC is off by about -0.1 V, so the
above numbers must be adjusted for. I decided to print the
battery level read by the ADC and accounted for what the
power supply was outputting at the time. The above numbers
are mathematical calculations based upon what the voltage should
be (theoretically). 
"""

while True:
    shutDown.on()
    conversion_factor = 3.3 / (65535)
    batteryLevel = (battery.read_u16() * conversion_factor) * 5
    print(batteryLevel)
    
    print("checking green")
    if batteryLevel >= 7.4:
        led.pixels_fill(GREEN)
        led.pixels_show()
        print("green")
        
    print("checking yellow")    
    if batteryLevel >= 6.5 and batteryLevel < 7.4:
        led.pixels_fill(YELLOW)
        led.pixels_show()
        print("yellow")
        
    print("checking red")    
    if batteryLevel < 6.5 and batteryLevel >= 5.55:
        led.pixels_fill(RED)
        led.pixels_show()
        print("red")
        
    if batteryLevel < 5.55:
        led.pixels_fill(WHITE)
        led.pixels_show()
        print("Shutting Down")
        shutDown.off()

    sleep(1)
    


