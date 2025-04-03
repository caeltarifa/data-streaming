# Docker Setup for Streamlit Camera Data Application

This folder contains Docker configuration files for containerizing the Streamlit Camera Data application.

## Files

- `Dockerfile`: Contains instructions for building the Docker image
- `docker-compose.yml`: Configuration for running the application using Docker Compose

## Running with Docker

### Option 1: Using Docker Compose (Recommended)

1. Make sure you have Docker and Docker Compose installed on your system
2. Navigate to the root directory of the project
3. Run the following command:

```bash
docker-compose up
```

This will build the image if it doesn't exist and start the container.
The application will be accessible at http://localhost:5000

### Option 2: Using Docker Directly

1. Build the Docker image:

```bash
docker build -t streamlit-camera-app .
```

2. Run the container:

```bash
docker run -p 5000:5000 streamlit-camera-app
```

## Development with Docker

If you want to make changes to the code and see them reflected immediately:

```bash
docker-compose up --build
```

This will rebuild the image before starting the container, ensuring your latest code is used.

## Notes

- The application sends data to an external API endpoint every 15 seconds when camera buttons are active
- All dependencies are installed during the Docker image build process
- The application runs on port 5000 inside the container and is mapped to port 5000 on your host machine