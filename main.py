#Import required libraries
import os
from getGPS import GPS
from getPressure import Pressure
from getMotion import Motion
from time import sleep
from picamera import PiCamera
from saveData import getFolder, saveData_and_Image
from display import initDisplay, text
from gpiozero import Button

'''
We start by initializing all the required hardware and code.
This includes: transmission counter, data saving variables,
camera, OLED screen, tranmission on/off variable, and the 
GPIO pins for the shutdown button, and the battery low indicator.
'''

#this counter determines the transmission
counter = 0

#initialize the camera and save folder
folder = getFolder()
folderIndex, index, saveTo = saveData_and_Image(currentFolder = folder)
camera = PiCamera()

#initialize the screen
screen = initDisplay()
text(screen, "Initializing CubeSat")

#set antenna to off currently
tx_operational = 0

#bug, buttons must be declared after screen initilization
shutDown = Button(23)
battery_low = Button(24)


"""
After initializing the required hardware and variables,
the main program loop is executed. The sensor data will be 
read, prepared for the screen and file saving, saved, and transmitted
if requested. Then the program will check for transmission requests,
shut down and program exit requests, and for low battery conditions.
"""
while True:
    #1.) Get the data from the sensors
    gps = GPS()
    motion = Motion()
    pressure = Pressure()
    
    #2.)Prepare data for screen
    time = 'Time:'+gps['time']
    lat = 'LT:'+gps['lat'].replace(',','.')
    long = 'LG:'+gps['long'].replace(',','.')
    
    if tx_operational == 0:
        tx = "Transmit is off"
    else:
        tx = "Transmit is on"
    
    text(screen, [time, lat, long, tx])
    
    #2.)Prepare data for file saving
    gps_data = gps['time']+ ',' + gps['lat'].replace(',','.') + ',' + gps['long'].replace(',','.')
    
    motion_data = str(motion['gx']) + ',' + str(motion['gy']) + ',' + str(motion['gz']) + ','
    motion_data = motion_data + str(motion['ax']) + ',' + str(motion['ay']) + ',' + str(motion['az'])
    
    pressure_data = str(pressure['pressure']) + ',' + str(pressure['altitude']) + ',' + str(pressure['temp'])
    
    #combine the data into a single line for saving.    
    data = gps_data + ',' + motion_data + ',' + pressure_data + '\n'
    print(data)
    
    #3.)Save the data and image.
    folderIndex, index, saveTo = saveData_and_Image(currentFolder = folder, dataToSave = data, folderIndex = folderIndex, index = index)
    camera.capture(saveTo+"/"+str(index)+".jpg")
    
    #4.)Transmit the data.
    tx_counter = counter % 5
    if tx_counter == 0 and tx_operational == 1:
        camera.close()
        text(screen, "Transmitting Data")
        dataSentence = gps['time'] + " - " + gps['lat'] + " - " + gps['long']

        filler = (51 - len(dataSentence))/2
        filler = int(filler)

        dataSentence = ("x"*filler) + dataSentence + ("x"*filler)
        #Enable the following code for transmission
        os.system('sudo ./rpitx/pirtty 434000000 1000 "' + dataSentence + '"')
        print(dataSentence)
        counter = 0
        camera = PiCamera()
        text(screen, "Data Transmitted")
    
    counter += 1
    
    #5.)Check for tx request, shut down, program exit and low battery.
    shutDown_time = 0
    while shutDown.is_active:
        sleep(1.1)
        antenna = "TX on/off > 5"
        shutdown = "5<=Shutdown>10"
        breakMain = "10<=stop program"
        time = "time: " + str(shutDown_time)
        text(screen, [tx, antenna, shutdown, breakMain, time])
        shutDown_time += 1
    
    if shutDown_time <5 and shutDown_time >0:
        if tx_operational == 0:
            print("transmission activated")
            text(screen, "TX activated")
            tx_operational = 1
        else:
            tx_operational = 0
            print("transmission deactivated")
            text(screen, "TX deactivated")
            tx_operational = 0
        
    if shutDown_time >=5 and shutDown_time <10:
        print("Shutting Down Sat")
        text(screen, "Shutdown Activated")
        camera.close()
        os.system('sudo shutdown -h now')
        sleep(5)
    
    if shutDown_time >=10:
        text(screen, "Program Exited")
        print("Breaking out of main Loop")
        camera.close()
        break

    if battery_low.is_active == True:
        print("battery is low, shutting down")
        text(screen, ["Battery Critical", "Shut down activated"])
        camera.close()
        os.system('sudo shutdown -h now')
        sleep(5)
    
        
        
      
    

    
