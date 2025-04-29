import { createRouter, createWebHistory } from 'vue-router'
import apiList from '../views/apiList.vue'
import newPage from '../views/newPage.vue'
import query from '../views/query.vue'
import edit from '../views/edit.vue'
import detail from '../views/detail.vue'
import homeIndex from '../views/home/index.vue'
import notFound from '../views/404.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/homeIndex',
    },
    {
      path: '/newPage',
      name: 'newPage',
      component: newPage,
    },
    {
      path: '/homeIndex',
      name: 'homeIndex',
      component: homeIndex,
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
    // 404 page
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: notFound,
    },
  ],
})

export default router
