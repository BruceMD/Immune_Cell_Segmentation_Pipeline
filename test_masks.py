import os
import cv2
import numpy as np
from PIL import Image

def compare_images(data_dir, masks_dir, output_dir):
    # Get the list of image files in the data and data_masks directories
    data_files = [f for f in os.listdir(data_dir) if f != '.gitkeep']
    masks_files = [f for f in os.listdir(masks_dir) if f != '.gitkeep']

    # Iterate over the list of image files
    for data_file, masks_file in zip(data_files, masks_files):
        # Read the original image and the mask image
        data_image = cv2.imread(os.path.join(data_dir, data_file))
        masks_image = cv2.imread(os.path.join(masks_dir, masks_file), cv2.IMREAD_GRAYSCALE)

        # Convert the mask image to RGB
        masks_image = cv2.cvtColor(masks_image, cv2.COLOR_GRAY2RGB)

        # Concatenate the original image and the mask image horizontally
        concatenated_image = np.hstack((data_image, masks_image))

        # Save the concatenated image to the output directory
        cv2.imwrite(os.path.join(output_dir, data_file), concatenated_image)


compare_images('data/data', 'data/data_masks', 'data/test')
