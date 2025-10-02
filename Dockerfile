FROM python:3.11-slim

# Install Tex Live
RUN apt-get update && apt-get -y upgrade \
    && apt-get -y install --no-install-recommends \
    texlive-latex-base \
    texlive-extra-utils \
    texlive-latex-extra

# Install Pandoc
RUN apt-get -y install --no-install-recommends \
    pandoc

# Clean up
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=dialog \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

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
