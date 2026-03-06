import csv
import sys

import os
csv_dir = os.environ.get("SIEX_CSV_DIR", "../../../Catalogos_csv")
f = open(os.path.join(csv_dir, 'Unidades de medida.csv'), encoding='cp1252')
r = csv.DictReader(f, delimiter=';')
for row in r:
    if row['Código SIEX'] in ['45', '46']:
        print(repr(row['Unidades de medida']))
