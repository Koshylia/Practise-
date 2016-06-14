import math
import arcpy
import re

class superClass(object):
    """
    This class is used to find the albedo for 4 and 5 bands, and to find the temperature for 10 and 11 bands
    P.S.: Path to file write through a double slash.
    """

    def __init__(self, Path, Rasterband):
        """
        :param Path: path to metadata
        :param Rasterband: path to raster that we want to process
        """
        self.Path = Path
        self.Rasterband = Rasterband


    def readMTL(self):
        """
        open and read file with metadata
        :return: return string with metadata
        """
        input = open(self.Path, "r")
        aString = input.read()
        return aString

    def NumOfTheBand(self):
        """
        search number band
        :return: return number band
        """
        stuff = re.findall("B([0-9]+)", self.Rasterband)
        num = int(stuff[0])
        return num

    def tempDef(self, Textparameter):
        """
        search parameter in file metadata
        :param Textparameter: parameter that we are search
        :return: return value parameter that we are search
        """
        a = self.readMTL()
        regexp = str(Textparameter)+" = ([-0-9.]+)"
        stuff = re.findall(regexp, a)
        return float(stuff[0])

    def workSpace(self, overwrite, workspace):
        """
        :param overwrite:
        :param workspace:
        :return:
        """
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.overwriteOutput = overwrite
        arcpy.env.workspace = workspace


    def calculateRadiation(self):
        """
        Find value radiation for all band
        :return: return raster
        """
        self.workSpace(True, r"D:\Practica")
        raster = arcpy.Raster(self.Rasterband)
        rad_max = self.tempDef("RADIANCE_MAXIMUM_BAND_"+str(self.NumOfTheBand()))
        rad_min = self.tempDef("RADIANCE_MINIMUM_BAND_"+str(self.NumOfTheBand()))
        q_min = self.tempDef("QUANTIZE_CAL_MIN_BAND_"+str(self.NumOfTheBand()))
        q_max = self.tempDef("QUANTIZE_CAL_MAX_BAND_"+str(self.NumOfTheBand()))
        r = (rad_max-rad_min)*((raster-q_min)/(q_max-q_min))
        return r
    '''
    def numOfPhoto(self):
        MTLlistName = MetaFile.split(".")
        return str(MTLlistName[0])
    '''
    def creationTemperatureRaster(self):
        """
        Find value temperature for 10 or 11 bands
        :return: return raster with estimated temperature
        """
        self.workSpace(True, r"D:\Practica")
        k1 = self.tempDef("K1_CONSTANT_BAND_"+str(self.NumOfTheBand()))
        k2 = self.tempDef("K2_CONSTANT_BAND_"+str(self.NumOfTheBand()))
        outrast = k2/(arcpy.sa.Ln(k1/self.calculateRadiation()+1.0))
        outrast.save("temperature"+str(self.NumOfTheBand())+".tif")

    def luminosityCoefficient(self):
        """

        :return: returns luminosity coefficient
        """
        if self.NumOfTheBand() == 4:
            E = 1547
        if self.NumOfTheBand() == 5:
            E = 1044
        return E

    def creationAlbedoRaster (self):
        """
        Find value albedo for 4 or 5 bands
        :return: return raster with estimated albedo
        """
        self.workSpace(True, r"D:\Practica")
        Eta = self.tempDef("SUN_ELEVATION")
        d = self.tempDef("EARTH_SUN_DISTANCE")
        outrast=(math.pi*self.calculateRadiation()*d**2)/(self.luminosityCoefficient()*(math.sin(Eta*math.pi/180)))
        outrast.save("albedo"+str(self.NumOfTheBand())+".tif")


Path = "D:\\Practica\\LC81810242016147LGN00\\LC81810242016147LGN00_MTL.txt"
Rasterband = "D:\\Practica\\LC81810242016147LGN00\\LC81810242016147LGN00_B10.TIF"

a = superClass(Path, Rasterband)
a.creationTemperatureRaster()
print "END"
