from rest_framework import serializers
from driving_school.models import School, Student, Car, Instructor, Course

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'car_number', 'model', 'car_make', 'vehicle_category']


class InstructorSerializer(serializers.ModelSerializer):
    school_name_display = serializers.CharField(source='school_name.name', read_only=True)
    car_display = serializers.CharField(source='car.car_number', read_only=True)

    class Meta:
        model = Instructor
        fields = ['id', 'name', 'age', 'car', 'school_name', 'car_display', 'school_name_display', "picture"]


class StudentSerializer(serializers.ModelSerializer):
    school_name = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    school_course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    school_name_display = serializers.CharField(source='school_name.name', read_only=True)
    school_course_display = serializers.CharField(source='school_course.name', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id',
            'name',
            'age',
            'school_name',
            'school_course',
            'school_name_display',
            'school_course_display',
            'picture',
            'user'
        ]
        read_only_fields = ['user']  # пользователь указывается автоматически

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)
