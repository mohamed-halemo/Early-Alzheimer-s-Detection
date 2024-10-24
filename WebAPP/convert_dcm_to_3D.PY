import os
import numpy as np
import pydicom
from vtk.util import numpy_support
import vtk

# Step 1: Load the DICOM files
dicom_dir = 'conversion'
dicom_files = sorted([os.path.join(dicom_dir, f) for f in os.listdir(dicom_dir) if f.endswith('.dcm')])
dicom_data = [pydicom.read_file(f,force=True) for f in dicom_files]

# Step 2: Sort the DICOM files
dicom_data.sort(key=lambda x: x.ImagePositionPatient[2])

# Step 3: Create a 3D volume
voxel_ndarray = np.stack([np.array(dcm.pixel_array) for dcm in dicom_data])
spacing = np.array([dicom_data[0].PixelSpacing[0], dicom_data[0].PixelSpacing[1], dicom_data[0].SliceThickness])
origin = np.array(dicom_data[0].ImagePositionPatient)
image = vtk.vtkImageData()
image.SetDimensions(voxel_ndarray.shape)
image.SetSpacing(spacing)
image.SetOrigin(origin)
voxel_array = numpy_support.numpy_to_vtk(voxel_ndarray.ravel(), deep=True, array_type=vtk.VTK_UNSIGNED_SHORT)
image.GetPointData().SetScalars(voxel_array)

# Step 4: Visualize the 3D volume
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
ren.SetBackground(0.1, 0.2, 0.4)

volumeMapper = vtk.vtkSmartVolumeMapper()
volumeMapper.SetInputData(image)
volumeMapper.SetBlendModeToComposite()
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()
colorFunc = vtk.vtkColorTransferFunction()
colorFunc.AddRGBPoint(-1000, 0.0, 0.0, 0.0)
colorFunc.AddRGBPoint(0, 1.0, 1.0, 1.0)
colorFunc.AddRGBPoint(1000, 1.0, 0.0, 0.0)
volumeProperty.SetColor(colorFunc)
opacityFunc = vtk.vtkPiecewiseFunction()
opacityFunc.Add
