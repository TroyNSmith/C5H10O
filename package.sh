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

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Check if source directory exists
if [ -d "$SOURCE_DIR" ]; then
    # Zip the source and move it to the destination
    zip -r "$ZIP_FILE" "$SOURCE_DIR"
    echo "Successfully zipped $SOURCE_DIR to $ZIP_FILE"
else
    echo "Error: Directory $SOURCE_DIR does not exist."
    exit 1
fi