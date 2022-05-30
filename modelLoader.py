from PyQt5.QtCore import pyqtSignal, QThread
import tensorflow as tf
import numpy as np


class ModelLoader(QThread):
    DetectionModel = pyqtSignal(object)
    Start = pyqtSignal()
    End = pyqtSignal()
    def run(self):
        self.Start.emit()
        model = tf.saved_model.load('./hand_detection_model/saved_model')
        self.DetectionModel.emit(model)
        model = None
        self.stop()

    def stop(self):
        self.End.emit()
        self.quit()
