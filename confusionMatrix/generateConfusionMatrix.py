import tensorflow as tf
import pandas as pd
import cv2 as cv2
import numpy as np
from collections import namedtuple
from PIL import Image

basePath = './confusionMatrix/dataset/'

def GetGestureName(id):
    if(id==''):
        return "None"
    if(id==2):
        return "Punch_VFR"
    if(id==3):
        return "Punch_VFL"
    if(id==4):
        return "One_VFR"
    if(id==5):
        return "One_VFL"
    if(id==6):
        return "Two_VFR"
    if(id==7):
        return "Two_VFL"
    if(id==8):
        return "Three_VFR"
    if(id==9):
        return "Three_VFL"
    if(id==10):
        return "Four_VFR"
    if(id==11):
        return "Four_VFL"
    if(id==12):
        return "Five_VFR"
    if(id==13):
        return "Five_VFL"
    if(id==14):
        return "Six_VFR"
    if(id==15):
        return "Six_VFL"
    if(id==16):
        return "Seven_VFR"
    if(id==17):
        return "Seven_VFL"
    if(id==18):
        return "Eight_VFR"
    if(id==19):
        return "Eight_VFL"
    if(id==20):
        return "Nine_VFR"
    if(id==21):
        return "Nine_VFL"
    if(id==22):
        return "Span_VFR"
    if(id==23):
        return "Span_VFL"
    if(id==24):
        return "Horiz_HBL"
    if(id==25):
        return "Horiz_HFL"
    if(id==26):
        return "Horiz_HBR"
    if(id==27):
        return "Horiz_HFR"
    if(id==28):
        return "Collab"
    if(id==29):
        return "XSign"
    if(id==30):
        return "TimeOut"

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]

def loadModel():
    model = tf.saved_model.load('./hand_detection_model/saved_model')
    return model

def readImage(path):
    print(path.filename.values[0])
    image = cv2.imread(basePath+path.filename.values[0])
    return image


def printPredictions(model):
    test_dataset_CSV = pd.read_csv('L:/University/Thesis/Code/Model_Interface/confusionMatrix/dataset/test_labels.csv')
    grouped = split(test_dataset_CSV, 'filename')

    for index, row in grouped:
        frame = readImage(row)
        #frame = np.asarray(frame)
        #frame = cv2.convertScaleAbs(frame,alpha=1.2, beta=30)

        image_np = np.array(image_resize(frame,640,640))
        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)

        detections = model(input_tensor)
    
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        print("Ground truth class: {} Predicted Class: {} Confidence: {}      ".format(row.values[0],GetGestureName(detections['detection_classes'][0]),detections['detection_scores'][0]*100))


def main():
    model = loadModel()
    printPredictions(model)


if __name__=='__main__':
    main()
