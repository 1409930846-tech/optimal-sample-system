#!/bin/bash

echo "=========================================="
echo "  Optimal Samples Selection System"
echo "  Streamlit Web Version"
echo "=========================================="
echo ""

cd "$(dirname "$0")"
cd "1_Source_Codes"

echo "Installing dependencies..."
pip3 install streamlit --quiet 2>/dev/null || python3 -m pip install streamlit --quiet

echo ""
echo "Starting Streamlit app..."
echo "Local URL: http://localhost:8501"

# 获取局域网IP (macOS兼容)
if [ -n "$(ifconfig en0 2>/dev/null | grep 'inet ')" ]; then
    LAN_IP=$(ifconfig en0 | grep 'inet ' | awk '{print $2}')
elif [ -n "$(ifconfig en1 2>/dev/null | grep 'inet ')" ]; then
    LAN_IP=$(ifconfig en1 | grep 'inet ' | awk '{print $2}')
else
    LAN_IP="localhost"
fi

echo "Network URL: http://$LAN_IP:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

streamlit run streamlit_app.py --server.headless true --server.port 8501
