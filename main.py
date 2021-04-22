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

#Colors
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.SetColorSpaceToRGB()  #Useless?
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)   #First point, all black
colorTransferFunction.AddRGBPoint(86.0, 1.0, 0.0, 0.0)  #One third points, all red
colorTransferFunction.AddRGBPoint(172.0, 0.0, 1.0, 0.0) #Two thirds points, all green
colorTransferFunction.AddRGBPoint(255.0, 0.0, 0.0, 1.0) #Three thirds points, all blue

#Mapper pushes geomtry into graphics library, color mapping with scalar attributes.
cubeMapper = vtk.vtkPolyDataMapper()                    #Creates mapper
cubeMapper.SetInputConnection(reader.GetOutputPort())   #Clears and specifies a single connection to the port
cubeMapper.SetLookupTable(colorTransferFunction)        #Sets color lookup table

#Opacity
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(0, 0.0)    #Add lowest opacity
opacityTransferFunction.AddPoint(255, 0.4)  #Add highest opacity

#Volume property
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOn()


#Volume mapper
volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
volumeMapper.SetBlendModeToComposite()
volumeMapper.SetInputConnection(reader.GetOutputPort())

# Setup color mapping bar
colorBar = vtk.vtkScalarBarActor()
colorBar.SetLookupTable(cubeMapper.GetLookupTable())
colorBar.SetTitle("Colormap")
colorBar.SetNumberOfLabels(0)
colorBar.SetLabelFormat("%6.0f")
colorBar.SetPosition(0.9, 0.1)
colorBar.SetWidth(0.08)
colorBar.SetHeight(0.5)

#Set volume
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

#Create renderer
ren = vtk.vtkRenderer()
ren.AddVolume(volume)
ren.AddActor(colorBar)

#Create window
window = vtk.vtkRenderWindow()
window.SetSize(1000,1000)
window.AddRenderer(ren)

#Create interactor that captures mouse interactions with window
interactor = vtk.vtkRenderWindowInteractor()    #Create
interactor.SetRenderWindow(window)              #Add

#Start renderer & interactor
window.Render()
interactor.Initialize()
interactor.Start()