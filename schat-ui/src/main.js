import { createApp } from 'vue'
import App from './App.vue'
import Home from './components/Home.vue'
import Chat from './components/Chat.vue'
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    { path: '/', component: Home },
    { path: '/chat', component: Chat }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

const app = createApp(App);

app.use(router);

app.mount('#app');
