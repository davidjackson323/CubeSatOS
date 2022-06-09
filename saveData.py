import os
from picamera import PiCamera

'''
We need a convention for creating folders so that we
can save data each time the satellite is turned on.
We want to save to a new folder so that we don't erase
the previous save data each time the satellite is turned on. 
'''


#this function checks for an existing data folder
#and creates one if it does not (exist). 
def getFolder():
    directory = os.listdir()
    if 'data' in directory:
        print('data folder found')

    else:
        print('making data folder')
        os.mkdir('data')

    currentFolder = len(os.listdir('data'))
    currentFolder = currentFolder + 1
    currentFolder = 'data/' + str(currentFolder)
    os.mkdir(currentFolder)
    return(currentFolder)

    
'''
we need a convention for associating the picture images with the text file that
contains all the data from the various modules (gps, barometer, accelerometer and gyroscope)
i.e. We create a text file that contains 100 measurements, and all the pictures for each
measurement are associated with that single text file through a nameing convention.

I include an index that refers to the current measurement readings,
and name each picture image according to the current measurement index so we can
associate the readigns to the image.
I.E. at this image (image 0), we have these readings (readings 0).

To make things easy, I create a new folder for each associated reading range.

By limiting the measurement readings to a certain number, we can minimize the damage
caused by a crash. I.E. if we have one big text file with all the readings, and the
OS crashes while accessign that file, there is a possibility it could corrupt the file
and we loose all our readings. By limiting the text file to x# of readings, then
we only lose x# number of readings

-argument currentFolder is the folder name returned by the above function "getFolder()"
-argument dataLineCount determines the max number of readings for each text file
-argument dataToSave is the data readings to be saved to the text file
-arguments folderIndex and index are the indexes required to keep track of the current
data reading, as well as the current folder name. These are kept track by a variable 
declared outside the saveData_and_Image().
Doing so allows us to isolate calling camera functions to the main program so 
that we don't have to create and call the camera object functions everytime the function is used.
This reduces processing time by 0.2 seconds for the RPI zero. 
'''


def saveData_and_Image(currentFolder = "/data/1", dataToSave = "test\n", folderIndex = 0, index = 0, dataLineCount=60):
    
    
    saveTo = currentFolder + "/" + str(folderIndex)
    print(index)
    #if our current index count is divisble by the dataLineCount,
    #create a new folder for the next x amount saves.
    if not index % dataLineCount:
        folderIndex += 1
        saveTo = currentFolder + "/" + str(folderIndex)
        os.mkdir(saveTo)
    
    if index != 0:
        with open(saveTo+"/"+str(folderIndex)+".txt", 'a+') as text_file:
            text_file.write(str(index)+","+dataToSave)

    
    index += 1
    return folderIndex, index, saveTo



#Test example on how to use this code when calling from main.
#Can be uncommented for testing purposes, but again this should be implemented 
#in main program, not here. 
'''
from picamera import PiCamera
folder = getFolder()

#we initilaze the folder saving by calling saveData once, and set the results
#equal to folderIndex, index

folderIndex, index, saveTo = saveData_and_Image(currentFolder = folder)

#then we incorporate this into the while loop that runs forever by passing those
#variables back into the function, almost like a recursive function
#the camera initilization is best kept in the main, to reduce the time required
#0.72 seconds vs 0.51 seconds. Else, if we incorporate it into the function,
#we have to open and close the camera to not cause an error with the camera library.

camera = PiCamera()
testCount = 0
while testCount < 121:
    
    folderIndex, index, saveTo = saveData_and_Image(currentFolder = folder, folderIndex = folderIndex, index = index)
    camera.capture(saveTo+"/"+str(index)+".jpg")
    testCount += 1 

'''





