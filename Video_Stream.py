from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import imutils
import socket

class VideoStream:
    def __init__(self,Storagebox, resolution=(640, 480), framerate=32):
        self.camera=None
        self.capture=None
        self.stream=None
        self.available=True
        self.sb=Storagebox
        self.frame = None
        self.stopped = False
        self.UDP_IP =None      #"192.168.137.1"
        self.UDP_PORT = 5002
        self.sock =None

    "Create camera object and initialize stream"   
    #640,480
    def start(self,resolution=(640, 480), framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.capture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.capture,
            format="bgr", use_video_port=True)
        return self
    "Update mat frame by reading from camera object"
    def update(self,arg):
        # keep looping infinitely until the stopped
        self.start()
        self.stopped=arg
        time.sleep(1)
        for frame in self.stream:
            # capture the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = frame.array
            self.capture.truncate(0)
            
            # if the thread stop-indicator variable is true, stop the thread
            if self.stopped:
                self.stream.close()
                self.capture.close()
                self.camera.close()
                break
        print("shutdown frameReader")
   
    "return the frame most recently read"
    def read(self):
        return self.frame
    "indicate that the thread should be stopped"
    def stop(self):
        self.stopped = True
        
    "Convert the read frames from picamera module to Jpg and compress before sending as UDP datagram over socket link"
    def streamUDP(self):
        sock=socket.socket(socket.AF_INET,   # Internet socket.
        socket.SOCK_DGRAM)  #UDP.
        time.sleep(0.2)
        #try to send data if fail, code wil not crash.
        try:
            self.available=self.sb.getConnection()
            self.UDP_IP=self.sb.getClientIP()
            print(self.UDP_IP)
            print(self.available)
            while self.available:
                # grab the latest read frame from the camera 
                frame = self.read()
               
                if (frame is not None):
                    __,compressed  = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                    sock.sendto(compressed,(self.UDP_IP,self.UDP_PORT))
                #Check if connection is still active
                self.available=self.sb.getConnection()
            
            #Do some cleanup if close signal has been sent
            cv2.destroyAllWindows()
            self.stop()
            sock.close()
            print("shutdown UDP")
            pass
        except socket.error as identifier:
            print(identifier)
            pass
       