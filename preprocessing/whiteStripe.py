import numpy as np
def whiteStripe(image):
    hist, bin_edges = np.histogram(image, bins=range(int(np.min(image)), int(np.max(image)) + 1))
    rightmost_mode_index = np.argmax(hist[::-1])
    rightmost_mode_value = bin_edges[::-1][rightmost_mode_index] 
    newImg = image/rightmost_mode_value
    return newImg