# 2026-01-01 18:27
import os
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Vercel 환경에서 실행될 때만 자동 마이그레이션 및 관리자 생성
if os.environ.get('VERCEL'):
    try:
        print("Running migrations...")
        call_command('migrate', interactive=False)
        
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            print("Creating superuser...")
            User.objects.create_superuser('admin', 'admin@example.com', 'admin1234')
            print("Superuser created: admin / admin1234")
    except Exception as e:
        print(f"Error during setup: {e}")

app = get_wsgi_application()
