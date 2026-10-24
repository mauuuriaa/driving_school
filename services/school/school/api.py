from django.db.models import Count, Avg, Max, Min
from django.http import HttpResponse
import openpyxl
from rest_framework import mixins, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from school.models import School, Student, Car, Instructor, Course
from school.serializers import (
    SchoolSerializer,
    StudentSerializer,
    CarSerializer,
    InstructorSerializer,
    CourseSerializer
)


class StatsSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    avg = serializers.FloatField(allow_null=True)
    max = serializers.FloatField(allow_null=True)
    min = serializers.FloatField(allow_null=True)


class SchoolViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request):
        stats = School.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        serializer = StatsSerializer(stats)
        return Response(serializer.data)


class StudentViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = StudentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Student.objects.all()
        if user.is_authenticated:
            return Student.objects.filter(user_id=user.id)
        return Student.objects.none()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request):
        queryset = self.get_queryset()
        stats = queryset.aggregate(
            count=Count("*"),
            avg=Avg("age"),
            max=Max("age"),
            min=Min("age"),
        )
        serializer = StatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], url_path="export")
    def export_excel(self, request):
        user = request.user
        is_2fa = getattr(user, 'second_factor_active', False)

        can_download = user.is_staff or user.is_superuser or (user.is_authenticated and is_2fa)

        if not can_download:
            return Response(status=403)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename=students.xlsx'

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Students"

        columns = ['ID', 'ФИО', 'Возраст', 'Школа', 'Курс']
        ws.append(columns)

        students = self.get_queryset()

        for student in students:
            ws.append([
                student.id,
                student.name,
                student.age,
                str(student.school_name) if student.school_name else '-',
                str(student.school_course) if student.school_course else '-'
            ])

        wb.save(response)
        return response


class CarViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request):
        stats = Car.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        serializer = StatsSerializer(stats)
        return Response(serializer.data)


class InstructorViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request):
        stats = Instructor.objects.aggregate(
            count=Count("*"),
            avg=Avg("age"),
            max=Max("age"),
            min=Min("age")
        )
        serializer = StatsSerializer(stats)
        return Response(serializer.data)


class CourseViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request):
        stats = Course.objects.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        serializer = StatsSerializer(stats)
        return Response(serializer.data)