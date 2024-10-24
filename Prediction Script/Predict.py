import os
import glob
import nibabel as nib
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
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
                    print('Match found:', matching_file)
                    image=nib.load(matching_file)
                    image = image.as_reoriented(ornt2)
                    # Read the other two files in the case folder
                    case_files.remove(matching_file)
                    for other_file in case_files:
                        print('Other file:', other_file)
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

    print(slices_arr)
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
    model = load_model('best_test_acc_VGG16(98.17%).h5',compile=False)
    #Preprocess the image to match the model
    Slices=preprocess_images(Slices)
    #predict
    prediction=model.predict(Slices)
    # prediction=model.predict(Slices).argmax(axis=1)
    print(prediction)
    Precentage=calculate_class_percentage(prediction)
    return Precentage

def calculate_class_percentage(predictions):
    # Convert predictions to a NumPy array 
    predictions_array = np.array(predictions)
    print(predictions)
    # Calculate the total number of predictions
    total_predictions = predictions_array.shape[0]
    print(total_predictions)
    # Calculate the sum of probabilities for each class
    class_probabilities_sum = np.sum(predictions_array, axis=0)
    print(class_probabilities_sum)
    # Calculate the percentages for each class
    class_percentages = class_probabilities_sum / total_predictions * 100
    print(np.sum(class_percentages))
    class_labels = ['AD', 'CN', 'MCI']

    class_percentages_dict = {label: percentage for label, percentage in zip(class_labels, class_percentages)}

    # Create a dictionary to store the class percentages
    # print(class_percentages_dict)
    return class_percentages_dict
# Specify the input image path and root folder
input_image_path = 'ADNI_002_S_0938_MR_MPR__GradWarp__B1_Correction__N3__Scaled_Br_20071110105158515_S41834_I81312.nii'
root_folder = 'E:/GP/Data_Classes'
# Call the function
prcentage=find_matching_file_Slices_and_predict(input_image_path, root_folder)
print(prcentage)

