from itertools import product
import numpy as np
import arcpy
input_raster = "D:\Practica\SingleflowFilterVush30m.tif.tif"

raster = arcpy.Raster(input_raster)
coner = arcpy.Point(raster.extent.XMin, raster.extent.YMin)
selsize = raster.meanCellHeight

Direcciones = arcpy.RasterToNumPyArray(input_raster)
Acum = np.zeros((len(Direcciones), len(Direcciones[0])), dtype=object)

for i, j in product(range(len(Direcciones)), range(len(Direcciones[0]))):
    Acum[i, j] = None


def AcumulacionCelda(x,y):
    d = {(-1, -1):  2,
         (-1, 0) :  4,
         (-1, 1) :  8,
         (0, -1) :  1,
         (0, 0)  :  'dummy',
         (0, 1)  :  16,
         (1, -1) :  128,
         (1, 0)  :  64,
         (1, 1)  :  32}

    if Acum[x, y] == None:
        Acum[x, y] = 0
        for m, n in product(range(-1, 2), range(-1, 2)):
            if (0 <= x+m < len(Direcciones)) and (0 <= y+n < len(Direcciones[0])):
                if Direcciones[x+m, y+n] == d[m, n]:
                    AcumulacionCelda(x+m, y+n)
                    Acum[x, y] += Acum[x+m, y+n] + 1


for i, j in product(range(0, len(Direcciones)), range(0, len(Direcciones[0]))):
    AcumulacionCelda(i, j)

Accumlation = np.array(Acum, dtype=int)

myRaster = arcpy.NumPyArrayToRaster(Accumlation, lower_left_corner=coner, x_cell_size=selsize)
myRaster.save("D:\\Practica\\AccumulationVush.tif")

#print Accumlation
