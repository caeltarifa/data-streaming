FROM python:3.11-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Create necessary directory for streamlit config
RUN mkdir -p /root/.streamlit

# Create config.toml with server settings
RUN echo "[server]\nheadless = true\nport = 5000\naddress = \"0.0.0.0\"\nenableCORS = false" > /root/.streamlit/config.toml

# Expose port
EXPOSE 5000

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=5000"]