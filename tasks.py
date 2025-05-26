# tasks.py
from celery_worker import make_celery
from app import app, apply_gender_detection

celery = make_celery(app)

@celery.task(bind=True)
def apply_gender_detection_async(self, csv_path, model_name, setting):
    try:
        apply_gender_detection(csv_path, model_name, setting)
    except Exception as e:
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        raise
