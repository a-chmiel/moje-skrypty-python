import arcpy
from collections import defaultdict
import matplotlib.pyplot as plt

# Ustawienie środowiska pracy
arcpy.env.workspace = r"C:\ZMG_2025_2026\arcgis_zmg\arcgis_zmg.gdb"

# Lista klas obiektów
featureclasses = arcpy.ListFeatureClasses()

# Listy do przechowywania warstw z 2014 i 2020
PT2014_list = []
PT2020_list = []

# Wyszukiwanie odpowiednich warstw
for fc in featureclasses:
    if "R_2014" in fc and "OT_PT" in fc:  # Poprawka: R_2024 → dane z 2014
        print("2014 - ", fc)
        PT2014_list.append(fc)
    elif "R_2020" in fc and "OT_PT" in fc:
        print("2020 - ", fc)
        PT2020_list.append(fc)

# Nazwy warstw wynikowych po scaleniu
PT2014 = "PT_2014"
PT2020 = "PT_2020"
print (PT2014_list)
print (PT2020_list)
# Scalanie warstw
arcpy.management.Merge(PT2014_list, PT2014)
arcpy.management.Merge(c, PT2020)

# Przecięcie przestrzenne między 2014 a 2020
inter_2014_2020 = "PT_2014_2020"
arcpy.analysis.Intersect([PT2014, PT2020], inter_2014_2020)

# Analiza zmian: obliczanie powierzchni całkowitej i zmienionej
area_pary = defaultdict(float)
area_all = 0.0
area_change = 0.0
i = 0

with arcpy.da.SearchCursor(inter_2014_2020, ["X_KOD", "X_KOD_1", "Shape_Area"]) as cursor:
    for row in cursor:
        area_all += row[2]
        if row[0] != row[1]:
            i += 1
            area_change += row[2]
            pary = f"{row[0]}-{row[1]}"
            area_pary[pary] += row[2]

# Wyniki procentowe
proc_bez_zmian = ((area_all - area_change) / area_all) * 100
proc_zmian = (area_change / area_all) * 100
print(f"Liczba zmian: {i}")
print(f"Bez zmian: {proc_bez_zmian:.2f}% | Ze zmianą: {proc_zmian:.2f}%")

# Sortowanie par zmian według powierzchni
area_pary_sort = sorted(area_pary.items(), key=lambda x: x[1], reverse=True)

# Grupowanie: top 5 zmian + "reszta"
separator = 5
new_list = []
area_inne = 0.0
j = 0

for kod, powierzchnia in area_pary_sort:
    procent = (powierzchnia / area_change) * 100
    if j < separator:
        new_list.append([kod, procent])
    else:
        area_inne += procent
    j += 1

if area_inne > 0:
    new_list.append(["reszta", area_inne])

print("\nTop zmiany (procentowo od powierzchni zmienionej):")
for item in new_list:
    print(f"{item[0]}: {item[1]:.2f}%")

# Wykres kołowy
wartosci = [x[1] for x in new_list]
etykiety = [x[0] for x in new_list]

plt.figure(figsize=(8, 8))
plt.pie(wartosci, labels=etykiety, autopct='%1.1f%%', startangle=90)
plt.title('Zmiany klas pokrycia terenu 2014 → 2020\n(top 5 + reszta)')
plt.axis('equal')
plt.show()