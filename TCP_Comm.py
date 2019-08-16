import socket
import struct

#from Storagebox import Storagebox
class TCP_Comm():
    
    def __init__(self,Storagebox):
        # Create library object using our Bus I2C port
        #self.sb=storagebox
        self.sb=Storagebox
        self.connection=None
        self.connected=None
        self.ClientIP=None
        self.available=None

    def establishConnection(self):
        #Create TCP/IP socket 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # get the according IP address of server/ Set static in Raspberry Pi EThernet!
        #ip_address = '192.168.137.63'
        ip_address = '192.168.137.63'
        # bind the socket to the port 5001
        server_address = (ip_address, 5001)
        sock.bind(server_address)
        # listen for incoming connections (server mode) with one connection at a time
        sock.listen(1)
        # wait for a connection, retrieve connection and the IP of incoming client
        self.connection, self.ClientIP = sock.accept()
        self.sb.setClientIP(self.ClientIP[0])
        self.connected=True
        print("connected")
        return self.connected
             
    "Thread method runnning indefinetely as long as connected to client"            
    def runMethod(self):
        while self.connected:
            self.readMethod()
            self.writeMethod() 
            self.connected=self.sb.getConnection()
        if self.connected==False:
            #Clean up the connection
            print("close TCP connection")
            self.connection.close()
    "Read method that reads incoming data from client and sends data to Storagebox"
    def readMethod(self):
        #Read the bytes from socket connection
        try:  
            data = self.connection.recv(17)
            if data:
                self.byteToStruct(data)
            pass
        except:
            print("No data to read")

            pass
    
    "Write method that sends values from StorageBox to the client as Bytearray"
    def writeMethod(self):
        value=self.sb.getDataList()
        self.connection.sendall(value)

    "Convert byte array to float values using Struct library"
    def byteToStruct(self,data):
        # output received data
        connectionValue=data[0]
        #Returns tuple 
        lightValue=struct.unpack('>f', data[1:5])
        servoXAxis=struct.unpack('>f', data[5:9])
        servoYAxis=struct.unpack('>f', data[9:13])
        seaLevelPressure=struct.unpack('>f', data[13:17])
        #Take out single value from the Tuple
        self.sb.setConnection(connectionValue)
        self.sb.setLightValue(lightValue[0])
        #self.sb.setCleanXAxisValue(servoXAxis[0])
        #self.sb.setCleanYAxisValue(servoYAxis[0])
        self.sb.setServoValueXAxis(servoXAxis[0])
        self.sb.setServoValueYAxis(servoYAxis[0])
        self.sb.setSeaLevelhPa(seaLevelPressure[0])

  