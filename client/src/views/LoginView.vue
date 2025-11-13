<script setup lang="ts">
import {ref} from "vue";
import {useRouter} from "vue-router";
import {useUserStore} from "@/stores/user_store";

const username = ref("");
const password = ref("");
const router = useRouter();
const userStore = useUserStore();

async function onFormSend() {
  await userStore.login(username.value, password.value);
  if (userStore.userInfo?.is_authenticated) {
    router.push("/");
  }
}
</script>

<template>
  <div class="d-flex justify-content-center mt-5">
    <form @submit.prevent="onFormSend" style="max-width: 300px; width: 100%;">
      <input v-model="username" class="form-control mb-2" placeholder="Имя пользователя" required />
      <input v-model="password" class="form-control mb-3" type="password" placeholder="Пароль" required />
      <button class="btn btn-primary w-100">Войти</button>
    </form>
  </div>
</template>
