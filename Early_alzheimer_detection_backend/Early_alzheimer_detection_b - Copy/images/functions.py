import os
import numpy as np
import pydicom
from nibabel import load
import re
import vtk
import nibabel as nib
import glob
from PIL import Image
from tensorflow import keras 

# Load the NIfTI image using SimpleITK
def cropping(img):
    if np.count_nonzero(img) == 0:
        return img
    xs, ys = np.where(img != 0)
    result = img[min(xs):max(xs) + 1, min(ys):max(ys) + 1]
    return result
def find_matching_file_Slices_and_predict(input_path, root_folder):
    # Get the base name of the input image file
    input_filename = os.path.basename(input_path)
    ornt = np.array([[0,-1],
                [1, 1],
                [2, 1]])

    ornt2 = np.array([[2,-1],
                    [1, -1],
                    [0, -1]])
    # Traverse the specified root folder and search for matching file names
    for folder in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder)
        if not os.path.isdir(folder_path):
            continue

        for case_folder in os.listdir(folder_path):
            case_folder_path = os.path.join(folder_path, case_folder)
            if not os.path.isdir(case_folder_path):
                continue

            case_files = glob.glob(os.path.join(case_folder_path, '*.nii'))
            matching_files = [f for f in case_files if input_filename in f]
            
            # Process matching files
            if matching_files:
                for matching_file in matching_files:
                    image=nib.load(matching_file)
                    image = image.as_reoriented(ornt2)
                    # Read the other two files in the case folder
                    case_files.remove(matching_file)
                    for other_file in case_files:
                        if 'Hippocampal' in other_file:
                            Hippocampal=nib.load(other_file)
                            Hippocampal = Hippocampal.as_reoriented(ornt)
                        else :
                            whole_mask=nib.load(other_file)
                            whole_mask = whole_mask.as_reoriented(ornt2)
    skull_stripped=skull_stripping(image,whole_mask)
    Slices=Hippo_slices(skull_stripped,Hippocampal)
    Precentage=Predict(Slices)
    return Precentage

def Hippo_slices(image,hippo_mask):
    #Getting image data
    image_data = image
    mask_data = hippo_mask.get_fdata()
    #specifiying slices
    x_slices, y_slices, z_slices =  np.where(mask_data!=0)
    slices_arr=[]
        # Process and save each slice as PNG
    for i in range(z_slices.min(), z_slices.max()+1):
        im = np.asarray(image_data[:, :, i])
        im = cropping(im)
        im = np.abs(((im - im.min()) / (im.max() - im.min())) * 255)
        img = Image.fromarray(im)
        img = img.convert("L")
        slices_arr.append(img)
        # img.save(os.path.join( "_slice" + str(i) + ".png"))

    return slices_arr

def skull_stripping(image,whole_brain_mask):
    #Getting image data
    image_data = image.get_fdata()
    mask_data = whole_brain_mask.get_fdata()
    #skull stripping 
    skull_stripped=image_data*mask_data
    return skull_stripped

def preprocess_images(image_list, target_size=(150, 150)):
    # Create an empty array to store the preprocessed images
    num_images = len(image_list)
    images = np.empty((num_images,) + target_size, dtype=np.float32)

    # Resize and convert each image to an array
    for i, image in enumerate(image_list):
        image = image.resize(target_size)
        image_array = np.array(image, dtype=np.float32)
        images[i] = image_array
       
    # Normalize the pixel values to the range [0, 1]
    images /= 255.0

    # Expand dimensions to match expected input shape (150, 150, 3)
    images = np.expand_dims(images, axis=-1)
    images = np.repeat(images, 3, axis=-1)

    return images
def Predict(Slices):
    #Load the model
    model = keras.models.load_model('./images/best_test_acc_VGG16(98.17%).h5',compile=False)
    #Preprocess the image to match the model
    Slices=preprocess_images(Slices)
    #predict
    prediction=model.predict(Slices)
    # prediction=model.predict(Slices).argmax(axis=1)
    Precentage=calculate_class_percentage(prediction)
    return Precentage

def calculate_class_percentage(predictions):
    # Convert predictions to a NumPy array 
    predictions_array = np.array(predictions)

    # Calculate the total number of predictions
    total_predictions = predictions_array.shape[0]
    # Calculate the sum of probabilities for each class
    class_probabilities_sum = np.sum(predictions_array, axis=0)

    # Calculate the percentages for each class
    class_percentages = (class_probabilities_sum / (total_predictions)) * 100

    class_labels = ['AD', 'CN', 'MCI']

    class_percentages_dict = {label: percentage for label, percentage in zip(class_labels, class_percentages)}

    # Create a dictionary to store the class percentages
    return class_percentages_dict



def ConvertToVTI(nifti_file):
    # Load the Nifti image
    reader = vtk.vtkNIFTIImageReader()

    folder_path=os.path.join("D:\\Graduation_project\\Dataset\\AD_stripped", nifti_file[2:])
    
    if not os.path.isfile(folder_path):
        folder_path= os.path.join("D:\\Graduation_project\\Dataset\\CN_stripped", nifti_file[2:])
        if not os.path.isfile(folder_path):
            folder_path= os.path.join("D:\\Graduation_project\\Dataset\\MCI_stripped", nifti_file[2:])   
    reader.SetFileName(folder_path)

    reader.Update()
    parent_directory='D:\\Graduation_project\\Github\\Early_alzheimer_detection_f\\public'
    # Convert the Nifti image to a VTK image
    vtk_image = vtk.vtkImageData()
    vtk_image.DeepCopy(reader.GetOutput())
    file_name= os.path.join(parent_directory , nifti_file)
    # Write the VTK image to file
    file_name = file_name.replace(".nii",".vti")
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName(file_name)
    writer.SetInputData(vtk_image)
    writer.Write()




def convertNsave(arr,file_dir, index=0,window_center=None,window_width=None):
    """
    `arr`: parameter will take a numpy array that represents only one slice.
    `file_dir`: parameter will take the path to save the slices
    `index`: parameter will represent the index of the slice, so this parameter will be used to put 
    the name of each slice while using a for loop to convert all the slices
    """
    
    dicom_file = pydicom.dcmread('./images/vhf.1502.dcm')
    epsilon = 1e-12
    min_value = (window_center+50) - 0.5 * (window_width+100)
    max_value = (window_center+50) + 0.5 * (window_width+100)
    # arr = np.clip(arr, min_value, max_value)
    arr = ((arr - (arr.min())) / (arr.max() - (arr.min()+ epsilon))) * 1400+window_width
    # print(max_value)
    arr = arr.astype("uint16")
  
 
    # arr = np.clip(arr, min_value, max_value)

    dicom_file.Rows = arr.shape[0]
    dicom_file.Columns = arr.shape[1]
    # dicom_file.PhotometricInterpretation = "MONOCHROME2"
    dicom_file.SamplesPerPixel = 1
    dicom_file.BitsStored = 16
    dicom_file.BitsAllocated = 16
    dicom_file.HighBit = 15
    dicom_file.PixelRepresentation = 0

    dicom_file.PixelData = arr.tobytes()
    dicom_file.WindowCenter = 0+window_center
    dicom_file.WindowWidth = 1400+window_width
    
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

    parent_directory='D:\\Graduation_project\\Github\\Early_alzheimer_detection_f\\public'
    Patient_id=re.search(r"ADNI_\d+_S_\d+",nifti_file)
    Patient_id=Patient_id.group()
    Patient_id=Patient_id.replace("ADNI","")
    main_folder_name=Patient_id.replace("_","",1)

    secondary_folder_name=study
    axis_name=axis
    path=os.path.join(parent_directory,main_folder_name)
    # path=main_folder_name

    if axis_name == "axial":
        try:
            os.mkdir(path)
        except:
            print("Same patient")
    path2=os.path.join(path,secondary_folder_name)
    if axis_name == "axial":
        os.mkdir(path2)
    path3=os.path.join(path2,axis_name)
    os.mkdir(path3)
    # Create a list of DICOM files
    ornt2 = np.array([[2,-1],
                    [1, -1],
                    [0, -1]])
    ornt3 = np.array([[1,1],
                    [0, 1],
                    [2, 1]])

    if axis_name == "axial":
        img = img.as_reoriented(ornt2)
        img = img.as_reoriented(ornt3)

        nifti_array = img.get_fdata()
        number_slices = nifti_array.shape[2]


        for slice_ in (range(number_slices)):
            convertNsave(nifti_array[:,:,slice_], path3, slice_,window_center=slice_,window_width=slice_)


    # Loop through the NIfTI slices and convert each one to a DICOM file
    elif axis_name == "coronal":
        # img = img.as_reoriented(ornt2)
        img = img.as_reoriented(ornt3)

        nifti_array = img.get_fdata()
        number_slices = nifti_array.shape[0]


        for slice_ in (range(number_slices)):
            convertNsave(nifti_array[slice_,:,:], path3, slice_,window_center=slice_,window_width=slice_)

    elif axis_name == "sagittal":
        img = img.as_reoriented(ornt2)
        img = img.as_reoriented(ornt3)
        img = img.as_reoriented(ornt2)

        nifti_array = img.get_fdata()
        number_slices = nifti_array.shape[1]


        for slice_ in (range(number_slices)):
            convertNsave(nifti_array[:,slice_,:], path3, slice_,window_center=slice_,window_width=slice_)
        