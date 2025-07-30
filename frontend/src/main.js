import { createApp } from 'vue';
import App from './App.vue';
import Buefy from 'buefy';
import 'buefy/dist/buefy.css';
import router from './router';
import '@fortawesome/fontawesome-free/css/all.css';

createApp(App).use(router).use(Buefy).mount('#app');
