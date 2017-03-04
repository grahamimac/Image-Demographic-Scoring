# Parts modified from different programs in dlib - https://github.com/davisking/dlib

import sys
import os
import dlib
import glob
from skimage import io
import pandas as pd
import numpy as np
import json
import multiprocessing

def score_face(file):
	print("Processing file: {}".format(file))
	img = io.imread(file)
	dets = detector(img, 1)
	print("Number of faces detected: {}".format(len(dets)))
	for k, d in enumerate(dets):
		shape = sp(img, d)
		face_descriptor = facerec.compute_face_descriptor(img, shape)
		np_face_descriptor = np.array(face_descriptor).tolist()
		return np_face_descriptor
		break


if __name__ == '__main__':
	predictor_path = "shape_predictor_68_face_landmarks.dat"
	face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"

	detector = dlib.get_frontal_face_detector()
	sp = dlib.shape_predictor(predictor_path)
	facerec = dlib.face_recognition_model_v1(face_rec_model_path)

	cfd_path = '../../Downloads/CFD Version 2.0.3/'
	data = pd.read_excel(cfd_path + 'CFD 2.0.3 Norming Data and Codebook.xlsx', header=4)
	data["Age_Range"] = ""
	ranges = [(x-1, x+4) for x in range(1,100,5)]
	for rang in ranges:
		data["Age_Range"][np.multiply(data["Age"] > rang[0], data["Age"] <= rang[1])] = str(rang[0]) + " to " + str(rang[1])
	data = data[["Target","Race","Gender","Age_Range"]]

	images = []
	for image in data["Target"].values.tolist():
		images.append(glob.glob(os.path.join(cfd_path + 'CFD 2.0.3 Images/' + image, "*N.jpg"))[0])

	p = multiprocessing.Pool(2)
	faces = p.map(score_face, images)

	dat = []
	for a, b, c, d in zip(data["Race"], data["Gender"], data["Age_Range"], faces):
		dat.append({"age": c, "gender": b, "race": a, "face": d})

	f = open('CFD values.json', 'w')
	json.dump(dat, f)
	f.close()


