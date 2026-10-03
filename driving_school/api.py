# api.py
from rest_framework import viewsets, mixins
from driving_school.models import School, Student, Car, Instructor, Course, UserProfile
from driving_school.serializers import (
    SchoolSerializer,
    StudentSerializer,
    CarSerializer,
    InstructorSerializer,
    CourseSerializer
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from django.db.models import Count, Avg, Max, Min
from rest_framework.serializers import Serializer
from django.contrib.auth import authenticate, login, logout
import pyotp
import openpyxl 
from django.http import HttpResponse 


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
            avg=Avg("age"),
            max=Max("age"),
            min=Min("age"),
        )
        serializer = StatsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=["GET"], url_path="export")
    def export_excel(self, request):
        user = request.user
        is_2fa = request.session.get('second_factor_active', False)

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


class UserProfileViewSet(GenericViewSet):
    queryset = UserProfile.objects.all()

    @action(url_path="my", methods=["GET"],  detail=False)
    def get_my(self, *args, **kwargs):
        return Response({
            'username': self.request.user.username,
            'is_authenticated': self.request.user.is_authenticated,
            'is_staff': self.request.user.is_staff,
            'is_superuser': self.request.user.is_superuser,
            'second_factor_active': self.request.session.get('second_factor_active', False)
        })
    
    @action(url_path="login", methods=["POST"],  detail=False)
    def login_user(self, *args, **kwargs):
        class LoginSerializer(serializers.Serializer):
            username = serializers.CharField()
            password = serializers.CharField()
        
        serializer = LoginSerializer(data = self.request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username = username, password = password)

        if user:
            login(self.request, user)
            return Response({"status": "success"})   
        else:
            return Response({"status": "failed"}, status=401)
        
    
    @action(url_path="logout", methods=["POST"], detail=False)
    def logout_user(self, request, *args, **kwargs):  
        logout(request)
        return Response({"status": "success"})
    
    @action(url_path="get-totp", methods=['GET'], detail=False)
    def get_totp(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        
        if not user_profile.totp_key:
            user_profile.totp_key = pyotp.random_base32()
            user_profile.save()

        url = pyotp.totp.TOTP(user_profile.totp_key).provisioning_uri(
            name=request.user.username, 
            issuer_name="DrivingSchoolApp"
        )

        return Response({"url": url})

    @action(url_path="second-login", methods=['POST'], detail=False)
    def second_login(self, request, *args, **kwargs):
        key_from_user = request.data.get('key')
        user_profile = request.user.userprofile

        if not user_profile.totp_key:
             return Response({"status": "failed", "detail": "2FA not set up"}, status=400)

        totp = pyotp.totp.TOTP(user_profile.totp_key)
        
        if totp.verify(key_from_user):
            request.session['second_factor_active'] = True
            return Response({"status": "success"})
        else:
            return Response({"status": "failed", "detail": "Invalid code"}, status=400)