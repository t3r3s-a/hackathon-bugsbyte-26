<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";


import logoParceria from "../assets/logo-parceria.png"; 

const router = useRouter();
const username = ref("");
const password = ref("");

const handleLogin = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/users/login", {
      username: username.value,
      password: password.value,
    });

    if (response.data.status === "success") {
      localStorage.setItem("usuario_logado", response.data.username);
      if (response.data.questionnaire === null) {
        router.push("/questionnaire");
      } else {
        router.push("/welcome");
      }
    }
  } catch (error) {
    console.error("Erro no login:", error);
    alert("Dados incorretos ou servidor offline.");
  }
};
</script>

<template>
  <div class="view-wrapper">
    <div class="decor-blob blob-1"></div>
    <div class="decor-blob blob-2"></div>
    <div class="decor-blob blob-3"></div>

    <div class="login-container">
      <div class="header-section">
        <img :src="logoParceria" alt="Nutrium x Snack-e" class="brand-logo" />
        <h1 class="title">Bem-vindo!</h1>
        <p class="subtitle">Insere os teus dados para entrar na plataforma.</p>
      </div>

      <form @submit.prevent="handleLogin" class="form-content">
        <div class="field">
          <label>Utilizador</label>
          <input v-model="username" type="text" required placeholder="Ex: joao_silva" />
        </div>

        <div class="field">
          <label>Palavra-passe</label>
          <input v-model="password" type="password" required placeholder="••••••••" />
        </div>

        <button type="submit" class="btn-main">Entrar</button>
      </form>

      <div class="footer-section">
        <p>Ainda não tens conta?</p>
        <router-link to="/register" class="btn-ghost">Criar conta</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.view-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f8fafc; 
  font-family: 'Inter', sans-serif;
  padding: 20px;
  position: relative;
  overflow: hidden; 
}

/* Estilo dos Blobs Decorativos */
.decor-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 0;
  opacity: 0.5;
  animation: move 20s infinite alternate;
}

.blob-1 {
  width: 400px;
  height: 400px;
  background: #dcfce7;
  top: -100px;
  left: -100px;
}

.blob-2 {
  width: 350px;
  height: 350px;
  background: #47baac33; 
  bottom: -50px;
  right: -50px;
  animation-delay: -5s;
}

.blob-3 {
  width: 300px;
  height: 300px;
  background: #fef9c3; 
  top: 20%;
  right: 10%;
  animation-delay: -10s;
}

@keyframes move {
  from { transform: translate(0, 0) scale(1); }
  to { transform: translate(50px, 100px) scale(1.2); }
}

.login-container {
  width: 100%;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.9); 
  padding: 48px 40px;
  border-radius: 28px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.8);
  position: relative;
  z-index: 1; /* Garante que o card fica por cima dos blobs */
  backdrop-filter: blur(10px); /* Efeito de vidro fosco */
}


.header-section { text-align: center; margin-bottom: 32px; }
.brand-logo { height: 42px; margin-bottom: 16px; }
.title { font-size: 1.5rem; color: #1e293b; font-weight: 700; }
.subtitle { font-size: 0.9rem; color: #64748b; }
.form-content { display: flex; flex-direction: column; gap: 20px; }
.field { display: flex; flex-direction: column; gap: 8px; }
.field label { font-size: 0.8rem; font-weight: 600; color: #47baac; text-transform: uppercase; }
.field input { padding: 12px 16px; border-radius: 12px; border: 1.5px solid #e2e8f0; background: #f8fafc; }
.btn-main { background: #47baac; color: white; padding: 14px; border-radius: 12px; font-weight: 600; cursor: pointer; border: none; }
.footer-section { margin-top: 32px; text-align: center; border-top: 1px solid #f1f5f9; padding-top: 24px; }
.btn-ghost { color: #47baac; font-weight: 700; text-decoration: none; }
</style>