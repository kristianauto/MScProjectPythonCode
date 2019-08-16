import math as m
import time
import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_htu21d import HTU21D as humidity
from adafruit_bno055 import BNO055 as IMU
from adafruit_bmp280 import Adafruit_BMP280_I2C as pressure
import smbus
class I2C_Comm:
    def __init__(self,Storagebox):
        # Create library object using our Bus I2C port
        i2c = busio.I2C(board.SCL, board.SDA)
        #Create link to Arduino using smbus library.
        self.bus = smbus.SMBus(1)
        self.pressureSensor = pressure(i2c)
        self.IMUSensor = IMU(i2c)
        self.humiditySensor = humidity(i2c)
        
        #Change this to match location's pressure (hPa) at sea level.
        #Set for Glasgow University JWS building space lab 1031.
        self.pressureSensor.sea_level_pressure= 1024 
        #Establish link to Storagebox class to use its functions and data
        self.sb=Storagebox
        self.connection=False
        #Debug active/not active
        self.DEBUG=False
        #Adresses in use  
        #pressureSensor = 0x77
        #IMUSensor = 0x28
        #humiditySensor = 0x40
        #Arduino motor/light = 0x07
    "Retrieve values from sensors over I2C bus and send new values to microcontroller, running as a Thread"  
    def updateI2C(self):
      self.connection=self.sb.getConnection()
      while self.connection:
        self.getHumidityData()
        self.getIMUData()
        self.getPressureData()
        self.sendDataToServoController()
        self.connection=self.sb.getConnection()
      print("shutDown I2C")
       
    "Send control data to microcontroller to perform control action"
    "Light value to be sent controlling the output of LED lights"
    "ServoXAxis values control X axis motor"
    "ServoYAxis values control Y axis motor"
    def sendDataToServoController(self):
        #Adress of the arduino to connect to
        i2c_address = 0x07
        #Command value, had to be added to work....
        i2c_cmd = 0x01 
        #Build a String of char values to send over I2C 
        stringData =self.sb.getLightValue()+self.sb.getServoValueXaxis()+self.sb.getServoValueYAxis() +self.sb.getPitch() +self.sb.getYaw()
        #Convert string to byteArray
        bytesToSend = self.ConvertStringToBytes(stringData)
        try: 
          #Send the values over I2C link to receiving microcontroller
          self.bus.write_i2c_block_data(i2c_address, i2c_cmd, bytesToSend)
          #Delay to give Arduino time to read data
          time.sleep(0.05)
          pass
        except:
          print("Could not write to arduino  ")
          pass
       
    "Convert strings to byteArray to send over I2C"
    def ConvertStringToBytes(self,src):
      converted = []
      for b in src:
        converted.append(ord(b))
      return converted

    "Retrieve data from inertial measurement unit in Euler angles and store them in StorageBox"
    "Yaw, Pitch, Roll"
    def getIMUData(self):
        #Retrieve IMU data from sensor using adafruit lib BNO055
        yaw=self.IMUSensor.euler[0]
        pitch=self.IMUSensor.euler[1]
        roll=self.IMUSensor.euler[2] 
        temp=self.IMUSensor.temperature
        #Time delay to give sensor time to write data 
        time.sleep(0.1)

        #Set values to be stored in Storagebox
        self.sb.setYaw(yaw)
        self.sb.setPitch(pitch)
        self.sb.setRoll(roll)
        self.sb.setTempCamera(temp)
        #Debug
        if self.DEBUG:
          print("yaw" )
          print(yaw)
          print("pitch" )
          print(pitch)
          print("roll" )
          print(roll)
          print("temperature")
          print(temp)


    "Retrieve data from pressure sensor BMP280 and store them in Storagebox "
    "Temperature in %0.1C"
    "Pressure in %0.1 hPa"
    "Altitude in %0.2 meters"
    def getPressureData(self):
        #Retrieve humidity data from sensor using adafruit lib BMP280
        temp=self.pressureSensor.temperature
        pressure=self.pressureSensor.pressure
        altitude=self.pressureSensor.altitude

        #Time delay to give sensor time to write data 
        time.sleep(0.1)
         
        #Set values to be stored in Storagebox
        self.sb.setTempOutside(temp)
        self.sb.setPressure(pressure)
        self.sb.setAltitude(altitude)
        self.pressureSensor.sea_level_pressure =  self.sb.getSealevelPressure()
        #Debug
        if self.DEBUG:
          print("TempOutside")
          print(temp)
          print("pressure")
          print(pressure)
          print("altitude")
          print(altitude)

    "Retrieve data from humidity sensor HTU21D and store them in Storagebox"
    "Temperature in %0.1 C"
    "Humidity in %0.1 %%"
    def getHumidityData(self):
        #Retrieve humidity data from sensor using adafruit lib HTU21D
        temp=self.humiditySensor.temperature
        humid=self.humiditySensor.relative_humidity
        #Time delay to give sensor time to write data 
        time.sleep(0.1)
        #Generate dewPoint using Magnus's formula 
        dewPoint=self.generateDewPoint(temp,humid)
        #Set values to be stored in Storagebox
        self.sb.setTempTop(temp)
        self.sb.setHumidity(humid)
        self.sb.setDewPoint(dewPoint)

        #Debug 
        if self.DEBUG:
          print("tempinside" )
          print(temp)
          print("relative humidity" )
          print(humid)
          print("dewPoint" )
          print(dewPoint)

    "Definition to find dewPoint inside module using Magnus's formula"      
    def generateDewPoint(self,temp,humid):
      b = 17.62
      c = 243.12
      gamma = (b * temp /(c + temp)) + m.log(humid / 100.0)
      dewpoint = (c * gamma) / (b - gamma)
      return dewpoint