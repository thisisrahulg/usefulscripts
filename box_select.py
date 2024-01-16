import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

class BoxSelector:
    def __init__(self, ax, fits_data):
        self.ax = ax
        self.fits_data = fits_data
        self.selection_active = False
        self.selection_start = None
        self.selection_rect = None

        self.cid_press = ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.button == 1:
            self.selection_active = True
            self.selection_start = (event.xdata, event.ydata)

    def on_release(self, event):
        if event.button == 1 and self.selection_active:
            self.selection_active = False
            if self.selection_rect:
                self.selection_rect.remove()
                self.selection_rect = None

            x1, y1 = self.selection_start
            x2, y2 = event.xdata, event.ydata

            # Ensure the coordinates are in the correct order
            y1, y2 = sorted([y1, y2])
            x1, x2 = sorted([x1, x2])

            self.selected_data = self.fits_data[int(y1):int(y2), int(x1):int(x2)]

            # Display the selected region
            self.plot_selected()

    def on_motion(self, event):
        if self.selection_active:
            x1, y1 = self.selection_start
            x2, y2 = event.xdata, event.ydata

            # Ensure the coordinates are in the correct order
            y1, y2 = sorted([y1, y2])
            x1, x2 = sorted([x1, x2])

            # Draw or update the selection rectangle
            if self.selection_rect:
                self.selection_rect.set_width(x2 - x1)
                self.selection_rect.set_height(y2 - y1)
                self.selection_rect.set_xy((x1, y1))
            else:
                self.selection_rect = plt.Rectangle((x1, y1), x2 - x1, y2 - y1, edgecolor='red', facecolor='none')
                self.ax.add_patch(self.selection_rect)
            
            self.ax.figure.canvas.draw()

    def plot_selected(self):
        plt.figure()
        plt.imshow(self.selected_data, cmap='viridis', interpolation='nearest')
        plt.title('Selected Region')
        plt.show()

def plot_and_select(fits_file):
    # Read the FITS file
    hdul = fits.open(fits_file)
    array = hdul[0].data

    # Plot the original array
    fig, ax = plt.subplots()
    ax.imshow(array, cmap='viridis', interpolation='nearest')
    ax.set_title('Click and drag to select a region')

    # Initialize the BoxSelector
    box_selector = BoxSelector(ax, array)

    plt.show()

if __name__ == "__main__":
    # Provide the path to your FITS file as a command-line argument
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/your/file.fits")
        sys.exit(1)
    fits_file_path = sys.argv[1] 
    
    # Call the function
    plot_and_select(fits_file_path)

