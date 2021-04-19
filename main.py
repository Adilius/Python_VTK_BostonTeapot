# Verify that we are running right python version
import sys
print("Python " + str(sys.version_info[0]) + "." + str(sys.version_info[1]))

import vtk

# Read raw dataset
reader = vtk.vtkImageReader()
reader.SetFileName('BostonTeapot.raw')
reader.SetDataByteOrderToBigEndian()
reader.SetNumberOfScalarComponents(1)
reader.SetFileDimensionality(3)
reader.SetDataExtent(0, 255, 0, 255, 0, 177)
reader.SetDataScalarTypeToUnsignedChar()
reader.Update()