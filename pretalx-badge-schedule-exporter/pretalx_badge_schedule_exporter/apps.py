from django.apps import AppConfig
from django.utils.translation import gettext_lazy

from . import __version__


class PluginApp(AppConfig):
    name = "pretalx_badge_schedule_exporter"
    verbose_name = "pretalx Badge schedule exporter"

    class PretalxPluginMeta:
        name = gettext_lazy("pretalx Badge schedule exporter")
        author = "SqyD"
        description = gettext_lazy("Generates minimal schedule json export files for consumption by embedded systems such as the conference badges by badge.team")
        visible = True
        version = __version__
        category = "EXPORTER"

    def ready(self):
        from . import signals  # NOQA
