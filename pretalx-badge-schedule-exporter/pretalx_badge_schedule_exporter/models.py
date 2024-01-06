from django.db import models




class BadgeScheduleExporterSettings(models.Model):
    event = models.OneToOneField(
        to="event.Event",
        on_delete=models.CASCADE,
        related_name="pretalx_badge_schedule_exporter_settings",
    )
    some_setting = models.CharField(max_length=10, default="A")

