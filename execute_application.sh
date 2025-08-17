#!/bin/bash
set -e

# Keep up to date
# git pull

# Move to correct directory
cd automated_photo_pipeline

# Activate virtual env and install dependencies
brew install yq
python3.12 -m venv .venv
source .venv/bin/activate
# python3.12 -m pip install --upgrade pip setuptools # Needed for installing pillow-heif
pip install -r ../requirements.txt

# Run test
python3.12 -m pytest

# Get parameters from build_config.yaml
YAML_FILE="../build_config.yaml"
YAML_ROOT=".commands.execute-app"

DEVICE=$(yq "$YAML_ROOT.device" $YAML_FILE)
PATH_TO_PHOTOS=$(yq "$YAML_ROOT.path-to-photos" $YAML_FILE)
DESTINATION=$(yq "$YAML_ROOT.destination-path" $YAML_FILE)
MIGRATION=$(yq "$YAML_ROOT.migration-name" $YAML_FILE)
END_ON=$(yq "$YAML_ROOT.end-on" $YAML_FILE)

# Execute python script to transfer photos
python3.12 src/main.py --device "$DEVICE" --path_to_photos "$PATH_TO_PHOTOS" --destination_path "$DESTINATION" --migration_name "$MIGRATION" --end_on "$END_ON"