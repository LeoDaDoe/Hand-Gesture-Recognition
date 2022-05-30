from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtGui import QImage

import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils

import cv2 
import numpy as np

from util import showMessage

class DetectionWorker(QThread):
    def __init__(self):
        super(DetectionWorker,self).__init__()
        self.category_index = label_map_util.create_category_index_from_labelmap('./hand_detection_model/saved_model/assets/labelMap.pbtxt')
    
    ImageUpdate = pyqtSignal(QImage)
    Detections = pyqtSignal(object)
    Load = pyqtSignal()
    Start = pyqtSignal()
    Exception_raised = pyqtSignal(object)
    Exit = pyqtSignal()

    def SetModel(self,model):
        self.detection_model = model

    def image_resize(self,image, width = None, height = None, inter = cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image

        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)

        else:
            r = width / float(w)
            dim = (width, int(h * r))

        resized = cv2.resize(image, dim, interpolation = inter)

        return resized

    def run(self):
        self.Load.emit()
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        if(Capture==None):
            showMessage('Camera error',3,'No camera found on the first port')
            self.ThreadActive = False
            self.quit()

        self.Start.emit()
        while self.ThreadActive:          
            ret, frame = Capture.read()
            if ret:
                #frame[frame<255-40]+=40

                frame = cv2.convertScaleAbs(frame,alpha=1.1, beta=20)

                image_np = np.array(self.image_resize(frame,640,640))
                input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)

                try:
                    detections = self.detection_model(input_tensor)
                except Exception as ex:
                    self.Exception_raised.emit(ex)
                    self.ThreadActive = False
                    self.quit()
                
                
                num_detections = int(detections.pop('num_detections'))
                detections = {key: value[0, :num_detections].numpy()
                            for key, value in detections.items()}
                detections['num_detections'] = num_detections

                detections['detection_classes'] = detections['detection_classes'].astype(np.int64)


                label_id_offset = 0
                image_np_with_detections = image_np.copy()

                viz_utils.visualize_boxes_and_labels_on_image_array(
                    image_np_with_detections,
                    detections['detection_boxes'],
                    detections['detection_classes']+label_id_offset,
                    detections['detection_scores'],
                    self.category_index,
                    use_normalized_coordinates=True,
                    max_boxes_to_draw=1,
                    min_score_thresh=.8,
                    agnostic_mode=False)


                Image = cv2.cvtColor(image_np_with_detections, cv2.COLOR_BGR2RGB)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(321, 260, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                self.Detections.emit(detections)
        self.Exit.emit()


    def stop(self):
        self.ThreadActive = False      
        self.quit()

