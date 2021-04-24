# Verify that we are running right python version
import sys
print("Python " + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]))

import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

# Read raw dataset
reader = vtk.vtkImageReader() #Declare new Image Reader object
reader.SetFileName('BostonTeapot.raw')
reader.SetDataByteOrderToBigEndian()
reader.SetNumberOfScalarComponents(1)
reader.SetFileDimensionality(3)
reader.SetDataExtent(0, 255, 0, 255, 0, 177)
reader.SetDataScalarTypeToUnsignedChar()
reader.Update()

# Calculate the center of the volume
(xMin, xMax, yMin, yMax, zMin, zMax) = reader.GetExecutive().GetWholeExtent(reader.GetOutputInformation(0)) # Get coordinate values
(xSpacing, ySpacing, zSpacing) = reader.GetOutput().GetSpacing()    # Get spacing values
(x0, y0, z0) = reader.GetOutput().GetOrigin()   # Get origin

# Set center
center= [x0 + xSpacing * 0.5 * (xMin + xMax),
        y0 + ySpacing * 0.5 * (yMin + yMax),
        z0 + zSpacing * 0.5 * (zMin + zMax)]

# Matrice for coronal, axial, sagittal  view orientations
axial = vtk.vtkMatrix4x4()
axial.DeepCopy((1, 0, 0, center[0],
                0, 1, 0, center[1],
                0, 0, 1, center[2],
                0, 0, 0, 1))

coronal = vtk.vtkMatrix4x4()
coronal.DeepCopy((1, 0, 0, center[0],
                0, 0, 1, center[1],
                0,-1, 0, center[2],
                0, 0, 0, 1))

sagittal = vtk.vtkMatrix4x4()
sagittal.DeepCopy((0, 0,-1, center[0],
                1, 0, 0, center[1],
                0,-1, 0, center[2],
                0, 0, 0, 1))

oblique = vtk.vtkMatrix4x4()
oblique.DeepCopy((1, 0, 0, center[0],
                0, 0.866025, -0.5, center[1],
                0, 0.5, 0.866025, center[2],
                0, 0, 0, 1))

# Extract a slice in the desired orientation
reslice = vtk.vtkImageReslice()
reslice.SetInputConnection(reader.GetOutputPort())
reslice.SetOutputDimensionality(2)
reslice.SetResliceAxes(axial)
reslice.SetInterpolationModeToLinear()

# Colors - edit values in RGBPoints to change colors
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)   #First point, all black
colorTransferFunction.AddRGBPoint(50, 1.0, 0.0, 0.0)  #One third points, all red
colorTransferFunction.AddRGBPoint(100, 0.0, 1.0, 0.0) #Two thirds points, all green
colorTransferFunction.AddRGBPoint(150, 0.0, 0.0, 1.0) #Three thirds points, all blue
  
# Map the image through the lookup table
color = vtk.vtkImageMapToColors()
color.SetLookupTable(colorTransferFunction)
color.SetInputConnection(reslice.GetOutputPort())

# Add current position text actor
txtpos = vtk.vtkTextActor()
txtpos.SetInput("Current Y:")
txtposprop = txtpos.GetTextProperty()
txtposprop.SetFontFamilyToArial()
txtposprop.SetFontSize(18)
txtposprop.SetColor(1, 1, 1)
txtpos.SetDisplayPosition(10, 10)

# Add current view text actor
txtview = vtk.vtkTextActor()
txtview.SetInput("Current view:")
txtviewprop = txtview.GetTextProperty()
txtviewprop.SetFontFamilyToArial()
txtviewprop.SetFontSize(18)
txtviewprop.SetColor(1, 1, 1)
txtview.SetDisplayPosition(10, 40)

# Create color actor mapping bar
colorBar = vtk.vtkScalarBarActor()
colorBar.SetLookupTable(color.GetLookupTable())
colorBar.SetTitle("Colormap")
colorBar.SetNumberOfLabels(0)
colorBar.SetLabelFormat("%6.0f")
colorBar.SetPosition(0.9, 0.1)
colorBar.SetWidth(0.08)
colorBar.SetHeight(0.5)
  
# Create image actor
actor = vtk.vtkImageActor()
actor.GetMapper().SetInputConnection(color.GetOutputPort())

# Create renderer and add actors
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(txtpos)
renderer.AddActor(txtview)
renderer.AddActor(colorBar)

# Create window, add renderer
window = vtk.vtkRenderWindow()
window.SetSize(1000,1000)
window.AddRenderer(renderer)
  
# Set up the interaction
interactorStyle = vtk.vtkInteractorStyleImage()
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(interactorStyle)
window.SetInteractor(interactor)
window.Render()
  
# Create callbacks for slicing the image
actions = {}
actions["Slicing"] = 0
currentOrientation = 0  # Change view orientation
def ButtonCallback(obj, event):
    if event == "LeftButtonPressEvent":
        actions["Slicing"] = 1
    else:
        actions["Slicing"] = 0

    # Change view orientation
    if event == "RightButtonPressEvent":
        global currentOrientation
        currentOrientation += 1
        if currentOrientation == 1:
            reslice.SetResliceAxes(coronal)
            print("Coronal view")
            txtview.SetInput("Current view:" + "Coronal view")
            txtviewprop = txtview.GetTextProperty()

        if currentOrientation == 2:
            reslice.SetResliceAxes(axial)
            print("Axial view")
            txtview.SetInput("Current view:" + "Axial view")
            txtviewprop = txtview.GetTextProperty()

        if currentOrientation == 3:
            reslice.SetResliceAxes(sagittal)
            print("Sagittal view")
            txtview.SetInput("Current view:" + "Sagittal view")
            txtviewprop = txtview.GetTextProperty()

        if currentOrientation == 4:
            reslice.SetResliceAxes(oblique)
            print("Oblique view")
            txtview.SetInput("Current view:" + "Oblique view")
            txtviewprop = txtview.GetTextProperty()
            currentOrientation = 0
        
        # Render new frame
        window.Render()

def MouseMoveCallback(obj, event):
    (lastX, lastY) = interactor.GetLastEventPosition()
    (mouseX, mouseY) = interactor.GetEventPosition()
    if actions["Slicing"] == 1:
        deltaY = mouseY - lastY
        reslice.Update()
        sliceSpacing = reslice.GetOutput().GetSpacing()[2]
        matrix = reslice.GetResliceAxes()

        # move the center point that we are slicing through
        center = matrix.MultiplyPoint((0, 0, sliceSpacing*deltaY, 1))
        matrix.SetElement(0, 3, center[0])
        matrix.SetElement(1, 3, center[1])
        matrix.SetElement(2, 3, center[2])

        #Update text
        txtpos.SetInput("Current Y:" + str(mouseY))
        txtposprop = txtpos.GetTextProperty()

        # Render new frame
        window.Render()
    else:
        interactorStyle.OnMouseMove()
  
  
interactorStyle.AddObserver("MouseMoveEvent", MouseMoveCallback)
interactorStyle.AddObserver("LeftButtonPressEvent", ButtonCallback)
interactorStyle.AddObserver("LeftButtonReleaseEvent", ButtonCallback)
interactorStyle.AddObserver("RightButtonPressEvent", ButtonCallback)
interactorStyle.AddObserver("RightButtonReleaseEvent", ButtonCallback)

# Start interaction
interactor.Start()

