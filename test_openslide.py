from config import PROJECT_DIRECTORY
from pathlib import Path
from paquo.projects import QuPathProject

import os
from config import OPENSLIDE_DIRECTORY, SLIDE_PATH
if hasattr(os, 'add_dll_directory'):
    with os.add_dll_directory(OPENSLIDE_DIRECTORY):
        import openslide
else:
    import openslide

from OpenSlideExportTiles import black_tile


def orchestrate():
    """
    Facilitate workflow:
        1. Open QuPath project
        2. Iterate through images loaded in project
        3. Iterate through annotations in images - add 512X512 tiles as keys to dic
        4. Iterate through annotations again - add marked cells to value list if co-ords in tile
        5. Pass image name and dictionary to distribute_tiles
    """

    slide = openslide.OpenSlide(f'D:/Bruce_Data/02_human_bd/01_mrxs/R5-S14-2021-11-18T22-47-44.mrxs')

    print(slide.dimensions)

    for i in range(220):
        for j in range(220):

            tile = slide.read_region((4000*i, 3000*j), 0, (4000, 3000))

            if black_tile(tile):
                continue

            tile.convert('RGB').save(format='TIFF', fp=f'fuck/temp_image_{i}_{j}.tiff')


orchestrate()
