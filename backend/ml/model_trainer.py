import pandas as pd
import numpy as np
import logging
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import joblib
from sklearn.neighbors import BallTree

class ModelTrainer:
    def __init__(self, disaster_data_path, weather_data_path, model_dir='models'):
        self.disaster_data_path = disaster_data_path
        self.weather_data_path = weather_data_path
        self.model_dir = model_dir
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def merge_nearest_coordinates(self, disaster_data, weather_data, max_distance_km=100):
        """
        Merge disaster and weather data based on nearest coordinates using BallTree
        """
        try:
            # Log initial shape
            self.logger.info(f"Initial disaster_data shape: {disaster_data.shape}")
            self.logger.info(f"Initial weather_data shape: {weather_data.shape}")

            # Check and log missing values in disaster_data
            disaster_missing_lat = disaster_data['latitude'].isna().sum()
            disaster_missing_lon = disaster_data['longitude'].isna().sum()
            self.logger.info(f"Disaster data missing latitude: {disaster_missing_lat}")
            self.logger.info(f"Disaster data missing longitude: {disaster_missing_lon}")

            # Drop rows with NaN in 'latitude' or 'longitude' in disaster_data
            disaster_data = disaster_data.dropna(subset=['latitude', 'longitude'])
            self.logger.info(f"Disaster data shape after dropping NaNs: {disaster_data.shape}")

            # Check and log missing values in weather_data
            weather_missing_lat = weather_data['latitude'].isna().sum()
            weather_missing_lon = weather_data['longitude'].isna().sum()
            self.logger.info(f"Weather data missing latitude: {weather_missing_lat}")
            self.logger.info(f"Weather data missing longitude: {weather_missing_lon}")

            # Drop rows with NaN in 'latitude' or 'longitude' in weather_data
            weather_data = weather_data.dropna(subset=['latitude', 'longitude'])
            self.logger.info(f"Weather data shape after dropping NaNs: {weather_data.shape}")

            # Convert lat/lon to numeric if not already using .loc to avoid warnings
            disaster_data.loc[:, 'latitude'] = pd.to_numeric(disaster_data['latitude'], errors='coerce')
            disaster_data.loc[:, 'longitude'] = pd.to_numeric(disaster_data['longitude'], errors='coerce')
            weather_data.loc[:, 'latitude'] = pd.to_numeric(weather_data['latitude'], errors='coerce')
            weather_data.loc[:, 'longitude'] = pd.to_numeric(weather_data['longitude'], errors='coerce')

            # After conversion, drop any new NaNs introduced
            disaster_data = disaster_data.dropna(subset=['latitude', 'longitude'])
            weather_data = weather_data.dropna(subset=['latitude', 'longitude'])

            self.logger.info(f"Disaster data shape after ensuring numeric coordinates: {disaster_data.shape}")
            self.logger.info(f"Weather data shape after ensuring numeric coordinates: {weather_data.shape}")

            # Convert lat/lon to radians
            disaster_coords = np.radians(disaster_data[['latitude', 'longitude']].values)
            weather_coords = np.radians(weather_data[['latitude', 'longitude']].values)

            # Create BallTree for efficient nearest neighbor search
            tree = BallTree(weather_coords, metric='haversine')

            # Find nearest weather station for each disaster
            distances, indices = tree.query(disaster_coords, k=1)

            # Convert distances from radians to kilometers (Earth radius ≈ 6371 km)
            distances_km = distances * 6371.0

            # Create mask for valid matches within threshold
            valid_matches = distances_km.ravel() <= max_distance_km

            self.logger.info(f"Number of valid matches: {valid_matches.sum()} out of {len(valid_matches)}")

            # Get matched indices
            matched_disaster = disaster_data[valid_matches].reset_index(drop=True)
            matched_weather = weather_data.iloc[indices[valid_matches].ravel()].reset_index(drop=True)

            # Merge the datasets
            result = pd.concat([
                matched_disaster,
                matched_weather.drop(['latitude', 'longitude'], axis=1)
            ], axis=1)

            self.logger.info(f"Successfully merged {len(result)} records")
            self.logger.info(f"Average distance to nearest weather station: {distances_km[valid_matches].mean():.2f} km")
            self.logger.info(f"Resulting combined data shape: {result.shape}")
            self.logger.info(f"Resulting combined data columns: {result.columns.tolist()}")

            return result

        except Exception as e:
            self.logger.error(f"Error in merging coordinates: {str(e)}")
            raise

    def load_and_combine_data(self):
        try:
            self.logger.info("Loading disaster data...")
            disaster_data = pd.read_csv(self.disaster_data_path)
            disaster_data.columns = disaster_data.columns.str.lower()  # Standardize to lowercase
            self.logger.info(f"Disaster data columns: {disaster_data.columns.tolist()}")
            self.logger.info(f"Disaster data shape: {disaster_data.shape}")

            self.logger.info("Loading weather data...")
            weather_data = pd.read_csv(self.weather_data_path)
            weather_data.columns = weather_data.columns.str.lower()    # Standardize to lowercase
            self.logger.info(f"Weather data columns: {weather_data.columns.tolist()}")
            self.logger.info(f"Weather data shape: {weather_data.shape}")

            combined_data = self.merge_nearest_coordinates(disaster_data, weather_data)
            self.logger.info(f"Combined data shape: {combined_data.shape}")
            self.logger.info(f"Combined data columns: {combined_data.columns.tolist()}")

            return combined_data

        except Exception as e:
            self.logger.error(f"Error in loading and merging data: {str(e)}")
            raise

    def preprocess_data(self, combined_data):
        try:
            self.logger.info("Preprocessing data...")

            # Log initial combined data
            self.logger.info(f"Initial combined_data shape: {combined_data.shape}")
            self.logger.debug(combined_data.head())

            # Rename columns with standardized lowercase names
            column_mapping = {
                'total deaths': 'total_deaths',
                "total damage ('000 us$)": 'infrastructure_loss',
                'disaster type': 'disaster_type',
                'temperature_celsius': 'temperature',
                'pressure_mb': 'pressure',
                'humidity': 'humidity',
                'wind_kph': 'wind_speed'
            }

            combined_data = combined_data.rename(columns=column_mapping)
            self.logger.info(f"Columns after renaming: {combined_data.columns.tolist()}")

            # Required columns
            required_columns = [
                'latitude', 'longitude', 'temperature', 
                'pressure', 'humidity', 'wind_speed',
                'total_deaths', 'infrastructure_loss', 'disaster_type'
            ]

            missing_cols = [col for col in required_columns if col not in combined_data.columns]
            if missing_cols:
                self.logger.error(f"Missing required columns after renaming: {missing_cols}")
                raise KeyError(missing_cols)

            # Convert numeric columns using .loc to avoid SettingWithCopyWarning
            numeric_columns = ['total_deaths', 'infrastructure_loss']
            for col in numeric_columns:
                combined_data.loc[:, col] = pd.to_numeric(combined_data[col], errors='coerce')

            # Log missing values before dropna
            self.logger.info("Missing values before dropna:")
            self.logger.info(combined_data[required_columns].isna().sum())

            # Drop rows with missing values in required columns
            initial_shape = combined_data.shape
            combined_data = combined_data.dropna(subset=required_columns)
            self.logger.info(f"Dropped {initial_shape[0] - combined_data.shape[0]} rows due to missing values")
            self.logger.info(f"Data shape after dropna: {combined_data.shape}")

            if combined_data.empty:
                raise ValueError("No data left after dropping rows with missing values.")

            # Log unique disaster types
            self.logger.info("Unique disaster types after dropna:")
            self.logger.info(combined_data['disaster_type'].unique())

            # Ensure 'disaster_type' is a 1D array
            disaster_type = combined_data['disaster_type'].astype(str)
            self.logger.info(f"disaster_type shape: {disaster_type.shape}")
            self.logger.info(f"disaster_type dtype: {disaster_type.dtype}")

            if disaster_type.ndim != 1:
                self.logger.error("disaster_type is not a 1D array.")
                raise ValueError("disaster_type is not a 1D array.")

            # Label encode disaster types
            label_encoder = LabelEncoder()
            y_disaster_type = label_encoder.fit_transform(disaster_type.values)
            self.logger.info(f"y_disaster_type shape: {y_disaster_type.shape}")
            self.logger.info(f"Unique classes in y_disaster_type: {np.unique(y_disaster_type)}")

            # Check for multiple classes
            unique_classes = np.unique(y_disaster_type)
            self.logger.info(f"Number of unique classes: {len(unique_classes)}")

            if len(unique_classes) < 2:
                self.logger.error("Insufficient classes for classification. At least two classes are required.")
                raise ValueError("Insufficient classes for classification. At least two classes are required.")

            # Prepare target variables
            y_deaths = combined_data['total_deaths'].values
            y_infra_loss = combined_data['infrastructure_loss'].values

            # Prepare feature matrix
            feature_columns = ['latitude', 'longitude', 'temperature', 
                               'pressure', 'humidity', 'wind_speed']
            missing_feature_cols = [col for col in feature_columns if col not in combined_data.columns]
            if missing_feature_cols:
                self.logger.error(f"Missing feature columns: {missing_feature_cols}")
                raise KeyError(missing_feature_cols)
            X = combined_data[feature_columns]

            self.logger.info(f"Feature columns have shape: {X.shape}")

            # Scale features
            scaler = StandardScaler()
            X = scaler.fit_transform(X)

            self.logger.info(f"Preprocessed X shape: {X.shape}")
            self.logger.info(f"y_disaster_type shape: {y_disaster_type.shape}")
            self.logger.info(f"y_deaths shape: {y_deaths.shape}")
            self.logger.info(f"y_infra_loss shape: {y_infra_loss.shape}")

            # Assign scaler and label_encoder as class attributes
            self.scaler = scaler
            self.label_encoder = label_encoder

            return X, y_disaster_type, y_deaths, y_infra_loss, label_encoder, feature_columns, scaler

        except Exception as e:
            self.logger.error(f"Error in preprocessing: {str(e)}")
            raise
    def preprocess_infrastructure_loss(self, disaster_data):
        try:
        # Convert to numeric and handle invalid values
            disaster_data['infrastructure_loss'] = pd.to_numeric(
            disaster_data['infrastructure_loss'], 
            errors='coerce'
            )
        
        # Replace negative values with 0
            disaster_data['infrastructure_loss'] = disaster_data['infrastructure_loss'].clip(lower=0)
        
        # Log statistics
            self.logger.info(f"Infrastructure loss statistics:")
            self.logger.info(f"Mean: {disaster_data['infrastructure_loss'].mean():.2f}")
            self.logger.info(f"Max: {disaster_data['infrastructure_loss'].max():.2f}")
            self.logger.info(f"Min: {disaster_data['infrastructure_loss'].min():.2f}")
        
            return disaster_data

        except Exception as e:
            self.logger.error(f"Error preprocessing infrastructure loss: {str(e)}")
            raise

    def train_models(self, X, y_disaster_type, y_deaths, y_infra_loss, feature_columns):
        try:
            self.logger.info("Training models...")

        # Initialize models
            type_model = RandomForestClassifier(
            n_estimators=200, max_depth=15, 
            min_samples_split=5, min_samples_leaf=2,
            class_weight='balanced', random_state=42
            )
        
            deaths_model = RandomForestRegressor(
            n_estimators=200, max_depth=15,
            min_samples_split=5, min_samples_leaf=2,
            random_state=42
            )
        
            infra_loss_model = RandomForestRegressor(
            n_estimators=300,
            max_depth=20,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )

        # Train disaster type classifier
            self.logger.info("Training disaster type classifier...")
            type_model.fit(X, y_disaster_type)
            type_score = type_model.score(X, y_disaster_type)
            self.logger.info(f"Disaster type classifier R2 score: {type_score:.4f}")

        # Train death count predictor
            self.logger.info("Training death count predictor...")
            deaths_model.fit(X, y_deaths)
            deaths_score = deaths_model.score(X, y_deaths)
            self.logger.info(f"Death count predictor R2 score: {deaths_score:.4f}")

        # Train infrastructure loss predictor
            self.logger.info("Training infrastructure loss model...")
            infra_loss_model.fit(X, y_infra_loss)
            infra_score = infra_loss_model.score(X, y_infra_loss)
            self.logger.info(f"Infrastructure loss predictor R2 score: {infra_score:.4f}")

        # Save all models
            self.logger.info("Saving models...")
            model_path = f"{self.model_dir}/disaster_type_model.pkl"
            deaths_model_path = f"{self.model_dir}/deaths_model.pkl"
            infra_loss_model_path = f"{self.model_dir}/infra_loss_model.pkl"
            scaler_path = f"{self.model_dir}/scaler.pkl"
            label_encoder_path = f"{self.model_dir}/label_encoder.pkl"

            joblib.dump(type_model, model_path)
            joblib.dump(deaths_model, deaths_model_path)
            joblib.dump(infra_loss_model, infra_loss_model_path)
            joblib.dump(self.scaler, scaler_path)
            joblib.dump(self.label_encoder, label_encoder_path)

            self.logger.info("All models saved successfully.")

            return type_model, deaths_model, infra_loss_model

        except Exception as e:
            self.logger.error(f"Error in training models: {str(e)}")
            raise

def main():
    try:
        disaster_data_path = r'C:\Users\Asus\Desktop\disaster-management-system\backend\ml\data\raw\disaster_historical_data.csv'  # Update path
        weather_data_path = r'C:\Users\Asus\Desktop\disaster-management-system\backend\ml\data\raw\GlobalWeatherRepository.csv'    # Update path
        model_dir = 'models'

        trainer = ModelTrainer(disaster_data_path, weather_data_path, model_dir)
        combined_data = trainer.load_and_combine_data()
        X, y_disaster_type, y_deaths, y_infra_loss, label_encoder, feature_columns, scaler = trainer.preprocess_data(combined_data)
        trainer.train_models(X, y_disaster_type, y_deaths, y_infra_loss, feature_columns)

    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")

if __name__ == "__main__":
    main()