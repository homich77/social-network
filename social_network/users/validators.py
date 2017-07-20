import json
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

from django.conf import settings
from rest_framework.exceptions import ValidationError


class EmailHunterValidate:
    valid_params = settings.EMAILHUNTER_VALID_PARAMS.items()
    message = 'Email address is not valid.'

    def __call__(self, value):
        url = '{}?{}'.format(
            settings.EMAILHUNTER_URL,
            urlencode({
                'api_key': settings.EMAILHUNTER_KEY,
                'email': value,
            })
        )

        try:
            with urlopen(url) as response:
                body = json.loads(response.read().decode('utf8'))
        except HTTPError:
            raise ValidationError(self.message)

        if not self.valid_params <= body['data'].items():
            raise ValidationError(self.message)
