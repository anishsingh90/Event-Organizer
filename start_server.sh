#!/bin/bash

echo "============================================================"
echo "Event Booking System - Server Startup"
echo "============================================================"
echo ""

echo "Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python is not installed or not in PATH"
    exit 1
fi
echo ""

echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo ""

echo "============================================================"
echo "Starting Event Booking System API Server..."
echo "============================================================"
echo ""
echo "Server will start on: http://localhost:5000"
echo ""
echo "To test the API, open another terminal and run:"
echo "  python3 demo.py"
echo "  OR"
echo "  python3 test_api.py"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================================"
echo ""

python3 app.py
