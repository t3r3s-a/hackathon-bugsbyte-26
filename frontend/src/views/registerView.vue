<script setup>
import { ref } from 'vue'

const username = ref('')
const password = ref('')

const handleRegister = (event) => {
  event.preventDefault()
}
</script>

<template>
  <div class="login-box">
    <h3>Registo</h3> 
    
    <form @submit="handleRegister">
      <div class="field">
        <label>Utilizador</label>
        <input v-model="username" type="text" placeholder="Novo utilizador" />
      </div>
      
      <div class="field">
        <label>Palavra-passe</label>
        <input v-model="password" type="password" placeholder="Nova palavra-passe" />
      </div>

      <button type="submit" style="background-color: #3498db;">Registar</button>
    </form>
  </div>
</template>

<style scoped>
.login-box {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.field {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}
input {
  padding: 5px;
}
button {
  color: white;
  border: none;
  padding: 8px;
  cursor: pointer;
}
</style>