import SimpleITK as sitk
import vtk
import nibabel as nib
# Load the NIfTI image using SimpleITK
path='ADNI_002_S_0729_MR_MPR__GradWarp__B1_Correction__N3__Scaled_Br_20070217001935821_S16874_I40708.nii'




# Load the Nifti image
# reader = vtk.vtkNIFTIImageReader()
# reader.SetFileName(path)
# reader.Update()

# # Convert the Nifti image to a VTK image
# vtk_image = vtk.vtkImageData()
# vtk_image.DeepCopy(reader.GetOutput())

# # Write the VTK image to file
# writer = vtk.vtkXMLImageDataWriter()
# writer.SetFileName("ADNI.vti")
# writer.SetInputData(vtk_image)
# writer.Write()



# # Read the VTK image from file
# reader = vtk.vtkXMLImageDataReader()
# reader.SetFileName("ADNI.vti")
# reader.Update()

# # Get the scalar range of the image data
# scalar_range = reader.GetOutput().GetScalarRange()

# # Create a volume mapper and actor
# mapper = vtk.vtkSmartVolumeMapper()
# mapper.SetInputData(reader.GetOutput())
# actor = vtk.vtkVolume()
# actor.SetMapper(mapper)

# # Create a transfer function to map scalar values to opacity
# opacity_tf = vtk.vtkPiecewiseFunction()
# opacity_tf.AddPoint(scalar_range[0], 0.0)
# opacity_tf.AddPoint(scalar_range[1], 1.0)

# # Create a transfer function to map scalar values to color
# color_tf = vtk.vtkColorTransferFunction()
# color_tf.AddRGBPoint(scalar_range[0], 1.0, 1.0, 1.0)
# color_tf.AddRGBPoint(scalar_range[1], 1.0, 1.0, 1.0)

# # Create a volume property and set the transfer functions
# volume_property = vtk.vtkVolumeProperty()
# volume_property.SetScalarOpacity(opacity_tf)
# volume_property.SetColor(color_tf)
# volume_property.ShadeOn()
# volume_property.SetInterpolationTypeToLinear()

# # Set the volume property on the actor
# actor.SetProperty(volume_property)

# # Create a renderer, render window, and interactor
# renderer = vtk.vtkRenderer()
# render_window = vtk.vtkRenderWindow()
# render_window.AddRenderer(renderer)
# interactor = vtk.vtkRenderWindowInteractor()
# interactor.SetRenderWindow(render_window)

# # Add the actor to the renderer, set background color, and render
# renderer.AddVolume(actor)
# renderer.SetBackground(0.1, 0.2, 0.4)
# render_window.Render()

# # Start the interactor
# interactor.Start()

import vtk

# Read the VTI file
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("ADNI.vti")
reader.Update()

# Create a transfer function to map scalar values to colors and opacities
color_func = vtk.vtkColorTransferFunction()
color_func.AddRGBPoint(0, 0.0, 0.0, 0.0)
color_func.AddRGBPoint(255, 1.0, 1.0, 1.0)

opacity_func = vtk.vtkPiecewiseFunction()
opacity_func.AddPoint(0, 0.0)
opacity_func.AddPoint(255, 1.0)

# Create a volume property to control the rendering of the volume
volume_property = vtk.vtkVolumeProperty()
volume_property.SetColor(color_func)
volume_property.SetScalarOpacity(opacity_func)
volume_property.SetInterpolationTypeToLinear()

# Create a volume mapper to render the volume
volume_mapper = vtk.vtkSmartVolumeMapper()
volume_mapper.SetInputConnection(reader.GetOutputPort())

# Create a volume actor to represent the volume in the scene
volume_actor = vtk.vtkVolume()
volume_actor.SetMapper(volume_mapper)
volume_actor.SetProperty(volume_property)

# Create a renderer and add the volume actor to it
renderer = vtk.vtkRenderer()
renderer.AddActor(volume_actor)

# Create a render window and set the renderer to it
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

# Create an interactor to handle user events
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Set the background color of the renderer
renderer.SetBackground(0.1, 0.1, 0.2)

# Set the camera position and focal point
camera = renderer.GetActiveCamera()
camera.SetPosition(-500, 0, 0)
camera.SetFocalPoint(0, 0, 0)

# Reset the camera and render the scene
renderer.ResetCamera()
render_window.Render()

# Start the interactor loop
interactor.Start()
