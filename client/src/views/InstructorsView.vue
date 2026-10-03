<script setup>
import { ref, computed, onBeforeMount } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import { useUserStore } from "@/stores/user_store";
import { storeToRefs } from "pinia";

const userStore = useUserStore();
const { userInfo } = storeToRefs(userStore);


const instructorsStats = ref(null);

const instructors = ref([]);
const cars = ref([]);
const schools = ref([]);

const instructorToAdd = ref({
  name: "",
  age: "",
  car: "",
  school_name: "",
  picture: null,
});
const instructorAddPictureRef = ref();
const instructorAddImageUrl = ref(null);

const instructorToEdit = ref({});
const instructorEditPictureRef = ref();
const instructorEditImageUrl = ref(null);

const previewImage = ref(null);

const filterName = ref("");
const filterAge = ref("");
const filterCar = ref("");
const filterSchool = ref("");

const normalize = (v) => (v ?? "").toString().toLowerCase();

const filteredInstructors = computed(() => {
  return instructors.value.filter(inst => {
    return (
      normalize(inst.name).includes(normalize(filterName.value)) &&
      normalize(inst.age).includes(normalize(filterAge.value)) &&
      normalize(inst.car_display).includes(normalize(filterCar.value)) &&
      normalize(inst.school_name_display).includes(normalize(filterSchool.value))
    );
  });
});


async function fetchInstructors() {
  const r = await axios.get("/api/instructors/");
  instructors.value = r.data;
}

async function fetchCars() {
  const r = await axios.get("/api/cars/");
  cars.value = r.data;
}

async function fetchSchools() {
  const r = await axios.get("/api/schools/");
  schools.value = r.data;
}

async function fetchInstructorsStats() {
  const r = await axios.get("/api/instructors/stats/");
  instructorsStats.value = r.data;
}

function onAddPictureChange() {
  if (instructorAddPictureRef.value?.files?.length) {
    instructorToAdd.value.picture = instructorAddPictureRef.value.files[0];
    instructorAddImageUrl.value = URL.createObjectURL(instructorToAdd.value.picture);
  }
}

async function onInstructorAdd() {
  if (!instructorToAdd.value.picture) {
    alert("Выберите фото инструктора!");
    return;
  }

  const formData = new FormData();
  formData.append("name", instructorToAdd.value.name);
  formData.append("age", instructorToAdd.value.age);
  formData.append("car", instructorToAdd.value.car);
  formData.append("school_name", instructorToAdd.value.school_name);
  formData.append("picture", instructorToAdd.value.picture);

  await axios.post("/api/instructors/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  
  instructorToAdd.value = { name: "", age: "", car: "", school_name: "", picture: null };
  instructorAddPictureRef.value.value = "";
  instructorAddImageUrl.value = null;

  await Promise.all([fetchInstructors(), fetchInstructorsStats()]);
}

async function onRemoveClick(inst) {
  await axios.delete(`/api/instructors/${inst.id}/`);
  await Promise.all([fetchInstructors(), fetchInstructorsStats()]);
}

function onInstructorEditClick(inst) {
  instructorToEdit.value = { ...inst };
  instructorEditImageUrl.value = inst.picture || null;
  if (instructorEditPictureRef.value) instructorEditPictureRef.value.value = "";
}

function onEditPictureChange() {
  if (instructorEditPictureRef.value?.files?.length) {
    instructorEditImageUrl.value = URL.createObjectURL(instructorEditPictureRef.value.files[0]);
  }
}

async function onUpdateInstructor() {
  const formData = new FormData();
  formData.append("name", instructorToEdit.value.name);
  formData.append("age", instructorToEdit.value.age);
  formData.append("car", instructorToEdit.value.car);
  formData.append("school_name", instructorToEdit.value.school_name);
  if (instructorEditPictureRef.value?.files?.length) {
    formData.append("picture", instructorEditPictureRef.value.files[0]);
  }

  await axios.put(`/api/instructors/${instructorToEdit.value.id}/`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  instructorEditImageUrl.value = null;
  if (instructorEditPictureRef.value) instructorEditPictureRef.value.value = "";

  await Promise.all([fetchInstructors(), fetchInstructorsStats()]);
}

onBeforeMount(async () => {
  await Promise.all([fetchInstructors(), fetchInstructorsStats(), fetchCars(), fetchSchools()]);
});
</script>

<template>
  <div>
    <h3>Инструкторы</h3>

    

    <div v-if="instructorsStats" class="mb-3 p-2 border rounded bg-light">
      <strong>Статистика по инструкторам:</strong>
      <div>Всего: {{ instructorsStats.count }}</div>
      <div>Средний возраст: {{ instructorsStats.avg }}</div>
      <div>Минимальный возраст: {{ instructorsStats.min }}</div>
      <div>Максимальный возраст: {{ instructorsStats.max }}</div>
    </div>


    <form v-if="userInfo?.is_superuser" @submit.prevent.stop="onInstructorAdd" class="mb-3">
      <div class="row g-2">
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
              <option value="">Выберите машину</option>
              <option v-for="c in cars" :key="c.id" :value="c.id">{{ c.car_number }} ({{ c.model }})</option>
            </select>
            <label>Машина</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <select class="form-select" v-model="instructorToAdd.school_name" required>
              <option value="">Выберите школу</option>
              <option v-for="s in schools" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
            <label>Школа</label>
          </div>
        </div>
        <div class="col-auto">
          <input type="file" class="form-control" ref="instructorAddPictureRef" @change="onAddPictureChange" accept="image/*" required />
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
      
      <div v-if="instructorAddImageUrl" class="mt-2">
        <img :src="instructorAddImageUrl" style="max-height: 120px; border-radius: 5px; object-fit: cover;" />
      </div>
    </form>

    
    <div class="mb-3 row g-2">
      <div class="col">
        <input type="text" class="form-control" placeholder="Фильтр по имени" v-model="filterName" />
      </div>
      <div class="col">
        <input type="text" class="form-control" placeholder="Фильтр по возрасту" v-model="filterAge" />
      </div>
      <div class="col">
        <input type="text" class="form-control" placeholder="Фильтр по машине" v-model="filterCar" />
      </div>
      <div class="col">
        <input type="text" class="form-control" placeholder="Фильтр по школе" v-model="filterSchool" />
      </div>
    </div>

    <div v-for="inst in filteredInstructors" :key="inst.id" class="border rounded p-2 d-flex align-items-center justify-content-between mb-2">
      <div class="d-flex align-items-center">
        <img
          v-if="inst.picture"
          :src="inst.picture"
          style="width: 70px; height: 70px; object-fit: cover; border-radius: 6px; margin-right: 12px; cursor:pointer;"
          @click="previewImage = inst.picture"
        />
        <div>
          <strong>{{ inst.name }}</strong> — возраст {{ inst.age }}, школа: {{ inst.school_name_display }}, авто: {{ inst.car_display }}
        </div>
      </div>

      <div v-if="userInfo?.is_superuser" class="btn-group">
        <button class="btn btn-success btn-sm" @click="onInstructorEditClick(inst)" data-bs-toggle="modal" data-bs-target="#editInstructorModal">
          <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-danger btn-sm" @click="onRemoveClick(inst)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>

    <div v-if="filteredInstructors.length === 0" class="text-center text-muted py-4">
      <i class="bi bi-search display-4 d-block mb-2"></i>
      <p>Инструкторы не найдены</p>
    </div>

    <div v-if="previewImage" class="preview-overlay" @click.self="previewImage = null">
      <img :src="previewImage" class="preview-img" />
      <button class="close-btn" @click="previewImage = null">✕</button>
    </div>

    <div class="modal fade" id="editInstructorModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать инструктора</h1>
            <button class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <input type="text" class="form-control mb-2" placeholder="ФИО" v-model="instructorToEdit.name" />
            <input type="number" class="form-control mb-2" placeholder="Возраст" v-model="instructorToEdit.age" />
            <select class="form-select mb-2" v-model="instructorToEdit.car">
              <option value="">Выберите машину</option>
              <option v-for="c in cars" :key="c.id" :value="c.id">{{ c.car_number }} ({{ c.model }})</option>
            </select>
            <select class="form-select mb-2" v-model="instructorToEdit.school_name">
              <option value="">Выберите школу</option>
              <option v-for="s in schools" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
            <input 
              type="file" 
              class="form-control mb-2" 
              ref="instructorEditPictureRef" 
              @change="onEditPictureChange" 
              accept="image/*" 
            />
            <img 
              v-if="instructorEditImageUrl" 
              :src="instructorEditImageUrl" 
              style="max-height: 120px; border-radius: 5px; object-fit: cover;" 
              class="mt-2"
            />
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateInstructor">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

.preview-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.85); 
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; 
  backdrop-filter: blur(4px); 
}

.preview-img {
  max-width: 90%;
  max-height: 90vh;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
  object-fit: contain;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 30px;
  background: transparent;
  border: none;
  color: white;
  font-size: 3rem;
  font-weight: bold;
  cursor: pointer;
  line-height: 1;
  transition: transform 0.2s;
}

.close-btn:hover {
  transform: scale(1.1);
  color: #ddd;
}
</style>
