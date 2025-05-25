import nibabel as nib
import SimpleITK as sitk
import os

def registro(movingImgDir):
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fixed_img = nib.load(os.path.join(current_dir, "fixed.nii"))
    moving_img = nib.load(movingImgDir)


    fixed_img_sitk = sitk.GetImageFromArray(fixed_img.get_fdata())
    moving_img_sitk = sitk.GetImageFromArray(moving_img.get_fdata())


    registration_method = sitk.ImageRegistrationMethod()

    # Configurar el método de registración
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100)
    registration_method.SetOptimizerScalesFromPhysicalShift()

    # Aplicar la registración
    transform = sitk.CenteredTransformInitializer(fixed_img_sitk, moving_img_sitk, sitk.Euler3DTransform())
    registration_method.SetInitialTransform(transform)
    final_transform = registration_method.Execute(fixed_img_sitk, moving_img_sitk)

    # Aplicar la transformación a la imagen movible
    registered_img = sitk.Resample(moving_img_sitk, fixed_img_sitk, final_transform, sitk.sitkLinear, 0.0)

    # Guardar la imagen registrada
    nib.save(nib.Nifti1Image(sitk.GetArrayFromImage(registered_img), fixed_img.affine), 'imagen_movil_registrada.nii')