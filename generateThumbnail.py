# Generates a thumbnail for every image contained in a folder and subfolders.
# Author: Marco Pinato, 02/12/2018

import os
import sys

import cv2
import numpy as np

from overlayImage import is_image


def generate_thumb(img, thumbShape, keepAspectRatio=True):
    """
    Generates a thumbnail of @img of shape @thumbShape. If @keepAspectRatio is 
    True, @thumbShape will be overridden, using just the width of the specified 
    image.
    The number of channels in the image is automatically inferred.
    """
    if not type(thumbShape[0]) and type(thumbShape[1]):
        print('All values of shape must be integers')
        return 1
    if not keepAspectRatio:
        thumb = cv2.resize(img, thumbShape)
    else:
        aspectRatio = img.shape[1]/img.shape[0]
        thumbWidth = thumbShape[1]
        thumbHeight = int(thumbShape[0]*aspectRatio)
        thumb = cv2.resize(img, (thumbHeight, thumbWidth))

    return thumb


def process_folder(masterFolder, thumbShape, keepAspectRatio=True):
    """
    Replaces all the images in @masterFolder and subdirectories with thumbs.
    @masterFolder should be complete with path
    @thumbShape, @keepAspectRatio are parameters of generate_thumb
    """
    for root, _, _ in os.walk(os.path.abspath(masterFolder)):
        filenames = [os.path.join(root, filename)
                     for filename in os.listdir(root)
                     if is_image(os.path.join(root, filename))]

        for filename in filenames:
            print('Replacing ', filename, ' with its thumbnail.')
            img = cv2.imread(os.path.join(root, filename), 3)
            thumb = generate_thumb(img, thumbShape, keepAspectRatio)
            cv2.imwrite(filename, thumb)


def main():
    SHAPE = (256, 256)
    try:
        masterFolder = sys.argv[1]
    except IndexError:
        home = os.environ.get('HOME')
        desktop = os.path.join(home, 'Desktop')
        masterFolder = os.path.join(desktop, 'images')

    process_folder(masterFolder, SHAPE, True)


if __name__ == '__main__':
    main()
