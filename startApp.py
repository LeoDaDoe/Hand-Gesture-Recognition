from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QComboBox, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5 import uic

import serial.tools.list_ports
import sys

from modelLoader import ModelLoader
from detectionWorker import DetectionWorker
from microcontrollerInterface import MicrocontrollerInterface
from util import showMessage



class Home(QMainWindow):
     
    def __init__(self):
        super(Home,self).__init__()
        uic.loadUi('./UI/HomeWindow.ui',self)
        self.detection_model = None
        self.MicrocontrollerInterface = MicrocontrollerInterface()
        self.CameraThread = DetectionWorker()

        self.Cbox_USBDevices = self.findChild(QComboBox,'CBox_USBDevices')
        self.TextField_BaudRate = self.findChild(QLineEdit,'TextField_BaudRate')
        self.TextField_BoxNumber = self.findChild(QLineEdit,'TextField_BoxNumber')

        self.Label_Detection = self.findChild(QLabel,'Label_Detection')
        self.Label_ModelState = self.findChild(QLabel,'Label_ModelState')
        self.Label_Spinner = self.findChild(QLabel,'Label_Spinner')
        self.Label_Status = self.findChild(QLabel,'Label_Status')

        self.Btn_OpenComm = self.findChild(QPushButton,'Btn_OpenComm')
        self.Btn_CloseComm = self.findChild(QPushButton,'Btn_CloseComm')
        self.Btn_StartDetection = self.findChild(QPushButton,'Btn_StartDetection')
        self.Btn_StopDetection = self.findChild(QPushButton,'Btn_StopDetection')
        self.Btn_RefreshUSBDevices = self.findChild(QPushButton,'Btn_RefreshUSBDevices')
        self.Btn_LoadModel = self.findChild(QPushButton,'Btn_LoadModel')

        self.TextField_BaudRate.setText("9600")
        self.TextField_BoxNumber.setText("1")
        self.Btn_StopDetection.setEnabled(False)
        self.Btn_StartDetection.setEnabled(False)
        self.Btn_CloseComm.setEnabled(False)
        #self.Btn_OpenComm.setEnabled(False)


        def ShowProgressStatus(status):
            self.Label_Status.setText(status)
            movie = QMovie('./Resources/Gif/Spinner.gif')
            self.Label_Spinner.setMovie(movie)
            movie.start()

        def ShowStatus(status,iconPath):
            self.Label_Status.setText(status)
            self.Label_Spinner.setPixmap(QPixmap(iconPath))


        def HideProgressStatus():
            self.Label_Status.clear()
            self.Label_Spinner.clear()

        def RefreshUSBPortList():
            self.Cbox_USBDevices.clear()
            ports = serial.tools.list_ports.comports()
            if len(ports)>0:
                for port in sorted(ports):
                    self.Cbox_USBDevices.addItem(port.name)
        self.Btn_RefreshUSBDevices.clicked.connect(RefreshUSBPortList)


        def ModelLoadStart_Handler():
            self.Btn_LoadModel.setEnabled(False)
            ShowProgressStatus("Loading model")
        def ModelLoadEnd_Handler(model):
            if(model==None):
                showMessage('Model error',2,'Failed to load the model')
                self.Label_ModelState.setText("Error loading model")
                self.Btn_LoadModel.setEnabled(True)
                return     
            self.Label_ModelState.setText("Loaded")
            self.Label_ModelState.setStyleSheet(r"QLabel {color: green;}")
            self.detection_model=model
            self.Btn_StartDetection.setEnabled(True)
            self.Btn_LoadModel.setEnabled(False)
            self.CameraThread.SetModel(self.detection_model)
            ShowStatus('Model loaded successfully','./Resources/Icons/pass.png')

        def LoadModel():         
            self.ModelLoader = ModelLoader()
            self.ModelLoader.Start.connect(ModelLoadStart_Handler)
            self.ModelLoader.DetectionModel.connect(ModelLoadEnd_Handler)        
            self.ModelLoader.start()
        self.Btn_LoadModel.clicked.connect(LoadModel)

        def FetchWebcamFrame(Image):
            self.Label_Detection.setPixmap(QPixmap.fromImage(Image))


        def DetectionStart_Handler():
            self.Btn_StopDetection.setEnabled(True)
            self.Btn_StartDetection.setEnabled(False)
            self.Btn_OpenComm.setEnabled(True)
            ShowStatus('Successfully started model','./Resources/Icons/pass.png')
        def DetectionLoad_Handler():
            ShowProgressStatus("Preparing the model")
        def DetectionStop_Handler():
            self.Label_Detection.clear()
            self.Label_Detection.setText("No image")
            self.Btn_StartDetection.setEnabled(True)
            self.Btn_StopDetection.setEnabled(False)
        def DetectionException_Handler(ex):
            showMessage('Detection error',3,ex)
            ShowStatus('Error preparing the model','./Resources/Icons/error.png')
            self.Btn_StartDetection.setEnabled(True)
            self.Btn_StopDetection.setEnabled(False)


        def ConnectDetectionHandlers():
            self.CameraThread.ImageUpdate.connect(FetchWebcamFrame)   
            self.CameraThread.Detections.connect(self.MicrocontrollerInterface.SetValues)
            self.CameraThread.Load.connect(DetectionLoad_Handler)
            self.CameraThread.Start.connect(DetectionStart_Handler)
            self.CameraThread.Exception_raised.connect(DetectionException_Handler)
            self.CameraThread.Exit.connect(DetectionStop_Handler)   

        def StartDetection():               
            self.CameraThread.start() 
        self.Btn_StartDetection.clicked.connect(StartDetection)
        
        def StopDetection():
            self.CameraThread.stop()
        self.Btn_StopDetection.clicked.connect(StopDetection)

        def CommunicationStart_Handler():
            self.Btn_OpenComm.setEnabled(False)
            self.Btn_CloseComm.setEnabled(True)
            ShowStatus('Successfully opened port','./Resources/Icons/pass.png')
        def CommunicationStop_Handler():
            self.Btn_OpenComm.setEnabled(True)
            self.Btn_CloseComm.setEnabled(False)
            ShowStatus('Successfully closed port','./Resources/Icons/pass.png')
        def CommunicationLoad_Handler():
            self.Btn_OpenComm.setEnabled(False)
            self.Btn_CloseComm.setEnabled(False)
            ShowProgressStatus("Attempting to open port")
        def CommunicationException_Handler(ex):
            showMessage('Communication Error',3,ex)
            ShowStatus('Failed to open the port','./Resources/Icons/error.png')
            self.Btn_OpenComm.setEnabled(True)
            self.Btn_CloseComm.setEnabled(False)

        def ConnectMicrocontrollerHandlers():
            self.MicrocontrollerInterface.Start.connect(CommunicationStart_Handler)
            self.MicrocontrollerInterface.Exit.connect(CommunicationStop_Handler)
            self.MicrocontrollerInterface.Load.connect(CommunicationLoad_Handler)
            self.MicrocontrollerInterface.Exception_raised.connect(CommunicationException_Handler)

        def StartCommunication():
            if(self.Cbox_USBDevices.currentText()==''):
                showMessage('Error starting communication',2,'No port selected')
                ShowStatus('No communication port set','./Resources/Icons/error.png')
                return

            if(self.TextField_BaudRate.text()=='' or not self.TextField_BaudRate.text().isnumeric()):
                showMessage('Error starting communication',2,'Invalid baud rate')
                ShowStatus('No baud rate set','./Resources/Icons/error.png')
                return

            if(self.TextField_BoxNumber.text()=='' or not self.TextField_BoxNumber.text().isnumeric() or int(self.TextField_BoxNumber.text())<1):
                showMessage('Error starting communication',2,'Invalid number of detections')
                ShowStatus('No number of detections set','./Resources/Icons/error.png')
                return

            self.MicrocontrollerInterface.SetProtocol(self.Cbox_USBDevices.currentText())
            self.MicrocontrollerInterface.SetBaudRate(self.TextField_BaudRate.text())
            self.MicrocontrollerInterface.SetDetectionNumber(self.TextField_BoxNumber.text())

            try:
                self.MicrocontrollerInterface.start()
            except:
                ShowStatus('An error occured while trying to open port','./Resources/Icons/error.png')
                return
        self.Btn_OpenComm.clicked.connect(StartCommunication)

        def StopCommunication():
            self.MicrocontrollerInterface.stop()
        self.Btn_CloseComm.clicked.connect(StopCommunication)

        ConnectMicrocontrollerHandlers()
        ConnectDetectionHandlers()
        RefreshUSBPortList()
        self.show()



def main():
    app = QApplication(sys.argv)
    HomeWindow = Home()
    app.exec_()



if __name__=='__main__':
    main()