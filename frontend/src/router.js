import { createRouter, createWebHistory } from 'vue-router';

// Importação dos teus componentes (ajusta o nome do ficheiro se for preciso)
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import QuestionnaireView from '../views/QuestionnaireView.vue';
import WelcomeView from '../views/WelcomeView.vue';
import ChatView from '../views/Robo.vue';  // O teu Robo.vue
import JogoView from '../views/Jogo.vue';  // O teu Jogo.vue

const routes = [
  { path: '/', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/questionnaire', name: 'questionnaire', component: QuestionnaireView },
  { path: '/welcome', name: 'welcome', component: WelcomeView },
  { path: '/chat', name: 'chat', component: ChatView },
  { path: '/jogo', name: 'jogo', component: JogoView },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;