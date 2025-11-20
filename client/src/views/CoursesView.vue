<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

const courses = ref([]);
const stats = ref(null);
const loading = ref(false);

// Фильтр для групп
const courseFilter = ref('');

const courseToAdd = ref({ name: '' });
const courseToEdit = ref({}); // выбранная группа для редактирования

// Отфильтрованные группы
const filteredCourses = computed(() => {
  if (!courseFilter.value) {
    return courses.value;
  }
  return courses.value.filter(course => 
    course.name.toLowerCase().includes(courseFilter.value.toLowerCase())
  );
});

// Уникальные названия групп для автодополнения
const uniqueCourseNames = computed(() => {
  const names = courses.value.map(course => course.name);
  return [...new Set(names)].sort();
});

// Сброс фильтра
function resetFilter() {
  courseFilter.value = '';
}

//Статистика
async function fetchStats() {
  try {
    const r = await axios.get('/api/courses/stats/')
    stats.value = r.data
  } catch (e) {
    console.error("Ошибка получения статистики", e)
  }
}

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
  await fetchStats();
});
</script>

<template>
  <h3 class="mb-3">Группы</h3>

  <div v-if="stats" class="alert alert-info mb-4">
    <h5 class="alert-heading">Статистика</h5>
    <div class="d-flex gap-4"> 
      <span class="me-3">Всего групп: {{ stats.count }}</span>
      <span class="me-3">Макс. ID: {{ stats.max }}</span>
      <span class="me-3">Мин. ID: {{ stats.min }}</span>
    </div>
  </div>

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

  <!-- Панель фильтра -->
  <div class="card mb-3">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h6 class="mb-0">Фильтр</h6>
      <button class="btn btn-outline-secondary btn-sm" @click="resetFilter">
        Сбросить фильтр
      </button>
    </div>
    <div class="card-body">
      <div class="row g-2 align-items-center">
        <!-- Фильтр по названию группы -->
        <div class="col-md-6">
          <div class="form-floating">
            <input 
              type="text" 
              class="form-control" 
              v-model="courseFilter" 
              placeholder="Название группы"
              list="courseNamesList"
            />
            <label>Название группы</label>
          </div>
          <datalist id="courseNamesList">
            <option :value="name" v-for="name in uniqueCourseNames" :key="name">
              {{ name }}
            </option>
          </datalist>
        </div>
        
        <!-- Счетчик результатов -->
        <div class="col-md-6">
          <small class="text-muted">
            Найдено групп: {{ filteredCourses.length }} 
          </small>
        </div>
      </div>
    </div>
  </div>

  <!-- Список групп -->
  <div v-if="loading">Загрузка...</div>
  <div v-else>
    <div
      v-for="course in filteredCourses"
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

    <!-- Сообщение, если ничего не найдено -->
    <div v-if="filteredCourses.length === 0 && courses.length > 0" class="text-center text-muted py-4">
      <i class="bi bi-search display-4 d-block mb-2"></i>
      <p>Группы не найдены</p>
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