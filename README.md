# Gemma Vision Streamlit App

A Streamlit-based vision application connected to a local `llama-server` running Gemma 4 (12B IT).

---

## Architecture Overview

* **Backend:** Local `llama.cpp` server running `gemma-4-12B-it-GGUF` on port `8080`.
* **Frontend:** Streamlit application running inside a Docker container on port `8501`.
* **Networking:** The container reaches the host machine's Llama server via `http://host.docker.internal:8080`.

---

## Prerequisites

* [Git](https://git-scm.com/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine on Linux)
* A compiled [`llama.cpp`](https://github.com/ggerganov/llama.cpp) build (specifically the `./build/bin/llama-server` binary)
* Sufficient VRAM / RAM to run Gemma 4 12B Q4_K_M

---

## Quick Start Guide

### 1. Clone the Repository

```bash
git clone <YOUR_REPO_URL>
cd <YOUR_REPO_DIR>

2. Start the Local Llama Server
From your llama.cpp directory, launch llama-server. Ensure --host 0.0.0.0 is specified so requests from the Docker bridge can be accepted:
./build/bin/llama-server \
  -hf bartowski/gemma-4-12B-it-GGUF:Q4_K_M \
  -ngl 99 \
  -c 32768 \
  --host 0.0.0.0 --port 
  
  curl http://localhost:8080/health  (to verify server running)

  3. Build the Docker Image
From the root of this project (where the Dockerfile resides), build the container image:

docker build -t gemmavisionapp:latest .

Verification: Confirm the image was created:

docker images | grep gemmavisionapp

4. Run the Streamlit Container
Run the container with port 8501 mapped and --add-host enabled so the container can resolve host.docker.internal:

docker run -d \
  -p 8501:8501 \
  --add-host=host.docker.internal:host-gateway \
  --name gemmavisionapp \
  gemmavisionapp:latest

5. Access the Prototype Application
Open your browser and navigate to:

http://localhost:8501

Troubleshooting & Verification
Check container logs:
Bash
docker logs -f gemmavisionapp
Verify container-to-host connectivity:
Bash
docker exec -it gemmavisionapp curl -I [http://host.docker.internal:8080/health](http://host.docker.internal:8080/health)
Stop and remove container:
Bash
docker rm -f gemmavisionapp
