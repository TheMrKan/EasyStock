import { createRouter, createWebHistory } from 'vue-router';
import LayoutDefault from './components/LayoutDefault.vue';
import ComponentsView from './views/ComponentsView.vue';
import AboutView from './views/AboutView.vue';
import HomeView from './views/HomeView.vue';

const routes = [
  {
    path: '/',
    component: LayoutDefault,
    children: [
      {
        path: '',
        name: 'home',
        component: HomeView,
      },
      {
        path: '/components',
        name: 'component',
        component: ComponentsView,
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
