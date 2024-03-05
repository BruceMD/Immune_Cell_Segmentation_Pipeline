import os
OPENSLIDE_PATH = r'C:/Users/maxbr/PycharmProjects/HistologyRP/openslide-win64-20231011/bin'
if hasattr(os, 'add_dll_directory'):
    # Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
else:
    import openslide


def export_tiles(image_name, rect_tuple):
    slide_path = f'C:/Users/maxbr/Documents/University/BIOL61230 - Research Project 1/Example data/{image_name}'
    # A list of tuples, each defining a region: (start_x, start_y, width, height)
    output_dir = 'C:/Users/maxbr/PycharmProjects/HistologyRP/data'
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
