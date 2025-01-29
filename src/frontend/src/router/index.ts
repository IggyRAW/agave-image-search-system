import { createRouter, createWebHistory } from 'vue-router'
import SearchView from '../views/SearchView.vue'
import ManagementView from '@/views/ManagementView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'search',
      component: SearchView,
    },
    {
      path: '/manage',
      name: 'management',
      component: ManagementView,
    },
  ],
})

export default router
