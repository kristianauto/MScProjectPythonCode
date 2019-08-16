from Storagebox import Storagebox
from I2C_Comm import I2C_Comm
from TCP_Comm import TCP_Comm
from Video_Stream import VideoStream
import concurrent.futures
class Startup():
    def __init__(self):
        self.sb=Storagebox()
        self.tcp=TCP_Comm( self.sb)
        self.i2c=I2C_Comm( self.sb)
        self.vs=VideoStream( self.sb)
        self.waitForConn()
    "Wait for a connection to be made"
    def waitForConn(self):
        try: 
            connection= self.tcp.establishConnection()
            self.sb.setConnection(connection)
            if(connection):
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    executor.submit(self.tcp.runMethod)
                    executor.submit(self.i2c.updateI2C)
                    executor.submit(self.vs.update,False)
                    executor.submit(self.vs.streamUDP)
            pass
        except EnvironmentError as identifier:
            print(identifier)           
            pass
        self.waitToStop()
       
    "Wait for connection to be false to start listening again"
    def waitToStop(self):
        while self.sb.getConnection():
            s=10  
      
        print("ended session")
        self.waitForConn()
        

start=Startup()

    

        


