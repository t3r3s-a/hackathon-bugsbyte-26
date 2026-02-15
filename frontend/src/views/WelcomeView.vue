<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const loading = ref(false); // Para mostrar "A carregar..."

// Recupera o utilizador logado (ex: "pou")
const usuario = localStorage.getItem("usuario_logado") || "Explorador";

// --- FUNÇÃO PARA BAIXAR O PDF DA IA ---
const baixarPlano = async () => {
  loading.value = true;
  try {
    const response = await axios.post(`http://127.0.0.1:8000/plano/gerar-pdf`, 
      { username: usuario }, 
      { responseType: 'blob' }
    );
    // ... lógica de download (URL.createObjectURL) ...
    
    // Opcional: Bloquear o botão localmente após sucesso
    jaDescarregou.value = true; 

  } catch (error) {
    if (error.response && error.response.status === 403) {
      alert("🚀 Oops! Já tens o teu plano. Só podes fazer o download uma vez para focares na tua missão!");
    } else {
      alert("Erro ao gerar o plano.");
    }
  } finally {
    loading.value = false;
  }
};

const irParaJogo = () => router.push('/games');
const irParaChat = () => router.push('/chat'); // Confirma se tens esta rota
</script>

<template>
  <div class="view-wrapper">
    <div class="decor-blob blob-1"></div>
    <div class="decor-blob blob-2"></div>
    <div class="decor-blob blob-3"></div>

    <div class="dashboard-container">
      
      <header class="welcome-header">
        <h1 class="brand">Olá, <span class="snake-text">{{ usuario }}</span>!</h1>
        <p>O teu perfil nutricional foi analisado. O que queres explorar agora?</p>
      </header>

      <div class="options-container">
        <button @click="baixarPlano" class="botao-download-especial" :disabled="loading">
    <div class="conteudo-botao">
      <span class="foguete-emoji">🚀</span>
      
      <div class="texto-botao">
        <span class="titulo-plano">Plano Personalizado</span>
        <span class="sub-download">{{ loading ? 'A preparar...' : 'download' }}</span>
      </div>

      <span class="foguete-emoji">🚀</span>
    </div>
  </button>
        <div class="options-grid">
          <button @click="irParaJogo" class="choice-card snake-card">
            <div class="icon-circle">🐍</div>
            <h3>Snack-e Game</h3>
            <p>Aprende e diverte-te!</p>
            <span class="btn-label">Jogar Agora</span>
          </button>

          <button @click="irParaChat" class="choice-card ai-card">
            <div class="icon-circle">🤖</div>
            <h3>Amigo Presente</h3>
            <p>Dúvidas? Pergunta à IA.</p>
            <span class="btn-label">Conversar</span>
          </button>
        </div> </div> <button @click="router.push('/')" class="btn-logout">Sair da conta</button>
      
    </div> </div> </template>
    
<style scoped>
/* Mantive o teu estilo base e melhorei as transições */
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
.welcome-header h1 { font-size: 30px; font-weight: 800; margin-bottom: 10px; }
.welcome-header p { color: #64748b; margin-bottom: 35px; }

/* Gradiente Laranja/Verde para o nome */
.snake-text { 
  background: linear-gradient(90deg, #27ae60, #2ecc71); 
  -webkit-background-clip: text; 
  -webkit-text-fill-color: transparent; 
}

.welcome-header { text-align: center; margin-bottom: 40px; }
.brand-logo { height: 45px; margin-bottom: 20px; }
.title { font-size: 2.2rem; font-weight: 800; color: #1e293b; margin-bottom: 10px; }
.highlight { color: #47baac; }
.subtitle { color: #64748b; font-size: 1.1rem; }

.plan-hero-btn {
  display: flex; align-items: center; justify-content: space-between;
  padding: 25px; border-radius: 24px; border: none;
  background: #2d3436; color: white; cursor: pointer;
  transition: all 0.3s ease; text-align: left;
  background: linear-gradient(135deg, #47baac 0%, #3a968a 100%); color: white;
}
.plan-hero-btn:hover {
  background: #27ae60; transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(39, 174, 96, 0.2);
}

.options-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

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

.icon-circle {
  width: 60px; height: 60px; background: #f0fdf4;
  border-radius: 50%; display: flex; align-items: center;
  justify-content: center; font-size: 30px; margin-bottom: 15px;
}

.btn-label { font-weight: 700; font-size: 12px; color: #27ae60; text-transform: uppercase; margin-top: 10px; }

.btn-logout {
  margin-top: 30px; background: none; border: none; color: #94a3b8;
  font-size: 14px; cursor: pointer; text-decoration: underline;
}



@media (max-width: 650px) {
  .sub-grid { grid-template-columns: 1fr; }
  .dashboard-container { padding: 30px; }
  .title { font-size: 1.8rem; }
}
</style>

<style scoped>
/* Garante que o botão aparece bem no meio */
.container-plano {
  width: 100%;
  display: flex;           /* Ativa o alinhamento flexível */
  justify-content: center; /* Centraliza na horizontal */
  align-items: center;     /* Centraliza na vertical */
  margin: 30px 0;          /* Dá espaço em cima e em baixo */
}

.botao-download-especial {
  display: flex;           /* Mantém para alinhar os foguetes lá dentro */
  margin: 0 auto 30px;     /* O 'auto' nas laterais centra o botão no ecrã */
  
  /* Resto do teu código que já tinhas: */
  width: 80%;
  max-width: 550px;
  padding: 40px;
  border-radius: 100px;
  border: none;
  background: linear-gradient(150deg, #47baac 0%, #2ecc71 100%);
  color: white;
  box-shadow: 0 10px 20px rgba(71, 186, 172, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.botao-download-especial:hover {
  transform: scale(1.02);
  box-shadow: 0 15px 30px rgba(71, 186, 172, 0.5);
}

.botao-download-especial:active {
  transform: scale(0.98);
}

.conteudo-botao {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 30px;
}

.texto-botao {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.titulo-plano {
  font-size: 2.2rem;
  font-weight: 900;
  text-transform: none; /* Mantém como escreveste */
  letter-spacing: -1px;
}

.sub-download {
  font-size: 1.2rem;
  font-weight: 500;
  opacity: 0.9;
  text-transform: lowercase; /* Fica o "download" pequeno em baixo */
}

.foguete-emoji {
  font-size: 45px;
  /* Animação para o foguete abanar um bocadinho */
  animation: balanco 2s infinite ease-in-out;
}

@keyframes balanco {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(10deg); }
}

/* Se estiver a carregar, o botão fica mais cinzento */
.botao-download-especial:disabled {
  filter: grayscale(0.6);
  cursor: wait;
}
</style>