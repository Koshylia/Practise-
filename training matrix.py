import arcpy
import numpy as np

tm_output = np.array([[0, 1, 2, 3, 0, 0, 0, 0, 0, 0], [0, 1, 2, 3, 8, 1, 2, 1, 2, 0], [0, 1, 2, 3, 4, 16, 3, 2, 4, 0],
               [0, 1, 2, 6, 8, 10, 21, 8, 2, 0], [0, 1, 2, 0, 0, 0, 34, 20, 4, 0], [0, 1, 2, 0, 0, 1, 56, 0, 2, 2],
               [0, 0, 0, 3, 4, 59, 1, 0, 1, 1], [0, 2, 1, 8, 60, 0, 1, 0, 0, 0], [0, 1, 7, 9, 61, 7, 3, 2, 1, 0],
               [0, 1, 2, 83, 0, 0, 11, 2, 1, 0]])

tm_input = np.array([[1, 1, 1, 2, 2, 2, 4, 4, 4, 8], [1, 1, 1, 1, 2, 4, 4, 4, 4, 8], [1, 1, 1, 1, 1, 2, 4, 4, 8, 8],
                     [1, 1, 1, 1, 1, 2, 4, 4, 8, 16], [1, 1, 128, 128, 128, 4, 4, 8, 16, 16], [1, 1, 2, 2, 4, 8, 8, 32, 32, 32],
                     [2, 2, 2, 4, 8, 8, 16, 16, 64, 64], [1, 2, 4, 4, 4, 4, 8, 16, 64, 64], [1, 1, 2, 4, 8, 2, 16, 16, 16, 16],
                     [1, 1, 1, 4, 4, 4, 4, 16, 16, 16]])

print tm_input

print tm_output

inputRaster = arcpy.NumPyArrayToRaster(tm_input)
inputRaster.save(r'D:\Practica\inputRaster.tif')

outRaster = arcpy.NumPyArrayToRaster(tm_output)
outRaster.save(r"D:\Practica\outRaster.tif")

print "END"