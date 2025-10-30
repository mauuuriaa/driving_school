from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import mixins

from driving_school.models import School, Student, Car, Instructor, Course


from driving_school.serializers import SchoolSerializer, StudentSerializer, CarSerializer, InstructorSerializer, CourseSerializer


class SchoolViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class StudentViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CarViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class InstructorViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

class CourseViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer