<script setup>
import { ref, nextTick } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const username = localStorage.getItem("usuario_logado") || "Explorador";

// --- ESTADOS ---
const question = ref("");
const chatContainer = ref(null);
const loading = ref(false);

// Histórico de mensagens
const messages = ref([
  { text: `Olá ${username}! Sou o teu NutriBot. Em que posso ajudar-te hoje?`, isAi: true }
]);

// Função para fazer scroll automático para a última mensagem
const scrollToBottom = async () => {
  await nextTick();
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

const sendQuestion = async () => {
  // Remove only leading/trailing spaces, but allow spaces in the middle
  if (!question.value || loading.value) return;

  const userMsg = question.value.trim(); // Trim spaces only for sending
  messages.value.push({ text: userMsg, isAi: false });
  question.value = ""; // Clear the input field
  loading.value = true;
  await scrollToBottom();

  try {
    // Liga-se à rota da IA que o teu colega criou
    const response = await axios.post("http://127.0.0.1:8000/nutrium/chat-sos", {
      pergunta: userMsg
    });

    messages.value.push({ text: response.data.resposta, isAi: true });
  } catch (error) {
    messages.value.push({ 
      text: "Houve um erro a falar com o meu cérebro (IA). Verifica se o servidor está ligado!", 
      isAi: true 
    });
  } finally {
    loading.value = false;
    await scrollToBottom();
  }
};
</script>

<template>
  <div class="page-wrapper">
    <button @click="router.push('/welcome')" class="back-floating-btn">
      ← Voltar
    </button>

    <div class="chat-card">
      <div class="robo-avatar">
        <div class="avatar-circle">🤖</div>
        <div class="online-indicator"></div>
      </div>

      <div class="chat-header">
        <h2>Amigo <span class="green-text">Presente</span></h2>
        <p>Assistente Virtual Nutrium</p>
      </div>

      <div class="chat-body" ref="chatContainer">
        <div v-for="(msg, index) in messages" :key="index" 
             :class="['bubble', msg.isAi ? 'ai-bubble' : 'user-bubble']">
          {{ msg.text }}
        </div>

        <div v-if="loading" class="bubble ai-bubble typing">
          <span></span><span></span><span></span>
        </div>
      </div>

      <div class="chat-footer">
        <input 
          v-model="question" 
          @keyup.enter="sendQuestion"
          placeholder="Escreve a tua pergunta..." 
          type="text" 
        />
        <button @click="sendQuestion" :disabled="loading" class="send-btn">
          <span v-if="!loading">Enviar</span>
          <span v-else>...</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 20px;
}

.back-floating-btn {
  position: absolute;
  top: 30px;
  left: 30px;
  padding: 10px 20px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 10px;
  cursor: pointer;
  font-weight: bold;
  transition: 0.3s;
}

.back-floating-btn:hover { background: #f9f9f9; transform: translateX(-5px); }

.chat-card {
  width: 100%;
  max-width: 450px;
  height: 600px;
  background: white;
  border-radius: 25px;
  display: flex;
  flex-direction: column;
  position: relative;
  box-shadow: 0 15px 35px rgba(0,0,0,0.1);
}

/* Posicionamento do Robô */
.robo-avatar {
  position: absolute;
  top: -30px;
  right: 20px;
  z-index: 5;
}

.avatar-circle {
  width: 70px;
  height: 70px;
  background: #27ae60;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 35px;
  border: 4px solid white;
  box-shadow: 0 8px 15px rgba(39, 174, 96, 0.3);
}

.online-indicator {
  position: absolute;
  bottom: 5px;
  right: 5px;
  width: 15px;
  height: 15px;
  background: #2ecc71;
  border: 3px solid white;
  border-radius: 50%;
}

.chat-header {
  padding: 30px 25px 15px;
  border-bottom: 1px solid #f0f0f0;
}

.chat-header h2 { margin: 0; font-size: 22px; color: #2d3436; }
.green-text { color: #27ae60; }
.chat-header p { margin: 5px 0 0; font-size: 13px; color: #636e72; }

.chat-body {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #fdfdfd;
}

.bubble {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.5;
}

.ai-bubble {
  align-self: flex-start;
  background: #eef2f7;
  color: #2d3436;
  border-bottom-left-radius: 4px;
}

.user-bubble {
  align-self: flex-end;
  background: #27ae60;
  color: white;
  border-bottom-right-radius: 4px;
}

.chat-footer {
  padding: 20px;
  display: flex;
  gap: 10px;
  border-top: 1px solid #f0f0f0;
}

.chat-footer input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  outline: none;
}

.chat-footer input:focus { border-color: #27ae60; }

.send-btn {
  background: #27ae60;
  color: white;
  border: none;
  padding: 0 20px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: bold;
}

/* Animação de digitação */
.typing span {
  display: inline-block;
  width: 6px;
  height: 6px;
  background: #999;
  border-radius: 50%;
  margin-right: 3px;
  animation: bounce 1.3s infinite;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-5px); }
}
</style>