import { createRouter, createWebHistory } from 'vue-router'

// Импорт всех вью-компонентов
import StudentsView from '../views/StudentsView.vue'
import SchoolsView from '../views/SchoolsView.vue'
import CoursesView from '../views/CoursesView.vue'
import CarsView from '../views/CarsView.vue'
import InstructorsView from '../views/InstructorsView.vue'

// Список маршрутов
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes:[
    { path: '/', redirect: '/students' },
  { path: '/students', 
    name: 'Students', 
    component: StudentsView 
  },
  { path: '/schools', 
    name: 'Schools', 
    component: SchoolsView 
  },
  { path: '/courses', 
    name: 'Courses', 
    component: CoursesView 
  },
  { path: '/cars', 
    name: 'Cars', 
    component: CarsView 
  },
  { path: '/instructors', 
    name: 'Instructors', 
    component: InstructorsView 
  }
  ]
}) 

export default router
