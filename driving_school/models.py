from django.db import models


class School(models.Model):
    name = models.TextField("Название школы")

    class Meta:
        verbose_name = "Автошкола"
        verbose_name_plural = "Автошколы"

    def __str__(self) -> str:
        return self.name
    
class Course(models.Model):
    name = models.TextField("Группа")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self) -> str:
        return self.name

class Student(models.Model):
    name = models.TextField("ФИО")
    age = models.TextField("Возраст")
    school_course = models.ForeignKey("Course", on_delete=models.CASCADE, null=True)
    school_name = models.ForeignKey("School", on_delete=models.CASCADE, null=True)

    picture = models.ImageField("Изображение", null=True, upload_to="students")

    class Meta:
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"

class Instructor(models.Model):
    name = models.TextField("ФИО")
    age = models.TextField("Возраст")
    car = models.ForeignKey("Car", on_delete=models.CASCADE, null=True)
    school_name = models.ForeignKey("School", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Инструктор"
        verbose_name_plural = "Инструкторы"


class Car(models.Model):
    car_number = models.TextField("Номер")
    model = models.TextField("Модель")
    car_make = models.TextField("Марка")
    vehicle_category = models.TextField("Категория транспортного средства")

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"

    def __str__(self) -> str:
        return self.car_number


    
