FROM python:3.11-slim

# Install dependencies
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Copy semua file ke root container
COPY . /

# Default run
CMD ["python", "run.py"]
