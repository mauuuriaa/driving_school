import {defineStore} from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
  state: () => ({
    userInfo: null as any,
  }),

  actions: {
    async fetchUserInfo() {
      const response = await axios.get("/api/users/info/");
      this.userInfo = response.data;
    },

    async login(username: string, password: string) {
      const response = await axios.post("/api/users/login/", {username, password});
      if (response.data.success) {
        await this.fetchUserInfo();
      } else {
        alert("Неверное имя пользователя или пароль");
      }
    },

    async logout() {
      await axios.post("/api/users/logout/");
      this.userInfo = {is_authenticated: false};
    },
  },
});
