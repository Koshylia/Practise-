import math
import arcpy
from arcpy.sa import *
import re
Path=r"C:\Users\K\Desktop\Practise\LC81810262015304LGN00_MTL.txt"
MetaFile="LC81810262015304LGN00_MTL.txt"
def readMTL(Path):
    input=open(Path,"r")
    aString = input.read ()
    return  aString

def tempDef(NumOftheBand,Textparameter,Path):
    a = readMTL(Path)
    regexp=str(Textparameter)+str(NumOftheBand)+" = ([-0-9.]+)"
    print regexp
    stuff = re.findall(regexp, a)
    print stuff
    if len(stuff)== 1:
        Parameter = float(stuff[0])
    return Parameter

def workSpace(overwrite,workspace):
    arcpy.CheckOutExtension("Spatial")
    arcpy.env.overwriteOutput = overwrite
    arcpy.env.workspace=workspace

def calculateRadiation(NumOftheBand,Rasterband):
    workSpace(True,r"C:\Users\K\Desktop\Practise")
    Rasterband= r"C:\Users\K\Desktop\Practise\LC81810262015304LGN00_B5.TIF"
    raster=arcpy.Raster(Rasterband)
    RadMax= tempDef(NumOftheBand,"RADIANCE_MAXIMUM_BAND_",Path)
    RadMin= tempDef(NumOftheBand,"RADIANCE_MINIMUM_BAND_",Path)
    Qmin=tempDef(NumOftheBand,"QUANTIZE_CAL_MIN_BAND_",Path)
    Qmax=tempDef(NumOftheBand,"QUANTIZE_CAL_MAX_BAND_",Path)
    R=(RadMax-RadMin)*((raster-Qmin)/(Qmax-Qmin))
    return R

def numOfPhoto(MetaFile):
    MTLlistName=MetaFile.split(".")
    return str(MTLlistName[0])

def creationTemperatureRaster(NumOftheBand):
    workSpace(True,r"C:\Users\K\Desktop\Practise")
    Rasterband= r"C:\Users\K\Desktop\Practise\LC81810262015304LGN00_B5.TIF"
    k1=tempDef(NumOftheBand,"K1_CONSTANT_BAND_",Path)
    k2=tempDef(NumOftheBand,"K2_CONSTANT_BAND_",Path)
    outrast=k2/(arcpy.sa.Ln(k1/calculateRadiation(NumOftheBand,Rasterband)+1.0))
    outrast.save("temperature"+numOfPhoto(MetaFile)+str(NumOftheBand)+".tif")

def E(NumOftheBand):
    if NumOftheBand==4:
        E=1547
    if NumOftheBand==5:
        E=1044
    return E

def creationAlbedoRaster(NumOftheBand):
    workSpace(True,r"C:\Users\K\Desktop\Practise")
    Rasterband= r"C:\Users\K\Desktop\Practise\LC81810262015304LGN00_B5.TIF"
    raster = arcpy.Raster(Rasterband)
    Eta=tempDef("","SUN_ELEVATION",Path)
    d=tempDef("", "EARTH_SUN_DISTANCE",Path)
    outrast=(math.pi*calculateRadiation(NumOftheBand,Rasterband)*d**2)/(E(NumOftheBand)*(math.sin(Eta*math.pi/180)))
    outrast.save("albedo"+numOfPhoto(MetaFile)+str(NumOftheBand)+".tif")

#tempDef("","SUN_ELEVATION",Path)
#creationAlbedoRaster(5)