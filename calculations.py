############################################################################################
# Project Name: Motor Skill Acquisition Error Management System
# 
# Authors: Milton Tinoco, Ethan Weldon, Joshua Samson, Michael Cabrera
# San Francisco State University
#
# File Description:
# This file contains the code for calcuations related to pixel distances,
# scaling factors, errors, and real-world coordinates.
############################################################################################

from numpy import sqrt

def calculate_error(point1, point2, scaling_factor=1):
    """ Calculates the euclidian distance between two points, scaled by the scaling_factor. 
    Args: 
        point1 (float, float): A tuple representing the first point
        point2 (float, float): A tuple representing the second point
        scaling_factor (float): The ratio between the real-world and pixel distance
    Returns:
        float: The euclidian distance
    """
    x1, y1 = point1
    x2, y2 = point2 
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * scaling_factor

def calculate_scaling_factor(real_world_distance, point1, point2):
    """ Calculate the scaling factor given a real-world distance and a pixel distance.
    Args:
        real_world_distance (float): The real-world distance
        pixel_distance (float): The pixel distance
    Returns:
        float: The scaling factor.
    Raises:
        ValueError: If pixel_distance is zero to prevent division by zero.
    """
    pixel_distance = calculate_error(point1, point2)
    if pixel_distance == 0:
        raise ValueError("The same point was selected twice. Please select two different points.")
    return real_world_distance / pixel_distance

