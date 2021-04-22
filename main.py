# Verify that we are running right python version
import sys
print("Python " + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]))

import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

# Read raw dataset
reader = vtk.vtkImageReader() #Declare new Image Reader object
reader.SetDataScalarType(vtk.VTK_UNSIGNED_CHAR) #Unsigned char
reader.SetFileName('BostonTeapot.raw')
reader.SetDataByteOrderToBigEndian()
reader.SetNumberOfScalarComponents(1)
reader.SetFileDimensionality(3)
reader.SetDataExtent(0, 255, 0, 255, 0, 177)
reader.SetDataScalarTypeToUnsignedChar()
reader.Update()

#Mapper pushes geomtry into graphics library, color mapping with scalar attributes.
cubeMapper = vtk.vtkPolyDataMapper()
cubeMapper.SetInputConnection(reader.GetOutputPort())   #Clears and specifies a single connection to the port

#Opacity
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(20, 0.0)
opacityTransferFunction.AddPoint(255, 0.2)

#Color
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(255.0, 0.0, 0.2, 0.0)
colorTransferFunction.AddRGBPoint(255.0, 0.0, 0.2, 0.0)
colorTransferFunction.AddRGBPoint(255.0, 0.2, 0.0, 0.0)


#Volume property
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOn()


#Volume mapper
volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
volumeMapper.SetBlendModeToComposite()
volumeMapper.SetInputConnection(reader.GetOutputPort())

#Set volume
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

#Create renderer
ren = vtk.vtkRenderer()
ren.AddVolume(volume)

#Create window
window = vtk.vtkRenderWindow()
window.SetSize(1000,1000)
window.AddRenderer(ren)

#Create interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

#Start renderer & interactor
window.Render()
interactor.Initialize()
interactor.Start()