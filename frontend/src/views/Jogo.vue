<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

// --- ESTADOS DO CATÁLOGO ---
const alimentos = ref([]);
const alimentoSelecionado = ref(null);

// 1. Carregar Alimentos para o Catálogo (Lado Esquerdo)
const carregarAlimentos = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/alimentos-jogo");
    alimentos.value = response.data;
  } catch (error) {
    console.error("Erro ao carregar catálogo:", error);
  }
};

onMounted(() => {
  carregarAlimentos();
});
</script>

<template>
  <div class="game-container">
    <div class="catalog-side">
      <button @click="router.push('/welcome')" class="btn-back">← Voltar</button>
      <h2 class="section-title">🍎 Biblioteca de <span class="green-text">Nutrientes</span></h2>
      
      <div class="food-list">
        <div 
          v-for="item in alimentos" 
          :key="item.nome" 
          @click="alimentoSelecionado = item"
          :class="['food-card', { active: alimentoSelecionado?.nome === item.nome }]"
        >
          {{ item.nome }}
        </div>
      </div>

      <div v-if="alimentoSelecionado" class="food-details">
        <div class="food-header-info">
            <img 
              :src="`http://127.0.0.1:8000/static/${alimentoSelecionado.nome}.png`" 
              class="food-image" 
              @error="(e) => e.target.src = '/placeholder-food.png'" 
            />
          <div>
            <h3>{{ alimentoSelecionado.nome }}</h3>
            <span :class="['tag-cor', alimentoSelecionado.cor]">{{ alimentoSelecionado.cor.toUpperCase() }}</span>
          </div>
        </div>
        
        <p class="description">{{ alimentoSelecionado.descricao }}</p>
        
        <div class="stats-grid">
          <div class="stat"><span>🔥 Calorias:</span> {{ alimentoSelecionado.energia_kcal }}</div>
          <div class="stat"><span>💪 Proteína:</span> {{ alimentoSelecionado.proteina_g }}g</div>
        </div>
      </div>
    </div>

    <div class="game-side">
      <div class="iframe-wrapper">
        <div class="game-header-bar">
          <h3>NutriSnake (Python Engine)</h3>
        </div>
        <iframe 
          src="http://127.0.0.1:8000/play-game" 
          class="game-iframe"
          frameborder="0"
          scrolling="no"
        ></iframe>
        <p class="controls-hint">💡 Clica no jogo para ativar os comandos das setas!</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.game-container { display: flex; height: 100vh; background: #f8fafc; overflow: hidden; }

/* Lado Esquerdo */
.catalog-side { flex: 0 0 400px; padding: 40px; overflow-y: auto; border-right: 1px solid #e2e8f0; background: white; }
.food-list { display: flex; flex-wrap: wrap; gap: 8px; margin: 20px 0; }
.food-card { padding: 8px 15px; background: #f1f5f9; border: 2px solid transparent; border-radius: 10px; cursor: pointer; font-size: 14px; transition: 0.2s; }
.food-card.active { border-color: #27ae60; background: #f0fdf4; color: #27ae60; font-weight: bold; }

.food-details { margin-top: 20px; padding: 20px; background: #2d3436; color: white; border-radius: 20px; }
.food-header-info { display: flex; gap: 15px; align-items: center; margin-bottom: 15px; }
.food-image { width: 60px; height: 60px; object-fit: cover; border-radius: 10px; background: white; padding: 3px; }
.tag-cor.verde { color: #2ecc71; }
.tag-cor.amarelo { color: #f1c40f; }
.tag-cor.vermelho { color: #e74c3c; }

/* Lado Direito */
.game-side { flex: 1; display: flex; align-items: center; justify-content: center; background: #f0fdf4; }
.iframe-wrapper { width: 920px; height: 850px; display: flex; flex-direction: column; align-items: center; }
.game-header-bar { width: 100%; background: #27ae60; color: white; padding: 10px 20px; border-radius: 20px 20px 0 0; text-align: left; }
.game-iframe { width: 900px; height: 800px; border: 4px solid #27ae60; background: black; }
.controls-hint { margin-top: 10px; font-size: 14px; color: #64748b; font-weight: bold; }

.btn-back { margin-bottom: 20px; padding: 8px 15px; cursor: pointer; border-radius: 8px; border: 1px solid #ddd; background: white; }
.green-text { color: #27ae60; }
</style>