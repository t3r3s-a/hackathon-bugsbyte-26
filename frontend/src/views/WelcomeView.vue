<script setup>
import { useRouter } from "vue-router";
const router = useRouter();
const usuario = localStorage.getItem("usuario_logado") || "Explorador";
</script>

<template>
  <div class="view-wrapper">
    <div class="card selection-card">
      <header class="welcome-header">
        <h1 class="brand">Olá, <span class="snake-text">{{ usuario }}</span>!</h1>
        <p>O teu perfil nutricional foi analisado com sucesso.</p>
      </header>

      <div class="options-container">
        <button @click="router.push('/dashboard')" class="plan-hero-btn">
          <div class="hero-content">
            <span class="hero-icon">📋</span>
            <div class="hero-text">
              <h3>Ver o meu Plano</h3>
              <p>Consulta as tuas metas de calorias e macros</p>
            </div>
          </div>
          <span class="arrow">→</span>
        </button>

        <div class="options-grid">
          <button @click="alert('Jogo da Cobra em breve!')" class="choice-card snake-card">
            <div class="icon-circle">🐍</div>
            <h3>Snack-e Game</h3>
            <p>Diverte-te e queima calorias!</p>
            <span class="btn-label">Jogar</span>
          </button>

          <button @click="router.push('/chat')" class="choice-card ai-card">
            <div class="icon-circle">🤖</div>
            <h3>Amigo Presente</h3>
            <p>Dúvidas? Pergunta à nossa IA.</p>
            <span class="btn-label">Conversar</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.view-wrapper {
  display: flex; align-items: center; justify-content: center;
  min-height: 100vh; background: #f8fafc; padding: 20px;
}
.selection-card {
  max-width: 650px; width: 100%; background: white;
  padding: 40px; border-radius: 40px; text-align: center;
  box-shadow: 0 30px 60px rgba(0,0,0,0.06);
}
.welcome-header h1 { font-size: 30px; font-weight: 800; margin-bottom: 10px; }
.welcome-header p { color: #64748b; margin-bottom: 35px; }
.snake-text { background: linear-gradient(90deg, #f39c12, #e67e22); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

.options-container { display: flex; flex-direction: column; gap: 20px; }

/* Estilo do Botão de Destaque (Ver Plano) */
.plan-hero-btn {
  display: flex; align-items: center; justify-content: space-between;
  padding: 25px; border-radius: 24px; border: none;
  background: #2d3436; color: white; cursor: pointer;
  transition: all 0.3s ease; text-align: left;
}
.plan-hero-btn:hover {
  background: #27ae60; transform: scale(1.02);
  box-shadow: 0 15px 30px rgba(39, 174, 96, 0.2);
}
.hero-content { display: flex; align-items: center; gap: 20px; }
.hero-icon { font-size: 32px; }
.hero-text h3 { margin: 0; font-size: 18px; font-weight: 700; }
.hero-text p { margin: 5px 0 0; font-size: 13px; opacity: 0.8; }
.arrow { font-size: 24px; font-weight: bold; }

/* Grelha para os outros dois */
.options-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

.choice-card {
  padding: 25px; border-radius: 24px; border: 2px solid #f1f5f9;
  background: white; cursor: pointer; transition: all 0.3s ease;
  display: flex; flex-direction: column; align-items: center;
}
.choice-card:hover {
  transform: translateY(-5px); border-color: #27ae60;
  box-shadow: 0 15px 30px rgba(0,0,0,0.05);
}
.icon-circle {
  width: 60px; height: 60px; background: #f8fafc;
  border-radius: 50%; display: flex; align-items: center;
  justify-content: center; font-size: 30px; margin-bottom: 15px;
}
.choice-card h3 { font-size: 16px; font-weight: 800; margin-bottom: 8px; color: #1e293b; }
.choice-card p { font-size: 13px; color: #64748b; margin-bottom: 15px; line-height: 1.4; }
.btn-label { font-weight: 700; font-size: 12px; color: #27ae60; text-transform: uppercase; }

@media (max-width: 500px) { .options-grid { grid-template-columns: 1fr; } }
</style>