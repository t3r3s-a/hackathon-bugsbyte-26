<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const username = localStorage.getItem("usuario_logado") || "Explorador";

// Campos do questionário
const peso = ref("");
const altura = ref("");
const exercicio = ref("nao");
const frequencia = ref(0);
const doencas = ref("");

const handleSave = async () => {
  try {
    await axios.post("http://127.0.0.1:8000/users/save-profile", {
      username: username,
      peso: parseFloat(peso.value),
      altura: parseInt(altura.value),
      objetivo: "Geral", 
      restricoes: doencas.value,
      exercicio_fisico: exercicio.value,
      frequencia_exercicio: String(frequencia.value) + " vezes por semana",
    });

    alert("Perfil guardado! A gerar o teu plano personalizado...");
    router.push("/welcome"); // Redireciona para a tela de escolha (Cobra vs IA)
  } catch (error) {
    console.error(error);
    alert("Erro ao guardar o questionário. Verifica se o servidor está ligado.");
  }
};
</script>

<template>
  <div class="view-wrapper">
    <div class="card questionnaire-card">
      <div class="progress-container">
        <div class="progress-bar"></div>
      </div>

      <header class="header-area">
        <span class="badge">Passo 1: Perfil</span>
        <h2 class="title">Vamos criar o teu <span class="green-text">Plano</span></h2>
        <p class="subtitle">
          Olá <strong>{{ username }}</strong>, os teus dados ajudam a nossa IA a ser mais precisa.
        </p>
      </header>

      <form @submit.prevent="handleSave" class="styled-form">
        <div class="row">
          <div class="input-group">
            <label><i class="icon">⚖️</i> Peso (kg)</label>
            <input v-model="peso" type="number" step="0.1" required placeholder="00.0" />
          </div>
          <div class="input-group">
            <label><i class="icon">📏</i> Altura (cm)</label>
            <input v-model="altura" type="number" required placeholder="170" />
          </div>
        </div>

        <div class="input-group">
          <label><i class="icon">🏃‍♂️</i> Praticas exercício físico?</label>
          <div class="select-wrapper">
            <select v-model="exercicio">
              <option value="sim">Sim, mantenho-me ativo</option>
              <option value="nao">Não, de momento sou sedentário</option>
            </select>
          </div>
        </div>

        <transition name="fade">
          <div v-if="exercicio === 'sim'" class="input-group">
            <label><i class="icon">📅</i> Vezes por semana</label>
            <input v-model="frequencia" type="number" min="1" max="7" placeholder="1 a 7" />
          </div>
        </transition>

        <div class="input-group">
          <label><i class="icon">⚠️</i> Restrições ou Doenças</label>
          <textarea
            v-model="doencas"
            placeholder="Ex: Alergia a glúten, Diabetes, Vegetariano..."
          ></textarea>
        </div>

        <button type="submit" class="btn-main">
          Gerar Plano Inteligente
          <span class="btn-icon">→</span>
        </button>
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
  padding: 20px;
  background: linear-gradient(135deg, #f6f9fc 0%, #eef2f7 100%);
}

.questionnaire-card {
  max-width: 550px;
  width: 100%;
  background: white;
  padding: 45px;
  border-radius: 32px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0,0,0,0.03);
}

/* Barra de progresso animada */
.progress-container {
  width: 100%;
  height: 6px;
  background: #f0f0f0;
  border-radius: 10px;
  margin-bottom: 30px;
  overflow: hidden;
}
.progress-bar {
  width: 40%;
  height: 100%;
  background: #27ae60;
  border-radius: 10px;
  animation: load 1.5s ease-out;
}

.header-area {
  margin-bottom: 35px;
  text-align: left;
}

.badge {
  background: rgba(39, 174, 96, 0.1);
  color: #27ae60;
  padding: 6px 14px;
  border-radius: 50px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}

.title {
  font-size: 28px;
  font-weight: 800;
  margin-top: 15px;
  color: #2d3436;
}

.green-text { color: #27ae60; }

.subtitle {
  color: #636e72;
  font-size: 15px;
  margin-top: 8px;
}

.styled-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.row {
  display: flex;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  text-align: left;
  flex: 1;
}

.input-group label {
  font-size: 13px;
  font-weight: 700;
  color: #2d3436;
  margin-bottom: 8px;
}

.input-group input, 
.input-group select, 
.input-group textarea {
  padding: 14px;
  border-radius: 14px;
  border: 2px solid #f1f3f5;
  background: #f8fafc;
  font-size: 15px;
  transition: all 0.2s ease;
}

.input-group input:focus, 
.input-group select:focus, 
.input-group textarea:focus {
  border-color: #27ae60;
  background: white;
  outline: none;
  box-shadow: 0 0 0 4px rgba(39, 174, 96, 0.1);
}

textarea {
  min-height: 100px;
  resize: vertical;
}

.btn-main {
  background: #2d3436;
  color: white;
  padding: 18px;
  border-radius: 18px;
  border: none;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.btn-main:hover {
  background: #27ae60;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(39, 174, 96, 0.2);
}

.btn-icon {
  font-size: 20px;
  transition: transform 0.2s;
}

.btn-main:hover .btn-icon {
  transform: translateX(5px);
}

/* Animações */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s, transform 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-10px); }

@keyframes load {
  from { width: 0%; }
  to { width: 40%; }
}

@media (max-width: 480px) {
  .row { flex-direction: column; }
  .questionnaire-card { padding: 30px; }
}
</style>