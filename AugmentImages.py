import albumentations as A
import cv2
from pathlib import Path
import numpy as np


def orchestrate():
    augment_images()


def augment_images():
    input_data_path = Path('data/')
    mask_data_path = Path('data_masks/')

    input_images = list(input_data_path.glob('*.tiff'))
    mask_images = list(mask_data_path.glob('*.tiff'))

    transform = A.Compose([
        A.OneOf([A.HorizontalFlip(p=0.25),
                 A.VerticalFlip(p=0.25),
                 A.Rotate(limit=90, p=0.17),
                 A.Rotate(limit=180, p=0.17),
                 A.Rotate(limit=270, p=0.16),
                 # A.RandomBrightnessContrast(p=0.2),
                 ])

    ], p=1.0)

    for image, mask in zip(input_images, mask_images):
        input_image = cv2.imread(str(image))
        mask_image = cv2.imread(str(mask), cv2.IMREAD_GRAYSCALE)
        augmented = transform(image=input_image, mask=mask_image, always_apply=False)
        aug_image = augmented['image']
        aug_mask = augmented['mask']

        # Check if a transformation was applied
        if not np.array_equal(input_image, aug_image) or not np.array_equal(mask_image, aug_mask):
            cv2.imwrite(f'data_trans/{image.stem}_trans.tiff', aug_image)
            cv2.imwrite(f'data_masks_trans/{mask.stem}_trans.tiff', aug_mask)

if __name__ == '__main__':
    orchestrate()
