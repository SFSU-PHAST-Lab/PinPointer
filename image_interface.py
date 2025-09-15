############################################################################################
# Project Name: Motor Skill Acquisition Error Management System 
# 
# Filename: Image_interface.py
#
# Authors: Milton Tinoco, Ethan Weldon, Joshua Samson, Michael Cabrera
# San Francisco State University
#
# File Description:
# The image interface displays images and allows users to select points on them. The 
# ImageView class is a custom QGraphicsView that displays images and emits signals when 
# points are clicked on the image.
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

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QPen
from PyQt5.QtCore import Qt, QLineF, pyqtSignal

from constants import CIRCLE_RADIUS, CROSS_WIDTH, PEN_COLOR, TARGET_COLOR, PEN_WIDTH, ZOOM_SCALE

class ImageView(QGraphicsView):
    """ 
    A custom QGraphicsView that displays images and emits signals when points are clicked on 
    the image. It allows users to click on the image to select points and emits signals with 
    the coordinates of the clicked points.
    """
    point_clicked = pyqtSignal(float, float) # Signal emitted when a point is clicked on the image

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self) # Create a QGraphicsScene
        self.setScene(self.scene) # Set the scene for the view

        self.pen = QPen(PEN_COLOR) # Color of the pen
        self.pen.setWidth(PEN_WIDTH) # Width of the pen

        self.image_selected = False # Flag to check if an image is loaded

    def draw_point_circle(self, x, y):
        """ Draw a circle centered at the specified point on the image. 
        Args:
            x (float): x-coordinate of the point to draw.
            y (float): y-coordinate of the point to draw. """
        # Add an ellipse item to the scene to represent the circle
        ellipse_item =self.scene.addEllipse(
            x - CIRCLE_RADIUS, y - CIRCLE_RADIUS, 2 * CIRCLE_RADIUS, 2 * CIRCLE_RADIUS, self.pen
        )
        ellipse_item.setBrush(TARGET_COLOR)  # Set the brush color

    def load_image(self, image_path):
        """ Load and display the selected image.
        Args:
            image_path (string): Path to the image file to laod """
        pixmap = QPixmap(image_path).scaled(1600, 1200, Qt.KeepAspectRatio) # Load the image and scale it
        self.scene.clear() # Clear the scene
        self.image_item = QGraphicsPixmapItem(pixmap) # Create a QGraphicsPixmapItem with the image
        self.scene.addItem(self.image_item) # Add the image item to the scene
        self.image_selected = True # Set the flag to indicate that an image is loaded
        self.fitInView(self.image_item, Qt.KeepAspectRatio) # Fit the image to the view

    def mousePressEvent(self, event):
        """ Handle mouse press events on the image view. When the left mouse button is 
            clicked, emit a signal with the coordinates of the clicked point. 
        Args:
            event: Mouse press event """
        # Check if an image is loaded and return if not
        if not self.image_selected:
            return

        # Check if the left mouse button is clicked
        if event.button() == Qt.LeftButton:
            scene_pos = self.mapToScene(event.pos()) # Get the position of the click in the scene
            self.point_clicked.emit(scene_pos.x(), scene_pos.y())  # Emit the clicked point         

            # Draw a cross centered at the clicked position
            self.scene.addLine(
                QLineF(scene_pos.x() - CROSS_WIDTH, scene_pos.y(),
                       scene_pos.x() + CROSS_WIDTH, scene_pos.y()),
                self.pen)
            self.scene.addLine(
                QLineF(scene_pos.x(), scene_pos.y() - CROSS_WIDTH,
                       scene_pos.x(), scene_pos.y() + CROSS_WIDTH),
                self.pen)

    def wheelEvent(self, event):
        """ Zoom in and out of the image based on the specified scale_factor.
        Args:
            event: Wheel event """
        if event.angleDelta().y() > 0:
            self.scale(ZOOM_SCALE, ZOOM_SCALE)
        else:
            self.scale(1 / ZOOM_SCALE, 1 / ZOOM_SCALE)
