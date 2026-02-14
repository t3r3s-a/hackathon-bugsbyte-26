<script setup>
import { ref } from "vue";

const username = ref("");
const email = ref("");
const password = ref("");

const handleRegister = () => {
  console.log("A tentar registo com:", {
    user: username.value,
    email: email.value,
    pass: password.value,
  });
};
</script>

<template>
  <div class="view-wrapper">
    <div class="card">
      <!-- Logo -->
      <div class="logo-area">
        <div class="logo-shadow">
          <div class="logo-wrapper">
            <svg width="96" height="96" viewBox="0 0 96 96">
              <rect width="96" height="96" rx="22" fill="#27ae60" />
              <path d="M48 24C42 30 36 34 36 42C36 48 42 54 48 60C54 54 60 48 60 42C60 34 54 30 48 24Z" fill="white"/>
            </svg>

            <svg class="snake-overlay" width="100" height="100" viewBox="0 0 72 72">
              <defs>
                <linearGradient id="snakeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#f39c12" />
                  <stop offset="100%" stop-color="#e67e22" />
                </linearGradient>
              </defs>
              <path d="M16 44C20 38 26 42 30 36C34 30 32 24 36 20C40 16 44 22 42 28C40 34 44 36 48 32"
                stroke="url(#snakeGrad)" stroke-width="4" stroke-linecap="round" fill="none"/>
            </svg>
          </div>
        </div>
        <h1 class="brand">Nutrium <span class="snake-text">Snack-e</span></h1>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleRegister">
        <div class="input-group">
          <label>Utilizador</label>
          <input v-model="username" type="text" placeholder="Novo utilizador"/>
        </div>

        <div class="input-group">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="Introduza o email"/>
        </div>

        <div class="input-group">
          <label>Palavra-passe</label>
          <input v-model="password" type="password" placeholder="Nova palavra-passe"/>
        </div>

        <button type="submit" class="btn">Registar</button>

        <div class="extra">
          <router-link to="/" class="extra-button">Já tenho conta</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.view-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.card {
  position: relative;
  width: 100%;
  max-width: 420px;
  padding: 40px;
  border-radius: 28px;
  text-align: center;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 30px 60px rgba(0,0,0,0.1), inset 0 0 0 1px rgba(255,255,255,0.3);
  animation: float 6s ease-in-out infinite;
}

.logo-wrapper {
  position: relative;
  width: 96px;
  height: 96px;
  margin: 0 auto 20px auto;
}
.logo-shadow { filter: drop-shadow(0 10px 30px rgba(39,174,96,0.4)); margin-bottom: 15px; }
.brand { font-weight: 800; font-size: 26px; }
.snake-text { background: linear-gradient(90deg, #f39c12, #e67e22); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

.snake-overlay { position: absolute; top: -6px; left: -6px; filter: drop-shadow(0 0 8px rgba(255,140,0,0.6)); animation: float-snake 3s ease-in-out infinite; }

.input-group { text-align: left; margin-bottom: 20px; }
.input-group label { font-size: 12px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px; display: block; }
.input-group input { width: 100%; padding: 14px; border-radius: 14px; border: 1px solid #e0e0e0; background: rgba(255,255,255,0.6); transition: all 0.2s ease; }
.input-group input:focus { border-color:#27ae60; outline:none; box-shadow:0 0 0 4px rgba(39,174,96,0.15); }

.btn { width:100%; padding:16px; margin-top:10px; border-radius:50px; border:none; font-weight:700; text-transform:uppercase; cursor:pointer; background:linear-gradient(90deg,#27ae60,#1f9d55); color:white; box-shadow:0 10px 30px rgba(39,174,96,0.3); transition: all 0.3s ease; }
.btn:hover { transform: translateY(-3px); box-shadow: 0 15px 40px rgba(39,174,96,0.4); }

.extra { margin-top: 20px; }
.extra-button { display: inline-block; background: none; border: none; color: #27ae60; font-weight: 600; cursor:pointer; text-decoration:none; }
.extra-button:hover { text-decoration: underline; }

@keyframes float { 0%,100%{ transform:translateY(0); } 50%{ transform:translateY(-10px); } }
@keyframes float-snake { 0%,100%{ transform:translateY(0); } 50%{ transform:translateY(-4px); } }
</style>
 