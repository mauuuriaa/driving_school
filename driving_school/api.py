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
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny


# Общий сериализатор статистики (оставь как есть, но убедись, что он такой)
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
            return Student.objects.filter(user=user)
        return Student.objects.none()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request):
        queryset = self.get_queryset()
        stats = queryset.aggregate(
            count=Count("*"),
            avg=Avg("age"),  # Средний возраст
            max=Max("age"),  # Максимальный возраст
            min=Min("age"),  # Минимальный возраст
        )
        serializer = StatsSerializer(stats)
        return Response(serializer.data)


# 3. МАШИНЫ (У машин нет числовых полей, считаем по ID или просто количество)
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


# 2. ИНСТРУКТОРЫ (Считаем статистику по возрасту)
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


# 4. КУРСЫ
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
    

class UserViewset(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["POST"], url_path="login")
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Неверный логин или пароль"}, status=400)

        token, created = Token.objects.get_or_create(user=user)

        # Возвращаем токен
        return Response({"token": token.key, "username": user.username})

    @action(detail=False, methods=["POST"], url_path="logout")
    def logout(self, request):
        # Удаляем токен, если он передан
        if request.user.is_authenticated:
             # Удаляем токен пользователя
             request.user.auth_token.delete()
        return Response({"status": "ok"})

    @action(detail=False, methods=["GET"], url_path="me")
    def me(self, request):
        # Проверяем авторизацию
        if not request.user.is_authenticated:
            return Response({"is_authenticated": False, "user": None})
            
        # Если авторизован
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "is_superuser": request.user.is_superuser,
            "is_authenticated": True  
        })
