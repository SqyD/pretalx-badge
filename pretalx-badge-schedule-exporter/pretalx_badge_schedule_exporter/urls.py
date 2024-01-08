
from django.urls import include, path, re_path
from pretalx.event.models.event import SLUG_REGEX

from pretalx.agenda.views.schedule import ExporterView

from .views import BadgeScheduleExportRoomDay, BadgeScheduleTalk


urlpatterns = [
    path(
        "<slug:event>/",
        include(
            [
                path(
                    "schedule/badge/room<int:room>_day<int:day>.json",
                    BadgeScheduleExportRoomDay.as_view(),
                    name="badge_schedule_room_day",
                )
            ]
        )
    ),
    path(
        "<slug:event>/",
        include(
            [
                path(
                    "schedule/badge/talk<int:talk>.json",
                    BadgeScheduleTalk.as_view(),
                    name="badge_schedule_talk",
                )
            ]
        )
    ),
    path(
        "<slug:event>/",
        include(
            [
                path(
                    "schedule/badge/base.json",
                    ExporterView.as_view(),
                    name="export.badge_schedule_base",
                )
            ]
        )
    ),
]
