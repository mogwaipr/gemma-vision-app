#!/usr/bin/env bash
set -e

LLAMA_PORT=8080
LLAMA_URL="http://localhost:${LLAMA_PORT}/v1/models"

echo "🔍 Checking for running llama-server on port ${LLAMA_PORT}..."

# Test if llama-server is actively responding
if ! curl -s --connect-timeout 2 "$LLAMA_URL" > /dev/null; then
    echo "❌ ERROR: llama-server is NOT running on port ${LLAMA_PORT}!"
    echo "--------------------------------------------------------"
    echo "Please start llama-server on your Mac host first:"
    echo ""
    echo "  cd ~/Projects/llama.cpp"
    echo "  ./build/bin/llama-server \\"
    echo "    -hf bartowski/gemma-4-12B-it-GGUF:Q4_K_M \\"
    echo "    -ngl 99 -c 32768 --port 8080"
    echo "--------------------------------------------------------"
    exit 1
fi

echo "✅ llama-server detected!"
echo "🚀 Building and starting TTB Label Compliance Verifier in Docker..."

docker build -t ttb-verifier-app .
docker run -p 8501:8501 ttb-verifier-app