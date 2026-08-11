from django.apps import AppConfig
from django.core.checks import Warning, register


class HomeConfig(AppConfig):
    name = 'home'

    def ready(self):
        register(_rasmli_test_rasmlari)
        register(_diktant_rasmlari)
        register(_qalamdon_fayllari)
        register(_xonqizi_fayllari)


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


def _qalamdon_fayllari(app_configs, **kwargs):
    """«Qalamdon» xaritasining rasm va videolari joyidami.

    Videolar `media/` da turadi va hech qanday yig'ish bosqichidan
    o'tmaydi — ko'chirilmay qolsa sahifada bo'sh pleyer qoladi, xato esa
    hech qayerda ko'rinmaydi. Shuning uchun ular ham shu yerda sanaladi.
    """
    from . import qalamdon
    yoq = qalamdon.yetishmagan_fayllar()
    if not yoq:
        return []
    return [Warning(
        "«Qalamdon» xaritasi fayllari yetishmayapti: " + ', '.join(yoq),
        hint="static/img/qalamdon/ va media/xarita/qalamdon/ ni tekshiring.",
        id='home.W003',
    )]


def _xonqizi_fayllari(app_configs, **kwargs):
    """«Xonqizi» xaritasining rasm va videolari joyidami — W003 bilan bir xil sabab."""
    from . import xonqizi
    yoq = xonqizi.yetishmagan_fayllar()
    if not yoq:
        return []
    return [Warning(
        "«Xonqizi» xaritasi fayllari yetishmayapti: " + ', '.join(yoq),
        hint="static/img/xonqizi/ va media/xarita/xonqizi/ ni tekshiring.",
        id='home.W004',
    )]
