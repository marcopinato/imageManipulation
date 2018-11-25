# Quick script to overlay an image upon every other image in a folder,
# centering it. Can be used for example to place a logo over a series of
# images.

import os
import shutil
import sys

import cv2


def overlay_image_alpha(img, imgOverlay, pos, alphaMask):
    """Overlay @imgOverlay on top of @img at the position @pos and blend using
    @alphaMask.

    @alphaMask must contain values within the range [0, 1] and be the
    same size as @imgOverlay.
    """

    x, y = pos

    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + imgOverlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + imgOverlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(imgOverlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(imgOverlay.shape[1], img.shape[1] - x)

    # Exit if there's nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    channels = img.shape[2]

    alpha = alphaMask[y1o:y2o, x1o:x2o]
    alphaInv = 1.0 - alpha

    for c in range(channels):
        img[y1:y2, x1:x2, c] = (alpha * imgOverlay[y1o:y2o, x1o:x2o, c] +
                                alphaInv * img[y1:y2, x1:x2, c])


def get_logo_center_coordinates(img, logo):
    """
    Identifies the cooordinates to place @logo centered respect to @img.
    """
    w = img.shape[0]/2
    h = img.shape[1]/2

    wL = logo.shape[0]/2
    hL = logo.shape[1]/2

    x = int(w-wL)
    y = int(h-hL)

    # OpenCV uses flip x,y respect to Numpy
    return y, x


def is_image(filename, extensions=['.jpg', '.png', '.tiff']):
    """
    Simple check of whether @filename is an image or not based on @extensions.
    @filename must be complete with path.
    """
    for extension in extensions:
        if os.path.isfile(filename) and filename.endswith(extension):
            return True
    return False


def scale_logo(logo, img, divider=5):
    """
    Scales @logo proportionally to @image, according to @divider factor. 
    Used to overlay a logo to an image, and keep things visually pleasing.
    @logo, @image are Numpy arrays, with the OpenCV axis convention.
    """
    h, w, _ = img.shape
    hL, wL, _ = logo.shape
    wLNew = w/divider
    # Keep aspect ratio by adjusting y accordingly
    logoRatioFactor = wLNew/wL
    hLNew = hL*logoRatioFactor

    return cv2.resize(logo, (int(wLNew), int(hLNew)), cv2.INTER_CUBIC)


def main():
    try:
        logoFilename = sys.argv[1]
        masterDir = sys.argv[2]

    except IndexError:
        home = os.environ.get('HOME')
        desktop = os.path.join(home, 'Desktop')
        masterDir = os.path.join(desktop, 'images')
        logoFilename = os.path.join(desktop, 'logo.png')

    print('Image to overlay: ', logoFilename)
    print('Source directory: ', masterDir)

    # Explore all subdirectories and replace original images.
    for root, _, _ in os.walk(os.path.abspath(masterDir)):
        filenames = [os.path.join(root, filename)
                     for filename in os.listdir(root)
                     if is_image(os.path.join(root, filename))]

        for filename in filenames:
            print('Modifying image: ', filename)
            img = cv2.imread(os.path.join(root, filename), 3)

            # Scale logo proportionally to the image
            logo = cv2.imread(logoFilename, 3)
            logo = scale_logo(logo, img)
            x, y = get_logo_center_coordinates(img, logo)

            overlay_image_alpha(img,
                                logo[:, :, 0:3],
                                (x, y),
                                logo[:, :, 2] / 255.0)

            cv2.imwrite(filename, img)


if __name__ == '__main__':
    main()
