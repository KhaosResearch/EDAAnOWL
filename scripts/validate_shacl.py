#!/usr/bin/env python3
"""
EDAAnOWL SHACL Validation Script
================================

More robust SHACL validation that properly merges vocabulary graphs 
with data before validation, solving issues with the -e flag.
"""

import sys
import os
from pathlib import Path

try:
    from pyshacl import validate
    from rdflib import Graph
except ImportError:
    print("❌ Please install dependencies: pip install rdflib pyshacl")
    sys.exit(1)


def find_latest_version(src_dir: Path) -> str:
    """Find the latest semver version folder in src/"""
    import re
    versions = []
    for item in src_dir.iterdir():
        if item.is_dir() and re.match(r'^\d+\.\d+\.\d+$', item.name):
            versions.append(item.name)
    if not versions:
        return None
    # Sort by semver
    versions.sort(key=lambda v: [int(x) for x in v.split('.')])
    return versions[-1]


def validate_file(data_file: Path, shapes_file: Path, vocab_files: list, ontology_file: Path) -> bool:
    """Validate a single data file against shapes with vocabularies merged."""
    print(f"\n📋 Validating: {data_file.name}")
    
    # Load data graph
    data = Graph()
    data.parse(str(data_file), format='turtle')
    
    # Load and merge ontology + vocabularies
    ontology = Graph()
    ontology.parse(str(ontology_file), format='turtle')
    for vocab in vocab_files:
        ontology.parse(str(vocab), format='turtle')
    
    # Merge data with ontology for proper inference
    merged = data + ontology
    
    # Load shapes
    shapes = Graph()
    shapes.parse(str(shapes_file), format='turtle')
    
    # Validate
    conforms, results_graph, results_text = validate(
        merged,
        shacl_graph=shapes,
        ont_graph=None,  # Already merged
        inference='rdfs',
        debug=False
    )
    
    if conforms:
        print(f"   ✅ Conforms: True")
    else:
        print(f"   ❌ Conforms: False")
        # Show violations
        for line in results_text.split('\n')[2:30]:  # First 30 lines of report
            if line.strip():
                print(f"      {line}")
    
    return conforms


def main():
    # Find project root (script is in /app/scripts/)
    script_dir = Path(__file__).parent.resolve()
    if script_dir.name == 'scripts':
        root_dir = script_dir.parent
    else:
        root_dir = Path.cwd()
    
    src_dir = root_dir / 'src'
    
    # Find latest version
    version = find_latest_version(src_dir)
    if not version:
        print("❌ No version folder found in src/")
        sys.exit(1)
    
    print(f"🔍 EDAAnOWL SHACL Validation (v{version})")
    print("=" * 50)
    
    version_dir = src_dir / version
    shapes_file = version_dir / 'shapes' / 'edaan-shapes.ttl'
    ontology_file = version_dir / 'EDAAnOWL.ttl'
    
    vocab_dir = version_dir / 'vocabularies'
    vocab_files = [
        vocab_dir / 'metric-types.ttl',
        vocab_dir / 'observed-properties.ttl',
        vocab_dir / 'agro-vocab.ttl',
        vocab_dir / 'sector-scheme.ttl',
        vocab_dir / 'datatype-scheme.ttl',
    ]
    
    # Data files to validate
    examples_dir = version_dir / 'examples'
    data_files = [
        examples_dir / 'test-consistency.ttl',
        examples_dir / 'eo-instances.ttl',
    ]
    
    all_valid = True
    for data_file in data_files:
        if data_file.exists():
            if not validate_file(data_file, shapes_file, vocab_files, ontology_file):
                all_valid = False
    
    print("\n" + "=" * 50)
    if all_valid:
        print("✅ All SHACL validations passed!")
        sys.exit(0)
    else:
        print("❌ Some SHACL validations failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
