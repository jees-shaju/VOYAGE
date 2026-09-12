import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.db.utils import OperationalError
from django.core.management import call_command
from .models import Score

MAX_DB_CAP = 100


def _ensure_tables():
    """Ensures database tables exist by running migrations."""
    try:
        call_command('migrate', interactive=False)
    except Exception as e:
        print(f"Migration error: {e}")


@require_GET
def leaderboard_api(request):
    """
    GET /api/leaderboard/
    Returns top 10 scores as JSON:
    [{ "username": str, "seconds_wasted": float, "created_at": str }]
    """
    def fetch():
        top_scores = Score.objects.all()[:10]
        return [
            {
                'username': s.username,
                'seconds_wasted': round(s.seconds_wasted, 2),
                'created_at': s.created_at.strftime('%Y-%m-%d %H:%M') if s.created_at else '',
            }
            for s in top_scores
        ]

    try:
        return JsonResponse(fetch(), safe=False)
    except OperationalError:
        _ensure_tables()
        try:
            return JsonResponse(fetch(), safe=False)
        except Exception:
            return JsonResponse([], safe=False)


@csrf_exempt
@require_POST
def submit_score_api(request):
    """
    POST /api/submit/
    Body: { "username": str, "seconds": float }
    Saves score, enforces 100-row cap, returns success JSON.
    """
    try:
        try:
            body = json.loads(request.body.decode('utf-8'))
        except (ValueError, json.JSONDecodeError):
            body = request.POST

        username = str(body.get('username', '')).strip() or 'Anonymous Idler'
        username = username[:30]

        try:
            seconds_wasted = round(max(0.0, float(body.get('seconds', 0.0))), 2)
        except (TypeError, ValueError):
            return JsonResponse({'status': 'error', 'message': 'Invalid seconds value'}, status=400)

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
                'seconds_wasted': new_score.seconds_wasted,
            }
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
