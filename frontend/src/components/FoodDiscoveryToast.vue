<template>
  <Teleport to="body">
    <Transition name="toast">
      <div
        v-if="isVisible"
        class="food-discovery-toast"
        @click="close"
      >
        <div class="toast-content">
          <div class="food-icon">
            <img 
              :src="`/src/assets/games/foods/${food.sprite}`" 
              :alt="food.name"
              @error="handleImageError"
            />
          </div>
          <div class="food-info">
            <h3>🎉 Novo Alimento Descoberto!</h3>
            <h4>{{ food.name }}</h4>
            <p>{{ food.discovery_message }}</p>
            <div class="food-stats">
              <span class="calories">{{ food.calories }} cal</span>
              <span class="health-badge" :class="food.health_color">
                {{ getHealthLabel(food.health_color) }}
              </span>
            </div>
          </div>
          <button class="close-btn" @click="close" aria-label="Fechar">✕</button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { Food } from '../games/snakeTypes'

interface Props {
  food: Food
  duration?: number
}

const props = withDefaults(defineProps<Props>(), {
  duration: 5000
})

const emit = defineEmits<{
  close: []
}>()

const isVisible = ref(false)
let timeoutId: number | null = null

onMounted(() => {
  isVisible.value = true
  
  if (props.duration > 0) {
    timeoutId = setTimeout(() => {
      close()
    }, props.duration)
  }
})

onUnmounted(() => {
  if (timeoutId) {
    clearTimeout(timeoutId)
  }
})

const close = () => {
  isVisible.value = false
  setTimeout(() => {
    emit('close')
  }, 300) // Aguarda animação terminar
}

const getHealthLabel = (color: string): string => {
  switch (color) {
    case 'green': return 'Saudável'
    case 'yellow': return 'Moderado'
    case 'orange': return 'Ocasional'
    default: return ''
  }
}

const handleImageError = (event: Event) => {
  const target = event.target as HTMLImageElement
  target.style.display = 'none'
}
</script>

<style scoped>
.food-discovery-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1005;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  max-width: 350px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.food-discovery-toast:hover {
  transform: translateY(-2px);
}

.toast-content {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  color: white;
  position: relative;
}

.food-icon {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.food-icon img {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.food-info {
  flex: 1;
}

.food-info h3 {
  margin: 0 0 4px 0;
  font-size: 14px;
  font-weight: 600;
  opacity: 0.9;
}

.food-info h4 {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 700;
}

.food-info p {
  margin: 0 0 12px 0;
  font-size: 14px;
  line-height: 1.4;
  opacity: 0.9;
}

.food-stats {
  display: flex;
  gap: 12px;
  align-items: center;
}

.calories {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.health-badge {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.health-badge.green {
  background-color: #27ae60;
}

.health-badge.yellow {
  background-color: #f1c40f;
  color: #2c3e50;
}

.health-badge.orange {
  background-color: #e67e22;
}

.close-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  color: white;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Animações */
.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
