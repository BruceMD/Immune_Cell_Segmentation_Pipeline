#!/bin/bash

EXTRACT_DIR="Immune_Cell_Segementation_Pipeline"

# Download and extract OpenSlide, remove zip file
QUPATH_URL="https://github.com/qupath/qupath/releases/download/v0.5.1/QuPath-v0.5.1-Windows.zip"
wget "$QUPATH_URL" -P "$EXTRACT_DIR"
unzip "$EXTRACT_DIR/QuPath-v0.5.1-Windows.zip" -d "$EXTRACT_DIR"
rm "$EXTRACT_DIR/QuPath-v0.5.1-Windows.zip"

OPENSLIDE_URL="https://github.com/openslide/openslide-bin/releases/download/v20231011/openslide-win64-20231011.zip"
wget "$OPENSLIDE_URL" -P "$EXTRACT_DIR"
unzip "$EXTRACT_DIR/openslide-win64-20231011.zip" -d "$EXTRACT_DIR"
rm "$EXTRACT_DIR/openslide-win64-20231011.zip"

pip install -r requirements.txt
