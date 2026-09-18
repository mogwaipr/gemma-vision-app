# Use a lightweight, official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency definition file first (for efficient Docker caching)
COPY requirements.txt .

# Install dependencies without caching build artifacts to keep image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code into the working directory
COPY app.py guideline_data.py ollama_client.py prompt_builder.py ./

# Expose Streamlit's default port
EXPOSE 8501

# Run the application bound to 0.0.0.0 so external docker traffic can reach it
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
