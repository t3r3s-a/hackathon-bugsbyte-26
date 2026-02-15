<template>
  <div class="game-container">
    <!-- Menu de Seleção -->
    <GameMenu
      v-if="currentView === 'menu'"
      :calories="calories"
      :show-calories="showCalories"
      @select-game="handleGameSelect"
    />

    <!-- Canvas do Jogo -->
    <div v-else-if="currentView === 'playing'" class="game-view">
      <div class="game-header">
        <button @click="returnToMenu" class="back-button">
          ← Voltar ao Menu
        </button>
        <div v-if="showCalories" class="header-calories">
          🔥 {{ calories }} calorias
        </div>
      </div>
      
      <GameCanvas
        ref="gameCanvasRef"
        :width="canvasWidth"
        :height="canvasHeight"
        :calories="calories"
        :game-type="selectedGameType"
        @game-end="handleGameEnd"
        @restart="handleRestart"
        @menu="returnToMenu"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import GameMenu from './GameMenu.vue';
import GameCanvas from './GameCanvas.vue';
import type { GameType, GameResult } from '../games/types';

interface Props {
  initialCalories?: number;
  canvasWidth?: number;
  canvasHeight?: number;
  showCalories?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  initialCalories: 1000,
  canvasWidth: 800,
  canvasHeight: 600,
  showCalories: true
});

const emit = defineEmits<{
  gameEnd: [result: GameResult];
  caloriesChange: [calories: number];
}>();

type ViewType = 'menu' | 'playing';

const currentView = ref<ViewType>('menu');
const selectedGameType = ref<GameType | null>(null);
const calories = ref(props.initialCalories);
const gameCanvasRef = ref<InstanceType<typeof GameCanvas> | null>(null);

function handleGameSelect(gameType: GameType) {
  selectedGameType.value = gameType;
  currentView.value = 'playing';
}

function handleGameEnd(result: GameResult) {
  if (result.success && result.caloriesLost) {
    calories.value = Math.max(0, calories.value - result.caloriesLost);
    emit('caloriesChange', calories.value);
  }
  emit('gameEnd', result);
}

function handleRestart() {
  if (selectedGameType.value && gameCanvasRef.value) {
    gameCanvasRef.value.startGame(selectedGameType.value);
  }
}

function returnToMenu() {
  if (gameCanvasRef.value) {
    gameCanvasRef.value.stopGame();
  }
  currentView.value = 'menu';
  selectedGameType.value = null;
}

// Expor métodos para o componente pai (se necessário)
defineExpose({
  returnToMenu,
  getCalories: () => calories.value,
  setCalories: (value: number) => { calories.value = value; }
});
</script>

<style scoped>
.game-container {
  width: 100%;
  min-height: 100vh;
}

.game-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.game-header {
  width: 100%;
  max-width: 800px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.back-button {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: white;
  background-color: rgba(255, 255, 255, 0.2);
  border: 2px solid white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.back-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: translateX(-5px);
}

.header-calories {
  padding: 0.75rem 1.5rem;
  font-size: 1.2rem;
  font-weight: bold;
  color: white;
  background-color: rgba(245, 158, 11, 0.9);
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}
</style>
