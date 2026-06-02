import paho.mqtt.client as mqtt
import time
import json
import random

# Configuration
BROKER = "mqtt"
TOPIC = "industrial/telemetry/pump_01"

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

print("Starting ADVANCED simulator... Press Ctrl+C to stop.")

# Simulation states
state = "NORMAL"

try:
    while True:
        # Generate signals
        if state == "NORMAL":
            vibration = random.gauss(5.0, 0.2)
            temperature = random.gauss(60.0, 0.5)
            # 2% chance to trigger fault
            if random.random() > 0.98: state = "FAULTY"
        else:
            # Fault mode: rapid heating and vibration
            vibration = random.gauss(8.0, 0.5)
            temperature = random.gauss(85.0, 2.0)
            # 10% chance to recover
            if random.random() > 0.90: state = "NORMAL"

        payload = {
            "device_id": "pump_01",
            "vibration": round(vibration, 2),
            "temperature": round(temperature, 2),
            "timestamp": time.time()
        }

        client.publish(TOPIC, json.dumps(payload))
        print(f"[{state}] Published: {payload}")
        time.sleep(1)
except KeyboardInterrupt:
    client.disconnect()
