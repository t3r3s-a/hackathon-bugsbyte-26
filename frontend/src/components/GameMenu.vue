<template>
  <div class="game-menu">
    <div class="menu-container">
      <h1 class="menu-title">
        🐍 Jogos da Cobra
      </h1>
      
      <p class="menu-subtitle">
        Escolhe o teu jogo!
      </p>

      <div class="game-cards">
        <!-- Card do Jogo de Salto -->
        <div 
          class="game-card jump-card"
          @click="selectGame('jump')"
          :class="{ selected: selectedGame === 'jump' }"
        >
          <div class="card-icon">🦖</div>
          <h2 class="card-title">Cobra Saltadora</h2>
          <p class="card-description">
            Salta obstáculos com a cobra! 
            Use a barra de espaço para saltar.
          </p>
          <div class="card-difficulty">
            <span class="difficulty-label">Dificuldade:</span>
            <div class="difficulty-bars">
              <div class="bar filled"></div>
              <div class="bar filled"></div>
              <div class="bar"></div>
            </div>
          </div>
        </div>

        <!-- Card do Jogo de Equilíbrio -->
        <div 
          class="game-card balance-card"
          @click="selectGame('balance')"
          :class="{ selected: selectedGame === 'balance' }"
        >
          <div class="card-icon">⚖️</div>
          <h2 class="card-title">Equilíbrio</h2>
          <p class="card-description">
            Mantém a cobra equilibrada!
            Use as setas ← → para controlar.
          </p>
          <div class="card-difficulty">
            <span class="difficulty-label">Dificuldade:</span>
            <div class="difficulty-bars">
              <div class="bar filled"></div>
              <div class="bar filled"></div>
              <div class="bar filled"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Informação das Calorias -->
      <div v-if="showCalories" class="calories-info">
        <div class="calories-label">🔥 Calorias Atuais:</div>
        <div class="calories-value">{{ calories }}</div>
        <div class="segments-info">
          Segmentos da cobra: {{ numSegments }}
        </div>
      </div>

      <!-- Botão de Jogar -->
      <button 
        class="play-button"
        :disabled="!selectedGame"
        @click="startGame"
      >
        {{ selectedGame ? '▶️ Começar Jogo' : 'Escolhe um Jogo' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { GameType } from '../games/types';

interface Props {
  calories?: number;
  showCalories?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  calories: 1000,
  showCalories: true
});

const emit = defineEmits<{
  selectGame: [gameType: GameType];
}>();

const selectedGame = ref<GameType | null>(null);

const numSegments = computed(() => {
  return Math.max(1, Math.floor(props.calories / 100));
});

function selectGame(gameType: GameType) {
  selectedGame.value = gameType;
}

function startGame() {
  if (selectedGame.value) {
    emit('selectGame', selectedGame.value);
  }
}
</script>

<style scoped>
.game-menu {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.menu-container {
  max-width: 900px;
  width: 100%;
}

.menu-title {
  font-size: 3.5rem;
  text-align: center;
  color: white;
  margin-bottom: 0.5rem;
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
  animation: bounceIn 0.8s ease-out;
}

@keyframes bounceIn {
  0% {
    transform: scale(0.3);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.menu-subtitle {
  text-align: center;
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 3rem;
}

.game-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.game-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 3px solid transparent;
}

.game-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.2);
}

.game-card.selected {
  border-color: #4ade80;
  background: linear-gradient(to bottom, #f0fdf4, white);
}

.jump-card.selected {
  border-color: #f59e0b;
}

.balance-card.selected {
  border-color: #3b82f6;
}

.card-icon {
  font-size: 4rem;
  text-align: center;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.8rem;
  text-align: center;
  color: #1f2937;
  margin-bottom: 1rem;
}

.card-description {
  text-align: center;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  min-height: 3rem;
}

.card-difficulty {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.difficulty-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 600;
}

.difficulty-bars {
  display: flex;
  gap: 0.25rem;
}

.bar {
  width: 1.5rem;
  height: 0.5rem;
  background-color: #e5e7eb;
  border-radius: 2px;
}

.bar.filled {
  background-color: #f59e0b;
}

.calories-info {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.calories-label {
  font-size: 1.2rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.calories-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: #f59e0b;
  margin-bottom: 0.5rem;
}

.segments-info {
  font-size: 1rem;
  color: #9ca3af;
}

.play-button {
  width: 100%;
  padding: 1.25rem 2rem;
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.play-button:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
}

.play-button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

.play-button:active:not(:disabled) {
  transform: scale(0.98);
}
</style>
