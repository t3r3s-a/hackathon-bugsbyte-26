export interface Food {
  id: string;
  name: string;
  calories: number;
  health_color: 'green' | 'yellow' | 'orange';
  sprite: string;
  category: string;
  protein: number;
  hydration: number;
  vitamins: number;
  rating: number;
  discovery_message: string;
}

export interface MealConfig {
  name: string;
  icon: string;
  description: string;
  target_calories: { min: number; max: number };
  food_ids: string[];
  duration?: number;
}

export interface Meal {
  name: string;
  icon: string;
  description: string;
  duration: number;
  cols?: number; // Número de colunas da grid (varia por refeição)
  rows?: number; // Número de linhas da grid (varia por refeição)
  target_calories: {
    min: number;
    max: number;
  };
  food_ids: string[]; // Apenas IDs que referenciam foods.json
  foods: Food[]; // Lista completa de alimentos após carregar
}

export interface MealData {
  [key: string]: Meal;
}

export interface GameState {
  day: number;
  currentMeal: number;
  mealNames: string[];
  calories: number;
  discoveredFoods: Set<string>;
  gamePhase: 'menu' | 'instructions' | 'meal' | 'choice' | 'training-select' | 'training' | 'sleep' | 'gameover';
  lastMealResult?: MealResult;
}

export interface MealResult {
  success: boolean;
  caloriesConsumed: number;
  newFoodsDiscovered: string[];
  message: string;
  resetToMenu?: boolean; // Flag para indicar que deve voltar ao menu inicial (Game Over)
}

export interface TrainingChoice {
  id: string;
  name: string;
  icon: string;
  description: string;
  caloriesBurned: number;
}

// Helper function to load meals with food data
export async function loadMealsData(): Promise<MealData> {
  const [foodsData, mealsConfig] = await Promise.all([
    import('../data/foods.json'),
    import('../data/meals.json')
  ]);
  
  const foods = foodsData.default;
  const meals = mealsConfig.default;
  
  // Create a map for quick food lookup
  const foodMap = new Map<string, any>();
  foods.forEach((food: any) => {
    foodMap.set(food.nome, {
      id: food.nome,
      name: food.nome,
      calories: food.energia_kcal,
      health_color: food.cor === 'verde' ? 'green' : food.cor === 'amarelo' ? 'yellow' : 'orange',
      sprite: `/src/assets/games/foods/${food.nome}.png`,
      category: food.alergias?.[0] || 'outros',
      protein: food.proteina_g,
      hydration: food.agua_g,
      vitamins: food.vitamina_c_mg + food.vitamina_a_ug / 100,
      rating: food.cor === 'verde' ? 5 : food.cor === 'amarelo' ? 3 : 1,
      discovery_message: food.descricao
    });
  });
  
  // Transform meals config to meals with full food data
  const mealsData: MealData = {};
  
  for (const [key, mealConfig] of Object.entries(meals) as [string, any][]) {
    const mealFoods: Food[] = [];
    
    for (const foodId of mealConfig.food_ids) {
      const food = foodMap.get(foodId);
      if (food) {
        mealFoods.push(food);
      } else {
        console.warn(`Food not found: ${foodId}`);
      }
    }
    
    mealsData[key] = {
      name: mealConfig.name,
      icon: mealConfig.icon,
      description: mealConfig.description,
      target_calories: mealConfig.target_calories,
      food_ids: mealConfig.food_ids,
      foods: mealFoods,
      duration: mealConfig.duration || 30,
      cols: mealConfig.cols, // Carregar colunas da grid
      rows: mealConfig.rows  // Carregar linhas da grid
    };
  }
  
  return mealsData;
}

// Adicionar às exportações existentes
export type { GameConfig, GameResult, GameType } from './types';