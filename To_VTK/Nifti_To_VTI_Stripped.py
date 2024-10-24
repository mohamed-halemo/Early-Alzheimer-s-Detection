import SimpleITK as sitk
import vtk
import nibabel as nib
# Load the NIfTI image using SimpleITK
path='E:/GP/Data_Classes/ADAD/002_S_0619/ADNI_002_S_0619_MR_MIDAS_Whole_Brain_Mask_Br_20120802025539470_S15145_I320896.nii'

reader = vtk.vtkNIFTIImageReader()
reader.SetFileName(path)
reader.Update()
print (reader)

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

#save .vtk polydata
writer = vtk.vtkXMLPolyDataWriter()
# writer.SetFileTypeToASCII()
writer.SetInputConnection(contour.GetOutputPort())
writer.SetFileName("Whole_brain.vti")
writer.Write()


##############

# Load the VTK file
reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName('Whole_brain.vti')
reader.Update()

# Create mapper and actor
mapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(reader.GetOutput())
else:
    mapper.SetInputConnection(reader.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

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
