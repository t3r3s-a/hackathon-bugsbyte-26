<template>
  <Teleport to="body">
    <div class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="close-btn" @click="closeModal" aria-label="Fechar">✕</button>
        
        <div class="food-header">
          <div class="food-image">
            <img 
              :src="`/src/assets/games/foods/${food.sprite}`" 
              :alt="food.name"
              @error="handleImageError"
            />
          </div>
          <div class="food-title">
            <h2>{{ food.name }}</h2>
            <div class="food-category">{{ getCategoryLabel(food.category) }}</div>
            <div class="calories-badge">{{ food.calories }} cal</div>
          </div>
        </div>

        <div class="food-description">
          <p>{{ food.discovery_message }}</p>
        </div>

        <div class="nutrition-stats">
          <h3>Informação Nutricional</h3>
          
          <div class="stat-row">
            <div class="stat-label">
              <span class="icon">💪</span>
              Proteína
            </div>
            <div class="stat-bars">
              <div 
                v-for="i in 5" 
                :key="`protein-${i}`"
                :class="['stat-bar', { filled: i <= food.protein }]"
              ></div>
            </div>
            <div class="stat-value">{{ food.protein }}/5</div>
          </div>

          <div class="stat-row">
            <div class="stat-label">
              <span class="icon">💧</span>
              Hidratação
            </div>
            <div class="stat-bars">
              <div 
                v-for="i in 5" 
                :key="`hydration-${i}`"
                :class="['stat-bar', { filled: i <= food.hydration }]"
              ></div>
            </div>
            <div class="stat-value">{{ food.hydration }}/5</div>
          </div>

          <div class="stat-row">
            <div class="stat-label">
              <span class="icon">🌟</span>
              Vitaminas
            </div>
            <div class="stat-bars">
              <div 
                v-for="i in 5" 
                :key="`vitamins-${i}`"
                :class="['stat-bar', { filled: i <= food.vitamins }]"
              ></div>
            </div>
            <div class="stat-value">{{ food.vitamins }}/5</div>
          </div>
        </div>

        <div class="food-rating">
          <h3>Classificação Nutricional</h3>
          <div class="rating-display">
            <div class="stars">
              <span 
                v-for="i in 5" 
                :key="`star-${i}`"
                :class="['star', { filled: i <= food.rating }]"
              >
                ⭐
              </span>
            </div>
            <span class="rating-text">{{ food.rating }}/5</span>
          </div>
          <div class="health-badge" :class="food.health_color">
            {{ getHealthLabel(food.health_color) }}
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import type { Food } from '../games/snakeTypes'

interface Props {
  food: Food
}

const props = defineProps<Props>()

const emit = defineEmits<{
  close: []
}>()

const closeModal = () => {
  emit('close')
}

const getCategoryLabel = (category: string): string => {
  const labels: { [key: string]: string } = {
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

const getHealthLabel = (color: string): string => {
  switch (color) {
    case 'green': return 'Muito Saudável'
    case 'yellow': return 'Moderadamente Saudável'
    case 'orange': return 'Consumir com Moderação'
    default: return ''
  }
}

const handleImageError = (event: Event) => {
  const target = event.target as HTMLImageElement
  target.style.display = 'none'
}

// Fechar modal com ESC
const handleEscKey = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    closeModal()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscKey)
  document.body.style.overflow = 'hidden'
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscKey)
  document.body.style.overflow = 'auto'
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10001;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  animation: modalAppear 0.3s ease-out;
  z-index: 10002;
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(0, 0, 0, 0.1);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.2);
}

.food-header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 30px 30px 20px;
  border-bottom: 1px solid #ecf0f1;
}

.food-image {
  width: 80px;
  height: 80px;
  background: #f8f9fa;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.food-image img {
  width: 60px;
  height: 60px;
  object-fit: contain;
}

.food-title h2 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 24px;
}

.food-category {
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 8px;
}

.calories-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  display: inline-block;
}

.food-description {
  padding: 20px 30px;
  border-bottom: 1px solid #ecf0f1;
}

.food-description p {
  margin: 0;
  color: #2c3e50;
  line-height: 1.6;
  font-size: 16px;
}

.nutrition-stats {
  padding: 20px 30px;
  border-bottom: 1px solid #ecf0f1;
}

.nutrition-stats h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 18px;
}

.stat-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.stat-row:last-child {
  margin-bottom: 0;
}

.stat-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #2c3e50;
  min-width: 120px;
}

.stat-label .icon {
  font-size: 18px;
}

.stat-bars {
  display: flex;
  gap: 4px;
  flex: 1;
}

.stat-bar {
  width: 20px;
  height: 8px;
  background: #ecf0f1;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.stat-bar.filled {
  background: linear-gradient(90deg, #2ecc71, #27ae60);
}

.stat-value {
  font-weight: 600;
  color: #7f8c8d;
  min-width: 40px;
  text-align: right;
}

.food-rating {
  padding: 20px 30px;
  text-align: center;
}

.food-rating h3 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  font-size: 18px;
}

.rating-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 16px;
}

.stars {
  display: flex;
  gap: 4px;
}

.star {
  font-size: 24px;
  filter: grayscale(100%);
  transition: filter 0.2s;
}

.star.filled {
  filter: grayscale(0%);
}

.rating-text {
  font-weight: 600;
  color: #2c3e50;
  font-size: 18px;
}

.health-badge {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 14px;
}

.health-badge.green {
  background: #d5edda;
  color: #155724;
}

.health-badge.yellow {
  background: #fff3cd;
  color: #856404;
}

.health-badge.orange {
  background: #f8d7da;
  color: #721c24;
}

/* Responsividade */
@media (max-width: 600px) {
  .modal-content {
    margin: 0;
    border-radius: 16px 16px 0 0;
    max-height: 95vh;
  }
  
  .food-header {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }
  
  .stat-row {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
  
  .stat-label {
    min-width: auto;
    justify-content: center;
  }
  
  .stat-bars {
    justify-content: center;
    max-width: 200px;
  }
}
</style>
