<script setup lang="ts">
import {onMounted} from "vue";
import {useUserStore} from "@/stores/user_store";
import {storeToRefs} from "pinia";

const userStore = useUserStore();
const { userInfo } = storeToRefs(userStore);

onMounted(() => {
  userStore.fetchUserInfo();
});

async function handleLogout() {
  await userStore.logout();
  window.location.reload(); // обновляем страницу, чтобы отобразить разлогиненного пользователя
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
    <div class="container">
      <router-link class="navbar-brand" to="/">Автошкола</router-link>

      <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
        <ul class="navbar-nav">
          <li class="nav-item"><router-link class="nav-link" to="/students">Ученики</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/schools">Школы</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/courses">Группы</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/cars">Машины</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/instructors">Инструкторы</router-link></li>
        </ul>

        <ul class="navbar-nav">
          <li v-if="userInfo && userInfo.is_authenticated" class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
              {{ userInfo.username }}
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="/admin">Админка</a></li>
              <li><button class="dropdown-item text-danger" @click="handleLogout">Выйти</button></li>
            </ul>
          </li>

          <li v-else class="nav-item">
            <router-link class="nav-link" to="/login">Войти</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="container">
    <router-view></router-view>
  </div>
</template>

