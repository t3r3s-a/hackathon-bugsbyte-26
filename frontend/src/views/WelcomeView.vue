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
    // Chama a rota que criámos no backend: /api/plano/{username}
    const response = await axios.get(`http://127.0.0.1:8000/api/plano/${usuario}`, {
      responseType: 'blob' // OBRIGATÓRIO para ficheiros (PDF, Imagens, etc)
    });

    // Cria um link invisível para forçar o download no browser
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `Plano_Nutrium_${usuario}.pdf`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

  } catch (error) {
    console.error(error);
    alert("Não foi possível gerar o plano. Verifica se preencheste o questionário!");
  } finally {
    loading.value = false;
  }
};

const irParaJogo = () => router.push('/jogo');
const irParaChat = () => router.push('/chat'); // Confirma se tens esta rota
</script>

<template>
  <div class="view-wrapper">
    <div class="card selection-card">
      <header class="welcome-header">
        <h1 class="brand">Olá, <span class="snake-text">{{ usuario }}</span>!</h1>
        <p>O teu perfil nutricional foi analisado. O que queres explorar agora?</p>
      </header>

      <div class="options-container">
        <button 
          @click="baixarPlano" 
          class="plan-hero-btn" 
          :disabled="loading"
          :style="loading ? 'opacity: 0.7; cursor: wait;' : ''"
        >
          <div class="hero-content">
            <span class="hero-icon" v-if="!loading">📋</span>
            <span class="hero-icon spinning" v-else>⏳</span>
            
            <div class="hero-text">
              <h3 v-if="!loading">Baixar o meu Plano Personalizado</h3>
              <h3 v-else>A IA está a criar o teu plano...</h3>
              
              <p v-if="!loading">Consulta as tuas metas de calorias e macros</p>
              <p v-else>Isto pode demorar uns segundos.</p>
            </div>
          </div>
          <span class="arrow" v-if="!loading">⬇️</span>
        </button>

        <div class="options-grid">
          <button @click="irParaJogo" class="choice-card snake-card">
            <div class="icon-circle">🐍</div>
            <h3>Snack-e Game</h3>
            <p>Aprende sobre alimentos e diverte-te!</p>
            <span class="btn-label">Jogar Agora</span>
          </button>

          <button @click="irParaChat" class="choice-card ai-card">
            <div class="icon-circle">🤖</div>
            <h3>Amigo Presente</h3>
            <p>Dúvidas? Pergunta ao nosso robô.</p>
            <span class="btn-label">Conversar</span>
          </button>
        </div>
      </div>

      <button @click="router.push('/')" class="btn-logout">Sair da conta</button>
    </div>
  </div>
</template>

<style scoped>
/* Mantive o teu estilo base e melhorei as transições */
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

/* Gradiente Laranja/Verde para o nome */
.snake-text { 
  background: linear-gradient(90deg, #27ae60, #2ecc71); 
  -webkit-background-clip: text; 
  -webkit-text-fill-color: transparent; 
}

.options-container { display: flex; flex-direction: column; gap: 20px; }

.plan-hero-btn {
  display: flex; align-items: center; justify-content: space-between;
  padding: 25px; border-radius: 24px; border: none;
  background: #2d3436; color: white; cursor: pointer;
  transition: all 0.3s ease; text-align: left;
}
.plan-hero-btn:hover {
  background: #27ae60; transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(39, 174, 96, 0.2);
}

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
  width: 60px; height: 60px; background: #f0fdf4;
  border-radius: 50%; display: flex; align-items: center;
  justify-content: center; font-size: 30px; margin-bottom: 15px;
}

.btn-label { font-weight: 700; font-size: 12px; color: #27ae60; text-transform: uppercase; margin-top: 10px; }

.btn-logout {
  margin-top: 30px; background: none; border: none; color: #94a3b8;
  font-size: 14px; cursor: pointer; text-decoration: underline;
}

@media (max-width: 500px) { .options-grid { grid-template-columns: 1fr; } }
</style>