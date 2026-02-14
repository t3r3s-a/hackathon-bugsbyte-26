import { createApp } from 'vue'; 
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';

import MainView from './views/MainView.vue';
import LoginView from './views/LoginView.vue';
import RegisterView from './views/RegisterView.vue';
import QuestionnaireView from './views/QuestionnaireView.vue';
import WelcomeView from './views/WelcomeView.vue';
import ChatView from './views/ChatView.vue';
import SnackView from './views/SnackView.vue';

const routes = [
  { path: '/', component: MainView },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/questionnaire', component: QuestionnaireView },
  { path: '/welcome', component: WelcomeView },
  { path: '/chat', component: ChatView },
  {path: '/snake-game', component: SnackView}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);
app.use(router);
app.mount('#app');