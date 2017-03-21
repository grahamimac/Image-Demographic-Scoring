
# Gets image mean for IMDB face images from https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/imdb_crop.tar
import glob
import os
from skimage import io
import numpy as np

folders = [str(x).zfill(2) for x in range(100)]
faces = []
for folder in folders:
	faces += glob.glob(os.path.join(folder + "/*.jpg"))

a = []
progress = 0
for face in faces:
	img = io.imread(face)
	a.append(np.mean(np.mean(img, 0), 0))
	progress += 1
	print progress
	if progress % 1000 == 0: print("Processed {} of {} - mean {}").format(progress, len(faces), np.mean(np.array(a), 0))
print np.mean(np.array(a), 0)