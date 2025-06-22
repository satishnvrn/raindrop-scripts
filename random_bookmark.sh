#!/bin/bash
# Simple wrapper script for the random bookmark fetcher

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/random_bookmark.py" "$@"
