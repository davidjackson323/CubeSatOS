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
RPITX - Requires different installation process. Please refer to this page to install
https://github.com/F5OEO/rpitx

pip install git+https://github.com/inmcm/micropyGPS.git
pip install pyserial
sudo pip install bmp280

The documentation can be found for each library at their respective github pages, found here

https://github.com/inmcm/micropyGPS
https://github.com/pyserial/pyserial
https://github.com/pimoroni/py-smbus
https://github.com/F5OEO/rpitx

MicropyGPS is already provided in the master folder, but can also be downloaded from its github repository. 


For smbus, the I2C protocol needs to be enabled. This can be done from the raspi-config menu. 
If any questions on how to do so, please contact me. 

