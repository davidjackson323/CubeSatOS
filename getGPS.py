import serial #required for serial communications
from micropyGPS import MicropyGPS #GPS parser

'''
Our (and most) GPS modules return data through a serial comm port that
is hooked up to the RX and TX pins of a microcontroller. The format 
returned is reffered to as "NEMA" sentences that need to be parsed. 
I found the parsing library micropyGPS and wrote some simplification code
so that I can get the values I am interested in which are long, lat and 
the current timestamp.

micropyGPS installation instructions can be found here
https://github.com/inmcm/micropyGPS

or the file can be directly copied into the working directory, and 
and __init__.py file created to allow imports from the current directory.

Since micropyGPS doesn't provide a version function, I have added the file
to the directory of this project, and included an __init__.py file to allow
for importing it.

PySerial version 3.5 is used for this project, and can be found here
https://github.com/pyserial/pyserial
'''

#we start by declaring the serial port of the GPS device.
#Our GPS module uses UART (serial comms) to send/recieve data

#Step one, open the serial com port
gps_module = serial.Serial("/dev/serial0")

#we also select our time zone to correct the timestamp
TIMEZONE = -7
my_gps = MicropyGPS(TIMEZONE)

#this is a refresher function to get the latest data from the GPS
def updateGPS():
    gps_module = serial.Serial("/dev/serial0")
    my_gps = MicropyGPS(TIMEZONE)

#This function gets the latest data, parses and returns it in the format
#of a dictionary with the keys being "lat", "long" and "timestamp".
def GPS():
    #refresh GPS to latest reading
    #Step two, get the GPS NEMA sentences from the GPS com port
    updateGPS()

    #read the latest 9 lines from the serial device
    counter = 0    
    while counter < 9:
        b = gps_module.readline()
        length = len(b)
        
        for x in b:
            msg = my_gps.update(chr(x))
        counter += 1
    
    #parse the timestamp
    #Step 3 Parse the NEMA sentences into usable data
    timeStamp = str(my_gps.timestamp[0])+':'+str(my_gps.timestamp[1])+':'+str(my_gps.timestamp[2])
    
    #parse the latitude
    Lat = str(my_gps.latitude)
    Lat = Lat.strip("["); Lat = Lat.strip("]")
    Lat = Lat.replace("'",""); Lat = Lat.replace(" ",'')
    
    #parse the longitude
    Long = str(my_gps.longitude)
    Long = Long.strip("["); Long = Long.strip("]")
    Long = Long.replace("'",""); Long = Long.replace(" ",'') 

    #Step 4 Return the Desired GPS data
    return {"lat":Lat, "long":Long, "time":timeStamp}
    gps_module.close()
