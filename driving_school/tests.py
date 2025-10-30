from rest_framework.test import APIClient
from django.test import TestCase
from driving_school.models import Student, Course, School, Car, Instructor
from model_bakery import baker

# Create your tests here.
class StudentsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    

    def test_get_list(self):
        course = Course.objects.create(
        name="20-1"
        )

        school = School.objects.create(
        name="Трек"
        )

        student = Student.objects.create(
            name="Василий Андреевич Иванов",
            age="21",
            school_course=course,
            school_name = school,
        )

        r = self.client.get('/api/students/')
        data = r.json()
        print(data)

        assert student.name == data[0]['name']
        assert student.age == data[0]['age']
        assert student.school_course.id == data[0]['school_course']
        assert student.school_name.id == data[0]['school_name']['id']
        assert len(data) == 1

        

    def test_create_student(self):
        crs = baker.make("driving_school.Course")
                
        r = self.client.post("/api/students/", {
        "name": "Иван",
        "age": "18",
        "school_course": crs.id,
        })

        new_student_id = r.json()['id']
        students = Student.objects.all()
        assert len(students) == 1

        new_student = Student.objects.filter(id=new_student_id).first()
        assert new_student.name == "Иван"
        assert new_student.age == "18"
        assert new_student.school_course == crs
    
    def test_delete_student(self):
        students = baker.make("Student", 10)
        r = self.client.get("/api/students/")
        data = r.json()
        assert len(data) == 10

        student_id_to_delete = students[3].id
        self.client.delete(f"/api/students/{student_id_to_delete}/")

        r = self.client.get('/api/students/')
        data = r.json()
        assert len(data) == 9

        assert student_id_to_delete not in [i['id'] for i in data]
    
    def test_update_student(self):
        students = baker.make("Student", 10)
        student: Student = students[2]

        r = self.client.put(f"/api/students/{student.id}/", {
            "name": "Женя Петрушин",
            "age": student.age,          
            "school_course": student.school_course.id if student.school_course else "",
            "school_name": student.school_name.id if student.school_name else "",
        })
        assert r.status_code == 200

        r = self.client.get(f"/api/students/{student.id}/")
        data = r.json()
        assert data['name'] == "Женя Петрушин"

        student.refresh_from_db()
        assert data['name'] == student.name

    


class SchoolsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    

    def test_get_list(self):
        
        school = School.objects.create(
        name="Трек2.0"
        )

        r = self.client.get('/api/schools/')
        data = r.json()
        print(data)

        assert school.name == data[0]['name']
        assert school.id == data[0]['id']
        assert len(data) == 1

    def test_create_school(self):
                        
        r = self.client.post("/api/schools/", {
        "name": "Трек"
        })

        new_school_id = r.json()['id']
        schools = School.objects.all()
        assert len(schools) == 1

        new_school = School.objects.filter(id=new_school_id).first()
        assert new_school.name == "Трек"

    def test_delete_school(self):
        schools = baker.make("School", 10)
        r = self.client.get("/api/schools/")
        data = r.json()
        assert len(data) == 10

        school_id_to_delete = schools[3].id
        self.client.delete(f"/api/schools/{school_id_to_delete}/")

        r = self.client.get('/api/schools/')
        data = r.json()
        assert len(data) == 9

        assert school_id_to_delete not in [i['id'] for i in data]

    def test_update_school(self):
        schools = baker.make("School", 10)
        school: School = schools[2]

        r = self.client.put(f"/api/schools/{school.id}/", {
            "name": "Пульс",
            
        })
        assert r.status_code == 200

        r = self.client.get(f"/api/schools/{school.id}/")
        data = r.json()
        assert data['name'] == "Пульс"

        school.refresh_from_db()
        assert data['name'] == school.name
       

class CarsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    

    def test_get_list(self):
        
        car = Car.objects.create(
        car_number="О345ПР138",
        model="Логан",
        car_make = "Рено",
        vehicle_category = "B",
        )

        r = self.client.get('/api/cars/')
        data = r.json()
        print(data)

        assert car.car_number == data[0]['car_number']
        assert car.model == data[0]['model']
        assert car.car_make == data[0]['car_make']
        assert car.vehicle_category == data[0]['vehicle_category']
        assert len(data) == 1

    def test_create_car(self):
                        
        r = self.client.post("/api/cars/", {
        "car_number": "О345ПР138",
        "model":"Логан",
        "car_make":"Рено",
        "vehicle_category":"B"
        })

        cars = Car.objects.all()
        assert len(cars) == 1

        new_car = cars.first()
        assert new_car.car_number == "О345ПР138"
        assert new_car.model == "Логан"
        assert new_car.car_make == "Рено"
        assert new_car.vehicle_category == "B"

    def test_delete_car(self):
        cars = baker.make("Car", 10)
        r = self.client.get("/api/cars/")
        data = r.json()
        assert len(data) == 10

        car_to_delete = cars[3]
        self.client.delete(f"/api/cars/{car_to_delete.id}/")

        r = self.client.get('/api/cars/')
        data = r.json()
        assert len(data) == 9

        assert car_to_delete.car_number not in [i['car_number'] for i in data]

    def test_update_car(self):
        cars = baker.make("Car", 10)
        car: Car = cars[2]

        r = self.client.put(f"/api/cars/{car.id}/", {
            "car_number": "О345ПР138",
            "model":"Логан",
            "car_make":"Рено",
            "vehicle_category":"B"
        })
        assert r.status_code == 200

        r = self.client.get(f"/api/cars/{car.id}/")
        data = r.json()
        assert data['car_number'] == "О345ПР138"

        car.refresh_from_db()
        assert data['car_number'] == car.car_number



class CoursesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    

    def test_get_list(self):
        
        course = Course.objects.create(
        name="20-2"
        )

        r = self.client.get('/api/courses/')
        data = r.json()
        print(data)

        assert course.name == data[0]['name']
        assert len(data) == 1

    def test_create_course(self):
                        
        r = self.client.post("/api/courses/", {
        "name": "25-4"
        })

        courses = Course.objects.all()
        assert len(courses) == 1

        new_courses = courses.first()
        assert new_courses.name == "25-4"

    def test_delete_course(self):
        courses = baker.make("Course", 10)
        r = self.client.get("/api/courses/")
        data = r.json()
        assert len(data) == 10

        course_to_delete = courses[3]
        self.client.delete(f"/api/courses/{course_to_delete.id}/")

        r = self.client.get('/api/courses/')
        data = r.json()
        assert len(data) == 9

        assert course_to_delete.name not in [i['name'] for i in data]
    
    def test_update_course(self):
        courses = baker.make("Course", 10)
        course: Course = courses[2]

        r = self.client.put(f"/api/courses/{course.id}/", {
            "name": "25-1",
            
        })
        assert r.status_code == 200

        r = self.client.get(f"/api/courses/{course.id}/")
        data = r.json()
        assert data['name'] == "25-1"

        course.refresh_from_db()
        assert data['name'] == course.name

       



class InstructorViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    

    def test_get_list(self):
        car = Car.objects.create(
        car_number="О255ПР138",
        model="Логан",
        car_make = "Рено",
        vehicle_category = "B",
        )

        school = School.objects.create(
        name="Трек3.0"
        )

        instructor = Instructor.objects.create(
            name="Покровский Григорий Даниилович",
            age="49",
            car=car,
            school_name = school,
        )

        r = self.client.get('/api/instructors/')
        data = r.json()
        print(data)

        assert instructor.name == data[0]['name']
        assert instructor.age == data[0]['age']
        assert instructor.car.car_number == data[0]['car']['car_number'] 
        assert instructor.school_name.id == data[0]['school_name']['id']
        assert len(data) == 1

    def test_create_instructor(self):
  
                
        r = self.client.post("/api/instructors/", {
        "name": "Иван",
        "age": "18",
        })    

        instructors = Instructor.objects.all()
        assert len(instructors) == 1

        new_instructor = instructors.first()
        assert new_instructor.name == "Иван"
        assert new_instructor.age == "18"

    def test_delete_instructor(self):
        instructors = baker.make("Instructor", 10)
        r = self.client.get("/api/instructors/")
        data = r.json()
        assert len(data) == 10

        instructor_to_delete = instructors[3]
        self.client.delete(f"/api/instructors/{instructor_to_delete.id}/")

        r = self.client.get('/api/instructors/')
        data = r.json()
        assert len(data) == 9

        assert instructor_to_delete.name not in [i['name'] for i in data]

    def test_update_instructor(self):
        instructors = baker.make("Instructor", 10)
        instructor: Instructor = instructors[2]

        r = self.client.put(f"/api/instructors/{instructor.id}/", {
            "name": "Женя Петрушин",
            "age": instructor.age,          

        })
        assert r.status_code == 200

        r = self.client.get(f"/api/instructors/{instructor.id}/")
        data = r.json()
        assert data['name'] == "Женя Петрушин"

        instructor.refresh_from_db()
        assert data['name'] == instructor.name

       
        

    

