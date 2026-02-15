<template>
  <div class="food-catalog">
    <div class="catalog-header">
      <h2>📖 Caderneta de Alimentos</h2>
      <p>{{ discoveredCount }}/{{ totalFoodsCount }} alimentos descobertos</p>
      <div class="progress-bar">
        <div 
          class="progress-fill" 
          :style="{ width: `${(discoveredCount / totalFoodsCount) * 100}%` }"
        ></div>
      </div>
    </div>

    <div class="catalog-filters">
      <button 
        v-for="category in categories" 
        :key="category"
        :class="{ active: selectedCategory === category }"
        @click="selectedCategory = category"
        class="filter-btn"
      >
        {{ getCategoryLabel(category) }}
      </button>
    </div>

    <div class="catalog-grid">
      <div
        v-for="food in filteredFoods"
        :key="food.id"
        :class="['food-card', { discovered: isDiscovered(food.id), locked: !isDiscovered(food.id) }]"
        @click="selectFood(food)"
      >
        <div class="food-image">
          <img 
            v-if="isDiscovered(food.id)"
            :src="`/src/assets/games/foods/${food.sprite}`" 
            :alt="food.name"
            @error="handleImageError"
          />
          <div v-else class="locked-icon">🔒</div>
        </div>
        
        <div class="food-info">
          <h3>{{ isDiscovered(food.id) ? food.name : '???' }}</h3>
          <div v-if="isDiscovered(food.id)" class="food-category">
            {{ getCategoryLabel(food.category) }}
          </div>
          <div 
            v-if="isDiscovered(food.id)"
            class="health-indicator"
            :class="food.health_color"
          ></div>
        </div>
      </div>
    </div>

  </div>
  <!-- Modal de detalhes do alimento -->
  <FoodDetailModal
    v-if="selectedFood && isDiscovered(selectedFood.id)"
    :food="selectedFood"
    @close="selectedFood = null"
  />
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Food } from '../games/snakeTypes'
import FoodDetailModal from './FoodDetailModal.vue'
import foodsData from '../data/foods.json'

interface Props {
  discoveredFoods: Set<string>
}

const props = defineProps<Props>()

const selectedCategory = ref<string>('all')
const selectedFood = ref<Food | null>(null)

// Extrair todos os alimentos dos dados
const allFoods = computed(() => {
  // foods.json é um array direto de alimentos
  return foodsData.map(food => ({
    id: food.nome,
    name: food.nome,
    calories: food.energia_kcal,
    sprite: `${food.nome}.png`,
    health_color: food.cor as 'green' | 'yellow' | 'orange',
    category: getCategoryFromFood(food),
    // Calcular barras de nutrição (0-5)
    protein: calculateProteinBars(food.proteina_g),
    hydration: calculateHydrationBars(food.agua_g),
    vitamins: calculateVitaminBars(food.vitamina_c_mg, food.vitamina_a_ug),
    rating: getRatingFromColor(food.cor),
    discovery_message: food.descricao
  }))
})

const calculateProteinBars = (proteina: number): number => {
  // 0g = 0 barras, 30g+ = 5 barras
  if (proteina >= 30) return 5
  if (proteina >= 20) return 4
  if (proteina >= 10) return 3
  if (proteina >= 5) return 2
  if (proteina >= 1) return 1
  return 0
}

const calculateHydrationBars = (agua: number): number => {
  // 0g = 0 barras, 90g+ = 5 barras (baseado em % de água)
  if (agua >= 90) return 5
  if (agua >= 70) return 4
  if (agua >= 50) return 3
  if (agua >= 30) return 2
  if (agua >= 10) return 1
  return 0
}

const calculateVitaminBars = (vitC: number, vitA: number): number => {
  // Média ponderada de vitaminas C e A
  const scoreC = Math.min(5, Math.round(vitC / 20))
  const scoreA = Math.min(5, Math.round(vitA / 200))
  const average = Math.round((scoreC + scoreA) / 2)
  return Math.max(0, Math.min(5, average))
}

const getCategoryFromFood = (food: any): string => {
  // Determinar categoria baseada nas características do alimento
  const nome = food.nome.toLowerCase()
  
  if (nome.includes('maçã') || nome.includes('banana') || nome.includes('laranja') || 
      nome.includes('morango') || nome.includes('kiwi') || nome.includes('pera') ||
      nome.includes('framboesa') || nome.includes('abacate')) return 'fruta'
  
  if (nome.includes('leite') || nome.includes('iogurte') || nome.includes('queijo')) return 'laticinios'
  
  if (nome.includes('pão') || nome.includes('arroz') || nome.includes('massa') || 
      nome.includes('aveia') || nome.includes('cereal') || nome.includes('quinoa')) return 'cereais'
  
  if (nome.includes('frango') || nome.includes('bife') || nome.includes('peixe') || 
      nome.includes('salmão') || nome.includes('atum') || nome.includes('ovo') ||
      nome.includes('peru') || nome.includes('bacalhau') || nome.includes('camarão')) return 'proteina'
  
  if (nome.includes('brócolos') || nome.includes('espinafre') || nome.includes('alface') ||
      nome.includes('tomate') || nome.includes('cenoura') || nome.includes('cogumelo') ||
      nome.includes('berinjela') || nome.includes('curgete')) return 'vegetais'
  
  if (nome.includes('chocolate') || nome.includes('mel') || nome.includes('waffle') ||
      nome.includes('muffin') || nome.includes('xarope')) return 'doces'
  
  if (nome.includes('água') || nome.includes('café') || nome.includes('chá') || 
      nome.includes('sumo') || nome.includes('smoothie')) return 'bebida'
  
  return 'outros'
}

const getRatingFromColor = (cor: string): number => {
  const ratings: { [key: string]: number } = {
    'verde': 5,
    'amarelo': 3,
    'laranja': 2
  }
  return ratings[cor] || 3
}

const categories = computed(() => {
  const cats = new Set<string>(['all'])
  allFoods.value.forEach(food => {
    if (food.category) {
      cats.add(food.category)
    }
  })
  return Array.from(cats)
})

const filteredFoods = computed(() => {
  if (selectedCategory.value === 'all') {
    return allFoods.value
  }
  return allFoods.value.filter(food => food.category === selectedCategory.value)
})

const discoveredCount = computed(() => props.discoveredFoods.size)
const totalFoodsCount = computed(() => allFoods.value.length)

const isDiscovered = (foodId: string): boolean => {
  return props.discoveredFoods.has(foodId)
}

const selectFood = (food: Food) => {
  if (isDiscovered(food.id)) {
    selectedFood.value = food
  }
}

const getCategoryLabel = (category: string): string => {
  const labels: { [key: string]: string } = {
    all: 'Todos',
    cereais: '🌾 Cereais',
    laticinios: '🥛 Laticínios',
    fruta: '🍎 Frutas',
    doces: '🍪 Doces',
    proteina: '🍗 Proteínas',
    vegetais: '🥦 Vegetais',
    fritos: '🍟 Fritos',
    sandes: '🥪 Sandes',
    bebida: '🧃 Bebidas',
    sopa: '🥣 Sopas',
    fast_food: '🍕 Fast Food'
  }
  return labels[category] || category
}

const handleImageError = (event: Event) => {
  const target = event.target as HTMLImageElement
  target.style.display = 'none'
}
</script>

<style scoped>
.food-catalog {
  background-color: #f8f9fa;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.catalog-header {
  background-color: #f8f9fa;
  text-align: center;
  margin-bottom: 30px;
}

.catalog-header h2 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.catalog-header p {
  color: #7f8c8d;
  margin-bottom: 15px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #ecf0f1;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #2ecc71, #27ae60);
  transition: width 0.3s ease;
}

.catalog-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-bottom: 30px;
}

.filter-btn {
  padding: 8px 16px;
  border: 2px solid #ecf0f1;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
}

.filter-btn:hover {
  border-color: #3498db;
}

.filter-btn.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.catalog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.food-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
  cursor: pointer;
  border: 2px solid transparent;
}

.food-card.discovered:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  border-color: #3498db;
}

.food-card.locked {
  opacity: 0.6;
  cursor: not-allowed;
  background: #f8f9fa;
}

.food-image {
  width: 80px;
  height: 80px;
  margin: 0 auto 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 8px;
}

.food-image img {
  width: 60px;
  height: 60px;
  object-fit: contain;
}

.locked-icon {
  font-size: 32px;
  opacity: 0.5;
}

.food-info {
  text-align: center;
}

.food-info h3 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
}

.food-category {
  font-size: 12px;
  color: #7f8c8d;
  margin-bottom: 8px;
}

.health-indicator {
  width: 20px;
  height: 4px;
  margin: 0 auto;
  border-radius: 2px;
}

.health-indicator.green {
  background-color: #27ae60;
}

.health-indicator.yellow {
  background-color: #f1c40f;
}

.health-indicator.orange {
  background-color: #e67e22;
}

/* Responsividade */
@media (max-width: 768px) {
  .catalog-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }
  
  .food-card {
    padding: 12px;
  }
  
  .food-image {
    width: 60px;
    height: 60px;
  }
  
  .food-image img {
    width: 45px;
    height: 45px;
  }
}
</style>
