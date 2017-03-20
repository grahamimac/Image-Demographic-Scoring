# Inspired by http://nbviewer.jupyter.org/github/BVLC/caffe/blob/master/examples/00-classification.ipynb

import numpy as np
import os
import caffe
import dlib
import glob
from skimage import io
import scipy.misc

proto = 'age.prototxt'
model = 'dex_imdb_wiki.caffemodel'
image = 'test.JPG'
cur_path = os.path.dirname(os.path.realpath(image))
if cur_path[-1] == '/': cur_path = cur_path[:-1]

caffe.set_mode_cpu()

print("Starting Basic Classifier")
net = caffe.Classifier(proto, model, caffe.TEST)

print("Setting up transform")
mu = np.array([104.0069879317889, 116.66876761696767, 122.6789143406786]) # ImageNet mean
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

print("Getting faces")
face_path = ''
faces = glob.glob(os.path.join(face_path + "*.jpg")) + glob.glob(os.path.join(face_path + "*.jpeg"))

# set the size of the input (we can skip this if we're happy
#  with the default; we can also change it later, e.g., for different batch sizes)
net.blobs['data'].reshape(len(faces),        # batch size
                          3,         # 3-channel (BGR) images
                          224, 224)  # image size is 227x227

print("Preprocessing Image")
predictor_path = "shape_predictor_68_face_landmarks.dat" # https://github.com/davisking/dlib
face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)
def score_face(file):
	print("Getting Face for: {}".format(file))
	img = io.imread(file)
	dets = detector(img, 1)
	print("Number of faces detected: {}".format(len(dets)))
	for k, d in enumerate(dets):
		break
	if len(dets) > 0:
		margin = 0.4
		arr = [d.left(), d.right(), d.top(), d.bottom()]
		asize = [arr[1] - arr[0], arr[3] - arr[2]]
		top = int(arr[2]-(asize[1]*margin))
		bottom = int(arr[3]+(asize[1]*margin))
		left = int(arr[0]-(asize[0]*margin))
		right = int(arr[1]+(asize[0]*margin))
		if top < arr[2]: top = arr[2]
		if bottom > arr[3]: bottom = arr[3]
		if left < arr[0]: left = arr[0]
		if right > arr[1]: right = arr[1]
		image_top = img[top:bottom]
		image_left = np.array([a[left:right] for a in image_top])
		scipy.misc.toimage(image_left, cmin=0.0, cmax=255.0).save(file.replace('.jpg','_cropped.jpg').replace('jpeg','_cropped.jpeg'))
		return True
	else:
		return False

nums = []
for i in range(len(faces)):
	check = score_face(cur_path + faces[i])
	if check:
		image = caffe.io.load_image(cur_path + faces[i].replace('.jpg','_cropped.jpg').replace('.jpeg','_cropped.jpeg'))
		transformed_image = transformer.preprocess('data', image)
		os.remove(faces[i].replace('.jpg','_cropped.jpg').replace('.jpeg','_cropped.jpeg'))
		net.blobs['data'].data[i] = transformed_image
		nums.append(i)	

output = net.forward()
results = []
for i in range(len(faces)):
	if i in nums:
		results.append(output["prob"][i].argmax())
	else:
		results.append(0)
print dict([(a,b) for a,b in zip(faces,results)])