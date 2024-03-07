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

## Setup

1. Run a git clone on the Immune Cell Segmentation Pipeline repo
   * ```git clone https://github.com/BruceMD/Immune_Cell_Segmentation_Pipeline.git```

2. Run `pip install -r requirements.txt` to download all the necessary libraries for this project.

3. Download the [OpenSlide](https://github.com/openslide/openslide-bin/releases/download/v20231011/openslide-win64-20231011.zip) zip folder, and extract it 
(I have extracted it to the project directory for simplification).
    * In the `config.py` folder, copy the `openslide-wind64-20231011/bin` directory to the `OPENSLIDE_DIRECTORY` variable.

4. From the terminal, run `paquo get_qupath --install-path ./qupath 0.4.3`
and update the config/.paquo.toml variable `qupath_dir` to the `$HOME/qupath/QuPath-0.4.3`.
   * Ensure [QuPath](https://qupath.github.io/) has been installed on your computer

5. Update the `config.py` variables:
    * PROJECT_DIRECTORY
      * Directory where the QuPath project is saved
    * OPENSLIDE_DIRECTORY
      * Directory where openslide has been extracted (step 3) 
    * SLIDE_PATH
      * Directory where mrxs images are stored
    * QUPATH_ROTATED
      * `True` if images were imported to QuPath with rotation (thus resetting the coordinates)
      * Other wise `False`
