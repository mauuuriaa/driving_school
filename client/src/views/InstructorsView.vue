<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")

// Данные
const instructors = ref([])
const cars = ref([])
const schools = ref([])
const loading = ref(false)

// Добавление/редактирование
const instructorToAdd = ref({ name: '', age: '', car: '', school_name: '' })
const instructorToEdit = ref({})

// Файлы и превью
const instructorAddPictureRef = ref()
const instructorAddImageUrl = ref()
const instructorEditPictureRef = ref()
const instructorEditImageUrl = ref()

// Получение данных
async function fetchInstructors() {
  loading.value = true
  const r = await axios.get('/api/instructors/')
  instructors.value = r.data
  loading.value = false
}

async function fetchCars() {
  const r = await axios.get('/api/cars/')
  cars.value = r.data
}

async function fetchSchools() {
  const r = await axios.get('/api/schools/')
  schools.value = r.data
}

// Изменение превью фото
function instructorAddPictureChange() {
  if (instructorAddPictureRef.value?.files?.length) {
    instructorAddImageUrl.value = URL.createObjectURL(instructorAddPictureRef.value.files[0])
  }
}

function instructorEditPictureChange() {
  if (instructorEditPictureRef.value?.files?.length) {
    instructorEditImageUrl.value = URL.createObjectURL(instructorEditPictureRef.value.files[0])
  }
}

// Добавление инструктора
async function onInstructorAdd() {
  try {
    const formData = new FormData()
    formData.set('name', instructorToAdd.value.name)
    formData.set('age', instructorToAdd.value.age)
    formData.set('car', instructorToAdd.value.car)
    formData.set('school_name', instructorToAdd.value.school_name)
    if (instructorAddPictureRef.value?.files?.length) {
      formData.append('picture', instructorAddPictureRef.value.files[0])
    }

    await axios.post('/api/instructors/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    // Очистка формы
    instructorToAdd.value = { name: '', age: '', car: '', school_name: '' }
    if (instructorAddPictureRef.value) instructorAddPictureRef.value.value = ''
    instructorAddImageUrl.value = null

    await fetchInstructors()
  } catch (error) {
    console.error('Ошибка при добавлении инструктора:', error.response?.data || error)
  }
}

// Удаление
async function onRemoveClick(inst) {
  try {
    await axios.delete(`/api/instructors/${inst.id}/`)
    await fetchInstructors()
  } catch (error) {
    console.error('Ошибка при удалении:', error.response?.data || error)
  }
}

// Редактирование
async function onInstructorEditClick(inst) {
  instructorToEdit.value = { ...inst }
  instructorEditImageUrl.value = inst.picture || null
  if (instructorEditPictureRef.value) instructorEditPictureRef.value.value = ''
}

// Сохранение изменений
async function onUpdateInstructor() {
  try {
    const formData = new FormData()
    formData.set('name', instructorToEdit.value.name)
    formData.set('age', instructorToEdit.value.age)
    formData.set('car', instructorToEdit.value.car)
    formData.set('school_name', instructorToEdit.value.school_name)
    if (instructorEditPictureRef.value?.files?.length) {
      formData.append('picture', instructorEditPictureRef.value.files[0])
    }

    await axios.put(`/api/instructors/${instructorToEdit.value.id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    instructorEditImageUrl.value = null
    if (instructorEditPictureRef.value) instructorEditPictureRef.value.value = ''

    await fetchInstructors()
  } catch (error) {
    console.error('Ошибка при обновлении инструктора:', error.response?.data || error)
  }
}

// Инициализация
onBeforeMount(async () => {
  await Promise.all([fetchInstructors(), fetchCars(), fetchSchools()])
})
</script>

<template>
  <h3 class="mb-3">Инструкторы</h3>

  <!-- Форма добавления -->
  <form @submit.prevent="onInstructorAdd" class="mb-3">
    <div class="row g-2 align-items-center">
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="instructorToAdd.name" required />
          <label>ФИО</label>
        </div>
      </div>

      <div class="col-auto">
        <input class="form-control" type="file" ref="instructorAddPictureRef" @change="instructorAddPictureChange" accept="image/*" />
      </div>
      <div class="col-auto" v-if="instructorAddImageUrl">
        <img :src="instructorAddImageUrl" style="max-height: 60px; border-radius: 5px;" />
      </div>

      <div class="col">
        <div class="form-floating">
          <input type="number" class="form-control" v-model="instructorToAdd.age" required />
          <label>Возраст</label>
        </div>
      </div>

      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="instructorToAdd.car" required>
            <option :value="c.id" v-for="c in cars" :key="c.id">{{ c.car_number }} ({{ c.model }})</option>
          </select>
          <label>Машина</label>
        </div>
      </div>

      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="instructorToAdd.school_name" required>
            <option :value="s.id" v-for="s in schools" :key="s.id">{{ s.name }}</option>
          </select>
          <label>Школа</label>
        </div>
      </div>

      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </div>
  </form>

  <!-- Список инструкторов -->
  <div v-if="loading">Загрузка...</div>
  <div v-else>
    <div
      v-for="inst in instructors"
      :key="inst.id"
      class="instructor-item d-flex align-items-center justify-content-between border p-2 rounded mb-2"
    >
      <div v-if="inst.picture">
        <img :src="inst.picture" style="max-height: 60px; border-radius: 5px;" />
      </div>
      <div class="flex-grow-1 ms-3 text-start">
        <strong>{{ inst.name }}</strong>, возраст — {{ inst.age }} лет,
        школа: {{ inst.school_name_display }},
        авто: {{ inst.car_display }}
      </div>

      <div class="btn-group">
        <button
          class="btn btn-success btn-sm"
          @click="onInstructorEditClick(inst)"
          data-bs-toggle="modal"
          data-bs-target="#editInstructorModal"
        >
          <i class="bi bi-pen-fill"></i>
        </button>

        <button class="btn btn-danger btn-sm" @click="onRemoveClick(inst)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  </div>

  <!-- Модалка редактирования -->
  <div class="modal fade" id="editInstructorModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать инструктора</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">
          <div class="mb-3">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="instructorToEdit.name" />
              <label>ФИО</label>
            </div>
          </div>

          <div class="mb-3">
            <input class="form-control" type="file" ref="instructorEditPictureRef" @change="instructorEditPictureChange" accept="image/*" />
          </div>
          <div v-if="instructorEditImageUrl" class="mb-3">
            <img :src="instructorEditImageUrl" style="max-height: 100px; border-radius:5px;" />
          </div>

          <div class="mb-3">
            <div class="form-floating">
              <input type="number" class="form-control" v-model="instructorToEdit.age" />
              <label>Возраст</label>
            </div>
          </div>

          <div class="mb-3">
            <div class="form-floating">
              <select class="form-select" v-model="instructorToEdit.car">
                <option :value="c.id" v-for="c in cars" :key="c.id">{{ c.car_number }}</option>
              </select>
              <label>Машина</label>
            </div>
          </div>

          <div class="mb-3">
            <div class="form-floating">
              <select class="form-select" v-model="instructorToEdit.school_name">
                <option :value="s.id" v-for="s in schools" :key="s.id">{{ s.name }}</option>
              </select>
              <label>Школа</label>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateInstructor">Сохранить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.instructor-item {
  transition: all 0.2s ease;
}
.instructor-item:hover {
  background-color: #f8f9fa;
}
</style>
