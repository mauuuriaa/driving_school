
import { createRouter, createWebHistory } from 'vue-router'

import StudentsView from '../views/StudentsView.vue'
import SchoolsView from '../views/SchoolsView.vue'
import CoursesView from '../views/CoursesView.vue'
import CarsView from '../views/CarsView.vue'
import InstructorsView from '../views/InstructorsView.vue'
import LoginView from '../views/LoginView.vue'
import SecondAuthView from '../views/SecondAuthView.vue'
import { useUserStore } from "@/stores/user_store"; 

const routes = [
  { path: '/', redirect: '/students' },
  { 
    path: '/students', 
    name: 'Students', 
    component: StudentsView 
  },
  { 
    path: '/schools', 
    name: 'Schools', 
    component: SchoolsView 
  },
  { 
    path: '/courses', 
    name: 'Courses', 
    component: CoursesView 
  },
  { 
    path: '/cars', 
    name: 'Cars', 
    component: CarsView 
  },
  { 
    path: '/instructors', 
    name: 'Instructors', 
    component: InstructorsView 
  },
  { 
    path: '/login', 
    name: 'Login', 
    component: LoginView 
  },
  { 
    path: '/second-auth',   
    name: 'SecondAuth', 
    component: SecondAuthView 
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from) =>{
  const userUserStore = useUserStore();
  if (userUserStore.is_authenticated == false && to.name != 'Login')
    return { name: 'Login'}
})

export default router