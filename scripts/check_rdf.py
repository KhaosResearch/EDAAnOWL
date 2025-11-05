#!/usr/bin/env python3
"""
RDF Syntax Validator for EDAAnOWL
Validates all Turtle files in the repository
"""

import os
import sys
from pathlib import Path
from rdflib import Graph
from rdflib.plugins.parsers.notation3 import BadSyntax

def validate_rdf_file(file_path):
    """Validate a single RDF file"""
    try:
        g = Graph()
        g.parse(str(file_path), format='turtle')
        print(f"✅ [OK] {file_path}")
        return True
    except BadSyntax as e:
        error_lines = str(e).splitlines()
        line_info = error_lines[0] if error_lines else "No details"
        print(f"❌ [FAIL] {file_path} - Syntax error: {line_info}")
        return False
    except Exception as e:
        print(f"❌ [FAIL] {file_path} - Error: {e}")
        return False

def main():
    """Main validation function"""
    print("🔍 EDAAnOWL RDF Syntax Validation")

    # Find the latest version path dynamically
    try:
        src_path = Path('src')
        if not src_path.is_dir():
            print(f"❌ [FAIL] 'src' directory not found. Run this script from the repository root.")
            sys.exit(1)

        versions = [d for d in src_path.iterdir() if d.is_dir() and d.name[0].isdigit()]
        if not versions:
            print(f"❌ [FAIL] No version folders (e.g., '0.0.1') found in 'src'.")
            sys.exit(1)

        versions.sort(key=lambda v: list(map(int, v.name.split('.'))))
        latest_version_path = versions[-1] # Path object
        latest_version = latest_version_path.name # string
        
        print(f"--- Found latest version: {latest_version} ---")
        print(f"Checking all *.ttl files recursively under: {latest_version_path}\n")

    except Exception as e:
        print(f"❌ [FAIL] Could not find any version folder in /src: {e}")
        sys.exit(1)

    valid_files = 0
    total_files = 0
    has_errors = False
    
    if not latest_version_path.is_dir():
        print(f"⚠️ [WARN] Directory not found, skipping: {latest_version_path}")
        sys.exit(1)

    # Use rglob to search recursively
    for file_path in latest_version_path.rglob("*.ttl"):
        total_files += 1
        if validate_rdf_file(file_path):
            valid_files += 1
        else:
            has_errors = True

    print(f"\n--- Validation Summary ---")
    print(f"   Total files: {total_files}")
    print(f"   Valid files: {valid_files}")
    print(f"   Invalid files: {total_files - valid_files}")

    if has_errors:
        print("\n❌ Validation FAILED - Syntax errors found")
        sys.exit(1)
    else:
        print("\n✅ All RDF files are syntactically valid")
        sys.exit(0)

if __name__ == "__main__":
    main()