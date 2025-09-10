#############################################################################################################
# Project Name: Motor Skill Acquisition Error Management System
# 
# Filename: data_review_page.py
# 
# Authors: Milton Tinoco, Ethan Weldon, Joshua Samson, Michael Cabrera
# San Francisco State University
#
# File Description:
# This file contains the code for the data review page, which loads data from a results file,
# displays it in a table, and provides options to export the data, show statistics, and generate graphs.
###########################################################################################################

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget,
                             QTableWidgetItem, QHBoxLayout, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use(("Qt5Agg"))
import matplotlib.pyplot as plt

from constants import FONT_SIZE, BUTTON_FONT_SIZE, RESULTS_DIR, RESULTS_FILENAME, NO_IMAGE, OUT_OF_BOUNDS, HEADERS

class DataReviewPage(QWidget):
    """
    This class represents the data review page of the application.
    It allows users to load data from a Results_File.txt file, display it in a table,
    export the data to Excel or CSV, show statistics, and generate graphs.
    """

    def __init__(self, parent=None):
        super().__init__(parent)  # Pass parent to the base class constructor
        self.parent = parent # Set the parent widget
        self.initUI() # Initialize the UI elements of the page

        self.data = None # The data to review

    def initUI(self):
        """ Initializes the UI elements for the page. """
        self.setWindowTitle("Data Review Page")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        # Label for data review page
        self.data_label = QLabel("Data Review Page")
        self.data_label.setAlignment(Qt.AlignCenter)
        self.data_label.setStyleSheet(f"font-size: {FONT_SIZE};")
        layout.addWidget(self.data_label)

        # Table to display data
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(len(HEADERS))
        self.data_table.setHorizontalHeaderLabels([header.value for header in HEADERS])
        layout.addWidget(self.data_table)

        # Buttons
        button_layout = QHBoxLayout()

        # Button to load folder
        self.load_folder_button = QPushButton("Load Folder")
        self.load_folder_button.clicked.connect(self.load_folder)

        # Button to export data
        self.export_button = QPushButton("Export Data")
        self.export_button.clicked.connect(self.export_data)

        # Button to display statistics
        self.stats_button = QPushButton("Show Statistics")
        self.stats_button.clicked.connect(self.show_statistics)

        # Button to display graphs
        self.graphs_button = QPushButton("Show Graphs")
        self.graphs_button.clicked.connect(self.show_graphs)

        # Button to go back to main menu
        self.back_button = QPushButton("Back to Menu")
        self.back_button.clicked.connect(self.parent.nav_to_main_menu)

        # Set font size for all buttons
        buttons = [self.load_folder_button, self.export_button, self.stats_button, 
                   self.graphs_button, self.back_button]
        [button.setStyleSheet(f'font-size: {BUTTON_FONT_SIZE}') for button in buttons]
        [button_layout.addWidget(button) for button in buttons]

        # Add button layout to the main layout
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_folder(self):
        """ Prompts the user to select a folder and reads the data 
            in the results folder. """
        # Prompt the user to select a folder
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Folder", os.path.expanduser("~")
        )
        if folder_path:
            # Construct the file path
            results_file = os.path.join(folder_path, RESULTS_DIR, RESULTS_FILENAME)
            # Read the data if the file is valid
            if os.path.exists(results_file):
                self.read_and_display_data(results_file)
            # Otherwise, display an error message
            else:
                self.data_label.setText(f"❌ Error: {RESULTS_FILENAME} not found in the selected folder.")

    def read_and_display_data(self, file_path):
        """ Read data from the results and display it in the table. 
        Args:
            file_path (string): Absolute path to the file to open """
        try:
            with open(file_path, "r") as file:
                data = [self.format_line(line) for line in file if not line.strip().startswith("=")]

            # Save data for exporting
            self.data = pd.DataFrame(data, columns=[header.value for header in HEADERS])

            # Populate the table
            self.data_table.setRowCount(len(data))
            for row_idx, row_data in enumerate(data):
                for col_idx, value in enumerate(row_data):
                    self.data_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
            self.data_label.setText(f"Loaded data from: {file_path}")

        except IndexError as e:
            self.data_label.setText(f"Encountered error: '{e}'. Results file may be malformed.")
    
    def format_line(self, line):
        """ Extracts the data from the given line
        Args:
            line (string): The data with values to extract """
        if line.startswith(HEADERS.IMAGE_ID.value):
            try:
                id = line.split(HEADERS.IMAGE_ID.value)[1].split()[0]
                # name = line.split(HEADERS.IMAGE_NAME.value)[1].split()[0]
                name = line[line.find(HEADERS.IMAGE_NAME.value)+len(HEADERS.IMAGE_NAME.value) : line.rfind(HEADERS.RADIAL.value)].strip()
                radial = line.split(HEADERS.RADIAL.value)[1].split()[0]
                x_axis = line.split(HEADERS.X_AXIS.value)[1].split()[0]
                y_axis = line.split(HEADERS.Y_AXIS.value)[1].split()[0]

                if all(data == "N/A" for data in (radial, x_axis, y_axis)):
                    return [str(id), str(name), str(radial), str(x_axis), str(y_axis)]
                else:
                    return [str(id), str(name), float(radial), float(x_axis), float(y_axis)]
            except IndexError as e:
                raise e

    def show_statistics(self):
        """ Display enhanced statistics such as mean, median, standard deviation, and 
            variability metrics. """
        if self.data is not None:
            stats_summary = "Statistics:\n"

            # Get the last 3 columns (radial, xaxis, yaxis)
            for column in self.data.columns[-3:]: 
                column_data = self.data[column]
                # Mask the values to remove any with NO_IMAGE or OUT_OF_BOUNDS values
                column_data = column_data[~column_data.isin([NO_IMAGE, OUT_OF_BOUNDS])]
                
                # Basic numerical measures: Mean, median, and mode
                mean_value = column_data.mean()
                median_value = column_data.median()
                mode_value = column_data.mode().iloc[0] if not column_data.mode().empty else "No mode"
                
                # Spread and variability measures:
                # Standard deviation, variance, range, and interquartile range
                std_dev = column_data.std()
                variance = column_data.var()
                data_range = column_data.max() - column_data.min()
                iqr = column_data.quantile(0.75) - column_data.quantile(0.25)
                
                # Additional measure: max difference percentage
                # Calculate the maximum difference percentage from the mean
                absolute_difference = (column_data - mean_value).abs()
                max_difference = absolute_difference.max()
                max_difference_percentage = (max_difference / mean_value) * 100 if mean_value != 0 else 0

                # Append statistics for this column to the summary
                # Format the statistics with two decimal places
                stats_summary += (
                    f"Column: {column}\n"
                    f"  Mean (Average): {mean_value:.2f}\n"
                    f"  Median (Midpoint): {median_value:.2f}\n"
                    f"  Mode (Most Frequent): {mode_value}\n"
                    f"  Standard Deviation (Spread): {std_dev:.2f}\n"
                    f"  Variance: {variance:.2f}\n"
                    f"  Range (Max - Min): {data_range:.2f}\n"
                    f"  Interquartile Range (IQR): {iqr:.2f}\n"
                    f"  Max Difference (%): {max_difference_percentage:.2f}%\n"
                    "\n"
                )

            # Display the statistics in a dialog
            # Create a message box to show the statistics summary
            stats_dialog = QMessageBox()
            stats_dialog.setWindowTitle("Statistics Summary")
            stats_dialog.setText(stats_summary)
            stats_dialog.exec_() # Execute the dialog
        else:
            self.data_label.setText("No data ")

    def show_graphs(self):
        """ Generate and display graphs for the Radial, Y-Axis, and X-Axis data. """
        if self.data is not None:
            # Save column data into numpy arrays
            image_id = self.data[HEADERS.IMAGE_ID.value]
            radial = np.array(self.data[HEADERS.RADIAL.value])
            x_axis = np.array(self.data[HEADERS.X_AXIS.value])
            y_axis = np.array(self.data[HEADERS.Y_AXIS.value])

            # Mask all N/A points
            mask = ~np.all(np.column_stack((radial, x_axis, y_axis)) == NO_IMAGE, axis=1)
            image_id = image_id[mask]
            radial = radial[mask]
            x_axis = x_axis[mask]
            y_axis = y_axis[mask]

            # Mask all out of bounds points
            mask = ~np.all(np.column_stack((radial, x_axis, y_axis)) == OUT_OF_BOUNDS, axis=1)
            image_id = image_id[mask]
            radial = radial[mask]
            x_axis = x_axis[mask]
            y_axis = y_axis[mask]

            # Plot Radial
            plt.figure()
            plt.scatter(image_id, radial, marker="o", label=HEADERS.RADIAL.value)
            plt.xlabel(HEADERS.IMAGE_ID.value)
            plt.ylabel(HEADERS.RADIAL.value)
            plt.title("Radial vs. Image Trial")
            plt.legend()
            plt.grid(True)

            # Plot Y-Axis
            plt.figure()
            plt.scatter(image_id, y_axis, marker="o", label=HEADERS.Y_AXIS.value, color="green")
            plt.xlabel(HEADERS.IMAGE_NAME.value)
            plt.ylabel(HEADERS.Y_AXIS.value)
            plt.title("Y-Axis vs. Image Name")
            plt.legend()
            plt.grid(True)

            # Plot X-Axis
            plt.figure()
            plt.scatter(image_id, x_axis, marker="o", label=HEADERS.X_AXIS.value, color="red")
            plt.xlabel(HEADERS.IMAGE_NAME.value)
            plt.ylabel(HEADERS.X_AXIS.value)
            plt.title("X-Axis vs. Image Name")
            plt.legend()
            plt.grid(True)

            plt.show()
        else:
            self.data_label.setText("No data loaded to generate graphs.")

    def export_data(self):
        """ Export the data to Excel or CSV. """
        if self.data is not None:
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save File", os.path.expanduser("~"),
                "Excel Files (*.xlsx); CSV Files (*.csv)"
            )
            if save_path:
                if save_path.endswith(".xlsx"):
                    self.data.to_excel(save_path, index=False)
                elif save_path.endswith(".csv"):
                    self.data.to_csv(save_path, index=False)
                else:
                    self.data_label.setText("Invalid file format selected.")
                self.data_label.setText(f"Data exported to: {save_path}")
        else:
            self.data_label.setText("No data to export.")
