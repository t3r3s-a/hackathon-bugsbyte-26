import { createRouter, createWebHistory } from "vue-router";
import LoginView from "./views/loginView.vue";        // maiúscula L
import RegisterView from "./views/registerView.vue";  // minúscula r

const routes = [
  { path: "/", component: LoginView },
  { path: "/register", component: RegisterView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
