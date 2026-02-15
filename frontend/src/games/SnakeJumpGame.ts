// SnakeJumpGame.ts - Jogo da cobra saltando obstáculos (tipo dinossauro do Chrome)

import { GameBase } from './GameBase';
import type { GameConfig } from './types';

interface Obstacle {
  x: number;
  y: number;
  width: number;
  height: number;
}

export class SnakeJumpGame extends GameBase {
  private readonly GROUND_Y: number;
  private readonly GRAVITY = 1.2;
  private readonly JUMP_FORCE = -18;
  private readonly OBSTACLE_SPEED = 7;
  private readonly GROUND_HEIGHT = 80;
  private readonly RUNNER_SIZE = 30;

  private runnerY: number;
  private runnerVelocityY: number = 0;
  private isOnGround: boolean = true;
  private obstacles: Obstacle[] = [];
  private spawnTimer: number = 0;
  private readonly SPAWN_INTERVAL = 80; // Frames entre obstáculos
  private score: number = 0;

  constructor(canvas: HTMLCanvasElement, config: GameConfig) {
    super(canvas, config);
    this.GROUND_Y = this.canvas.height - this.GROUND_HEIGHT - this.RUNNER_SIZE;
    this.runnerY = this.GROUND_Y;
    this.timeRemaining = 30; // 30 segundos para sobreviver
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
    if ((e.key === ' ' || e.key === 'ArrowUp') && this.isOnGround) {
      this.runnerVelocityY = this.JUMP_FORCE;
      this.isOnGround = false;
    }
  }

  protected update(deltaTime: number): void {
    // Física do corredor
    this.runnerVelocityY += this.GRAVITY;
    this.runnerY += this.runnerVelocityY;

    // Verificar se está no chão
    if (this.runnerY >= this.GROUND_Y) {
      this.runnerY = this.GROUND_Y;
      this.runnerVelocityY = 0;
      this.isOnGround = true;
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

    // Desenhar corredor (cobra)
    const runnerX = 100;
    if (this.assets.runner) {
      this.ctx.save();
      this.ctx.translate(runnerX + this.RUNNER_SIZE / 2, this.runnerY + this.RUNNER_SIZE / 2);
      this.ctx.rotate(-Math.PI / 2); // Virado para direita
      this.ctx.drawImage(
        this.assets.runner,
        -this.RUNNER_SIZE / 2,
        -this.RUNNER_SIZE / 2,
        this.RUNNER_SIZE,
        this.RUNNER_SIZE
      );
      this.ctx.restore();
    } else {
      this.drawRect(runnerX, this.runnerY, this.RUNNER_SIZE, this.RUNNER_SIZE, '#FFD700');
      // Olhos
      this.ctx.fillStyle = '#000000';
      this.ctx.fillRect(runnerX + 20, this.runnerY + 8, 4, 4);
      this.ctx.fillRect(runnerX + 20, this.runnerY + 18, 4, 4);
    }

    // UI
    this.renderUI();
  }

  private renderUI(): void {
    const padding = 20;

    // Score
    this.ctx.fillStyle = '#2C3E50';
    this.ctx.font = 'bold 24px Arial';
    this.ctx.fillText(`Score: ${this.score}`, padding, 40);

    // Tempo restante
    this.ctx.fillText(`Tempo: ${Math.ceil(this.timeRemaining)}s`, padding, 70);

    // Instruções
    this.ctx.fillStyle = '#7F8C8D';
    this.ctx.font = 'bold 18px Arial';
    this.ctx.fillText('ESPAÇO ou ↑ para SALTAR', padding, this.canvas.height - 20);
  }

  protected checkGameEnd(): boolean {
    // Verificar colisão com obstáculos
    const runnerX = 100;
    const runnerRect = {
      x: runnerX,
      y: this.runnerY,
      width: this.RUNNER_SIZE,
      height: this.RUNNER_SIZE
    };

    for (const obstacle of this.obstacles) {
      if (this.checkCollision(runnerRect, obstacle)) {
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
    const height = 30 + Math.floor(Math.random() * 40); // 30-70px
    const groundY = this.canvas.height - this.GROUND_HEIGHT;
    
    this.obstacles.push({
      x: this.canvas.width,
      y: groundY - height,
      width: 25,
      height: height
    });
  }

  public cleanup(): void {
    super.cleanup();
  }
}
