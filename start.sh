#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 127.0.0.1:8000
