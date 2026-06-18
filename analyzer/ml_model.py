import pickle
import os
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Class label mapping (determined empirically)
# 0=anger, 1=fear, 2=joy, 3=love, 4=sadness, 5=surprise
EMOTION_LABELS = {
    0: 'Anger',
    1: 'Fear',
    2: 'Joy',
    3: 'Love',
    4: 'Sadness',
    5: 'Surprise',
}

EMOTION_META = {
    'Joy': {
        'emoji': '😊',
        'color': '#FBBF24',
        'bg_class': 'bg-yellow-50',
        'text_class': 'text-yellow-600',
        'bar_class': 'bg-yellow-400',
        'glow': 'rgba(251,191,36,0.3)',
        'insight': 'Your words radiate warmth and positivity. Embrace this moment of joy!',
    },
    'Sadness': {
        'emoji': '😢',
        'color': '#60A5FA',
        'bg_class': 'bg-blue-50',
        'text_class': 'text-blue-600',
        'bar_class': 'bg-blue-400',
        'glow': 'rgba(96,165,250,0.3)',
        'insight': 'It\'s okay to feel sad. Acknowledging your emotions is the first step toward healing.',
    },
    'Anger': {
        'emoji': '😠',
        'color': '#F87171',
        'bg_class': 'bg-red-50',
        'text_class': 'text-red-600',
        'bar_class': 'bg-red-400',
        'glow': 'rgba(248,113,113,0.3)',
        'insight': 'Your feelings are valid. Take a breath and give yourself space to process this.',
    },
    'Fear': {
        'emoji': '😨',
        'color': '#A78BFA',
        'bg_class': 'bg-purple-50',
        'text_class': 'text-purple-600',
        'bar_class': 'bg-purple-400',
        'glow': 'rgba(167,139,250,0.3)',
        'insight': 'Feeling afraid is natural. You are stronger than you think.',
    },
    'Love': {
        'emoji': '❤️',
        'color': '#F472B6',
        'bg_class': 'bg-pink-50',
        'text_class': 'text-pink-600',
        'bar_class': 'bg-pink-400',
        'glow': 'rgba(244,114,182,0.3)',
        'insight': 'Love is a powerful emotion. Cherish these deep connections.',
    },
    'Surprise': {
        'emoji': '😮',
        'color': '#FB923C',
        'bg_class': 'bg-orange-50',
        'text_class': 'text-orange-600',
        'bar_class': 'bg-orange-400',
        'glow': 'rgba(251,146,60,0.3)',
        'insight': 'Life is full of unexpected moments. Stay curious and open to what comes next.',
    },
}

_vectorizer = None
_model = None

def load_models():
    global _vectorizer, _model
    if _vectorizer is None:
        with open(os.path.join(BASE_DIR, 'count_vectorizer.pkl'), 'rb') as f:
            _vectorizer = pickle.load(f)
    if _model is None:
        with open(os.path.join(BASE_DIR, 'lr_model.pkl'), 'rb') as f:
            _model = pickle.load(f)
    return _vectorizer, _model

def predict_emotion(text):
    vectorizer, model = load_models()
    vec = vectorizer.transform([text])
    pred_class = model.predict(vec)[0]
    probabilities = model.predict_proba(vec)[0]
    
    primary_emotion = EMOTION_LABELS[pred_class]
    
    # Build breakdown with all emotions and their probabilities
    breakdown = []
    for idx, label in EMOTION_LABELS.items():
        breakdown.append({
            'emotion': label,
            'percentage': round(probabilities[idx] * 100, 1),
            'meta': EMOTION_META[label],
        })
    breakdown.sort(key=lambda x: x['percentage'], reverse=True)
    
    return {
        'primary_emotion': primary_emotion,
        'primary_meta': EMOTION_META[primary_emotion],
        'confidence': round(probabilities[pred_class] * 100, 1),
        'breakdown': breakdown,
    }
