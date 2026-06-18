import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ml_model import predict_emotion

# In-memory history store (session-like, per-process)
_history = []

def index(request):
    return render(request, 'analyzer/index.html')

@csrf_exempt
def analyze(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '').strip()
            if not text:
                return JsonResponse({'error': 'No text provided'}, status=400)
            if len(text) > 2000:
                return JsonResponse({'error': 'Text too long (max 2000 characters)'}, status=400)
            
            result = predict_emotion(text)
            
            # Save to history
            entry = {
                'id': len(_history) + 1,
                'text': text[:120] + ('...' if len(text) > 120 else ''),
                'emotion': result['primary_emotion'],
                'confidence': result['confidence'],
                'meta': result['primary_meta'],
            }
            _history.insert(0, entry)
            if len(_history) > 20:
                _history.pop()
            
            return JsonResponse({'success': True, 'result': result})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def history(request):
    return render(request, 'analyzer/history.html', {'history': _history})
