import pandas as pd
from backend.ml.models.disaster_predictor import DisasterPredictor

def train_disaster_model(data_path):
    """Train a disaster prediction model."""
    data = pd.read_csv(data_path)
    X = data.drop(columns=['disaster_occurred'])
    y = data['disaster_occurred']

    predictor = DisasterPredictor()
    predictor.train(X, y)

    return predictor
