import arcpy
from arcpy.sa import *
import numpy
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
Rasterband= r"C:\Users\K\Desktop\Practise\SingleflowFilterVush30m.tif.tif"
arcpy.env.workspace=r"C:\Users\K\Desktop\Practise"
def creationFlowDirectionRaster(Rasterband):
    raster=arcpy.Raster(Rasterband)
    outrast=arcpy.sa.FlowAccumulation(Rasterband)
    outrast.save("FlowDirectionvus30m.tif")
