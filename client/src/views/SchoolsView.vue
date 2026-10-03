<script setup>
import { ref, computed, onBeforeMount } from "vue";
import axios from "axios";
import { useUserStore } from "@/stores/user_store";
import { storeToRefs } from "pinia";

const userStore = useUserStore();
const { userInfo } = storeToRefs(userStore);


const schools = ref([]);
const schoolsStats = ref(null);
const schoolToAdd = ref({ name: "" });
const schoolToEdit = ref({});


const filterName = ref("");

const filteredSchools = computed(() => {
  return schools.value.filter(school => 
    !filterName.value || school.name.toLowerCase().includes(filterName.value.toLowerCase())
  );
});


async function fetchSchools() {
  const r = await axios.get("/api/schools/");
  schools.value = r.data;
}

async function fetchSchoolsStats() {
  const r = await axios.get("/api/schools/stats/");
  schoolsStats.value = r.data;
}

async function onSchoolAdd() {
  await axios.post("/api/schools/", schoolToAdd.value);
  schoolToAdd.value = { name: "" };
  await Promise.all([fetchSchools(), fetchSchoolsStats()]);
}

async function onRemoveClick(school) {
  await axios.delete(`/api/schools/${school.id}/`);
  await Promise.all([fetchSchools(), fetchSchoolsStats()]);
}

function onSchoolEditClick(school) {
  schoolToEdit.value = { ...school };
}

async function onUpdateSchool() {
  await axios.put(`/api/schools/${schoolToEdit.value.id}/`, schoolToEdit.value);
  await Promise.all([fetchSchools(), fetchSchoolsStats()]);


  const modalEl = document.getElementById('editSchoolModal');
  const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
  modal.hide();
}

onBeforeMount(async () => {
  await Promise.all([fetchSchools(), fetchSchoolsStats()]);
});
</script>

<template>
  <div>
    <h3>Автошколы</h3>

    <div v-if="schoolsStats" class="mb-3 p-2 border rounded bg-light">
      <strong>Статистика по школам:</strong>
      <div>Всего школ: {{ schoolsStats.count }}</div>

    </div>


    <form v-if="userInfo?.is_superuser" @submit.prevent="onSchoolAdd" class="mb-3 row g-2 align-items-center">
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="schoolToAdd.name" required />
          <label>Название школы</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </form>

    <div class="mb-3">
      <input type="text" class="form-control" placeholder="Фильтр по названию" v-model="filterName" />
    </div>


    <div v-for="school in filteredSchools" :key="school.id" class="school-item d-flex align-items-center justify-content-between border p-2 rounded mb-2">
      <div>{{ school.name }}</div>

      <div v-if="userInfo?.is_superuser" class="btn-group">
        <button class="btn btn-success btn-sm" @click="onSchoolEditClick(school)" data-bs-toggle="modal" data-bs-target="#editSchoolModal">
          <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-danger btn-sm" @click="onRemoveClick(school)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>

    <div v-if="filteredSchools.length === 0" class="text-center text-muted py-4">
      <i class="bi bi-search display-4 d-block mb-2"></i>
      <p>Школы не найдены</p>
    </div>

    <div  class="modal fade" id="editSchoolModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать школу</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating mb-3">
              <input type="text" class="form-control" v-model="schoolToEdit.name" />
              <label>Название школы</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" @click="onUpdateSchool">Сохранить</button>
          </div>
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
