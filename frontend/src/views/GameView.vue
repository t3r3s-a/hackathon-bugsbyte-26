<template>
  <div class="view-wrapper">
    <div class="decor-blob blob-1"></div>
    <div class="decor-blob blob-2"></div>
    <div class="decor-blob blob-3"></div>

    <button @click="router.push('/welcome')" class="back-floating-btn">
      ← Voltar
    </button>

    <!-- Menu de seleção de jogos -->
    <div v-if="!selectedGame" class="game-selection">
      <h1>🎮 Escolhe o teu Jogo</h1>
      <div class="game-options">
        <div class="game-option" @click="selectedGame = 'nutrium-snake'">
          <div class="game-icon">🐍</div>
          <h3>Nutrium Snake</h3>
          <p>O jogo clássico da cobra com alimentos nutritivos</p>
        </div>
        
        <div class="game-option" @click="selectedGame = 'snacke'">
          <div class="game-icon">🍎</div>
          <h3>Snack-e</h3>
          <p>A aventura alimentar da cobra através das 5 refeições do dia!</p>
        </div>
      </div>
    </div>

    <!-- Nutrium Snake original -->
    <div v-if="selectedGame === 'nutrium-snake'" class="game-wrapper">
      <div class="game-header">
        <h2>🐍 Nutrium Snake</h2>
        <button @click="selectedGame = null" class="change-game-btn">Mudar Jogo</button>
      </div>
      
      <GameContainer
        :initial-calories="userCalories"
        :canvas-width="800"
        :canvas-height="600"
        :show-calories="true"
        @game-end="handleGameEnd"
        @calories-change="handleCaloriesChange"
      />
    </div>

    <!-- Novo jogo Snack-e -->
    <div v-if="selectedGame === 'snacke'" class="game-wrapper">
      <div class="game-header">
        <h2>🍎 Snack-e</h2>
        <button @click="selectedGame = null" class="change-game-btn">Mudar Jogo</button>
      </div>
      
      <SnackeGame />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import GameContainer from "../components/GameContainer.vue";
import SnackeGame from "../components/SnackeGame.vue";

const router = useRouter();
const username = localStorage.getItem("usuario_logado") || "Explorador";
const userCalories = ref(1000);
const selectedGame = ref(null);

onMounted(() => {
  const savedCalories = localStorage.getItem("user_calories");
  if (savedCalories) {
    userCalories.value = parseInt(savedCalories);
  }
});

function handleGameEnd(result) {
  console.log('🎮 Jogo terminou:', result);
  
  if (result.success) {
    console.log(`🎉 Vitória ${username}! Perdeu ${result.caloriesLost} calorias`);
    
  } else {
    console.log('😢 Game Over! Tenta outra vez!');
  }
}

function handleCaloriesChange(newCalories) {
  userCalories.value = newCalories;
  localStorage.setItem("user_calories", newCalories.toString());
  console.log(`🔥 Calorias atuais: ${newCalories}`);
}
</script>

<style scoped>
.view-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f8fafc;
  font-family: 'Inter', sans-serif;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

/* Blobs decorativos (mantendo consistência com o design) */
.decor-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 0;
  opacity: 0.4;
  animation: move 20s infinite alternate;
}

.blob-1 { 
  width: 400px; 
  height: 400px; 
  background: #dcfce7; 
  top: -100px; 
  left: -100px; 
}

.blob-2 { 
  width: 300px; 
  height: 300px; 
  background: #47baac33; 
  bottom: -50px; 
  right: -50px; 
  animation-delay: -5s; 
}

.blob-3 { 
  width: 250px; 
  height: 250px; 
  background: #fef9c3; 
  top: 10%; 
  right: 5%; 
  animation-delay: -10s; 
}

@keyframes move {
  from { transform: translate(0, 0); }
  to { transform: translate(30px, 50px); }
}

.back-floating-btn {
  position: fixed;
  top: 30px;
  left: 30px;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid #47baac;
  border-radius: 12px;
  cursor: pointer;
  font-weight: bold;
  color: #47baac;
  transition: all 0.3s ease;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.back-floating-btn:hover {
  background: #47baac;
  color: white;
  transform: translateX(-5px);
  box-shadow: 0 8px 15px rgba(71, 186, 172, 0.3);
}

.game-selection {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 800px;
  width: 100%;
}

.game-selection h1 {
  font-size: 3rem;
  color: #2c3e50;
  margin-bottom: 40px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.game-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.game-option {
  background: white;
  border-radius: 20px;
  padding: 40px 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 3px solid transparent;
}

.game-option:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
  border-color: #47baac;
}

.game-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.game-option h3 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 15px;
}

.game-option p {
  color: #7f8c8d;
  font-size: 1.1rem;
  line-height: 1.6;
}

.game-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.game-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 2rem;
}

.change-game-btn {
  padding: 10px 20px;
  background: #47baac;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.change-game-btn:hover {
  background: #3a9688;
  transform: translateY(-2px);
}

.game-wrapper {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1000px;
}

/* Responsivo */
@media (max-width: 900px) {
  .view-wrapper {
    padding: 10px;
  }
  
  .back-floating-btn {
    top: 20px;
    left: 20px;
    padding: 10px 20px;
    font-size: 14px;
  }
  
  .game-selection h1 {
    font-size: 2.5rem;
  }
  
  .game-options {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .game-option {
    padding: 30px 20px;
  }
  
  .game-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
}
</style>