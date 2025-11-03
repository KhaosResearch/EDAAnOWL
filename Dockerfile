# Usar una imagen base con Eclipse Temurin JDK 17
FROM eclipse-temurin:17-jdk-jammy

LABEL maintainer="martin.salvachua1@gmail.com"
LABEL description="Local validation environment for EDAAnOWL ontology"

# Instalar Python 3, pip y wget
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
 && rm -rf /var/lib/apt/lists/*

# Instalar paquetes de Python
RUN pip3 install --upgrade pip
RUN pip3 install rdflib pyshacl

# Descargar ROBOT en un directorio que NO se monta como volumen
WORKDIR /opt/robot
RUN wget -q -O robot.jar https://github.com/ontodev/robot/releases/download/v1.9.4/robot.jar

# Directorio de trabajo por defecto del contenedor
WORKDIR /app

# Copiar el script de validación de sintaxis (aunque luego se monte el volumen, no molesta)
COPY scripts/check_rdf.py /app/scripts/check_rdf.py
