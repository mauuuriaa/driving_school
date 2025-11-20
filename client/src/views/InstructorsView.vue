<script setup>
import { ref, onBeforeMount, computed } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")

// Данные
const instructors = ref([])
const cars = ref([])
const schools = ref([])
const stats = ref(null)
const loading = ref(false)

// Фильтры для инструкторов
const instructorFilters = ref({
  name: '',
  age: '',
  car: '',
  school_name: ''
})

// Добавление/редактирование
const instructorToAdd = ref({ name: '', age: '', car: '', school_name: '' })
const instructorToEdit = ref({})

// Файлы и превью
const instructorAddPictureRef = ref()
const instructorAddImageUrl = ref()
const instructorEditPictureRef = ref()
const instructorEditImageUrl = ref()

// Отфильтрованные инструкторы
const filteredInstructors = computed(() => {
  return instructors.value.filter(instructor => {
    return (
      instructor.name.toLowerCase().includes(instructorFilters.value.name.toLowerCase()) &&
      instructor.age.toString().includes(instructorFilters.value.age) &&
      (instructorFilters.value.car === '' || instructor.car?.toString() === instructorFilters.value.car) &&
      (instructorFilters.value.school_name === '' || instructor.school_name?.toString() === instructorFilters.value.school_name)
    );
  });
});

// Уникальные значения для автодополнения
const uniqueNames = computed(() => {
  const names = instructors.value.map(instructor => instructor.name);
  return [...new Set(names)].sort();
});

const uniqueAges = computed(() => {
  const ages = instructors.value.map(instructor => instructor.age);
  return [...new Set(ages)].sort((a, b) => a - b);
});

// Сброс фильтров
function resetFilters() {
  instructorFilters.value = {
    name: '',
    age: '',
    car: '',
    school_name: ''
  };
}

//Статистика
async function fetchStats() {
  try {
    const r = await axios.get('/api/instructors/stats/')
    stats.value = r.data
  } catch (e) {
    console.error("Ошибка получения статистики", e)
  }
}

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
  await Promise.all([fetchInstructors(), fetchCars(), fetchSchools(), fetchStats()])
})
</script>

<template>
  <h3 class="mb-3">Инструкторы</h3>

  <div v-if="stats" class="alert alert-info mb-4">
    <h5 class="alert-heading">Статистика</h5>
    <div class="d-flex gap-4">
      <div>Всего инструкторов: <strong>{{ stats.count }}</strong></div>
      <div v-if="stats.avg">Средний возраст: <strong>{{ stats.avg.toFixed(1) }}</strong></div>
      <div v-if="stats.max">Макс. возраст: <strong>{{ stats.max }}</strong></div>
      <div v-if="stats.min">Мин. возраст: <strong>{{ stats.min }}</strong></div>
    </div>
  </div>

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
            <option value="">Выберите машину</option>
            <option :value="c.id" v-for="c in cars" :key="c.id">{{ c.car_number }} ({{ c.model }})</option>
          </select>
          <label>Машина</label>
        </div>
      </div>

      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="instructorToAdd.school_name" required>
            <option value="">Выберите школу</option>
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

  <!-- Панель фильтров -->
  <div class="card mb-3">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h6 class="mb-0">Фильтры</h6>
      <button class="btn btn-outline-secondary btn-sm" @click="resetFilters">
        Сбросить фильтры
      </button>
    </div>
    <div class="card-body">
      <div class="row g-2">
        <!-- Фильтр по ФИО -->
        <div class="col-md-3">
          <div class="form-floating">
            <input 
              type="text" 
              class="form-control" 
              v-model="instructorFilters.name" 
              placeholder="ФИО"
              list="namesList"
            />
            <label>ФИО</label>
          </div>
          <datalist id="namesList">
            <option :value="name" v-for="name in uniqueNames" :key="name">
              {{ name }}
            </option>
          </datalist>
        </div>

        <!-- Фильтр по возрасту -->
        <div class="col-md-2">
          <div class="form-floating">
            <input 
              type="number" 
              class="form-control" 
              v-model="instructorFilters.age" 
              placeholder="Возраст"
              list="agesList"
            />
            <label>Возраст</label>
          </div>
          <datalist id="agesList">
            <option :value="age" v-for="age in uniqueAges" :key="age">
              {{ age }}
            </option>
          </datalist>
        </div>

        <!-- Фильтр по машине -->
        <div class="col-md-3">
          <div class="form-floating">
            <select class="form-select" v-model="instructorFilters.car">
              <option value="">Все машины</option>
              <option :value="c.id" v-for="c in cars" :key="c.id">
                {{ c.car_number }} ({{ c.model }})
              </option>
            </select>
            <label>Машина</label>
          </div>
        </div>

        <!-- Фильтр по школе -->
        <div class="col-md-2">
          <div class="form-floating">
            <select class="form-select" v-model="instructorFilters.school_name">
              <option value="">Все школы</option>
              <option :value="s.id" v-for="s in schools" :key="s.id">
                {{ s.name }}
              </option>
            </select>
            <label>Школа</label>
          </div>
        </div>

        <!-- Счетчик результатов -->
        <div class="col-md-2 d-flex align-items-center">
          <small class="text-muted">
            Найдено: {{ filteredInstructors.length }}
          </small>
        </div>
      </div>
    </div>
  </div>

  <!-- Список инструкторов -->
  <div v-if="loading">Загрузка...</div>
  <div v-else>
    <div
      v-for="inst in filteredInstructors"
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

    <!-- Сообщение, если ничего не найдено -->
    <div v-if="filteredInstructors.length === 0 && instructors.length > 0" class="text-center text-muted py-4">
      <i class="bi bi-search display-4 d-block mb-2"></i>
      <p>Инструкторы не найдены</p>
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
                <option value="">Выберите машину</option>
                <option :value="c.id" v-for="c in cars" :key="c.id">{{ c.car_number }} ({{ c.model }})</option>
              </select>
              <label>Машина</label>
            </div>
          </div>

          <div class="mb-3">
            <div class="form-floating">
              <select class="form-select" v-model="instructorToEdit.school_name">
                <option value="">Выберите школу</option>
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