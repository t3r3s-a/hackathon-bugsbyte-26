import type { Food, Meal, MealData, GameState, MealResult } from './snakeTypes';

interface FoodWithPosition extends Food {
  x: number;
  y: number;
}

export class SnakeGame {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private gameState: GameState;
  private meals: MealData;
  private snake: { x: number; y: number }[];
  private direction: { x: number; y: number };
  private currentFood: FoodWithPosition | null = null;
  private gameLoop: number | null = null;
  private onGameEnd?: (result: MealResult) => void;
  private onFoodDiscovered?: (food: Food) => void;
  
  // Adicionar referência ao event listener para poder remover depois
  private keydownHandler: ((e: KeyboardEvent) => void) | null = null;
  
  // Configurações do jogo
  private readonly GAME_SPEED = 150;
  private readonly HUD_HEIGHT = 80;
  private readonly MAX_CALORIES = 2500;
  private readonly MIN_CALORIES = 0;
  private readonly CALORIES_PER_SECOND = 5;
  
  // Grid dinâmica (varia por refeição)
  private gridCols: number = 20;
  private gridRows: number = 16;
  private cellSize: number = 20;
  private gridOffsetX: number = 0;
  private gridOffsetY: number = 80;
  private gridWidth: number = 0;
  private gridHeight: number = 0;
  
  // Cores da cobra (laranja como no Python)
  private readonly SNAKE_HEAD_COLOR = '#BE4B00';
  private readonly SNAKE_BODY_COLOR = '#F97316';
  
  // Cache de imagens
  private foodImages: Map<string, HTMLImageElement> = new Map();
  private snakeHeadImage: HTMLImageElement | null = null;
  private imagesLoaded: boolean = false;
  
  // Estado da refeição atual
  private currentMealKey: string = '';
  private currentCalories: number = 0;
  private newFoodsDiscovered: string[] = [];
  private isRunning: boolean = false;
  private timeRemaining: number = 0;
  private lastTimeUpdate: number = 0;
  
  constructor(canvas: HTMLCanvasElement, meals: MealData) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d')!;
    this.meals = meals;
    
    // Estado inicial do jogo
    this.gameState = {
      day: 1,
      currentMeal: 0,
      mealNames: ['pequeno_almoco', 'lanche_manha', 'almoco', 'lanche_tarde', 'jantar'],
      calories: 300,
      discoveredFoods: new Set(),
      gamePhase: 'meal'
    };
    
    // Estado inicial da cobra
    this.snake = [{ x: 10, y: 10 }];
    this.direction = { x: 0, y: 0 };
    
    this.setupControls();
    this.loadAssets();
  }
  
  private async loadAssets() {
    try {
      const headImg = new Image();
      headImg.src = '/src/assets/games/cabeca_snake.png';
      await new Promise((resolve, reject) => {
        headImg.onload = resolve;
        headImg.onerror = reject;
      });
      this.snakeHeadImage = headImg;
      
      const commonFoods = [
        'Maçã', 'Banana', 'Pão integral', 'Leite', 'Arroz branco cozido',
        'Peito de frango grelhado (sem pele)', 'Salmão grelhado', 'Brócolos cozidos'
      ];
      
      for (const foodName of commonFoods) {
        const img = new Image();
        img.src = `/src/assets/games/foods/${foodName}.png`;
        img.onerror = () => {
          console.warn(`Sprite não encontrado para: ${foodName}`);
        };
        this.foodImages.set(foodName, img);
      }
      
      this.imagesLoaded = true;
    } catch (error) {
      console.warn('Erro ao carregar assets:', error);
      this.imagesLoaded = true;
    }
  }
  
  private async loadFoodSprite(foodName: string): Promise<HTMLImageElement | null> {
    if (this.foodImages.has(foodName)) {
      return this.foodImages.get(foodName)!;
    }
    
    try {
      const img = new Image();
      img.src = `/src/assets/games/foods/${foodName}.png`;
      await new Promise((resolve, reject) => {
        img.onload = resolve;
        img.onerror = reject;
      });
      this.foodImages.set(foodName, img);
      return img;
    } catch (error) {
      console.warn(`Sprite não encontrado para: ${foodName}`);
      return null;
    }
  }
  
  public setCallbacks(onGameEnd?: (result: MealResult) => void, onFoodDiscovered?: (food: Food) => void) {
    this.onGameEnd = onGameEnd;
    this.onFoodDiscovered = onFoodDiscovered;
  }
  
  public setInitialCalories(calories: number) {
    this.gameState.calories = calories;
  }
  
  private setupControls() {
    // Remover listener antigo se existir
    if (this.keydownHandler) {
      document.removeEventListener('keydown', this.keydownHandler);
    }
    
    // Criar novo handler e guardar referência
    this.keydownHandler = (e: KeyboardEvent) => {
      if (!this.isRunning) return;
      
      switch (e.key) {
        case 'ArrowUp':
          if (this.direction.y !== 1) this.direction = { x: 0, y: -1 };
          e.preventDefault();
          break;
        case 'ArrowDown':
          if (this.direction.y !== -1) this.direction = { x: 0, y: 1 };
          e.preventDefault();
          break;
        case 'ArrowLeft':
          if (this.direction.x !== 1) this.direction = { x: -1, y: 0 };
          e.preventDefault();
          break;
        case 'ArrowRight':
          if (this.direction.x !== -1) this.direction = { x: 1, y: 0 };
          e.preventDefault();
          break;
      }
    };
    
    document.addEventListener('keydown', this.keydownHandler);
  }
  
  private calculateGridOffset(meal: Meal) {
    this.gridCols = meal.cols || 20;
    this.gridRows = meal.rows || 16;
    
    const availableWidth = this.canvas.width;
    const availableHeight = this.canvas.height - this.HUD_HEIGHT;
    
    const sizePerCol = availableWidth / this.gridCols;
    const sizePerRow = availableHeight / this.gridRows;
    this.cellSize = Math.floor(Math.min(sizePerCol, sizePerRow));
    
    this.gridWidth = this.gridCols * this.cellSize;
    this.gridHeight = this.gridRows * this.cellSize;
    
    this.gridOffsetX = Math.floor((availableWidth - this.gridWidth) / 2);
    this.gridOffsetY = this.HUD_HEIGHT + Math.floor((availableHeight - this.gridHeight) / 2);
  }
  
  public async startMeal(): Promise<MealResult> {
    return new Promise(async (resolve) => {
      this.currentMealKey = this.gameState.mealNames[this.gameState.currentMeal];
      const meal = this.meals[this.currentMealKey];
      
      if (!meal) {
        resolve({ 
          success: false, 
          caloriesConsumed: 0, 
          newFoodsDiscovered: [], 
          message: 'Refeição não encontrada!' 
        });
        return;
      }
      
      this.calculateGridOffset(meal);
      
      this.currentCalories = this.gameState.calories;
      this.newFoodsDiscovered = [];
      const targetMin = meal.target_calories.min;
      const targetMax = meal.target_calories.max;
      
      this.timeRemaining = meal.duration || 30;
      this.lastTimeUpdate = Date.now();
      
      const initialSize = Math.max(1, Math.floor(this.currentCalories / 100));
      this.snake = [];
      const centerCol = Math.floor(this.gridCols / 2);
      const centerRow = Math.floor(this.gridRows / 2);
      const startX = this.gridOffsetX + centerCol * this.cellSize;
      const startY = this.gridOffsetY + centerRow * this.cellSize;
      
      for (let i = 0; i < initialSize; i++) {
        this.snake.push({ 
          x: startX - (i * this.cellSize), 
          y: startY 
        });
      }
      
      this.direction = { x: 1, y: 0 };
      await this.spawnFood(meal);
      this.isRunning = true;
      
      this.gameLoop = setInterval(() => {
        if (!this.isRunning) return;
        
        const now = Date.now();
        const deltaTime = (now - this.lastTimeUpdate) / 1000;
        this.lastTimeUpdate = now;
        this.timeRemaining = Math.max(0, this.timeRemaining - deltaTime);
        
        this.currentCalories = Math.max(0, this.currentCalories - (this.CALORIES_PER_SECOND * deltaTime));
        
        if (this.currentCalories <= this.MIN_CALORIES || this.currentCalories >= this.MAX_CALORIES) {
          this.stopGame();
          this.resetToDay1();
          
          const message = this.currentCalories <= this.MIN_CALORIES 
            ? 'Ficaste sem energia! 😵 Voltando ao início...'
            : 'Comeste demasiado! 🤢 Voltando ao início...';
          
          resolve({
            success: false,
            caloriesConsumed: 300,
            newFoodsDiscovered: this.newFoodsDiscovered,
            message: message,
            resetToMenu: true
          });
          return;
        }
        
        if (this.checkCollisions()) {
          this.stopGame();
          this.resetToDay1();
          
          resolve({
            success: false,
            caloriesConsumed: 300,
            newFoodsDiscovered: this.newFoodsDiscovered,
            message: 'Game Over! A cobra bateu! 💥 Voltando ao início...',
            resetToMenu: true
          });
          return;
        }
        
        this.update();
        this.draw(meal, this.currentCalories, targetMin, targetMax);
        
        const head = this.snake[0];
        if (this.currentFood && 
            Math.abs(head.x - this.currentFood.x) < this.cellSize &&
            Math.abs(head.y - this.currentFood.y) < this.cellSize) {
          
          this.currentCalories += this.currentFood.calories;
          
          if (this.currentCalories >= this.MAX_CALORIES) {
            this.stopGame();
            this.resetToDay1();
            
            resolve({
              success: false,
              caloriesConsumed: 300,
              newFoodsDiscovered: this.newFoodsDiscovered,
              message: 'Comeste demasiado! 🤢 Voltando ao início...',
              resetToMenu: true
            });
            return;
          }
          
          if (!this.gameState.discoveredFoods.has(this.currentFood.id)) {
            this.gameState.discoveredFoods.add(this.currentFood.id);
            this.newFoodsDiscovered.push(this.currentFood.id);
            if (this.onFoodDiscovered) {
              this.onFoodDiscovered(this.currentFood);
            }
          }
          
          const newSize = Math.max(1, Math.floor(this.currentCalories / 100));
          while (this.snake.length < newSize) {
            const tail = this.snake[this.snake.length - 1];
            this.snake.push({ ...tail });
          }
          
          this.spawnFood(meal);
        }
        
        if (this.timeRemaining <= 0.1) {
          this.stopGame();
          this.gameState.calories = this.currentCalories;
          
          if (this.currentCalories > this.MIN_CALORIES && this.currentCalories < this.MAX_CALORIES) {
            resolve({
              success: true,
              caloriesConsumed: this.currentCalories,
              newFoodsDiscovered: this.newFoodsDiscovered,
              message: `${meal.name} completo! Mantiveste um nível saudável de ${Math.round(this.currentCalories)} calorias. 🎉`
            });
          } else if (this.currentCalories <= this.MIN_CALORIES) {
            resolve({
              success: false,
              caloriesConsumed: this.currentCalories,
              newFoodsDiscovered: this.newFoodsDiscovered,
              message: `Ficaste sem energia durante a refeição! 😕`
            });
          } else {
            resolve({
              success: false,
              caloriesConsumed: this.currentCalories,
              newFoodsDiscovered: this.newFoodsDiscovered,
              message: `Comeste demasiado durante a refeição! 🤢`
            });
          }
        }
      }, this.GAME_SPEED);
    });
  }
  
  private async spawnFood(meal: Meal) {
    if (!meal.foods || meal.foods.length === 0) {
      console.error('Meal sem alimentos:', meal);
      return;
    }
    
    const randomFood = meal.foods[Math.floor(Math.random() * meal.foods.length)];
    await this.loadFoodSprite(randomFood.name);
    
    let foodPosition: { x: number; y: number };
    let attempts = 0;
    
    do {
      const col = Math.floor(Math.random() * this.gridCols);
      const row = Math.floor(Math.random() * this.gridRows);
      
      foodPosition = {
        x: this.gridOffsetX + col * this.cellSize,
        y: this.gridOffsetY + row * this.cellSize
      };
      
      attempts++;
    } while (attempts < 100 && this.snake.some(segment => 
      Math.abs(segment.x - foodPosition.x) < this.cellSize && 
      Math.abs(segment.y - foodPosition.y) < this.cellSize
    ));
    
    this.currentFood = { ...randomFood, x: foodPosition.x, y: foodPosition.y };
  }
  
  private update() {
    if (this.direction.x === 0 && this.direction.y === 0) return;
    
    const head = { ...this.snake[0] };
    head.x += this.direction.x * this.cellSize;
    head.y += this.direction.y * this.cellSize;
    
    this.snake.unshift(head);
    this.snake.pop();
  }
  
  private draw(meal: Meal, calories: number, targetMin: number, targetMax: number) {
    this.ctx.fillStyle = '#18181B';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    
    this.ctx.strokeStyle = 'rgba(63, 63, 70, 0.5)';
    this.ctx.lineWidth = 1;
    
    for (let col = 0; col <= this.gridCols; col++) {
      const x = this.gridOffsetX + col * this.cellSize;
      this.ctx.beginPath();
      this.ctx.moveTo(x, this.gridOffsetY);
      this.ctx.lineTo(x, this.gridOffsetY + this.gridHeight);
      this.ctx.stroke();
    }
    
    for (let row = 0; row <= this.gridRows; row++) {
      const y = this.gridOffsetY + row * this.cellSize;
      this.ctx.beginPath();
      this.ctx.moveTo(this.gridOffsetX, y);
      this.ctx.lineTo(this.gridOffsetX + this.gridWidth, y);
      this.ctx.stroke();
    }
    
    this.ctx.fillStyle = '#27272A';
    this.ctx.fillRect(0, 0, this.canvas.width, this.HUD_HEIGHT);
    
    this.ctx.strokeStyle = '#A0400B';
    this.ctx.lineWidth = 2;
    this.ctx.beginPath();
    this.ctx.moveTo(0, this.HUD_HEIGHT);
    this.ctx.lineTo(this.canvas.width, this.HUD_HEIGHT);
    this.ctx.stroke();
    
    const barWidth = 300;
    const barHeight = 14;
    const barX = this.canvas.width / 2 - barWidth / 2;
    const barY = 15;
    
    this.ctx.fillStyle = '#2D2D30';
    this.ctx.beginPath();
    this.ctx.roundRect(barX, barY, barWidth, barHeight, 7);
    this.ctx.fill();
    
    const proportion = Math.max(0, Math.min(1, calories / this.MAX_CALORIES));
    if (proportion > 0) {
      this.ctx.fillStyle = '#F97316';
      this.ctx.beginPath();
      this.ctx.roundRect(barX, barY, barWidth * proportion, barHeight, 7);
      this.ctx.fill();
    }
    
    this.ctx.fillStyle = '#FAFAF9';
    this.ctx.font = 'bold 18px Arial';
    const calText = `${Math.round(calories)}/${this.MAX_CALORIES} kcal`;
    const calTextWidth = this.ctx.measureText(calText).width;
    this.ctx.fillText(calText, this.canvas.width / 2 - calTextWidth / 2, barY + barHeight + 18);
    
    this.ctx.fillStyle = '#FAFAF9';
    this.ctx.font = 'bold 26px Arial';
    const timeText = `⏱️ ${Math.ceil(this.timeRemaining)}s`;
    this.ctx.fillText(timeText, 15, 35);
    
    this.ctx.font = 'bold 18px Arial';
    const dayText = `Dia ${this.gameState.day}`;
    const dayTextWidth = this.ctx.measureText(dayText).width;
    this.ctx.fillText(dayText, this.canvas.width - dayTextWidth - 15, 35);
    
    this.snake.forEach((segment, index) => {
      if (index === 0) {
        if (this.snakeHeadImage && this.snakeHeadImage.complete) {
          this.ctx.save();
          this.ctx.translate(segment.x + this.cellSize / 2, segment.y + this.cellSize / 2);
          
          if (this.direction.x === 1) this.ctx.rotate(0);
          else if (this.direction.x === -1) this.ctx.rotate(Math.PI);
          else if (this.direction.y === -1) this.ctx.rotate(-Math.PI / 2);
          else if (this.direction.y === 1) this.ctx.rotate(Math.PI / 2);
          
          this.ctx.drawImage(
            this.snakeHeadImage,
            -this.cellSize / 2,
            -this.cellSize / 2,
            this.cellSize,
            this.cellSize
          );
          this.ctx.restore();
        } else {
          this.ctx.fillStyle = '#BE4B00';
          this.ctx.beginPath();
          this.ctx.roundRect(segment.x, segment.y, this.cellSize - 2, this.cellSize - 2, 6);
          this.ctx.fill();
          
          this.ctx.fillStyle = '#000000';
          const eyeSize = Math.max(2, Math.floor(this.cellSize / 7));
          const eyeOffset = Math.floor(this.cellSize * 0.6);
          const eyeMargin = Math.floor(this.cellSize * 0.2);
          
          if (this.direction.x === 1) {
            this.ctx.fillRect(segment.x + eyeOffset, segment.y + eyeMargin, eyeSize, eyeSize);
            this.ctx.fillRect(segment.x + eyeOffset, segment.y + eyeOffset, eyeSize, eyeSize);
          } else if (this.direction.x === -1) {
            this.ctx.fillRect(segment.x + eyeMargin, segment.y + eyeMargin, eyeSize, eyeSize);
            this.ctx.fillRect(segment.x + eyeMargin, segment.y + eyeOffset, eyeSize, eyeSize);
          } else if (this.direction.y === -1) {
            this.ctx.fillRect(segment.x + eyeMargin, segment.y + eyeMargin, eyeSize, eyeSize);
            this.ctx.fillRect(segment.x + eyeOffset, segment.y + eyeMargin, eyeSize, eyeSize);
          } else if (this.direction.y === 1) {
            this.ctx.fillRect(segment.x + eyeMargin, segment.y + eyeOffset, eyeSize, eyeSize);
            this.ctx.fillRect(segment.x + eyeOffset, segment.y + eyeOffset, eyeSize, eyeSize);
          }
        }
      } else {
        this.ctx.fillStyle = '#A0400B';
        this.ctx.beginPath();
        this.ctx.roundRect(segment.x + 1, segment.y + 1, this.cellSize - 4, this.cellSize - 4, 4);
        this.ctx.fill();
      }
    });
    
    if (this.currentFood) {
      const foodSprite = this.foodImages.get(this.currentFood.name);
      
      if (foodSprite && foodSprite.complete) {
        this.ctx.drawImage(
          foodSprite,
          this.currentFood.x,
          this.currentFood.y,
          this.cellSize,
          this.cellSize
        );
      } else {
        const color = this.getFoodColor(this.currentFood.health_color);
        this.ctx.fillStyle = color;
        this.ctx.beginPath();
        this.ctx.roundRect(this.currentFood.x, this.currentFood.y, this.cellSize, this.cellSize, 4);
        this.ctx.fill();
        
        this.ctx.strokeStyle = '#FAFAF9';
        this.ctx.lineWidth = 1;
        this.ctx.strokeRect(this.currentFood.x, this.currentFood.y, this.cellSize, this.cellSize);
      }
      
      const calText = `${this.currentFood.calories} cal`;
      this.ctx.font = 'bold 10px Arial';
      this.ctx.fillStyle = '#FAFAF9';
      this.ctx.strokeStyle = '#18181B';
      this.ctx.lineWidth = 3;
      this.ctx.strokeText(calText, this.currentFood.x + 2, this.currentFood.y + this.cellSize + 12);
      this.ctx.fillText(calText, this.currentFood.x + 2, this.currentFood.y + this.cellSize + 12);
    }
    
    this.ctx.fillStyle = 'rgba(250, 250, 249, 0.5)';
    this.ctx.font = '12px Arial';
    this.ctx.fillText('Use as setas (↑↓←→) para controlar a cobra', 10, this.canvas.height - 10);
  }
  
  private getFoodColor(healthColor: string): string {
    switch (healthColor) {
      case 'green': return '#2ECC71';
      case 'yellow': return '#F1C40F';
      case 'orange': return '#E67E22';
      default: return '#95A5A6';
    }
  }
  
  private checkCollisions(): boolean {
    const head = this.snake[0];
    
    if (head.x < this.gridOffsetX || 
        head.x >= this.gridOffsetX + this.gridWidth || 
        head.y < this.gridOffsetY || 
        head.y >= this.gridOffsetY + this.gridHeight) {
      return true;
    }
    
    for (let i = 1; i < this.snake.length; i++) {
      if (head.x === this.snake[i].x && head.y === this.snake[i].y) {
        return true;
      }
    }
    
    return false;
  }
  
  private stopGame() {
    this.isRunning = false;
    if (this.gameLoop) {
      clearInterval(this.gameLoop);
      this.gameLoop = null;
    }
  }
  
  private resetToDay1() {
    this.gameState.day = 1;
    this.gameState.currentMeal = 0;
    this.gameState.calories = 300;
  }
  
  public getGameState(): GameState {
    return { ...this.gameState };
  }
  
  public nextMeal() {
    this.gameState.currentMeal++;
    if (this.gameState.currentMeal >= this.gameState.mealNames.length) {
      this.gameState.currentMeal = 0;
      this.gameState.day++;
    }
  }
  
  public cleanup() {
    this.stopGame();
    
    // Remover event listener quando limpar o jogo
    if (this.keydownHandler) {
      document.removeEventListener('keydown', this.keydownHandler);
      this.keydownHandler = null;
    }
  }
}