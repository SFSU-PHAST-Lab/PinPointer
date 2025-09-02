############################################################################################
# Project Name: Motor Skill Acquisition Error Management System
# 
# Filename: image_editing_page.py
# 
# Authors: Milton Tinoco, Ethan Weldon, Joshua Samson, Michael Cabrera
# San Francisco State University
#
# File Description:
# This file contains the code for the image editing page, where users can select points on images
# to calculate real-world measurements. The EditPage class allows users to select a target point
# and an implement point on the image to calculate the z-axis, y-axis, and x-axis values. The calculated
# values are displayed on the screen and saved to a text file. The page also provides navigation
# options to move between images and return to the main menu. At the end of the image list, users
# can choose to go to the data review page, return to the main menu, or exit the program.
############################################################################################

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QMessageBox, QApplication)
from PyQt5.QtCore import Qt, QTimer
import os

import calculations as calc
from file_manager_class import FileManager
from image_interface import ImageView
from calibration_page import CalibrationPage

from constants import BUTTON_FONT_SIZE, BUTTON_PADDING, STYLE_SHEET, OUT_OF_BOUNDS, NO_IMAGE, IMAGE_TYPES, HEADERS

class Image():
    """
    Stores relevant information for an image
    """
    def __init__(self, name, path, index):
        self.name = name    # Name of the image file
        self.path = path    # Full image path
        self.index = index  # Index of the image in the list
        self.radial = None  # Calculated radial error
        self.xaxis = None   # Calculated x-axis error
        self.yaxis = None   # Calculated y-axis error

class EditPage(QWidget):
    """
    Represents the image editing page where users can select points on images to 
    calculate real-world measurements. 
    """

    def __init__(self, parent): 
        super().__init__()
        self.parent = parent # Save the reference to the parent

        # Initialize the file manager and calculations manager objects
        self.file_manager = FileManager()

        # Initialize the class attributes
        self.axis_orientation = None  # The orientation of the axes
        self.scaling_factor = None # Ratio between images and the real world
        
        self.current_idx = 0 # Current image we are analyzing
        self.num_images = 0 # Total number of images to analyze

        self.target_point = None  # The target point in each image

        self.initUI()

    def handle_point_clicked(self, x, y):
        """ Handle the event when a point is clicked on the image. 
            Calculate the z-axis, y-axis, and x-axis values based on the selected points.
        Args: 
            x (float): x-coordinate of the clicked point
            y (float): y-coordinate of the clicked point """
        # If target has not been selected, set the selected point as the target
        if not self.target_point:
            self.target_point = (x, y)
            # Update the text so the user knows to click again
            self.direction_label.setText("Please click on the implement.")
            # Draw a circle on the target point
            self.image_viewer.draw_point_circle(self.target_point[0], self.target_point[1])
            # Show and enable the button to reselect the target
            self.target_button.show() # Show the reselect target button
            self.target_button.setEnabled(True) # Enable the reselect target button

        # Otherwise, this is an implement selection
        else:
            self.direction_label.setText("Loading Next Image .....")
            self.calculate_and_display(x, y)

    def calculate_and_display(self, x, y):
        """ Calculate the radial, y-axis, and x-axis values based on the selected points.
        Args: 
            x (float): x-coordinate of the clicked point
            y (float): y-coordinate of the clicked point """
        
        # Calculate delta x and y values based on the target point
        delta_x = self.target_point[0] - x
        delta_y = self.target_point[1] - y

        # Determine vertical and horizontal values based on the selected axes
        # Adjust the values based on the selected axis orientation
        # Default orientation is 0 (x-axis: horizontal, y-axis: vertical)

        # Adjust x and y values to match the orientation
        if self.axis_orientation == 0:
            delta_x, delta_y = -delta_x, delta_y
        elif self.axis_orientation == 1:
            delta_x, delta_y = -delta_y, -delta_x
        elif self.axis_orientation == 2:
            delta_x, delta_y = delta_x, -delta_y
        elif self.axis_orientation == 3:
            delta_x, delta_y = delta_y, delta_x
        else:
            print("Axis orientation is not valid. Using the default orientation")
            self.axis_orientation = 0

        img = self.images[self.current_idx]

        # Calculate the z-axis error using the adjusted delta_x and delta_y  values
        img.radial = f'{calc.calculate_error(self.target_point, (x, y), self.scaling_factor):.2f}'

        # Calculate real-world distances using the adjusted delta_x and delta_y values
        img.xaxis = f'{(delta_x * self.scaling_factor):.2f}'
        img.yaxis = f'{(delta_y * self.scaling_factor):.2f}'

        # Display the next image after a delay
        QTimer.singleShot(500, lambda: self.next_image("Please click on the implement"))

    def reselect_target(self):
        """ Allow the user to reselect the target point on the image.
            Load the current image with a message to click on the target again. """
        self.target_point = None
        self.load_image("Please click on the target")
       
    def load_image(self, text): 
        """ Load the image at the specified index from the image list.
            Update the direction label with the specified text.
            Clear the clicked points and load the image in the image viewer.
        Args:
            text (string): Text to display in the direction label
        Raises:
            IndexError if the current index is out of range.
            FileNotFoundError if the image to load is not found.
        """
        # Validate index
        if self.current_idx < 0 or self.current_idx >= len(self.images):
            raise IndexError("Index out of range for image list.")
        # Get image path from the list
        image = self.images[self.current_idx]
        # Validate image file existence
        if not os.path.exists(image.path):
            raise FileNotFoundError(f"Image not found: {image.path}")

        self.direction_label.setText(text)
        # Load the image in the image viewer
        self.image_viewer.load_image(image.path)  
        # Draw the target point if target point is selected
        if self.target_point:
            self.image_viewer.draw_point_circle(self.target_point[0], self.target_point[1])

    def next_image(self, text):
        """ Load the next image in the image list.
            Increment the image index and update the information label.
        Args:
            text (string): Text to display in the direction label """
        # Increment the image index and update information
        self.current_idx += 1 
        # Advance to the next image if there is one
        if self.current_idx < len(self.images): 
            # Update the info label with the most recent data
            self.info_label.setText(self.format_label())
            self.load_image(text)
        # Otherwise, we have reached the end of our image list
        else:
            self.end_editing()

    def previous_image(self):
        """ Load the previous image in the image list. Decrement the image 
            index and update the information label. """
        if self.current_idx > 0:
            self.current_idx -= 1
            # Update the info label with the most recent data
            self.info_label.setText(self.format_label())
            self.load_image("Loaded previous image please click on the implement")
        else:
            QMessageBox.warning(self, "Start of Images", "This is the first image.")

    def no_image(self):
        """ When trial with no existing picture exists, user presses this button
            to add 'zero' data to resuts. """
        img = self.images[self.current_idx]
        img.radial, img.xaxis, img.yaxis = NO_IMAGE, NO_IMAGE, NO_IMAGE # Placeholder data
        self.next_image("Previous trial image DNE. Next image loaded")
            
    def invalid_trial(self):
        """ When trial exists when implement lies outside of valid grid area, user
            presses button to add outlier to results data. """
        img = self.images[self.current_idx]
        img.radial, img.xaxis, img.yaxis = OUT_OF_BOUNDS, OUT_OF_BOUNDS, OUT_OF_BOUNDS # Placeholder data
        self.next_image("Previous trial was out of bounds. Next image loaded")

    def format_label(self):
        """ Format the text to display in the label at the top of the window. """
        # Subtract 1 to get values for the previous image
        img = self.images[self.current_idx-1]
        # Add 1 to current_idx to make the values 1 indexed
        return f"On Trial [{self.current_idx+1}] out of [{self.num_images}] || Previous Trial Values: || {HEADERS.RADIAL.value}: {img.radial} | {HEADERS.X_AXIS.value}: {img.xaxis} | {HEADERS.Y_AXIS.value}: {img.yaxis}"

    def end_editing(self):
        """ Clean up the window at the end of the editing session. """
        # First, write the image data to the results file
        self.file_manager.write_results(self.images)
        # If at the end of the image list, remove image viewer and add options
        QMessageBox.information(self, "End of Images", 
                                "All images have been processed.")

        # Add a label to indicate completion
        completion_label = QLabel("Processing complete! What would you like to do next?")
        completion_label.setAlignment(Qt.AlignCenter)
        completion_label.setStyleSheet(f"font-size: 18px; font-weight: 20px;")
        self.layout.addWidget(completion_label)

        # Add a button to navigate to do another trial
        trial_button = QPushButton("Another Trial")
        trial_button.setStyleSheet(
            f"font-size: {BUTTON_FONT_SIZE}; padding: {BUTTON_PADDING};")
        trial_button.clicked.connect(self.go_back_to_trial)
        self.layout.addWidget(trial_button)

        # Add a button to navigate to the Data Review Page
        data_review_button = QPushButton("Go to Data Review")
        data_review_button.setStyleSheet(
            f"font-size: {BUTTON_FONT_SIZE}; padding: {BUTTON_PADDING};")
        data_review_button.clicked.connect(self.go_to_data_review)
        self.layout.addWidget(data_review_button)

        # Add a button to return to the main menu
        main_menu_button = QPushButton("Back to Main Menu")
        main_menu_button.setStyleSheet(
            f"font-size: {BUTTON_FONT_SIZE}; padding: {BUTTON_PADDING};")
        main_menu_button.clicked.connect(self.go_to_main_menu)
        self.layout.addWidget(main_menu_button)

        # Add a button to exit the program
        exit_button = QPushButton("Exit Program")
        exit_button.setStyleSheet(
            f"font-size: {BUTTON_FONT_SIZE}; padding: {BUTTON_PADDING};")
        exit_button.clicked.connect(self.exit_program)
        self.layout.addWidget(exit_button)


    ###############################
    # Data initialization methods #
    ###############################

    def create_files_list(self, folder_path, cal_image_path):
        """ Create the list of image files in the selected folder.
        Args: 
            folder_path (string): Path to the folder containing images to analyze.
            cal_image_path (string): Path to the selected calibration image.
        """
        # Ensure image_path is the first in the image list
        self.image_files = [
            os.path.normpath(os.path.join(folder_path, f))
            for f in sorted(os.listdir(folder_path))
            if f.lower().endswith(tuple(IMAGE_TYPES))
        ]

        # Normalize image_path for comparison
        normalized_image_path = os.path.normpath(cal_image_path)

        # Remove image_path if it exists and insert it at the beginning
        if normalized_image_path in self.image_files:
            self.image_files.remove(normalized_image_path)

        # Create a list of Images for each image in the file list
        self.images = [Image(os.path.basename(file), file, idx) for idx, file in enumerate(self.image_files)]
        self.num_images = len(self.images)

    def set_data(self, scaling_factor, folder_path, image_path, axis_orientation):
        """ Set the data required for image editing.
        Args:
            scaling_factor (float): Ratio between the real-world and pixel distance for the images
            folder_path (string): Path to the folder containing images
            image_path (string): Path to the selected calibration image
            axis_orientation (int): The index of the axis orientation image """
        self.scaling_factor = scaling_factor
        self.file_manager.set_results_folders(folder_path)
        self.axis_orientation = axis_orientation
        self.create_files_list(folder_path, image_path)
        self.info_label.setText(f"On trial [{self.current_idx+1}] out of [{len(self.images)}]")
        self.load_image("Please click on the target")

    #############################
    # UI and Navigation Methods #
    #############################
    
    def initUI(self):
        self.layout = QVBoxLayout() # Create a vertical layout for the page

        # Direction label: text on the top of the page of directions for the user
        self.direction_label = QLabel("Direction: Click to select the target point")
        # Set the alignment of the text to target
        self.direction_label.setAlignment(Qt.AlignCenter)
        # Set the font size, weight, and margin for the text
        self.direction_label.setStyleSheet(STYLE_SHEET)
        # Add the text to the layout
        self.layout.addWidget(self.direction_label)

        # create a horizontal layout for buttons
        axis_button_layout = QHBoxLayout()

        # Button to reselect the target point in the image
        self.target_button = QPushButton("Reselect Target")
        self.target_button.setEnabled(False)
        self.target_button.clicked.connect(self.reselect_target)
        self.target_button.hide()

        # Button to go back to the previous image in the list
        self.previous_button = QPushButton("Previous Image")
        self.previous_button.clicked.connect(self.previous_image)

        # Button to skip an image if it does not exist
        self.skip_button = QPushButton("No Trial")
        self.skip_button.clicked.connect(self.no_image)

        # Button to skip invalid image
        self.outlier_button = QPushButton("Out of bounds")
        self.outlier_button.clicked.connect(self.invalid_trial)

        # Add buttons to horizontal layout
        buttons = [self.previous_button, self.target_button, self.skip_button, self.outlier_button]
        [axis_button_layout.addWidget(button) for button in buttons]
        [button.setStyleSheet(f'font-size: {BUTTON_FONT_SIZE}') for button in buttons]

        # Add the horizontal layout to the main vertical layout
        self.layout.addLayout(axis_button_layout)

        # Info Label: text on top of image to display the information
        self.info_label = QLabel("")
        # Set the alignment of the text to center
        self.info_label.setAlignment(Qt.AlignCenter)
        # Set the font size, weight, and margin for the text
        self.info_label.setStyleSheet(STYLE_SHEET)
        # Add the text to the layout
        self.layout.addWidget(self.info_label)

        # Image viewer
        # Create an image viewer widget
        self.image_viewer = ImageView()
        # Add the image viewer to the layout
        self.layout.addWidget(self.image_viewer)
        self.setLayout(self.layout)

        # Connect the point_clicked signal from the ImageView to the point_clicked method
        self.image_viewer.point_clicked.connect(self.handle_point_clicked)

    def go_to_data_review(self):
        """ Navigate to the DataReviewPage and load the result file. """
        result_file_path = self.file_manager.results_file
        if result_file_path:
            self.restart_page()
            self.parent.data_review_page.read_and_display_data(result_file_path)
            self.parent.nav_to_data_page()
        else:
            QMessageBox.warning(self, "File Missing", "Result file path is not available.")

    def go_to_main_menu(self):
        """ Navigate back to the main menu. """
        self.restart_page()
        self.parent.nav_to_main_menu()

    def go_back_to_trial(self):
        """ Navigate back to the calibration page. """
        self.restart_page()
        self.parent.nav_to_calibration_page()

    def exit_program(self):
        """ Exit the program. """
        self.restart_page()
        QApplication.quit()

    def restart_page(self):
        """ Clear memory to start a new trial  """
        parent_stack = self.parent.stack  # Get reference to QStackedWidget

        # Remove existing instances of EditPage and CalibrationPage from QStackedWidget
        parent_stack.removeWidget(self.parent.edit_page)
        parent_stack.removeWidget(self.parent.calibration_page)

        # Delete the old instances to free memory
        self.parent.edit_page.deleteLater()
        self.parent.calibration_page.deleteLater()

        #  Create fresh instances of both pages
        self.parent.calibration_page = CalibrationPage(self.parent)
        self.parent.edit_page = EditPage(self.parent)

        #  Add the new instances back to QStackedWidget
        parent_stack.addWidget(self.parent.calibration_page)
        parent_stack.addWidget(self.parent.edit_page)
