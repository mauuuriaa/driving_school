from django.http import HttpResponse
from django.shortcuts import render
from typing import Any, Dict


from django.views import View
from driving_school.models import School
from django.views.generic import TemplateView

class ShowSchollView(TemplateView):
    template_name = "school/show_school.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['school'] = School.objects.all()

        return context



