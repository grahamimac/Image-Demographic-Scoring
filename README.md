# Using Images to Obtain Demographic Variables

The goal of this code is to test whether images can be used to estimate basic demographics - Age, Race, and Sex. Some studies have show this can be done well for gender and race, but that age is more difficult. My brief test with comparing faces seems to point that way as well. CFD files can be downloaded here: http://faculty.chicagobooth.edu/bernd.wittenbrink/cfd/download/download.html. 

## Running face comparison code

You first need to install dlib. Then to analyze faces for demographic characteristics, place the images in the faces folder and run.

``` bash
python Compare_Faces.py
```

You'll get a list of tuples, with lower scores being the most likely assignment of demographics.

## Running Deep Learning Age Prediction

### Caffe Model

Deep learning age prediction uses the pre-trained IMDB-Wiki model from https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/ - you'll first need to install dlib and caffe, and download the caffemodel file https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/dex_imdb_wiki.caffemodel that's too big to put on Github. Place any number of images in the imdb-wiki folder, and run classify.py. The algorithm uses the average image from ImageNet, so it may not be as accurate for this model, but the authors do not provide the average image from the model.

``` bash
python classify.py
```

It will output a dictionary of predicted ages for your files. A value of 0 indicates that a face couldn't be detected.

### Amazon Rekognition

In February, Amazon released a service through AWS that uses the company's deep learning algorithm Rekognition to analyze images for gender and age, among other features. The service costs $1 per 1,000 faces analyzed, and requires an AWS account. You must also install AWS CLI and run `aws cli --configure`, passing in your access key and secret key to make the service work. Then, you can run the python file.

``` bash
python Score_Faces_Recognition.py
```

I will output a dictionary of different attributes and their scores for each of the files.