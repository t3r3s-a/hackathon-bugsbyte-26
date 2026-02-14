<script setup>
import LoginView from './views/loginView.vue';
</script>

<template>
    <img alt="nutrium logo" src="./assets/logo-nutrium.png" class="logo">
    <LoginView/>

</template>

<style scoped>

.logo {
  height: 100px;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
