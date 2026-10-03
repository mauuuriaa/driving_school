<script setup>
import { ref, computed, onBeforeMount } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import { useUserStore } from "@/stores/user_store";
import { storeToRefs } from "pinia";

const userStore = useUserStore();
const { userInfo } = storeToRefs(userStore);


const courses = ref([]);
const coursesStats = ref(null);
const courseToAdd = ref({ name: "" });
const courseToEdit = ref({});


const filterName = ref("");

const filteredCourses = computed(() => {
  return courses.value.filter(course =>
    !filterName.value || course.name.toLowerCase().includes(filterName.value.toLowerCase())
  );
});


async function fetchCourses() {
  const r = await axios.get("/api/courses/");
  courses.value = r.data;
}

async function fetchCoursesStats() {
  const r = await axios.get("/api/courses/stats/");
  coursesStats.value = r.data;
}

async function onCourseAdd() {
  const formData = new FormData();
  formData.append("name", courseToAdd.value.name);

  await axios.post("/api/courses/", formData);
  courseToAdd.value = { name: "" };
  await Promise.all([fetchCourses(), fetchCoursesStats()]);
}

async function onRemoveClick(course) {
  await axios.delete(`/api/courses/${course.id}/`);
  await Promise.all([fetchCourses(), fetchCoursesStats()]);
}

function onCourseEditClick(course) {
  courseToEdit.value = { ...course };
}

async function onUpdateCourse() {
  const formData = new FormData();
  formData.append("name", courseToEdit.value.name);

  await axios.put(`/api/courses/${courseToEdit.value.id}/`, formData);
  await Promise.all([fetchCourses(), fetchCoursesStats()]);

  const modalEl = document.getElementById('editCourseModal');
  const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
  modal.hide();
}

onBeforeMount(async () => {
  await Promise.all([fetchCourses(), fetchCoursesStats()]);
});
</script>

<template>
  <div>
    <h3>Группы</h3>

    <div v-if="coursesStats" class="mb-3 p-2 border rounded bg-light">
      <strong>Статистика по группам:</strong>
      <div>Всего групп: {{ coursesStats.count }}</div>
    </div>


    <form v-if="userInfo?.is_superuser" @submit.prevent="onCourseAdd" class="mb-3 row g-2 align-items-center">
      <div class="col">
        <div class="form-floating">
          <input type="text" class="form-control" v-model="courseToAdd.name" required />
          <label>Название группы</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </form>

    <div class="mb-3">
      <input type="text" class="form-control" placeholder="Фильтр по названию группы" v-model="filterName" />
    </div>

    <div v-for="course in filteredCourses" :key="course.id" class="course-item d-flex align-items-center justify-content-between border p-2 rounded mb-2">
      <div>{{ course.name }}</div>

      <div v-if="userInfo?.is_superuser" class="btn-group">
        <button class="btn btn-success btn-sm" @click="onCourseEditClick(course)" data-bs-toggle="modal" data-bs-target="#editCourseModal">
          <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-danger btn-sm" @click="onRemoveClick(course)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>

    <div v-if="filteredCourses.length === 0" class="text-center text-muted py-4">
      <i class="bi bi-search display-4 d-block mb-2"></i>
      <p>Группы не найдены</p>
    </div>

    <div class="modal fade" id="editCourseModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать группу</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="courseToEdit.name" />
              <label>Название группы</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button type="button" class="btn btn-primary" @click="onUpdateCourse">Сохранить</button>
          </div>
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
