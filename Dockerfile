# Stage 1: Build the frontend
FROM node:18-slim AS frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Backend and serve frontend
FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application
COPY app/ ./app/

# Copy built frontend from Stage 1 into a directory the backend can serve
# Note: app/main.py is configured to serve ../frontend/dist relative to itself
# So if main.py is in /app/app/main.py, it looks for /app/frontend/dist
COPY --from=frontend-build /frontend/dist ./frontend/dist

# Expose the port used by Hugging Face Spaces
EXPOSE 7860

ENV PYTHONUNBUFFERED=1
ENV PORT=7860
ENV APP_MODULE=app.main:app

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
