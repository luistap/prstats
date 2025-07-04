FROM python:3.10-slim

RUN apt-get update && apt-get install -y unzip && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else (Python code + r6-dissect binary)
COPY . .

# Make sure r6-dissect binary is executable
RUN chmod +x ./dissect/r6-dissect

# Expose the FastAPI port
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
