<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

const schools = ref([]);
const loading = ref(false);

const schoolToAdd = ref({ name: '' });
const schoolToEdit = ref({}); // выбранная школа для редактирования

// Загрузка школ
async function fetchSchools() {
  loading.value = true;
  const r = await axios.get('/api/schools/');
  schools.value = r.data;
  loading.value = false;
}

// Добавление новой школы
async function onSchoolAdd() {
  try {
    await axios.post('/api/schools/', { name: schoolToAdd.value.name });
    schoolToAdd.value = { name: '' };
    await fetchSchools();
  } catch (error) {
    console.error('Ошибка при добавлении школы:', error.response?.data || error);
  }
}

// Удаление школы
async function onRemoveClick(school) {
  try {
    await axios.delete(`/api/schools/${school.id}/`);
    await fetchSchools();
  } catch (error) {
    console.error('Ошибка при удалении школы:', error.response?.data || error);
  }
}

// Открытие модалки редактирования
async function onSchoolEditClick(school) {
  schoolToEdit.value = { ...school };
}

// Сохранение изменений
async function onUpdateSchool() {
  try {
    await axios.put(`/api/schools/${schoolToEdit.value.id}/`, { name: schoolToEdit.value.name });
    await fetchSchools();
  } catch (error) {
    console.error('Ошибка при обновлении школы:', error.response?.data || error);
  }
}

onBeforeMount(async () => {
  await fetchSchools();
});
</script>

<template>
<h3 class="mb-3">Автошколы</h3>
  <!-- Форма добавления школы -->
  <form @submit.prevent.stop="onSchoolAdd" class="mb-3">
    <div class="row g-2 align-items-center">
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="schoolToAdd.name" required />
          <label>Название школы</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </div>
  </form>

  <!-- Список школ -->
  <div v-if="loading">Загрузка...</div>
  <div v-else>
    <div
      v-for="school in schools"
      :key="school.id"
      class="school-item d-flex align-items-center justify-content-between border p-2 rounded mb-2"
    >
      <div>
        {{ school.name }}
      </div>

      <div class="btn-group">
        <button
          class="btn btn-success btn-sm"
          @click="onSchoolEditClick(school)"
          data-bs-toggle="modal"
          data-bs-target="#editSchoolModal"
        >
          <i class="bi bi-pen-fill"></i>
        </button>

        <button class="btn btn-danger btn-sm" @click="onRemoveClick(school)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  </div>

  <!-- Модальное окно редактирования -->
  <div class="modal fade" id="editSchoolModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать школу</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>

        <div class="modal-body">
          <div class="mb-3">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="schoolToEdit.name" />
              <label>Название школы</label>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateSchool">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.school-item {
  transition: all 0.2s ease;
}
.school-item:hover {
  background-color: #f8f9fa;
}
</style>
