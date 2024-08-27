import sys
import os
import re
from PIL import Image, ExifTags
from pillow_heif import register_heif_opener
register_heif_opener()


class HeicToJpeg:
	# Set the working directory to the script location, if no CLI second argument supplied for directory.
	# Process all heic files in that directory.
	# @return	void
	def __init__ (self):
		self.workingDirectory = '.'
		if (len(sys.argv) == 2):
			self.workingDirectory = sys.argv[1]

		self.sourceFormat = 'heic'
		self.targetFormat = 'jpg'
		self.processImages()


	# Convert all heic files in the provided working directory
	# @return	void
	def processImages (self):
		for file in os.listdir(self.workingDirectory):
			# Filter for the desired format/filetype of images to convert.
			if (file.endswith('.' + self.sourceFormat)):
				self.name = re.sub('\\.[a-z|A-Z]+$', '', file)
				self.processImage()



	# Convert a heic file to a jpeg if not already done so.
	# @return	void
	def processImage (self):
		# Proceed only if target file of the same name does not already exist
		if (not os.path.exists(self.workingDirectory + '/' + self.name + '.' + self.targetFormat)):
			self.saveNewFormat()
			print(self.name + '.' + self.targetFormat + ' created.')
			return

		print(self.name + '.' + self.targetFormat + ' already exists!')


	# Save a copy in the new format, whilst trying to maintain the original orientation.
	# @return	void
	def saveNewFormat (self):
		# Open the heic file and check if any exif meta data on orientation is present.
		img = Image.open(self.workingDirectory + '/' + self.name + '.' + self.sourceFormat)
		orientation = self.checkOrientation(img)
	
		# Leave the orientation unchanged if nothing found or it seems normal (1)
		if (type(orientation) == type(2) and orientation >= 2):
			img = self.maintainOrientation(orientation, img)
	
		# Save a copy.
		img.save(self.workingDirectory + '/' + self.name + '.' + self.targetFormat)


	# Check the image exif meta data if possible, to assertain the orientation used by the photographer.
	# @param		PIL.image	image	The image to check
	# @return	int					The image orientation
	def checkOrientation (self, image):
		if hasattr(image, 'getexif'):
			# Attempt to assertain the key number for 'Orientation' in the meta data tags.
			for orientationKey in ExifTags.TAGS.keys():
				if ExifTags.TAGS[orientationKey] == 'Orientation':
					break

			# Now retieve the meta data for the picture
			exifPull = image.getexif()

			# Only continue with re-orientation if some meta data was found
			if (exifPull is not None):
				exif = dict(exifPull.items())

				# Even if we have the key number from the tags it may not be present, so check
				if (orientationKey in exif):
					return exif[orientationKey]

		return False

				
	# Rotate an image to match the original's orientation.
	# @param		int			orientation	Current orientation
	# @param		PIL.image	image			Image to re-orientate
	# @return	PIL.image					The image rotated (if needed)
	def maintainOrientation (self, orientation, image):
		# Rotate the picture so that when re-saved
		# the orientation matches the original (e.g from mobile phones placed on their side).
		match orientation:
			case 3:
				return image.transpose(Image.ROTATE_180)
			case 6:
				return image.transpose(Image.ROTATE_270)
			case 8:
				return image.transpose(Image.ROTATE_90)
			case _:
				return image


if (__name__ == '__main__'):
	HeicToJpeg()