    import math
    import arcpy
    from arcpy.sa import *
    import re
    Path=r"D:\Practica\LC81810242016147LGN00\LC81810262015304LGN00_MTL.txt"
    MetaFile="LC81810262015304LGN00_MTL.txt"

 class superClass(object):

    def __init__(self,Path,NumOftheBand):
        self.Path = Path
        self.NumOftheBand = NumOftheBand

    def readMTL(self):
        input=open(self.Path,"r")
        aString = input.read ()
        return  aString

    def tempDef(self,Textparameter):
        a = readMTL(self.Path)
        regexp=str(Textparameter)+str(self.NumOftheBand)+" = ([-0-9.]+)"
        stuff = re.findall(regexp, a)
        return float(stuff[0])

    def workSpace(overwrite,workspace):
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.overwriteOutput = overwrite
        arcpy.env.workspace=workspace

    def calculateRadiation(self,Rasterband):
        workSpace(True,r"D:\Practica")
        raster=arcpy.Raster(Rasterband)
        RadMax= tempDef(self.NumOftheBand,"RADIANCE_MAXIMUM_BAND_",self.Path)
        RadMin= tempDef(self.NumOftheBand,"RADIANCE_MINIMUM_BAND_",self.Path)
        Qmin=tempDef(self.NumOftheBand,"QUANTIZE_CAL_MIN_BAND_",self.Path)
        Qmax=tempDef(self.NumOftheBand,"QUANTIZE_CAL_MAX_BAND_",self.Path)
        R=(RadMax-RadMin)*((raster-Qmin)/(Qmax-Qmin))
        return R

    def numOfPhoto(MetaFile):
        MTLlistName=MetaFile.split(".")
        return str(MTLlistName[0])

    def creationTemperatureRaster(NumOftheBand,Rasterband):
        workSpace(True,r"D:\Practica")
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

    def creationAlbedoRaster(NumOftheBand,Rasterband):
        workSpace(True,r"D:\Practica")
        raster = arcpy.Raster(Rasterband)
        Eta=tempDef("","SUN_ELEVATION",Path)
        d=tempDef("", "EARTH_SUN_DISTANCE",Path)
        outrast=(math.pi*calculateRadiation(NumOftheBand,Rasterband)*d**2)/(E(NumOftheBand)*(math.sin(Eta*math.pi/180)))
        outrast.save("albedo"+numOfPhoto(MetaFile)+str(NumOftheBand)+".tif")


    Rasterband= r"D:\Practica\LC81810242016147LGN00\LC81810262015304LGN00_B5.TIF"



    tempDef("","SUN_ELEVATION",Path)
    creationAlbedoRaster(5)