@echo off
setlocal

set IMAGE_NAME=edaanowl-validator
REM
set ROOT_DIR=%~dp0..

echo --- Building local validation image (%IMAGE_NAME%) ---
docker build -t %IMAGE_NAME% -f "%ROOT_DIR%\Dockerfile" "%ROOT_DIR%"
if %errorlevel% neq 0 (
    echo [ERROR] Docker image build failed.
    goto :eof
)

REM Find latest version folder (only folders matching semver pattern like 0.3.2)
echo --- Finding latest version ---
set LATEST_VERSION=
for /f "tokens=*" %%a in ('dir /b /ad /on "%ROOT_DIR%\src" ^| findstr /r "^[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*$"') do (
    set LATEST_VERSION=%%a
)

if "%LATEST_VERSION%"=="" (
    echo [ERROR] No version folder found in /src (looking for semver pattern like 0.3.2)
    goto :eof
)

echo --- Validating against latest version: %LATEST_VERSION% ---
REM
set LATEST_PATH=src/%LATEST_VERSION%

REM
echo.
echo --- 🚀 Running syntax validation (scripts/check_rdf.py) ---
docker run --rm -v "%ROOT_DIR%:/app" %IMAGE_NAME% python3 /app/scripts/check_rdf.py
if %errorlevel% neq 0 (
    echo [ERROR] Syntax validation failed.
    goto :eof
)

REM
echo.
echo --- 🚀 Running SHACL validation (pyshacl) ---
docker run --rm -v "%ROOT_DIR%:/app" %IMAGE_NAME% python3 -m pyshacl ^
    -s /app/%LATEST_PATH%/shapes/edaan-shapes.ttl ^
    -e /app/%LATEST_PATH%/EDAAnOWL.ttl ^
    -e /app/%LATEST_PATH%/vocabularies/metric-types.ttl ^
    -e /app/%LATEST_PATH%/vocabularies/observed-properties.ttl ^
    -e /app/%LATEST_PATH%/vocabularies/agro-vocab.ttl ^
    -e /app/%LATEST_PATH%/vocabularies/sector-scheme.ttl ^
    -e /app/%LATEST_PATH%/vocabularies/datatype-scheme.ttl ^
    -m -i rdfs -f human ^
    /app/%LATEST_PATH%/examples/test-consistency.ttl

if %errorlevel% neq 0 (
    echo [ERROR] SHACL validation failed.
    goto :eof
)

echo.
echo --- 🚀 Running SHACL validation (pyshacl) on EO examples ---
docker run --rm -v "%ROOT_DIR%:/app" %IMAGE_NAME% python3 -m pyshacl ^
    -s /app/%LATEST_PATH%/shapes/edaan-shapes.ttl ^
    -e /app/%LATEST_PATH%/EDAAnOWL.ttl ^
    -e /app/%LATEST_PATH%/vocabularies/metric-types.ttl ^
    -e /app/%LATEST_PATH%/vocabularies/observed-properties.ttl ^
    -e /app/%LATEST_PATH%/vocabularies/agro-vocab.ttl ^
    -e /app/%LATEST_PATH%/vocabularies/sector-scheme.ttl ^
    -e /app/%LATEST_PATH%/vocabularies/datatype-scheme.ttl ^
    -m -i rdfs -f human ^
    /app/%LATEST_PATH%/examples/eo-instances.ttl

if %errorlevel% neq 0 (
    echo [ERROR] SHACL validation (EO examples) failed.
    goto :eof
)

REM
echo.
echo --- 🚀 Running OWL consistency validation (ROBOT) ---
(
    echo ^<?xml version="1.0" encoding="UTF-8"?^>
    echo ^<catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog" prefer="public"^>
    echo     ^<uri name="https://w3id.org/EDAAnOWL/" uri="file:/app/%LATEST_PATH%/EDAAnOWL.ttl"/^>
    echo ^</catalog^>
) > "%ROOT_DIR%\robot-catalog.xml"

docker run --rm -v "%ROOT_DIR%:/app" %IMAGE_NAME% java -jar /opt/robot/robot.jar reason ^
    --catalog /app/robot-catalog.xml ^
    --input /app/%LATEST_PATH%/examples/test-consistency.ttl ^
    --reasoner ELK ^
    --output /tmp/edaanowl-reasoned.owl

if %errorlevel% neq 0 (
    echo [ERROR] ROBOT consistency check failed.
    goto :eof
)

echo.
echo --- 🚀 Running OWL consistency validation (ROBOT) on EO examples ---
docker run --rm -v "%ROOT_DIR%:/app" %IMAGE_NAME% java -jar /opt/robot/robot.jar reason ^
    --catalog /app/robot-catalog.xml ^
    --input /app/%LATEST_PATH%/examples/eo-instances.ttl ^
    --reasoner ELK ^
    --output /tmp/edaanowl-reasoned-eo.owl

if %errorlevel% neq 0 (
    echo [ERROR] ROBOT consistency check (EO examples) failed.
    goto :eof
)

del "%ROOT_DIR%\robot-catalog.xml"

echo.
echo --- ✅ All local validations completed successfully! ---
endlocal
