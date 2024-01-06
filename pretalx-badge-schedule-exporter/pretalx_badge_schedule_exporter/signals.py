
from django.dispatch import receiver
from django.urls import reverse
from pretalx.orga.signals import nav_event_settings
from pretalx.common.signals import register_data_exporters

@receiver(nav_event_settings)
def pretalx_badge_schedule_exporter_settings(sender, request, **kwargs):
    if not request.user.has_perm("orga.change_settings", request.event):
        return []
    return [
        {
            "label": "pretalx Badge schedule exporter",
            "url": reverse(
                "plugins:pretalx_badge_schedule_exporter:settings",
                kwargs={"event": request.event.slug},
            ),
            "active": request.resolver_match.url_name
            == "plugins:pretalx_badge_schedule_exporter:settings",
        }
    ]

@receiver(register_data_exporters, dispatch_uid="exporter_badge_base")
def register_badge_base_exporter(sender, **kwargs):
    from .exporter import BadgeExporterBase

    return BadgeExporterBase

@receiver(register_data_exporters, dispatch_uid="exporter_badge_room_day")
def register_badge_room_day_exporter(sender, **kwargs):
    from .exporter import BadgeExporterRoomDay

    return BadgeExporterRoomDay
