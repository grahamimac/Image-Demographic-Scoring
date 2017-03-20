# Using Images to Obtain Demographic Variables

The goal of this code is to test whether images can be used to estimate basic demographics - Age, Race, and Sex. Some studies have show this can be done well for gender and race, but that age is more difficult. My brief test with comparing faces seems to point that way as well. CFD files can be downloaded here: http://faculty.chicagobooth.edu/bernd.wittenbrink/cfd/download/download.html. 

## Running face comparison code

You first need to install dlib. Then to analyze faces for demographic characteristics, place the images in the faces folder and run.

``` bash
python Compare_Faces.py
```

You'll get a list of tuples, with lower scores being the most likely assignment of demographics.

## Running gcForest image analysis code

This code, in the gcForest folder, uses the gcForest implementation to to a deep-learning like analysis on the images and try to predict the demographic characteristics using multi-grained scanning and random forests. For this analysis, you will need to download the CFD datasets and change the relative path in the Python file to reference it.

## Running Deep Learning Age Prediction

Deep learning age prediction uses the pre-trained IMDB-Wiki model from https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/ - you'll first need to install dlib and caffe, and download the caffemodel file https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/dex_imdb_wiki.caffemodel that's too big to put on Github. Place any number of images in the imdb-wiki folder, and run classify.py. The algorithm uses the average image from ImageNet, so it may not be as accurate for this model, but the authors do not provide the average image from the model where I got the caffemodel.

``` bash
python classify.py
```

It will output a dictionary of predicted ages for your files. A value of 0 indicates that a face couldn't be detected.