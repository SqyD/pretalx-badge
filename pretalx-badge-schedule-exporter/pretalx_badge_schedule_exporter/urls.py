
from django.urls import include, path, re_path
from pretalx.event.models.event import SLUG_REGEX

from pretalx.agenda.views.schedule import ExporterView

from .views import BadgeScheduleExportRoomDay


urlpatterns = [
    #re_path(
    #    rf"^orga/event/(?P<event>{SLUG_REGEX})/settings/p/pretalx_badge_schedule_exporter/$",
    #    BadgeScheduleExporterSettings.as_view(),
    #    name="settings",
    #),
    #re_path(
        # fr"^(?P<event>[{SLUG_REGEX}]+)/schedule/badge/<int:room>_day<int:day>.json$",
        #fr"<slug:event>/ schedule/badge/bla.json",
        #BadgeScheduleExportRoomDay.as_view(),
        # name="badge_schedule_room_day",
    #),
]
urlpatterns = [
    path(
        "<slug:event>/",
        include(
            [
                path(
                    "schedule/badge/<str:room>_day<int:day>.json",
                    BadgeScheduleExportRoomDay.as_view(),
                    # ExporterView.as_view(),
                    # name="export.schedule.badge_schedule_roomday",
                    name="export.badge_schedule_room_day.json",
                )
            ]
        )
    )
]
