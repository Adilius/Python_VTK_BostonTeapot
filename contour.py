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

# Create volume mapper
volumeMap = vtk.vtkSmartVolumeMapper()
volumeMap.SetInputData(reader.GetOutput())

# Create volume
volume = vtk.vtkVolume()
volume.SetMapper(volumeMap)

# Create contour filter using reader
contour = vtk.vtkContourFilter()
contour.SetInputConnection(reader.GetOutputPort())
contour.GenerateValues(20, 0, 255)   # numContours, rangeStart, rangeEnd

# Create mapper using contour filter
modelToContour = vtk.vtkPolyDataMapper()
modelToContour.SetInputConnection(contour.GetOutputPort())

# Create contour actor using mapper
contourActor = vtk.vtkActor()
contourActor.SetMapper(modelToContour)

# Window
window = vtk.vtkRenderWindow()
window.SetSize(1000, 1000)
interactor = vtk.vtkRenderWindowInteractor()

# contour
renderer = vtk.vtkRenderer()
renderer.SetBackground(.2, .2, .2 ) #Change background color
renderer.AddActor(contourActor)
window.AddRenderer(renderer)

# Start
interactor.SetRenderWindow(window)
window.Render()
interactor.Start()