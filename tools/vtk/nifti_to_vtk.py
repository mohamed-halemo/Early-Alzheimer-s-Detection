import SimpleITK as sitk
import vtk
# Load the NIfTI image using SimpleITK
path_face='E:/GP/Data_Classes/ADAD/002_S_0938/ADNI_002_S_0938_MR_MPR__GradWarp__B1_Correction__N3__Scaled_Br_20071110105158515_S41834_I81312.nii'
path_stripped='E:/GP/Data_Classes/ADAD/002_S_0619/ADNI_002_S_0619_MR_MIDAS_Whole_Brain_Mask_Br_20120802025539470_S15145_I320896.nii'
path_hippo='E:/GP/Data_Classes/ADAD/002_S_0619/ADNI_002_S_0619_MR_Hippocampal_Mask_Hi_20080228111542738_S15145_I93333.nii'
path_output="Whole_brain.vti"

def Nifti_Reader(path):
 # Load the Nifti image
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(path)
    reader.Update()
    return reader

def Read_Stripped_Or_Hippo(path):
    reader=Nifti_Reader(path)

    contour=vtk.vtkMarchingCubes()  
    contour.SetInputData(reader.GetOutput())
    contour.ComputeNormalsOn()
    contour.ComputeGradientsOn()
    contour.SetValue(0,0.1)
    contour.Update()
    
    # Write in vtk
    triangle = vtk.vtkTriangleFilter()
    triangle.SetInputConnection(contour.GetOutputPort())
    triangle.PassVertsOff()
    triangle.PassLinesOff()
    
    decimation=vtk.vtkQuadricDecimation()
    decimation.SetInputConnection(triangle.GetOutputPort())
    
    clean=vtk.vtkCleanPolyData()
    clean.SetInputConnection(triangle.GetOutputPort())
    
    triangle2 = vtk.vtkTriangleFilter()
    triangle2.SetInputConnection(clean.GetOutputPort())
    triangle2.PassVertsOff()
    triangle2.PassLinesOff()
    
    if "Whole" or "whole" in path:
        #save .vtk polydata
        output='Whole_brain.vti'
        writer = vtk.vtkXMLPolyDataWriter()
        # writer.SetFileTypeToASCII()
        writer.SetInputConnection(contour.GetOutputPort())
        writer.SetFileName(output)
    else:
        output='Hippo.vti'
        writer = vtk.vtkPolyDataWriter()
        writer.SetFileTypeToASCII()
        writer.SetInputConnection(contour.GetOutputPort())
        writer.SetFileName(output)
    writer.Write()
    return output


def Reader_Full_Face(path):
    reader=Nifti_Reader(path)
    # Convert the Nifti image to a VTK image
    vtk_image = vtk.vtkImageData()
    vtk_image.ShallowCopy(reader.GetOutput())
    # Write the VTK image to file
    writer = vtk.vtkXMLImageDataWriter()
    output='Face.vti'
    writer.SetFileName(output)
    writer.SetInputData(vtk_image)
    writer.Write()
    return output

def Visualize_Stripped_Or_Hippo(path):
    print(path)
    # Load the VTK file

    if "Whole" or "whole" in path:
        print("hi")
        reader = vtk.vtkXMLPolyDataReader()
        reader.SetFileName('Whole_brain.vti')   
    else:
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName('Hippo.vti')
        print("Hippo")
    reader.Update()
    
    # Create mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(reader.GetOutput())
    else:
        mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    

    actor.GetProperty().SetColor(0,1,0)  # set opacity to 50%
    actor.GetProperty().SetOpacity(0.3)  # set opacity to 50%
    # Create renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Set camera position and focal point
    camera = renderer.GetActiveCamera()
    camera.SetPosition(0, 0, -300)  # Move the camera behind the brain
    camera.SetFocalPoint(0, 0, 0)  # Set the focal point to the center of the brain

    # Reset camera and render
    renderer.ResetCamera()
    renderWindow.Render()

    # Start the interactor
    renderWindowInteractor.Start()

def Visualize_Full(path):
    # Read the VTK image from file
    reader = vtk.vtkXMLImageDataReader()

    reader.SetFileName(path)
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


# Read_Stripped_Or_Hippo(path_stripped)
Visualize_Stripped_Or_Hippo(path_output)