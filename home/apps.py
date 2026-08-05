from django.apps import AppConfig
from django.core.checks import Warning, register


class HomeConfig(AppConfig):
    name = 'home'

    def ready(self):
        register(_rasmli_test_rasmlari)
        register(_diktant_rasmlari)


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


def _diktant_rasmlari(app_configs, **kwargs):
    """«Texnologik diktantlar» rasmlari joyidami — W001 bilan bir xil sabab.

    64 ta rasmdan bittasi tushib qolsa, o'quvchi javob berolmaydigan
    topshiriq paydo bo'ladi; shuning uchun sahifaga chiqishdan oldin
    `manage.py check` da ushlaymiz.
    """
    from . import diktant
    yoq = diktant.yetishmagan_rasmlar()
    if not yoq:
        return []
    return [Warning(
        "«Texnologik diktantlar» rasmlari yetishmayapti: " + ', '.join(yoq),
        hint="static/img/diktant/ ni Worddan qayta yasang.",
        id='home.W002',
    )]
