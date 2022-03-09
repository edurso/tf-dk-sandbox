#!/usr/bin/env python3
import os
from tkinter import W
from cscore import CameraServer, UsbCamera
import json

def start(config_file: str, cam_num: int, cam_name: str, output_name: str):

    with open(config_file) as cfg:
        config = json.load(cfg)
    camera = config['cameras'][cam_num]
    print(camera)

    width = camera['width']
    height = camera['height']
    cameraPath = camera['path']
    exposure = camera['exposure']
    brightness = camera['brightness']
    cs = CameraServer.getInstance()

    # Test making camera
    cam = UsbCamera(dev=cam_num, name=cam_name)
    cam.setFPS(camera['fps'])

    cam.setResolution(width, height)

    inp = None
    cs.startAutomaticCapture(camera=cam, return_server=True) # Returns `VideoSource`
    inp = cs.getVideo(name=cam_name) # Returns `CvSink`
    if output_name != None:
        out = cs.putVideo(name=output_name, width=width, height=height)
    else:
        out = None

    return inp, out, width, height, cam, exposure, brightness, cameraPath

if __name__ == "__main__":
    print('do not run this script\nsomething is wrong')
