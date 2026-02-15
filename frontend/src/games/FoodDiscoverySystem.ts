// FoodDiscoverySystem.ts - Sistema de descoberta e catálogo de alimentos

import type { Food, FoodDiscovery, FoodNutritionBars } from './types';

export class FoodDiscoverySystem {
  private discoveries: Map<string, FoodDiscovery>;
  private readonly STORAGE_KEY = 'nutrium_snake_discoveries';

  constructor() {
    this.discoveries = new Map();
    this.loadFromStorage();
  }

  /**
   * Marca um alimento como descoberto
   * @returns true se é a primeira vez que descobre este alimento
   */
  public discoverFood(foodName: string): boolean {
    const existing = this.discoveries.get(foodName);
    
    if (existing) {
      // Já foi descoberto antes, apenas incrementa contador
      existing.timesEaten++;
      this.saveToStorage();
      return false;
    } else {
      // Primeira vez descobrindo este alimento
      this.discoveries.set(foodName, {
        foodName,
        discoveredAt: new Date(),
        timesEaten: 1
      });
      this.saveToStorage();
      return true;
    }
  }

  /**
   * Verifica se um alimento já foi descoberto
   */
  public isDiscovered(foodName: string): boolean {
    return this.discoveries.has(foodName);
  }

  /**
   * Obtém informações de descoberta de um alimento
   */
  public getDiscovery(foodName: string): FoodDiscovery | null {
    return this.discoveries.get(foodName) || null;
  }

  /**
   * Obtém todos os alimentos descobertos
   */
  public getAllDiscoveries(): FoodDiscovery[] {
    return Array.from(this.discoveries.values());
  }

  /**
   * Número total de alimentos descobertos
   */
  public getTotalDiscovered(): number {
    return this.discoveries.size;
  }

  /**
   * Calcula as barras de nutrição para visualização (0-5)
   */
  public calculateNutritionBars(food: Food): FoodNutritionBars {
    return {
      // Proteína: 0g = 0, 30g+ = 5
      protein: Math.min(5, Math.round((food.proteina_g / 6))),
      
      // Hidratação: baseado na água
      hydration: Math.min(5, Math.round((food.agua_g / 20))),
      
      // Calorias: 0 = 0, 500+ = 5
      calories: Math.min(5, Math.round((food.energia_kcal / 100))),
      
      // Vitaminas: baseado em Vit C e A
      vitamins: Math.min(5, Math.round(
        ((food.vitamina_c_mg / 20) + (food.vitamina_a_ug / 200)) / 2
      )),
      
      // Minerais: baseado em potássio, cálcio, ferro
      minerals: Math.min(5, Math.round(
        ((food.potassio_mg / 100) + (food.calcio_mg / 50) + (food.ferro_mg * 5)) / 3
      ))
    };
  }

  /**
   * Calcula avaliação geral do alimento (0-5 estrelas)
   */
  public calculateRating(food: Food): number {
    // Baseado na cor de saúde
    const colorRating: Record<string, number> = {
      'verde': 5,
      'amarelo': 4,
      'laranja': 3,
      'vermelho': 2,
      'castanho': 3,
      'branco': 3,
      'roxo': 4
    };

    return colorRating[food.cor] || 3;
  }

  /**
   * Salva descobertas no localStorage
   */
  private saveToStorage(): void {
    try {
      const data = Array.from(this.discoveries.entries()).map(([name, discovery]) => ({
        name,
        discoveredAt: discovery.discoveredAt.toISOString(),
        timesEaten: discovery.timesEaten
      }));
      
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(data));
    } catch (error) {
      console.error('Erro ao salvar descobertas:', error);
    }
  }

  /**
   * Carrega descobertas do localStorage
   */
  private loadFromStorage(): void {
    try {
      const stored = localStorage.getItem(this.STORAGE_KEY);
      if (!stored) return;

      const data = JSON.parse(stored);
      this.discoveries.clear();

      for (const item of data) {
        this.discoveries.set(item.name, {
          foodName: item.name,
          discoveredAt: new Date(item.discoveredAt),
          timesEaten: item.timesEaten
        });
      }
    } catch (error) {
      console.error('Erro ao carregar descobertas:', error);
    }
  }

  /**
   * Reseta todas as descobertas (útil para debug)
   */
  public resetAllDiscoveries(): void {
    this.discoveries.clear();
    localStorage.removeItem(this.STORAGE_KEY);
  }

  /**
   * Exporta descobertas para JSON
   */
  public exportToJSON(): string {
    return JSON.stringify(Array.from(this.discoveries.values()), null, 2);
  }
}

// Instância singleton
let instance: FoodDiscoverySystem | null = null;

export function getFoodDiscoverySystem(): FoodDiscoverySystem {
  if (!instance) {
    instance = new FoodDiscoverySystem();
  }
  return instance;
}
