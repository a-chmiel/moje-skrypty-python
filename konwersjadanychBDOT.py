import os
import shutil 
import arcpy
folder_shp = r"C:\ZMG_2025_2026\arcgis_zmg\0204_SHP_2020"
folder_new_shp = r"C:\ZMG_2025_2026\arcgis_zmg\new_0204_SHP_2020"
arcpy.env.workspace = r"C:\ZMG_2025_2026\arcgis_zmg\arcgis_zmg.gdb"

for file in os.listdir(folder_shp):
    name, ext = os.path.splitext(file)
    new_file = name.replace(".", "_") + ext
    #print(f"{folder_shp}\\{file}", f"{folder_new_shp}\\{new_file}")
    shutil.copy(f"{folder_shp}\\{file}", f"{folder_new_shp}\\{new_file}")

for new_file in os.listdir(folder_new_shp):
    name, ext = os.path.splitext(new_file)
    if ext == ".shp":
        # print(f"{folder_new_shp}\\{new_file}", name.split("__")[1])
        arcpy.conversion.ExportFeatures(
            in_features=f"{folder_new_shp}\\{new_file}",
            out_features = "R_2020" + name.split("__")[1])
print ("koniec")