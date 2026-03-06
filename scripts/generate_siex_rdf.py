import csv
import os
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import SKOS, DCTERMS, RDFS, XSD, OWL
import re

# Namespaces
SIEX_ONT = URIRef("https://w3id.org/EDAAnOWL/0.8.0/vocabularies/siex")
SIEX_DEF = Namespace("https://w3id.org/EDAAnOWL/0.8.0/vocabularies/siex#")
EDAAN = Namespace("https://w3id.org/EDAAnOWL/")

# Paths relative to this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CSV_DIR = os.environ.get("SIEX_CSV_DIR", os.path.abspath(os.path.join(PROJECT_ROOT, "..", "..", "Catalogos_csv")))
BASE_ONTOLOGY = os.path.join(PROJECT_ROOT, "src", "0.8.0", "vocabularies", "siex.ttl")

def clean_id(raw_str):
    if not raw_str: return ""
    return re.sub(r'[^a-zA-Z0-9-]', '', str(raw_str).strip())

def generate_rdf():
    g = Graph()
    g.bind("", SIEX_DEF)
    g.bind("siex", SIEX_ONT)
    g.bind("skos", SKOS)
    g.bind("dct", DCTERMS)
    g.bind("rdfs", RDFS)
    g.bind("owl", OWL)

    # LOAD BASE CLEAN
    if os.path.exists(BASE_ONTOLOGY):
        g.parse(BASE_ONTOLOGY, format="turtle")
        to_remove = []
        for s in list(g.subjects()):
            s_str = str(s)
            if s_str == str(SIEX_ONT): continue
            if "siex" in s_str: to_remove.append(s)
        for s in to_remove: g.remove((s, None, None))
        
    print("Base ontology loaded and cleaned.")

    # Helpers
    def get_scheme(name): return SIEX_DEF[f"siex_{name}_Scheme"]
    def get_concept(name, cid): return SIEX_DEF[f"siex_{name}_{cid}"]

    # 1. Unidades de medida
    print("Processing Unidades de medida...")
    f_path = os.path.join(CSV_DIR, "Unidades de medida.csv")
    scheme = get_scheme("MeasurementUnit")
    g.add((scheme, RDF.type, SKOS.ConceptScheme))
    g.add((scheme, SKOS.notation, Literal("siex_MeasurementUnit_Scheme")))
    g.add((scheme, SKOS.prefLabel, Literal("Esquema SIEX: Unidades de medida", lang="es")))
    if os.path.exists(f_path):
        with open(f_path, mode='r', encoding='cp1252') as f:
            for row in csv.DictReader(f, delimiter=';'):
                cid = clean_id(row.get("Código SIEX"))
                if not cid: continue
                curi = get_concept("MeasurementUnit", cid)
                g.add((curi, RDF.type, SKOS.Concept))
                g.add((curi, SKOS.inScheme, scheme))
                g.add((curi, SKOS.notation, Literal(cid)))
                if row.get("Unidades de medida"):
                    g.add((curi, SKOS.prefLabel, Literal(row["Unidades de medida"].strip(), lang="es")))

    # 2. Destino del cultivo
    print("Processing Destino del cultivo...")
    f_path = os.path.join(CSV_DIR, "Destino del cultivo.csv")
    scheme = get_scheme("CropDestination")
    g.add((scheme, RDF.type, SKOS.ConceptScheme))
    g.add((scheme, SKOS.notation, Literal("siex_CropDestination_Scheme")))
    g.add((scheme, SKOS.prefLabel, Literal("Esquema SIEX: Destino del cultivo", lang="es")))
    if os.path.exists(f_path):
        with open(f_path, mode='r', encoding='cp1252') as f:
            for row in csv.DictReader(f, delimiter=';'):
                cid = clean_id(row.get("Código SIEX"))
                if not cid: continue
                curi = get_concept("CropDestination", cid)
                g.add((curi, RDF.type, SKOS.Concept))
                g.add((curi, SKOS.inScheme, scheme))
                g.add((curi, SKOS.notation, Literal(cid)))
                if row.get("Destino del cultivo"):
                    g.add((curi, SKOS.prefLabel, Literal(row["Destino del cultivo"].strip(), lang="es")))

    # 3. Cultivo
    print("Processing Cultivos...")
    f_path = os.path.join(CSV_DIR, "Cultivo.csv")
    scheme_cultivo = get_scheme("CropType")
    g.add((scheme_cultivo, RDF.type, SKOS.ConceptScheme))
    g.add((scheme_cultivo, SKOS.notation, Literal("siex_CropType_Scheme")))
    g.add((scheme_cultivo, SKOS.prefLabel, Literal("Esquema SIEX: Cultivo", lang="es")))
    if os.path.exists(f_path):
        with open(f_path, mode='r', encoding='cp1252') as f:
            for row in csv.DictReader(f, delimiter=';'):
                cid = clean_id(row.get("Código"))
                if not cid: continue
                curi = get_concept("CropType", cid)
                g.add((curi, RDF.type, SKOS.Concept))
                g.add((curi, SKOS.inScheme, scheme_cultivo))
                g.add((curi, SKOS.notation, Literal(cid)))
                if row.get("Cultivo"):
                    g.add((curi, SKOS.prefLabel, Literal(row["Cultivo"].strip(), lang="es")))
                if row.get("Latín"):
                    g.add((curi, SKOS.altLabel, Literal(row["Latín"].strip(), lang="la")))

    # 4. Producto Vegetal
    print("Processing Producto Vegetal...")
    f_path = os.path.join(CSV_DIR, "Producto Vegetal.csv")
    scheme = get_scheme("CropProduct")
    g.add((scheme, RDF.type, SKOS.ConceptScheme))
    g.add((scheme, SKOS.notation, Literal("siex_CropProduct_Scheme")))
    g.add((scheme, SKOS.prefLabel, Literal("Esquema SIEX: Producto Vegetal", lang="es")))
    if os.path.exists(f_path):
        with open(f_path, mode='r', encoding='cp1252') as f:
            for row in csv.DictReader(f, delimiter=';'):
                cid = clean_id(row.get("Id"))
                if not cid: continue
                curi = get_concept("CropProduct", cid)
                g.add((curi, RDF.type, SKOS.Concept))
                g.add((curi, SKOS.inScheme, scheme))
                g.add((curi, SKOS.notation, Literal(cid)))
                if row.get("Producto"):
                    g.add((curi, SKOS.prefLabel, Literal(row["Producto"].strip(), lang="es")))
                
                cultivo_id = clean_id(row.get("Código SIEX"))
                if cultivo_id:
                    cultivo_uri = get_concept("CropType", cultivo_id)
                    g.add((curi, SKOS.relatedMatch, cultivo_uri))

    # 5. Variedad
    print("Processing Variedades...")
    f_path = os.path.join(CSV_DIR, "Variedad - Especie - Tipo.csv")
    scheme = get_scheme("CropVariety")
    g.add((scheme, RDF.type, SKOS.ConceptScheme))
    g.add((scheme, SKOS.notation, Literal("siex_CropVariety_Scheme")))
    g.add((scheme, SKOS.prefLabel, Literal("Esquema SIEX: Variedad", lang="es")))
    if os.path.exists(f_path):
        with open(f_path, mode='r', encoding='cp1252') as f:
            for row in csv.DictReader(f, delimiter=';'):
                c_cul = clean_id(row.get("Código cultivo"))
                c_var = clean_id(row.get("Código Variedad/ Especie/ Tipo"))
                if not c_cul or not c_var: continue
                cid = f"{c_cul}-{c_var}"
                curi = get_concept("CropVariety", cid)
                g.add((curi, RDF.type, SKOS.Concept))
                g.add((curi, SKOS.inScheme, scheme))
                g.add((curi, SKOS.notation, Literal(cid)))
                if row.get("Variedad/ Especie/ Tipo"):
                    g.add((curi, SKOS.prefLabel, Literal(row["Variedad/ Especie/ Tipo"].strip(), lang="es")))
                
                if c_cul:
                    cultivo_uri = get_concept("CropType", c_cul)
                    g.add((curi, SKOS.broadMatch, cultivo_uri))

    # 6. Especies animales y Familias
    print("Processing Animal Species...")
    f_path = os.path.join(CSV_DIR, "Especies animales.csv")
    scheme_species = get_scheme("AnimalSpecies")
    g.add((scheme_species, RDF.type, SKOS.ConceptScheme))
    g.add((scheme_species, SKOS.notation, Literal("siex_AnimalSpecies_Scheme")))
    g.add((scheme_species, SKOS.prefLabel, Literal("Esquema SIEX: Especies animales", lang="es")))
    
    scheme_family = get_scheme("AnimalFamily")
    g.add((scheme_family, RDF.type, SKOS.ConceptScheme))
    g.add((scheme_family, SKOS.notation, Literal("siex_AnimalFamily_Scheme")))
    g.add((scheme_family, SKOS.prefLabel, Literal("Esquema SIEX: Familias animales", lang="es")))
    
    species_name_map = {}
    if os.path.exists(f_path):
        with open(f_path, mode='r', encoding='cp1252') as f:
            for row in csv.DictReader(f, delimiter=';'):
                fam_id = clean_id(row.get("Código familia"))
                fam_uri = None
                if fam_id:
                    fam_uri = get_concept("AnimalFamily", fam_id)
                    g.add((fam_uri, RDF.type, SKOS.Concept))
                    g.add((fam_uri, SKOS.inScheme, scheme_family))
                    g.add((fam_uri, SKOS.notation, Literal(fam_id)))
                    if row.get("Familia"):
                        g.add((fam_uri, SKOS.prefLabel, Literal(row["Familia"].strip(), lang="es")))

                sp_id = clean_id(row.get("Código SIEX"))
                sp_name = str(row.get("Especies animales", "")).strip()
                if sp_id:
                    sp_uri = get_concept("AnimalSpecies", sp_id)
                    g.add((sp_uri, RDF.type, SKOS.Concept))
                    g.add((sp_uri, SKOS.inScheme, scheme_species))
                    g.add((sp_uri, SKOS.notation, Literal(sp_id)))
                    if sp_name:
                        g.add((sp_uri, SKOS.prefLabel, Literal(sp_name, lang="es")))
                        species_name_map[sp_name.lower()] = sp_uri
                    
                    if fam_uri:
                        g.add((sp_uri, SKOS.broadMatch, fam_uri))

    # 7. Razas de ganado
    print("Processing Animal Breeds...")
    f_path = os.path.join(CSV_DIR, "Catálogo oficial de razas de ganado de España.csv")
    scheme = get_scheme("AnimalBreed")
    g.add((scheme, RDF.type, SKOS.ConceptScheme))
    g.add((scheme, SKOS.notation, Literal("siex_AnimalBreed_Scheme")))
    g.add((scheme, SKOS.prefLabel, Literal("Esquema SIEX: Razas animales", lang="es")))
    if os.path.exists(f_path):
        with open(f_path, mode='r', encoding='cp1252') as f:
            for row in csv.DictReader(f, delimiter=';'):
                cid = clean_id(row.get("Código"))
                if not cid: continue
                curi = get_concept("AnimalBreed", cid)
                g.add((curi, RDF.type, SKOS.Concept))
                g.add((curi, SKOS.inScheme, scheme))
                g.add((curi, SKOS.notation, Literal(cid)))
                if row.get("Raza"):
                    g.add((curi, SKOS.prefLabel, Literal(row["Raza"].strip(), lang="es")))
                
                sp_name = str(row.get("Especie", "")).strip().lower()
                if sp_name in species_name_map:
                    g.add((curi, SKOS.broadMatch, species_name_map[sp_name]))

    print("Serializing graph...")
    out = g.serialize(format="turtle")
    match = re.search(r"@prefix (\w+): <https://w3id\.org/EDAAnOWL/0\.8\.0/vocabularies/siex> \.", out)
    if match:
        prefix_name = match.group(1)
        if "@prefix siex:" not in out:
            out = out.replace(f"@prefix {prefix_name}:", "@prefix siex:")
            out = out.replace(f"{prefix_name}:", "siex:")
    
    with open(BASE_ONTOLOGY, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Generated and CLEANED vocabulary at {BASE_ONTOLOGY}")

if __name__ == "__main__":
    generate_rdf()
