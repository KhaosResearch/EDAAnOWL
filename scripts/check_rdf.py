#!/usr/bin/env python3
"""
RDF Syntax Validator for AgoraOWL.

Validates all Turtle files in the latest version folder under `src/`.
"""

import sys
from pathlib import Path

from rdflib import Graph
from rdflib.plugins.parsers.notation3 import BadSyntax


def validate_rdf_file(file_path: Path) -> bool:
    """Validate a single RDF file."""
    try:
        graph = Graph()
        graph.parse(str(file_path), format="turtle")
        print(f"[OK] {file_path}")
        return True
    except BadSyntax as exc:
        error_lines = str(exc).splitlines()
        line_info = error_lines[0] if error_lines else "No details"
        print(f"[FAIL] {file_path} - Syntax error: {line_info}")
        return False
    except Exception as exc:  # pragma: no cover - defensive CLI path
        print(f"[FAIL] {file_path} - Error: {exc}")
        return False


def main() -> None:
    """Main validation function."""
    print("AgoraOWL RDF Syntax Validation")

    try:
        src_path = Path("src")
        if not src_path.is_dir():
            print("[FAIL] 'src' directory not found. Run this script from the repository root.")
            sys.exit(1)

        versions = [directory for directory in src_path.iterdir() if directory.is_dir() and directory.name[0].isdigit()]
        if not versions:
            print("[FAIL] No version folders (e.g. '1.1.0') found in 'src'.")
            sys.exit(1)

        versions.sort(key=lambda version: list(map(int, version.name.split("."))))
        latest_version_path = versions[-1]
        latest_version = latest_version_path.name

        print(f"--- Found latest version: {latest_version} ---")
        print(f"Checking all *.ttl files recursively under: {latest_version_path}\n")
    except Exception as exc:  # pragma: no cover - defensive CLI path
        print(f"[FAIL] Could not find a version folder in 'src': {exc}")
        sys.exit(1)

    if not latest_version_path.is_dir():
        print(f"[WARN] Directory not found, skipping: {latest_version_path}")
        sys.exit(1)

    total_files = 0
    valid_files = 0
    has_errors = False

    for file_path in latest_version_path.rglob("*.ttl"):
        total_files += 1
        if validate_rdf_file(file_path):
            valid_files += 1
        else:
            has_errors = True

    print("\n--- Validation Summary ---")
    print(f"   Total files: {total_files}")
    print(f"   Valid files: {valid_files}")
    print(f"   Invalid files: {total_files - valid_files}")

    if has_errors:
        print("\n[FAIL] Validation FAILED - Syntax errors found")
        sys.exit(1)

    print("\n[OK] All RDF files are syntactically valid")
    sys.exit(0)


if __name__ == "__main__":
    main()
