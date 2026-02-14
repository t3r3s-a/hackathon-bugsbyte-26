<script setup>
import { ref } from "vue";

const username = ref("");
const password = ref("");

const handleLogin = () => {
  console.log("A tentar login com:", {
    user: username.value,
    pass: password.value,
  });
};
</script>

<template>
  <div class="wrapper">
    <!-- Ambient glow -->
    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>

    <div class="card">
      <!-- Logo -->
      <div class="logo-area">
        <div class="logo-shadow">
          <div class="logo-wrapper">
            <!-- Ícone base Nutrium -->
            <svg width="96" height="96" viewBox="0 0 96 96">
              <rect width="96" height="96" rx="22" fill="#27ae60" />
              <path
                d="M48 24C42 30 36 34 36 42C36 48 42 54 48 60C54 54 60 48 60 42C60 34 54 30 48 24Z"
                fill="white"
              />
            </svg>

            <!-- Cobra por cima -->
            <svg
              class="snake-overlay"
              width="100"
              height="100"
              viewBox="0 0 72 72"
            >
              <defs>
                <linearGradient
                  id="snakeGrad"
                  x1="0%"
                  y1="0%"
                  x2="100%"
                  y2="100%"
                >
                  <stop offset="0%" stop-color="#f39c12" />
                  <stop offset="100%" stop-color="#e67e22" />
                </linearGradient>
              </defs>

              <path
                d="M16 44C20 38 26 42 30 36C34 30 32 24 36 20C40 16 44 22 42 28C40 34 44 36 48 32"
                stroke="url(#snakeGrad)"
                stroke-width="4"
                stroke-linecap="round"
                fill="none"
              />
            </svg>
          </div>
        </div>

        <h1 class="brand">Nutrium <span class="snake-text">Snack-e</span></h1>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label>Utilizador</label>
          <input
            v-model="username"
            type="text"
            placeholder="Introduza o utilizador"
          />
        </div>

        <div class="input-group">
          <label>Palavra-passe</label>
          <input v-model="password" type="password" placeholder="••••••••" />
        </div>

        <button type="submit" class="btn">Entrar</button>

        <div class="extra">
          <button type="button">Criar conta</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap");

.wrapper {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-family: "Inter", sans-serif;

  background: linear-gradient(135deg, #fdfaf4 0%, #eef7ff 40%, #e3f2ff 100%);
}

/* Glow */
.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.4;
  animation: pulse 5s ease-in-out infinite;
}

.glow-1 {
  width: 300px;
  height: 300px;
  background: #27ae60;
  top: 10%;
  left: 15%;
}

.glow-2 {
  width: 350px;
  height: 350px;
  background: #3498db;
  bottom: 10%;
  right: 10%;
  animation-delay: 1s;
}

/* Card */
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

  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.1),
    inset 0 0 0 1px rgba(255, 255, 255, 0.3);

  animation: float 6s ease-in-out infinite;
}

/* Logo */
.logo-area {
  margin-bottom: 30px;
}

.logo-shadow {
  filter: drop-shadow(0 10px 30px rgba(39, 174, 96, 0.4));
  margin-bottom: 15px;
}

.brand {
  font-weight: 800;
  font-size: 26px;
}

.snake-text {
  background: linear-gradient(90deg, #f39c12, #e67e22);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Form */
.input-group {
  text-align: left;
  margin-bottom: 20px;
}

.input-group label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 6px;
  display: block;
}

.input-group input {
  width: 100%;
  padding: 14px;
  border-radius: 14px;
  border: 1px solid #e0e0e0;
  background: rgba(255, 255, 255, 0.6);
  transition: all 0.2s ease;
}

.input-group input:focus {
  border-color: #27ae60;
  outline: none;
  box-shadow: 0 0 0 4px rgba(39, 174, 96, 0.15);
}

.btn {
  width: 100%;
  padding: 16px;
  margin-top: 10px;
  border-radius: 50px;
  border: none;
  font-weight: 700;
  text-transform: uppercase;
  cursor: pointer;

  background: linear-gradient(90deg, #27ae60, #1f9d55);
  color: white;

  box-shadow: 0 10px 30px rgba(39, 174, 96, 0.3);
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(39, 174, 96, 0.4);
}

.extra {
  margin-top: 20px;
}

.extra button {
  background: none;
  border: none;
  color: #27ae60;
  font-weight: 600;
  cursor: pointer;
}

.extra button:hover {
  text-decoration: underline;
}

/* Animations */
@keyframes pulse {
  0%,
  100% {
    opacity: 0.4;
  }
  50% {
    opacity: 0.7;
  }
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
.logo-wrapper {
  position: relative;
  width: 96px;
  height: 96px;
  margin: 0 auto 20px auto;
}

.snake-overlay {
  position: absolute;
  top: -6px;
  left: -6px;
  filter: drop-shadow(0 0 8px rgba(255,140,0,0.6));
  animation: float-snake 3s ease-in-out infinite;
}

@keyframes float-snake {
  0%,100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

</style>
