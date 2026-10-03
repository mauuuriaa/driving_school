# models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import pyotp


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
    age = models.IntegerField("Возраст")
    school_course = models.ForeignKey("Course", on_delete=models.CASCADE, null=True)
    school_name = models.ForeignKey("School", on_delete=models.CASCADE, null=True)
    picture = models.ImageField("Изображение", null=True, upload_to="students")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"


class Instructor(models.Model):
    name = models.TextField("ФИО")
    age = models.IntegerField("Возраст")
    car = models.ForeignKey("Car", on_delete=models.CASCADE, null=True)
    school_name = models.ForeignKey("School", on_delete=models.CASCADE, null=True)
    picture = models.ImageField("Изображение", null=True, upload_to="instructors")

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


class UserProfile(TimestampModel):
    class Type(models.TextChoices):
        STUDENT = 'student', 'Студент'
        INSTRUCTOR = 'instructor', 'Инструктор'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(choices=Type.choices, max_length=20)
    totp_key = models.CharField(max_length=128, null=True, blank=True)
    student = models.OneToOneField(
        "Student",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    instructor = models.OneToOneField(
        "Instructor",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} ({self.type})"
    def save(self, *args, **kwargs):
        if not self.totp_key:
            self.totp_key = pyotp.random_base32()
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()