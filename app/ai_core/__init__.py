import os
import torch
import pickle
import logging
import traceback
from ultralytics import YOLO

logger = logging.getLogger(__name__)


class AIModelRegistry:
    """
    Singleton registry to hold all AI models in memory.
    Prevents reloading massive weight files on every API request.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIModelRegistry, cls).__new__(cls)
            cls._instance.models = {
                'disease': None,
                'pest': None,
                'nutrient': {
                    'N': None,
                    'P': None,
                    'K': None
                },
                'irrigation': None,
                'yield': None,
                'weather': None,
                'scalers': {},
                'encoders': {}
            }
            cls._instance.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            cls._instance.is_loaded = False
        return cls._instance

    def load_all_models(self, weights_dir: str):
        """
        Loads all AI weights into memory. Call this once during app startup.

        Every model is loaded in its own try/except block so that a missing
        or broken model never prevents the others from loading. Failures are
        logged with a full traceback and the registry is marked as loaded
        regardless of how many individual models succeeded.
        """
        logger.info(f"Loading AI Models into memory using device: {self.device}")

    
        try:
            from .disease_model import MultiModalEfficientNet
            disease_path = os.path.join(weights_dir, 'disease_detection', 'best.pth')
            if os.path.exists(disease_path):
                model = MultiModalEfficientNet(num_classes=10, num_varieties=10)
                checkpoint = torch.load(disease_path, map_location=self.device)
                model.load_state_dict(checkpoint['model_state_dict'])
                model.to(self.device)
                model.eval()
                self.models['disease'] = model
                logger.info(f"✓ Loaded Disease model from {disease_path}")
            else:
                logger.warning(f"✗ Missing Disease model at {disease_path}")
        except Exception:
            logger.error("✗ Failed to load Disease model:\n" + traceback.format_exc())

        try:
            pest_path = os.path.join(weights_dir, 'pest_detection', 'best.pt')
            if os.path.exists(pest_path):
                self.models['pest'] = YOLO(pest_path)
                logger.info(f"✓ Loaded Pest model from {pest_path}")
            else:
                logger.warning(f"✗ Missing Pest model at {pest_path}")
        except Exception:
            logger.error("✗ Failed to load Pest model:\n" + traceback.format_exc())

        nutrient_dir = os.path.join(weights_dir, 'nutrient_irrigation')
        for nutrient in ('N', 'P', 'K'):
            try:
                nutrient_path = os.path.join(nutrient_dir, f'{nutrient}_model.pkl')
                if os.path.exists(nutrient_path):
                    with open(nutrient_path, 'rb') as f:
                        self.models['nutrient'][nutrient] = pickle.load(f)
                    logger.info(f"✓ Loaded Nutrient[{nutrient}] model from {nutrient_path}")
                else:
                    logger.warning(f"✗ Missing Nutrient[{nutrient}] model at {nutrient_path}")
            except Exception:
                logger.error(f"✗ Failed to load Nutrient[{nutrient}] model:\n" + traceback.format_exc())

        try:
            irr_path = os.path.join(nutrient_dir, 'irrigation_model.pkl')
            if os.path.exists(irr_path):
                with open(irr_path, 'rb') as f:
                    self.models['irrigation'] = pickle.load(f)
                logger.info(f"✓ Loaded Irrigation model from {irr_path}")
            else:
                logger.warning(f"✗ Missing Irrigation model at {irr_path}")
        except Exception:
            logger.error("✗ Failed to load Irrigation model:\n" + traceback.format_exc())

        try:
            scalers_path = os.path.join(nutrient_dir, "scalers.pkl")

            if os.path.exists(scalers_path):
                with open(scalers_path, "rb") as f:
                    self.models["scalers"]["nutrient"] = pickle.load(f)

                logger.info(f"✓ Loaded Nutrient scalers from {scalers_path}")
            else:
                logger.warning(f"✗ Missing Nutrient scalers at {scalers_path}")

        except Exception:
            logger.error("✗ Failed to load Nutrient scalers:\n" + traceback.format_exc())

        try:
            yield_dir = os.path.join(weights_dir, 'yield_prediction')
            yield_path = os.path.join(yield_dir, 'best_yield_model.pkl')
            yield_encoders_path = os.path.join(yield_dir, 'label_encoders.pkl')

            if os.path.exists(yield_path):
                with open(yield_path, 'rb') as f:
                    self.models['yield'] = pickle.load(f)
                logger.info(f"✓ Loaded Yield model from {yield_path}")
            else:
                logger.warning(f"✗ Missing Yield model at {yield_path}")

            if os.path.exists(yield_encoders_path):
                with open(yield_encoders_path, 'rb') as f:
                    self.models['encoders']['yield'] = pickle.load(f)
                logger.info(f"✓ Loaded Yield label encoders from {yield_encoders_path}")
            else:
                logger.warning(f"✗ Missing Yield label encoders at {yield_encoders_path}")
        except Exception:
            logger.error("✗ Failed to load Yield model/encoders:\n" + traceback.format_exc())

        try:
            from .weather_risk_model import AttentionLSTM
            weather_dir = os.path.join(weights_dir, 'weather_prediction')
            weather_path = os.path.join(weather_dir, 'best_lstm_model.h5')
            weather_scaler_path = os.path.join(weather_dir, 'scaler.pkl')

            if os.path.exists(weather_path):
                model = AttentionLSTM(input_dim=6, hidden_size=64, num_layers=2, dropout=0.3)
                model.load_state_dict(torch.load(weather_path, map_location=self.device))
                model.to(self.device)
                model.eval()
                self.models['weather'] = model
                logger.info(f"✓ Loaded Weather model from {weather_path}")
            else:
                logger.warning(f"✗ Missing Weather model at {weather_path}")

            if os.path.exists(weather_scaler_path):
                with open(weather_scaler_path, 'rb') as f:
                    self.models['scalers']['weather'] = pickle.load(f)
                logger.info(f"✓ Loaded Weather scaler from {weather_scaler_path}")
            else:
                logger.warning(f"✗ Missing Weather scaler at {weather_scaler_path}")
        except Exception:
            logger.error("✗ Failed to load Weather model/scaler:\n" + traceback.format_exc())

        self.is_loaded = True
        logger.info("Model loading pass complete (see log above for per-model status).")


# Global registry instance
registry = AIModelRegistry()