############################################################################################
# Project Name: Motor Skill Acquisition Error Management System
# 
# Authors: Milton Tinoco, Ethan Weldon, Joshua Samson, Michael Cabrera
# San Francisco State University
#
# File Description:
# This file contains the code for the calibration page of the application. 
# The calibration page allows users to select a folder of images, choose a calibration image, 
# horizontal and vertical axis, and set the distance between two points in the image to 
# calculate a scaling factor for real-world measurements. It also reslect the points and 
# axis if the user made a mistake. Then proceed to the image editing page to apply the 
# scaling factor to other images.
############################################################################################

import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QWidget, QMessageBox, QLineEdit, QFileDialog)

import calculations as calc
from image_interface import ImageView

from constants import AXIS_ORIENTATION_DIR, FONT_SIZE, STYLE_SHEET, IMAGE_TYPES

class CalibrationPage(QWidget):
    """ 
    This class represents the calibration page of the application. It allows 
    users to select a folder of images, choose a calibration image, and set 
    the distance between two points in the image to calculate a scaling factor 
    for real-world measurements. The user can then proceed to the image editing 
    page to apply the scaling factor to other images.
    """

    def __init__(self, parent=None):
        super().__init__(parent) # Pass parent to the base class constructor
        self.parent = parent # Set the parent widget
        self.initUI() # Initialize the UI elements of the page

        #####################################################
        # Variables for Selection Tracking
        #####################################################

        self.cal_image_path = None  # Store calibration image path
        self.point1 = None  # The first point for calibration
        self.point2 = None  # The second point for calibration
        
    def initUI(self):
        """ Initializes the UI elements for the page. """
        # Set vertical layout
        self.layout = QVBoxLayout(self)
        self.button_layout = QHBoxLayout()

        # Load image information
        self.axis_image_folder = os.path.join(os.path.dirname(__file__), AXIS_ORIENTATION_DIR)
        self.axis_image_files = sorted(os.listdir(self.axis_image_folder))
        self.axis_orientation = 0  # Start at the first image

        # Direction label
        self.direction_label = QLabel(
            "Please select a folder with image set, then select a calibration image.") 
        self.direction_label.setAlignment(Qt.AlignCenter)
        self.direction_label.setStyleSheet(STYLE_SHEET)
        self.layout.addWidget(self.direction_label)

        # Back to main menu button
        self.main_menu_button = QPushButton("Return to Main Menu")
        self.main_menu_button.clicked.connect(self.parent.nav_to_main_menu)
        self.button_layout.addWidget(self.main_menu_button)

        # Folder selection button
        self.select_folder_button = QPushButton("Select Folder")
        self.select_folder_button.clicked.connect(self.select_folder)
        self.button_layout.addWidget(self.select_folder_button)

        # Image selection button
        self.select_image_button = QPushButton("Reselect Image")
        self.select_image_button.setEnabled(False)
        self.select_image_button.clicked.connect(self.select_cal_image)
        self.button_layout.addWidget(self.select_image_button)
        self.select_image_button.hide()

        # Reselect points button
        self.reselect_points_button = QPushButton("Reselect Points")
        self.reselect_points_button.setEnabled(False)
        self.reselect_points_button.clicked.connect(self.reselect_points)
        self.button_layout.addWidget(self.reselect_points_button)
        self.reselect_points_button.hide()

        self.layout.addLayout(self.button_layout)

        #####################################################
        # Graph Display Section with Buttons NEXT to Image
        #####################################################

        # Create a horizontal layout for the graph and buttons
        graph_layout = QHBoxLayout()

        # Left (counter clockwise) button (previous graph)
        self.left_button = QPushButton("⬅ Spin Orientation \n" "Counter-clockwise")
        self.left_button.clicked.connect(self.previous_image)

        # QLabel for displaying the graph
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(150, 100)  # Set fixed size for consistency
        self.load_axis_image()  # Load the initial axis image

        # Right (clockwise) button (next graph)
        self.right_button = QPushButton("Spin Orientation ➡\n" "Clockwise")
        self.right_button.clicked.connect(self.next_image)

        # Add elements to the horizontal layout (Buttons on sides, Image in center)
        graph_layout.addWidget(self.left_button)  # Add left button
        graph_layout.addWidget(self.image_label)  # Add image in center
        graph_layout.addWidget(self.right_button)  # Add right button
    
        # Add the graph layout to the main layout
        self.layout.addLayout(graph_layout)
        
        # Hide 
        self.hide_graph_and_buttons()

        #####################################################
        # Distance Input Section
        #####################################################

        # Create a horizontal layout for the distance input and submit button
        distance_layout = QHBoxLayout()

        # Distance input field
        self.distance_input = QLineEdit()
        self.distance_input.setPlaceholderText(
            "Enter real-world distance between points (e.g., 10)")
        self.distance_input.setStyleSheet(f"font-size: {FONT_SIZE}")
        # self.distance_input.setEnabled(False)  # Enable after selecting two points
        self.distance_input.installEventFilter(self)  # Enable Enter key press event
        # self.layout.addWidget(self.distance_input)
        self.distance_input.returnPressed.connect(self.load_edit_page)
        # self.distance_input.hide()  # Initially hidden

        # Start button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.load_edit_page)
        self.start_button.hide()

        # Add the elements to the layout
        distance_layout.addWidget(self.distance_input)
        distance_layout.addWidget(self.start_button)

        self.layout.addLayout(distance_layout)

        self.hide_distance_calibration()
        
        #####################################################
        # Image Viewer for Point Selection
        #####################################################

        # Image viewer for calibration selection
        self.image_viewer = ImageView()
        self.layout.addWidget(self.image_viewer)

        # Assign the layout to the widget
        self.setLayout(self.layout)

        # Connect ImageView click signal
        self.image_viewer.point_clicked.connect(self.handle_point_clicked)

    def hide_graph_and_buttons(self):
        """ Hides the graph image and navigation buttons. """
        self.image_label.hide()
        self.left_button.hide()
        self.right_button.hide()
        
    def show_graph_and_buttons(self):
        """ Shows the graph image and navigation buttons. """
        self.image_label.show()
        self.left_button.show()
        self.right_button.show()

    def hide_distance_calibration(self):
        """ Hides the distance text box and start button. """
        self.distance_input.setVisible(False) # Show the distance input field
        self.distance_input.setEnabled(False) # Enable the distance input field  
        self.distance_input.hide()
        self.start_button.hide()

    def show_distance_calibration(self):
        self.distance_input.setVisible(True) # Show the distance input field
        self.distance_input.setEnabled(True) # Enable the distance input field  
        self.distance_input.show()
        self.start_button.show()

    def load_axis_image(self):
        """ Loads the current axis image based on the current index. """
        image_path = os.path.join(self.axis_image_folder, 
                                  self.axis_image_files[self.axis_orientation])

        # Raise an error if the file does not exist
        if not os.path.exists(image_path):
            self.error_loading_image(image_path)
            return

        pixmap = QPixmap(image_path)
        # Raise an error if there was a problem loading the image
        if pixmap.isNull():
            self.error_loading_image(image_path)
        # Otherwise, display image
        else:
            self.image_label.setPixmap(pixmap) 

    def error_loading_image(self, image_path):
        """ Notifies the user that there was an error loading the specified image. 
        Args:
           image_path (string): Path to the image that was unable to load 
        """
        print(f"❌ Error: Image not found at {image_path}")
        self.image_label.setText(
            f"Error loading image: {self.axis_image_files[self.axis_orientation]}")

    def next_image(self):
        """ Increment and load the next axis orientation image. """
        self.axis_orientation = (self.axis_orientation + 1) % len(self.axis_image_files)
        self.load_axis_image()
    
    def previous_image(self):
        """ Decrement and load the previous axis orientation image. """
        self.axis_orientation = (self.axis_orientation - 1) % len(self.axis_image_files)
        self.load_axis_image()

    def load_edit_page(self):
        """ This method handler after the user presses the Enter key in the distance 
            input field. It validates the entered distance, calculates the scaling factor 
            based on the selected distance between points, update the direction label 
            with the distance entered, pixel distance, and scaling factor.
        """
        # Get and validate the entered distance
        try:
            distance = float(self.distance_input.text())
        except:
            QMessageBox.warning(self, "Invalid Input", "Could not interpret distance as a number.")
            return

        if distance <= 0:
            QMessageBox.warning(self, "Invalid Input", "Distance must be a positive number.")
            return
        else:
            # Calculate the scaling factor
            scaling_factor = calc.calculate_scaling_factor(
                distance, self.point1, self.point2)
            # Transition to the next page after a delay
            QTimer.singleShot(500, lambda: self.advance_to_edit_page(scaling_factor))

    def advance_to_edit_page(self, scaling_factor):
        """ Sends relevant information to the edit page then switches pages.
        Args: 
            scaling_factor (float): The ratio between the real-world and pixel distances.
        """
        # Transition to the next page (image editing page)
        self.parent.edit_page.set_data(scaling_factor, self.folder_path, 
                                       self.cal_image_path, self.axis_orientation)
        self.parent.nav_to_edit_page()

    def reselect_points(self):
        """ Resets the selected values to reselect two points in the image to set 
            the calibration distance.
        """
        self.hide_graph_and_buttons()
        self.point1, self.point2 = None, None   # Reset the selected points
        self.reselect_points_button.setEnabled(False) # Disable the button
        self.direction_label.setText("Please select new two points to set the distance")
        self.image_viewer.load_image(self.cal_image_path) # Reload the image
        
    def handle_point_clicked(self, x, y):
        """ Handles the clicked points on the image viewer. It checks if the clicked 
            point is too close to an already clicked point and displays a warning message.
            If two points are selected, it enables the next steps and prompts the user 
            to select the vertical axis.
        Args: 
            x (float): The x coordinate of the selected point
            y (float): The y coordinate of the selected point
        """
        # Save the first point if it has not been selected yet
        if not self.point1:
            self.point1 = (x, y)

        # Save the second point if it has not been selected yet
        elif not self.point2:
            # Ensure the second point is sufficiently far away from the first
            if abs(self.point1[0] - x) < 1 and abs(self.point1[1] - y) < 1:
                QMessageBox.warning(self, "Invalid Selection", 
                                    "You cannot select the same spot or too close to it.")
                self.reselect_points() # Reselect the points
            
            else:
                self.point2 = (x, y)
                # Show and enable the reselect points button
                self.reselect_points_button.setVisible(True) 
                self.reselect_points_button.setEnabled(True) 
                # Prompt the user to select the axes orientation
                self.direction_label.setText("Please select the orientation of the axes,\n" "and actual distance between the two selected points.\n" "Press 'Enter' to continue.")
                # Show the graph images
                self.show_graph_and_buttons()
                self.show_distance_calibration()
                # self.distance_input.setVisible(True) # Show the distance input field
                # self.distance_input.setEnabled(True) # Enable the distance input field  

    def select_folder(self):
        """ Opens a dialog to select a folder containing images.
            It updates the folder path label and enables the select image button.
        """
        # Open a dialog to select a folder
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_path = folder_path # Store the selected folder path
            self.select_image_button.setEnabled(True) # Enable the select image button
            self.select_image_button.setVisible(True) # Show the select image button
            self.select_cal_image() # Select the calibration image

    
    def select_cal_image(self):
        """ This method opens a dialog to select a calibration image from the selected 
            folder. It loads the selected image in the image viewer and prompts the 
            user to select two points to set the distance.
        """
        self.point1, self.point2 = None, None

        if not self.folder_path:
            return
        # Open a dialog to select an image from the selected folder
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        image_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            self.folder_path,
            f"Images (*.{' *.'.join(IMAGE_TYPES)})",
            options=options
        )
        # If an image is selected, load it in the image viewer
        if image_path:
            # Store the selected image path
            self.cal_image_path = image_path 
            # Load the selected image in the image viewer
            self.image_viewer.load_image(image_path) 
            # Prompt the user to select two points
            self.direction_label.setText("Please select two points to set the distance") 
            # Change the text of the select folder button
            self.select_folder_button.setText("Reselect Folder")

