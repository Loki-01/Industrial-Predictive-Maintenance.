# AlgeriaPredict

AlgeriaPredict is an industrial-grade, AI-driven Predictive Maintenance (PdM) platform designed for distributed,
  ▎ low-connectivity, and edge-computing environments.

## Project Structure
- `src/edge`: Handles data ingestion from industrial sensors (MQTT/OPC-UA).
- `src/ml`: Contains anomaly detection and failure prediction models.
- `infrastructure/k8s`: Kubernetes/K3s deployment files for edge/local nodes.
- `config`: Configuration files for equipment and thresholds.
- `data`: Local storage for training logs and temporary telemetry buffers.

###Core Capabilities
  - Edge-First Architecture: Designed to ingest and analyze sensor data locally (MQTT/OPC-UA), minimizing reliance on
  high-bandwidth cloud connections.
  - Production-Ready: Containerized with Docker and ready for K8s/K3s deployment on factory floor hardware.
  - Anomaly Detection Pipeline: Pre-configured for real-time failure prediction on rotating equipment (pumps, turbines,
  compressors).