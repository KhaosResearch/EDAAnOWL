#!/bin/bash
set -e

IMAGE_NAME="edaanowl-validator"
ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)

echo "--- Building local validation image ($IMAGE_NAME) ---"
docker build -t "$IMAGE_NAME" -f "$ROOT_DIR/Dockerfile" "$ROOT_DIR"

LATEST_VERSION=$(ls -v "$ROOT_DIR/src" | tail -n 1)
if [ -z "$LATEST_VERSION" ]; then
    echo "❌ [ERROR] No version folder found in /src"
    exit 1
fi
echo "--- Validating against latest version: $LATEST_VERSION ---"
LATEST_PATH="src/$LATEST_VERSION"

echo -e "\n--- 🚀 Running syntax validation (scripts/check_rdf.py) ---"
docker run --rm -v "$ROOT_DIR:/app" "$IMAGE_NAME" \
    python3 /app/scripts/check_rdf.py

echo -e "\n--- 🚀 Running SHACL validation (pyshacl) ---"
docker run --rm -v "$ROOT_DIR:/app" "$IMAGE_NAME" \
    python3 -m pyshacl \
        -s /app/$LATEST_PATH/shapes/edaan-shapes.ttl \
        -e /app/$LATEST_PATH/EDAAnOWL.ttl \
        -m -i rdfs -f human \
        /app/$LATEST_PATH/examples/test-consistency.ttl

echo -e "\n--- 🚀 Running SHACL validation (pyshacl) on EO examples ---"
docker run --rm -v "$ROOT_DIR:/app" "$IMAGE_NAME" \
    python3 -m pyshacl \
        -s /app/$LATEST_PATH/shapes/edaan-shapes.ttl \
        -e /app/$LATEST_PATH/EDAAnOWL.ttl \
        -m -i rdfs -f human \
        /app/$LATEST_PATH/examples/eo-instances.ttl

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

echo -e "\n--- 🚀 Running OWL consistency validation (ROBOT) on EO examples ---"
docker run --rm -v "$ROOT_DIR:/app" "$IMAGE_NAME" \
    java -jar /opt/robot/robot.jar reason \
        --catalog /app/robot-catalog.xml \
        --input /app/$LATEST_PATH/examples/eo-instances.ttl \
        --reasoner ELK \
        --output /tmp/edaanowl-reasoned-eo.owl

rm "$ROOT_DIR/robot-catalog.xml"

echo -e "\n✅ All local validations completed successfully!"
