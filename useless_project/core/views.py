import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.db.utils import OperationalError
from django.core.management import call_command
from .models import Score

MAX_DB_CAP = 100


def _ensure_tables():
    """Ensures database tables exist by executing migrations."""
    try:
        call_command('migrate', interactive=False)
    except Exception as e:
        print(f"Migration error: {e}")


def index_view(request):
    """Renders the main game interface."""
    return render(request, 'index.html')


@require_GET
def leaderboard_api(request):
    """
    Returns the top 10 scores formatted as:
    [{ "username": str, "seconds_wasted": float }]
    """
    try:
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
    except OperationalError:
        _ensure_tables()
        try:
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
        except Exception:
            return JsonResponse([], safe=False)


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
        username = username[:30]

        seconds = body.get('seconds', 0.0)
        try:
            seconds_wasted = float(seconds)
            if seconds_wasted < 0:
                seconds_wasted = 0.0
            seconds_wasted = round(seconds_wasted, 2)
        except (TypeError, ValueError):
            return JsonResponse({'status': 'error', 'message': 'Invalid seconds value'}, status=400)

        # Function to perform DB create and cap enforcement
        def save_and_cap():
            new_score = Score.objects.create(
                username=username,
                seconds_wasted=seconds_wasted
            )
            while Score.objects.count() > MAX_DB_CAP:
                lowest = Score.objects.order_by('seconds_wasted', '-created_at').first()
                if lowest:
                    lowest.delete()
                else:
                    break
            return new_score

        try:
            new_score = save_and_cap()
        except OperationalError:
            _ensure_tables()
            new_score = save_and_cap()

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

