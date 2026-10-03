<script setup>
import { ref, onBeforeMount, computed } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import { useUserStore } from "@/stores/user_store";


const userStore = useUserStore();

const students = ref([]);
const schools = ref([]);
const courses = ref([]);
const studentsStats = ref(null);

const filterName = ref("");
const filterAge = ref("");
const filterSchool = ref("");
const filterCourse = ref("");

async function onExportClick() {
  
    const response = await axios.get("/api/students/export/", {
      responseType: 'blob', 
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'students.xlsx'); 
    document.body.appendChild(link);
    link.click();
    
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  
}

const normalize = (v) => (v ?? "").toString().toLowerCase();

const filteredStudents = computed(() => {
  return students.value.filter(student => {
    return (
      normalize(student.name).includes(normalize(filterName.value)) &&
      normalize(student.age).includes(normalize(filterAge.value)) &&
      normalize(student.school_name_display).includes(normalize(filterSchool.value)) &&
      normalize(student.school_course_display).includes(normalize(filterCourse.value))
    );
  });
});

const studentToAdd = ref({
  name: "",
  age: "",
  school_name: "",
  school_course: "",
  picture: null,
});

const studentAddPictureRef = ref();

const studentToEdit = ref({});
const studentEditPictureRef = ref();
const studentEditPreview = ref(null);

const previewImage = ref(null);

async function fetchStudents() {
  const r = await axios.get("/api/students/");
  students.value = r.data;
}

async function fetchStudentsStats() {
  const r = await axios.get("/api/students/stats/");
  studentsStats.value = r.data;
}

async function fetchSchools() {
  const r = await axios.get("/api/schools/");
  schools.value = r.data;
}

async function fetchCourses() {
  const r = await axios.get("/api/courses/");
  courses.value = r.data;
}

function onAddPictureChange() {
  if (studentAddPictureRef.value?.files?.length) {
    studentToAdd.value.picture = studentAddPictureRef.value.files[0];
  }
}

async function onStudentAdd() {
  if (!studentToAdd.value.picture) {
    alert("Выберите фото студента!");
    return;
  }

  const formData = new FormData();
  formData.append("name", studentToAdd.value.name);
  formData.append("age", studentToAdd.value.age);
  formData.append("school_name", studentToAdd.value.school_name);
  formData.append("school_course", studentToAdd.value.school_course);
  formData.append("picture", studentToAdd.value.picture);

  await axios.post("/api/students/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  studentToAdd.value = { name: "", age: "", school_name: "", school_course: "", picture: null };
  studentAddPictureRef.value.value = "";

  await Promise.all([fetchStudents(), fetchStudentsStats()]);
}

async function onRemoveClick(student) {
  await axios.delete(`/api/students/${student.id}/`);
  await Promise.all([fetchStudents(), fetchStudentsStats()]);
}

function onStudentEditClick(student) {
  studentToEdit.value = { ...student };
  studentEditPreview.value = student.picture || null;
  studentEditPictureRef.value.value = "";
}

function onEditPictureChange() {
  if (studentEditPictureRef.value?.files?.length) {
    studentEditPreview.value = URL.createObjectURL(studentEditPictureRef.value.files[0]);
  }
}

async function onUpdateStudent() {
  const formData = new FormData();
  formData.append("name", studentToEdit.value.name);
  formData.append("age", studentToEdit.value.age);
  formData.append("school_name", studentToEdit.value.school_name);
  formData.append("school_course", studentToEdit.value.school_course);
  if (studentEditPictureRef.value?.files?.length) {
    formData.append("picture", studentEditPictureRef.value.files[0]);
  }

  await axios.put(`/api/students/${studentToEdit.value.id}/`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  await Promise.all([fetchStudents(), fetchStudentsStats()]);
}

onBeforeMount(async () => {
  await Promise.all([
    fetchStudents(),
    fetchSchools(),
    fetchCourses(),
    fetchStudentsStats()
  ]);
});
</script>

<template>
  <div>
    <h3>Ученики</h3>
    
    <div class="mb-3 p-2 border rounded bg-light">
      <strong>Статистика по студентам:</strong>
      <div>Всего студентов: {{ studentsStats.count }}</div>
      <div>Средний возраст: {{ studentsStats.avg }}</div>
      <div>Минимальный возраст: {{ studentsStats.min }}</div>
      <div>Максимальный возраст: {{ studentsStats.max }}</div>
    </div>
    
    <form v-if="userStore.is_authenticated" @submit.prevent.stop="onStudentAdd" class="mb-3">
      <div class="row g-2">
        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="studentToAdd.name" required />
            <label>ФИО</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="number" class="form-control" v-model="studentToAdd.age" required />
            <label>Возраст</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <select class="form-select" v-model="studentToAdd.school_name" required>
              <option value="">Выберите школу</option>
              <option v-for="s in schools" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
            <label>Школа</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <select class="form-select" v-model="studentToAdd.school_course" required>
              <option value="">Выберите группу</option>
              <option v-for="c in courses" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
            <label>Группа</label>
          </div>
        </div>
        <div class="col-auto">
          <input type="file" class="form-control" ref="studentAddPictureRef" @change="onAddPictureChange" accept="image/*" />
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
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
        <input type="text" class="form-control" placeholder="Фильтр по школе" v-model="filterSchool" />
      </div>
      <div class="col">
        <input type="text" class="form-control" placeholder="Фильтр по группе" v-model="filterCourse" />
      </div>
    </div>

    <div class="mb-3" v-if="userStore.can_export_data">
        <button class="btn btn-success" @click="onExportClick">
            <i class="bi bi-file-earmark-excel"></i> Скачать таблицу в Excel
        </button>
    </div>

   
    <div v-for="item in filteredStudents" :key="item.id" class="border rounded p-2 d-flex align-items-center justify-content-between mb-2">
      <div class="d-flex align-items-center">
        <img
          v-if="item.picture"
          :src="item.picture"
          style="width: 70px; height: 70px; object-fit: cover; border-radius: 6px; margin-right: 12px; cursor: pointer;"
          @click="previewImage = item.picture"
        />
        <div>
          <strong>{{ item.name }}</strong> — возраст {{ item.age }}, школа: {{ item.school_name_display }}, группа: {{ item.school_course_display }}
        </div>
      </div>

      <div v-if="userStore.can_edit_or_delete_students" class="btn-group">
        <button class="btn btn-success btn-sm" @click="onStudentEditClick(item)" data-bs-toggle="modal" data-bs-target="#editStudentModal">
          <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-danger btn-sm" @click="onRemoveClick(item)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>

    <div v-if="filteredStudents.length === 0" class="text-center text-muted py-4">
      <i class="bi bi-search display-4 d-block mb-2"></i>
      <p>Студенты не найдены</p>
    </div>
  </div>


    <div v-if="previewImage" class="preview-overlay" @click.self="previewImage = null">
      <img :src="previewImage" class="preview-img" />
      <button class="close-btn" @click="previewImage = null">✕</button>
    </div>

    <div class="modal fade" id="editStudentModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать</h1>
            <button class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <input type="text" class="form-control mb-2" v-model="studentToEdit.name" />
            <input type="number" class="form-control mb-2" v-model="studentToEdit.age" />
            <select class="form-select mb-2" v-model="studentToEdit.school_name">
              <option v-for="s in schools" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
            <select class="form-select mb-2" v-model="studentToEdit.school_course">
              <option v-for="c in courses" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
            <input type="file" class="form-control mb-2" ref="studentEditPictureRef" @change="onEditPictureChange" accept="image/*" />
            <img v-if="studentEditPreview" :src="studentEditPreview" style="max-height: 120px; border-radius: 5px;" />
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <button class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateStudent">Сохранить</button>
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
