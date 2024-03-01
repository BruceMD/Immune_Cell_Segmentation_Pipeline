from pathlib import Path
from paquo.projects import QuPathProject
from OpenSlideExportTiles import export_tiles

import rasterio
from rasterio.plot import show
from shapely.geometry import Polygon, mapping
import numpy as np
from PIL import Image, ImageDraw
from shapely.affinity import translate



def orchestrate():
    EXAMPLE_PROJECT = Path("C:/Users/maxbr/Documents/University/BIOL61230 - Research Project "
                           "1/QuPathImages/project.qpproj")

    # read the project and raise Exception if it's not there
    with QuPathProject(EXAMPLE_PROJECT, mode='r') as qp:
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

            # print(f'Name: {image.image_name}')
            # for k, cells in tile_anno_dict.items():
            #     print(f'Tile: {k}')
            #     for c in cells:
            #         print(f'\tCell: {c}')

    print("done")


def anno_in_tile(centroid, bounds):

    centroid_x, centroid_y = centroid.coords[0]

    if bounds[0] <= centroid_x <= bounds[0] + 512:
        if bounds[1] <= centroid_y <= bounds[1] + 512:
            return True
    return False


def distribute_tiles(image_name, tile_anno_dict):
    index = 0
    for tile, cells in tile_anno_dict.items():
        build_mask(image_name, index, tile, cells)
        index += 1


def build_mask(image_name, tile_no, tile, cell_list):

    output_name = image_name.replace('.mrxs', '')

    top_x, top_y = tile.bounds[0], tile.bounds[1]
    print(f'Top: {top_x}-{top_y}')

    image = Image.new('RGB', (512, 512), 'black')
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
                draw.polygon(exterior_coords_int, fill='white', outline='white')
        else:
            # Extract the exterior coordinates of the translated polygon
            exterior_coords = list(trans_cell.exterior.coords)
            # Convert exterior coordinates to integer tuples
            exterior_coords_int = [(int(x), int(y)) for x, y in exterior_coords]
            # Draw the polygon
            draw.polygon(exterior_coords_int, fill='white', outline='white')

    image.save(f'data_masks/{output_name}_T{tile_no}.tiff')
