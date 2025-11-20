<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

const cars = ref([]);
const stats = ref(null);
const loading = ref(false);

// Фильтры для машин
const carFilters = ref({
  car_number: '',
  model: '',
  car_make: '',
  vehicle_category: ''
});

const carToAdd = ref({
  car_number: '',
  model: '',
  car_make: '',
  vehicle_category: ''
});

const carToEdit = ref({});

// Отфильтрованные машины
const filteredCars = computed(() => {
  return cars.value.filter(car => {
    return (
      car.car_number.toLowerCase().includes(carFilters.value.car_number.toLowerCase()) &&
      (carFilters.value.model === '' || car.model === carFilters.value.model) &&
      (carFilters.value.car_make === '' || car.car_make === carFilters.value.car_make) &&
      (carFilters.value.vehicle_category === '' || car.vehicle_category === carFilters.value.vehicle_category)
    );
  });
});

// Уникальные значения для автодополнения и выпадающих списков
const uniqueCarNumbers = computed(() => {
  const numbers = cars.value.map(car => car.car_number);
  return [...new Set(numbers)].sort();
});

const uniqueModels = computed(() => {
  const models = cars.value.map(car => car.model);
  return [...new Set(models)].sort();
});

const uniqueMakes = computed(() => {
  const makes = cars.value.map(car => car.car_make);
  return [...new Set(makes)].sort();
});

const uniqueCategories = computed(() => {
  const categories = cars.value.map(car => car.vehicle_category);
  return [...new Set(categories)].sort();
});

// Сброс фильтров
function resetFilters() {
  carFilters.value = {
    car_number: '',
    model: '',
    car_make: '',
    vehicle_category: ''
  };
}

//Статистика
async function fetchStats() {
  try {
    const r = await axios.get('/api/cars/stats/')
    stats.value = r.data
  } catch (e) {
    console.error("Ошибка получения статистики", e)
  }
}

async function fetchCars() {
  loading.value = true;
  const r = await axios.get('/api/cars/');
  cars.value = r.data;
  loading.value = false;
}

async function onAddCar() {
  try {
    await axios.post('/api/cars/', { ...carToAdd.value });
    carToAdd.value = { car_number: '', model: '', car_make: '', vehicle_category: '' };
    await fetchCars();
  } catch (error) {
    console.error('Ошибка при добавлении машины:', error.response?.data || error);
  }
}

async function onEditClick(car) {
  carToEdit.value = { ...car };
}

async function onUpdateCar() {
  try {
    await axios.put(`/api/cars/${carToEdit.value.id}/`, { ...carToEdit.value });
    await fetchCars();
  } catch (error) {
    console.error('Ошибка при обновлении машины:', error.response?.data || error);
  }
}

async function onRemoveClick(car) {
  try {
    await axios.delete(`/api/cars/${car.id}/`);
    await fetchCars();
  } catch (error) {
    console.error('Ошибка при удалении машины:', error.response?.data || error);
  }
}

onBeforeMount(async () => {
    await fetchCars();
    await fetchStats(); 
});
</script>

<template>
  <h3 class="mb-3">Машины</h3>
  
  <div v-if="stats" class="alert alert-info mb-4">
    <h5 class="alert-heading">Статистика</h5>
    <div class="d-flex gap-4"> 
      <span class="me-3">Всего машин: {{ stats.count }}</span>
      <span class="me-3">Макс. ID: {{ stats.max }}</span>
      <span class="me-3">Мин. ID: {{ stats.min }}</span>
    </div>
  </div>

  <!-- Форма добавления -->
  <form @submit.prevent.stop="onAddCar" class="mb-4">
    <div class="row g-2">
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="carToAdd.car_number" required />
          <label>Номер</label>
        </div>
      </div>

      <!-- Модель - выпадающий список -->
      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="carToAdd.model" required>
            <option value="">Выберите модель</option>
            <option :value="model" v-for="model in uniqueModels" :key="model">
              {{ model }}
            </option>
          </select>
          <label>Модель</label>
        </div>
      </div>

      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="carToAdd.car_make" required>
            <option value="">Выберите марку</option>
            <option :value="make" v-for="make in uniqueMakes" :key="make">
              {{ make }}
            </option>
          </select>
          <label>Марка</label>
        </div>
      </div>

      <div class="col">
        <div class="form-floating">
          <select class="form-select" v-model="carToAdd.vehicle_category" required>
            <option value="">Выберите категорию</option>
            <option :value="category" v-for="category in uniqueCategories" :key="category">
              {{ category }}
            </option>
          </select>
          <label>Категория ТС</label>
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
        <!-- Фильтр по номеру -->
        <div class="col-md-3">
          <div class="form-floating">
            <input 
              type="text" 
              class="form-control" 
              v-model="carFilters.car_number" 
              placeholder="Номер"
              list="carNumbersList"
            />
            <label>Номер</label>
          </div>
          <datalist id="carNumbersList">
            <option :value="number" v-for="number in uniqueCarNumbers" :key="number">
              {{ number }}
            </option>
          </datalist>
        </div>

        <!-- Фильтр по модели (выпадающий список) -->
        <div class="col-md-3">
          <div class="form-floating">
            <select class="form-select" v-model="carFilters.model">
              <option value="">Все модели</option>
              <option :value="model" v-for="model in uniqueModels" :key="model">
                {{ model }}
              </option>
            </select>
            <label>Модель</label>
          </div>
        </div>

        <!-- Фильтр по марке (выпадающий список) -->
        <div class="col-md-3">
          <div class="form-floating">
            <select class="form-select" v-model="carFilters.car_make">
              <option value="">Все марки</option>
              <option :value="make" v-for="make in uniqueMakes" :key="make">
                {{ make }}
              </option>
            </select>
            <label>Марка</label>
          </div>
        </div>

        <!-- Фильтр по категории (выпадающий список) -->
        <div class="col-md-3">
          <div class="form-floating">
            <select class="form-select" v-model="carFilters.vehicle_category">
              <option value="">Все категории</option>
              <option :value="category" v-for="category in uniqueCategories" :key="category">
                {{ category }}
              </option>
            </select>
            <label>Категория ТС</label>
          </div>
        </div>

        <!-- Счетчик результатов -->
        <div class="col-12 mt-2">
          <small class="text-muted">
            Найдено машин: {{ filteredCars.length }}
          </small>
        </div>
      </div>
    </div>
  </div>

  <!-- Список машин -->
  <div v-if="loading">Загрузка...</div>
  <div v-else>
    <div
      v-for="car in filteredCars"
      :key="car.id"
      class="car-item border rounded p-2 mb-2 d-flex justify-content-between align-items-center"
    >
      <div>
        <strong>{{ car.car_number }}</strong> — {{ car.model }} ({{ car.car_make }}),
        категория: {{ car.vehicle_category }}
      </div>

      <div class="btn-group">
        <button
          class="btn btn-success btn-sm"
          @click="onEditClick(car)"
          data-bs-toggle="modal"
          data-bs-target="#editCarModal"
        >
          <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-danger btn-sm" @click="onRemoveClick(car)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>

    <!-- Сообщение, если ничего не найдено -->
    <div v-if="filteredCars.length === 0 && cars.length > 0" class="text-center text-muted py-4">
      <i class="bi bi-search display-4 d-block mb-2"></i>
      <p>Машины не найдены</p>
    </div>
  </div>

  <!-- Модалка редактирования -->
  <div class="modal fade" id="editCarModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Редактировать машину</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">
          <div class="form-floating mb-3">
            <input type="text" class="form-control" v-model="carToEdit.car_number" />
            <label>Номер</label>
          </div>

          <!-- Модель - выпадающий список -->
          <div class="form-floating mb-3">
            <select class="form-select" v-model="carToEdit.model">
              <option value="">Выберите модель</option>
              <option :value="model" v-for="model in uniqueModels" :key="model">
                {{ model }}
              </option>
            </select>
            <label>Модель</label>
          </div>

          <div class="form-floating mb-3">
            <select class="form-select" v-model="carToEdit.car_make">
              <option value="">Выберите марку</option>
              <option :value="make" v-for="make in uniqueMakes" :key="make">
                {{ make }}
              </option>
            </select>
            <label>Марка</label>
          </div>

          <div class="form-floating mb-3">
            <select class="form-select" v-model="carToEdit.vehicle_category">
              <option value="">Выберите категорию</option>
              <option :value="category" v-for="category in uniqueCategories" :key="category">
                {{ category }}
              </option>
            </select>
            <label>Категория ТС</label>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button
            class="btn btn-primary"
            data-bs-dismiss="modal"
            @click="onUpdateCar"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.car-item {
  transition: all 0.2s ease;
}
.car-item:hover {
  background-color: #f8f9fa;
}
</style>