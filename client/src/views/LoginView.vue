<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user_store";
import axios from "axios";

const router = useRouter();
const userStore = useUserStore();


const username = ref();
const password = ref();

async function onLoginFormSubmit() {
  try {
    const r = await axios.post("/api/users/login/", {
      username: username.value,
      password: password.value,
    })

    username.value = '';
    password.value = '';

    await userStore.fetchUserInfo();

    router.push("/students");
  } catch (err) {
    console.error("Ошибка при логине:", err);
    alert("Неверный логин или пароль");
  }
}
</script>

<template>
  <form
    
    @submit.prevent.stop="onLoginFormSubmit"
    class="form d-flex flex-column p-3"
    style="gap: 8px"
  >
    <input
      placeholder="логин"
      class="form-control"
      type="text"
      v-model="username"
    />
    <input
      placeholder="пароль"
      class="form-control"
      type="password"
      v-model="password"
    />
    <button class="btn btn-info">Войти</button>
  </form>
</template>
