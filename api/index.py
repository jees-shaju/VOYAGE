import os
import sys

# Add useless_project directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, 'useless_project')

if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nothing_game.settings')

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

app = get_wsgi_application()

# Automatically run database migrations on Vercel container startup
try:
    call_command('migrate', interactive=False)
except Exception as e:
    print(f"Auto-migration warning: {e}")
