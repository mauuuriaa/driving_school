from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from school import views
from school.api import SchoolViewset, StudentViewset, CarViewset, InstructorViewset, CourseViewset

router = DefaultRouter()
router.register("schools", SchoolViewset, basename="schools")
router.register("students", StudentViewset, basename="students")
router.register("cars", CarViewset, basename="cars")
router.register("instructors", InstructorViewset, basename="instructor")
router.register("courses", CourseViewset, basename="courses")

urlpatterns = [
    path('', views.ShowSchoolView.as_view()),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)