############################################################################################
# Project Name: PinPointer
# 
# Filename: file_manager_class.py
# 
# Authors: Milton Tinoco, Ethan Weldon, Joshua Samson, Michael Cabrera
# San Francisco State University
#
# File Description:
# This file contains the code for file management, which creates folders and text files,
# appends data to files, and removes the last line from a file.
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

import os
from constants import RESULTS_DIR, RESULTS_FILENAME, HEADERS, NO_IMAGE

# Class: FileManager
# Description: This class provides methods to create folders, text files, 
#              append data to files, and remove the last line from a file.

class FileManager:
    """ 
    This class provides methods to create folders, text files, 
    append data to files, and remove the last line from a file.
    """
    def __init__(self):
        self.results_folder = None  # Directory to save the results
        self.results_file = None    # File name to save the results

    def set_results_folders(self, folder_path):
        """ Create and store the absolute paths to the results folder and file.
        Args:
            folder_path (string): The absolute path of the image set """
        self.results_folder = os.path.join(folder_path, RESULTS_DIR)
        self.results_file = os.path.join(self.results_folder, RESULTS_FILENAME)

    def write_results(self, images):
        """ Write the calculated values to the results file.
        Args:
            images ([Image]): The list of images to save """
        # Create the results folder if it does not already exist
        if not os.path.exists(self.results_folder):
            os.makedirs(self.results_folder, exist_ok=True)

        # If the results file does not already exist, create a new file and write the headers
        if not os.path.exists(self.results_file):
            with open(self.results_file, "w") as file:
                # Header with column names
                formatted_header = ''.join([f"{h.value:<{15}}" for h in HEADERS])
                file.write(f"={formatted_header}\n")
                file.write("===\n") # Separator line

        # Write the values to the file for each image
        with open(self.results_file, "a") as file:
            for image in images:
                file.write(f"{HEADERS.IMAGE_ID.value} {image.index:<10} {HEADERS.IMAGE_NAME.value} {image.name:<10} {HEADERS.RADIAL.value} {image.radial} \t\t {HEADERS.X_AXIS.value} {image.xaxis}\t {HEADERS.Y_AXIS.value} {image.yaxis}\n")
        
           
