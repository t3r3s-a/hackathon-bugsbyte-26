import { createRouter, createWebHistory } from 'vue-router';
import LoginView from "./views/LoginView.vue";      
import RegisterView from "./views/RegisterView.vue"; 
import QuestionnaireView from "./views/QuestionnaireView.vue"; 

const routes = [
  { path: '/', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/questionnaire', name: 'questionnaire', component: QuestionnaireView }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;