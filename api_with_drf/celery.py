import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_with_drf.settings')

app = Celery('api_with_drf')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()










# 🚦 Celery Execution Flow: Step by Step
# User একটা order দেয় (POST request).

# Django সেই order টি save করে → perform_create() call হয়।

# Celery-কে .delay() দিয়ে বলা হয়: “এই email পাঠাও”।

# Celery সেই task queue করে Redis এ রাখে।

# Celery worker Redis থেকে সেই task নেয়, এবং background-এ send_mail() চালায়।

# Meanwhile, Django user-কে খুব দ্রুত response দিয়ে ফেলে — wait করে না।

# 🎁 Summary – কে কী করে?
# Component	কাজ
# CELERY_BROKER_URL	Redis কে কাজ জমা দেয়ার জায়গা বানায়
# @shared_task	যেকোনো ফাংশনকে Celery task বানায়
# .delay()	সেই task-টা Celery worker-এ পাঠায়
# celery.py	Celery app কে configure করে এবং tasks detect করে
# Redis	Task-দের queue/staging ground
# Celery Worker	Real background worker — সে কাজগুলো asynchronously চালায়

