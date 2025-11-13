from django.core.management.base import BaseCommand
from faker import Faker
import random, os, shutil

from django.conf import settings
from django.contrib.auth.models import User
from driving_school.models import School, Course, Car, Instructor, Student


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])

        # --- Настройки ---
        photos_dir = r"E:\politex\3kyrs\django2\media\sample_photos"
        os.makedirs(os.path.join(settings.MEDIA_ROOT, "students"), exist_ok=True)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, "instructors"), exist_ok=True)

        # --- Фото ---
        male_photos = [os.path.join(photos_dir, f) for f in os.listdir(photos_dir)
                       if f.lower().startswith("man") and f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        female_photos = [os.path.join(photos_dir, f) for f in os.listdir(photos_dir)
                         if f.lower().startswith("woman") and f.lower().endswith(('.jpg', '.jpeg', '.png'))]

      

 
        # --- Школы ---
        for _ in range(1000):
            School.objects.create(name=fake.company())

        # --- Курсы ---
        for _ in range(1000):
            Course.objects.create(name=f"Группа {fake.random_uppercase_letter()}{fake.random_int(1, 9)}")

        # --- Машины ---
        for _ in range(1000):
            Car.objects.create(
                car_number=f"{fake.random_uppercase_letter()}{fake.random_int(100,999)}{fake.random_uppercase_letter()}",
                model=random.choice(["Lada", "Kia Rio", "Toyota Corolla", "Hyundai Solaris", "Ford Focus"]),
                car_make=random.choice(["Sedan", "Hatchback", "Crossover"]),
                vehicle_category=random.choice(["A", "B", "C"])
            )

        schools = list(School.objects.all())
        courses = list(Course.objects.all())
        cars = list(Car.objects.all())
        users = list(User.objects.all()) or [User.objects.create_user(username="test_user", password="12345")]

        # --- Инструкторы ---
        for i in range(1000):
            gender = random.choice(["male", "female"])
            name = fake.name_male() if gender == "male" else fake.name_female()
            photo_src = random.choice(male_photos if gender == "male" else female_photos)
            photo_filename = f"instructors/instructor_{i+1}_{os.path.basename(photo_src)}"
            dest_path = os.path.join(settings.MEDIA_ROOT, photo_filename)
            shutil.copy(photo_src, dest_path)

            Instructor.objects.create(
                name=name,
                age=str(fake.random_int(25, 65)),
                school_name=random.choice(schools),
                car=random.choice(cars),
                picture=photo_filename
            )

        # --- Студенты ---
        for i in range(1000):
            gender = random.choice(["male", "female"])
            name = fake.name_male() if gender == "male" else fake.name_female()
            photo_src = random.choice(male_photos if gender == "male" else female_photos)
            photo_filename = f"students/student_{i+1}_{os.path.basename(photo_src)}"
            dest_path = os.path.join(settings.MEDIA_ROOT, photo_filename)
            shutil.copy(photo_src, dest_path)

            Student.objects.create(
                name=name,
                age=str(fake.random_int(16, 60)),
                school_course=random.choice(courses),
                school_name=random.choice(schools),
                user=random.choice(users),
                picture=photo_filename
            )

        
