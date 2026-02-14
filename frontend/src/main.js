import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js'  // se tiveres router

createApp(App)
  .use(router)   // só se tiver router
  .mount('#app')
