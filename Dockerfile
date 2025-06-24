FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install the taratool package using setup.py
RUN pip install .

WORKDIR /workspace

# Default command (can be overridden)
# CMD ["taratool", "check"]
