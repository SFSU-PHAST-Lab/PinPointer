############################################################################################
# Project Name: PinPointer
# 
# Authors: Milton Tinoco, Ethan Weldon, Joshua Samson, Michael Cabrera
# San Francisco State University
#
# File Description:
# This file contains the code for constant values used across the program.
#
# Copyright 2025 SFSU PHAST Lab
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#        http://www.apache.org/licenses/LICENSE-2.0
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
############################################################################################

from PyQt5.QtCore import Qt
from enum import Enum

PROGRAM_NAME = "PinPointer"

# File and folder names
AXIS_ORIENTATION_DIR = "axisOrientationGraphics"
RESULTS_FILENAME = "Results_File.txt"
RESULTS_DIR = "Results"

# Valid image types
IMAGE_TYPES = ['png', 'jpg', 'jpeg', 'bmp']

# Window Configurations
WINDOW_X = 100
WINDOW_Y = 100
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

# Font Configurations
FONT_SIZE = "20px"
FONT_WEIGHT = "bold"
BUTTON_FONT_SIZE = "16px" 
BUTTON_PADDING = "10px"
LAYOUT_MARGINS = 100
STYLE_SHEET = f"font-size: {FONT_SIZE}; font-weight: {FONT_WEIGHT}; margin-bottom: {FONT_SIZE};"

# Image Interface Configurations
CIRCLE_RADIUS = 6
CROSS_WIDTH = 10
PEN_COLOR = Qt.red
TARGET_COLOR = Qt.green
PEN_WIDTH = 2
ZOOM_SCALE = 1.1

# Table Headers
class HEADERS(Enum):
    IMAGE_ID = "ID"
    IMAGE_NAME = "Image Name"
    RADIAL = "Radial"
    X_AXIS = "X-Axis"
    Y_AXIS = "Y-Axis"

# Default Values
OUT_OF_BOUNDS = 99999
NO_IMAGE = "N/A"
