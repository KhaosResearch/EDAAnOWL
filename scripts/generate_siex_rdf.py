import csv
import os
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import SKOS, DCTERMS, RDFS, XSD

# Namespaces
SIEX_DEF = Namespace("https://agrixels.upc.edu/def/medio-rural-pesca/agrixel/")
SIEX_KOS = Namespace("https://agrixels.upc.edu/kos/medio-rural-pesca/siex/")
EDAAN = Namespace("https://w3id.org/EDAAnOWL/")

# Configuration: Mapping SIEX Schemes to CSV file names and their columns
MAPPING = {
    "siexCropProductValueCode": {
        "file": "Producto Vegetal.csv",
        "id_col": "C\u00f3digo SIEX", # "Id" or "C\u00f3digo SIEX"? Looking at previous head, "C\u00f3digo SIEX" exists
        "label_col": "Cultivo SIEX",
        "csv_id": "C\u00f3digo"
    },
    "siexCropTypeValueCode": {
        "file": "Cultivo.csv",
        "id_col": "C\u00f3digo",
        "label_col": "Cultivo",
        "alt_label_col": "Lat\u00edn"
    },
    "siexFarmingSystemValueCode": {
        "file": "Sistema de cultivo.csv",
        "id_col": "C\u00f3digo",
        "label_col": "Sistema de cultivo"
    },
    "siexFertilizationMethodValueCode": {
        "file": "M\u00e9todo de aplicaci\u00f3n de fertilizante.csv",
        "id_col": "C\u00f3digo",
        "label_col": "M\u00e9todo de aplicaci\u00f3n de fertilizante"
    },
    "siexFertilizationTypeValueCode": {
        "file": "Tipo de fertilizaci\u00f3n.csv",
        "id_col": "C\u00f3digo",
        "label_col": "Tipo de fertilizaci\u00f3n"
    },
    "siexFertilizerMaterialValueCode": {
        "file": "Material fertilizante.csv",
        "id_col": "C\u00f3digo",
        "label_col": "Material fertilizante"
    },
    "siexIntendedCropUseValueCode": {
        "file": "Finalidad de la cosecha.csv",
        "id_col": "C\u00f3digo",
        "label_col": "Finalidad de la cosecha"
    },
    "siexIrrigationWaterSourceValueCode": {
        "file": "Procedencia del agua de riego.csv",
        "id_col": "C\u00f3digo",
        "label_col": "Procedencia del agua de riego"
    },
    "siexRootstockValueCode": {
        "file": "Portainjerto.csv",
        "id_col": "C\u00f3digo",
        "label_col": "Portainjerto"
    },
    "siexSoilCoverActivityValueCode": {
        "file": "Buenas pr\u00e1cticas.csv",
        "id_col": "C\u00f3digo",
        "label_col": "Buenas pr\u00e1cticas"
    },
    "siexSoilCoverTypeValueCode": {
        "file": "Tipo de cobertura del suelo.csv",
        "id_col": "C\u00f3digo",
        "label_col": "Tipo de cobertura del suelo"
    },
    "siexTreatmentEffectivenessValueCode": {
        "file": "Eficacia del tratamiento.csv",
        "id_col": "C\u00f3digo",
        "label_col": "Eficacia del tratamiento"
    },
    "siexTrellisingSystemValueCode": {
        "file": "Sistema de conducci\u00f3n.csv",
        "id_col": "C\u00f3digo",
        "label_col": "Sistema de conducci\u00f3n"
    }
}

CSV_DIR = r"c:\Users\khaosdev\Downloads\Catalogos_csv"
OUTPUT_FILE = r"c:\Users\khaosdev\Downloads\EDAAnOWL_ultimo\EDAAnOWL\src\0.6.1\vocabularies\siex-data.ttl"

def generate_rdf():
    g = Graph()
    g.bind("skos", SKOS)
    g.bind("siex-def", SIEX_DEF)
    g.bind("siex-kos", SIEX_KOS)
    g.bind("dct", DCTERMS)

    for scheme_name, config in MAPPING.items():
        file_path = os.path.join(CSV_DIR, config["file"])
        if not os.path.exists(file_path):
            print(f"Warning: File {file_path} not found. Skipping scheme {scheme_name}.")
            continue

        scheme_uri = SIEX_KOS[scheme_name]
        print(f"Processing {scheme_name} from {config['file']}...")

        with open(file_path, mode='r', encoding='latin-1') as f:
            # Using semicolon as delimiter based on previous head output
            reader = csv.DictReader(f, delimiter=';')
            processed_ids = set()
            for row in reader:
                concept_id = row.get(config["id_col"])
                if not concept_id or concept_id in processed_ids:
                    continue
                
                # Create URI for the concept
                # Pattern: siex-kos:[scheme]/[id]
                concept_uri = URIRef(f"{scheme_uri}/{concept_id}")
                
                g.add((concept_uri, RDF.type, SKOS.Concept))
                g.add((concept_uri, SKOS.inScheme, scheme_uri))
                g.add((concept_uri, SKOS.notation, Literal(concept_id)))
                
                label = row.get(config["label_col"])
                if label:
                    g.add((concept_uri, SKOS.prefLabel, Literal(label.strip(), lang="es")))
                
                alt_label = row.get(config.get("alt_label_col"))
                if alt_label:
                    g.add((concept_uri, SKOS.altLabel, Literal(alt_label.strip(), lang="la")))

                processed_ids.add(concept_id)

    g.serialize(destination=OUTPUT_FILE, format="turtle")
    print(f"Generated {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_rdf()
