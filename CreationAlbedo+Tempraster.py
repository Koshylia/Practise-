import math
import arcpy
#from arcpy.sa import *
import re
#Path=r"D:\Practica\LC81810242016147LGN00\LC81810262015304LGN00_MTL.txt"
#MetaFile = "LC81810262015304LGN00_MTL.txt"
#Rasterband= r"D:\Practica\LC81810242016147LGN00\LC81810262015304LGN00_B5.TIF"

class superClass(object):

    def __init__(self, Path, Rasterband):
        '''

        :param Path: path to metadata
        :param Rasterband: path to raster that we want to process
        '''
        self.Path = Path
        self.Rasterband = Rasterband


    def readMTL(self):
        '''
        open and read file with metadata
        :return: return string with metadata
        '''
        input=open(self.Path,"r")
        aString = input.read ()
        return  aString

    def NumOfTheBand(self):
        '''
        search number band
        :return: return number band
        '''
        stuff = re.findall("B([0-9]+)", self.Rasterband)
        num = int(stuff[0])
        return num

    def tempDef(self,Textparameter):
        '''
        search parameter in file metadata
        :param Textparameter: parameter that we are
        :return:
        '''
        a = self.readMTL()
        NumOftheBand = self.NumOfTheBand()
        regexp=str(Textparameter)+str(NumOftheBand)+" = ([-0-9.]+)"
        stuff = re.findall(regexp, a)
        return float(stuff[0])

    def workSpace(self,overwrite,workspace):
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.overwriteOutput = overwrite
        arcpy.env.workspace=workspace


    def calculateRadiation (self):
        '''

        :return:
        '''
        self.workSpace(True,r"D:\Practica")
        raster = arcpy.Raster(self.Rasterband)
        RadMax = self.tempDef("RADIANCE_MAXIMUM_BAND_")
        RadMin = self.tempDef("RADIANCE_MINIMUM_BAND_")
        Qmin = self.tempDef("QUANTIZE_CAL_MIN_BAND_")
        Qmax = self.tempDef("QUANTIZE_CAL_MAX_BAND_")
        R =(RadMax-RadMin)*((raster-Qmin)/(Qmax-Qmin))
        return R
    '''
    def numOfPhoto (self):
        MTLlistName = MetaFile.split(".")
        return str(MTLlistName[0])
    '''
    def creationTemperatureRaster (self):
        self.workSpace(True, r"D:\Practica")
        k1=self.tempDef("K1_CONSTANT_BAND_")
        k2=self.tempDef("K2_CONSTANT_BAND_")
        outrast=k2/(arcpy.sa.Ln(k1/self.calculateRadiation()+1.0))
        outrast.save("temperature"+self.NumOfTheBand()+".tif")

    def E (self):
        if self.NumOfTheBand() == 4:
            E = 1547
        if self.NumOfTheBand() == 5:
            E = 1044
        return E

    def creationAlbedoRaster (self):
        self.workSpace(True,r"D:\Practica")
        Eta = self.tempDef("SUN_ELEVATION")
        d = self.tempDef("EARTH_SUN_DISTANCE")
        outrast=(math.pi*self.calculateRadiation()*d**2)/(self.E()*(math.sin(Eta*math.pi/180)))
        outrast.save("albedo"+self.NumOfTheBand()+".tif")
