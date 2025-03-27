FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY StreamlitIntelligence /app

# Install dependencies (if pyproject.toml exists)
RUN pip install --no-cache-dir streamlit && \
    [ -f pyproject.toml ] && pip install --no-cache-dir . || true

# Expose Streamlit default port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "app.py"]
