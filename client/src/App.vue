<script setup>
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
    <div class="container">
      <router-link class="navbar-brand" to="/">Автошкола</router-link>

      <!-- Основное меню -->
      <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/students">Ученики</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/schools">Школы</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/courses">Группы</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/cars">Машины</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/instructors">Инструкторы</router-link>
          </li>
        </ul>

        <!-- Меню пользователя -->
        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Пользователь
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="/admin">Админка</a></li>
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

<style scoped>
.navbar-nav .dropdown-menu {
  right: 0;
  left: auto;
}
</style>
