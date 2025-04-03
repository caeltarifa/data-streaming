
# Docker Setup for Streamlit Camera Data Application

Docker configuration files for containerizing the Camera Data Producer application.

## Files

- `docker-build.sh`: Script to build and run the Docker container
- `docker-cleanup.sh`: Script to stop and cleanup Docker containers
- `docker-compose.yml`: Straighforward service for running the application

## Running with Docker

### Option 1: Using Shell Scripts (Recommended)

1. Make the scripts executable and run them:

```bash
# Build and run the application
./docker-build.sh

# To stop and cleanup
./docker-cleanup.sh
```

The application will be accessible at http://0.0.0.0:5000

### Option 2: Using Docker Compose

```bash
docker-compose up
```

## Development Notes

- The application sends data to an external API endpoint every 15 seconds when camera buttons are active
- All dependencies are installed during the Docker image build process
- The application runs on port 5000 inside the container and is mapped to port 5000 on the hoster machine
