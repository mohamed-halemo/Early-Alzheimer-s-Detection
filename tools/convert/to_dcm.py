import os
import numpy as np
import pydicom
from nibabel import load
import re
def convertNsave(arr,file_dir, index=0):
    """
    `arr`: parameter will take a numpy array that represents only one slice.
    `file_dir`: parameter will take the path to save the slices
    `index`: parameter will represent the index of the slice, so this parameter will be used to put 
    the name of each slice while using a for loop to convert all the slices
    """
    
    dicom_file = pydicom.dcmread('vhf.1502.dcm')
    arr = arr.astype('uint16')
    # arr = np.uint16(arr * (2**16-1) / np.max(arr))  

    dicom_file.Rows = arr.shape[0]
    dicom_file.Columns = arr.shape[1]
    dicom_file.PhotometricInterpretation = "MONOCHROME2"
    dicom_file.SamplesPerPixel = 1
    dicom_file.BitsStored = 16
    dicom_file.BitsAllocated = 16
    dicom_file.HighBit = 15
    dicom_file.PixelRepresentation = 0
    dicom_file.PixelData = arr.tobytes()
    dicom_file.save_as(os.path.join(file_dir, f'slice{index}.dcm'))

# Path to the NIfTI file 
def ConvertNIFTI(nifti_file, axis):
    # Load the NIfTI image data
    img = load(nifti_file)
    header = img.header
    # # Get the image dimensions and voxel size
    dims = img.header.get_zooms()[:3]
    spacing = np.array(img.header.get_zooms()[:3])
    spacing = np.append(spacing, 0)
  
    # # Create the DICOM header
    study=re.search(r"S\d+",nifti_file)
    study= study.group()
    study=study.replace("S","")
    Series=re.search(r"I\d+",nifti_file)
    series=Series.group()
    series=series.replace("I","")

    parent_directory='E:/GP/Brain/To_DCM/output'
    Patient_id=re.search(r"ADNI_\d+_S_\d+",nifti_file)
    Patient_id=Patient_id.group()
    Patient_id=Patient_id.replace("ADNI","")
    main_folder_name=Patient_id.replace("_","",1)

    secondary_folder_name=study
    axis_name=axis
    path=os.path.join(parent_directory,main_folder_name)
    # path=main_folder_name

    if axis_name == "axial":
        os.mkdir(path)
    path2=os.path.join(path,secondary_folder_name)
    if axis_name == "axial":
        os.mkdir(path2)
    path3=os.path.join(path2,axis_name)
    os.mkdir(path3)
    # Create a list of DICOM files
    # ornt2 = np.array([[2,-1],
    #                 [1, -1],
    #                 [0, -1]])
    # ornt3 = np.array([[1,1],
    #                 [0, 1],
    #                 [2, 1]])

    if axis_name == "axial":
        # img = img.as_reoriented(ornt2)
        # img = img.as_reoriented(ornt3)

        nifti_array = img.get_fdata()
        number_slices = nifti_array.shape[2]


        for slice_ in (range(number_slices)):
            convertNsave(nifti_array[:,:,slice_], path3, slice_)


    # Loop through the NIfTI slices and convert each one to a DICOM file
    elif axis_name == "coronal":
        # img = img.as_reoriented(ornt2)
        # img = img.as_reoriented(ornt3)

        nifti_array = img.get_fdata()
        number_slices = nifti_array.shape[1]


        for slice_ in (range(number_slices)):
            convertNsave(nifti_array[:,slice_,:], path3, slice_)

    elif axis_name == "sagittal":
        # img = img.as_reoriented(ornt2)
        # img = img.as_reoriented(ornt3)

        nifti_array = img.get_fdata()
        number_slices = nifti_array.shape[0]


        for slice_ in (range(number_slices)):
            convertNsave(nifti_array[slice_,:,:], path3, slice_)


ConvertNIFTI('ADNI_023_S_0042_MR_MPR-R__GradWarp__B1_Correction__N3__Scaled_Br_20061130173634563_S8852_I31084.nii','sagittal')