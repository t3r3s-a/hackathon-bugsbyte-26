<script>
import { ref } from 'vue'

export default{
    name:'loginView',
}

const username=ref('')
const password=ref('')

const handleLogin = (event) => {
  event.preventDefault()

  const dataBackend = {
    user: username.value,
    pass: password.value
  }
  // logica de backend de python
}

</script>

<template>

    <form name="login-form" >
        <div class="mb-3">
            <label for="username">Utilizador: </label>
            <input id="username" type="text" />
        </div>
        <div class="mb-3">
            <label for="password">Palavra-passe: </label>
            <input id="password" type="password" />
        </div>
        <button class="btn btn-outline-dark" type="submit">
            Login 
        </button>
    </form>
</template>


