#!/bin/bash

# Check if label is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <label>"
    exit 1
fi

LABEL=$1
SOURCE_DIR="computations/$LABEL"
DEST_DIR="final"
ZIP_FILE="$DEST_DIR/$LABEL.zip"

# Define the specific files we want
HESS_FILE="$SOURCE_DIR/freq.hess"
XYZ_FILE="$SOURCE_DIR/freq.xyz"

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Check if source directory exists
if [ -d "$SOURCE_DIR" ]; then
    # Check if at least one of the target files exists
    if [ -f "$HESS_FILE" ] || [ -f "$XYZ_FILE" ]; then
        # Zip only the specific files
        # Using -j (junk paths) if you want just the files in the zip 
        # root, otherwise remove -j to keep the folder structure.
        zip -j "$ZIP_FILE" "$HESS_FILE" "$XYZ_FILE"
        echo "Successfully zipped .xyz and .hess from $SOURCE_DIR to $ZIP_FILE"
    else
        echo "Error: Neither freq.hess nor freq.xyz found in $SOURCE_DIR"
        exit 1
    fi
else
    echo "Error: Directory $SOURCE_DIR does not exist."
    exit 1
fi