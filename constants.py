############################################################################################
# Project Name: Motor Skill Acquisition Error Management System
# 
# Authors: Milton Tinoco, Ethan Weldon, Joshua Samson, Michael Cabrera
# San Francisco State University
#
# File Description:
# This file contains the code for constant values used across the program.
############################################################################################

from PyQt5.QtCore import Qt
from enum import Enum

PROGRAM_NAME = "Motor Skill Acquisition Error Management System"

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