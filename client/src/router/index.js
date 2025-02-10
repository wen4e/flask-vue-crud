import { createRouter, createWebHistory } from 'vue-router'
import apiList from '../views/apiList.vue'
import newPage from '../views/newPage.vue'
import query from '../views/query.vue'
import edit from '../views/edit.vue'
import detail from '../views/detail.vue'
import login from '../views/login.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'newPage',
      component: newPage,
    },
    {
      path: '/login',
      name: 'login',
      component: login,
    },
    {
      path: '/query',
      name: 'query',
      component: query,
    },
    {
      path: '/apiList',
      name: 'apiList',
      component: apiList,
    },
  ]
})

export default router
