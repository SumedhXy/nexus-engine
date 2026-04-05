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

# Launch the Engine with Uvicorn (Render/Cloud Run dynamic port)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
