#!/usr/bin/python3
import sys
import cv2
import logging
import numpy as np
import math
import imutils
from enum import Enum
from networktables import NetworkTables
from cscore import CameraServer, VideoSource, UsbCamera

#   initialize constants for networktables

__IP = '10.35.1.2'
# __SENT_TABLE_NAME = 'tommyTheTable'
# __ORIENTATION_TABLE_NAME = 'Front Or Back'
# TODO: Uncomment when these work

camera_value = None
# get cameraserver instance
cs = CameraServer.getInstance()

print("main method")


def mainMain():
    #   network tables initialization
    NetworkTables.initialize(server=__IP)
    print("nt initialized")
    smartdash = NetworkTables.getTable("SmartDashboard")
    #    table = NetworkTables.getTable(__SENT_TABLE_NAME)
    #    subtable = smartdash.getSubTable(__ORIENTATION_TABLE_NAME)

    #   initialize cameras
    # CAMERA 1
    cam = UsbCamera('Cam 1 Front', 1)
    cam.setResolution(160, 120)
    cam.setExposureManual(0)
    cam.setBrightness(0)
    cam.setFPS(30)
    print("cam1 initialized")
    # CAMERA 2
    cam2 = UsbCamera('Cam 2 Back', 0)
    cam2.setResolution(160, 120)
    cam2.setExposureManual(0)
    cam2.setBrightness(0)
    cam2.setFPS(30)
    print("cam2 initialized")

    # EACH CAMERA STARTS CAPTURING VIDEO
    cs.startAutomaticCapture(camera=cam)
    cs.startAutomaticCapture(camera=cam2)

    # GETTING THE VIDEO STREAM OF EACH CAMERA
    vid = cs.getVideo(camera=cam)
    vid2 = cs.getVideo(camera=cam2)

    #   initialize outputstream, this is the place where we send frames to shuffleboard.
    output_stream = cs.putVideo('TOP CAMERAS', 160, 120)

    print("Running while loop")
    counter = 0
    while True:
        # get front or back value
        camera_value = subtable.getString("value", "FRONT")

        img = np.zeros(shape=(160, 120, 3), dtype=np.uint8)
        #   get video
        time, frame = video.grabFrame(img, 0.5)

        #   This condition sends video from different cameras based on the robots orientation.
        if camera_value == 'BACK':
            print("BACK")
            video = vid
        elif camera_value == 'FRONT':
            print("FRONT")
            video = vid2
        else:
            print('error, no camera value detected')

        print("sending frame")
        # send frame to shuffleboard
        output_stream.putFrame(frame)

        print('Done.')
        sys.stdout.flush()
        # just counting how fast it is running and if it is running at all
        counter += 1
        print(counter)


# END OF TAPE DETECTION

if __name__ == "__main__":
    mainMain()
