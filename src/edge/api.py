from fastapi import FastAPI, HTTPException
import uvicorn
import logging

app = FastAPI(title="AlgeriaPredict Edge API")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "edge-ingestion"}

@app.get("/status/sensors")
def get_sensor_status():
    # Placeholder for logic checking last heartbeat from InfluxDB
    return {"active_sensors": ["pump_01", "compressor_01"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
