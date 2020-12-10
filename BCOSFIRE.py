import numpy as np
import cosfire as c


def BCOSFIRE(img_rgb, mask=[]):
	## Model configuration

	proto_symm = np.zeros(shape=(201,201)).astype(np.uint8)
	proto_symm[:,100] = 255

	subject = 255 - img_rgb[:,:,1]
	subject = subject/255
	
	cx, cy = (100,100)

	# Symmetrical filter
	cosfire_symm = c.COSFIRE(
		c.CircleStrategy(c.DoGFilter, (2.4, 1), prototype=proto_symm, center=(cx,cy), rhoList=range(0,9,2), sigma0=3,  alpha=0.7,
		rotationInvariance = np.arange(12)/12*np.pi)
	   ).fit()
	resp_symm = cosfire_symm.transform(subject)

	# Asymmetrical filter
	cosfire_asymm = c.COSFIRE(
			c.CircleStrategy(c.DoGFilter, (1.8, 1), prototype=proto_symm, center=(cx,cy), rhoList=range(0,23,2), sigma0=2,  alpha=0.1,
			rotationInvariance = np.arange(24)/12*np.pi)
		   ).fit()


	# Make asymmetrical
	asymmTuples = []
	for tupl in cosfire_asymm.strategy.tuples:
		if tupl[1] <= np.pi:
			asymmTuples.append(tupl)
	cosfire_asymm.strategy.tuples = asymmTuples
	resp_asymm = cosfire_asymm.transform(subject)


	resp = resp_symm + resp_asymm
	resp_symm = c.rescaleImage(resp_symm, 0, 255)
	resp_asymm = c.rescaleImage(resp_asymm, 0, 255)
	resp = np.multiply(resp, mask)
	resp = c.rescaleImage(resp, 0, 255)
	segresp = np.where(resp > 37, 255, 0)
	return resp,segresp


if __name__ == '__main__':
	import sys
	import cv2
	import matplotlib.pyplot as plt
	img_rgb = cv2.cvtColor(cv2.imread(sys.argv[1],1), cv2.COLOR_BGR2RGB)
	img_rgb = np.pad(img_rgb,((20,20),(20,20),(0,0))) # Add some padding to get rid of the white edges in the output vessel image
	mask = np.ones(shape=img_rgb.shape[:-1])

	resp,segresp = BCOSFIRE(img_rgb,mask)
	resp = resp[20:-20,20:-20]
	p_vessel = resp/np.amax(resp)
	# plt.imsave('./figures/sample_0_out.png',p_vessel,cmap='gray')
	plt.imshow(p_vessel,cmap='gray')
	plt.show()