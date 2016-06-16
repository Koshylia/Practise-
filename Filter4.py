import arcpy
from arcpy.sa import *
import numpy
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
Rasterband= r"C:\Users\K\Desktop\Practise\Bilaclip"
arcpy.env.workspace=r"C:\Users\K\Desktop\Practise"
arcpy.CheckOutExtension("Spatial")
raster=arcpy.Raster(Rasterband)
endi=raster.height
endj=raster.width
selsize=raster.meanCellHeight
corner=arcpy.Point(raster.extent.XMin,raster.extent.YMin)
Spatref=raster.spatialReference
r=1
arr=arcpy.RasterToNumPyArray(raster,nodata_to_value=None)
newarr=[]
for i in range(0,endi):
    G=[]
    for j in range(0,endj):
        a=arr[i:i+(2*r+1),j:j+(2*r+1)]
        stdArr=numpy.std(a)
        meanArr=numpy.mean(a)
        ListArr=a.tolist()
        List=[]
        for k in range(len(ListArr)):
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
myRaster = arcpy.NumPyArrayToRaster(array,lower_left_corner=corner,x_cell_size=selsize)
myRaster.save("FilterBilaclip30m1.tif")
