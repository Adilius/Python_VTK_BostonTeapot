# Verify that we are running right python version
import sys
print("Python " + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]))

import vtk
from vtkmodules.vtkRenderingCore import vtkColorTransferFunction

# Read raw dataset
reader = vtk.vtkImageReader() #Declare new Image Reader object
reader.SetFileName('BostonTeapot.raw')
reader.SetDataByteOrderToBigEndian()
reader.SetNumberOfScalarComponents(1)
reader.SetFileDimensionality(3)
reader.SetDataExtent(0, 255, 0, 255, 0, 177)
reader.SetDataScalarTypeToUnsignedChar()
reader.Update()

# Create volume mapper using reader 
volumeMap = vtk.vtkSmartVolumeMapper()
volumeMap.SetInputData(reader.GetOutput())

# Create volume using volume mapper
volume = vtk.vtkVolume()
volume.SetMapper(volumeMap)

# Filter
contour = vtk.vtkContourFilter()
contour.SetInputConnection(reader.GetOutputPort())
contour.GenerateValues(10, 0, 255)   # numContours (sensitivity), rangeStart, rangeEnd

# Create plane
plane = vtk.vtkPlane()
plane.SetOrigin(60, 0, 0)   # Changes the clip plane
plane.SetNormal(1, -1.0, 1) # somehow

# Create clip
clip = vtk.vtkClipPolyData()
clip.SetInputConnection(contour.GetOutputPort())
clip.SetClipFunction(plane)

# Mapper
contourToSlice = vtk.vtkPolyDataMapper()
contourToSlice.SetInputConnection(clip.GetOutputPort())

# Create Actor
clipActor = vtk.vtkActor()
clipActor.SetMapper(contourToSlice)

# Renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(.2, .2, .2 ) #Change background color
renderer.AddActor(clipActor)

# Window
window = vtk.vtkRenderWindow()
window.SetSize(1000, 1000)
window.AddRenderer(renderer)
window.Render()

# Interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)
interactor.Start()