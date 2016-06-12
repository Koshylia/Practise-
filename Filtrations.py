import arcpy
from arcpy.sa import *
import numpy

Rasterband= r"C:\Users\K\Desktop\Practise\vush30m"
RasterName = "vush30m"



def workSpace(overwrite, workspace):
    # This function works with enviromets settings in the Arcgis
    arcpy.CheckOutExtension("Spatial")
    arcpy.env.overwriteOutput = overwrite
    arcpy.env.workspace = workspace


def rasterHeight(Rasterband):
    #This function determines raster height
    raster = arcpy.Raster(Rasterband)
    endi = raster.height
    return endi


def rasterWidth(Rasterband):
    #This function determines raster width
    raster = arcpy.Raster(Rasterband)
    endj = raster.width
    return endj


def cellSize(Rasterband):
    #This function determines raster cell size
    raster = arcpy.Raster(Rasterband)
    cellsize = raster.meanCellHeight
    return cellsize

def leftCorner(Rasterband):
    #this function determines position of the raster left corner
    coner = arcpy.Point(raster.extent.XMin, raster.extent.YMin)
    return coner


def rasterArray(Rasterband):
    #this function creates array with include information about each pixel
    raster = arcpy.Raster(Rasterband)
    arr = arcpy.RasterToNumPyArray(raster, nodata_to_value=None)
    return arr

def filtration(r,Rasterband):
    #This feature filters the raster method and removes depression
    newarr=[]
    for i in range(0,rasterHeight(Rasterband)):
        G=[]
        for j in range(0,rasterWidth(Rasterband)):
            a=rasterArray(Rasterband)[i:i+(2*r+1),j:j+(2*r+1)]
            stdArr=numpy.std(a)
            meanArr=numpy.mean(a)
            ListArr=a.tolist()
            List=[]
            f for k in range(len(ListArr)):
            for t in range(len(ListArr[0])):
                if ListArr[k][t]>=(meanArr-stdArr) and ListArr[k][t]<=(meanArr+stdArr):
                    List.append(ListArr[k][t])
        if len(List)>0:
            if List[int(len(List)/2.0)]is min(List)and len(List)>1:
                g=float(sum(List)-List[int(len(List)/2.0)])/(len(List)-1)
            else:
                g=float(sum(List)/len(List))
            G.append(g)
        newarr.append(G)
    array=numpy.array(newarr)
    myRaster = arcpy.NumPyArrayToRaster(array,lower_left_corner=coner,x_cell_size=selsize)
    myRaster.save("FilterVush30m.tif")
filtration(1,Rasterband)