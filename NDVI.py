import math
import arcpy
from arcpy.sa import *

def workSpace(overwrite,workspace):
    arcpy.CheckOutExtension("Spatial")
    arcpy.env.overwriteOutput = overwrite
    arcpy.env.workspace=workspace

def creationNDVIRaster(NumOftheNDVI):
    workSpace(True,r"C:\Users\K\Desktop\Practise")
    Rasterband4= r"C:\Users\K\Desktop\Practise\albedoLC81810262015304LGN00_MTL4.TIF"
    Rasterband5=r"C:\Users\K\Desktop\Practise\albedoLC81810262015304LGN00_MTL5.TIF"
    raster4=arcpy.Raster(Rasterband4)
    raster5=arcpy.Raster(Rasterband5)
    outrast=(raster5-raster4)/(raster5+raster4)
    outrast.save("NDVI"+str(NumOftheNDVI)+".tif")