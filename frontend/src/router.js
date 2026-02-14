import { createRouter, createWebHistory } from 'vue-router';
import LoginView from "../views/LoginView.vue";      
import RegisterView from "../views/RegisterView.vue"; 
import QuestionnaireView from "../views/QuestionnaireView.vue";
import MainView from "../views/MainView.vue"; 
import SnackView from "../views/SnackView.vue"; 
import ChatView from "../views/ChatView.vue";
import WelcomeView from './views/WelcomeView.vue';

const routes = [
  { 
    path: '/', 
    name: 'login', 
    component: LoginView 
  },
  { 
    path: '/register', 
    name: 'register', 
    component: RegisterView 
  },
  { 
    path: '/questionnaire', 
    name: 'questionnaire', 
    component: QuestionnaireView 
  },
  { 
    path: '/snake-game', 
    name: 'SnakeGame', 
    component: SnackView
  },
  { path: '/chat', 
    name: 'chat', 
    component: ChatView },
    { path: '/welcom', 
    name: 'welcome', 
    component: WelcomeView }

  
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Opcional: Proteger as rotas para que só quem fez login possa jogar
router.beforeEach((to, from, next) => {
  const usuarioLogado = localStorage.getItem("usuario_logado");
  
  if (to.name !== 'login' && to.name !== 'register' && !usuarioLogado) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router;