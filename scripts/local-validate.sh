#!/bin/bash
set -e

IMAGE_NAME="edaanowl-validator"
ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)

echo "--- Building local validation image ($IMAGE_NAME) ---"
docker build -t "$IMAGE_NAME" -f "$ROOT_DIR/Dockerfile" "$ROOT_DIR"

# 1. Encontrar la última carpeta de versión en src/
LATEST_VERSION=$(ls -v "$ROOT_DIR/src" | tail -n 1)
if [ -z "$LATEST_VERSION" ]; then
    echo "❌ [ERROR] No version folder found in /src"
    exit 1
fi
echo "--- Validating against latest version: $LATEST_VERSION ---"
LATEST_PATH="src/$LATEST_VERSION"

# 2. Run RDF Syntax Check
echo -e "\n--- 🚀 Running syntax validation (scripts/check_rdf.py) ---"
docker run --rm -v "$ROOT_DIR:/app" "$IMAGE_NAME" \
    python3 /app/scripts/check_rdf.py

# 3. Run SHACL Validation
echo -e "\n--- 🚀 Running SHACL validation (pyshacl) ---"
docker run --rm -v "$ROOT_DIR:/app" "$IMAGE_NAME" \
    python3 -m pyshacl \
        -s /app/$LATEST_PATH/shapes/edaan-shapes.ttl \
        -e /app/$LATEST_PATH/EDAAnOWL.ttl \
        -m -i rdfs -f human \
        /app/$LATEST_PATH/examples/test-consistency.ttl

# 4. Run OWL Consistency Check (ROBOT)
echo -e "\n--- 🚀 Running OWL consistency validation (ROBOT) ---"
cat > "$ROOT_DIR/robot-catalog.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog" prefer="public">
  <uri name="https://w3id.org/EDAAnOWL/" uri="file:/app/$LATEST_PATH/EDAAnOWL.ttl"/>
</catalog>
EOF

docker run --rm -v "$ROOT_DIR:/app" "$IMAGE_NAME" \
    java -jar /opt/robot/robot.jar reason \
        --catalog /app/robot-catalog.xml \
        --input /app/$LATEST_PATH/examples/test-consistency.ttl \
        --reasoner ELK \
        --output /tmp/edaanowl-reasoned.owl

rm "$ROOT_DIR/robot-catalog.xml"

echo -e "\n✅ All local validations completed successfully!"
