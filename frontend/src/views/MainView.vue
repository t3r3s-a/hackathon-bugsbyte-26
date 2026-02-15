<script setup>
import { Apple, MessageSquare, Gamepad2, Leaf } from "lucide-vue-next";
import healthychild from "../assets/healthychild.jpg";

import logoParceria from "../assets/logo-parceria.png"; 

const features = [
  { 
    icon: Apple, 
    title: "Planos Alimentares", 
    desc: "Refeições equilibradas pensadas para os mais pequenos." 
  },
  { 
    icon: MessageSquare, 
    title: "AI Nutricional", 
    desc: "Esclarece as tuas dúvidas sobre os teus hábitos alimentares e muito mais!" 
  },
  { 
    icon: Gamepad2, 
    title: "Snack-e", 
    desc: "Diverte-te e queima calorias enquanto aprendes a comer melhor!" 
  },
];
</script>

<template>
  <div class="main-container">
    <header class="header">
      <div class="logo-container">
        <img :src="logoParceria" alt="Nutrium x Snack-e" class="nav-logo" />
      </div>
      <nav class="nav">
        <router-link to="/login" class="btn-text">Entrar</router-link>
        <router-link to="/register" class="btn-primary">Registar</router-link>
      </nav>
    </header>

    <section class="hero">
      <div class="hero-content">
        <div class="partnership">
        </div>

        <h1 class="hero-title">
          Alimentação saudável e <span class="highlight">divertida</span> para crianças!
        </h1>

        <p class="hero-text">
          Uma plataforma nutricional que ajuda crianças a descobrir e melhorar os seus hábitos alimentares de forma simples e interativa.
        </p>

        <div class="actions">
          <router-link to="/register" class="btn-cta">Começar Agora →</router-link>
          <router-link to="/login" class="btn-secondary">Já tenho conta</router-link>
        </div>
      </div>

      <div class="hero-image-container">
        <img :src="healthychild" alt="Crianças saudáveis" class="hero-image" />
      </div>
    </section>

    <section class="features">
      <div class="features-grid">
        <div v-for="(item, i) in features" :key="i" class="feature-card">
          <div class="feature-icon">
            <component :is="item.icon" />
          </div>
          <h3>{{ item.title }}</h3>
          <p>{{ item.desc }}</p>
        </div>
      </div>
    </section>

    <footer class="footer">
      <p>© 2026 Nutrium × Snack-e. Todos os direitos reservados.</p>
    </footer>
  </div>
</template>

<style scoped>
.main-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
  background: white;
  min-height: 100vh;
}

/* Header & Logo */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 5%;
  max-width: 1200px;
  margin: 0 auto;
}

.nav-logo {
  height: 40px; /* Ajusta o tamanho conforme o teu logo */
  width: auto;
  display: block;
}

.nav { display: flex; gap: 20px; }

.btn-primary {
  background: #47baac;
  color: white;
  padding: 10px 25px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
}

.btn-text {
  color: #47baac;
  text-decoration: none;
  font-weight: 600;
  padding: 10px;
}

/* Hero */
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 50px;
  padding: 60px 5% 80px;
  background: linear-gradient(to bottom, #f0fdf4, white);
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-title { font-size: 3rem; line-height: 1.1; margin-bottom: 25px; color: #111; }
.highlight { color: #47baac; }
.hero-text { font-size: 1.1rem; color: #666; margin-bottom: 30px; line-height: 1.6; }

.partnership { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
.badge { background: white; border: 1px solid #ddd; padding: 5px 15px; border-radius: 10px; font-weight: bold; }
.badge-green { background: white; border: 1px solid #bbf7d0; padding: 5px 15px; border-radius: 10px; font-weight: bold; color: #47baac; }

.actions { display: flex; gap: 15px; }

.btn-cta {
  background: #47baac;
  color: white;
  padding: 15px 30px;
  border-radius: 15px;
  text-decoration: none;
  font-weight: bold;
}

.btn-secondary {
  background: white;
  border: 1px solid #ddd;
  padding: 15px 30px;
  border-radius: 15px;
  text-decoration: none;
  font-weight: bold;
  color: #444;
}

.hero-image {
  width: 100%;
  border-radius: 30px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

/* Features Grid */
.features {
  padding: 60px 5%;
  background: white;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); 
  gap: 30px;
  max-width: 1100px;
  margin: 0 auto;
}

.feature-card {
  background: #f9fafb;
  padding: 40px 30px;
  border-radius: 25px;
  text-align: center;
  border: 1px solid #f0f0f0;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  border-color: #dcfce7;
}

.feature-icon {
  background: #dcfce7;
  color: #47baac;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  border-radius: 18px;
}

.feature-card h3 {
  margin-bottom: 15px;
  font-size: 1.25rem;
  color: #111;
}

.feature-card p {
  font-size: 0.95rem;
  color: #666;
  line-height: 1.5;
}

.footer {
  text-align: center;
  padding: 40px;
  border-top: 1px solid #eee;
  color: #999;
  font-size: 0.9rem;
}

/* Mobile */
@media (max-width: 900px) {
  .hero { grid-template-columns: 1fr; text-align: center; }
  .partnership, .actions { justify-content: center; }
  .features-grid { grid-template-columns: 1fr; }
}
</style>