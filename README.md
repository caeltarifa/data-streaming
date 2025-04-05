
# Streaming Camera Data Application

This repository deploys a webapp which is broken down into 3 sections. Each:
1. **sets** secure and restricted traffic towards Kafka clusters over [Async Data Ingestor API](https://github.com/caeltarifa/async_data_ingestor/).
2. **establishes** a `WebSocket` connection by interface: [real-time analytics API]
3. **serves** an AI agent as an assistant for further analytics retrieved from the first-section database: [agent interaction serving API]

[Visit here 🟢!](https://web-camera-data-ingestor.nicedesert-291b7b89.eastus.azurecontainerapps.io/) Come back later if off.

#### > DevOps + DataOps + MLOps
Besides, here confluences **3** entities. `DevOps` (in charge of keeping the whole webapp online), `DataOps` (the handshake among extracting, transforming, and loading to an uninterrupted video data flow turning them into insights), and `MLOps` (which takes an LLM and serves it to the client, continuously fine-tuning the prompts for intuitive interaction) together make this project a window on how a business workload gets translated into an agile multidisciplinary setup (April 2025).

## Azure-architectured solution

Scrum product ownership over data and software development life cycle:
[Open diagram](https://github.com/user-attachments/assets/7e226f59-4bc3-429e-bb4c-f00e795a4366)

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
