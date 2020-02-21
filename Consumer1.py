import cv2
import zmq
import sys
from config import * 
import pickle
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu


def apply_threshold(image):
    grayscale = rgb2gray(image)
    thresh = threshold_otsu(grayscale)
    binary = grayscale <= thresh
    return binary

def msg_to_image(message):
    message = pickle.loads(message)
    frameNum = message["frameNum"]
    image = message["img"]
    return frameNum, image

def image_to_msg(frameNum, frame):
    msgD = {"frameNum": frameNum, "img": frame}
    msg = pickle.dumps(msgD)
    return msg

senderSocket = configure_Publisher(sys.argv[2])
receiverSocket = configure_Replier(sys.argv[1])
while True:
    message = receiverSocket.recv()
    frameNum, image = msg_to_image(message)
    binaryImage = apply_threshold(image)
    senderSocket.send(image_to_msg(frameNum, binaryImage))