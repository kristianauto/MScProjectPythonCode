#StorageBox class that handles incoming and outgoing data 
import numpy as np
import struct
"Class to store values for the drill camera module application bytearray created to"
"be used to send retrieve information to GUI, server"
class Storagebox:
    def __init__(self):
        self.lightValue=1023
        self.servoValueXAxis= 500
        self.servoValueYAxis= 500
        self.pressure = 0
        self.altitude = 0
        self.humidity = 0
        self.tempOutside = 0 
        self.tempCamera = 0
        self.tempTop = 0
        self.yaw = 0
        self.pitch = 0
        self.roll = 0
        self.dewPoint = 0
        self.connection = False
        self.clientIP = None
        self.SeaLevelhPa = 1023
        self.yawOrigin = None
        self.pitchOrigin = None
        self.cleanXAxisValue = 500
        self.cleanYAxisValue = 500 
    "Set the values of Storagebox data, convert float values to bytes with little endian order, positive values"
    def setLightValue(self,value):
        self.lightValue = str(round(value))
        if(len( self.lightValue)<5):
            while(len( self.lightValue)<5):
                self.lightValue=self.lightValue+'F'

    def setServoValueXAxis(self,value):
        self.servoValueXAxis = str(round(value))
        if(len( self.servoValueXAxis)<5):
            while(len( self.servoValueXAxis)<5):
                self.servoValueXAxis=self.servoValueXAxis+'F'
    def setCleanXAxisValue(self,value):
          self.cleanXAxisValue = value
   
    def setServoValueYAxis(self,value):
        self.servoValueYAxis = str(round(value))
        if(len( self.servoValueYAxis)<5):
            while(len( self.servoValueYAxis)<5):
                self.servoValueYAxis=self.servoValueYAxis+'F'
    
    def setCleanYAxisValue(self,value):
        self.cleanYAxisValue = value
   
    def setPressure(self,value):
        self.pressure = value

    def setAltitude(self,value):
        self.altitude = value

    def setHumidity(self,value):
        self.humidity = value 

    def setTempOutside(self,value):
        self.tempOutside = value  

    def setTempCamera(self,value):
        self.tempCamera = value
    
    def setTempTop(self,value):
        self.tempTop = value  
   
    def setYaw(self,value):
        self.yaw = value  

    def setPitch(self,value):
        self.pitch = value  

    def setRoll(self,value):
        self.roll = value  
   
    def setDewPoint(self,value):
        self.dewPoint = value

    def setConnection(self,value):
        if(value == 2):
            self.connection = False
        else:
              self.connection=True
        

    def setClientIP(self,IP):
        self.clientIP = IP
   
    def setYawOrigin(self,yaw):
        self.yawOrigin = yaw

    def setPitchOrigin(self,pitch):
        self.pitchOrigin = pitch

    def setSeaLevelhPa(self,value):
        self.SeaLevelhPa=value

    ##########################################################################################################################################
    ##########################################################################################################################################

    "Return the value of the parameters for sending to microcontrooller as strings"
    def getLightValue(self):
        return self.lightValue

    def getServoValueXaxis(self):
        return self.servoValueXAxis

    def getServoValueYAxis(self):
        return self.servoValueYAxis
    "return the sensor values as a bytearray with Big endian readings containing float values for precision "
    def getDataList(self):
        value = bytearray(struct.pack(">f", self.pressure)) 
        value += bytearray(struct.pack(">f", self.altitude)) 
        value += bytearray(struct.pack(">f", self.humidity)) 
        value += bytearray(struct.pack(">f", self.tempOutside)) 
        value += bytearray(struct.pack(">f", self.tempCamera)) 
        value += bytearray(struct.pack(">f", self.tempTop)) 
        value += bytearray(struct.pack(">f", self.dewPoint)) 
        value += bytearray(struct.pack(">f", self.yaw)) 
        value += bytearray(struct.pack(">f", self.pitch))
        value += bytearray(struct.pack(">f", self.roll))  
        return value
    "Return the state of connection between server and client"
    def getConnection(self):
        isConnected = self.connection
        return isConnected
    "return the IP address of the connecting client"
    def getClientIP(self):
        return self.clientIP

    def getCleanYAxisValue(self):
        return self.cleanYAxisValue
    
    def getCleanXAxisValue(self):
        return self.cleanXAxisValue
        
    def getSealevelPressure(self):
        return self.SeaLevelhPa

    def getPitch(self):
        pitch = self.pitch
        pitch = pitch *10
        pitch = round(pitch)
        pitch= pitch/10
        stringPitch = str(pitch)
      
        if(len(stringPitch)<5):
            while(len(stringPitch)<5):
                stringPitch = stringPitch+'F'  
       
        return stringPitch

    def getYaw(self):
        yaw = self.yaw
        yaw = yaw *10
        yaw = round(yaw)
        yaw= yaw/10
        stringYaw = str(yaw)
        if(len(stringYaw)<5):
            while(len(stringYaw)<5):
                stringYaw = stringYaw+'F'
        return stringYaw



