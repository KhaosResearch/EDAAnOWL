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

def validate_file(data_file: Path, shape_files: list, ontology_file: Path, vocab_files: list = None) -> bool:
    """Validate a single data file against shapes."""
    print(f"\n📋 Validating: {data_file.name}")
    
    # Load data graph
    data = Graph()
    data.parse(str(data_file), format='turtle')
    
    # Load ontology
    merged = Graph()
    merged += data
    merged.parse(str(ontology_file), format='turtle')
    
    # Load vocabs if they exist (for legacy versions)
    if vocab_files:
        for vocab in vocab_files:
            if vocab.exists():
                merged.parse(str(vocab), format='turtle')
    
    # Load and merge shapes
    shapes = Graph()
    for sf in shape_files:
        if sf.exists():
            print(f"   🔗 Loading shapes: {sf.name}")
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
        # Show ONLY violations
        results_text_clean = results_text
        for result in results_graph.subjects(SH.resultSeverity, SH.Violation):
            # Extract relevant info for this specific violation
            msg = results_graph.value(result, SH.resultMessage)
            path = results_graph.value(result, SH.resultPath)
            focus = results_graph.value(result, SH.focusNode)
            print(f"      - Violation: {msg}")
            print(f"        Focus: {focus}")
            print(f"        Path: {path}")
    
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
    
    # Dynamic shape list
    shape_files = [
        version_dir / 'shapes' / 'edaan-shapes.ttl',
        version_dir / 'shapes' / 'dcat-ap-alignment.ttl',
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
    data_files = [
        examples_dir / 'test-consistency.ttl',
        examples_dir / 'eo-instances.ttl',
        examples_dir / 'cred-asset-example.ttl',
    ]
    
    all_valid = True
    for data_file in data_files:
        if data_file.exists():
            if not validate_file(data_file, shape_files, ontology_file, vocab_files):
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
