from django.contrib.auth import get_user_model
from requests import HTTPError

from config import celery_app


@celery_app.task(bind=True, max_retries=5, default_retry_delay=5*60)
def fill_user_data(self, user_pk):
    User = get_user_model()
    user = User.objects.get(pk=user_pk)

    try:
        user.get_data_from_clearbit()
    except HTTPError as exc:
        if exc.response.status_code != 422:
            self.retry()
