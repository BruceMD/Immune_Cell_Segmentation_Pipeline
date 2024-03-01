from HandleTIFF import orchestrate
from test_openslide import test
from BuildMasks import orchestrate


def main():
    orchestrate()
    # test()


if __name__ == '__main__':
    main()
