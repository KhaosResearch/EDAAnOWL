import csv
import os
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import SKOS, DCTERMS, RDFS, XSD, OWL
import re

# Namespaces
SIEX_DEF = Namespace("https://w3id.org/EDAAnOWL/0.7.0/vocabularies/siex/")
SIEX_KOS = Namespace("https://w3id.org/EDAAnOWL/0.7.0/vocabularies/siex/kos/")
EDAAN = Namespace("https://w3id.org/EDAAnOWL/")

# Configuration: Mapping SIEX Schemes to CSV file names and their columns
MAPPING = {
    "siexCropProductValueCode": {
        "file": "Producto Vegetal.csv",
        "id_col": "C\u00f3digo SIEX",
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
        "id_col": "C\u00f3digo SIEX",
        "label_col": "Sistema de cultivo"
    },
    "siexFertilizationMethodValueCode": {
        "file": "M\u00e9todo de aplicación de fertilizante.csv",
        "id_col": "C\u00f3digo SIEX",
        "label_col": "M\u00e9todo de fertilizaci\u00f3n"
    },
    "siexFertilizationTypeValueCode": {
        "file": "Tipo de fertilizaci\u00f3n.csv",
        "id_col": "C\u00f3digo SIEX",
        "label_col": "Tipo de fertilizaci\u00f3n"
    },
    "siexFertilizerMaterialValueCode": {
        "file": "Material fertilizante.csv",
        "id_col": "C\u00f3digo SIEX",
        "label_col": "Tipo de material"
    },
    "siexIntendedCropUseValueCode": {
        "file": "Finalidad de la cosecha.csv",
        "id_col": "C\u00f3digo SIEX",
        "label_col": "Declaraci\u00f3n de cosecha / producci\u00f3n"
    },
    "siexIrrigationWaterSourceValueCode": {
        "file": "Procedencia del agua de riego.csv",
        "id_col": "C\u00f3digo SIEX",
        "label_col": "Procedencia del agua de riego"
    },
    "siexRootstockValueCode": {
        "file": "Portainjerto.csv",
        "id_col": "C\u00f3digo SIEX",
        "label_col": "Portainjerto"
    },
    "siexSoilCoverActivityValueCode": {
        "file": "Buenas pr\u00e1cticas.csv",
        "id_col": "C\u00f3digo SIEX",
        "label_col": "Buenas pr\u00e1cticas"
    },
    "siexSoilCoverTypeValueCode": {
        "file": "Tipo de cobertura del suelo.csv",
        "id_col": "C\u00f3digo SIEX",
        "label_col": "Tipo de cobertura del suelo"
    },
    "siexTreatmentEffectivenessValueCode": {
        "file": "Eficacia del tratamiento.csv",
        "id_col": "C\u00f3digo SIEX",
        "label_col": "Eficacia del tratamiento"
    },
    "siexTrellisingSystemValueCode": {
        "file": "Sistema de conducci\u00f3n.csv",
        "id_col": "C\u00f3digo SIEX",
        "label_col": "Sistema de conducci\u00f3n"
    }
}

CSV_DIR = r"c:\Users\khaosdev\Downloads\Catalogos_csv"
OUTPUT_FILE = r"c:\Users\khaosdev\Downloads\EDAAnOWL_ultimo\EDAAnOWL\src\0.7.0\vocabularies\siex-data.ttl"

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
        core_name_simple = scheme_name.replace("siex", "").replace("ValueCode", "")
        
        print(f"Processing {scheme_name} ({core_name_simple}) from {config['file']}...")

        # Add the scheme definition
        g.add((scheme_uri, RDF.type, SKOS.ConceptScheme))
        g.add((scheme_uri, SKOS.notation, Literal(scheme_name)))
        # Use the name of the file or a custom label
        scheme_label = config["file"].replace(".csv", "")
        g.add((scheme_uri, SKOS.prefLabel, Literal(f"Esquema SIEX: {scheme_label}", lang="es")))

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

    # Merge with the base ontology file
    BASE_ONTOLOGY = r"c:\Users\khaosdev\Downloads\EDAAnOWL_ultimo\EDAAnOWL\src\0.7.0\vocabularies\siex.ttl"
    
    # We create a new graph to ensure a clean serialization of the unified vocabulary
    unified_g = Graph()
    
    # Bind prefixes (v0.7.0 style)
    unified_g.bind("", SIEX_DEF)
    unified_g.bind("skos", SKOS)
    unified_g.bind("dct", DCTERMS)
    unified_g.bind("rdfs", RDFS)
    unified_g.bind("owl", OWL)
    unified_g.bind("xsd", XSD)
    unified_g.bind("edaan", EDAAN)
    
    # Load the base part (the ontology and schemes)
    if os.path.exists(BASE_ONTOLOGY):
        unified_g.parse(BASE_ONTOLOGY, format="turtle")
        
        # Cleanup: Remove ALL existing SIEX concepts and schemes 
        # to avoid duplicates and stale labels (like old English ones)
        # We match both versioned and unversioned patterns
        patterns = [
            re.compile(r"https://w3id.org/EDAAnOWL/siex_.*"),
            re.compile(r"https://w3id.org/EDAAnOWL/0\.7\.0/vocabularies/siex/siex_.*")
        ]
        
        for s in list(unified_g.subjects()):
            s_str = str(s)
            if any(p.match(s_str) for p in patterns):
                for p, o in list(unified_g.predicate_objects(s)):
                    unified_g.remove((s, p, o))
    
    # Process and add the generated data from our current graph
    for s, p, o in g:
        # Convert the temporary URIs to the new permanent pattern
        # From: .../siex/kos/siexCropProductValueCode/1
        # To: https://w3id.org/EDAAnOWL/siex_CropProduct_1
        
        s_str = str(s)
        if "/kos/" in s_str:
            parts = s_str.split("/")
            idx_kos = parts.index("kos")
            remaining = parts[idx_kos + 1 :]

            if len(remaining) == 2:  # It's a Concept: .../kos/SchemeName/ID
                scheme_full = remaining[0]
                item_id = remaining[1]
                core_name = scheme_full.replace("siex", "").replace("ValueCode", "")
                new_s = SIEX_DEF[f"siex_{core_name}_{item_id}"]
            elif len(remaining) == 1:  # It's the Scheme itself: .../kos/SchemeName
                scheme_full = remaining[0]
                core_name = scheme_full.replace("siex", "").replace("ValueCode", "")
                new_s = SIEX_DEF[f"siex_{core_name}_Scheme"]
            else:
                new_s = s

            # Translate Objects too if they are SIEX URIs
            new_o = o
            o_str = str(o)
            if "/kos/" in o_str:
                o_parts = o_str.split("/")
                o_idx_kos = o_parts.index("kos")
                o_remaining = o_parts[o_idx_kos + 1 :]
                
                if len(o_remaining) == 2: # Concept as object
                    o_scheme_full = o_remaining[0]
                    o_item_id = o_remaining[1]
                    o_core_name = o_scheme_full.replace("siex", "").replace("ValueCode", "")
                    new_o = SIEX_DEF[f"siex_{o_core_name}_{o_item_id}"]
                elif len(o_remaining) == 1: # Scheme as object (common for skos:inScheme)
                    o_scheme_full = o_remaining[0]
                    o_core_name = o_scheme_full.replace("siex", "").replace("ValueCode", "")
                    new_o = SIEX_DEF[f"siex_{o_core_name}_Scheme"]

            unified_g.add((new_s, p, new_o))
        else:
            unified_g.add((s, p, o))
    
    # Serialize to siex.ttl
    # With no slashes in local names, rdflib will use :prefix automatically
    unified_g.serialize(destination=BASE_ONTOLOGY, format="turtle")
    print(f"Generated unified and NATIVE vocabulary at {BASE_ONTOLOGY}")

if __name__ == "__main__":
    generate_rdf()
