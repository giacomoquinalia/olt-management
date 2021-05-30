#!/usr/bin/env bash

# Remove __pycache__ folder inside the whole project
find . -iname "__pycache__" -type d -exec rm -r {} 2>/dev/null \;