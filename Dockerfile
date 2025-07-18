FROM python:3.11-slim
# Add user 'tara' with UID/GID 1000:1000
RUN addgroup --gid 1000 tara && \
    adduser --disabled-password --gecos "" --uid 1000 --gid 1000 tara

# Set user to 'tara'
USER tara

# Ensure /home/tara/.local/bin is in PATH for user tara
ENV PATH="/home/tara/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install the taratool package using setup.py
RUN pip install .

WORKDIR /workspace

# Default command (can be overridden)
# CMD ["taratool", "check"]
