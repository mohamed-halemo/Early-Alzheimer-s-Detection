import SimpleITK as sitk
import vtk
import nibabel as nib
# Load the NIfTI image using SimpleITK
path='E:/GP/Data_Classes/ADAD/002_S_0938/ADNI_002_S_0938_MR_MPR__GradWarp__B1_Correction__N3__Scaled_Br_20071110105158515_S41834_I81312.nii'




# Load the Nifti image
reader = vtk.vtkNIFTIImageReader()
reader.SetFileName(path)
reader.Update()

# Convert the Nifti image to a VTK image
vtk_image = vtk.vtkImageData()
vtk_image.ShallowCopy(reader.GetOutput())

# Write the VTK image to file
writer = vtk.vtkXMLImageDataWriter()
writer.SetFileName("file.vti")
writer.SetInputData(vtk_image)
writer.Write()



# Read the VTK image from file
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("file.vti")
reader.Update()

# Get the scalar range of the image data
scalar_range = reader.GetOutput().GetScalarRange()

# Create a volume mapper and actor
mapper = vtk.vtkSmartVolumeMapper()
mapper.SetInputData(reader.GetOutput())
actor = vtk.vtkVolume()
actor.SetMapper(mapper)

# Create a transfer function to map scalar values to opacity
opacity_tf = vtk.vtkPiecewiseFunction()
opacity_tf.AddPoint(scalar_range[0], 0.0)
opacity_tf.AddPoint(scalar_range[1], 1.0)

# Create a transfer function to map scalar values to color
color_tf = vtk.vtkColorTransferFunction()
color_tf.AddRGBPoint(scalar_range[0], 1.0, 1.0, 1.0)
color_tf.AddRGBPoint(scalar_range[1], 1.0, 1.0, 1.0)

# Create a volume property and set the transfer functions
volume_property = vtk.vtkVolumeProperty()
volume_property.SetScalarOpacity(opacity_tf)
volume_property.SetColor(color_tf)
volume_property.ShadeOn()
volume_property.SetInterpolationTypeToLinear()

# Set the volume property on the actor
actor.SetProperty(volume_property)

# Create a renderer, render window, and interactor
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Add the actor to the renderer, set background color, and render
renderer.AddVolume(actor)
renderer.SetBackground(0.1, 0.2, 0.4)
render_window.Render()

# Start the interactor
interactor.Start()

