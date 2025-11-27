import arcpy
import os

# --- Ustawienia ---
gdb_path = r"C:\ZMG_2025_2026\arcgis_zmg"
txt_path = r"C:\ZMG_2025_2026\arcgis_zmg\data.txt"
output_fc_name = "Punkty_z_txt"

arcpy.env.workspace = gdb_path
arcpy.env.overwriteOutput = True   # odkomentowane – żeby nie było 000725

# --- Sprawdź plik ---
if not os.path.exists(txt_path):
    raise FileNotFoundError(f"Nie znaleziono pliku: {txt_path}")

# --- Czytaj współrzędne ---
ListCoor = []
with open(txt_path, 'r') as f:
    for line_num, line in enumerate(f, 1):
        line = line.strip()
        if not line: continue
        parts = line.replace(',', ' ').split()
        if len(parts) < 2: 
            print(f"Pominięto linię {line_num}: {line}")
            continue
        try:
            x = float(parts[0])
            y = float(parts[1])
            ListCoor.append([x, y])
        except ValueError as e:
            print(f"Błąd w linii {line_num}: {e}")

if not ListCoor:
    raise ValueError("Brak współrzędnych!")

# --- Tworzenie warstwy ---
spatial_reference = arcpy.SpatialReference(2180)   # ← DZIAŁA ZAWSZE

arcpy.management.CreateFeatureclass(
    out_path=gdb_path,
    out_name=output_fc_name,
    geometry_type="POINT",
    spatial_reference=spatial_reference
)

# --- Wstawianie punktów ---
with arcpy.da.InsertCursor(output_fc_name, ["SHAPE@XY"]) as cursor:
    for x, y in ListCoor:
        cursor.insertRow([(x, y)])

print(f"Sukces! Utworzono: {output_fc_name} z {len(ListCoor)} punktami")