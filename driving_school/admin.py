from django.contrib import admin

from driving_school.models import School, Student, Course, Car, Instructor

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "school_name", "school_course", "user")
    list_filter = ("school_name", "school_course", "user")  # фильтр по юзеру


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['car_number', 'model', 'car_make', 'vehicle_category']

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'car', 'school_name']

 