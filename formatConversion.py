# Convert all images contained into an input folder in a given format, 
# and save them in an output folder.

# Author: Marco Pinato, 26/02/2018
import cv2
import os

# Returns a list with all the filenames in a folder
def get_all_images_filenames(folder):
    filenames = []
    for filename in os.listdir(folder):
         filenames.append(filename)
    return filenames

PNG_QUALITY_LEVEL = 9 # 0-9
JPEG_QUALITY_LEVEL = 100 # 0-100


extensionOut = 'png'
inputFolderName = 'input'
outputFolderName = 'output_' + extensionOut
currentPath = os.path.dirname(os.path.abspath(__file__))
inputPath = os.path.join(currentPath,inputFolderName) 
outputPath = os.path.join(currentPath,outputFolderName) 

# Try to create a folder, and ignore the exception raised if the folder
# already exists.
try:
    os.makedirs(outputPath)
except OSError:
    if not os.path.isdir(outputPath):
        raise

# For each image, read it and convert it.
imagesNamesList = get_all_images_filenames(inputPath)

for imageName in imagesNamesList: 
    print('Reading ' + imageName)
    name = os.path.join(inputPath,imageName) 
    image = cv2.imread(name)
    # Replace current extension with the output one
    name, separator, extensionIn = imageName.partition('.')
    imageNameOut = os.path.join(outputPath,name + separator + extensionOut)
    print('Writing ' + imageNameOut)

    if extensionOut == 'png':
        # Workaround for OpenCV bug: see
        # https://stackoverflow.com/questions/10410521/opencv-python-save-jpg-specifying-
        # quality-gives-systemerror
        cv2.imwrite(imageNameOut, image, [int(cv2.IMWRITE_PNG_COMPRESSION),PNG_QUALITY_LEVEL])
    elif extensionOut == 'jpg':
        # Workaround for OpenCV bug: see
        # https://stackoverflow.com/questions/10410521/opencv-python-save-jpg-specifying-
        # quality-gives-systemerror
        cv2.imwrite(imageNameOut, image, [int(cv2.IMWRITE_JPEG_QUALITY),JPEG_QUALITY_LEVEL])

