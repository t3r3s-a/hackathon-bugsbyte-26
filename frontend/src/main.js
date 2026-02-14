import { createApp } from 'vue'; // Não te esqueças de importar o createApp!
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';

// Corrigido: Usamos ./ para indicar que a pasta views está ao lado do main.js
import LoginView from './views/LoginView.vue';
import RegisterView from './views/RegisterView.vue';
import QuestionnaireView from './views/QuestionnaireView.vue';
import WelcomeView from './views/WelcomeView.vue';
import ChatView from './views/ChatView.vue';

const routes = [
  { path: '/', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/questionnaire', component: QuestionnaireView },
  { path: '/welcome', component: WelcomeView },
  { path: '/chat', component: ChatView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);
app.use(router);
app.mount('#app');