<template>
  <!-- Fundo fixo -->
  <div class="app-background">
    <img alt="nutrium logo" src="./assets/logo-nutrium.png" class="logo" />
    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>
  </div>

  <!-- Transição entre views -->
  <transition name="view-fade" mode="out-in">
    <router-view />
  </transition>
</template>

<script setup>
// Nada especial aqui
</script>

<style scoped>
.app-background {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(135deg, #fdfaf4 0%, #eef7ff 40%, #e3f2ff 100%);
  z-index: -1;
}

/* Logo */
.logo {
  position: absolute;
  top: 1.5em;
  height: 100px;
  transition: filter 0.3s;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

/* Glow fixo */
.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.4;
  animation: pulse 5s ease-in-out infinite;
}

.glow-1 {
  width: 300px;
  height: 300px;
  background: #27ae60;
  top: 10%;
  left: 15%;
}

.glow-2 {
  width: 350px;
  height: 350px;
  background: #3498db;
  bottom: 10%;
  right: 10%;
  animation-delay: 1s;
}

/* Transição das views */
.view-fade-enter-active,
.view-fade-leave-active {
  transition: opacity 0.5s, transform 0.5s;
}

.view-fade-enter-from,
.view-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

@keyframes pulse {
  0%,
  100% {
    opacity: 0.4;
  }
  50% {
    opacity: 0.7;
  }
}
</style>
