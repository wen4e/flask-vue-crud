import { createRouter, createWebHistory } from 'vue-router'
import apiFileList from '@/views/apiFile/list.vue'
import apiFileDetail from '@/views/apiFile/detail.vue'
import newPage from '@/views/newPage.vue'
import query from '@/views/query.vue'
import edit from '@/views/edit.vue'
import detail from '@/views/detail.vue'
import homeIndex from '@/views/home/index.vue'
import notFound from '@/views/404.vue'
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
      path: '/apiFile',
      redirect: '/apiFile/list',
      children: [
        {
          path: 'list',
          name: 'apiFileList',
          component: apiFileList,
        },
        {
          path: 'detail',
          name: 'apiFileDetail',
          component: apiFileDetail,
        },
      ],
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
