import boto3
import glob
from PIL import Image
import os

# Code to analyze faces using Amazon Rekognition - need to setup aws cli --configure beforehand
# Modified from https://gist.github.com/alexcasalboni/0f21a1889f09760f8981b643326730ff and http://stackoverflow.com/questions/41388926/an-example-of-calling-aws-rekognition-http-api-from-python

def detect_faces(img, attributes=['ALL'], region="us-east-1"):
	with open(img, 'r') as image:
		image_b = image.read()
	rekognition = boto3.client("rekognition", region)
	response = rekognition.detect_faces(
	    Image={
			"Bytes": image_b
		},
	    Attributes=attributes,
	)
	return response['FaceDetails']

face_path = 'faces/'

for file in glob.glob(os.path.join(face_path + '*')):
	extension = file.split('.')[-1].lower()
	if extension not in ['jpg', 'jpeg']:
		im = Image.open(file)
		im.save(file.split('.' + extension)[0] + '.jpg')
		os.remove(file)

faces = glob.glob(os.path.join(face_path + "*.jpg")) + glob.glob(os.path.join(face_path + "*.jpeg"))
for face in faces:
	print(detect_faces(face))