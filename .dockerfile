FROM python:3.9.7-slim-buster

WORKDIR /app

# Copy the requirements.txt file first to leverage Docker caching
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

CMD ["python", "GETAGAME.py"]
