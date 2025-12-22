@echo off
setlocal enabledelayedexpansion

set IMAGE_NAME=edaanowl-validator
set ROOT_DIR=%~dp0..

echo --- Building local validation image ---
docker build -t %IMAGE_NAME% -f "%ROOT_DIR%\Dockerfile" "%ROOT_DIR%"
if errorlevel 1 goto :build_error

echo --- Finding latest version ---
set LATEST_VERSION=
pushd "%ROOT_DIR%\src"
for /d %%d in (0.*) do set LATEST_VERSION=%%d
popd

if "!LATEST_VERSION!"=="" goto :version_error

echo --- Validating against version: !LATEST_VERSION! ---
set LATEST_PATH=src/!LATEST_VERSION!

echo.
echo --- Running syntax validation ---
docker run --rm -v "%ROOT_DIR%:/app" %IMAGE_NAME% python3 /app/scripts/check_rdf.py
if errorlevel 1 goto :syntax_error

echo.
echo --- Running SHACL validation ---
docker run --rm -v "%ROOT_DIR%:/app" %IMAGE_NAME% python3 /app/scripts/validate_shacl.py
if errorlevel 1 goto :shacl_error

echo.
echo --- Running OWL consistency (ROBOT) ---
echo ^<?xml version="1.0" encoding="UTF-8"?^> > "%ROOT_DIR%\robot-catalog.xml"
echo ^<catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog" prefer="public"^> >> "%ROOT_DIR%\robot-catalog.xml"
echo   ^<uri name="https://w3id.org/EDAAnOWL/" uri="file:/app/!LATEST_PATH!/EDAAnOWL.ttl"/^> >> "%ROOT_DIR%\robot-catalog.xml"
echo ^</catalog^> >> "%ROOT_DIR%\robot-catalog.xml"

docker run --rm -v "%ROOT_DIR%:/app" %IMAGE_NAME% java -jar /opt/robot/robot.jar reason --catalog /app/robot-catalog.xml --input /app/!LATEST_PATH!/examples/test-consistency.ttl --reasoner ELK --output /tmp/reasoned.owl
if errorlevel 1 goto :robot_error

echo.
echo --- Running OWL consistency (ROBOT) EO examples ---
docker run --rm -v "%ROOT_DIR%:/app" %IMAGE_NAME% java -jar /opt/robot/robot.jar reason --catalog /app/robot-catalog.xml --input /app/!LATEST_PATH!/examples/eo-instances.ttl --reasoner ELK --output /tmp/reasoned-eo.owl
if errorlevel 1 goto :robot_eo_error

del "%ROOT_DIR%\robot-catalog.xml" 2>nul

echo.
echo === All local validations completed successfully! ===
goto :end

:build_error
echo [ERROR] Docker image build failed.
goto :end

:version_error
echo [ERROR] No version folder found.
goto :end

:syntax_error
echo [ERROR] Syntax validation failed.
goto :end

:shacl_error
echo [ERROR] SHACL validation failed.
goto :end

:robot_error
echo [ERROR] ROBOT consistency check failed.
goto :end

:robot_eo_error
echo [ERROR] ROBOT check EO examples failed.
goto :end

:end
endlocal
