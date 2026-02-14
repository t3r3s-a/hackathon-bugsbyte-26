<script setup>
import { useRouter } from "vue-router";
// Importamos a logo para manter a marca presente
import logoParceria from "../assets/logo-parceria.png"; 

const router = useRouter();
const usuario = localStorage.getItem("usuario_logado") || "Explorador";

// Dica aleatória para dar vida à página
const dicas = [
  "Beber água ajuda-te a pensar melhor! 💧",
  "As maçãs dão-te energia para brincar! 🍎",
  "Um prato colorido é um prato de super-herói! 🌈",
  "Cresce forte e saudável com a ajuda dos legumes! 🥦",
  "Fruta fresca é o melhor doce da natureza! 🍓",
  "Mastiga bem para sentires todos os sabores! 😋",
  "Beber água é o segredo para teres super velocidade! ⚡",
  "Experimenta um alimento novo hoje e sê um explorador! 🧭",
  "Barriga feliz, coração contente! ❤️",
  "Sopa no início da refeição dá-te superpoderes! 🥣",
  "O pequeno-almoço é o combustível para o teu dia! 🚀",
  "O teu corpo é o teu castelo, cuida bem dele! 🏰",
  "Beber leite ou bebidas vegetais fortalece os teus ossos! 🥛",
  "Cenouras ajudam-te a ver melhor, como um lince! 🥕",
  "Frutos secos são pequenos tesouros de energia! 🥜",
  "Dormir bem ajuda a tua comida a fazer-te crescer! 💤",
  "Lavar as mãos antes de comer é o primeiro passo da saúde! 🧼",
  "Tu és o que comes: escolhe ser incrível! ✨"
];
  
const dicaDoDia = dicas[Math.floor(Math.random() * dicas.length)];
</script>

<template>
  <div class="view-wrapper">
    <div class="decor-blob blob-1"></div>
    <div class="decor-blob blob-2"></div>
    <div class="decor-blob blob-3"></div>

    <div class="dashboard-container">
      <header class="welcome-header">
        <img :src="logoParceria" alt="Nutrium x Snack-e" class="brand-logo" />
        <h1 class="title">Olá, <span class="highlight">{{ usuario }}</span>! 🌟</h1>
        <p class="subtitle">O que vamos explorar hoje?</p>
      </header>

      <div class="main-grid">
        <button @click="router.push('/dashboard')" class="hero-card plan-card">
          <div class="hero-info">
            <span class="big-icon">🥗</span>
            <div class="hero-text-content">
              <h3>O Meu Plano Saudável</h3>
              <p>Descobre o que o teu corpo precisa hoje para crescer forte!</p>
            </div>
          </div>
          <span class="action-tag">Ver agora</span>
        </button>

        <div class="sub-grid">
          <button @click="router.push('/chat')" class="choice-card ai-card">
            <div class="icon-bg">🤖</div>
            <h3>IA Nutricional</h3>
            <p>Tens dúvidas? Conversa com a nossa IA!</p>
            <div class="card-footer">Falar agora →</div>
          </button>

          <button @click="router.push('/snake-game')" class="choice-card game-card">
            <div class="icon-bg">🐍</div>
            <h3>Snack-e Game</h3>
            <p>Diverte-te e queima calorias!</p>
            <div class="card-footer">Começar Jogo →</div>
          </button>
        </div>

        <div class="tip-card">
          <span class="tip-icon">💡</span>
          <p><strong>Dica do dia:</strong> {{ dicaDoDia }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.view-wrapper {
  display: flex; align-items: center; justify-content: center;
  min-height: 100vh; background: #f8fafc; padding: 30px;
  position: relative; overflow: hidden; font-family: 'Inter', sans-serif;
}

/* Blobs de Fundo */
.decor-blob { position: absolute; border-radius: 50%; filter: blur(80px); z-index: 0; opacity: 0.4; animation: move 20s infinite alternate; }
.blob-1 { width: 500px; height: 500px; background: #dcfce7; top: -100px; left: -100px; }
.blob-2 { width: 400px; height: 400px; background: #47baac33; bottom: -50px; right: -50px; animation-delay: -5s; }
.blob-3 { width: 300px; height: 300px; background: #fef9c3; top: 20%; right: 10%; }

@keyframes move { from { transform: translate(0, 0); } to { transform: translate(40px, 60px); } }

.dashboard-container {
  width: 100%; max-width: 800px; position: relative; z-index: 1;
  background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(15px);
  padding: 50px; border-radius: 40px; border: 1px solid rgba(255, 255, 255, 0.7);
  box-shadow: 0 25px 50px rgba(0,0,0,0.05);
}

.welcome-header { text-align: center; margin-bottom: 40px; }
.brand-logo { height: 45px; margin-bottom: 20px; }
.title { font-size: 2.2rem; font-weight: 800; color: #1e293b; margin-bottom: 10px; }
.highlight { color: #47baac; }
.subtitle { color: #64748b; font-size: 1.1rem; }

.main-grid { display: flex; flex-direction: column; gap: 24px; }

/* Hero Card */
.hero-card {
  width: 100%; display: flex; align-items: center; justify-content: space-between;
  padding: 30px; border-radius: 28px; border: none; cursor: pointer;
  transition: all 0.3s ease; text-align: left;
  background: linear-gradient(135deg, #47baac 0%, #3a968a 100%); color: white;
}
.hero-card:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(71, 186, 172, 0.3); }
.hero-info { display: flex; align-items: center; gap: 25px; }
.big-icon { font-size: 45px; }
.hero-text-content h3 { font-size: 1.4rem; margin: 0 0 5px 0; font-weight: 800; }
.hero-text-content p { margin: 0; opacity: 0.9; font-size: 1rem; }
.action-tag { background: rgba(255, 255, 255, 0.2); padding: 8px 16px; border-radius: 50px; font-weight: 700; font-size: 0.8rem; text-transform: uppercase; }

/* Sub Grid */
.sub-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }

.choice-card {
  background: white; border: 1.5px solid #f1f5f9; padding: 30px;
  border-radius: 28px; cursor: pointer; transition: all 0.3s ease;
  display: flex; flex-direction: column; align-items: center; text-align: center;
}
.choice-card:hover { transform: translateY(-5px); border-color: #47baac; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }

.icon-bg {
  width: 70px; height: 70px; background: #f0fdf4; border-radius: 20px;
  display: flex; align-items: center; justify-content: center;
  font-size: 35px; margin-bottom: 20px;
}
.choice-card h3 { font-size: 1.2rem; font-weight: 800; color: #1e293b; margin: 0 0 10px 0; }
.choice-card p { font-size: 0.95rem; color: #64748b; margin: 0 0 20px 0; line-height: 1.5; }
.card-footer { font-weight: 700; color: #47baac; font-size: 0.9rem; }

/* Dica do Dia */
.tip-card {
  display: flex; align-items: center; gap: 15px; padding: 20px;
  background: #fef9c3; border-radius: 20px; color: #854d0e;
}
.tip-icon { font-size: 24px; }
.tip-card p { margin: 0; font-size: 0.95rem; }

@media (max-width: 650px) {
  .sub-grid { grid-template-columns: 1fr; }
  .dashboard-container { padding: 30px; }
  .title { font-size: 1.8rem; }
}
</style>