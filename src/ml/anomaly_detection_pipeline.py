import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from influxdb_client import InfluxDBClient
from sklearn.preprocessing import StandardScaler

# --- AutoEncoder Model ---
class AnomalyDetector(nn.Module):
    def __init__(self, input_dim):
        super(AnomalyDetector, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU()
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, input_dim)
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))

# --- Data Pipeline ---
class MLPipeline:
    def __init__(self):
        self.client = InfluxDBClient(url="http://localhost:8086", token="my-token", org="algeria_predict")
        self.query_api = self.client.query_api()
        self.scaler = StandardScaler()

    def fetch_data(self, device_id, time_range="24h"):
        query = f'''
        from(bucket: "telemetry_data")
          |> range(start: -{time_range})
          |> filter(fn: (r) => r["device_id"] == "{device_id}")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        '''
        df = self.query_api.query_data_frame(query)
        return df[['vibration', 'temperature']]

    def prepare_data(self, df, fit=False):
        if fit:
            return self.scaler.fit_transform(df.values)
        return self.scaler.transform(df.values)

    def run_inference(self, model, data):
        model.eval()
        with torch.no_grad():
            tensor = torch.FloatTensor(data)
            reconstructed = model(tensor)
            # Calculate MSE loss (reconstruction error)
            loss = torch.mean((tensor - reconstructed)**2, dim=1)
        return loss.numpy()

if __name__ == "__main__":
    # Initialize
    pipeline = MLPipeline()
    model = AnomalyDetector(input_dim=2)

    # Example flow
    df = pipeline.fetch_data("pump_01")
    if not df.empty:
        scaled_data = pipeline.prepare_data(df, fit=True)
        scores = pipeline.run_inference(model, scaled_data)

        # Simple thresholding logic
        threshold = np.mean(scores) + 3 * np.std(scores)
        anomalies = scores > threshold
        print(f"Detected {np.sum(anomalies)} anomalies in the last 24h.")
    else:
        print("No data available for inference.")
