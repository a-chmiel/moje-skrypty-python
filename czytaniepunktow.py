import arcpy

# Zmień tę linijkę na dokładną pełną ścieżkę do Twojej warstwy punktowej
# Przykład 1 – jeśli jest w geobazie:
WarstwaPKT = r"C:\ZMG_2025_2026\arcgis_zmg\arcgis_zmg.gdb\OT_KUKO_P"


arcpy.env.workspace = r"C:\ZMG_2025_2026\arcgis_zmg\arcgis_zmg.gdb"   
arcpy.env.overwriteOutput = True   

WarstwaPKT = "OT_KUKO_P"   

ListCoor = []
cursor = arcpy.da.SearchCursor(WarstwaPKT, ["SHAPE@X", "SHAPE@Y"])
for row in cursor:
    print(row)
    ListCoor.append([row[0] + 1000, row[1] + 2000])  
del cursor


NowaWarstwa = "OT_KUKO_P_przesu"
arcpy.management.CreateFeatureclass(
    arcpy.env.workspace,          
    NowaWarstwa, 
    "POINT", 
    spatial_reference=WarstwaPKT   
)


cursor = arcpy.da.InsertCursor(NowaWarstwa, ["SHAPE@XY"])
for coor in ListCoor:
    cursor.insertRow([coor])     

del cursor

