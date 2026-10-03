<script setup>
import { ref, computed, onBeforeMount } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import { useUserStore } from "@/stores/user_store";
import { storeToRefs } from "pinia";

const userStore = useUserStore();
const { userInfo } = storeToRefs(userStore);


const cars = ref([]);
const carsStats = ref(null);
const carToAdd = ref({ car_number: "", model: "", car_make: "", vehicle_category: "" });
const carToEdit = ref({});

const filterCarNumber = ref("");
const filterModel = ref("");
const filterCarMake = ref("");
const filterVehicleCategory = ref("");

const filteredCars = computed(() => {
  return cars.value.filter(car =>
    (!filterCarNumber.value || car.car_number.toLowerCase().includes(filterCarNumber.value.toLowerCase())) &&
    (!filterModel.value || car.model.toLowerCase().includes(filterModel.value.toLowerCase())) &&
    (!filterCarMake.value || car.car_make.toLowerCase().includes(filterCarMake.value.toLowerCase())) &&
    (!filterVehicleCategory.value || car.vehicle_category.toLowerCase().includes(filterVehicleCategory.value.toLowerCase()))
  );
});


async function fetchCars() {
  const r = await axios.get("/api/cars/");
  cars.value = r.data;
}

async function fetchCarsStats() {
  const r = await axios.get("/api/cars/stats/");
  carsStats.value = r.data;
}

async function onAddCar() {
  await axios.post("/api/cars/", carToAdd.value);
  carToAdd.value = { car_number: "", model: "", car_make: "", vehicle_category: "" };
  await Promise.all([fetchCars(), fetchCarsStats()]);
}

function onEditClick(car) {
  carToEdit.value = { ...car };
}

async function onUpdateCar() {
  await axios.put(`/api/cars/${carToEdit.value.id}/`, carToEdit.value);
  await Promise.all([fetchCars(), fetchCarsStats()]);

  const modalEl = document.getElementById('editCarModal');
  const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
  modal.hide();
}

async function onRemoveClick(car) {
  await axios.delete(`/api/cars/${car.id}/`);
  await Promise.all([fetchCars(), fetchCarsStats()]);
}

onBeforeMount(async () => {
  await Promise.all([fetchCars(), fetchCarsStats()]);
});
</script>

<template>
  <div>
    <h3>Машины</h3>

    <div v-if="carsStats" class="mb-3 p-2 border rounded bg-light">
      <strong>Статистика по машинам:</strong>
      <div>Всего машин: {{ carsStats.count }}</div>

    </div>

    <form v-if="userInfo?.is_superuser" @submit.prevent="onAddCar" class="mb-3 row g-2">
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
    </form>

    <div class="mb-3 row g-2">
      <div class="col">
        <input type="text" class="form-control" v-model="filterCarNumber" placeholder="Фильтр по номеру" />
      </div>
      <div class="col">
        <input type="text" class="form-control" v-model="filterModel" placeholder="Фильтр по модели" />
      </div>
      <div class="col">
        <input type="text" class="form-control" v-model="filterCarMake" placeholder="Фильтр по марке" />
      </div>
      <div class="col">
        <input type="text" class="form-control" v-model="filterVehicleCategory" placeholder="Фильтр по категории" />
      </div>
    </div>

    <div v-for="car in filteredCars" :key="car.id" class="car-item border rounded p-2 mb-2 d-flex justify-content-between align-items-center">
      <div>
        <strong>{{ car.car_number }}</strong> — {{ car.model }} ({{ car.car_make }}), категория: {{ car.vehicle_category }}
      </div>

      <div v-if="userInfo?.is_superuser" class="btn-group">
        <button class="btn btn-success btn-sm" @click="onEditClick(car)" data-bs-toggle="modal" data-bs-target="#editCarModal">
          <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-danger btn-sm" @click="onRemoveClick(car)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>

    <div v-if="filteredCars.length === 0" class="text-center text-muted py-4">
      <i class="bi bi-search display-4 d-block mb-2"></i>
      <p>Машины не найдены</p>
    </div>

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
            <button class="btn btn-primary" @click="onUpdateCar">Сохранить</button>
          </div>
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
