#!/usr/bin/env python3

import os
from re import I
from pipeline import VisionPipeline
import camera
import numpy as np
import cv2
import sys
from time import sleep
import grip
import time


class HubPipeline(VisionPipeline):

	def __init__(self, config: str, cam_num: int, cam_name: str, output_name: str, table) -> None:

		self.nttable = table

		self.exposure_entry = table.getEntry('exposure')
		self.capture_entry = table.getEntry('capture frame')
		self.distance_entry = table.getEntry('distance input')

		# Initialize entry as 7	(idk why, just 7)	
		self.exposure_entry.setNumber(7)
		self.capture_entry.setBoolean(False)
		self.distance_entry.setString('42-thousand-tonnes')

		self.pipeline = grip.GripPipeline()

		self.fov_horiz = 0 # TODO Measure horizontal fov on cameras
		self.fov_vert = 0 # TODO Measure vertical fov on cameras

		# start camera
		self.inp, self.out, self.width, self.height, self.cam, self.exposure, self.cameraPath = camera.start(config, cam_num, cam_name, output_name)

		self.targetHeightRatio = 0
		self.targetRatioThreshold = 0

		# allocate image for whenever
		self.img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)
		self.output_img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)

	def process(self):

		# set exposure
		os.system("v4l2-ctl --device " + self.cameraPath + " --set-ctrl=exposure_absolute=" + str(self.exposure_entry.getNumber(7)))	
		# get frame from camera
		self.t, self.img = self.inp.grabFrame(self.img)

		if self.capture_entry.getBoolean(False):
			mills = str(int(time.time() * 1000))
			dist = self.distance_entry.getString('42-thousand-tonnes')
			fname = str('/home/lightning/voidvision/images/frame-distance-{}-{}.jpg'.format(dist, mills))
			cv2.imwrite(fname, self.img)
			print('FILE: {} WRITTEN ... Maybe'.format(fname))
			self.capture_entry.setBoolean(False)

		self.pipeline.process(self.img)

		# TODO grab center of bounding box arounuuud target from grip pipeline
		#row, col = grip.getBlahBlahBlah()

		self.output_img = self.pipeline.rgb_threshold_output
		self.out.putFrame(self.output_img)

		# TODO do some math to correspond the column to an angle offset based on these vars
		targetAngle = 0 # TODO fixme
		centerCol = 0 # Center column of target
		imgWidthCols = 0 # Center Row of target


		# TODO do some more math to correspond row to distance (interpolation table?)
		distance = 3 # TODO fixme

		targetCenterCol = 0 # Should hold the center height of target
		imgWidthCols = 0 # Should hold width of target in columns

		# targetAngle = get_angle_from_target(targetCenterCol, imgWidthCols)
		targetAngle = 15 
		self.nttable.putNumber('Target Angle', targetAngle)
		self.nttable.putNumber('Target Distance', distance)
		try: 
			numContours = len(self.pipeline.filter_contours_output)
		except:
			numContours = -1

		# Puts number of contours detected in current image to the dashboard
		self.nttable.putNumber('Contour Number', numContours)

		# throw output image to dashboard
		self.out.putFrame(self.output_img)

	def get_angle_from_target(self, target_center_col, image_width_cols):
			return (target_center_col - (image_width_cols / 2) * (self.fov_horiz / image_width_cols))
		
	def interpolated_dist_from_target(self):
			pass

	def checkTargetProportion(self, targetBoxHeight, targetCenterRow):
			ratio = targetBoxHeight / targetCenterRow
			return (ratio - self.targetHeightRatio) < self.targetRatioThreshold
