import datetime as dt
import json
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import vobject
from django.template.loader import get_template
from django.utils.functional import cached_property
from i18nfield.utils import I18nJSONEncoder

from pretalx import __version__
from pretalx.common.exporter import BaseExporter
from pretalx.schedule.exporters import ScheduleData
from pretalx.common.urls import get_base_url


class BadgeExporterBase(ScheduleData):
    identifier = "badge_schedule_base"
    verbose_name = "Conference Basic info as JSON (badge optimized)"
    public = True
    icon = "{ }"
    cors = "*"

    def get_data(self, **kwargs):
        schedule = self.schedule
        return {
            "version": schedule.version,
            "base_url": self.metadata["base_url"],
            "conference": {
                "acronym": self.event.slug,
                "title": str(self.event.name),
                "start": self.event.date_from.strftime("%Y-%m-%d"),
                "end": self.event.date_to.strftime("%Y-%m-%d"),
                "daysCount": self.event.duration,
                "time_zone_name": self.event.timezone,
                "rooms": [
                    {
                        "name": str(room.name),
                        "id": room.id,
                        "description": str(room.description) or None,
                    }
                    for room in self.event.rooms.all()
                ],
                "days": [
                    {
                        "index": day["index"],
                        "date": day["start"].strftime("%Y-%m-%d"),
                        "day_start": day["start"].astimezone(self.event.tz).isoformat(),
                        "day_end": day["end"].astimezone(self.event.tz).isoformat(),
                    }
                    for day in self.data
                ],
            },
        }

    def render(self, **kwargs):
        content = self.get_data()
        return (
            f"{self.event.slug}.json".format(self.event.slug),
            "application/json",
            json.dumps({"event": content}, cls=I18nJSONEncoder),
        )

class BadgeExporterRoomDay(ScheduleData):
    identifier = "badge_schedule_room_day"
    verbose_name = "Schedule by Room and Day (badge optimized)"
    public = True
    icon = "{ }"
    cors = "*"


    def get_data(self, **kwargs):
        schedule = self.schedule
        thisday = self.day
        thisroom = self.room
        talks_data = {}
        for day in self.data:
            if day['index'] == thisday:
               for room in day["rooms"]:
                   if room['id'] == thisroom:
                        for talk in room["talks"]:
                            index = talk.id
                            talks_data[index] = {
                                "id": talk.submission.id,
                                "start": talk.local_start.strftime("%H:%M"),
                                "duration": talk.export_duration,
                                "title": talk.submission.title,
                            }
        return talks_data


    def render(self, **kwargs):
        content = self.get_data()
        return (
            f"{self.event.slug}.json".format(self.event.slug),
            "application/json",
            json.dumps({"schedule": content}, cls=I18nJSONEncoder),
        )

class BadgeExporterTalk(ScheduleData):
    identifier = "badge_schedule_talk"
    verbose_name = "Detailed talk info as JSON (badge optimized)"
    public = True
    icon = "{ }"
    cors = "*"

    def get_data(self, **kwargs):
        schedule = self.schedule
        thistalk = self.talk
        print(thistalk)
        for day in self.data:
           for room in day["rooms"]:
                for talk in room["talks"]:
                    print(talk)
                    if talk.submission.id == thistalk:
                        talk_data = {
                            "id": talk.submission.id,
                            "date": talk.local_start.isoformat(),
                            "start": talk.local_start.strftime("%H:%M"),
                            "duration": talk.export_duration,
                            "room": str(room["name"]),
                            "title": talk.submission.title,
                            "track": str(talk.submission.track.name)
                            if talk.submission.track
                            else None,
                            "type": str(talk.submission.submission_type.name),
                            "language": talk.submission.content_locale,
                            "abstract": talk.submission.abstract,
                            "description": talk.submission.description,
                            "persons": [
                                {
                                    "id": person.id,
                                    "public_name": person.get_display_name()
                                }
                                for person in talk.submission.speakers.all()
                            ],
                        }
        return talk_data

    def render(self, **kwargs):
        content = self.get_data()
        return (
            f"{self.event.slug}.json".format(self.event.slug),
            "application/json",
            json.dumps({"talk": content}, cls=I18nJSONEncoder),
        )
