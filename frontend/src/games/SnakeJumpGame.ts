// SnakeJumpGame.ts - Jogo da cobra saltando obstáculos (tipo dinossauro do Chrome)

import { GameBase } from './GameBase';
import type { GameConfig } from './types';

interface Obstacle {
  x: number;
  y: number;
  width: number;
  height: number;
}

interface TailSegment {
  y: number;
  velocityY: number;
}

export class SnakeJumpGame extends GameBase {
  private readonly GROUND_Y: number;
  private readonly GRAVITY = 0.8;
  private readonly JUMP_FORCE = -16; // Aumentado de -12 para -16 (salto mais alto)
  private readonly OBSTACLE_SPEED = 6;
  private readonly GROUND_HEIGHT = 80;
  private readonly RUNNER_SIZE = 30; // Aumentado de 20 para 30
  private readonly HEAD_X = 150; // Posição fixa X da cabeça

  // Cabeça
  private headY: number;
  private headVelocityY: number = 0;
  private headOnGround: boolean = true;

  // Cauda (segmentos atrás da cabeça)
  private tailSegments: TailSegment[] = [];
  private numSegments: number = 3; // Baseado nas calorias ATUAIS
  private readonly SEGMENT_DISTANCE = 40; // Aumentado de 30 para 40 (mais espaçamento)
  private readonly DELAY_FRAMES: number;

  // Buffer de inputs para a cauda seguir
  private inputBuffer: boolean[] = [];
  private readonly MAX_BUFFER: number;

  // Calorias atuais
  private currentCalories: number = 300;
  private readonly CALORIES_PER_SECOND = 5;

  // Cores
  private readonly SNAKE_HEAD_COLOR = '#FF8C00'; // Laranja escuro (cabeça)
  private readonly SNAKE_BODY_COLOR = '#FFA500'; // Laranja (corpo)

  private obstacles: Obstacle[] = [];
  private spawnTimer: number = 0;
  private readonly SPAWN_INTERVAL = 90; // Frames entre obstáculos
  private score: number = 0;

  constructor(canvas: HTMLCanvasElement, config: GameConfig) {
    super(canvas, config);
    this.GROUND_Y = this.canvas.height - this.GROUND_HEIGHT - this.RUNNER_SIZE;
    this.headY = this.GROUND_Y;
    this.timeRemaining = 20; // 20 segundos como no Python
    
    // Calorias iniciais
    this.currentCalories = config.calories || 300;
    
    // Calcular número de segmentos baseado nas calorias INICIAIS
    this.numSegments = Math.max(1, Math.floor(this.currentCalories / 100));
    
    // Calcular delay entre segmentos (quanto tempo leva para um segmento percorrer a distância)
    this.DELAY_FRAMES = Math.max(1, Math.floor(this.SEGMENT_DISTANCE / this.OBSTACLE_SPEED));
    
    // Tamanho máximo do buffer
    this.MAX_BUFFER = 30 * this.DELAY_FRAMES + 20; // Buffer grande o suficiente para 30 segmentos
    
    // Inicializar segmentos da cauda
    for (let i = 0; i < this.numSegments; i++) {
      this.tailSegments.push({
        y: this.GROUND_Y,
        velocityY: 0
      });
    }
  }

  protected async loadAssets(): Promise<void> {
    try {
      this.assets.background = await this.loadImage('/src/assets/games/background_dinossaur.png');
      this.assets.ground = await this.loadImage('/src/assets/games/chao_dinossaur.png');
      this.assets.runner = await this.loadImage('/src/assets/games/cabeca_snake.png');
    } catch (error) {
      console.warn('Erro ao carregar assets do dinossauro:', error);
    }
  }

  protected handleKeyDown(e: KeyboardEvent): void {
    super.handleKeyDown(e);
    
    // Saltar com espaço ou seta para cima
    if ((e.key === ' ' || e.key === 'ArrowUp') && this.headOnGround) {
      this.headVelocityY = this.JUMP_FORCE;
      this.headOnGround = false;
    }
  }

  protected update(deltaTime: number): void {
    // Física da cabeça
    this.headVelocityY += this.GRAVITY;
    this.headY += this.headVelocityY;

    // Verificar se está no chão
    if (this.headY >= this.GROUND_Y) {
      this.headY = this.GROUND_Y;
      this.headVelocityY = 0;
      this.headOnGround = true;
    }

    // Atualizar buffer de inputs
    this.inputBuffer.unshift(!this.headOnGround);
    if (this.inputBuffer.length > this.MAX_BUFFER) {
      this.inputBuffer.pop();
    }

    // Atualizar segmentos da cauda
    for (let i = 0; i < this.tailSegments.length; i++) {
      const segment = this.tailSegments[i];
      const bufferIndex = (i + 1) * this.DELAY_FRAMES;
      const shouldJump = this.inputBuffer[bufferIndex] || false;

      if (shouldJump && segment.y >= this.GROUND_Y) {
        segment.velocityY = this.JUMP_FORCE;
      }

      segment.velocityY += this.GRAVITY;
      segment.y += segment.velocityY;

      if (segment.y >= this.GROUND_Y) {
        segment.y = this.GROUND_Y;
        segment.velocityY = 0;
      }
    }

    // Spawnar obstáculos
    this.spawnTimer++;
    if (this.spawnTimer >= this.SPAWN_INTERVAL) {
      this.spawnTimer = 0;
      this.spawnObstacle();
    }

    // Mover obstáculos
    for (const obstacle of this.obstacles) {
      obstacle.x -= this.OBSTACLE_SPEED;
    }

    // Remover obstáculos fora da tela e contar score
    this.obstacles = this.obstacles.filter(obstacle => {
      if (obstacle.x + obstacle.width < 0) {
        this.score += 10;
        return false;
      }
      return true;
    });

    // Reduzir calorias ao longo do tempo
    this.currentCalories -= this.CALORIES_PER_SECOND * (deltaTime / 1000);
    this.currentCalories = Math.max(0, this.currentCalories);

    // Atualizar número de segmentos baseado nas calorias atuais
    const newNumSegments = Math.max(1, Math.floor(this.currentCalories / 100));
    if (newNumSegments !== this.numSegments) {
      if (newNumSegments > this.numSegments) {
        // Adicionar novos segmentos quando calorias aumentam
        const segmentsToAdd = newNumSegments - this.numSegments;
        for (let i = 0; i < segmentsToAdd; i++) {
          this.tailSegments.push({
            y: this.GROUND_Y,
            velocityY: 0
          });
        }
      } else {
        // Remover segmentos quando calorias diminuem
        this.tailSegments = this.tailSegments.slice(0, newNumSegments);
      }
      this.numSegments = newNumSegments;
    }
  }

  protected render(): void {
    // Desenhar fundo
    if (this.assets.background) {
      this.ctx.drawImage(this.assets.background, 0, 0, this.canvas.width, this.canvas.height);
    } else {
      const gradient = this.ctx.createLinearGradient(0, 0, 0, this.canvas.height);
      gradient.addColorStop(0, '#87CEEB');
      gradient.addColorStop(1, '#E0F6FF');
      this.ctx.fillStyle = gradient;
      this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }

    // Desenhar chão
    const groundY = this.canvas.height - this.GROUND_HEIGHT;
    if (this.assets.ground) {
      this.ctx.drawImage(this.assets.ground, 0, groundY, this.canvas.width, this.GROUND_HEIGHT);
    } else {
      this.drawRect(0, groundY, this.canvas.width, this.GROUND_HEIGHT, '#8B4513');
    }

    // Desenhar obstáculos
    this.ctx.fillStyle = '#DC2626';
    for (const obstacle of this.obstacles) {
      this.ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
      
      // Adicionar detalhe aos obstáculos
      this.ctx.fillStyle = '#991B1B';
      this.ctx.fillRect(obstacle.x + 2, obstacle.y + 2, obstacle.width - 4, obstacle.height - 4);
      this.ctx.fillStyle = '#DC2626';
    }

    // Desenhar cabeça (cobra)
    if (this.assets.runner) {
      this.ctx.save();
      this.ctx.translate(this.HEAD_X + this.RUNNER_SIZE / 2, this.headY + this.RUNNER_SIZE / 2);
      this.ctx.rotate(Math.PI / 2); // Girado 180º: de -Math.PI/2 para +Math.PI/2 (virada para a esquerda)
      this.ctx.drawImage(
        this.assets.runner,
        -this.RUNNER_SIZE / 2,
        -this.RUNNER_SIZE / 2,
        this.RUNNER_SIZE,
        this.RUNNER_SIZE
      );
      this.ctx.restore();
    } else {
      this.drawRect(this.HEAD_X, this.headY, this.RUNNER_SIZE, this.RUNNER_SIZE, this.SNAKE_HEAD_COLOR);
      // Olhos
      this.ctx.fillStyle = '#000000';
      this.ctx.fillRect(this.HEAD_X + 14, this.headY + 6, 4, 4);
      this.ctx.fillRect(this.HEAD_X + 14, this.headY + 14, 4, 4);
    }

    // Desenhar segmentos da cauda
    for (let i = 0; i < this.tailSegments.length; i++) {
      const segment = this.tailSegments[i];
      const segmentX = this.HEAD_X - (i + 1) * this.SEGMENT_DISTANCE;

      this.drawRect(segmentX, segment.y, this.RUNNER_SIZE, this.RUNNER_SIZE, this.SNAKE_BODY_COLOR);
    }

    // UI
    this.renderUI();
  }

  private renderUI(): void {
    const padding = 20;



    // Instruções
    this.ctx.fillStyle = '#7F8C8D';
    this.ctx.font = 'bold 18px Arial';
    this.ctx.fillText('ESPAÇO ou ↑ para SALTAR', padding, this.canvas.height - 20);
  }

  protected checkGameEnd(): boolean {
    // Verificar colisão com obstáculos
    const headRect = {
      x: this.HEAD_X,
      y: this.headY,
      width: this.RUNNER_SIZE,
      height: this.RUNNER_SIZE
    };

    for (const obstacle of this.obstacles) {
      if (this.checkCollision(headRect, obstacle)) {
        return true; // Game over
      }
    }

    return false;
  }

  private checkCollision(
    rect1: { x: number; y: number; width: number; height: number },
    rect2: { x: number; y: number; width: number; height: number }
  ): boolean {
    return (
      rect1.x < rect2.x + rect2.width &&
      rect1.x + rect1.width > rect2.x &&
      rect1.y < rect2.y + rect2.height &&
      rect1.y + rect1.height > rect2.y
    );
  }

  private spawnObstacle(): void {
    const height = 40 + Math.floor(Math.random() * 60); // Aumentado de 30-70px para 40-100px
    const groundY = this.canvas.height - this.GROUND_HEIGHT;
    
    this.obstacles.push({
      x: this.canvas.width,
      y: groundY - height,
      width: 35, // Aumentado de 25 para 35
      height: height
    });
  }

  public cleanup(): void {
    super.cleanup();
  }
}
