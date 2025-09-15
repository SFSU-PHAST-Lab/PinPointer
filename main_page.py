############################################################################################
# Project Name: Motor Skill Acquisition Error Management System 
# 
# Filename: main_page.py
# 
# Authors: Milton Tinoco, Joshua Samson, Michael Cabrera
# San Francisco State University
#
# Project Description:
# This project is an image editing tool designed to calculate real-life measurements
# between points in images. Users select a folder of images, including a calibration image,
# to determine a scaling factor. The tool applies this factor to calculate real-world 
# distances between points in images, displaying the results and saving them in a text file.
#
# File Description:
# This file contains the code for the main window of the application and initializes 
# the main menu, linking it to the calibration, data review, and image editing pages.
#
# Copyright 2025 SFSU PHAST Lab
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
############################################################################################

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QStackedWidget
)
from PyQt5.QtCore import Qt

from calibration_page import CalibrationPage
from data_review_page import DataReviewPage
from image_editing_page import EditPage

from constants import (PROGRAM_NAME, WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT, 
                    FONT_SIZE, STYLE_SHEET, LAYOUT_MARGINS)

class MainWindow(QMainWindow):
    """ Initializes the main application window and sets up the navigation between 
        the main menu, calibration page, data review page, and image editing page.
    """

    def __init__(self):
        """ Initializes the main window and sets the window title and size. """
        super().__init__()
        self.setWindowTitle(PROGRAM_NAME)  # Set application window title
        self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)     # Set initial window size
        self.initUI()   # Initialize the UI components
    
    def initUI(self):
        """ Initializes the main window with a stacked layout for navigation. """
        self.stack = QStackedWidget() # Create a stacked widget for page navigation
        self.setCentralWidget(self.stack)  # Display the top widget on the stack

        # Add pages to the stack
        self.main_menu = MainMenu(self) # Main menu page
        self.calibration_page = CalibrationPage(self) # Calibration page
        self.edit_page = EditPage(self) # Image editing page
        self.data_review_page = DataReviewPage(self)    # Data review page

        self.stack.addWidget(self.main_menu)          # Main menu page
        self.stack.addWidget(self.calibration_page)   # Calibration page
        self.stack.addWidget(self.edit_page)          # Image editing page
        self.stack.addWidget(self.data_review_page)   # Data review page

        # Connect main menu buttons to switch pages
        self.main_menu.calibration_button.clicked.connect(self.nav_to_calibration_page)
        self.main_menu.data_button.clicked.connect(self.nav_to_data_page)
        self.main_menu.exit_button.clicked.connect(self.close)

    def nav_to_main_menu(self):
        """ Navigate to the main menu. """
        self.stack.setCurrentWidget(self.main_menu) 

    def nav_to_calibration_page(self):
        """ Navigate to the calibration page. """
        self.stack.setCurrentWidget(self.calibration_page)

    def nav_to_edit_page(self):
        """ Navigate to the image editing page. """
        self.stack.setCurrentWidget(self.edit_page)

    def nav_to_data_page(self):
        """ Navigate to the data review page. """
        self.stack.setCurrentWidget(self.data_review_page)

class MainMenu(QWidget):
    """ Represents the main menu page with buttons to start image processing, 
        review data, or exit the program. """
    
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        layout = QVBoxLayout()  # Set vertical layout for buttons

        # Welcome text
        welcome_label = QLabel(f'{PROGRAM_NAME}\n')
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet(STYLE_SHEET)
        layout.addWidget(welcome_label)

        # Button to start image processing (navigate to calibration page)
        self.calibration_button = QPushButton("Start Image Processing")

        # Button to review data (navigate to data review page)
        self.data_button = QPushButton("Review Data")

        # Button to exit the application
        self.exit_button = QPushButton("Exit Program")

        # Style all buttons and add to layout
        buttons = [self.calibration_button, self.data_button, self.exit_button]
        [button.setStyleSheet(f'font-size: {FONT_SIZE}') for button in buttons]
        [layout.addWidget(button) for button in buttons]

        # Set layout margins (right, left, left, bottom)
        layout.setContentsMargins(LAYOUT_MARGINS, LAYOUT_MARGINS, LAYOUT_MARGINS, LAYOUT_MARGINS)

        # Apply layout to the main menu
        self.setLayout(layout)

# Main function to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)   # Initialize the application
    window = MainWindow()          # Create the main window
    window.show()                  # Display the main window
    sys.exit(app.exec_())          # Start the application event loop
