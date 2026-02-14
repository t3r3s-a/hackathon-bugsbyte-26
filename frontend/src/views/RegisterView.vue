<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

// Import da logo de parceria
import logoParceria from "../assets/logo-parceria.png"; 

const router = useRouter();
const username = ref("");
const email = ref("");
const password = ref("");

const handleRegister = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/users/register", {
      username: username.value,
      email: email.value,
      password: password.value,
    });

    localStorage.setItem("usuario_logado", username.value);
    router.push("/questionnaire"); 
    
  } catch (error) {
    console.error("Erro no registo:", error);
  }
};
</script>

<template>
  <div class="view-wrapper">
    <div class="decor-blob blob-1"></div>
    <div class="decor-blob blob-2"></div>
    <div class="decor-blob blob-3"></div>

    <div class="register-container">
      <div class="header-section">
        <img :src="logoParceria" alt="Nutrium x Snack-e" class="brand-logo" />
        <h1 class="title">Criar Conta</h1>
        <p class="subtitle">Junta-te a nós nesta aventura saudável!</p>
      </div>

      <form @submit.prevent="handleRegister" class="form-content">
        <div class="field">
          <label>Nome de Utilizador</label>
          <input
            v-model="username"
            type="text"
            required
            placeholder="Como te queres chamar?"
          />
        </div>

        <div class="field">
          <label>Email</label>
          <input
            v-model="email"
            type="email"
            required
            placeholder="exemplo@email.com"
          />
        </div>

        <div class="field">
          <label>Palavra-passe</label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="Mínimo 6 caracteres"
          />
        </div>

        <button type="submit" class="btn-main">Começar Agora</button>
      </form>

      <div class="footer-section">
        <p>Já és membro?</p>
        <router-link to="/login" class="btn-ghost">Fazer Login</router-link>
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

/* Blobs Animados */
.decor-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 0;
  opacity: 0.5;
  animation: move 20s infinite alternate;
}

.blob-1 { width: 450px; height: 450px; background: #dcfce7; top: -150px; left: -100px; }
.blob-2 { width: 350px; height: 350px; background: #47baac33; bottom: -50px; right: -50px; animation-delay: -5s; }
.blob-3 { width: 300px; height: 300px; background: #fef9c3; top: 10%; right: 10%; animation-delay: -10s; }

@keyframes move {
  from { transform: translate(0, 0) scale(1); }
  to { transform: translate(60px, 80px) scale(1.1); }
}

/* Card Register */
.register-container {
  width: 100%;
  max-width: 420px;
  background: rgba(255, 255, 255, 0.9);
  padding: 40px;
  border-radius: 28px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.8);
  position: relative;
  z-index: 1;
  backdrop-filter: blur(12px);
}

.header-section { text-align: center; margin-bottom: 30px; }
.brand-logo { height: 42px; margin-bottom: 16px; }
.title { font-size: 1.6rem; color: #1e293b; font-weight: 700; }
.subtitle { font-size: 0.9rem; color: #64748b; }

.form-content { display: flex; flex-direction: column; gap: 18px; }
.field { display: flex; flex-direction: column; gap: 6px; text-align: left; }
.field label { font-size: 0.75rem; font-weight: 700; color: #47baac; text-transform: uppercase; letter-spacing: 0.05em; }

.field input {
  padding: 14px;
  border-radius: 12px;
  border: 1.5px solid #e2e8f0;
  background: #f8fafc;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.field input:focus {
  outline: none;
  border-color: #47baac;
  background: white;
  box-shadow: 0 0 0 4px rgba(71, 186, 172, 0.1);
}

.btn-main {
  background: #47baac;
  color: white;
  padding: 16px;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 10px;
}

.btn-main:hover {
  background: #3a968a;
  transform: translateY(-2px);
  box-shadow: 0 8px 15px rgba(71, 186, 172, 0.2);
}

.footer-section {
  margin-top: 25px;
  text-align: center;
  border-top: 1px solid #f1f5f9;
  padding-top: 20px;
}

.footer-section p { font-size: 0.85rem; color: #64748b; margin-bottom: 5px; }
.btn-ghost { color: #47baac; font-weight: 700; text-decoration: none; font-size: 0.9rem; }
.btn-ghost:hover { text-decoration: underline; }
</style>