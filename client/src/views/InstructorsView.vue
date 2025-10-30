<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')

const instructors = ref([])
const cars = ref([])
const schools = ref([])
const loading = ref(false)

const instructorToAdd = ref({
  name: '',
  age: '',
  car: '',
  school_name: ''
})

const instructorToEdit = ref({})

// ==== CRUD ====

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

// === Добавить ===
async function onInstructorAdd() {
  try {
    await axios.post('/api/instructors/', {
      name: instructorToAdd.value.name,
      age: instructorToAdd.value.age,
      car: instructorToAdd.value.car,
      school_name: instructorToAdd.value.school_name
    })
    instructorToAdd.value = { name: '', age: '', car: '', school_name: '' }
    await fetchInstructors()
  } catch (error) {
    console.error('Ошибка при добавлении инструктора:', error.response?.data || error)
  }
}

// === Удалить ===
async function onRemoveClick(inst) {
  try {
    await axios.delete(`/api/instructors/${inst.id}/`)
    await fetchInstructors()
  } catch (error) {
    console.error('Ошибка при удалении:', error.response?.data || error)
  }
}

// === Открыть модалку редактирования ===
function onInstructorEditClick(inst) {
  instructorToEdit.value = { ...inst }
}

// === Сохранить изменения ===
async function onUpdateInstructor() {
  try {
    await axios.put(`/api/instructors/${instructorToEdit.value.id}/`, {
      name: instructorToEdit.value.name,
      age: instructorToEdit.value.age,
      car: instructorToEdit.value.car,
      school_name: instructorToEdit.value.school_name
    })
    await fetchInstructors()
  } catch (error) {
    console.error('Ошибка при обновлении инструктора:', error.response?.data || error)
  }
}

onBeforeMount(async () => {
  await Promise.all([fetchInstructors(), fetchCars(), fetchSchools()])
})
</script>

<template>
  <h3 class="mb-3">Инструкторы</h3>

  <!-- === Форма добавления === -->
  <form @submit.prevent="onInstructorAdd" class="mb-3">
    <div class="row g-2 align-items-center">
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="instructorToAdd.name" required />
          <label>ФИО</label>
        </div>
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

  <!-- === Список инструкторов === -->
  <div v-if="loading">Загрузка...</div>
  <div v-else>
    <div
      v-for="inst in instructors"
      :key="inst.id"
      class="border rounded p-2 mb-2 d-flex justify-content-between align-items-center"
    >
      <div>
        <strong>{{ inst.name }}</strong> — {{ inst.age }} лет,  
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

  <!-- === Модалка редактирования === -->
  <div class="modal fade" id="editInstructorModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать инструктора</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">
          <div class="form-floating mb-2">
            <input type="text" class="form-control" v-model="instructorToEdit.name" />
            <label>ФИО</label>
          </div>

          <div class="form-floating mb-2">
            <input type="number" class="form-control" v-model="instructorToEdit.age" />
            <label>Возраст</label>
          </div>

          <div class="form-floating mb-2">
            <select class="form-select" v-model="instructorToEdit.car">
              <option :value="c.id" v-for="c in cars" :key="c.id">{{ c.car_number }}</option>
            </select>
            <label>Машина</label>
          </div>

          <div class="form-floating mb-2">
            <select class="form-select" v-model="instructorToEdit.school_name">
              <option :value="s.id" v-for="s in schools" :key="s.id">{{ s.name }}</option>
            </select>
            <label>Школа</label>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateInstructor">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.border:hover {
  background-color: #f8f9fa;
}
</style>
