import nibabel as nib
import SimpleITK as sitk
import numpy as np
import os

# Función auxiliar para extraer información del affine de nibabel
def affine_to_sitk_metadata(affine):
    spacing = np.sqrt((affine[:3, :3]**2).sum(axis=0))
    direction = (affine[:3, :3] / spacing).flatten()
    origin = affine[:3, 3]
    return spacing, direction.tolist(), origin.tolist()

def registro(movingImgDir):
    # Obtener ruta actual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Cargar imágenes con nibabel
    fixed_nib = nib.load(os.path.join(current_dir, "fixed.nii"))
    moving_nib = nib.load(movingImgDir)

    # Extraer los datos como arrays
    fixed_data = fixed_nib.get_fdata()
    moving_data = moving_nib.get_fdata()

    # Crear imágenes SimpleITK desde arrays
    fixed_img_sitk = sitk.GetImageFromArray(fixed_data)
    moving_img_sitk = sitk.GetImageFromArray(moving_data)

    # ✅ CORRECCIÓN 1: Transferir metadata espacial desde nibabel a SimpleITK
    fixed_spacing, fixed_direction, fixed_origin = affine_to_sitk_metadata(fixed_nib.affine)
    moving_spacing, moving_direction, moving_origin = affine_to_sitk_metadata(moving_nib.affine)

    fixed_img_sitk.SetSpacing(fixed_spacing)
    fixed_img_sitk.SetDirection(fixed_direction)
    fixed_img_sitk.SetOrigin(fixed_origin)

    moving_img_sitk.SetSpacing(moving_spacing)
    moving_img_sitk.SetDirection(moving_direction)
    moving_img_sitk.SetOrigin(moving_origin)

    # Configurar el método de registración
    registration_method = sitk.ImageRegistrationMethod()
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    registration_method.SetMetricSamplingPercentage(0.01)  # Mejora el rendimiento
    registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100)
    registration_method.SetOptimizerScalesFromPhysicalShift()

    # ✅ CORRECCIÓN 2: Inicializar correctamente la transformación
    initial_transform = sitk.CenteredTransformInitializer(
        fixed_img_sitk, moving_img_sitk, sitk.Euler3DTransform(), sitk.CenteredTransformInitializerFilter.GEOMETRY
    )
    registration_method.SetInitialTransform(initial_transform, inPlace=False)

    # Ejecutar el registro
    final_transform = registration_method.Execute(fixed_img_sitk, moving_img_sitk)

    # Aplicar la transformación a la imagen movible
    registered_img = sitk.Resample(
        moving_img_sitk,
        fixed_img_sitk,
        final_transform,
        sitk.sitkLinear,
        0.0,
        moving_img_sitk.GetPixelID()
    )

    # ✅ CORRECCIÓN 3: Convertir correctamente a NIfTI y preservar la geometría del fixed
    registered_data = sitk.GetArrayFromImage(registered_img)
    nib.save(nib.Nifti1Image(registered_data, fixed_nib.affine), 'imagen_movil_registrada.nii')

    print("Registro completado y guardado como 'imagen_movil_registrada.nii'")
