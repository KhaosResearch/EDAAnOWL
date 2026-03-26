@echo off
setlocal enabledelayedexpansion

set IMAGE_NAME=edaanowl-validator
set ROOT_DIR=%~dp0..

echo --- Building local validation image ---
docker build -t %IMAGE_NAME% -f "%ROOT_DIR%\Dockerfile" "%ROOT_DIR%"
if errorlevel 1 (
    echo [ERROR] Docker image build failed.
    exit /b 1
)

echo --- Finding latest version ---
set "LATEST_VERSION="
pushd "%ROOT_DIR%\src"
for /f "delims=" %%i in ('dir /b /ad ^| findstr /r "^[0-9]*\.[0-9]*\.[0-9]*$"') do (
    set "LATEST_VERSION=%%i"
)
popd

if not defined LATEST_VERSION (
    echo [ERROR] No version folder (e.g., 1.1.0) found in /src/
    exit /b 1
)

echo --- Validating against version: %LATEST_VERSION% ---
set "LATEST_PATH=src/%LATEST_VERSION%"

echo.
echo --- Running syntax validation ---
docker run --rm -v "%ROOT_DIR%:/app" %IMAGE_NAME% python3 /app/scripts/check_rdf.py
if errorlevel 1 (
    echo [ERROR] Syntax validation failed.
    exit /b 1
)

echo.
echo --- Running SHACL validation ---
docker run --rm -v "%ROOT_DIR%:/app" %IMAGE_NAME% python3 /app/scripts/validate_shacl.py
if errorlevel 1 (
    echo [ERROR] SHACL validation failed.
    exit /b 1
)

echo.
echo --- Running OWL consistency (ROBOT) ---
set CATALOG_FILE=%ROOT_DIR%\robot-catalog.xml
echo ^<?xml version="1.0" encoding="UTF-8"?^> > "%CATALOG_FILE%"
echo ^<catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog" prefer="public"^> >> "%CATALOG_FILE%"
echo   ^<uri name="https://w3id.org/EDAAnOWL/" uri="file:/app/%LATEST_PATH%/EDAAnOWL.ttl"/^> >> "%CATALOG_FILE%"
echo ^</catalog^> >> "%CATALOG_FILE%"

docker run --rm -v "%ROOT_DIR%:/app" %IMAGE_NAME% java -jar /opt/robot/robot.jar reason --catalog /app/robot-catalog.xml --input /app/%LATEST_PATH%/examples/test-consistency.ttl --reasoner ELK --output /tmp/reasoned.owl
if errorlevel 1 (
    echo [ERROR] ROBOT consistency check failed.
    del "%CATALOG_FILE%" 2>nul
    exit /b 1
)

echo.
echo --- Running OWL consistency (ROBOT) EO examples ---
docker run --rm -v "%ROOT_DIR%:/app" %IMAGE_NAME% java -jar /opt/robot/robot.jar reason --catalog /app/robot-catalog.xml --input /app/%LATEST_PATH%/examples/eo-instances.ttl --reasoner ELK --output /tmp/reasoned-eo.owl
if errorlevel 1 (
    echo [ERROR] ROBOT check EO examples failed.
    del "%CATALOG_FILE%" 2>nul
    exit /b 1
)

del "%CATALOG_FILE%" 2>nul

echo.
echo === All local validations completed successfully! ===
exit /b 0
