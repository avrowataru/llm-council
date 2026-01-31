#!/bin/bash

# LLM Council - Start script

echo "Starting LLM Council..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found!"
    echo "Please copy .env.example to .env and configure your settings."
    echo ""
    read -p "Would you like to create .env from .env.example now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env
        echo "Created .env file. Please edit it with your LM Studio model names."
        exit 0
    fi
fi

# Start backend
echo "Starting backend on http://localhost:8001..."
python -m backend.main &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 2

# Start Streamlit
echo "Starting Streamlit UI on http://localhost:8501..."
streamlit run streamlit_app.py &
STREAMLIT_PID=$!

echo ""
echo "✓ LLM Council is running!"
echo "  Backend:   http://localhost:8001"
echo "  Streamlit: http://localhost:8501"
echo ""
echo "Make sure LM Studio is running with models loaded!"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $STREAMLIT_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
