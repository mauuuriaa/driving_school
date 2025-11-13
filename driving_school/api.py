from rest_framework import viewsets, mixins
from driving_school.models import School, Student, Car, Instructor, Course
from driving_school.serializers import (
    SchoolSerializer,
    StudentSerializer,
    CarSerializer,
    InstructorSerializer,
    CourseSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from django.db.models import Count, Avg, Max, Min


class StatsSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    avg = serializers.FloatField()
    max = serializers.FloatField()
    min = serializers.FloatField()


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
            return Student.objects.filter(user=user)
        return Student.objects.none()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request):
        queryset = self.get_queryset()  # чтобы статистика была по доступным пользователю данным
        stats = queryset.aggregate(
            count=Count("*"),
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
        )
        serializer = StatsSerializer(stats)
        return Response(serializer.data)


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
            avg=Avg("id"),
            max=Max("id"),
            min=Min("id")
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
