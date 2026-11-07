FROM python:3.11-slim

WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY config.py api.py json_to_csv.py ./

# Run the API script first, then convert JSON to CSV
CMD ["sh", "-c", "python api.py && python json_to_csv.py"]
