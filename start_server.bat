@echo off
echo ============================================================
echo Event Booking System - Server Startup
echo ============================================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo.

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo ============================================================
echo Starting Event Booking System API Server...
echo ============================================================
echo.
echo Server will start on: http://localhost:5000
echo.
echo To test the API, open another terminal and run:
echo   python demo.py
echo   OR
echo   python test_api.py
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python app.py
