import pandas as pd

def process_prediction_data(historical_data):
    # Example: Process historical data into training format
    df = pd.DataFrame(historical_data)
    df['features'] = df['severity'] * df['frequency']
    return df
