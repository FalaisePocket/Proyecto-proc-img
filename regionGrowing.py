import numpy as np

def region_growing(image, seed, threshold):
    mask = np.zeros(image.shape)

    region_pixels = [seed]

    while len(region_pixels) > 0:

        current_point = region_pixels[0]

        for neighbor in [(current_point[0]+1, current_point[1], current_point[2]),
                         (current_point[0]-1, current_point[1], current_point[2]),
                         (current_point[0], current_point[1]+1, current_point[2]),
                         (current_point[0], current_point[1]-1, current_point[2]),
                         (current_point[0], current_point[1], current_point[2]+1),
                         (current_point[0], current_point[1], current_point[2]-1)]:
            
            if (neighbor[0] < 0 or neighbor[0] >= image.shape[0] or
                neighbor[1] < 0 or neighbor[1] >= image.shape[1] or
                neighbor[2] < 0 or neighbor[2] >= image.shape[2]):
                continue
            
            if (mask[neighbor] == 0 and abs(int(image[neighbor]) - int(image[current_point])) < threshold):

                region_pixels.append(neighbor)
                mask[neighbor] = 1
        region_pixels.pop(0)
    return mask


