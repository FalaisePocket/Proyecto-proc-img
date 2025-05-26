import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def comparar_nii(path1, path2, mostrar_slice=False, slice_index=None):
    # Cargar los archivos
    img1 = nib.load(path1)
    img2 = nib.load(path2)

    data1 = img1.get_fdata()
    data2 = img2.get_fdata()

    # Comparar dimensiones
    if data1.shape != data2.shape:
        print(f"⚠️ Dimensiones distintas: {data1.shape} vs {data2.shape}")
    else:
        print(f"✅ Dimensiones iguales: {data1.shape}")

    # Comparar affines (espacio físico)
    if not np.allclose(img1.affine, img2.affine):
        print("⚠️ Las matrices affine son diferentes.")
        print("Affine 1:\n", img1.affine)
        print("Affine 2:\n", img2.affine)
    else:
        print("✅ Las matrices affine son iguales.")

    # Comparar voxel a voxel
    if data1.shape == data2.shape:
        mse = np.mean((data1 - data2) ** 2)
        mae = np.mean(np.abs(data1 - data2))
        max_diff = np.max(np.abs(data1 - data2))
        print(f"📊 MSE: {mse:.4f} | MAE: {mae:.4f} | Máxima diferencia: {max_diff:.4f}")
    else:
        print("❌ No se puede comparar voxel a voxel porque las dimensiones no coinciden.")

    # Visualización opcional
    if mostrar_slice and data1.shape == data2.shape:
        if slice_index is None:
            slice_index = data1.shape[2] // 2  # corte medio

        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        axes[0].imshow(data1[:, :, slice_index], cmap="gray")
        axes[0].set_title("Imagen 1")

        axes[1].imshow(data2[:, :, slice_index], cmap="gray")
        axes[1].set_title("Imagen 2")

        diff = np.abs(data1[:, :, slice_index] - data2[:, :, slice_index])
        axes[2].imshow(diff, cmap="hot")
        axes[2].set_title("Diferencia")

        for ax in axes:
            ax.axis("off")
        plt.tight_layout()
        plt.show()


comparar_nii("sub-33_T1w.nii", "imagen_movil_registrada.nii", mostrar_slice=True)
