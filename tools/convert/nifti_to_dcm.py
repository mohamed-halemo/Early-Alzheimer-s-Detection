import os
import glob
import numpy as np
import pydicom
from nibabel import load

# Path to the NIfTI file
nifti_file = "E:/GP/Data_Classes/CN/002_S_0295/ADNI_002_S_0295_MR_MIDAS_Whole_Brain_Mask_Br_20120214130507765_S13408_I284658.nii"

# Load the NIfTI image data
img = load(nifti_file)

# Get the image dimensions and voxel size
dims = img.header.get_zooms()[:3]
spacing = np.array(img.header.get_zooms()[:3])
spacing = np.append(spacing, 0)

# Create the DICOM header
dcm = pydicom.dataset.FileDataset('', {}, file_meta=pydicom.dataset.FileMetaDataset())
dcm.PatientName = "Anonymous"
dcm.PatientID = "12345"
dcm.Modality = "MR"
dcm.SeriesInstanceUID = pydicom.uid.generate_uid()
dcm.StudyInstanceUID = pydicom.uid.generate_uid()
dcm.SOPInstanceUID = pydicom.uid.generate_uid()
dcm.Rows = img.shape[0]
dcm.Columns = img.shape[1]
dcm.PixelSpacing = spacing.tolist()
dcm.SliceThickness = dims[2]
dcm.ImageOrientationPatient = [1,0,0,0,1,0]
dcm.ImagePositionPatient = [0,0,0]
dcm.BitsAllocated = 16
dcm.BitsStored = 16
dcm.HighBit = 15
dcm.SamplesPerPixel = 1
dcm.PhotometricInterpretation = "MONOCHROME2"
dcm.PixelRepresentation = 1
dcm.RescaleSlope = 1.0
dcm.RescaleIntercept = 0.0
dcm.WindowCenter = img.get_data().mean()
dcm.WindowWidth = img.get_data().max() - img.get_data().min()
dcm.LossyImageCompression = '01'

# Create a list of DICOM files
dcm_files = []

# Loop through the NIfTI slices and convert each one to a DICOM file
for i in range(img.shape[2]):
    # Get the NIfTI slice data
    slice_data = img.get_data()[:, :, i]
    
    # Convert the data type to unsigned integer
    slice_data = np.uint16(slice_data)
    
    # Set the image data and slice location in the DICOM header
    dcm.PixelData = slice_data.tobytes()
    dcm.SliceLocation = i*dims[2]
    
    # Set the file name for the DICOM file
    dcm_file = f"dicom_{i:04}.dcm"
    
    # Save the DICOM file
    pydicom.filewriter.dcmwrite(dcm_file, dcm)
    
    # Add the DICOM file to the list of files
    dcm_files.append(dcm_file)

# Create a DICOM series directory
series_dir = "E:\GP\Brain\Dicom"
os.makedirs(series_dir, exist_ok=True)

# Save the DICOM files to the series directory
for dcm_file in dcm_files:
    os.rename(dcm_file, os.path.join(series_dir, dcm_file))
