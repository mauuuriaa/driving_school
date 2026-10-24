from typing import Any

from django.views.generic import TemplateView

from school.models import School, Student


class ShowSchoolView(TemplateView):
    template_name = "school/show_school.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['school'] = School.objects.all()
        context['debug_info'] = f"Всего школ: {School.objects.count()}"
        context['student_count'] = Student.objects.count()
        return context