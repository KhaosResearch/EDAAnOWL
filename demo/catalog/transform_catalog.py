import json
import rdflib
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import DCAT, DCTERMS, XSD, SKOS, FOAF

# Namespaces
EDAAN = Namespace("https://w3id.org/EDAAnOWL/")
IDS = Namespace("https://w3id.org/idsa/core/")
BIGALG = Namespace("https://w3id.org/BIGOWLAlgorithms/")
DQV = Namespace("http://www.w3.org/ns/dqv#")
PROV = Namespace("http://www.w3.org/ns/prov#")

def transform_catalog(input_file, output_file):
    g = Graph()
    
    # Bind prefixes
    g.bind("edaan", EDAAN)
    g.bind("ids", IDS)
    g.bind("dcat", DCAT)
    g.bind("dct", DCTERMS)
    g.bind("bigalg", BIGALG)
    g.bind("dqv", DQV)
    g.bind("prov", PROV)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle list or single object
    catalogs = data if isinstance(data, list) else [data]

    for catalog in catalogs:
        datasets = catalog.get("dcat:dataset", [])
        for ds in datasets:
            process_dataset(g, ds)

    g.serialize(destination=output_file, format="turtle")
    print(f"Transformation complete. Output saved to {output_file}")

def process_dataset(g, ds):
    ds_id = ds.get("@id")
    if not ds_id:
        return

    # Determine type: DataAsset or DataApp (PredictionApp, etc.)
    # Logic: Check mediaType or keywords
    media_type = ds.get("dcat:mediaType", "")
    keywords = ds.get("dcat:keyword", [])
    
    is_app = "application/vnd.datasphere.service" in media_type
    
    resource_uri = URIRef(f"https://w3id.org/EDAAnOWL/demo/{ds_id}")
    
    if is_app:
        # Heuristic: if keyword contains "forecasting" or "prediction", make it a PredictionApp
        if any(k.lower() in ["forecasting", "prediction"] for k in keywords):
            g.add((resource_uri, RDF.type, EDAAN.PredictionApp))
        else:
            g.add((resource_uri, RDF.type, IDS.DataApp))
            
        # Map keywords to BIGOWL Algorithms
        for k in keywords:
            if k == "RandomForest":
                g.add((resource_uri, EDAAN.implementsAlgorithm, BIGALG.RandomForest)) # Hypothetical property or use generic link
            elif k == "SARIMAX":
                g.add((resource_uri, EDAAN.implementsAlgorithm, BIGALG.SARIMAX))
                
    else:
        g.add((resource_uri, RDF.type, EDAAN.DataAsset))
        
        # Add provenance placeholder if it looks like a result
        if "indexes" in ds.get("dct:title", "").lower():
             g.add((resource_uri, PROV.wasGeneratedBy, Literal("UnknownAppExecution")))

    # Common properties
    g.add((resource_uri, DCTERMS.title, Literal(ds.get("dct:title", ""), lang="en")))
    g.add((resource_uri, DCTERMS.description, Literal(ds.get("dct:description", ""), lang="en")))
    
    # Fix: Add required :hasDomainSector
    sector_uri = EDAAN.Agriculture
    g.add((resource_uri, EDAAN.hasDomainSector, sector_uri))
    g.add((sector_uri, RDF.type, SKOS.Concept)) # Ensure it's typed

    # Create a Representation (ids:Representation / edaan:DataRepresentation)
    representation_uri = URIRef(f"{resource_uri}/representation")
    g.add((representation_uri, RDF.type, EDAAN.DataRepresentation))
    g.add((representation_uri, RDF.type, IDS.Representation))

    # Link Asset -> Representation
    g.add((resource_uri, IDS.representation, representation_uri))

    # Common properties for Representation
    if media_type:
        g.add((representation_uri, DCAT.mediaType, Literal(media_type)))
        g.add((representation_uri, DCTERMS.format, Literal(media_type)))

    # Create a DataProfile
    profile_uri = URIRef(f"{resource_uri}/profile")
    g.add((profile_uri, RDF.type, EDAAN.DataProfile))
    
    # Link Representation -> Profile (v0.4.1 pattern)
    g.add((representation_uri, EDAAN.conformsToProfile, profile_uri))
    
    # Fix: Add required :declaresDataClass
    g.add((profile_uri, EDAAN.declaresDataClass, URIRef("https://w3id.org/BIGOWLData/TabularData")))

    if not is_app:
        g.add((resource_uri, RDF.type, EDAAN.DataAsset))
        
        # Fix: Add required :servesObservableProperty
        obs_prop = EDAAN.CropYield
        g.add((resource_uri, EDAAN.servesObservableProperty, obs_prop))
        g.add((obs_prop, RDF.type, EDAAN.ObservableProperty))
        g.add((obs_prop, RDF.type, SKOS.Concept))

        # Add provenance placeholder if it looks like a result
        if "indexes" in ds.get("dct:title", "").lower():
             # Fix: prov:wasGeneratedBy must be an IRI to a DataApp
             app_uri = URIRef("https://w3id.org/EDAAnOWL/demo/UnknownApp")
             g.add((resource_uri, PROV.wasGeneratedBy, app_uri))
             g.add((app_uri, RDF.type, IDS.DataApp))
             g.add((app_uri, DCTERMS.title, Literal("Unknown App")))
             g.add((app_uri, EDAAN.hasDomainSector, sector_uri))

    # Add dummy metrics for demonstration (with MetricType for v0.3.2)
    metric_uri = URIRef(f"{profile_uri}/metric/completeness")
    g.add((metric_uri, RDF.type, EDAAN.QualityMetric))
    g.add((metric_uri, RDF.type, EDAAN.Metric))
    g.add((metric_uri, RDF.type, DQV.QualityMetric))
    g.add((metric_uri, EDAAN.metricType, EDAAN.mt_completeness))  # v0.3.2: MetricType vocabulary
    g.add((metric_uri, EDAAN.metricName, Literal("completeness")))
    g.add((metric_uri, EDAAN.metricValue, Literal("0.99", datatype=XSD.decimal)))
    g.add((profile_uri, EDAAN.hasMetric, metric_uri))

if __name__ == "__main__":
    transform_catalog("catalog.json", "output.ttl")
