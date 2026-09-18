#!/usr/bin/env bash
set -e

OLLAMA_PORT=11434
OLLAMA_URL="http://localhost:${OLLAMA_PORT}/api/tags"

echo "Checking for running Ollama on port ${OLLAMA_PORT}..."

if ! curl -fsS --connect-timeout 2 "$OLLAMA_URL" > /dev/null; then
    echo "ERROR: Ollama is not running on port ${OLLAMA_PORT}."
    echo "Start Ollama and pull a vision-capable model first:"
    echo "  ollama serve"
    echo "  ollama pull gemma4:12b"
    exit 1
fi

echo "Ollama detected."
echo "Building and starting TTB Label Compliance Verifier in Docker..."

docker build -t ttb-verifier-app .
docker run -p 8501:8501 ttb-verifier-app