<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

const students = ref([]);
const schools = ref([]);
const courses = ref([]);
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

async function onStudentAdd() {
  try {
    await axios.post('/api/students/', {
      name: studentToAdd.value.name,
      age: studentToAdd.value.age,
      school_name: studentToAdd.value.school_name,
      school_course: studentToAdd.value.school_course
    })

    studentToAdd.value = { name: '', age: '', school_name: '', school_course: '' }
    await fetchStudents()
  } catch (error) {
    console.error('Ошибка при добавлении студента:', error.response?.data || error)
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
}

// сохранить изменения
async function onUpdateStudent() {
  try {
    await axios.put(`/api/students/${studentToEdit.value.id}/`, {
      name: studentToEdit.value.name,
      age: studentToEdit.value.age,
      school_name: studentToEdit.value.school_name,
      school_course: studentToEdit.value.school_course
    })
    await fetchStudents()
  } catch (error) {
    console.error('Ошибка при обновлении:', error.response?.data || error)
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
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="studentToAdd.name" required />
          <label>ФИО</label>
        </div>
      </div>

      <div class="col">
        <div class="form-floating">
          <input type="number" class="form-control" v-model="studentToAdd.age" required />
          <label>Возраст</label>
        </div>
      </div>

      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="studentToAdd.school_name" required>
            <option :value="s.id" v-for="s in schools" :key="s.id">{{ s.name }}</option>
          </select>
          <label>Школа</label>
        </div>
      </div>

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
      <div>
        <strong>{{ item.name }}</strong> — {{ item.age }} лет,
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
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>

        <div class="modal-body">
          <div class="mb-3">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="studentToEdit.name"
              />
              <label>ФИО</label>
            </div>
          </div>

          <div class="mb-3">
            <div class="form-floating">
              <input
                type="number"
                class="form-control"
                v-model="studentToEdit.age"
              />
              <label>Возраст</label>
            </div>
          </div>

          <div class="mb-3">
            <div class="form-floating">
              <select class="form-select" v-model="studentToEdit.school_name">
                <option :value="s.id" v-for="s in schools" :key="s.id">
                  {{ s.name }}
                </option>
              </select>
              <label>Школа</label>
            </div>
          </div>

          <div class="mb-3">
            <div class="form-floating">
              <select class="form-select" v-model="studentToEdit.school_course">
                <option :value="c.id" v-for="c in courses" :key="c.id">
                  {{ c.name }}
                </option>
              </select>
              <label>Группа</label>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            Закрыть
          </button>
          <button
            data-bs-dismiss="modal"
            type="button"
            class="btn btn-primary"
            @click="onUpdateStudent"
          >
            Сохранить
          </button>
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
