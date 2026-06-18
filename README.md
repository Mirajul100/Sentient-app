# Sentient — Text Emotion Analyzer (Django Web App)

A fully responsive Django web application that analyzes text and detects emotions using a pre-trained Machine Learning model.

## Features
- Real-time emotion detection (Joy, Sadness, Anger, Fear, Love, Surprise)
- Probability breakdown with animated bars
- Empathetic insights per emotion
- In-memory analysis history
- Mobile-first, fully responsive design (Glassmorphism + Material Design)

## Setup & Run

```bash
# 1. Install dependencies
pip install django scikit-learn

# 2. Run the server
cd sentient_app
python manage.py runserver

# 3. Open in browser
http://127.0.0.1:8000/
```

## Project Structure
```
sentient_app/
├── manage.py
├── sentient_app/          # Django project config
│   ├── settings.py
│   └── urls.py
├── analyzer/              # Main Django app
│   ├── views.py           # index, analyze (POST), history
│   ├── urls.py
│   ├── ml_model.py        # Model loading + prediction logic
│   ├── count_vectorizer.pkl
│   └── lr_model.pkl
└── templates/
    ├── base.html          # Shared layout, nav, header
    └── analyzer/
        ├── index.html     # Analyze page
        └── history.html   # History page
```

## ML Model Details
- **Vectorizer:** CountVectorizer (12,144 features)
- **Model:** Logistic Regression (6-class)
- **Classes:** 0=Anger, 1=Fear, 2=Joy, 3=Love, 4=Sadness, 5=Surprise
- **API Endpoint:** POST `/analyze/` — JSON body `{"text": "..."}`
