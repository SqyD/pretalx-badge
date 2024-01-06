from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from pretalx.common.mixins.views import PermissionRequired


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

