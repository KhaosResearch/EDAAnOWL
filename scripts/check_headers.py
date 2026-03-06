import csv
import os

files = [
    "Producto Vegetal.csv",
    "Variedad - Especie - Tipo.csv",
    "Unidades de medida.csv",
    "Destino del cultivo.csv",
    "Catálogo oficial de razas de ganado de España.csv",
    "Especies animales.csv",
    "Cultivo.csv"
]

csv_dir = os.environ.get("SIEX_CSV_DIR", "../../../Catalogos_csv")

for f_name in files:
    f_path = os.path.join(csv_dir, f_name)
    if not os.path.exists(f_path):
        print(f"File not found: {f_name}")
        continue
    with open(f_path, mode='r', encoding='latin-1') as f:
        reader = csv.DictReader(f, delimiter=';')
        print(f"--- {f_name} ---")
        print(reader.fieldnames)
