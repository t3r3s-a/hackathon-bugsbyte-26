// types.ts - Tipos principais do jogo Nutrium Snake

export interface Food {
  nome: string;
  energia_kcal: number;
  proteina_g: number;
  hidratos_g: number;
  acucares_g: number;
  lipidos_g: number;
  agua_g: number;
  vitamina_c_mg: number;
  vitamina_a_ug: number;
  potassio_mg: number;
  calcio_mg: number;
  ferro_mg: number;
  alergias: string[];
  descricao: string;
  cor: 'verde' | 'amarelo' | 'laranja' | 'vermelho' | 'castanho' | 'branco' | 'roxo';
}

export interface FoodNutritionBars {
  protein: number;      // 0-5
  hydration: number;    // 0-5
  calories: number;     // 0-5
  vitamins: number;     // 0-5
  minerals: number;     // 0-5
}

export interface FoodDiscovery {
  foodName: string;
  discoveredAt: Date;
  timesEaten: number;
}

export interface GamePhase {
  id: string;
  name: string;
  duration: number;      // Segundos
  cols: number;          // Colunas da grid
  rows: number;          // Linhas da grid
  foodList: string[];    // Nomes dos alimentos disponíveis
  bgColor: string;
}

export interface SnakeSegment {
  x: number;
  y: number;
}

export enum Direction {
  UP = 'up',
  DOWN = 'down',
  LEFT = 'left',
  RIGHT = 'right'
}

export enum GameState {
  PLAYING = 'playing',
  MENU = 'menu',
  SLEEPING = 'sleeping',
  GAME_OVER = 'game_over',
  PAUSED = 'paused',
  VICTORY = 'victory'
}

export interface MenuOption {
  text: string;
  type: 'phase' | 'minigame' | 'sleep' | 'wake' | 'exit';
  destination?: number; // Índice da fase se type === 'phase'
}

export interface GameResult {
  success: boolean;
  caloriesLost?: number;
  caloriesBurned?: number;
  timeRemaining?: number;
  score?: number;
  message?: string;
}

export interface GameConfig {
  targetCalories: number;
  difficulty: number;
  calories?: number;
  canvasWidth?: number;
  canvasHeight?: number;
}

export interface PlayerStats {
  score: number;
  calories: number;
  day: number;
  foodsDiscovered: number;
  gamesPlayed: number;
}

export interface Vector2D {
  x: number;
  y: number;
}

export type GameType = 'jump' | 'balance' | 'race';

// Constantes do jogo
export const GAME_CONSTANTS = {
  CANVAS_WIDTH: 900,
  CANVAS_HEIGHT: 800,
  HUD_HEIGHT: 80,
  GAME_SPEED: 7,                    // FPS
  CALORIES_PER_SECOND: 5,
  CALORIES_MIN: 0,
  CALORIES_MAX: 2500,
  CALORIES_INITIAL: 300,
  SEGMENTS_PER_100_CALORIES: 1
} as const;

export const COLOR_MAP = {
  verde: '#22C55E',      // Verde saudável
  amarelo: '#FDE047',    // Amarelo moderação
  laranja: '#FB923C',    // Laranja cuidado
  vermelho: '#EF4444',   // Vermelho evitar
  castanho: '#78350F',   // Castanho
  branco: '#FFFFFF',     // Branco
  roxo: '#A855F7'        // Roxo
} as const;
