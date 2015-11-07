from skimage import io 
from skimage.filters import threshold_otsu, threshold_li, threshold_yen
from skimage import feature
from scipy import ndimage as ndi
from skimage.color import rgb2gray

import matplotlib.pyplot as plt

def processImage(captchaPath, report=None, backgroundLayerPath=None, canny_sigma=0.1, corner_min_dist=2, debug = False):
	"""
		Processes the given image and returns a number of feature points.
		These feature points are presumably corner points of the tetragon.
	"""
	image = io.imread(captchaPath, True);
	
	image_without_bg = None
	
# remove background, if available
	if not None == backgroundLayerPath:
		bgl = io.imread(backgroundLayerPath, True)
		image_without_bg = (image - bgl)
	else:
		image_without_bg = image

# applying threshold operators
	thresh = threshold_otsu(image_without_bg)
	thrs_image = image_without_bg > thresh

	thresh_li = threshold_li(image_without_bg)
	thrs_image_li = image_without_bg > thresh_li

	thresh_yen = threshold_yen(image_without_bg)
	thrs_image_yen = image_without_bg > thresh_yen

#	thrs_image = thrs_image * thrs_image_li * thrs_image_yen
	thrs_image = image_without_bg * thrs_image
	thrs_image = thrs_image * thrs_image_li
	thrs_image = thrs_image * thrs_image_yen

#	thrs_image = ndi.gaussian_filter(thrs_image, 0.8)
# take the gray image
	gray_result = rgb2gray(thrs_image)

# find edges
#	canny_result = feature.canny(gray_result, sigma=0.5, low_threshold=1.8)
	canny_result = gray_result 

# store image
	processedImageName = captchaPath[0:len(captchaPath)-4] + "_processed.png"
	io.imsave(processedImageName, canny_result.clip(-1, 1))
	if not None == report:
		report.setProcessedImage(processedImageName)

	coords = feature.corner_peaks(feature.corner_harris(canny_result), min_distance=corner_min_dist)

	if debug:
		fig, axes = plt.subplots(nrows=6, figsize=(8, 3))
		ax0, ax1, ax2, ax3, ax4, ax5 = axes

		ax0.imshow(image, cmap=plt.cm.gray)
		ax0.set_title('Original image')
		ax0.axis('off')

		ax1.imshow(image_without_bg, cmap=plt.cm.gray)
		ax1.set_title('Image without background')
		ax1.axis('off')

		ax2.imshow(thrs_image, cmap=plt.cm.gray)
		ax2.set_title('Thresholded image')
		ax2.axis('off')

		ax3.imshow(gray_result, cmap=plt.cm.gray)
		ax3.set_title('After RGB -> Gray')
		ax3.axis('off')

		ax4.imshow(canny_result, cmap=plt.cm.gray)
		ax4.set_title('After Canny')
		ax4.axis('off')

		ax5.imshow(canny_result, cmap=plt.cm.gray)
		ax5.plot(coords[:, 1], coords[:, 0], '+r', markersize=15)
		ax5.set_title('Detected Features')
		ax5.axis('off')

		plt.show()

	return coords

def test():

	image_name = "./captcha/captcha_02-11-15_19-29-26.png"
	background = "./captcha/captcha_bg_02-11-15_19-29-26.png"

	processImage(image_name, backgroundLayerPath=background, debug=True, corner_min_dist=5)

if __name__ == '__main__':
	test()
