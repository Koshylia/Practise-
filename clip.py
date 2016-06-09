import arcpy

arcpy.env.workspace = r"E:\DZZ\practice"

arcpy.CheckOutExtension("Data Management")
arcpy.Clip_management("n50_e030_1arc_v3.tif","30.401345 50.571615 30.527159 50.648948", "clip_vysh2.tif","frame_vyshgorod.shp", "#", "ClippingGeometry","NO_MAINTAIN_EXTENT")
arcpy.Clip_management("n49_e030_1arc_v3.tif","30,031388 49,770681 30,120094 49,829311", "clip_bila2.tif","frame_bila.shp", "#", "ClippingGeometry","NO_MAINTAIN_EXTENT")

