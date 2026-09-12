import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Score

MAX_DB_CAP = 100


def index_view(request):
    """Renders the main game interface."""
    return render(request, 'index.html')


@require_GET
def leaderboard_api(request):
    """
    Returns the top 10 scores formatted as:
    [{ "username": str, "seconds_wasted": float }]
    """
    top_scores = Score.objects.all()[:10]
    data = [
        {
            'username': score.username,
            'seconds_wasted': round(score.seconds_wasted, 2),
            'created_at': score.created_at.strftime('%Y-%m-%d %H:%M') if score.created_at else ''
        }
        for score in top_scores
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
@require_POST
def submit_score_api(request):
    """
    Accepts JSON payload { "username": str, "seconds": float }
    Saves to DB, enforces 100-row cap by removing lowest score(s),
    and returns JSON success response.
    """
    try:
        try:
            body = json.loads(request.body.decode('utf-8'))
        except (ValueError, json.JSONDecodeError):
            body = request.POST

        username = str(body.get('username', '')).strip()
        if not username:
            username = 'Anonymous Idler'
        # Limit to 30 characters
        username = username[:30]

        seconds = body.get('seconds', 0.0)
        try:
            seconds_wasted = float(seconds)
            if seconds_wasted < 0:
                seconds_wasted = 0.0
            seconds_wasted = round(seconds_wasted, 2)
        except (TypeError, ValueError):
            return JsonResponse({'status': 'error', 'message': 'Invalid seconds value'}, status=400)

        # Create new score entry
        new_score = Score.objects.create(
            username=username,
            seconds_wasted=seconds_wasted
        )

        # Enforce strict 100-row cap in database
        # If count > 100, delete the entry with the lowest score
        while Score.objects.count() > MAX_DB_CAP:
            lowest = Score.objects.order_by('seconds_wasted', '-created_at').first()
            if lowest:
                lowest.delete()
            else:
                break

        return JsonResponse({
            'status': 'success',
            'message': 'Score submitted successfully!',
            'score': {
                'username': new_score.username,
                'seconds_wasted': new_score.seconds_wasted
            }
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
