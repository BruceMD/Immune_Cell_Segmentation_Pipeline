# Immune Cell Segmentation Pipeline

## Description


## Workflow
1. Identify target objects in histology slide images by hand annotating using QuPath and select 512X512 tiles for training
2. Using Python scripts and the PAQuo and OpenSlide modules, output three types of 512X512 tiles:
   1. Raw tile image
   2. Mask image (segmentation interpretation)
   3. Annotated raw image 
3. Split data into training, validation, and testing (70-15-15)


## Dependencies
* Python 3.11
* QuPath (0.4.3)
* PAQuo (0.7.1)
* OpenSlide (4.0.0)
* OpenSlide-python (1.3.1)
* Shapely (2.0.3)
* Pillow (10.2.0)
