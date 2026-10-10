<script setup lang="ts">
import { ref } from "vue";
import { storeToRefs } from "pinia";
import axios from "axios";
import { useUserStore } from "@/stores/user_store";
import router from "./router";

const userStore = useUserStore();
const password = ref("");

const { username, is_authenticated, is_superuser, is_staff } = storeToRefs(userStore);

async function onLogout() {
  try {
    await axios.post("/api/users/logout/");
    await userStore.fetchUserInfo();
    
    router.push("/login");
  } catch (err) {
    console.error("Ошибка при выходе:", err);
  }
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
    <div class="container">
      <router-link class="navbar-brand" to="/">Автошкола2</router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
        <ul class="navbar-nav">
          <li class="nav-item"><router-link class="nav-link" to="/students">Ученики</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/schools">Школы</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/courses">Группы</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/cars">Машины</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/instructors">Инструкторы</router-link></li>
        </ul>
        <ul class="navbar-nav" v-if="is_authenticated !== null"></ul>

        <ul class="navbar-nav" v-if="is_authenticated">
          <li class="nav-item">
            <router-link class="nav-link" to="/second-auth">2FA</router-link>
          </li>
          <li class="nav-item dropdown" >
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              {{ username || 'Пользователь' }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li v-if="is_staff">
                <a class="dropdown-item" href="/admin" target="_blank">Админка</a>
              </li>
              
              <li v-if="is_staff">
                <hr class="dropdown-divider">
              </li>
              
              <li>
                <button class="dropdown-item" @click="onLogout">Выйти</button>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="container">
    <router-view></router-view>
  </div>
</template>
