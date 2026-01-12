@echo off
echo ========================================
echo Docker Build Script for Backend
echo ========================================

REM Ensure we're in phuong-web directory
cd /d %~dp0

echo Current directory: 
cd
echo.

REM Check required files
echo [1/5] Checking required files...
if not exist uv.lock (
    echo ERROR: uv.lock not found!
    pause
    exit /b 1
)
if not exist pyproject.toml (
    echo ERROR: pyproject.toml not found!
    pause
    exit /b 1
)
if not exist core-api-service\Dockerfile (
    echo ERROR:  Dockerfile not found! 
    pause
    exit /b 1
)
echo OK: All required files found. 
echo.

REM Enable BuildKit
echo [2/5] Enabling BuildKit...
set DOCKER_BUILDKIT=1

REM Define variables
set IMAGE_REGISTRY=asia-southeast1-docker.pkg.dev
set PROJECT_ID=datn-483421
set REPO_NAME=datn-docker-repo
set IMAGE_NAME=backend
set IMAGE_TAG=v1
set FULL_IMAGE=%IMAGE_REGISTRY%/%PROJECT_ID%/%REPO_NAME%/%IMAGE_NAME%:%IMAGE_TAG%

echo [3/5] Building Docker image... 
echo Image: %FULL_IMAGE%
echo Dockerfile: core-api-service/Dockerfile
echo Context: %CD%
echo.

REM Build image from parent directory
docker build -f core-api-service/Dockerfile -t %FULL_IMAGE% .

REM Check result
if %ERRORLEVEL% EQU 0 (
    echo. 
    echo ========================================
    echo [5/5] BUILD SUCCESS! 
    echo ========================================
    echo. 
    echo Image: %FULL_IMAGE%
    echo. 
    echo Next steps:
    echo 1. gcloud auth configure-docker %IMAGE_REGISTRY%
    echo 2. docker push %FULL_IMAGE%
    echo. 
) else (
    echo.
    echo ========================================
    echo [5/5] BUILD FAILED! 
    echo ========================================
    echo.
)

pause