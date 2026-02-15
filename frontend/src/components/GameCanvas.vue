<template>
  <div class="game-canvas-container">
    <canvas 
      ref="gameCanvas" 
      :width="width" 
      :height="height"
      class="game-canvas"
    />
    
    <!-- Overlay para estados do jogo -->
    <div v-if="showOverlay" class="game-overlay">
      <div class="overlay-content">
        <h2 v-if="gameState === GameState.VICTORY" class="victory-title">
          🎉 Vitória!
        </h2>
        <h2 v-else-if="gameState === GameState.GAME_OVER" class="game-over-title">
          😢 Game Over
        </h2>
        
        <p v-if="result" class="result-text">
          {{ result.success ? 'Conseguiste!' : 'Tenta outra vez!' }}
          <br>
          <span v-if="result.success" class="calories-lost">
            Calorias perdidas: {{ result.caloriesLost }}
          </span>
        </p>
        
        <button @click="$emit('restart')" class="restart-button">
          Jogar Novamente
        </button>
        <button @click="$emit('menu')" class="menu-button">
          Menu Principal
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import { GameManager } from '../games/GameManager';
import { GameState } from '../games/types';
import type { GameConfig, GameResult, GameType } from '../games/types';

interface Props {
  width?: number;
  height?: number;
  calories?: number;
  gameType: GameType | null;
}

const props = withDefaults(defineProps<Props>(), {
  width: 800,
  height: 600,
  calories: 1000
});

const emit = defineEmits<{
  gameEnd: [result: GameResult];
  restart: [];
  menu: [];
}>();

const gameCanvas = ref<HTMLCanvasElement | null>(null);
const gameManager = ref<GameManager | null>(null);
const gameState = ref<GameState>(GameState.PLAYING);
const result = ref<GameResult | null>(null);
const showOverlay = ref(false);

onMounted(() => {
  if (gameCanvas.value) {
    const config: GameConfig = {
      targetCalories: props.calories,
      difficulty: 1,
      calories: props.calories,
      canvasWidth: props.width,
      canvasHeight: props.height
    };
    
    gameManager.value = new GameManager(gameCanvas.value, config);
    
    if (props.gameType) {
      startGame(props.gameType);
    }
  }
});

onBeforeUnmount(() => {
  if (gameManager.value) {
    gameManager.value.cleanup();
  }
});

// Observar mudanças no tipo de jogo
watch(() => props.gameType, (newGameType) => {
  if (newGameType && gameManager.value) {
    startGame(newGameType);
  }
});

// Observar mudanças nas calorias
watch(() => props.calories, (newCalories) => {
  if (gameManager.value) {
    gameManager.value.updateConfig({ 
      targetCalories: newCalories,
      difficulty: 1,
      calories: newCalories 
    });
  }
});

async function startGame(type: GameType) {
  if (!gameManager.value) return;
  
  showOverlay.value = false;
  result.value = null;
  gameState.value = GameState.PLAYING;
  
  try {
    const gameResult = await gameManager.value.startGame(type);
    result.value = gameResult;
    gameState.value = gameResult.success ? GameState.VICTORY : GameState.GAME_OVER;
    showOverlay.value = true;
    emit('gameEnd', gameResult);
  } catch (error) {
    console.error('Erro ao iniciar o jogo:', error);
  }
}

// Expor métodos para o componente pai
defineExpose({
  startGame,
  stopGame: () => gameManager.value?.stopGame()
});
</script>

<style scoped>
.game-canvas-container {
  position: relative;
  display: inline-block;
  border: 3px solid #8B4513;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.game-canvas {
  display: block;
  background-color: #87CEEB;
}

.game-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.overlay-content {
  text-align: center;
  color: white;
  padding: 2rem;
}

.victory-title {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #4ade80;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.game-over-title {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #ef4444;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.result-text {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.calories-lost {
  display: block;
  margin-top: 0.5rem;
  color: #fbbf24;
  font-weight: bold;
}

.restart-button,
.menu-button {
  padding: 0.75rem 2rem;
  margin: 0.5rem;
  font-size: 1.1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.restart-button {
  background-color: #4ade80;
  color: #1a1a1a;
}

.restart-button:hover {
  background-color: #22c55e;
  transform: scale(1.05);
}

.menu-button {
  background-color: #60a5fa;
  color: white;
}

.menu-button:hover {
  background-color: #3b82f6;
  transform: scale(1.05);
}
</style>
