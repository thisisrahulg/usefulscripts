import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from astropy.io import fits
from matplotlib.path import Path

def plot_and_cut(fits_file):
    # Read the FITS file
    hdul = fits.open(fits_file)
    array = hdul[0].data

    # Plot the original array
    plt.imshow(array, cmap='viridis', interpolation='nearest')
    plt.title('Click to select points for the closed shape')
    
    # Get the number of corners from the user
    num_corners = int(input('Enter the number of corners to click: '))

    # Get user input by clicking points
    points = plt.ginput(n=num_corners, timeout=0)

    # Close the plot
    plt.close()

    # Create a closed shape based on the selected points
    path = Path(points + [points[0]])

    # Create a binary mask based on the closed shape
    y, x = np.mgrid[:array.shape[0], :array.shape[1]]
    mask = path.contains_points(np.column_stack((x.ravel(), y.ravel()))).reshape(array.shape)

    # Apply the mask to the array
    cut_array = np.where(mask, array, 0)

    # Plot the original and cut arrays
    plt.subplot(121)
    plt.imshow(array, cmap='viridis', interpolation='nearest')
    plt.title('Original Array')

    plt.subplot(122)
    plt.imshow(cut_array, cmap='viridis', interpolation='nearest')
    plt.title('Array with Closed Shape Cut Out')

    plt.show()

if __name__ == "__main__":
    # Provide the path to your FITS file
    import sys
    fits_file_path = sys.argv[1]
    
    # Call the function
    plot_and_cut(fits_file_path)
