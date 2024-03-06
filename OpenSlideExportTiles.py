import os
from config import OPENSLIDE_DIRECTORY, SLIDE_PATH
if hasattr(os, 'add_dll_directory'):
    with os.add_dll_directory(OPENSLIDE_DIRECTORY):
        import openslide
else:
    import openslide


def export_tiles(image_name, rect_tuple):
    slide_path = f'{SLIDE_PATH}/{image_name}'
    # A list of tuples, each defining a region: (start_x, start_y, width, height)
    output_dir = 'data/'
    level = 0  # Level for extraction (0 for highest resolution)

    # --- Load Slide ---
    slide = openslide.OpenSlide(slide_path)
    print(slide.dimensions)

    # --- Extract and Save Subsets---
    for i, (x, y, w, h) in enumerate(rect_tuple):
        print(f'x: {x} and y: {y}')     # todo, double check on these values
        tile = slide.read_region((x, y), level, (w, h))
        tile.convert('RGB').save(os.path.join(output_dir, f"{image_name}_tile_{i}_{x}_{y}.tiff"), format='TIFF')

    # --- (Optional)  Explore Properties ---
    print(slide.properties)  # View image metadata
    print(slide.level_dimensions)  # Dimensions at each level
