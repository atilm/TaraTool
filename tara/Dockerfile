FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install build tools and pip if needed
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install the taratool package using setup.py
RUN pip install .

# Default command (can be overridden)
# CMD ["taratool", "check"]
