FROM python:3.11-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Create necessary directory for streamlit configuration
RUN mkdir -p /root/.streamlit

# Create Streamlit configuration to handle WebSocket connections in containerized environment
RUN echo '\
[server]\n\
headless = true\n\
port = 5000\n\
address = "0.0.0.0"\n\
enableCORS = true\n\
enableXsrfProtection = false\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
serverAddress = "localhost"\n\
serverPort = 5000\n\
' > /root/.streamlit/config.toml

# Expose port
EXPOSE 5000

# Run the application with proper parameters for containerized environment
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.enableCORS=true", "--server.enableWebsocketCompression=false"]