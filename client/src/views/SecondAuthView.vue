<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';
import { useUserStore } from "@/stores/user_store";
import QRCode from 'qrcode'; 

const key = ref('');
const userStore = useUserStore();
const totpUrl = ref('');
const qrcodeUrl = ref('');
const statusMsg = ref('');


watch(totpUrl, async () => {
    if (totpUrl.value) {
        qrcodeUrl.value = await QRCode.toDataURL(totpUrl.value);
    }
})


async function getTotpKey() {
    let r = await axios.get('/api/users/get-totp/');
    totpUrl.value = r.data.url;
   
}


async function onActivate() {
    try {
        await axios.post("/api/users/second-login/", {
            key: key.value
        });
        statusMsg.value = "Успешно!";
        await userStore.fetchUserInfo();
    } catch (err) {
        statusMsg.value = "Неверный код";
    }
}
</script>

<template>
    <div class="container mt-4">
        <h2>Двухфакторная аутентификация</h2>
        
        <div class="card p-4 mb-4">
            <h4>1. Настройка</h4>
            <button class="btn btn-secondary mb-3" @click="getTotpKey">Показать QR-код</button>
            <div v-if="qrcodeUrl">
                <p>Отсканируйте этот код :</p>
                <img :src="qrcodeUrl" alt="QR Code" style="border: 1px solid #ccc; padding: 10px;">
                <p class="small text-muted">{{ totpUrl }}</p>
            </div>
        </div>

        <div class="card p-4">
            <h4>2. Вход</h4>
            <div class="mb-3">
                <label>Введите код из приложения:</label>
                <input type="text" class="form-control" v-model="key" placeholder="000000">
            </div>
            <button class="btn btn-success" @click="onActivate">Подтвердить код</button>
            
            <p v-if="statusMsg" class="mt-2 fw-bold" :class="{'text-success': statusMsg === 'Успешно!', 'text-danger': statusMsg !== 'Успешно!'}">
                {{ statusMsg }}
            </p>
            
            <div v-if="userStore.is_second_factor_active" class="alert alert-success mt-3">
                Второй фактор активен для текущей сессии!
            </div>
        </div>
    </div>
</template>