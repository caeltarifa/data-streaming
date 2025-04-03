
#!/bin/bash

# Build the Docker image
echo "Building Docker image..."
docker build -t analyticsrepository.azurecr.io/streamlit-camera-app:latest .

# Run the container
# -p 5000:5000 maps port 5000 from the container to port 5000 on the host
# --name gives the container a name for easy reference
docker run -d -p 5000:5000 --name streamlit-camera-app analyticsrepository.azurecr.io/streamlit-camera-app:latest

echo "Streamlit Camera App is running at http://0.0.0.0:5000"
echo "To view logs: docker logs streamlit-camera-app"
echo "To stop the container: docker stop streamlit-camera-app"
echo "To deploy: log in and push the image analyticsrepository.azurecr.io/streamlit-camera-app:latest"
