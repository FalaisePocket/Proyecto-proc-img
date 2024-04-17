import numpy as np

def resize_image(image):
    
    minI=int(np.min(image))
    maxI=int(np.max(image))
    resized_image = (image-minI)/maxI-minI
    return resized_image
