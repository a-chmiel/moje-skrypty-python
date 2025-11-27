import os
import shutil
import arcpy

# Ścieżki do folderów źródłowych i docelowych
folder_shp = r"C:\ZMG_2025_2026\arcgis_zmg\0204_SHP_2020"
folder_new_shp = r"C:\ZMG_2025_2026\arcgis_zmg\new_0204_SHP_2020"

# Ustawienie workspace dla ArcPy (geobaza, do której eksportujemy dane)
arcpy.env.workspace = r"C:\ZMG_2025_2026\arcgis_zmg\arcgis_zmg.gdb"
arcpy.env.overwriteOutput = True  # Ważne: pozwala nadpisywać istniejące warstwy w GDB

# KROK 1: Kopiowanie plików .shp i zmiana kropki w nazwie na podkreślnik
# Przykład: "R.2020.shp" → "R_2020.shp"
for file in os.listdir(folder_shp):
    file_path = os.path.join(folder_shp, file)  # Bezpieczne łączenie ścieżek
    if os.path.isfile(file_path):  # Sprawdzamy, czy to plik
        name, ext = os.path.splitext(file)
        # Zastępujemy WSZYSTKIE kropki w nazwie pliku na podkreślniki
        new_name = name.replace(".", "_") + ext
        new_file_path = os.path.join(folder_new_shp, new_name)
        
        # Kopiujemy plik do nowego folderu z nową nazwą
        shutil.copy(file_path, new_file_path)
        print(f"Skopiowano: {file} → {new_name}")

# KROK 2: Eksport shapefile'ów do geobazy
for new_file in os.listdir(folder_new_shp):
    file_path = os.path.join(folder_new_shp, new_file)
    name, ext = os.path.splitext(new_file)
    
    if ext.lower() == ".shp":  # Sprawdzamy, czy to shapefile (małe/duże litery)
        # Przykład nazwy: "R_2020.shp" → wyciągamy "2020"
        parts = name.split("__")
        output_feature_class = f"R_2020{parts[1]}"  # np. "R_20202020"
            
            
        try:
            # Eksport do geobazy
            arcpy.conversion.ExportFeatures(
                in_features=file_path,
                out_features=output_feature_class
            )
            print(f"Eksportowano: {new_file} → {output_feature_class}")
        except arcpy.ExecuteError:
            print(f"Błąd ArcPy przy {new_file}: {arcpy.GetMessages()}")
        except Exception as e:
            print(f"Nieoczekiwany błąd przy {new_file}: {str(e)}")

print("Koniec przetwarzania.")