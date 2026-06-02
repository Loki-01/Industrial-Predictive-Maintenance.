import logging
import json
import paho.mqtt.client as mqtt
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants (Move to a config file later)
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "industrial/telemetry/+"
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-token"
INFLUXDB_ORG = "algeria_predict"
INFLUXDB_BUCKET = "telemetry_data"

class IndustrialDataIngestor:
    def __init__(self):
        self.influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
            client.subscribe(MQTT_TOPIC)
        else:
            logger.error(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            device_id = msg.topic.split('/')[-1]

            # Create InfluxDB Point
            point = Point("sensor_data") \
                .tag("device_id", device_id) \
                .field("vibration", float(payload.get("vibration", 0.0))) \
                .field("temperature", float(payload.get("temperature", 0.0))) \
                .time(datetime.utcnow(), WritePrecision.NS)

            self.write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            logger.info(f"Data stored for device {device_id}")

        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def start(self):
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.mqtt_client.loop_forever()

if __name__ == "__main__":
    ingestor = IndustrialDataIngestor()
    logger.info("Starting Edge Ingestion Service...")
    ingestor.start()
