
#!/bin/bash

# Stop the container if it's running
echo "Stopping container..."
docker stop streamlit-camera-app 2>/dev/null || true

# Remove the container
echo "Removing container..."
docker rm streamlit-camera-app 2>/dev/null || true

# Optional: Remove the image
echo "Removing image..."
docker rmi analyticsrepository.azurecr.io/streamlit-camera-app:latest 2>/dev/null || true

echo "Streamlit Camera App container stopped and removed."
