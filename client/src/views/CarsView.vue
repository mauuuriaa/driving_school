<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

const cars = ref([]);
const loading = ref(false);

const carToAdd = ref({
  car_number: '',
  model: '',
  car_make: '',
  vehicle_category: ''
});

const carToEdit = ref({});

// --- CRUD функции ---
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

onBeforeMount(fetchCars);
</script>

<template>
<h3 class="mb-3">Машины</h3>
  
    

    <!-- Добавление -->
    <form @submit.prevent.stop="onAddCar" class="mb-4">
      <div class="row g-2">
        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="carToAdd.car_number" required />
            <label>Номер</label>
          </div>
        </div>

        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="carToAdd.model" required />
            <label>Модель</label>
          </div>
        </div>

        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="carToAdd.car_make" required />
            <label>Марка</label>
          </div>
        </div>

        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="carToAdd.vehicle_category" required />
            <label>Категория ТС</label>
          </div>
        </div>

        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <!-- Список -->
    <div v-if="loading">Загрузка...</div>
    <div v-else>
      <div
        v-for="car in cars"
        :key="car.id"
        class="border rounded p-2 mb-2 d-flex justify-content-between align-items-center"
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

            <div class="form-floating mb-3">
              <input type="text" class="form-control" v-model="carToEdit.model" />
              <label>Модель</label>
            </div>

            <div class="form-floating mb-3">
              <input type="text" class="form-control" v-model="carToEdit.car_make" />
              <label>Марка</label>
            </div>

            <div class="form-floating mb-3">
              <input type="text" class="form-control" v-model="carToEdit.vehicle_category" />
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
