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
import operator
from PIL import Image

def score_face(file):
	print("Processing file: {}".format(file))
	img = io.imread(file)
	dets = detector(img, 1)
	print("Number of faces detected: {}".format(len(dets)))
	for k, d in enumerate(dets):
		shape = sp(img, d)
		face_descriptor = facerec.compute_face_descriptor(img, shape)
		np_face_descriptor = np.array(face_descriptor).tolist()
		break
	return compare_face(np_face_descriptor)

def compare_face(face_descriptor):
	data1 = list(data)
	for i in range(len(data)):
		data1[i]["diff"] = np.linalg.norm(np.array(face_descriptor) - np.array(data[i]["face"]))
	dat = pd.DataFrame(data1)
	scores = {}
	for a in ["age","race","gender"]:
		race_score = dat.groupby(a, as_index = False).mean()
		race_score["mindiff"] = np.subtract(race_score["diff"], race_score["diff"].min())
		for x, y, z in zip(race_score[a], race_score["diff"], race_score["mindiff"]):
			scores[a + x] = y
			scores["rel_" + a + x] = z
	return sorted(scores.items(), key=operator.itemgetter(1))

if __name__ == '__main__':
	predictor_path = "shape_predictor_68_face_landmarks.dat"
	face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"

	detector = dlib.get_frontal_face_detector()
	sp = dlib.shape_predictor(predictor_path)
	facerec = dlib.face_recognition_model_v1(face_rec_model_path)

	face_path = 'faces/'

	f = open('CFD values.json', 'r')
	data = json.load(f)

	for file in glob.glob(os.path.join(face_path + '*')):
		extension = file.split('.')[-1].lower()
		if extension not in ['jpg', 'jpeg']:
			im = Image.open(file)
			im.save(file.split('.' + extension)[0] + '.jpg')
			os.remove(file)

	faces = glob.glob(os.path.join(face_path + "*.jpg")) + glob.glob(os.path.join(face_path + "*.jpeg"))

	p = multiprocessing.Pool(2)
	faces = p.map(score_face, faces)
	for f in faces:
		print f


