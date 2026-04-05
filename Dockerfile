# Use the professional Python Slim image for mission-readiness
FROM python:3.11-slim

# Set the mission-critical environment
WORKDIR /app

# Prevent Python from writing .pyc files and buffer the logs for real-time audit
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install the Tactical Blueprint
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Orchestration Hub
COPY . .

# Expose the high-fidelity port
EXPOSE 8080

# Launch the Engine with Uvicorn (Render/Cloud Run default port 8080)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
