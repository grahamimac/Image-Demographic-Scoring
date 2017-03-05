# Using Images to Obtain Demographic Variables

The goal of this code is to test whether images can be used to estimate basic demographics - Age, Race, and Sex. Some studies have show this can be done well for gender and race, but that age is more difficult. My brief test seems to point that way as well. CFD files can be downloaded here: http://faculty.chicagobooth.edu/bernd.wittenbrink/cfd/download/download.html. 

## Running code

To analyze faces for demographic characteristics, place the images in the faces folder and run.

``` bash
python Compare_Faces.py
```

You'll get a list of tuples, with lower scores being the most likely assignment of demographics.