from bmp280 import BMP280
from time import sleep

#step 1 - establish I2C communications
barometer = BMP280()

#this setting determines the altitude readings and is dependent on
#daily weather readings at the location of launch. 
#This must be updated, or it will return the wrong altitude. 
local_altitude_qnh = 1020.6597
    
def Pressure():
    #step 2, get and parse data
    data = {"pressure":barometer.get_pressure(), "altitude":barometer.get_altitude(), "temp":barometer.get_temperature()}
    #step 3, return that data.
    return(data)



