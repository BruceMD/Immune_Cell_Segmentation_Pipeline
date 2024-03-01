from pathlib import Path
from paquo.projects import QuPathProject
from OpenSlideExportTiles import export_tiles


def export_tiles():
    EXAMPLE_PROJECT = Path("C:/Users/maxbr/Documents/University/BIOL61230 - Research Project "
                           "1/QuPathImages/project.qpproj")

    rect, neut = 0, 0

    # read the project and raise Exception if it's not there
    with QuPathProject(EXAMPLE_PROJECT, mode='r') as qp:
        # iterate over the images
        for image in qp.images:
            # annotations are accessible via the hierarchy
            annotations = image.hierarchy.annotations

            rect_list = []
            for annotation in annotations:
                # annotations are paquo.pathobjects.QuPathPathAnnotationObject instances
                # their ROIs are accessible as shapely geometries via the .roi property
                if annotation.roi.area > 600_000:
                    print("roi_full:", annotation.roi.bounds)
                elif annotation.roi.area > 200_000:
                    rect += 1
                    print("roi:", annotation.roi.bounds)
                    rect_list.append(top_left_rect(annotation.roi.bounds))
                else:
                    print("roi centre:", annotation.roi.centroid)
            export_tiles(image.image_name, rect_list)
    print("done")


def top_left_rect(boundary):
    return int(boundary[0]), int(boundary[1]), 512, 512
