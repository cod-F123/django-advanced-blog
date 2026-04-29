from celery import Celery
import os 
# from accounts.tasks import sendEmail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# @app.on_after_configure.connect
# def setup_on_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10, sendEmail.s(), name="send Email each 10 second")