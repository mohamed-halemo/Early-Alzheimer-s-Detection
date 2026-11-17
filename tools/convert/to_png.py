import numpy as np
from PIL import Image
import os
import nibabel as nib
input_dir = "E:\GP\Brain\Extract_Zip_\zip" 
output_dir = "E:\GP\Brain\To_PNG\Data\AD" 
def cropping(img):
    if np.count_nonzero(img) == 0:
        return img
    xs, ys = np.where(img != 0)
    result = img[min(xs):max(xs) + 1, min(ys):max(ys) + 1]
    return result


for filename in os.listdir(input_dir):
    if filename.endswith(".nii") : 
        # Load the nifti image
        nii_image = nib.load(os.path.join(input_dir, filename))
        nii_data = nii_image.get_fdata()
        
        # Get the slices from 60 to 86
        slices = nii_data[60:87, :, :]
        
        # Process and save each slice as PNG
        for i in range(slices.shape[0]):
            im = np.asarray(slices[i, :, :])
            im = cropping(im)
            im = np.abs(((im - im.min()) / (im.max() - im.min())) * 255)
            img = Image.fromarray(im)
            img = img.convert("L")
            img.save(os.path.join(output_dir, filename.split(".")[0] + "_slice" + str(i) + ".png"))
            
        # print(f"{filename} processed and saved as PNGs")