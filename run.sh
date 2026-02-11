#!/bin/bash
# Launch script for Batch ZIP GUI on macOS/Linux

# Check if virtual environment exists
if [ -d ".venv" ]; then
    .venv/bin/python batch_zip_gui.py
else
    python3 batch_zip_gui.py
fi
