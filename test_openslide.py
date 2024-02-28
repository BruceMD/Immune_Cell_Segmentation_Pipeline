import os
OPENSLIDE_PATH = r'C:/Users/maxbr/PycharmProjects/HistologyRP/openslide-win64-20231011/bin'
if hasattr(os, 'add_dll_directory'):
    # Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
else:
    import openslide


def test():

    level = 0
    slide = openslide.OpenSlide('C:/Users/maxbr/Documents/University/BIOL61230'
                                ' - Research Project 1/Example data/R3-S21-2021-11-18T20-41-45.mrxs')
    output = 'test_data'

    width, height = slide.dimensions
    print(f'Width: {width}')
    print(f'Height: {height}')

    count = 0
    for y in range(0, height, 2048):
        for x in range(0, width, 2048):
            count += 1
            # tile = slide.read_region((x, y), 0, (2048, 2048))
            # if black_tile(tile) or white_tile(tile):
            #     pass
            # else:
            #     tile.convert('RGB').save(f'test_data/test_tile_{count}_{x}_{y}.png')
    print(count)


def white_tile(image, threshold=230):
    avg_color = image.resize((1, 1)).getpixel((0, 0))  # Get average by resizing
    return all(channel >= threshold for channel in avg_color)


def black_tile(image, threshold=25):
    avg_color = image.resize((1, 1)).getpixel((0, 0))  # Get average by resizing
    return all(channel <= threshold for channel in avg_color)
