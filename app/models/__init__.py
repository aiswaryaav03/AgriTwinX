"""
Models package for AgriTwinX.
Importing all models here ensures they are registered with SQLAlchemy's metadata
when the application starts up.
"""
from .user import User
from .field_input import FieldInput
from .prediction import Prediction
from .treatment_log import TreatmentLog
from .farming_calendar import FarmingCalendar
from .feedback import Feedback
from .market_price import MarketPrice