import os
from django.conf import settings
from celery import Celery

IS_PRODUCTION = True if 'PRODUCT_UTE_ONLINE_JUDGE' in os.environ else False

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uteoj.settings')

if IS_PRODUCTION:
    app = Celery('uteoj', broker='redis://redis:6379')
else:
    app = Celery('uteoj', broker='redis://localhost:6379')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('HELLO I\' CELERY ------------------------')
