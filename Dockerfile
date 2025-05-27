# Use a Python base image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set working directory
WORKDIR /app

# Copy only dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies in a virtual environment using uv
RUN uv venv /opt/venv \
    && uv sync --venv /opt/venv --locked

# Copy the rest of the application code
COPY . .

# Activate the virtual environment for all future RUN/CMD
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port your app runs on (adjust if needed)
EXPOSE 8009

# Run the app using uv in the virtual environment
CMD ["uv", "run", "server.py"]
