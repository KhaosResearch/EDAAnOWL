#!/bin/bash
set -e

IMAGE_NAME="edaanowl-validator"
ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)

echo "--- Building local validation image ($IMAGE_NAME) ---"
docker build -t "$IMAGE_NAME" -f "$ROOT_DIR/Dockerfile" "$ROOT_DIR"

# Find latest version folder (only folders matching semver pattern like 0.3.2)
LATEST_VERSION=$(ls -d "$ROOT_DIR/src"/*/ 2>/dev/null | xargs -n 1 basename | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | tail -n 1)
if [ -z "$LATEST_VERSION" ]; then
    echo "❌ [ERROR] No version folder found in /src (looking for semver pattern like 0.3.2)"
    exit 1
fi
echo "--- Validating against latest version: $LATEST_VERSION ---"
LATEST_PATH="src/$LATEST_VERSION"

# Función auxiliar para ejecutar docker evitando la conversión de rutas en Windows (Git Bash)
docker_run() {
    # MSYS_NO_PATHCONV=1 evita que Git Bash transforme "/app" en "C:/Program Files/Git/app"
    MSYS_NO_PATHCONV=1 docker run --rm -v "$ROOT_DIR:/app" "$IMAGE_NAME" "$@"
}

echo -e "\n--- 🚀 Running syntax validation (scripts/check_rdf.py) ---"
docker_run python3 /app/scripts/check_rdf.py

echo -e "\n--- 🚀 Running SHACL validation (pyshacl) ---"
# Merge files specifically for validation to ensure all types are visible in the data graph
cat "$ROOT_DIR/$LATEST_PATH/examples/test-consistency.ttl" \
    "$ROOT_DIR/$LATEST_PATH/vocabularies/metric-types.ttl" \
    "$ROOT_DIR/$LATEST_PATH/vocabularies/observed-properties.ttl" \
    "$ROOT_DIR/$LATEST_PATH/vocabularies/agro-vocab.ttl" \
    "$ROOT_DIR/$LATEST_PATH/vocabularies/datatype-scheme.ttl" \
    "$ROOT_DIR/$LATEST_PATH/vocabularies/data-theme.ttl" \
    "$ROOT_DIR/$LATEST_PATH/vocabularies/crs-vocab.ttl" \
    "$ROOT_DIR/$LATEST_PATH/vocabularies/access-rights.ttl" > "$ROOT_DIR/merged_test.ttl"

docker_run python3 -m pyshacl \
        -s /app/$LATEST_PATH/shapes/edaan-shapes.ttl \
        -e /app/$LATEST_PATH/EDAAnOWL.ttl \
        -m -i rdfs -f human \
        /app/merged_test.ttl
rm "$ROOT_DIR/merged_test.ttl"

echo -e "\n--- 🚀 Running SHACL validation (pyshacl) on EO examples ---"
cat "$ROOT_DIR/$LATEST_PATH/examples/eo-instances.ttl" \
    "$ROOT_DIR/$LATEST_PATH/vocabularies/metric-types.ttl" \
    "$ROOT_DIR/$LATEST_PATH/vocabularies/observed-properties.ttl" \
    "$ROOT_DIR/$LATEST_PATH/vocabularies/agro-vocab.ttl" \
    "$ROOT_DIR/$LATEST_PATH/vocabularies/datatype-scheme.ttl" \
    "$ROOT_DIR/$LATEST_PATH/vocabularies/data-theme.ttl" \
    "$ROOT_DIR/$LATEST_PATH/vocabularies/crs-vocab.ttl" \
    "$ROOT_DIR/$LATEST_PATH/vocabularies/access-rights.ttl" > "$ROOT_DIR/merged_eo.ttl"

docker_run python3 -m pyshacl \
        -s /app/$LATEST_PATH/shapes/edaan-shapes.ttl \
        -e /app/$LATEST_PATH/EDAAnOWL.ttl \
        -m -i rdfs -f human \
        /app/merged_eo.ttl
rm "$ROOT_DIR/merged_eo.ttl"

echo -e "\n--- 🚀 Running OWL consistency validation (ROBOT) ---"
cat > "$ROOT_DIR/robot-catalog.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog" prefer="public">
  <uri name="https://w3id.org/EDAAnOWL/" uri="file:/app/$LATEST_PATH/EDAAnOWL.ttl"/>
</catalog>
EOF

docker_run java -jar /opt/robot/robot.jar reason \
        --catalog /app/robot-catalog.xml \
        --input /app/$LATEST_PATH/examples/test-consistency.ttl \
        --reasoner ELK \
        --output /tmp/edaanowl-reasoned.owl

echo -e "\n--- 🚀 Running OWL consistency validation (ROBOT) on EO examples ---"
docker_run java -jar /opt/robot/robot.jar reason \
        --catalog /app/robot-catalog.xml \
        --input /app/$LATEST_PATH/examples/eo-instances.ttl \
        --reasoner ELK \
        --output /tmp/edaanowl-reasoned-eo.owl

rm "$ROOT_DIR/robot-catalog.xml"

echo -e "\n✅ All local validations completed successfully!"
