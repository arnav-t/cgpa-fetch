from PIL import Image
import pytesseract as pyt

def getCaptchaText(image):
	threshold = 30
	img = Image.open(image)
	pixels = img.load()
	for y in range(img.size[1]):
		if pixels[0,y][0] <= threshold:
			for x in range(img.size[0]):
				try:
					pixels[x,y] = pixels[x,y-1]
				except:
					break
	for x in range(img.size[0]):
		if pixels[x,img.size[1] -1][0] <= threshold:
			for y in range(img.size[1]):
				try:
					pixels[x,y] = pixels[x-1,y]
				except:
					break
	if __name__ == '__main__':
		img.show()
	return pyt.image_to_string(img)

if __name__ == '__main__':
	print(getCaptchaText('captcha.jpeg'))
