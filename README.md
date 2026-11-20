# AgriTwinX – A Precision Paddy Farming Digital Twin System

AgriTwinX is an AI-powered precision farming system designed to support paddy cultivation through intelligent crop monitoring, disease detection, yield prediction, and data-driven farming recommendations.

The system integrates multiple machine learning and deep learning models into a modular Flask-based application to provide insights that can help farmers make informed agricultural decisions.

## Key Features

- **Paddy Disease Detection:** Multimodal EfficientNet-B3 model for identifying 10 rice disease and healthy-leaf categories using leaf images, rice variety, and crop age.
- **Pest Detection:** YOLO-based model for detecting paddy pests.
- **NPK Prediction:** XGBoost model for estimating soil nutrient requirements.
- **Irrigation Prediction:** Machine learning-based irrigation recommendations.
- **Yield Prediction:** LightGBM model for estimating crop yield.
- **Weather-Based Disease Risk:** Attention BiLSTM model for analyzing weather sequences and estimating disease risk.
- **Explainable AI:** Grad-CAM and SHAP visualizations to support model interpretability.
- **AI Farming Assistant:** Groq API integration for farming guidance and recommendations.
- **Weather Integration:** OpenWeather API integration for weather-related information.

## Technology Stack

| Category | Technologies |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Deep Learning | PyTorch, EfficientNet-B3, YOLO |
| Machine Learning | XGBoost, LightGBM, Scikit-learn |
| Explainable AI | Grad-CAM, SHAP |
| Database | SQLite, PostgreSQL |
| APIs | Groq API, OpenWeather API |
| Deployment | Gunicorn |

## Project Architecture

AgriTwinX follows a modular Flask architecture. Individual inference components handle different agricultural prediction tasks and are integrated into the application.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/aiswaryaav03/AgriTwinX.git
cd AgriTwinX
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template.

Add your own credentials:

```env
SECRET_KEY=your_secret_key
OPENWEATHER_API_KEY=your_openweather_api_key
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=your_postgresql_database_url
```

Never commit your actual `.env` file or API credentials.

### 5. Run the application

```bash
python run.py
```

Open the local application URL displayed in your terminal.

## Machine Learning Models

The project includes trained model files and supporting configurations in the `ai_weights/` directory.

Some models require their corresponding weights and preprocessing assets to be available for inference.

## Research and Documentation

Project reports, presentation materials, notebooks, and experimental visualizations are included in the repository where applicable.

## Project Information

**Project:** AgriTwinX – A Precision Paddy Farming Digital Twin System

**Project Type:** Individual Final-Year B.Tech Project

**Academic Year:** 2026–2027

## Disclaimer

AgriTwinX is an academic project developed for precision agriculture research and experimentation. Model predictions and recommendations should be validated against real-world agricultural conditions before practical use.