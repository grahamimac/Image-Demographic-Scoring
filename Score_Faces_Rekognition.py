import boto3

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

print(detect_faces('faces/Harrison Ford.jpg'))