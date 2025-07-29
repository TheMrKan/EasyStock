import { createRouter, createWebHistory } from 'vue-router';
import LayoutDefault from './components/LayoutDefault.vue';
import HomeView from './views/HomeView.vue';
import AboutView from './views/AboutView.vue';

const routes = [
  {
    path: '/',
    component: LayoutDefault, // Все маршруты будут использовать этот макет
    children: [
      {
        path: '',
        name: 'home',
        component: HomeView
      },
      {
        path: '/about',
        name: 'about',
        component: AboutView
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
