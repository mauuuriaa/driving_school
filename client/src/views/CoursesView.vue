<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

const courses = ref([]);
const loading = ref(false);

const courseToAdd = ref({ name: '' });
const courseToEdit = ref({}); // выбранная группа для редактирования

// Загрузка групп
async function fetchCourses() {
  loading.value = true;
  const r = await axios.get('/api/courses/');
  courses.value = r.data;
  loading.value = false;
}

// Добавление новой группы
async function onCourseAdd() {
  try {
    await axios.post('/api/courses/', { name: courseToAdd.value.name });
    courseToAdd.value = { name: '' };
    await fetchCourses();
  } catch (error) {
    console.error('Ошибка при добавлении группы:', error.response?.data || error);
  }
}

// Удаление группы
async function onRemoveClick(course) {
  try {
    await axios.delete(`/api/courses/${course.id}/`);
    await fetchCourses();
  } catch (error) {
    console.error('Ошибка при удалении группы:', error.response?.data || error);
  }
}

// Открытие модалки редактирования
async function onCourseEditClick(course) {
  courseToEdit.value = { ...course };
}

// Сохранение изменений
async function onUpdateCourse() {
  try {
    await axios.put(`/api/courses/${courseToEdit.value.id}/`, { name: courseToEdit.value.name });
    await fetchCourses();
  } catch (error) {
    console.error('Ошибка при обновлении группы:', error.response?.data || error);
  }
}

onBeforeMount(async () => {
  await fetchCourses();
});
</script>

<template>
<h3 class="mb-3">Группы</h3>
  <!-- Форма добавления группы -->
  <form @submit.prevent.stop="onCourseAdd" class="mb-3">
    <div class="row g-2 align-items-center">
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="courseToAdd.name" required />
          <label>Название группы</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </div>
  </form>

  <!-- Список групп -->
  <div v-if="loading">Загрузка...</div>
  <div v-else>
    <div
      v-for="course in courses"
      :key="course.id"
      class="course-item d-flex align-items-center justify-content-between border p-2 rounded mb-2"
    >
      <div>
        {{ course.name }}
      </div>

      <div class="btn-group">
        <button
          class="btn btn-success btn-sm"
          @click="onCourseEditClick(course)"
          data-bs-toggle="modal"
          data-bs-target="#editCourseModal"
        >
          <i class="bi bi-pen-fill"></i>
        </button>

        <button class="btn btn-danger btn-sm" @click="onRemoveClick(course)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  </div>

  <!-- Модальное окно редактирования -->
  <div class="modal fade" id="editCourseModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать группу</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>

        <div class="modal-body">
          <div class="mb-3">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="courseToEdit.name" />
              <label>Название группы</label>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateCourse">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.course-item {
  transition: all 0.2s ease;
}
.course-item:hover {
  background-color: #f8f9fa;
}
</style>
