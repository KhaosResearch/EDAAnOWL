#!/usr/bin/env python3
"""
EDAAnOWL SHACL Validation Script
================================

Supports multi-version validation with automatic vocabulary detection.
For v0.6.0+, it implements the Zero-Local policy (fetching external vocabs or 
relying on the main ontology and stubs).
"""

import sys
import os
import re
from pathlib import Path

try:
    from pyshacl import validate
    from rdflib import Graph, Namespace
except ImportError:
    print("❌ Please install dependencies: pip install rdflib pyshacl")
    sys.exit(1)

RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
SH = Namespace("http://www.w3.org/ns/shacl#")

def find_latest_version(src_dir: Path) -> str:
    """Find the latest semver version folder in src/"""
    versions = []
    if not src_dir.exists():
        return None
    for item in src_dir.iterdir():
        if item.is_dir() and re.match(r'^\d+\.\d+\.\d+$', item.name):
            versions.append(item.name)
    if not versions:
        return None
    # Sort by semver
    versions.sort(key=lambda v: [int(x) for x in v.split('.')])
    return versions[-1]

def validate_file(data_file: Path, shape_files: list, ontology_file: Path, vocab_files: list = None, fmt: str = 'turtle') -> bool:
    """Validate a single data file against shapes."""
    print(f"\n📋 Validating: {data_file.name} (Format: {fmt})")
    
    report_dir = Path("validation_reports")
    report_dir.mkdir(exist_ok=True)
    report_file = report_dir / f"report_{data_file.stem}.txt"

    # Load data graph
    data = Graph()
    data.parse(str(data_file), format=fmt)
    
    # Load ontology
    merged = Graph()
    merged += data
    merged.parse(str(ontology_file), format='turtle')
    
    # Load vocabs if they exist
    if vocab_files:
        for vocab in vocab_files:
            if vocab.exists():
                merged.parse(str(vocab), format='turtle')
    
    # Load and merge shapes
    shapes = Graph()
    for sf in shape_files:
        if sf.exists():
            shapes.parse(str(sf), format='turtle')
    
    # Validate
    conforms, results_graph, results_text = validate(
        merged,
        shacl_graph=shapes,
        ont_graph=None,
        inference='rdfs',
        debug=False
    )
    
    # Check for sh:Violation
    violations = list(results_graph.subjects(SH.resultSeverity, SH.Violation))
    is_success = len(violations) == 0
    
    if is_success:
        print(f"   ✅ Success (No Violations)")
    else:
        print(f"   ❌ Failed ({len(violations)} Violations found)")
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(results_text)
        print(f"      📄 Report saved to: {report_file}")
    
    return is_success

def main():
    script_dir = Path(__file__).parent.resolve()
    root_dir = script_dir.parent
    src_dir = root_dir / 'src'
    
    version = find_latest_version(src_dir)
    if not version:
        print("❌ No version folder found in src/")
        sys.exit(1)
    
    print(f"🔍 EDAAnOWL SHACL Validation (v{version})")
    print("=" * 50)
    
    version_dir = src_dir / version
    ontology_file = version_dir / 'EDAAnOWL.ttl'
    
    # Official DCAT-AP-ES SHACL shapes (modular)
    shape_dir = version_dir / 'shapes' / 'compliance' / 'dcat-ap-es' / '1.0.0'
    shape_files = [
        shape_dir / 'shacl_common_shapes.ttl',
        shape_dir / 'shacl_catalog_shape.ttl',
        shape_dir / 'shacl_dataset_shape.ttl',
        shape_dir / 'shacl_distribution_shape.ttl',
        shape_dir / 'shacl_dataservice_shape.ttl',
        shape_dir / 'shacl_mdr-vocabularies.shape.ttl',
        # Our own internal shapes
        version_dir / 'shapes' / 'edaan-shapes.ttl',
        version_dir / 'shapes' / 'idsa-shapes.ttl',
        version_dir / 'shapes' / 'cred-alignment-shapes.ttl',
    ]
    
    # Legacy vocabularies (pre-0.6.0)
    vocab_files = []
    major, minor, patch = map(int, version.split('.'))
    if major == 0 and minor < 6:
        vocab_dir = version_dir / 'vocabularies'
        vocab_names = [
            'metric-types.ttl', 'observed-properties.ttl', 'agro-vocab.ttl',
            'datatype-scheme.ttl', 'data-theme.ttl', 'crs-vocab.ttl', 'access-rights.ttl'
        ]
        vocab_files = [vocab_dir / name for name in vocab_names]
    
    # Examples to validate
    examples_dir = version_dir / 'examples'
    official_examples_dir = examples_dir / 'dcat-ap-es' / 'rdf' / '1.0.0'
    
    data_files = [
        (ontology_file, 'turtle'),
        (examples_dir / 'test-consistency.ttl', 'turtle'),
        (examples_dir / 'eo-instances.ttl', 'turtle'),
        (examples_dir / 'cred-asset-example.ttl', 'turtle'),
    ]
    
    # Add official examples if they exist
    if official_examples_dir.exists():
        for rdf_file in official_examples_dir.glob('*.rdf'):
            data_files.append((rdf_file, 'xml'))

    all_valid = True
    for data_file, fmt in data_files:
        if data_file.exists():
            if not validate_file(data_file, shape_files, ontology_file, vocab_files, fmt):
                all_valid = False
    
    print("\n" + "=" * 50)
    if all_valid:
        print(f"✅ All SHACL validations passed for v{version}!")
        sys.exit(0)
    else:
        print(f"❌ Some SHACL validations failed for v{version}.")
        sys.exit(1)

if __name__ == "__main__":
    main()
