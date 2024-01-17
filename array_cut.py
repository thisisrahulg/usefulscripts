#!/usr/bin/env python3

"""
Author: Rahul G

This is a small script to cut of desired portion from a 2D array.

Give the path to the fits file as input and then right click to start selecting. Double right-click at the end to close 
and show the output.

The outside will be just NaN values.

"""
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from matplotlib.path import Path

def plot_and_cut(fits_file):
    # Read the FITS file
    hdul = fits.open(fits_file)
    array = hdul[0].data

    # Plot the original array
    plt.imshow(array, cmap='viridis', interpolation='nearest')
    plt.title('Right-click to select points for the closed shape (Double right-click to finish)')
    
    # Initialize an empty list to store the clicked points
    points = []

    def onbutton(event):
        nonlocal points
        if event.button == 3 and event.dblclick:
            # Right double-click detected, end the input
            plt.close()
        elif event.button == 3:
            # Right-click detected, add the clicked point to the list
            points.append((event.xdata, event.ydata))
            
            # Draw a red dot at the clicked point for visual feedback
            plt.text(event.xdata, event.ydata, '+', color='red', ha='center', va='center', fontsize=10)

        plt.draw()

    # Connect the onbutton function to the figure
    plt.gcf().canvas.mpl_connect('button_press_event', onbutton)

    # Show the plot and wait for the user to double right-click
    plt.show()

    # Create a closed shape based on the selected points
    path = Path(points + [points[0]])

    # Create a binary mask based on the closed shape
    y, x = np.mgrid[:array.shape[0], :array.shape[1]]
    mask = path.contains_points(np.column_stack((x.ravel(), y.ravel()))).reshape(array.shape)

    # Apply the mask to the array
    cut_array = np.where(mask, array, np.nan)
    # Plot the original and cut arrays
    plt.subplot(121)
    plt.imshow(array, cmap='viridis', interpolation='nearest')
    plt.title('Original Array')

    plt.subplot(122)
    plt.imshow(cut_array, cmap='viridis', interpolation='nearest')
    plt.title('Array with Closed Shape Cut Out')

    plt.show()
    return cut_array

if __name__ == "__main__":
    # Provide the path to your FITS file
    import sys
    fits_file_path = sys.argv[1]
    
    # Call the function
    cut_part = plot_and_cut(fits_file_path)

