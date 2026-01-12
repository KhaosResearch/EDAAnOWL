"""
EDAAnOWL Demo: CSV to RDF Transformation
=========================================

This script transforms olive grove monitoring data (CSV) into EDAAnOWL RDF,
demonstrating a complete matchmaking scenario aligned with USE_CASES.md.

The generated DataAsset is designed to be COMPATIBLE with the OliveYieldPredictor
app from Use Case 1, serving all required observable properties.
"""

import csv
from datetime import datetime
from rdflib import Graph, Literal, RDF, URIRef, Namespace, BNode
from rdflib.namespace import DCAT, DCTERMS, XSD, SKOS

# Namespaces
EDAAN = Namespace("https://w3id.org/EDAAnOWL/")
IDS = Namespace("https://w3id.org/idsa/core/")
TIME = Namespace("http://www.w3.org/2006/time#")
GSP = Namespace("http://www.opengis.net/ont/geosparql#")
LOCN = Namespace("http://www.w3.org/ns/locn#")
DQV = Namespace("http://www.w3.org/ns/dqv#")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
OLIVE = Namespace("https://w3id.org/EDAAnOWL/demo/olive-grove/")


def transform_csv(input_file: str, output_file: str):
    """Transform olive grove CSV to EDAAnOWL RDF."""
    g = Graph()
    
    # Bind prefixes
    g.bind("edaan", EDAAN)
    g.bind("ids", IDS)
    g.bind("dcat", DCAT)
    g.bind("dct", DCTERMS)
    g.bind("time", TIME)
    g.bind("gsp", GSP)
    g.bind("locn", LOCN)
    g.bind("dqv", DQV)
    g.bind("vcard", VCARD)
    g.bind("olive", OLIVE)
    g.bind("skos", SKOS)
    
    # Read CSV and compute statistics
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Compute metrics from data
    record_count = len(rows)
    
    # Spatial bounds (bounding box)
    lats = [float(r['latitude']) for r in rows]
    lons = [float(r['longitude']) for r in rows]
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    
    # Temporal bounds
    dates = [datetime.strptime(r['observation_date'], '%Y-%m-%d') for r in rows]
    min_date, max_date = min(dates), max(dates)
    
    # Completeness (check for empty values)
    total_cells = record_count * 10  # 10 columns
    non_empty = sum(1 for r in rows for v in r.values() if v.strip())
    completeness = non_empty / total_cells
    
    # ========== THE DATASET (DataAsset) ==========
    dataset_uri = OLIVE.OliveGroveMonitoring2024
    
    g.add((dataset_uri, RDF.type, EDAAN.SpatialTemporalAsset))
    g.add((dataset_uri, RDF.type, EDAAN.DataAsset))
    g.add((dataset_uri, DCTERMS.title, Literal("Olive Grove Monitoring Dataset - Jaén 2024", lang="en")))
    g.add((dataset_uri, DCTERMS.title, Literal("Dataset de Monitorización de Olivar - Jaén 2024", lang="es")))
    g.add((dataset_uri, DCTERMS.description, Literal(
        "Multi-temporal monitoring data for olive groves in Jaén province, "
        "containing vegetation indices, meteorological variables, soil properties, and yield data. "
        "Compatible with yield prediction and water stress analysis applications.",
        lang="en"
    )))
    g.add((dataset_uri, DCTERMS.created, Literal("2024-11-20", datatype=XSD.date)))
    
    # Sector and topic
    g.add((dataset_uri, EDAAN.hasDomainSector, EDAAN.agriculture))
    g.add((dataset_uri, EDAAN.topic, EDAAN.agro_olive))
    
    # Observable properties this dataset SERVES (matches OliveYieldPredictor requirements!)
    g.add((dataset_uri, EDAAN.servesObservableProperty, EDAAN.ndvi))
    g.add((dataset_uri, EDAAN.servesObservableProperty, EDAAN.temperature))
    g.add((dataset_uri, EDAAN.servesObservableProperty, EDAAN.precipitation))
    g.add((dataset_uri, EDAAN.servesObservableProperty, EDAAN.soilMoisture))
    g.add((dataset_uri, EDAAN.servesObservableProperty, EDAAN["yield"]))
    
    # Create a Representation (ids:Representation / edaan:DataRepresentation)
    representation_uri = OLIVE.OliveMonitoringRepresentation
    g.add((representation_uri, RDF.type, EDAAN.DataRepresentation))
    g.add((representation_uri, RDF.type, IDS.Representation))
    g.add((representation_uri, DCAT.mediaType, Literal("text/csv")))
    g.add((representation_uri, DCTERMS.format, Literal("CSV")))

    # Link Asset -> Representation
    g.add((dataset_uri, IDS.representation, representation_uri))

    # Link Representation -> Profile (v0.4.1 pattern)
    g.add((representation_uri, EDAAN.conformsToProfile, OLIVE.OliveMonitoringProfile))

    # Spatial coverage (bounding box as WKT)
    spatial_coverage = BNode()
    g.add((spatial_coverage, RDF.type, LOCN.Geometry))
    wkt = f"POLYGON(({min_lon} {min_lat}, {max_lon} {min_lat}, {max_lon} {max_lat}, {min_lon} {max_lat}, {min_lon} {min_lat}))"
    g.add((spatial_coverage, GSP.asWKT, Literal(wkt, datatype=GSP.wktLiteral)))
    g.add((dataset_uri, EDAAN.hasSpatialCoverage, spatial_coverage))
    
    # Temporal coverage
    temporal_coverage = BNode()
    g.add((temporal_coverage, RDF.type, TIME.Interval))
    
    begin = BNode()
    g.add((begin, TIME.inXSDDate, Literal(min_date.strftime('%Y-%m-%d'), datatype=XSD.date)))
    g.add((temporal_coverage, TIME.hasBeginning, begin))
    
    end = BNode()
    g.add((end, TIME.inXSDDate, Literal(max_date.strftime('%Y-%m-%d'), datatype=XSD.date)))
    g.add((temporal_coverage, TIME.hasEnd, end))
    
    g.add((dataset_uri, EDAAN.hasTemporalCoverage, temporal_coverage))
    
    # Support contact
    contact = BNode()
    g.add((contact, RDF.type, VCARD.Kind))
    g.add((contact, VCARD.fn, Literal("Khaos Research Group")))
    g.add((contact, VCARD.hasEmail, URIRef("mailto:khaos@uma.es")))
    g.add((dataset_uri, EDAAN.supportContact, contact))
    
    # Additional properties
    g.add((dataset_uri, EDAAN.isAlive, Literal(True)))
    g.add((dataset_uri, EDAAN.accessType, Literal("Download")))
    
    # ========== THE PROFILE (DataProfile with MetricTypes) ==========
    profile_uri = OLIVE.OliveMonitoringProfile
    
    g.add((profile_uri, RDF.type, EDAAN.DataProfile))
    g.add((profile_uri, DCTERMS.title, Literal("Olive Grove Monitoring Profile", lang="en")))
    
    # Data class
    g.add((profile_uri, EDAAN.declaresDataClass, EDAAN.tabular))
    
    # Declared observed properties
    g.add((profile_uri, EDAAN.declaresObservedProperty, EDAAN.ndvi))
    g.add((profile_uri, EDAAN.declaresObservedProperty, EDAAN.temperature))
    g.add((profile_uri, EDAAN.declaresObservedProperty, EDAAN.precipitation))
    g.add((profile_uri, EDAAN.declaresObservedProperty, EDAAN.soilMoisture))
    g.add((profile_uri, EDAAN.declaresObservedProperty, EDAAN["yield"]))
    
    # Technical properties
    g.add((profile_uri, DCAT.temporalResolution, Literal("P1M", datatype=XSD.duration)))
    g.add((profile_uri, EDAAN.hasCRS, URIRef("http://www.opengis.net/def/crs/EPSG/0/4326")))
    
    # ========== QUALITY METRICS (with MetricType) ==========
    
    # Metric 1: Record Count
    metric1 = BNode()
    g.add((metric1, RDF.type, EDAAN.Metric))
    g.add((metric1, RDF.type, EDAAN.QualityMetric))
    g.add((metric1, RDF.type, DQV.QualityMetric))
    g.add((metric1, EDAAN.metricType, EDAAN.mt_recordCount))
    g.add((metric1, EDAAN.metricName, Literal("recordCount")))
    g.add((metric1, EDAAN.metricValue, Literal(record_count, datatype=XSD.integer)))
    g.add((metric1, EDAAN.computedAt, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
    g.add((profile_uri, EDAAN.hasMetric, metric1))
    
    # Metric 2: Completeness
    metric2 = BNode()
    g.add((metric2, RDF.type, EDAAN.Metric))
    g.add((metric2, RDF.type, EDAAN.QualityMetric))
    g.add((metric2, RDF.type, DQV.QualityMetric))
    g.add((metric2, EDAAN.metricType, EDAAN.mt_completeness))
    g.add((metric2, EDAAN.metricName, Literal("completeness")))
    g.add((metric2, EDAAN.metricValue, Literal(round(completeness, 2), datatype=XSD.decimal)))
    g.add((metric2, EDAAN.metricUnit, Literal("ratio")))
    g.add((metric2, EDAAN.computedAt, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
    g.add((profile_uri, EDAAN.hasMetric, metric2))
    
    # Metric 3: Feature Count
    metric3 = BNode()
    g.add((metric3, RDF.type, EDAAN.Metric))
    g.add((metric3, RDF.type, EDAAN.QualityMetric))
    g.add((metric3, EDAAN.metricType, EDAAN.mt_featureCount))
    g.add((metric3, EDAAN.metricName, Literal("featureCount")))
    g.add((metric3, EDAAN.metricValue, Literal(10, datatype=XSD.integer)))  # 10 columns
    g.add((profile_uri, EDAAN.hasMetric, metric3))
    
    # Metric 4: Spatial Extent
    metric4 = BNode()
    g.add((metric4, RDF.type, EDAAN.Metric))
    g.add((metric4, RDF.type, EDAAN.QualityMetric))
    g.add((metric4, EDAAN.metricType, EDAAN.mt_spatialExtent))
    g.add((metric4, EDAAN.metricName, Literal("spatialExtent")))
    g.add((metric4, EDAAN.metricValue, Literal(f"Jaén, Spain ({min_lat:.4f},{min_lon:.4f} to {max_lat:.4f},{max_lon:.4f})")))
    g.add((profile_uri, EDAAN.hasMetric, metric4))
    
    # Metric 5: Temporal Extent
    metric5 = BNode()
    g.add((metric5, RDF.type, EDAAN.Metric))
    g.add((metric5, RDF.type, EDAAN.QualityMetric))
    g.add((metric5, EDAAN.metricType, EDAAN.mt_temporalExtent))
    g.add((metric5, EDAAN.metricName, Literal("temporalExtent")))
    g.add((metric5, EDAAN.metricValue, Literal(f"{min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")))
    g.add((profile_uri, EDAAN.hasMetric, metric5))
    
    # Serialize
    g.serialize(destination=output_file, format="turtle")
    print(f"✅ Transformation complete!")
    print(f"   Input:  {input_file} ({record_count} records)")
    print(f"   Output: {output_file} ({len(g)} triples)")
    print(f"\n📊 Computed Metrics:")
    print(f"   - Record Count: {record_count}")
    print(f"   - Completeness: {completeness:.2%}")
    print(f"   - Spatial Extent: {min_lat:.4f},{min_lon:.4f} → {max_lat:.4f},{max_lon:.4f}")
    print(f"   - Temporal Extent: {min_date.date()} → {max_date.date()}")
    print(f"\n🔗 This dataset is COMPATIBLE with OliveYieldPredictor from USE_CASES.md!")
    print(f"   It serves: ndvi, temperature, precipitation, soilMoisture, yield")


if __name__ == "__main__":
    transform_csv("olive-grove-monitoring-2024.csv", "output.ttl")
