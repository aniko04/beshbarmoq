from django.apps import AppConfig
from django.core.checks import Warning, register


class HomeConfig(AppConfig):
    name = 'home'

    def ready(self):
        register(_rasmli_test_rasmlari)


def _rasmli_test_rasmlari(app_configs, **kwargs):
    """«Rasmli test» rasmlari joyidami — `manage.py check` tekshiradi.

    Rasmlar Worddan skript bilan yasaladi; bittasi tushib qolsa sahifada
    jimgina buzuq rasm chiqadi, shuning uchun uni shu yerda ushlaymiz.
    """
    from . import rasmli_test
    yoq = rasmli_test.yetishmagan_rasmlar()
    if not yoq:
        return []
    return [Warning(
        "«Rasmli test» rasmlari yetishmayapti: " + ', '.join(yoq),
        hint="static/img/rasmli-test/ ni Worddan qayta yasang.",
        id='home.W001',
    )]
