import sys
import os

csv_dir = os.environ.get("SIEX_CSV_DIR", "../../../Catalogos_csv")
files = [
    os.path.join(csv_dir, "Producto Vegetal.csv"),
    os.path.join(csv_dir, "Cultivo.csv"),
    os.path.join(csv_dir, "Variedad - Especie - Tipo.csv"),
    os.path.join(csv_dir, "Unidades de medida.csv"),
    os.path.join(csv_dir, "Destino del cultivo.csv"),
    os.path.join(csv_dir, "Catálogo oficial de razas de ganado de España.csv"),
    os.path.join(csv_dir, "Especies animales.csv")
]

for f in files:
    with open(f, 'rb') as file:
        rawdata = file.read(1000)
        try:
            rawdata.decode('utf-8-sig')
            encoding = 'utf-8-sig'
        except UnicodeDecodeError:
            try:
                rawdata.decode('utf-8')
                encoding = 'utf-8'
            except UnicodeDecodeError:
                encoding = 'latin-1'
        print(f"{os.path.basename(f)}: {encoding}")
