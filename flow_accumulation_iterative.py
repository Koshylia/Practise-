from itertools import product
import numpy as np
import arcpy
input_raster = "D:\\Practica\\SingleflowFilterVush30m.tif.tif"

raster = arcpy.Raster(input_raster)
coner = arcpy.Point(raster.extent.XMin, raster.extent.YMin)
selsize = raster.meanCellHeight

Direcciones = arcpy.RasterToNumPyArray(input_raster)
Acum = np.zeros((len(Direcciones), len(Direcciones[0])), dtype=object)

for i, j in product(range(len(Direcciones)), range(len(Direcciones[0]))):
    Acum[i, j] = None

def AcumulacionCelda(x,y):
    if Acum[x, y] != None:
        return
    Acum[x, y] = 1
    d = {(-1, -1): 2,
         (-1, 0): 4,
         (-1, 1): 8,
         (0, -1): 1,
         (0, 0): '',
         (0, 1): 16,
         (1, -1): 128,
         (1, 0): 64,
         (1, 1): 32}
    keys = tuple(product(range(-1, 2), range(-1, 2)))[::-1]
    queue = [('Loop', (x, y), list(keys))]

    while queue:
        instruction, coords, directions = queue.pop()
        x, y = coords
        if instruction == 'Loop':
            while directions:
                m, n = directions.pop()
                if (0 <= x + m < len(Direcciones)) and (0 <= y + n < len(Direcciones[0])):
                    if Direcciones[x+m, y+n] == d[m, n]:
                        queue.append(('Loop', (x, y), directions))
                        queue.append(('Add', (x, y), (m, n)))
                        if Acum[x+m, y+n] == None:
                            Acum[x+m, y+n] = 1
                            queue.append(('Loop', (x+m, y+n), list(keys)))
                        break
        elif instruction == 'Add':
            m, n = directions
            Acum[x, y] += Acum[x+m, y+n]

for i, j in product(range(0, len(Direcciones)), range(0, len(Direcciones[0]))):
    AcumulacionCelda(i, j)

Accumlation = np.array(Acum, dtype=int)

myRaster = arcpy.NumPyArrayToRaster(Accumlation, lower_left_corner=coner, x_cell_size=selsize)
myRaster.save("D:\\Practica\\AccamulationVush30m_iteretive_metod.tif")

print "End"