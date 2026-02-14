<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const username = ref("");
const email = ref("");
const password = ref("");

const handleRegister = async () => {
  try {
    // 1. Chamada ao backend para criar o utilizador
    const response = await axios.post("http://127.0.0.1:8000/users/register", {
      username: username.value,
      email: email.value,
      password: password.value,
    });

    // 2. AUTO-LOGIN: Se o registo deu certo, guardamos logo o nome no localStorage
    // Assim ele não precisa de fazer login outra vez agora.
    localStorage.setItem("usuario_logado", username.value);

    // 3. Sucesso e redirecionamento direto para o Questionário
    alert("Bem-vindo à família Nutrium! Vamos configurar o teu perfil.");
    router.push("/questionnaire"); 
    
  } catch (error) {
    console.error("Erro no registo:", error);
    alert(
      error.response?.data?.detail || "Erro ao registar. Tenta outro nome."
    );
  }
};
</script>

<template>
  <div class="view-wrapper">
    <div class="card register-card">
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
        <p class="tagline">Começa a tua jornada saudável hoje!</p>
      </div>

      <form @submit.prevent="handleRegister" class="form-area">
        <div class="input-group">
          <label>Nome de Utilizador</label>
          <input
            v-model="username"
            type="text"
            required
            placeholder="Como te queres chamar?"
          />
        </div>

        <div class="input-group">
          <label>Email Profissional</label>
          <input
            v-model="email"
            type="email"
            required
            placeholder="exemplo@email.com"
          />
        </div>

        <div class="input-group">
          <label>Palavra-passe</label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="Mínimo 6 caracteres"
          />
        </div>

        <button type="submit" class="btn">Criar Conta Grátis</button>

        <div class="extra">
          <span>Já és membro?</span>
          <router-link to="/" class="extra-button">Fazer Login</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* Aproveitando o teu estilo excelente e polindo alguns detalhes */
.view-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f8fafd; /* Fundo ligeiramente mais limpo */
}

.card {
  position: relative;
  width: 100%;
  max-width: 440px;
  padding: 40px;
  border-radius: 32px;
  text-align: center;
  background: white;
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 40px 80px rgba(0, 0, 0, 0.08);
  animation: float 6s ease-in-out infinite;
}

.tagline {
    color: #888;
    font-size: 14px;
    margin-bottom: 25px;
}

.logo-wrapper {
  position: relative;
  width: 96px;
  height: 96px;
  margin: 0 auto 20px auto;
}
.logo-shadow {
  filter: drop-shadow(0 15px 30px rgba(39, 174, 96, 0.3));
}
.brand {
  font-weight: 800;
  font-size: 28px;
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
  filter: drop-shadow(0 0 10px rgba(255, 140, 0, 0.5));
}

.input-group {
  text-align: left;
  margin-bottom: 18px;
}
.input-group label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: #27ae60;
  margin-bottom: 8px;
  display: block;
}
.input-group input {
  width: 100%;
  padding: 15px;
  border-radius: 16px;
  border: 2px solid #f1f3f5;
  background: #f8fafc;
  transition: all 0.3s ease;
}
.input-group input:focus {
  border-color: #27ae60;
  background: white;
  outline: none;
  box-shadow: 0 0 0 4px rgba(39, 174, 96, 0.1);
}

.btn {
  width: 100%;
  padding: 18px;
  margin-top: 15px;
  border-radius: 50px;
  border: none;
  font-weight: 800;
  font-size: 15px;
  text-transform: uppercase;
  cursor: pointer;
  background: #2d3436; /* Cor escura para contraste como no questionário */
  color: white;
  transition: all 0.3s ease;
}

.btn:hover {
  background: #27ae60;
  transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(39, 174, 96, 0.3);
}

.extra {
  margin-top: 25px;
  font-size: 14px;
  color: #636e72;
}
.extra-button {
  margin-left: 8px;
  color: #27ae60;
  font-weight: 700;
  text-decoration: none;
}
.extra-button:hover {
  text-decoration: underline;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12px); }
}
</style>