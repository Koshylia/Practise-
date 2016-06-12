import arcpy
from arcpy.sa import *
import numpy
import math
#environment settings in the ArcGis
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
Rasterband= r"C:\Users\K\Desktop\Practise\FilterVush30m.tif"
arcpy.env.workspace=r"C:\Users\K\Desktop\Practise"
arcpy.CheckOutExtension("Spatial")
# Raster properties
raster=arcpy.Raster(Rasterband)
endi=raster.height
endj=raster.width
selsize=raster.meanCellHeight
coner=arcpy.Point(raster.extent.XMin,raster.extent.YMin)
Spatref=raster.spatialReference
#radius of the movving window
r=1
#convert raster to the array for working with each pixel
arr=arcpy.RasterToNumPyArray(raster,nodata_to_value=None)
#creation new array for aplying values of each pixel to creation new raster that will include information about the direction
newarr=[]
# c is a matrix of direction 32=NW 64=N 128=NE 1=E 2=SE 4=S 8=SW 16=W
c=[32,64,128,16,"",1,8,4,2]
for i in range(0,endi):
    G=[]
    for j in range(0,endj):
        a=arr[i:i+(2*r+1),j:j+(2*r+1)]
        ListArr=a.tolist()
        List=[]
        for k in range(len(ListArr)):
            for t in range(len(ListArr[0])):
                if len(ListArr[0])>1:
                    #count excess for each pixel
                    Per= float(ListArr[int(len(ListArr)/2.0)][int(len(ListArr[0])/2.0)]-ListArr[k][t])
                    List.append(Per)
                else:
                    List.append(ListArr[k][t])
        #determine max excess
        a=max(List)
        if list.count(max(List))!=1:
            List=List*math.sqrt(2)
            a=max(List)
        ind=List.index(a)
        g=c[ind]
        G.append(g)
    newarr.append(G)
array=numpy.array(newarr)
myRaster = arcpy.NumPyArrayToRaster(array,lower_left_corner=coner,x_cell_size=selsize)
myRaster.save("SingleflowFilterVush30m.tif")

