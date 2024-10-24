from flask import Flask, render_template, request
import nibabel as nib
import os
import pydicom

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['nifti_file']
    filename = file.filename
    file.save(filename)
    nifti_image = nib.load(filename)
    image_data = nifti_image.get_fdata()
    image_min = image_data.min()
    image_max = image_data.max()
    image_scaled = (image_data - image_min) / (image_max - image_min) * 255
    image_scaled = image_scaled.astype('uint8')
    
    # Create a DICOM dataset and set required fields
    ds = pydicom.dataset.Dataset()
    ds.PatientName = "Anonymous"
    ds.PatientID = "000000"
    ds.Modality = "MR"
    ds.SeriesDescription = "NIfTI to DICOM conversion"
    ds.ContentDate = pydicom.valuerep.Date()
    ds.ContentTime = pydicom.valuerep.Time()
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    ds.Rows, ds.Columns, ds.NumberOfFrames = image_scaled.shape
    ds.PixelData = image_scaled.tobytes()
    ds.file_meta = pydicom.FileMetaDataset()
    ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
    
    # Save the DICOM file
    dicom_filename = os.path.splitext(filename)[0] + '.dcm'
    pydicom.filewriter.dcmwrite(dicom_filename, ds)
    
    return render_template('upload.html', dicom_filename=dicom_filename)

if __name__ == '__main__':
    app.run(debug=True)
