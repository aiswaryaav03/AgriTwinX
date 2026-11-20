import numpy as np

# Risk wise recommendation
ACTION_MAP = {
    "Low": "Continue normal crop monitoring.",
    "Medium": "Inspect the crop and keep preventive spray ready.",
    "High": "Immediate field inspection and preventive disease management is recommended."
}


def _calculate_daily_risk(avg_temp, avg_humidity, rain_hours):
    """
    Rule-based agronomic risk estimation.
    """

    if avg_humidity >= 85 and avg_temp >= 32:
        return "High"

    elif avg_humidity >= 75 or rain_hours >= 8:
        return "Medium"

    return "Low"


def generate_daily_forecast(weather_sequence, overall_weather):
    """
    Converts the 168x6 weather sequence into a 7-day farmer-friendly forecast.

    Input:
        weather_sequence : numpy array (168,6)

    Features:
        0 Temperature
        1 Humidity
        2 Wind Speed
        3 Wind Direction
        4 Pressure
        5 Precipitation Type

    Returns:
        {
            risk_level,
            risk_index,
            forecast:[7 objects]
        }
    """

    forecast = []

    if weather_sequence is None:
        return overall_weather

    try:

        sequence = np.array(weather_sequence)

        for day in range(7):

            start = day * 24
            end = start + 24

            day_data = sequence[start:end]

            avg_temp = round(float(np.mean(day_data[:, 0])), 1)
            avg_humidity = round(float(np.mean(day_data[:, 1])), 1)
            avg_wind = round(float(np.mean(day_data[:, 2])), 1)
            avg_pressure = round(float(np.mean(day_data[:, 4])), 1)

            rain_hours = int(np.sum(day_data[:, 5]))

            risk = _calculate_daily_risk(
                avg_temp,
                avg_humidity,
                rain_hours
            )

            forecast.append({

                "day": day + 1,

                "temperature": avg_temp,

                "humidity": avg_humidity,

                "wind_speed": avg_wind,

                "pressure": avg_pressure,

                "rainfall_hours": rain_hours,

                "risk": risk,

                "action": ACTION_MAP[risk]

            })

        return {

            "risk_level": overall_weather.get("risk_level", "Unknown"),

            "risk_index": overall_weather.get("risk_index", 0),

            "forecast": forecast

        }

    except Exception:

        return overall_weather