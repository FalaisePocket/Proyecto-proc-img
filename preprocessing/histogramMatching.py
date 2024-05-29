import numpy as np
import nibabel as nib
import os

def histogram_matching(imageData):

    
    image= imageData.tolist()        

    current_dir = os.path.dirname(os.path.abspath(__file__))
    fixed_img = nib.load(os.path.join(current_dir, "fixedres.nii"))
    image_source_data=fixed_img.get_fdata()
    image_source = image_source_data.tolist()
    '''
    histogram_source = calculate_histogram(image_source)
    histogram_reference = calculate_histogram(image)'''
    histogram_source, binssource = np.histogram(image_source, bins=30)
    histogram_reference, binsref = np.histogram(image, bins=30 )



    # Calcula las CDFs
    cdf_source = calculate_cdf(histogram_source)
    cdf_reference = calculate_cdf(histogram_reference)

    # Crea la tabla de correspondencia usando las CDFs
    lookup_table = match_histograms(cdf_source, cdf_reference)

    # Aplica la tabla de correspondencia a la imagen de origen
    matched_image = apply_lookup_table(image_source, lookup_table)

    # Ahora `matched_image` contiene la imagen de entrada ajustada al histograma de la imagen de referencia

    return np.array(matched_image)
    


def calculate_histogram(image):
    histogram = [0] * 256  # Asumiendo imágenes en escala de grises de 8 bits
    for slice in image:
        for row in slice:
            for pixel in row:
                histogram[pixel] += 1
    return histogram

def calculate_cdf(histogram):
    cdf = [0] * len(histogram)
    cumsum = 0
    for idx, val in enumerate(histogram):
        cumsum += val
        cdf[idx] = cumsum
    cdf = [x / cdf[-1] for x in cdf]  # Normalización
    return cdf

def match_histograms(cdf_source, cdf_reference):
    lookup_table = [0] * 256
    ref_idx = 0
    for src_idx in range(256):
        while ref_idx < 255 and cdf_reference[ref_idx] < cdf_source[src_idx]:
            ref_idx += 1
        lookup_table[src_idx] = ref_idx
    return lookup_table

def apply_lookup_table(image, lookup_table):
    matched_image = []
    for slice in image:
        matched_slice=[]
        for row in slice:
            matched_row = [lookup_table[int(pixel)] for pixel in row]
            matched_slice.append(matched_row)
        matched_image.append(matched_slice)
    return matched_image


'''# Supongamos que `image_source` y `image_reference` son tus matrices de intensidades
# Calcula los histogramas
histogram_source = calculate_histogram(image_source)
histogram_reference = calculate_histogram(image_reference)

# Calcula las CDFs
cdf_source = calculate_cdf(histogram_source)
cdf_reference = calculate_cdf(histogram_reference)

# Crea la tabla de correspondencia usando las CDFs
lookup_table = match_histograms(cdf_source, cdf_reference)

# Aplica la tabla de correspondencia a la imagen de origen
matched_image = apply_lookup_table(image_source, lookup_table)

# Ahora `matched_image` contiene la imagen de entrada ajustada al histograma de la imagen de referencia'''