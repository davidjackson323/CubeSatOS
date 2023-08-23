# CubeSatOS
CubeSatOS is an operating system for cubesatellites based upon Python and the Raspberry Pi.

I will place all my relevant code here that I develop for satellite systems.

The goal is to develop a collection of python scripts onto the raspbian OS that will allow 
researchers to better focus on the development of the payload.

The OS will be able to handle power, attitude control, motor control, communications and 
data logging from custom sensors through the GPIO pins available.

The current dependencies of this project are 

micropyGPS
pyserial
bmp280
RPITX 



The documentation and installation process of those libraries are documented at their respective github pages, found below.

https://github.com/inmcm/micropyGPS

https://github.com/pyserial/pyserial

https://github.com/pimoroni/py-smbus

https://github.com/F5OEO/rpitx

MicropyGPS is already provided in the master folder, but can also be downloaded from its github repository. 


For smbus, the I2C protocol needs to be enabled. This can be done from the raspi-config menu. 
If any questions on how to do so, please contact me. 

![cubesat](https://github.com/davidjackson323/CubeSatOS/assets/19483270/79785f46-29a7-4d95-97d9-3482a019cb8d)


![cubesat on](https://github.com/davidjackson323/CubeSatOS/assets/19483270/94301b9b-96a6-45a6-89fd-abe7ebe26fbe)


https://github.com/davidjackson323/CubeSatOS/assets/19483270/12f0e842-e458-49d4-b164-922a75c00499


![Team-Photo](https://github.com/davidjackson323/CubeSatOS/assets/19483270/4277ed5f-9ed7-4b97-9124-bc2505ee7761)





