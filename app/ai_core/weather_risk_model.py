import torch
import torch.nn as nn
import numpy as np
from . import registry

class AttentionLSTM(nn.Module):
    """
    Architecture matching Phase 1.5 exactly.
    """
    def __init__(self, input_dim=6, hidden_size=128, num_layers=2, dropout=0.3, num_classes=3):
        super(AttentionLSTM, self).__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
            bidirectional=True
        )
        self.attention_fc = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, 1)
        )
        self.classifier = nn.Sequential(
            nn.BatchNorm1d(hidden_size * 2),
            nn.Dropout(dropout),
            nn.Linear(hidden_size * 2, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Linear(64, num_classes)
        )
        
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        attn_weights = self.attention_fc(lstm_out)
        attn_weights = torch.softmax(attn_weights, dim=1)
        context = torch.sum(attn_weights * lstm_out, dim=1)
        out = self.classifier(context)
        return out, attn_weights

def predict_weather_risk(weather_sequence_7_days: np.ndarray) -> dict:
    """
    Accepts a 168-hour (7 day) sequence of weather features.
    Features must match Phase 1.5 order:
    ['Temperature (C)', 'Humidity', 'Wind Speed (km/h)', 'Wind Bearing (degrees)', 'Pressure (millibars)', 'Precip Type_Encoded']
    Returns the predicted risk level for the upcoming window.
    """
    model = registry.models.get('weather')
    scaler = registry.models.get('scalers', {}).get('weather')
    
    if model is None or scaler is None:
        return {"risk_level": "Unknown", "risk_index": 0}

    try:
        # Scale the sequence using the fitted StandardScaler from training
        seq_shape = weather_sequence_7_days.shape
        # Flatten to scale, then reshape back
        flattened = weather_sequence_7_days.reshape(-1, seq_shape[-1])
        scaled_flattened = scaler.transform(flattened)
        scaled_seq = scaled_flattened.reshape(1, seq_shape[0], seq_shape[1]) # Add batch dim
        
        seq_tensor = torch.tensor(scaled_seq, dtype=torch.float32).to(registry.device)
        
        with torch.no_grad():
            with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
                output, _ = model(seq_tensor)
                probs = torch.softmax(output, dim=1)[0]
                
        class_idx = torch.argmax(probs).item()
        
        risk_map = {0: "Low", 1: "Medium", 2: "High"}
        
        return {
            "risk_level": risk_map.get(class_idx, "Unknown"),
            "risk_index": class_idx
        }
        
    except Exception as e:
        print(f"Weather Risk Error: {e}")
        return {"error": str(e)}