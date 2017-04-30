#-------------------------------------------------------------------------------
# Name:        um-ab-mspdata
# Author:      Alicja Byzdra
# Created:     30-04-2017
# Copyright:   (c) Alicja Byzdra 2017
# Institution:     UMGDY
#-------------------------------------------------------------------------------

##try:
import arcpy
import os

################## PARAMETERS ####################################################################
layers = arcpy.GetParameterAsText(0)
layersList = layers.split(";")

coordSys = arcpy.GetParameterAsText(1)

outputGDB = arcpy.GetParameterAsText(2)

outputName = arcpy.GetParameterAsText(3)
################## PARAMETERS ####################################################################

#srcPath-tylko folder czy sciezka????
#typy pol i dlugosci

pointLayers = []
polygonLayers = []
polylineLayers = []
for lyr in layersList:
    desc = arcpy.Describe(lyr)
    arcpy.AddMessage(desc.name)
    arcpy.CopyFeatures_management(lyr, "in_memory"+"\\"+desc.name)

    fields=arcpy.ListFields("in_memory"+"\\"+desc.name)
    fields = [field.name for field in fields]
    if "srcLayer" not in fields:
        arcpy.AddField_management("in_memory"+"\\"+desc.name, "srcLayer", "TEXT",field_length=70)

##    arcpy.CalculateField_management(in_table="in_memory"+"\\"+desc.name, field="srcLayer", expression="""'"""+desc.name+"""'""", expression_type="PYTHON_9.3")
    arcpy.CalculateField_management(in_table="in_memory"+"\\"+desc.name, field="srcLayer", expression="""nazwa_gdb( !srcLayer! ,'"""+desc.name+"""')""", expression_type="PYTHON_9.3", code_block="def nazwa_gdb(src,fldr):\n    if src is None:\n        return fldr\n    else:\n        return src")

    if "srcPath" not in fields:
        arcpy.AddField_management("in_memory"+"\\"+desc.name, "srcPath", "TEXT",field_length=70)

    path = desc.catalogPath
    pathSpl = path.split("\\")
    path = pathSpl[-2]
##    arcpy.CalculateField_management(in_table="in_memory"+"\\"+desc.name, field="srcPath", expression="""'"""+path+"""'""", expression_type="PYTHON_9.3")
    arcpy.CalculateField_management(in_table="in_memory"+"\\"+desc.name, field="srcPath", expression="""nazwa_gdb( !srcPath! ,'"""+path+"""')""", expression_type="PYTHON_9.3", code_block="def nazwa_gdb(src,fldr):\n    if src is None:\n        return fldr\n    else:\n        return src")

    if desc.shapeType == "Point":
        pointLayers.append("in_memory"+"\\"+desc.name)
    elif desc.shapeType == "Polygon":
        polygonLayers.append("in_memory"+"\\"+desc.name)
    elif desc.shapeType == "Polyline":
        polylineLayers.append("in_memory"+"\\"+desc.name)


outLayers = [outputName + "_point", outputName + "_polygon", outputName + "_polyline"]
outTypes = ["POINT", "POLYGON", "POLYLINE"]
for i in range(len(outLayers)):
    arcpy.CreateFeatureclass_management(outputGDB, outLayers[i], outTypes[i], spatial_reference=coordSys)
    arcpy.AddField_management(outLayers[i],"seaUse","TEXT")
    arcpy.AddField_management(outLayers[i],"useType","TEXT")
    arcpy.AddField_management(outLayers[i],"useDsc","TEXT")
    arcpy.AddField_management(outLayers[i],"srcLayer","TEXT")
    arcpy.AddField_management(outLayers[i],"srcPath","TEXT")

arcpy.Append_management(pointLayers,outputName + "_point",schema_type="NO_TEST",field_mapping="",subtype="")
arcpy.Append_management(polygonLayers,outputName + "_polygon",schema_type="NO_TEST",field_mapping="",subtype="")
arcpy.Append_management(polylineLayers,outputName + "_polyline",schema_type="NO_TEST",field_mapping="",subtype="")

arcpy.Delete_management(in_data="in_memory", data_type="Workspace")

##except:
##    arcpy.AddError("Error occurred")
##    arcpy.AddMessage(arcpy.GetMessages())