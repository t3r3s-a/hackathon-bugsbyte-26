import { createRouter, createWebHistory } from 'vue-router';
import MainView from "./views/MainView.vue";
import LoginView from "./views/LoginView.vue";      
import RegisterView from "./views/RegisterView.vue"; 
import QuestionnaireView from "./views/QuestionnaireView.vue";
import WelcomeView from "./views/WelcomeView.vue";
import ChatView from "./views/ChatView.vue";
import GameView from "./views/GameView.vue";
import PlanoIAView from "./views/Questionario.vue";

const routes = [
  { path: '/', name: 'main', component: MainView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/questionnaire', name: 'questionnaire', component: QuestionnaireView },
  { path: '/welcome', name: 'welcome', component: WelcomeView },
  { path: '/chat', name: 'chat', component: ChatView },
  { path: '/games', name: 'games', component: GameView },
  { path: '/plano', name: 'plano', component: PlanoIAView }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;