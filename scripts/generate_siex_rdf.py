import csv
import os
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import SKOS, DCTERMS, RDFS, XSD, OWL
import re

# Namespaces
SIEX_ONT = URIRef("https://w3id.org/EDAAnOWL/0.7.0/vocabularies/siex")
SIEX_DEF = Namespace("https://w3id.org/EDAAnOWL/0.7.0/vocabularies/siex#")
SIEX_KOS = Namespace("https://w3id.org/EDAAnOWL/0.7.0/vocabularies/siex/kos/")
EDAAN = Namespace("https://w3id.org/EDAAnOWL/")

# Configuration: Mapping SIEX Schemes to CSV file names
MAPPING = {
    "siexCropProductValueCode": {"file": "Producto Vegetal.csv", "id_col": "Código SIEX", "label_col": "Cultivo SIEX"},
    "siexCropTypeValueCode": {"file": "Cultivo.csv", "id_col": "Código", "label_col": "Cultivo", "alt_label_col": "Latín"},
    "siexFarmingSystemValueCode": {"file": "Sistema de cultivo.csv", "id_col": "Código SIEX", "label_col": "Sistema de cultivo"},
    "siexFertilizationMethodValueCode": {"file": "Método de aplicación de fertilizante.csv", "id_col": "Código SIEX", "label_col": "Método de fertilización"},
    "siexFertilizationTypeValueCode": {"file": "Tipo de fertilización.csv", "id_col": "Código SIEX", "label_col": "Tipo de fertilización"},
    "siexFertilizerMaterialValueCode": {"file": "Material fertilizante.csv", "id_col": "Código SIEX", "label_col": "Tipo de material"},
    "siexIntendedCropUseValueCode": {"file": "Finalidad de la cosecha.csv", "id_col": "Código SIEX", "label_col": "Declaración de cosecha / producción"},
    "siexIrrigationWaterSourceValueCode": {"file": "Procedencia del agua de riego.csv", "id_col": "Código SIEX", "label_col": "Procedencia del agua de riego"},
    "siexRootstockValueCode": {"file": "Portainjerto.csv", "id_col": "Código SIEX", "label_col": "Portainjerto"},
    "siexSoilCoverActivityValueCode": {"file": "Buenas prácticas.csv", "id_col": "Código SIEX", "label_col": "Buenas prácticas"},
    "siexSoilCoverTypeValueCode": {"file": "Tipo de cobertura del suelo.csv", "id_col": "Código SIEX", "label_col": "Tipo de cobertura del suelo"},
    "siexTreatmentEffectivenessValueCode": {"file": "Eficacia del tratamiento.csv", "id_col": "Código SIEX", "label_col": "Eficacia del tratamiento"},
    "siexTrellisingSystemValueCode": {"file": "Sistema de conducción.csv", "id_col": "Código SIEX", "label_col": "Sistema de conducción"}
}

CSV_DIR = r"c:\Users\khaosdev\Downloads\Catalogos_csv"
BASE_ONTOLOGY = r"c:\Users\khaosdev\Downloads\EDAAnOWL_ultimo\EDAAnOWL\src\0.7.0\vocabularies\siex.ttl"

def generate_rdf():
    g = Graph()
    g.bind("skos", SKOS)
    g.bind("siex-def", SIEX_DEF)
    g.bind("siex-kos", SIEX_KOS)
    g.bind("dct", DCTERMS)

    for scheme_name, config in MAPPING.items():
        file_path = os.path.join(CSV_DIR, config["file"])
        if not os.path.exists(file_path):
            print(f"Warning: File {file_path} not found.")
            continue
        scheme_uri = SIEX_KOS[scheme_name]
        g.add((scheme_uri, RDF.type, SKOS.ConceptScheme))
        g.add((scheme_uri, SKOS.notation, Literal(scheme_name)))
        g.add((scheme_uri, SKOS.prefLabel, Literal(f"Esquema SIEX: {config['file'].replace('.csv', '')}", lang="es")))
        with open(file_path, mode='r', encoding='latin-1') as f:
            reader = csv.DictReader(f, delimiter=';')
            processed_ids = set()
            for row in reader:
                cid = row.get(config["id_col"])
                if not cid or cid in processed_ids: continue
                curi = URIRef(f"{scheme_uri}/{cid}")
                g.add((curi, RDF.type, SKOS.Concept))
                g.add((curi, SKOS.inScheme, scheme_uri))
                g.add((curi, SKOS.notation, Literal(cid)))
                lbl = row.get(config["label_col"])
                if lbl: g.add((curi, SKOS.prefLabel, Literal(lbl.strip(), lang="es")))
                alt = row.get(config.get("alt_label_col"))
                if alt: g.add((curi, SKOS.altLabel, Literal(alt.strip(), lang="la")))
                processed_ids.add(cid)

    unified_g = Graph()
    unified_g.bind("", SIEX_DEF)
    unified_g.bind("siex", SIEX_ONT)
    unified_g.bind("skos", SKOS)
    unified_g.bind("dct", DCTERMS)
    unified_g.bind("rdfs", RDFS)
    unified_g.bind("owl", OWL)
    
    # LOAD BASE CLEAN
    if os.path.exists(BASE_ONTOLOGY):
        unified_g.parse(BASE_ONTOLOGY, format="turtle")
        to_remove = []
        # Keep ONLY strictly the Ontology metadata subject
        for s in list(unified_g.subjects()):
            s_str = str(s)
            if s_str == str(SIEX_ONT): continue
            if "siex" in s_str: to_remove.append(s)
        for s in to_remove: unified_g.remove((s, None, None))
    
    # TRANSLATE & ADD
    for s, p, o in g:
        s_str = str(s)
        if "/kos/" in s_str:
            parts = s_str.split("/")
            idx = parts.index("kos")
            rem = parts[idx+1:]
            core = rem[0].replace("siex", "").replace("ValueCode", "")
            if len(rem) == 2: new_s = SIEX_DEF[f"siex_{core}_{rem[1]}"]
            else: new_s = SIEX_DEF[f"siex_{core}_Scheme"]
            
            new_o = o
            o_str = str(o)
            if "/kos/" in o_str:
                oparts = o_str.split("/")
                oidx = oparts.index("kos")
                orem = oparts[oidx+1:]
                ocore = orem[0].replace("siex", "").replace("ValueCode", "")
                if len(orem) == 2: new_o = SIEX_DEF[f"siex_{ocore}_{orem[1]}"]
                else: new_o = SIEX_DEF[f"siex_{ocore}_Scheme"]
            unified_g.add((new_s, p, new_o))
        else:
            unified_g.add((s, p, o))
    
    # FINAL POST-PROCESSING: Fix RDFlib's prefixing of Ontology subject
    # We output Turtle and then manually clean up 'defaultNN:' at the start
    out = unified_g.serialize(format="turtle")
    
    # Find the prefix RDFlib generated for the base URI if it didn't use 'siex'
    # Look for @prefix defaultXX: <https://w3id.org/EDAAnOWL/0.7.0/vocabularies/siex> .
    match = re.search(r"@prefix (\w+): <https://w3id\.org/EDAAnOWL/0\.7\.0/vocabularies/siex> \.", out)
    if match:
        prefix_name = match.group(1)
        # 1. Add siex prefix if missing
        if "@prefix siex:" not in out:
            out = out.replace(f"@prefix {prefix_name}:", "@prefix siex:")
            out = out.replace(f"{prefix_name}:", "siex:")
    
    with open(BASE_ONTOLOGY, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Generated and CLEANED vocabulary at {BASE_ONTOLOGY}")

if __name__ == "__main__":
    generate_rdf()
