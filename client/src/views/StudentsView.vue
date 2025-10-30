<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

const students = ref([]);
const schools = ref([]);
const courses = ref([]);
const studentsPictureRef = ref();
const studentAddImageUrl = ref();
const studentEditPictureRef = ref();
const studentEditImageUrl = ref();



const loading = ref(false);

const studentToAdd = ref({
  name: '',
  age: '',
  school_name: '',
  school_course: ''
})

const studentToEdit = ref({}); // выбранный студент для редактирования

async function fetchCourses() {
  const r = await axios.get('/api/courses/')
  courses.value = r.data
}

async function fetchSchools() {
  const r = await axios.get('/api/schools/')
  schools.value = r.data
}

async function fetchStudents() {
  loading.value = true
  const r = await axios.get('/api/students/')
  students.value = r.data
  loading.value = false
}

async function onLoadClick() {
  await fetchStudents();
}

async function studentAddPictureChange(){
  studentAddImageUrl.value = URL.createObjectURL(studentsPictureRef.value.files[0])
}

async function onStudentAdd() {
  try {
    const formData = new FormData();

    // добавляем обычные поля
    formData.set('name', studentToAdd.value.name);
    formData.set('age', studentToAdd.value.age);
    formData.set('school_name', studentToAdd.value.school_name);
    formData.set('school_course', studentToAdd.value.school_course);

    // добавляем файл, если выбран
    if (studentsPictureRef.value?.files?.length) {
      formData.append('picture', studentsPictureRef.value.files[0]);
    }

    // отправляем multipart/form-data
    await axios.post('/api/students/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    // очищаем форму
    studentToAdd.value = { name: '', age: '', school_name: '', school_course: '' };
    
    // сброс поля file и превью картинки
    if (studentsPictureRef.value) studentsPictureRef.value.value = '';
    studentAddImageUrl.value = null;

    await fetchStudents();
  } catch (error) {
    console.error('Ошибка при добавлении студента:', error.response?.data || error);
  }
}

async function onRemoveClick(student) {
  try {
    await axios.delete(`/api/students/${student.id}/`)
    await fetchStudents()
  } catch (error) {
    console.error('Ошибка при удалении:', error.response?.data || error)
  }
}

// открыть модалку для редактирования
async function onStudentEditClick(student) {
  studentToEdit.value = { ...student }

  // Если есть текущее фото, показываем его в превью
  studentEditImageUrl.value = student.picture || null

  // Сбрасываем поле file, чтобы не было старого выбранного файла
  if (studentEditPictureRef.value) studentEditPictureRef.value.value = ''
}

// сохранить изменения
async function onUpdateStudent() {
  try {
    const formData = new FormData();
    formData.set('name', studentToEdit.value.name);
    formData.set('age', studentToEdit.value.age);
    formData.set('school_name', studentToEdit.value.school_name);
    formData.set('school_course', studentToEdit.value.school_course);

    if (studentEditPictureRef.value?.files?.length) {
      formData.append('picture', studentEditPictureRef.value.files[0]);
    }

    await axios.put(`/api/students/${studentToEdit.value.id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    studentEditImageUrl.value = null;
    if (studentEditPictureRef.value) studentEditPictureRef.value.value = '';

    await fetchStudents();
  } catch (error) {
    console.error('Ошибка при обновлении:', error.response?.data || error);
  }
}


function studentEditPictureChange() {
  if (studentEditPictureRef.value?.files?.length) {
    studentEditImageUrl.value = URL.createObjectURL(studentEditPictureRef.value.files[0]);
  }
}

onBeforeMount(async () => {
  await Promise.all([fetchStudents(), fetchSchools(), fetchCourses()])
})
</script>

<template>
  <h3 class="mb-3">Ученики</h3>

  <!-- Форма добавления -->
  <form @submit.prevent.stop="onStudentAdd" class="mb-3">
    <div class="row g-2 align-items-center">
      <!-- ФИО -->
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="studentToAdd.name" required />
          <label>ФИО</label>
        </div>
      </div>

      <!-- Фото -->
      <div class="col-auto">
        <input class="form-control" type="file" ref="studentsPictureRef" @change="studentAddPictureChange" accept="image/*">
      </div>
      <div class="col-auto">
        <img :src="studentAddImageUrl" alt="" style="max-height: 60px; border-radius: 5px;">
      </div>

      <!-- Возраст -->
      <div class="col">
        <div class="form-floating">
          <input type="number" class="form-control" v-model="studentToAdd.age" required />
          <label>Возраст</label>
        </div>
      </div>

      <!-- Школа -->
      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="studentToAdd.school_name" required>
            <option :value="s.id" v-for="s in schools" :key="s.id">{{ s.name }}</option>
          </select>
          <label>Школа</label>
        </div>
      </div>

      <!-- Группа -->
      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="studentToAdd.school_course" required>
            <option :value="c.id" v-for="c in courses" :key="c.id">{{ c.name }}</option>
          </select>
          <label>Группа</label>
        </div>
      </div>

      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </div>
  </form>

  <!-- Список учеников -->
  <div v-if="loading">Загрузка...</div>
  <div v-else>
    <div
      v-for="item in students"
      :key="item.id"
      class="student-item d-flex align-items-center justify-content-between border p-2 rounded mb-2"
    >
      <div v-if="item.picture">
        <img :src="item.picture" style="max-height: 60px; border-radius: 5px;" />
      </div>
      <div class="flex-grow-1 ms-3 text-start">
        <strong>{{ item.name }}</strong>, возраст — {{ item.age }} лет,
        школа: {{ item.school_name_display }},
        группа: {{ item.school_course_display }}
      </div>

      <div class="btn-group">
        <button
          class="btn btn-success btn-sm"
          @click="onStudentEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editStudentModal"
        >
          <i class="bi bi-pen-fill"></i>
        </button>

        <button class="btn btn-danger btn-sm" @click="onRemoveClick(item)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  </div>

  <!-- Модальное окно редактирования -->
  <div class="modal fade" id="editStudentModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать ученика</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>

        <div class="modal-body">
          <div class="mb-3">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="studentToEdit.name" />
              <label>ФИО</label>
            </div>
          </div>

          

          <div class="mb-3">
            <div class="form-floating">
              <input type="number" class="form-control" v-model="studentToEdit.age" />
              <label>Возраст</label>
            </div>
          </div>

          <div class="mb-3">
            <div class="form-floating">
              <select class="form-select" v-model="studentToEdit.school_name">
                <option :value="s.id" v-for="s in schools" :key="s.id">{{ s.name }}</option>
              </select>
              <label>Школа</label>
            </div>
          </div>

          <div class="mb-3">
            <div class="form-floating">
              <select class="form-select" v-model="studentToEdit.school_course">
                <option :value="c.id" v-for="c in courses" :key="c.id">{{ c.name }}</option>
              </select>
              <label>Группа</label>
            </div>
          </div>

          <div class="mb-3">
            <label>Изменить фото</label>
            <input type="file" class="form-control" ref="studentEditPictureRef" @change="studentEditPictureChange" accept="image/*" />
          </div>
          <div v-if="studentEditImageUrl" class="mb-3">
            <img :src="studentEditImageUrl" style="max-height: 100px; border-radius: 5px;" />
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateStudent">Сохранить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.student-item {
  transition: all 0.2s ease;
}
.student-item:hover {
  background-color: #f8f9fa;
}
</style>



