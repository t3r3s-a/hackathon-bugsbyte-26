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
  
  // Cores inspiradas no Google Snake (vibrantes e modernas)
  private readonly BACKGROUND_COLOR = '#1A7F5A'; // Verde vibrante como fundo
  private readonly GRID_LIGHT = '#229663'; // Verde mais claro para células claras
  private readonly GRID_DARK = '#1A7F5A'; // Verde escuro para células escuras
  private readonly SNAKE_HEAD_COLOR = '#FF8C00'; // Laranja escuro
  private readonly SNAKE_BODY_COLOR = '#FFA500'; // Laranja mais claro
  private readonly HUD_BACKGROUND = '#F8F9FA'; // Cinza claro
  private readonly HUD_TEXT = '#202124'; // Preto suave
  
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
        
        // Verificar calorias antes de atualizar posição
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
        
        // Atualizar posição da cobra
        this.update();
        
        // Verificar colisões DEPOIS de atualizar mas ANTES de desenhar
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
        
        // Verificar se comeu comida
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
        
        // Verificar fim do tempo
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
          return;
        }
        
        // Desenhar APENAS depois de todas as verificações
        this.draw(meal, this.currentCalories, targetMin, targetMax);
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
    // Fundo principal com cor vibrante
    this.ctx.fillStyle = this.BACKGROUND_COLOR;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    
    // Grid com padrão de tabuleiro (checkered pattern como Google Snake)
    for (let col = 0; col < this.gridCols; col++) {
      for (let row = 0; row < this.gridRows; row++) {
        const isLightSquare = (col + row) % 2 === 0;
        this.ctx.fillStyle = isLightSquare ? this.GRID_LIGHT : this.GRID_DARK;
        
        const x = this.gridOffsetX + col * this.cellSize;
        const y = this.gridOffsetY + row * this.cellSize;
        
        this.ctx.fillRect(x, y, this.cellSize, this.cellSize);
      }
    }
    
    // Borda do grid
    this.ctx.strokeStyle = '#0D5A3E';
    this.ctx.lineWidth = 3;
    this.ctx.strokeRect(
      this.gridOffsetX - 1.5, 
      this.gridOffsetY - 1.5, 
      this.gridWidth + 3, 
      this.gridHeight + 3
    );
    
    // HUD com estilo Google
    this.ctx.fillStyle = this.HUD_BACKGROUND;
    this.ctx.fillRect(0, 0, this.canvas.width, this.HUD_HEIGHT);
    
    // Linha separadora do HUD
    this.ctx.strokeStyle = '#DADCE0';
    this.ctx.lineWidth = 2;
    this.ctx.beginPath();
    this.ctx.moveTo(0, this.HUD_HEIGHT);
    this.ctx.lineTo(this.canvas.width, this.HUD_HEIGHT);
    this.ctx.stroke();
    
    // Barra de calorias com estilo moderno
    const barWidth = 300;
    const barHeight = 20;
    const barX = this.canvas.width / 2 - barWidth / 2;
    const barY = 12;
    
    // Fundo da barra
    this.ctx.fillStyle = '#E8EAED';
    this.ctx.beginPath();
    this.ctx.roundRect(barX, barY, barWidth, barHeight, 10);
    this.ctx.fill();
    
    // Barra de progresso colorida (gradiente do verde ao vermelho)
    const proportion = Math.max(0, Math.min(1, calories / this.MAX_CALORIES));
    if (proportion > 0) {
      // Cor da barra baseada no nível de calorias
      let barColor = '#34A853'; // Verde (baixo)
      if (proportion > 0.7) {
        barColor = '#EA4335'; // Vermelho (alto)
      } else if (proportion > 0.4) {
        barColor = '#FBBC04'; // Amarelo (médio)
      }
      
      this.ctx.fillStyle = barColor;
      this.ctx.beginPath();
      this.ctx.roundRect(barX, barY, barWidth * proportion, barHeight, 10);
      this.ctx.fill();
    }
    
    // Borda da barra
    this.ctx.strokeStyle = '#DADCE0';
    this.ctx.lineWidth = 2;
    this.ctx.beginPath();
    this.ctx.roundRect(barX, barY, barWidth, barHeight, 10);
    this.ctx.stroke();
    
    // Texto de calorias
    this.ctx.fillStyle = this.HUD_TEXT;
    this.ctx.font = 'bold 16px "Google Sans", Arial, sans-serif';
    const calText = `${Math.round(calories)}/${this.MAX_CALORIES} kcal`;
    const calTextWidth = this.ctx.measureText(calText).width;
    this.ctx.fillText(calText, this.canvas.width / 2 - calTextWidth / 2, barY + barHeight + 20);
    
    // Timer com estilo Google
    this.ctx.fillStyle = this.HUD_TEXT;
    this.ctx.font = 'bold 24px "Google Sans", Arial, sans-serif';
    const timeText = `⏱️ ${Math.ceil(this.timeRemaining)}s`;
    this.ctx.fillText(timeText, 20, 38);
    
    // Dia com estilo Google
    this.ctx.font = 'bold 16px "Google Sans", Arial, sans-serif';
    const dayText = `Dia ${this.gameState.day}`;
    const dayTextWidth = this.ctx.measureText(dayText).width;
    this.ctx.fillText(dayText, this.canvas.width - dayTextWidth - 20, 38);
    
    // Desenhar comida com sombra e destaque
    if (this.currentFood) {
      const foodSprite = this.foodImages.get(this.currentFood.name);
      
      // Sombra da comida
      this.ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
      this.ctx.beginPath();
      this.ctx.arc(
        this.currentFood.x + this.cellSize / 2,
        this.currentFood.y + this.cellSize / 2 + 2,
        this.cellSize / 2,
        0,
        Math.PI * 2
      );
      this.ctx.fill();
      
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
        this.ctx.arc(
          this.currentFood.x + this.cellSize / 2,
          this.currentFood.y + this.cellSize / 2,
          this.cellSize / 2 - 2,
          0,
          Math.PI * 2
        );
        this.ctx.fill();
        
        // Borda branca
        this.ctx.strokeStyle = '#FFFFFF';
        this.ctx.lineWidth = 2;
        this.ctx.stroke();
        
        // Brilho
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
        this.ctx.beginPath();
        this.ctx.arc(
          this.currentFood.x + this.cellSize / 3,
          this.currentFood.y + this.cellSize / 3,
          this.cellSize / 6,
          0,
          Math.PI * 2
        );
        this.ctx.fill();
      }
      
      // Label de calorias com fundo
      const calText = `${this.currentFood.calories} cal`;
      this.ctx.font = 'bold 11px "Google Sans", Arial, sans-serif';
      const textWidth = this.ctx.measureText(calText).width;
      
      // Fundo do label
      this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
      this.ctx.beginPath();
      this.ctx.roundRect(
        this.currentFood.x + this.cellSize / 2 - textWidth / 2 - 4,
        this.currentFood.y + this.cellSize + 2,
        textWidth + 8,
        16,
        4
      );
      this.ctx.fill();
      
      // Texto
      this.ctx.fillStyle = '#FFFFFF';
      this.ctx.fillText(
        calText,
        this.currentFood.x + this.cellSize / 2 - textWidth / 2,
        this.currentFood.y + this.cellSize + 13
      );
    }
    
    // Desenhar cobra com estilo moderno
    this.snake.forEach((segment, index) => {
      if (index === 0) {
        // Cabeça da cobra (0.9x do tamanho da célula, centrada)
        const headSize = this.cellSize * 0.9;
        const headOffset = (this.cellSize - headSize) / 2;
        
        if (this.snakeHeadImage && this.snakeHeadImage.complete) {
          this.ctx.save();
          this.ctx.translate(segment.x + this.cellSize / 2, segment.y + this.cellSize / 2);
          
          if (this.direction.x === 1) this.ctx.rotate(0);
          else if (this.direction.x === -1) this.ctx.rotate(Math.PI);
          else if (this.direction.y === -1) this.ctx.rotate(-Math.PI / 2);
          else if (this.direction.y === 1) this.ctx.rotate(Math.PI / 2);
          
          this.ctx.drawImage(
            this.snakeHeadImage,
            -headSize / 2,
            -headSize / 2,
            headSize,
            headSize
          );
          this.ctx.restore();
        } else {
          // Cabeça laranja vibrante
          this.ctx.fillStyle = this.SNAKE_HEAD_COLOR;
          this.ctx.beginPath();
          this.ctx.roundRect(segment.x + headOffset, segment.y + headOffset, headSize, headSize, 6);
          this.ctx.fill();
          
          // Olhos brancos (ajustados para o novo tamanho)
          this.ctx.fillStyle = '#FFFFFF';
          const eyeSize = Math.max(3, Math.floor(headSize / 6));
          const eyeOffsetFromEdge = headSize * 0.65;
          const eyeMarginFromEdge = headSize * 0.25;
          
          if (this.direction.x === 1) {
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeOffsetFromEdge, segment.y + headOffset + eyeMarginFromEdge, eyeSize, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeOffsetFromEdge, segment.y + headOffset + eyeOffsetFromEdge, eyeSize, 0, Math.PI * 2);
            this.ctx.fill();
          } else if (this.direction.x === -1) {
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeMarginFromEdge, segment.y + headOffset + eyeMarginFromEdge, eyeSize, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeMarginFromEdge, segment.y + headOffset + eyeOffsetFromEdge, eyeSize, 0, Math.PI * 2);
            this.ctx.fill();
          } else if (this.direction.y === -1) {
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeMarginFromEdge, segment.y + headOffset + eyeMarginFromEdge, eyeSize, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeOffsetFromEdge, segment.y + headOffset + eyeMarginFromEdge, eyeSize, 0, Math.PI * 2);
            this.ctx.fill();
          } else if (this.direction.y === 1) {
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeMarginFromEdge, segment.y + headOffset + eyeOffsetFromEdge, eyeSize, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeOffsetFromEdge, segment.y + headOffset + eyeOffsetFromEdge, eyeSize, 0, Math.PI * 2);
            this.ctx.fill();
          }
          
          // Pupilas pretas (ajustadas para o novo tamanho)
          this.ctx.fillStyle = '#202124';
          const pupilSize = Math.max(1, Math.floor(eyeSize / 2));
          
          if (this.direction.x === 1) {
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeOffsetFromEdge, segment.y + headOffset + eyeMarginFromEdge, pupilSize, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeOffsetFromEdge, segment.y + headOffset + eyeOffsetFromEdge, pupilSize, 0, Math.PI * 2);
            this.ctx.fill();
          } else if (this.direction.x === -1) {
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeMarginFromEdge, segment.y + headOffset + eyeMarginFromEdge, pupilSize, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeMarginFromEdge, segment.y + headOffset + eyeOffsetFromEdge, pupilSize, 0, Math.PI * 2);
            this.ctx.fill();
          } else if (this.direction.y === -1) {
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeMarginFromEdge, segment.y + headOffset + eyeMarginFromEdge, pupilSize, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeOffsetFromEdge, segment.y + headOffset + eyeMarginFromEdge, pupilSize, 0, Math.PI * 2);
            this.ctx.fill();
          } else if (this.direction.y === 1) {
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeMarginFromEdge, segment.y + headOffset + eyeOffsetFromEdge, pupilSize, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.beginPath();
            this.ctx.arc(segment.x + headOffset + eyeOffsetFromEdge, segment.y + headOffset + eyeOffsetFromEdge, pupilSize, 0, Math.PI * 2);
            this.ctx.fill();
          }
        }
      } else {
        // Corpo da cobra com gradiente sutil
        const segmentAlpha = 1 - (index / this.snake.length) * 0.3;
        this.ctx.fillStyle = this.SNAKE_BODY_COLOR;
        this.ctx.globalAlpha = segmentAlpha;
        this.ctx.beginPath();
        this.ctx.roundRect(segment.x + 2, segment.y + 2, this.cellSize - 4, this.cellSize - 4, 5);
        this.ctx.fill();
        this.ctx.globalAlpha = 1;
        
        // Destaque no corpo
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        this.ctx.beginPath();
        this.ctx.roundRect(segment.x + 3, segment.y + 3, this.cellSize - 10, this.cellSize - 10, 3);
        this.ctx.fill();
      }
    });
    
    // Instruções com estilo moderno
    this.ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    this.ctx.font = '13px "Google Sans", Arial, sans-serif';
    const instructionText = 'Use as setas ↑ ↓ ← → para controlar a cobra';
    const instructionWidth = this.ctx.measureText(instructionText).width;
    
    // Fundo semi-transparente
    this.ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
    this.ctx.beginPath();
    this.ctx.roundRect(
      this.canvas.width / 2 - instructionWidth / 2 - 8,
      this.canvas.height - 26,
      instructionWidth + 16,
      20,
      10
    );
    this.ctx.fill();
    
    // Texto das instruções
    this.ctx.fillStyle = '#FFFFFF';
    this.ctx.fillText(
      instructionText,
      this.canvas.width / 2 - instructionWidth / 2,
      this.canvas.height - 12
    );
  }
  
  private getFoodColor(healthColor: string): string {
    switch (healthColor) {
      case 'green': return '#34A853'; // Verde Google
      case 'yellow': return '#FBBC04'; // Amarelo Google
      case 'orange': return '#FF6D00'; // Laranja vibrante
      default: return '#9AA0A6'; // Cinza Google
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