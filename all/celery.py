from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "all.settings")

app = Celery("all")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-every-second': {
        'task': 'cours.tasks.my_periodic_task',
        'schedule': 5.0,  # Exécute toutes les secondes
    },
    'run-evert-2mn': {
        'task': 'cours.tasks.enregistre_choix',
        'schedule': 5.0
    },
    'run-every-5mn': {
        'task': 'cours.tasks.update_because_planification',
        'schedule': 5.0
    },
    'run-every-7mn': {
        'task': 'cours.tasks.update_note_etudiant',
        'schedule': 7.0
    },

    'run-every-7': {
        'task': "cours.tasks.update_planification",
        'schedule': 8.0
    },

    'run-every-1': {
        'task': "cours.tasks.update_form",
        "schedule": 5,

    }
}

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")