from PyQt5.QtCore import QThread, pyqtSignal
import serial.tools.list_ports
import serial


class MicrocontrollerInterface(QThread):
    def __init__(self):
        super(MicrocontrollerInterface,self).__init__()
        self.protocol = None
        self.values = None
        self.baudRate = None
        self.numberOfDetections = 1
    
    Exit = pyqtSignal()
    Start = pyqtSignal()
    Load = pyqtSignal()
    Exception_raised = pyqtSignal(object)

    def SetProtocol(self,protocol):
        self.protocol = protocol

    def SetBaudRate(self,rate):
        self.baudRate = int(rate)
    
    def SetDetectionNumber(self, numberOfDetection):
        self.numberOfDetections = int(numberOfDetection)
    
    def SetValues(self,detections):
        value=""
        for i in range(0,self.numberOfDetections,1):
            value+=" id:"+str(detections['detection_classes'][i]) +";prob:"+str(detections['detection_scores'][i]*100)
        self.values = value
        value=""
    

    def run(self):
        self.Load.emit()
        self.ThreadActive = True

        try:
            ser = serial.Serial(self.protocol, self.baudRate)
        except PermissionError:
            self.Exception_raised.emit("Could not access the port")
            self.quit()
            return
        except Exception as ex:
            self.Exception_raised.emit("An error occured while trying to open the port: "+str(ex))
            self.quit()
            return
            
        while self.ThreadActive:
            self.Start.emit()
            ser.write((str(self.values)+'\n').encode())
        ser.close()

    def stop(self):
        self.ThreadActive = False
        self.Exit.emit()
        self.quit()