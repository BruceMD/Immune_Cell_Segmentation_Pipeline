from config import PROJECT_DIRECTORY
from pathlib import Path
from paquo.projects import QuPathProject

from PIL import Image, ImageDraw
from shapely.affinity import translate

import os
from config import OPENSLIDE_DIRECTORY, SLIDE_PATH, QUPATH_ROTATED
if hasattr(os, 'add_dll_directory'):
    with os.add_dll_directory(OPENSLIDE_DIRECTORY):
        import openslide
else:
    import openslide


def orchestrate():
    """
    Facilitate workflow:
        1. Open QuPath project
        2. Iterate through images loaded in project
        3. Iterate through annotations in images - add 512X512 tiles as keys to dic
        4. Iterate through annotations again - add marked cells to value list if co-ords in tile
        5. Pass image name and dictionary to distribute_tiles
    """
    PROJECT = Path(PROJECT_DIRECTORY)

    # read the project and raise Exception if it's not there
    with QuPathProject(PROJECT, mode='r') as qp:
        # iterate over the images
        for image in qp.images:
            # annotations are accessible via the hierarchy
            annotations = image.hierarchy.annotations

            tile_anno_dict = {}
            for annotation in annotations:
                if annotation.roi.area > 600_000:
                    print("roi_full:", annotation.roi.bounds)
                elif annotation.roi.area > 200_000:
                    tile_anno_dict[annotation.roi] = []

            for annotation in annotations:
                if annotation.roi.area < 200_000:
                    for key in tile_anno_dict.keys():
                        if anno_in_tile(annotation.roi.centroid, key.bounds):
                            tile_anno_dict[key].append(annotation.roi)

            distribute_tiles(image.image_name, tile_anno_dict)

    print("done")


def anno_in_tile(centroid, bounds):
    """
    Return true if centroid of cell annotation is within the bounds of 512X512 tile
    :param centroid: Co-ords of centre of cell annotation
    :param bounds: Bounds of 512X512 tile
    :return: boolean
    """

    centroid_x, centroid_y = centroid.coords[0]

    if bounds[0] <= centroid_x <= bounds[0] + 512:
        if bounds[1] <= centroid_y <= bounds[1] + 512:
            return True
    return False


def distribute_tiles(image_name, tile_anno_dict):
    """
    Iterate through dictionary (tile and containing cell annotations)
    Pass tile and cell annotations to build_masks function and keeping track of the number
    Pass tile to build_tile to output the 512X512 input image

    :param image_name: str
    :param tile_anno_dict: dic containing tile (key) and cell annotations (value)
    """
    index = 0
    for tile, cells in tile_anno_dict.items():
        build_mask(image_name, index, tile, cells)
        build_tile(image_name, index, tile)
        index += 1


def build_mask(image_name, tile_no, tile, cell_list):
    """
    Build mask/segmentation image
        Shift all values to treat top left corner as (0, 0)
        Draw black 512X512 tile
        Iterate through cell annotations and draw and fill white polygons onto black tile
        Export tiff images to data_masks directory

    :param image_name: Name from file associated to annotations
    :param tile_no: Keeping track of numbers of tiles for labelling purposes
    :param tile: Tuple of bounds of tile
    :param cell_list: List of cell annotations
    """

    output_name = image_name.replace('.mrxs', '')

    top_x, top_y = tile.bounds[0], tile.bounds[1]
    # print(f'Top: {top_x}-{top_y}')

    image = Image.new('L', (512, 512), 0)
    draw = ImageDraw.Draw(image)

    for cell in cell_list:
        trans_cell = translate(cell, xoff=-top_x, yoff=-top_y)

        # Check if the geometry is a MultiPolygon
        if trans_cell.geom_type == 'MultiPolygon':
            for poly in trans_cell.geoms:
                # Extract the exterior coordinates of the translated polygon
                exterior_coords = list(poly.exterior.coords)
                # Convert exterior coordinates to integer tuples
                exterior_coords_int = [(int(x), int(y)) for x, y in exterior_coords]
                # Draw the polygon
                draw.polygon(exterior_coords_int, fill=1, outline=1)
        else:
            # Extract the exterior coordinates of the translated polygon
            exterior_coords = list(trans_cell.exterior.coords)
            # Convert exterior coordinates to integer tuples
            exterior_coords_int = [(int(x), int(y)) for x, y in exterior_coords]
            # Draw the polygon
            draw.polygon(exterior_coords_int, fill=1, outline=1)

    # image.save(f'data_masks/{output_name}_{tile_no}_({top_x},{top_y})_mask.tiff')
    image.save(f'data_masks/{output_name}_{tile_no}.tiff')


def build_tile(image_name, index, tile):
    """
    Build a tile
    :param image_name:
    :param index:
    :param tile:
    :return:
    """
    slide_path = f'{SLIDE_PATH}/{image_name}'
    output_name = image_name.replace('.mrxs', '')
    level = 0  # Level for extraction (0 for highest resolution)

    # --- Load Slide ---
    slide = openslide.OpenSlide(slide_path)

    x, y = int(tile.bounds[0]), int(tile.bounds[1])
    x_new, y_new = rotate_coords(x, y, slide.dimensions, QUPATH_ROTATED)

    tile = slide.read_region((x_new, y_new), level, (512, 512))
    if QUPATH_ROTATED:
        tile = tile.rotate(180)
    # tile.convert('RGB').save(f"data/{output_name}_{index}_({x},{y})_tile.tiff", format='TIFF')
    tile.convert('RGB').save(f"data/{output_name}_{index}.tiff", format='TIFF')


def rotate_coords(x, y, dimensions, rotate=True):
    """
    Trial and error to rotate the image as I imported images into QuPath with a 180 rotation, and now undoing it...

    :param rotate:
    :param x:
    :param y:
    :param dimensions:
    :return:
    """
    if rotate:
        new_x = dimensions[0] - x - 513
        new_y = dimensions[1] - y - 513
        return new_x, new_y
    return x, y
