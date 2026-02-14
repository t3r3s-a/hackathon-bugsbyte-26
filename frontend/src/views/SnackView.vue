<script setup>
import { ref, computed, onMounted, onUnmounted, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { CONSTANTES } from '../game/constantes';
import { SnakeEngine } from '../game/SnakeEngine';
import { EquilibrioEngine } from '../game/minijogos/EquilibrioEngine';
import { CorridaEngine } from '../game/minijogos/CorridaEngine';
import { DinoEngine } from '../game/minijogos/DinoEngine';

const router = useRouter();
const canvasRef = ref(null);
const estadoCena = ref('JOGANDO');

const gameInstance = ref(null);
const minigameInstance = ref(null);
const teclasPressionadas = reactive({});

// 🔥 COMPUTED para reatividade
const pontuacao = computed(() => gameInstance.value?.pontuacao || 0);
const calorias = computed(() => Math.floor(gameInstance.value?.calorias || 0));

let lastTime = 0;
let frameCount = 0; // 🔥 Contador para debug

const gameLoop = (timestamp) => {
  const deltaTime = (timestamp - lastTime) / 1000;
  lastTime = timestamp;

  frameCount++;
  
  // 🔥 DEBUG: Log a cada 60 frames (1 segundo)
  if (frameCount % 60 === 0) {
    console.log('🎮 Frame:', frameCount, 'Estado:', estadoCena.value);
    console.log('🐍 Cobra:', gameInstance.value?.cobra);
    console.log('🍎 Alimento:', gameInstance.value?.alimento_pos);
  }

  if (estadoCena.value === 'JOGANDO') {
    if (!gameInstance.value) {
      console.error('❌ gameInstance é null!');
      return;
    }
    
    gameInstance.value.update();
    gameInstance.value.draw();
    
    if (gameInstance.value.emTransicao) estadoCena.value = 'TRANSICAO';
  } 
  else if (estadoCena.value === 'MINIJOGO') {
    minigameInstance.value?.update(deltaTime || 0.016, teclasPressionadas);
    minigameInstance.value?.draw();
    
    if (minigameInstance.value?.finalizado) {
      gameInstance.value.aplicarResultadoMinijogo(minigameInstance.value.resultado);
      estadoCena.value = 'JOGANDO';
      gameInstance.value.emTransicao = false;
      gameInstance.value.contador_frames_fase = 0;
    }
  }

  requestAnimationFrame(gameLoop);
};

const iniciarMinijogoAleatorio = () => {
  const jogos = ['equilibrio', 'corrida', 'dino'];
  const escolha = jogos[Math.floor(Math.random() * jogos.length)];
  
  if (escolha === 'equilibrio') minigameInstance.value = new EquilibrioEngine(canvasRef.value, gameInstance.value.calorias);
  if (escolha === 'corrida') minigameInstance.value = new CorridaEngine(canvasRef.value);
  if (escolha === 'dino') minigameInstance.value = new DinoEngine(canvasRef.value);
  
  estadoCena.value = 'MINIJOGO';
};

const handleInput = (e) => {
  if (estadoCena.value === 'JOGANDO') {
    gameInstance.value?.processInput(e.key);
  } else if (estadoCena.value === 'TRANSICAO') {
    handleMenuInput(e.key);
  }
};

const handleMenuInput = (key) => {
  const numOpcoes = 3;
  if (key === 'ArrowUp') {
    gameInstance.value.fase_selecionada = (gameInstance.value.fase_selecionada - 1 + numOpcoes) % numOpcoes;
  }
  if (key === 'ArrowDown') {
    gameInstance.value.fase_selecionada = (gameInstance.value.fase_selecionada + 1) % numOpcoes;
  }
  if (key === 'Enter') {
    if (gameInstance.value.fase_selecionada === 2) {
      iniciarMinijogoAleatorio();
    } else {
      const fases = ['fase1', 'fase2'];
      gameInstance.value.mudarFase(fases[gameInstance.value.fase_selecionada]);
      estadoCena.value = 'JOGANDO';
    }
  }
};

const onKeyDown = (e) => {
  teclasPressionadas[e.key] = true;
  handleInput(e);
};

const onKeyUp = (e) => {
  teclasPressionadas[e.key] = false;
};

onMounted(() => {
  console.log('🚀 Component mounted');
  console.log('📦 Canvas:', canvasRef.value);
  console.log('📦 CONSTANTES:', CONSTANTES);
  
  if (!canvasRef.value) {
    console.error('❌ Canvas não existe!');
    alert('Erro: Canvas não encontrado!');
    return;
  }
  
  try {
    gameInstance.value = new SnakeEngine(canvasRef.value, CONSTANTES);
    console.log('✅ SnakeEngine criado:', gameInstance.value);
    console.log('🐍 Cobra inicial:', gameInstance.value.cobra);
    console.log('🍎 Alimento inicial:', gameInstance.value.alimento_pos);
    
    window.addEventListener('keydown', onKeyDown);
    window.addEventListener('keyup', onKeyUp);
    
    requestAnimationFrame(gameLoop);
    console.log('🎬 Game loop iniciado');
  } catch (error) {
    console.error('❌ Erro ao criar jogo:', error);
    alert('Erro ao iniciar jogo: ' + error.message);
  }
});

onUnmounted(() => {
  window.removeEventListener('keydown', onKeyDown);
  window.removeEventListener('keyup', onKeyUp);
  console.log('🛑 Component unmounted');
});
</script>

<template>
  <div class="view-wrapper">
    <div class="game-header">
      <button @click="router.push('/welcome')" class="back-btn">← Sair</button>
      <div class="stats">
        <span>🍎 Pontos: {{ pontuacao }}</span>
        <span>🔥 Calorias: {{ calorias }}</span>
        <span>🌍 Fase: {{ faseAtual }}</span>
      </div>
    </div>

    <div class="canvas-container">
      <canvas ref="canvasRef" :width="800" :height="600"></canvas>
      
      <div v-if="estadoCena === 'TRANSICAO'" class="menu-overlay">
        <h3>Fase Concluída! 🌟</h3>
        <p>Escolhe o próximo desafio:</p>
        <ul class="menu-list">
          <li :class="{ active: gameInstance?.fase_selecionada === 0 }">Continuar: Floresta</li>
          <li :class="{ active: gameInstance?.fase_selecionada === 1 }">Mudar: Deserto</li>
          <li :class="{ active: gameInstance?.fase_selecionada === 2 }">🎲 Minijogo Aleatório</li>
        </ul>
        <span class="hint">Usa as setas e prime Enter</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.view-wrapper {
  display: flex; flex-direction: column; align-items: center;
  min-height: 100vh; background: #0f172a; padding: 20px;
}
.game-header {
  width: 800px; display: flex; justify-content: space-between;
  margin-bottom: 10px; color: white; font-family: 'Inter', sans-serif;
}
.stats {
  display: flex; gap: 20px; font-size: 1.1rem; font-weight: 600;
}
.back-btn { 
  background: #334155; border: none; color: white; 
  padding: 8px 16px; border-radius: 8px; cursor: pointer;
  transition: background 0.2s;
}
.back-btn:hover {
  background: #475569;
}
.canvas-container { 
  position: relative; border: 4px solid #334155; 
  border-radius: 12px; overflow: hidden; 
}

.menu-overlay { 
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(15, 23, 42, 0.9); display: flex; flex-direction: column;
  align-items: center; justify-content: center; color: white; text-align: center;
}
.menu-list { list-style: none; padding: 0; margin: 20px 0; }
.menu-list li { 
  padding: 15px 30px; font-size: 1.2rem; transition: 0.2s; 
  border-radius: 10px; color: #94a3b8;
}
.menu-list li.active { 
  background: #47baac; color: white; transform: scale(1.1); 
}
.hint { font-size: 0.8rem; opacity: 0.6; margin-top: 10px; }
</style>