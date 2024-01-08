from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import resolve, reverse
from django.views.generic import FormView
from pretalx.common.mixins.views import PermissionRequired
from pretalx.common.signals import register_data_exporters
from pretalx.agenda.views.schedule import ExporterView

from .forms import BadgeScheduleExporterSettingsForm


class BadgeScheduleExporterSettingsView(PermissionRequired, FormView):
    permission_required = "orga.change_settings"
    template_name = "pretalx_badge_schedule_exporter/settings.html"
    form_class = BadgeScheduleExporterSettingsForm

    def get_success_url(self):
        return self.request.path

    def get_object(self):
        return self.request.event

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["event"] = self.request.event
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("The pretalx Badge schedule exporter settings were updated."))
        return super().form_valid(form)

class BadgeScheduleExportRoomDay(ExporterView):
    def get_exporter(self, request):
        url = resolve(request.path_info)
        exporter = url.url_name
        responses = register_data_exporters.send(request.event)
        for __, response in responses:
            ex = response(request.event)
            if ex.identifier == exporter:
                if ex.public or request.is_orga:
                    ex.day = int(url.kwargs.get("day"))
                    ex.room = int(url.kwargs.get("room"))
                    return ex

class BadgeScheduleTalk(ExporterView):
    def get_exporter(self, request):
        url = resolve(request.path_info)
        exporter = url.url_name
        responses = register_data_exporters.send(request.event)
        for __, response in responses:
            ex = response(request.event)
            if ex.identifier == exporter:
                if ex.public or request.is_orga:
                    ex.talk = int(url.kwargs.get("talk"))
                    return ex
