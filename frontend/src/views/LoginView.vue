<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const username = ref("");
const password = ref("");

const handleLogin = async () => {
  try {
    // 1. Envia os dados para o teu Backend (FastAPI)
    const response = await axios.post("http://127.0.0.1:8000/users/login", {
      username: username.value,
      password: password.value,
    });

    // 2. Se o login for um sucesso:
    if (response.data.status === "success") {
      // Guardamos o nome no browser para usar no Amigo Presente
      localStorage.setItem("usuario_logado", response.data.username);

      // 3. Lógica de redirecionamento corrigida
      if (response.data.questionnaire === null) {
        console.log("Novo utilizador, a ir para o questionário...");
        router.push("/questionnaire");
      } else {
        console.log(
          "Utilizador antigo, a ir para a seleção de funcionalidades..."
        );
        // AQUI ESTÁ A CORREÇÃO: Enviamos para /welcome em vez de /dashboard
        router.push("/welcome");
      }
    }
  } catch (error) {
    // 4. Se o utilizador não existir ou houver erro de ligação
    console.error("Erro no login:", error);
    alert(
      "Dados incorretos ou servidor offline. Se não tens conta, clica em 'Criar conta'!"
    );
  }
};
</script>

<template>
  <div class="view-wrapper">
    <div class="card">
      <div class="logo-area">
        <div class="logo-shadow">
          <div class="logo-wrapper">
            <svg width="96" height="96" viewBox="0 0 96 96">
              <rect width="96" height="96" rx="22" fill="#27ae60" />
              <path
                d="M48 24C42 30 36 34 36 42C36 48 42 54 48 60C54 54 60 48 60 42C60 34 54 30 48 24Z"
                fill="white"
              />
            </svg>

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

      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label>Utilizador</label>
          <input
            v-model="username"
            type="text"
            required
            placeholder="Introduza o utilizador"
          />
        </div>

        <div class="input-group">
          <label>Palavra-passe</label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="••••••••"
          />
        </div>

        <button type="submit" class="btn">Entrar</button>

        <div class="extra">
          <router-link to="/register" class="extra-button"
            >Criar conta</router-link
          >
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
  background: #f0f2f5;
}

.card {
  position: relative;
  width: 100%;
  max-width: 420px;
  padding: 40px;
  border-radius: 28px;
  text-align: center;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.1);
  animation: float 6s ease-in-out infinite;
}

.logo-wrapper {
  position: relative;
  width: 96px;
  height: 96px;
  margin: 0 auto 20px auto;
}

.logo-shadow {
  filter: drop-shadow(0 10px 30px rgba(39, 174, 96, 0.4));
  margin-bottom: 15px;
}
.brand {
  font-weight: 800;
  font-size: 26px;
  color: #2d3436;
}
.snake-text {
  background: linear-gradient(90deg, #f39c12, #e67e22);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.snake-overlay {
  position: absolute;
  top: -6px;
  left: -6px;
  filter: drop-shadow(0 0 8px rgba(255, 140, 0, 0.6));
  animation: float-snake 3s ease-in-out infinite;
}

.input-group {
  text-align: left;
  margin-bottom: 20px;
}
.input-group label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 6px;
  display: block;
  color: #27ae60;
}
.input-group input {
  width: 100%;
  padding: 14px;
  border-radius: 14px;
  border: 1.5px solid #eee;
  background: #fdfdfd;
  transition: all 0.2s ease;
}
.input-group input:focus {
  border-color: #27ae60;
  outline: none;
  background: white;
  box-shadow: 0 0 0 4px rgba(39, 174, 96, 0.1);
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
  background: #2d3436;
  color: white;
  transition: all 0.3s ease;
}
.btn:hover {
  background: #27ae60;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(39, 174, 96, 0.2);
}

.extra {
  margin-top: 20px;
}
.extra-button {
  display: inline-block;
  color: #27ae60;
  font-weight: 700;
  text-decoration: none;
  font-size: 14px;
}
.extra-button:hover {
  text-decoration: underline;
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
@keyframes float-snake {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}
</style>
