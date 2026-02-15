<template>
  <div class="snacke-game">
    <!-- Menu inicial -->
    <div v-if="gameState.gamePhase === 'menu'" class="game-menu">
      <div class="menu-content">
        <h1 class="game-title">🐍 Snack-e</h1>
        <p class="game-subtitle">A aventura alimentar da cobra saudável!</p>
        
        <div class="game-stats" v-if="gameState.day > 1">
          <h3>Progresso Atual</h3>
          <p>📅 Dia {{ gameState.day }}</p>
          <p>🍎 {{ discoveredFoodsCount }}/{{ totalFoodsCount }} alimentos descobertos</p>
        </div>

        <div class="menu-buttons">
          <button @click="startNewGame" class="btn-primary">
            {{ gameState.day === 1 ? 'Começar Aventura' : 'Continuar Jogo' }}
          </button>
          <button @click="showCatalog = true" class="btn-secondary" v-if="discoveredFoodsCount > 0">
            📖 Ver Caderneta
          </button>
          <button @click="gameState.gamePhase = 'instructions'" class="btn-secondary">
            ❓ Como Jogar
          </button>
        </div>
      </div>
    </div>

    <!-- Instruções -->
    <div v-if="gameState.gamePhase === 'instructions'" class="instructions">
      <div class="instructions-content">
        <h2>🎮 Como Jogar Snack-e</h2>
        <div class="instruction-section">
          <h3>🐍 Objetivo</h3>
          <p>Guia a Snack-e através de 5 refeições por dia, comendo a quantidade certa de alimentos para manter-se saudável!</p>
        </div>
        
        <div class="instruction-section">
          <h3>🎯 Refeições</h3>
          <ul>
            <li><strong>🌅 Pequeno-Almoço:</strong> 300-500 calorias</li>
            <li><strong>🍎 Lanche Manhã:</strong> 100-200 calorias</li>
            <li><strong>🍽️ Almoço:</strong> 400-700 calorias</li>
            <li><strong>🥪 Lanche Tarde:</strong> 150-250 calorias</li>
            <li><strong>🌙 Jantar:</strong> 350-600 calorias</li>
          </ul>
        </div>

        <div class="instruction-section">
          <h3>🏃 Treino</h3>
          <p>Entre refeições podes escolher treinar para queimar calorias extras e manter-te em forma!</p>
        </div>

        <div class="instruction-section">
          <h3>🏆 Sistema de Descobertas</h3>
          <p>Descobre novos alimentos e adiciona-os à tua caderneta! Cada alimento tem informações nutricionais únicas.</p>
        </div>

        <button @click="gameState.gamePhase = 'menu'" class="btn-primary">Voltar</button>
      </div>
    </div>

    <!-- Jogo da cobra -->
    <div v-if="gameState.gamePhase === 'meal'" class="meal-phase">
      <div class="meal-header">
        <h2>{{ getCurrentMeal().icon }} {{ getCurrentMeal().name }}</h2>
        <p>{{ getCurrentMeal().description }}</p>
        <div class="day-info">Dia {{ gameState.day }} - Refeição {{ gameState.currentMeal + 1 }}/5</div>
      </div>
      
      <canvas 
        ref="gameCanvas" 
        :width="800" 
        :height="600"
        @keydown="handleCanvasKeydown"
        tabindex="0"
      ></canvas>
      
      <div class="meal-controls">
        <button @click="startMeal" :disabled="mealInProgress" class="btn-primary">
          {{ mealInProgress ? 'Jogando...' : 'Começar Refeição' }}
        </button>
      </div>
    </div>

    <!-- Escolha entre treino e próxima refeição -->
    <div v-if="gameState.gamePhase === 'choice'" class="choice-phase">
      <div class="choice-content">
        <h2>🤔 O que queres fazer agora?</h2>
        
        <div v-if="lastMealResult" class="meal-result">
          <div :class="['result-message', { success: lastMealResult.success }]">
            {{ lastMealResult.message }}
          </div>
          <div class="calories-consumed">
            Consumiste {{ lastMealResult.caloriesConsumed }} calorias
          </div>
          <div v-if="lastMealResult.newFoodsDiscovered.length > 0" class="new-foods">
            🎉 Novos alimentos descobertos: {{ lastMealResult.newFoodsDiscovered.length }}
          </div>
        </div>

        <div class="choice-buttons">
          <div class="choice-option" @click="chooseTraining">
            <div class="option-icon">🏃‍♂️</div>
            <h3>Treinar</h3>
            <p>Faz exercício para queimar calorias e manter-te em forma!</p>
          </div>
          
          <div class="choice-option" @click="skipToNextMeal">
            <div class="option-icon">⏭️</div>
            <h3>Próxima Refeição</h3>
            <p>Continua para a próxima refeição do dia.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Seleção de treino -->
    <div v-if="gameState.gamePhase === 'training-select'" class="training-select">
      <div class="training-content">
        <h2>🏋️ Escolhe o teu treino:</h2>
        
        <div class="training-options">
          <div class="training-option" @click="startTraining('balance')">
            <div class="option-icon">⚖️</div>
            <h3>Jogo do Equilíbrio</h3>
            <p>Mantém o equilíbrio para queimar calorias!</p>
            <div class="calories-burn">~150 cal</div>
          </div>
          
          <div class="training-option" @click="startTraining('race')">
            <div class="option-icon">🏃</div>
            <h3>Corrida</h3>
            <p>Prima as setas rapidamente para chegar à meta!</p>
            <div class="calories-burn">~200 cal</div>
          </div>
          
          <div class="training-option" @click="startTraining('dinosaur')">
            <div class="option-icon">🦕</div>
            <h3>Dinossauro</h3>
            <p>Salta os obstáculos como um dinossauro!</p>
            <div class="calories-burn">~180 cal</div>
          </div>
        </div>

        <button @click="gameState.gamePhase = 'choice'" class="btn-secondary">Voltar</button>
      </div>
    </div>

    <!-- Treino ativo -->
    <div v-if="gameState.gamePhase === 'training'" class="training-phase">
      <div class="training-header">
        <h2>🏋️ {{ getTrainingTitle() }}</h2>
      </div>
      
      <canvas 
        ref="trainingCanvas" 
        :width="800" 
        :height="600"
        @keydown="handleCanvasKeydown"
        tabindex="0"
      ></canvas>
    </div>

    <!-- Final do dia -->
    <div v-if="gameState.gamePhase === 'sleep'" class="sleep-phase">
      <div class="sleep-content">
        <h2>🌙 Fim do Dia {{ gameState.day }}</h2>
        <p>A Snack-e vai dormir... 😴</p>
        
        <div class="day-summary">
          <h3>📊 Resumo do Dia</h3>
          <p>🍎 Alimentos descobertos hoje: {{ todayDiscoveredFoods }}</p>
          <p>📖 Total na caderneta: {{ discoveredFoodsCount }}/{{ totalFoodsCount }}</p>
        </div>

        <div class="sleep-buttons">
          <button @click="startNewDay" class="btn-primary">🌅 Novo Dia</button>
          <button @click="exitGame" class="btn-secondary">🚪 Sair</button>
        </div>
      </div>
    </div>

    <!-- Catálogo de alimentos - FORA de qualquer outra div, com z-index máximo -->
    <Teleport to="body">
      <div v-if="showCatalog" class="catalog-overlay" @click="closeCatalog">
        <div class="catalog-wrapper" @click.stop>
          <div class="catalog-header-bar">
            <h2>📖 Caderneta de Alimentos</h2>
            <button @click="closeCatalog" class="close-catalog-btn">✕ Fechar</button>
          </div>
          <div class="catalog-content">
            <FoodCatalog :discoveredFoods="gameState.discoveredFoods" />
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Toast de descoberta de alimento -->
    <FoodDiscoveryToast
      v-if="discoveryToast"
      :food="discoveryToast"
      @close="discoveryToast = null"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { SnakeGame } from '../games/SnakeGame'
import { BalanceGame } from '../games/BalanceGame'
import { RaceGame } from '../games/RaceGame'
import { SnakeJumpGame } from '../games/SnakeJumpGame'
import { GameManager } from '../games/GameManager'
import { loadMealsData } from '../games/snakeTypes'
import type { GameState, MealResult, Food, Meal, MealData } from '../games/snakeTypes'
import type { GameResult, GameConfig } from '../games/types'
import FoodCatalog from './FoodCatalog.vue'
import FoodDiscoveryToast from './FoodDiscoveryToast.vue'

// Dados das refeições carregados
let mealsData: MealData = {}

// Estado do jogo
const gameState = ref<GameState>({
  day: 1,
  currentMeal: 0,
  mealNames: ['pequeno_almoco', 'lanche_manha', 'almoco', 'lanche_tarde', 'jantar'],
  calories: 300, // IMPORTANTE: Começar com 300 calorias (CALORIAS_INICIAL)
  discoveredFoods: new Set<string>(),
  gamePhase: 'menu'
})

// Refs dos componentes
const gameCanvas = ref<HTMLCanvasElement>()
const trainingCanvas = ref<HTMLCanvasElement>()

// Estado da UI
const showCatalog = ref(false)
const mealInProgress = ref(false)
const discoveryToast = ref<Food | null>(null)
const lastMealResult = ref<MealResult | null>(null)
const currentTrainingGame = ref<string>('')
const todayDiscoveredFoods = ref(0)

// Instâncias dos jogos
let snakeGame: SnakeGame | null = null
let currentTrainingGameInstance: any = null

// Função para limpar TODOS os jogos ativos
const cleanupAllGames = () => {
  if (snakeGame) {
    snakeGame.cleanup()
    snakeGame = null
  }
  if (currentTrainingGameInstance) {
    currentTrainingGameInstance.cleanup()
    currentTrainingGameInstance = null
  }
  mealInProgress.value = false
}

// Computed properties
const discoveredFoodsCount = computed(() => gameState.value.discoveredFoods.size)

const totalFoodsCount = computed(() => {
  let count = 0
  Object.values(mealsData).forEach(meal => {
    count += meal.foods.length
  })
  return count
})

const getCurrentMeal = (): Meal => {
  const mealKey = gameState.value.mealNames[gameState.value.currentMeal]
  return mealsData[mealKey]
}

const getTrainingTitle = (): string => {
  const titles = {
    balance: 'Jogo do Equilíbrio',
    race: 'Corrida',
    dinosaur: 'Dinossauro'
  }
  return titles[currentTrainingGame.value as keyof typeof titles] || 'Treino'
}

// Métodos do jogo
const startNewGame = async () => {
  // Limpar qualquer jogo anterior antes de começar
  cleanupAllGames()
  
  gameState.value.gamePhase = 'meal'
  await nextTick()
  initializeSnakeGame()
}

const initializeSnakeGame = () => {
  if (!gameCanvas.value) return

  gameCanvas.value.focus()
  
  if (snakeGame) {
    snakeGame.cleanup()
  }

  snakeGame = new SnakeGame(gameCanvas.value, mealsData)
  
  // IMPORTANTE: Definir calorias iniciais do gameState (persistentes)
  snakeGame.setInitialCalories(gameState.value.calories)
  
  snakeGame.setCallbacks(
    (result: MealResult) => handleMealEnd(result),
    (food: Food) => handleFoodDiscovery(food)
  )
}

const startMeal = async () => {
  if (!snakeGame || mealInProgress.value) return

  mealInProgress.value = true
  
  try {
    const result = await snakeGame.startMeal()
    handleMealEnd(result)
  } catch (error) {
    console.error('Erro durante a refeição:', error)
    mealInProgress.value = false
  }
}

const handleMealEnd = (result: MealResult) => {
  mealInProgress.value = false
  lastMealResult.value = result
  gameState.value.lastMealResult = result

  // IMPORTANTE: Verificar se deve resetar ao menu (Game Over)
  if (result.resetToMenu) {
    // LIMPAR TODOS OS JOGOS antes de resetar
    cleanupAllGames()
    
    // Resetar tudo para o início
    gameState.value.day = 1
    gameState.value.currentMeal = 0
    gameState.value.calories = 300
    gameState.value.gamePhase = 'menu'
    
    return
  }

  // IMPORTANTE: Atualizar calorias do gameState com o resultado da refeição
  gameState.value.calories = result.caloriesConsumed

  // Se é a última refeição do dia, ir para dormir
  if (gameState.value.currentMeal === gameState.value.mealNames.length - 1) {
    // Limpar jogo da cobra quando termina o dia
    if (snakeGame) {
      snakeGame.cleanup()
      snakeGame = null
    }
    gameState.value.gamePhase = 'sleep'
  } else {
    // Senão, mostrar escolhas
    gameState.value.gamePhase = 'choice'
  }
}

const handleFoodDiscovery = (food: Food) => {
  if (!gameState.value.discoveredFoods.has(food.id)) {
    gameState.value.discoveredFoods.add(food.id)
    discoveryToast.value = food
    todayDiscoveredFoods.value++
  }
}

const chooseTraining = () => {
  gameState.value.gamePhase = 'training-select'
}

const skipToNextMeal = () => {
  nextMeal()
}

const startTraining = async (trainingType: string) => {
  currentTrainingGame.value = trainingType
  gameState.value.gamePhase = 'training'
  
  await nextTick()
  
  if (!trainingCanvas.value) return

  trainingCanvas.value.focus()

  const config: GameConfig = {
    targetCalories: 1500,
    difficulty: 1,
    canvasWidth: 800,
    canvasHeight: 600,
    calories: gameState.value.calories  // IMPORTANTE: Passar calorias atuais para o treino!
  }

  // Limpar jogo anterior
  if (currentTrainingGameInstance) {
    currentTrainingGameInstance.cleanup()
  }

  // Criar novo jogo baseado no tipo
  switch (trainingType) {
    case 'balance':
      currentTrainingGameInstance = new BalanceGame(trainingCanvas.value, config)
      break
    case 'race':
      currentTrainingGameInstance = new RaceGame(trainingCanvas.value, config)
      break
    case 'dinosaur':
      currentTrainingGameInstance = new SnakeJumpGame(trainingCanvas.value, config)
      break
  }

  if (currentTrainingGameInstance) {
    try {
      const result = await currentTrainingGameInstance.start()
      handleTrainingEnd(result)
    } catch (error) {
      console.error('Erro durante o treino:', error)
      gameState.value.gamePhase = 'choice'
    }
  }
}

const handleTrainingEnd = (result: GameResult) => {
  // Limpar jogo de treino
  if (currentTrainingGameInstance) {
    currentTrainingGameInstance.cleanup()
    currentTrainingGameInstance = null
  }

  // Subtrair calorias queimadas se teve sucesso
  if (result.success && result.caloriesLost) {
    gameState.value.calories = Math.max(0, gameState.value.calories - result.caloriesLost)
  }

  // Voltar para escolhas
  gameState.value.gamePhase = 'choice'
}

const nextMeal = () => {
  gameState.value.currentMeal++
  
  if (gameState.value.currentMeal >= gameState.value.mealNames.length) {
    // Fim do dia
    if (snakeGame) {
      snakeGame.cleanup()
      snakeGame = null
    }
    gameState.value.gamePhase = 'sleep'
  } else {
    // Próxima refeição - calorias já estão persistidas no gameState
    gameState.value.gamePhase = 'meal'
    nextTick(() => {
      if (snakeGame) {
        snakeGame.cleanup()
        snakeGame = null
      }
      initializeSnakeGame()
    })
  }
}

const startNewDay = () => {
  // Limpar jogos antes de começar novo dia
  cleanupAllGames()
  
  gameState.value.day++
  gameState.value.currentMeal = 0
  // IMPORTANTE: Manter as calorias do dia anterior como ponto de partida
  // OU resetar para 300 se preferir começar do zero cada dia
  // gameState.value.calories = 300  // <- Descomentar para resetar calorias a cada dia
  gameState.value.gamePhase = 'meal'
  todayDiscoveredFoods.value = 0
  nextTick(() => initializeSnakeGame())
}

const exitGame = () => {
  // Limpar todos os jogos antes de sair
  cleanupAllGames()
  
  // Salvar progresso no localStorage
  localStorage.setItem('snacke-progress', JSON.stringify({
    day: gameState.value.day,
    calories: gameState.value.calories, // IMPORTANTE: Salvar calorias atuais
    discoveredFoods: Array.from(gameState.value.discoveredFoods)
  }))
  
  gameState.value.gamePhase = 'menu'
}

const handleCanvasKeydown = (e: KeyboardEvent) => {
  // Prevenir scroll da página quando usar setas
  if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
    e.preventDefault()
  }
}

// Carregar progresso salvo
const loadSavedProgress = () => {
  const saved = localStorage.getItem('snacke-progress')
  if (saved) {
    try {
      const progress = JSON.parse(saved)
      gameState.value.day = progress.day || 1
      gameState.value.calories = progress.calories || 300 // IMPORTANTE: Carregar calorias salvas
      gameState.value.discoveredFoods = new Set(progress.discoveredFoods || [])
    } catch (error) {
      console.warn('Erro ao carregar progresso salvo:', error)
    }
  }
}

// Função para fechar o catálogo
const closeCatalog = () => {
  showCatalog.value = false
}

// Função para abrir o catálogo
const openCatalog = () => {
  console.log('Abrindo catálogo...') // Debug
  showCatalog.value = true
  console.log('showCatalog:', showCatalog.value) // Debug
}

// Função de teste
const testClick = () => {
  alert('Botão de teste clicado!')
}

// Lifecycle hooks
onMounted(async () => {
  // Carregar dados das refeições com alimentos completos
  mealsData = await loadMealsData()
  loadSavedProgress()
})

onUnmounted(() => {
  // Usar a função de cleanup global ao desmontar o componente
  cleanupAllGames()
})
</script>

<style scoped>
.snacke-game {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  overflow-y: auto;
}

/* Menu inicial */
.game-menu {
  text-align: center;
  padding: 40px;
}

.game-title {
  font-size: 4rem;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.game-subtitle {
  font-size: 1.5rem;
  margin-bottom: 30px;
  opacity: 0.9;
}

.game-stats {
  background: rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
}

.menu-buttons {
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: center;
}

/* Instruções */
.instructions {
  max-width: 600px;
  padding: 40px;
}

.instructions-content {
  background: rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 30px;
}

.instruction-section {
  margin-bottom: 25px;
}

.instruction-section h3 {
  margin-bottom: 10px;
  color: #FFD700;
}

.instruction-section ul {
  list-style: none;
  padding: 0;
}

.instruction-section li {
  padding: 5px 0;
  margin-left: 20px;
}

/* Fase da refeição */
.meal-phase {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 20px;
}

.meal-header {
  text-align: center;
  background: rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 20px;
  min-width: 300px;
}

.meal-header h2 {
  margin: 0 0 10px 0;
  font-size: 2rem;
}

.day-info {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-top: 10px;
}

canvas {
  border: 3px solid rgba(255,255,255,0.3);
  border-radius: 8px;
  background: white;
}

.meal-controls {
  display: flex;
  gap: 15px;
}

/* Fase de escolha */
.choice-phase {
  max-width: 600px;
  padding: 40px;
}

.choice-content {
  background: rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 30px;
  text-align: center;
}

.meal-result {
  margin-bottom: 30px;
  padding: 20px;
  border-radius: 12px;
  background: rgba(255,255,255,0.1);
}

.result-message {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.result-message.success {
  color: #2ECC71;
}

.choice-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.choice-option {
  background: rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 25px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.choice-option:hover {
  background: rgba(255,255,255,0.2);
  transform: translateY(-2px);
}

.option-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

/* Seleção de treino */
.training-select {
  max-width: 800px;
  padding: 40px;
}

.training-content {
  background: rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 30px;
  text-align: center;
}

.training-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.training-option {
  background: rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.training-option:hover {
  background: rgba(255,255,255,0.2);
  transform: translateY(-2px);
}

.calories-burn {
  color: #FFD700;
  font-weight: bold;
  margin-top: 10px;
}

/* Fase de treino */
.training-phase {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 20px;
}

.training-header {
  text-align: center;
  background: rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 20px;
}

/* Fase do sono */
.sleep-phase {
  max-width: 500px;
  padding: 40px;
}

.sleep-content {
  background: rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 30px;
  text-align: center;
}

.day-summary {
  background: rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
}

.sleep-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}

/* Catálogo */
.catalog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.8);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  backdrop-filter: blur(5px);
}

.catalog-wrapper {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 10000;
}

.catalog-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255,255,255,1);
  border-radius: 12px;
  padding: 10px 20px;
}

.catalog-content {
  background: white;
  border-radius: 16px;
  padding: 20px;
  overflow-y: auto;
  max-height: calc(90vh - 60px);
}

.close-catalog-btn {
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 20px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  z-index: 10;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  transition: all 0.2s;
}

.close-catalog-btn:hover {
  background: #c0392b;
  transform: scale(1.05);
}

.close-catalog-btn:active {
  transform: scale(0.95);
}

/* Botões */
.btn-primary {
  background: linear-gradient(135deg, #2ecc71, #27ae60);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 200px;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(46, 204, 113, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: rgba(255,255,255,0.2);
  color: white;
  border: 2px solid rgba(255,255,255,0.3);
  padding: 12px 24px;
  border-radius: 20px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: rgba(255,255,255,0.3);
  border-color: rgba(255,255,255,0.5);
}

/* Responsividade */
@media (max-width: 768px) {
  .game-title {
    font-size: 3rem;
  }
  
  .choice-buttons {
    grid-template-columns: 1fr;
  }
  
  .training-options {
    grid-template-columns: 1fr;
  }
  
  canvas {
    width: 100%;
    max-width: 400px;
    height: auto;
  }
}
</style>