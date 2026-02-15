<script setup>
import { ref } from 'vue';
import axios from 'axios';

const loading = ref(false);
const dados = ref({
  nome: "",
  idade: 25,
  peso: 70,
  altura: 175,
  objetivo: "Perder peso",
  restricoes: ""
});

const gerarPlano = async () => {
  if (!dados.value.nome) {
    alert("Por favor preenche o nome!");
    return;
  }

  loading.value = true;
  try {
    const response = await axios.post("http://127.0.0.1:8000/plano/gerar-pdf", dados.value, {
      responseType: 'blob' // IMPORTANTE: Para receber ficheiros binários
    });

    // Criar um link invisível para forçar o download
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `Plano_${dados.value.nome}.pdf`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

  } catch (error) {
    console.error("Erro ao gerar plano:", error);
    alert("Erro ao gerar o plano. Verifica a consola.");
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="plano-container">
    <div class="card">
      <h2>📋 Gerar Plano IA</h2>
      <p class="subtitle">A Inteligência Artificial vai criar a tua dieta perfeita.</p>

      <div class="form-grid">
        <div class="input-group">
          <label>Nome</label>
          <input v-model="dados.nome" placeholder="Teu nome" />
        </div>
        
        <div class="input-group">
          <label>Objetivo</label>
          <select v-model="dados.objetivo">
            <option>Perder peso</option>
            <option>Ganhar massa muscular</option>
            <option>Manter peso</option>
            <option>Reeducação alimentar</option>
          </select>
        </div>

        <div class="row">
          <div class="input-group">
            <label>Idade</label>
            <input v-model="dados.idade" type="number" />
          </div>
          <div class="input-group">
            <label>Peso (kg)</label>
            <input v-model="dados.peso" type="number" />
          </div>
          <div class="input-group">
            <label>Altura (cm)</label>
            <input v-model="dados.altura" type="number" />
          </div>
        </div>

        <div class="input-group">
          <label>Restrições / Alergias</label>
          <textarea v-model="dados.restricoes" placeholder="Ex: Sem glúten, vegetariano..."></textarea>
        </div>
      </div>

      <button @click="gerarPlano" :disabled="loading" class="btn-generate">
        <span v-if="loading">⏳ A Gerar com IA...</span>
        <span v-else>✨ Baixar Plano PDF</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.plano-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f0fdf4;
  padding: 20px;
}

.card {
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 500px;
  text-align: center;
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin: 30px 0;
  text-align: left;
}

.input-group label {
  font-weight: bold;
  font-size: 0.9rem;
  color: #2c3e50;
  display: block;
  margin-bottom: 5px;
}

input, select, textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.row {
  display: flex;
  gap: 10px;
}

.btn-generate {
  width: 100%;
  padding: 15px;
  background: linear-gradient(to right, #27ae60, #2ecc71);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s;
}

.btn-generate:hover:not(:disabled) {
  transform: scale(1.02);
  box-shadow: 0 5px 15px rgba(39, 174, 96, 0.4);
}

.btn-generate:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}
</style>
