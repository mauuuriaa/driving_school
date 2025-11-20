import {defineStore} from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
  state: () => ({
    userInfo: null as any,
    token: localStorage.getItem("token") || null, // Считываем токен при запуске
  }),

  actions: {
    async fetchUserInfo() {
      // Если токена нет, нет смысла делать запрос
      if (!this.token) return;

      // Устанавливаем заголовок авторизации
      axios.defaults.headers.common['Authorization'] = `Token ${this.token}`;

      try {
        
      
        const response = await axios.get("/api/users/me/"); 
        this.userInfo = response.data;
      } catch (error) {
        console.error("Ошибка получения данных юзера", error);
        this.logout(); 
      }
    },

    async login(username: string, password: string) {
      try {
        const response = await axios.post("/api/users/login/", {username, password});
        
       
        if (response.data.token) {
          this.token = response.data.token;
          
          
          localStorage.setItem("token", this.token);
          
          
          axios.defaults.headers.common['Authorization'] = `Token ${this.token}`;
          
          await this.fetchUserInfo();
        } else {
            alert("Ошибка: Сервер не вернул токен");
        }
      } catch (error) {
        console.error(error);
        alert("Неверное имя пользователя или пароль");
      }
    },

    async logout() {
      try {
          // Пытаемся сказать бэкенду, что мы вышли (необязательно, но желательно)
          if (this.token) {
             axios.defaults.headers.common['Authorization'] = `Token ${this.token}`;
             await axios.post("/api/users/logout/");
          }
      } catch (e) {
          // Игнорируем ошибки при выходе
      } finally {
          // В любом случае чистим данные на клиенте
          this.userInfo = null;
          this.token = null;
          localStorage.removeItem("token");
          delete axios.defaults.headers.common['Authorization'];
      }
    },
  },
});