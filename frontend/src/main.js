import { createApp } from 'vue';
import App from './App.vue';
import Buefy from 'buefy';
import 'buefy/dist/buefy.css';
import router from './router';
import '@fortawesome/fontawesome-free/css/all.css';
import '@/scss/global.scss';
import { createPinia } from 'pinia';

const pinia = createPinia();

createApp(App).use(router).use(pinia).use(Buefy).mount('#app');
