<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { Leaf } from 'lucide-vue-next'

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

// --- GESTÃO DE ALERGIAS ---
const listaAlergiasOficiais = [
  "amendoim", "nozes", "avelã", "amêndoa", "castanha", "pistachio",
  "leite e derivados", "ovos", "trigo e outros cereais com glúten",
  "peixes", "crustáceos", "moluscos", "soja", "mostarda"
];
const alergiasSelecionadas = ref([]);

const handleSave = async () => {
  try {
   
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
      objetivo: "Saúde e Bem-estar" 
    };

    await axios.post("http://127.0.0.1:8000/users/save-questionnaire", payload);

    router.push("/welcome"); 
  } catch (error) {
    alert("Erro ao guardar. Verifica se preencheste tudo corretamente.");
  }
};
</script>

<template>
  <div class="view-wrapper">
    <div class="decor-blob blob-1"></div>
    <div class="decor-blob blob-2"></div>
    <div class="decor-blob blob-3"></div>

    <div class="card questionnaire-card">
      <header class="header-area">
        <span class="badge">Perfil Nutricional</span>
        <h2 class="title">Configura a tua <span class="green-text">Jornada</span></h2>
        <p class="subtitle">Olá <strong>{{ username }}</strong>, responde com sinceridade.</p>
      </header>

      <form @submit.prevent="handleSave" class="styled-form">
        
        <div class="form-column">
          <h3 class="section-title">📋 Informações Básicas</h3>
          <div class="row-two">
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

          <div class="row-two">
            <div class="input-group">
              <label>⚖️ Peso (kg)</label>
              <input v-model="peso" type="number" step="0.1" required placeholder="00.0" />
            </div>
            <div class="input-group">
              <label>📏 Altura (cm)</label>
              <input v-model="altura" type="number" step="0.1" required placeholder="160" />
            </div>
          </div>


          <h3 class="section-title">🏃‍♂️ Atividade Física</h3>

          <div class="row-two">
            <div class="input-group">
              <label>Praticas desporto?</label>
              <select v-model="exercicio">
                <option value="sim">Sim</option>
                <option value="nao">Não</option>
              </select>
            </div>
            <div v-if="exercicio === 'sim'" class="input-group">
              <label>📅 Vezes</label>
              <input v-model="frequencia" type="number" min="1" max="7" />
            </div>
          </div>


          <h3 class="section-title">🍳 Hábitos Alimentares</h3>

          <div class="input-group">
            <label>🍳 Quem cozinha em casa?</label>
            <select v-model="quemCozinha">
              <option value="mae">Mãe</option>
              <option value="pai">Pai</option>
              <option value="irmao">Irmão/Irmã</option>
              <option value="avos">Avós</option>
              <option value="outros">Outra pessoa...</option>
            </select>
            </div>


            <input 
              v-if="quemCozinha === 'outros'" 
              v-model="quemCozinhaOutro" 
              type="text" 
              placeholder="Quem cozinha?" 
              class="mt-10"
            />
          
        </div>

          <div class="form-column">
            <h3 class="section-title">⚠️ Alergias Alimentares</h3>
            <p class="helper-text">Seleciona todas as que se aplicam</p>
  
          <div class="allergies-container">
           <div class="allergies-grid">
            <label v-for="alergia in listaAlergiasOficiais" :key="alergia" class="checkbox-label">
              <input type="checkbox" :value="alergia" v-model="alergiasSelecionadas" />
              <span>{{ alergia }}</span>
              </label>
            </div>
            </div>

          <div class="selected-info" v-if="alergiasSelecionadas.length > 0">
          <strong>{{ alergiasSelecionadas.length }}</strong> alergia(s) selecionada(s)
          </div>

          <button type="submit" class="btn-main">
            Finalizar Questionário →
          </button>
        </div>

      </form>
    </div>
  </div>
</template>

<style scoped>

.header-area {
  text-align: center;
  margin-bottom: 40px;
}

.badge {
  background: linear-gradient(135deg, #47baac 0%, #3a968a 100%);
  font-size:150%;
  
}

.view-wrapper { 
  display: flex; align-items: center; justify-content: center; 
  min-height: 100vh; padding: 20px; background: #f8fafc;
  position: relative; overflow: hidden;
}

.decor-blob { position: absolute; border-radius: 50%; filter: blur(80px); z-index: 0; opacity: 0.4; animation: move 20s infinite alternate; }
.blob-1 { width: 400px; height: 400px; background: #dcfce7; top: -100px; left: -100px; }
.blob-2 { width: 300px; height: 300px; background: #47baac33; bottom: -50px; right: -50px; }
.blob-3 { width: 250px; height: 250px; background: #fef9c3; top: 10%; right: 5%; }

@keyframes move { from { transform: translate(0, 0); } to { transform: translate(30px, 50px); } }

.questionnaire-card { 
  max-width: 1200px; 
  width: 90%; background: white; 
  padding: 40px; border-radius: 30px; 
  box-shadow: 0 20px 50px rgba(0,0,0,0.05);
  position: relative; z-index: 1;
}

.row-two{
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.title { font-size: 2rem; font-weight: 800; color: #1e293b; margin: 10px 0; }
.green-text { color: #47baac; }
.subtitle { font-size: 1.1rem; color: #64748b; margin-bottom: 30px; }

.styled-form {
  display: grid; 
  grid-template-columns: 1fr 1fr; 
  gap: 40px; 
}
.row { display: flex; gap: 20px; }

.input-group label { 
  font-size: 1rem; 
  font-weight: 700; color: #47baac; margin-bottom: 10px; 
  display: block; text-align: left;
}

.input-group input, .input-group select { 
  padding: 16px; border-radius: 18px; border: 2px solid #e2e8f0; 
  background: #f8fafc; font-size: 1.1rem; transition: all 0.3s ease;
}

.input-group input:focus { 
  outline: none; border-color: #47baac; background: white; 
  box-shadow: 0 0 0 4px rgba(71, 186, 172, 0.08); 
}


.allergies-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
  background: #f0fdf4; padding: 20px; border-radius: 20px;
  border: 2px dashed #bbf7d0; max-height: 200px; overflow-y: auto;
}

.allergies-grid::-webkit-scrollbar {
  width: 6px;
}
.allergies-grid::-webkit-scrollbar-thumb {
  background: #47baac; 
}

.checkbox-label {
  display: flex; align-items: center; gap: 10px;
  font-size: 1rem; font-weight: 600; color: #374151; cursor: pointer;
}

.checkbox-label input { width: 20px; height: 20px; accent-color: #47baac; }

.btn-main { 
  background: #47baac; color: white; padding: 20px; 
  border-radius: 20px; font-size: 1.2rem; font-weight: 800; 
  cursor: pointer; border: none; margin-top: 25px;
  transition: all 0.3s ease;
}

.btn-main:hover { 
  background: #3a968a; transform: translateY(-3px); 
  box-shadow: 0 10px 20px rgba(71, 186, 172, 0.2); 
}

@media (max-width: 900px) {
  .styled-form {
    grid-template-columns: 1fr; /* 1 coluna em ecrãs pequenos */
  }
}

</style>
