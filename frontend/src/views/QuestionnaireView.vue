<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const username = localStorage.getItem("usuario_logado") || "Explorador";

// --- CAMPOS DO QUESTIONÁRIO ---
const idade = ref("");
const peso = ref("");
const altura = ref("");
const sexo = ref("Masculino");
const exercicio = ref("nao");
const frequencia = ref(0);
const brincaNaRua = ref("nao");
const comeNaCantina = ref("nao");
const quemCozinha = ref("mae");
const quemCozinhaOutro = ref("");

// --- GESTÃO DE ALERGIAS (Baseado no teu alergias.py) ---
const listaAlergiasOficiais = [
  "amendoim", "nozes", "avelã", "amêndoa", "castanha", "pistachio",
  "leite e derivados", "ovos", "trigo e outros cereais com glúten",
  "peixes", "crustáceos", "moluscos", "soja", "mostarda"
];
const alergiasSelecionadas = ref([]);

const handleSave = async () => {
  try {
    // Montamos o objeto exatamente como o teu backend espera (DadosUsuario)
    const payload = {
      username: username,
      idade: parseInt(idade.value),
      peso: parseFloat(peso.value),
      altura: parseFloat(altura.value),
      sexo: sexo.value,
      faz_desporto: exercicio.value,
      frequencia_desporto: parseInt(frequencia.value),
      brinca_na_rua: brincaNaRua.value,
      alergias: alergiasSelecionadas.value,
      quem_cozinha: quemCozinha.value,
      quem_cozinha_outro: quemCozinha.value === 'outros' ? quemCozinhaOutro.value : "",
      come_na_cantina: comeNaCantina.value,
      objetivo: "Saúde e Bem-estar" // Campo que a IA do colega costuma pedir
    };

    await axios.post("http://127.0.0.1:8000/users/save-questionnaire", payload);

    alert("Perfil e Alergias guardados com sucesso!");
    router.push("/welcome"); 
  } catch (error) {
    console.error("Erro ao salvar:", error.response?.data || error.message);
    alert("Erro ao guardar. Verifica se preencheste tudo corretamente.");
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
        <span class="badge">Perfil Nutricional</span>
        <h2 class="title">Configura a tua <span class="green-text">Jornada</span></h2>
        <p class="subtitle">Olá <strong>{{ username }}</strong>, responde com sinceridade.</p>
      </header>

      <form @submit.prevent="handleSave" class="styled-form">
        
        <div class="row">
          <div class="input-group">
            <label>🎂 Idade</label>
            <input v-model="idade" type="number" required placeholder="Ex: 14" />
          </div>
          <div class="input-group">
            <label>🚻 Sexo</label>
            <select v-model="sexo">
              <option value="Masculino">Masculino</option>
              <option value="Feminino">Feminino</option>
            </select>
          </div>
        </div>

        <div class="row">
          <div class="input-group">
            <label>⚖️ Peso (kg)</label>
            <input v-model="peso" type="number" step="0.1" required placeholder="00.0" />
          </div>
          <div class="input-group">
            <label>📏 Altura (cm)</label>
            <input v-model="altura" type="number" step="0.1" required placeholder="160" />
          </div>
        </div>

        <div class="row">
          <div class="input-group">
            <label>🏃‍♂️ Praticas Desporto?</label>
            <select v-model="exercicio">
              <option value="sim">Sim</option>
              <option value="nao">Não</option>
            </select>
          </div>
          <div v-if="exercicio === 'sim'" class="input-group">
            <label>📅 Vezes/Semana</label>
            <input v-model="frequencia" type="number" min="1" max="7" />
          </div>
        </div>

        <div class="row">
          <div class="input-group">
            <label>🌳 Brincas na rua?</label>
            <select v-model="brincaNaRua">
              <option value="sim">Sim, muito!</option>
              <option value="nao">Raramente</option>
            </select>
          </div>
          <div class="input-group">
            <label>🏫 Comes na cantina?</label>
            <select v-model="comeNaCantina">
              <option value="sim">Sim</option>
              <option value="nao">Não</option>
            </select>
          </div>
        </div>

        <div class="input-group">
          <label>🍳 Quem cozinha em casa?</label>
          <select v-model="quemCozinha">
            <option value="mae">Mãe</option>
            <option value="pai">Pai</option>
            <option value="irmao">Irmão/Irmã</option>
            <option value="avos">Avós</option>
            <option value="outros">Outra pessoa...</option>
          </select>
          <input 
            v-if="quemCozinha === 'outros'" 
            v-model="quemCozinhaOutro" 
            type="text" 
            placeholder="Quem cozinha?" 
            class="mt-10"
          />
        </div>

        <div class="input-group">
          <label>⚠️ Alergias Alimentares (Seleciona as que tens)</label>
          <div class="allergies-grid">
            <label v-for="alergia in listaAlergiasOficiais" :key="alergia" class="checkbox-label">
              <input type="checkbox" :value="alergia" v-model="alergiasSelecionadas" />
              <span>{{ alergia }}</span>
            </label>
          </div>
        </div>

        <button type="submit" class="btn-main">
          Finalizar Questionário
          <span class="btn-icon">→</span>
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* Mantive o teu CSS e adicionei o das alergias */
.view-wrapper { display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 40px 20px; background: #f6f9fc; }
.questionnaire-card { max-width: 650px; width: 100%; background: white; padding: 40px; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }

.allergies-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  background: #f8fafc;
  padding: 15px;
  border-radius: 14px;
  border: 2px solid #f1f3f5;
  max-height: 150px;
  overflow-y: auto;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  cursor: pointer;
}

.checkbox-label input { width: auto; }

.mt-10 { margin-top: 10px; }
.green-text { color: #27ae60; }
.styled-form { display: flex; flex-direction: column; gap: 15px; }
.row { display: flex; gap: 15px; }
.input-group { display: flex; flex-direction: column; flex: 1; }
.input-group label { font-size: 13px; font-weight: bold; margin-bottom: 5px; }
.input-group input, .input-group select { padding: 12px; border-radius: 10px; border: 1px solid #ddd; }
.btn-main { background: #2d3436; color: white; padding: 15px; border-radius: 12px; font-weight: bold; cursor: pointer; border: none; margin-top: 20px; }
.btn-main:hover { background: #27ae60; }

/* ... resto do teu CSS ... */
</style>