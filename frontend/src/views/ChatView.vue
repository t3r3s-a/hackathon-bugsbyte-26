<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();
</script>

<template>
  <div class="chat-container">
    <h1>🤖 Amigo Presente</h1>
    <p>O chat da IA vai aparecer aqui!</p>
    <button @click="router.push('/welcome')">Voltar</button>
  </div>
</template>

<style scoped>
.chat-container {
  padding: 40px;
  text-align: center;
  font-family: sans-serif;
}
button {
  margin-top: 20px;
  padding: 10px 20px;
  cursor: pointer;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 8px;
}
</style>