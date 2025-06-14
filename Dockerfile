# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for some Python libs like pytesseract or numpy)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code to /app
COPY . .

# Set the port Hugging Face expects
ENV PORT 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
