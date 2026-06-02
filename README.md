# Industrial Edge Predictive Maintenance (PdM)

A production-grade, AI-driven Predictive Maintenance platform designed for distributed, low-connectivity, and resource-constrained industrial edge environments.

## Overview
This platform provides real-time anomaly detection and failure prediction for critical rotating equipment (pumps, turbines, compressors). By leveraging edge computing, it minimizes reliance on high-bandwidth cloud infrastructure, making it ideal for factory floors, remote industrial sites, and IoT deployments.

## Core Capabilities
- **Edge-First Architecture:** Localized ingestion and processing of industrial sensor data (MQTT/OPC-UA), reducing latency and bandwidth overhead.
- **Anomaly Detection Pipeline:** Pre-configured machine learning models for real-time failure prediction.
- **Production-Ready:** Containerized with Docker and ready for deployment via Kubernetes/K3s on edge hardware.
- **Scalable Configuration:** Flexible configuration schema for diverse equipment and operational thresholds.

## Project Structure
- `src/edge`: High-performance ingestion service and API for sensor data.
- `src/ml`: Core machine learning pipeline for anomaly detection.
- `infrastructure/k8s`: Kubernetes/K3s manifests for scalable deployment.
- `config`: Environment-specific equipment settings.

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.13+

### Quick Start
1. Clone the repository.
2. Build and run the services:
   ```bash
   docker-compose up --build
   ```
3. Run the simulator to generate test data:
   ```bash
   python src/edge/simulator.py
   ```

## License
MIT
