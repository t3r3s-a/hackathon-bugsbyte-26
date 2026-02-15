import { GameBase } from './GameBase';
import type { GameConfig, GameResult } from './types';

interface RunnerState {
  position: number;
  speed: number;
  stamina: number;
  maxStamina: number;
}

export class RaceGame extends GameBase {
  private runner: RunnerState;
  private goalPosition: number;
  private keyPressCount: number = 0;
  private lastKeyTime: number = 0;
  private readonly MAX_SPEED = 10;
  private readonly STAMINA_DRAIN_RATE = 20;
  private readonly STAMINA_RECOVERY_RATE = 30;
  private readonly SPEED_PER_PRESS = 0.5;

  constructor(canvas: HTMLCanvasElement, config: GameConfig) {
    super(canvas, config);
    
    this.goalPosition = this.canvas.width - 100;
    this.runner = {
      position: 50,
      speed: 0,
      stamina: 100,
      maxStamina: 100
    };
  }

  protected async loadAssets(): Promise<void> {
    try {
      this.assets.background = await this.loadImage('/src/assets/games/background_equilibrio.png');
      this.assets.ground = await this.loadImage('/src/assets/games/chao_equilibrio.png');
      this.assets.runner = await this.loadImage('/src/assets/games/cabeca_snake.png');
    } catch (error) {
      console.warn('Erro ao carregar assets da corrida:', error);
    }
  }

  protected handleKeyDown(e: KeyboardEvent): void {
    super.handleKeyDown(e);
    
    const currentTime = performance.now();
    const timeSinceLastPress = currentTime - this.lastKeyTime;
    
    // Aceitar qualquer seta para correr
    if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
      this.keyPressCount++;
      this.lastKeyTime = currentTime;
      
      // Aumentar velocidade se tiver stamina
      if (this.runner.stamina > 0) {
        this.runner.speed = Math.min(this.MAX_SPEED, this.runner.speed + this.SPEED_PER_PRESS);
        
        // Bonus se pressionar rápido (< 200ms)
        if (timeSinceLastPress < 200 && timeSinceLastPress > 0) {
          this.runner.speed = Math.min(this.MAX_SPEED, this.runner.speed + 0.3);
        }
      }
    }
  }

  protected update(deltaTime: number): void {
    // Drenar stamina quando correndo
    if (this.runner.speed > 0) {
      this.runner.stamina -= this.STAMINA_DRAIN_RATE * deltaTime;
      this.runner.stamina = Math.max(0, this.runner.stamina);
    } else {
      // Recuperar stamina quando parado
      this.runner.stamina += this.STAMINA_RECOVERY_RATE * deltaTime;
      this.runner.stamina = Math.min(this.runner.maxStamina, this.runner.stamina);
    }

    // Reduzir velocidade gradualmente (fadiga)
    this.runner.speed = Math.max(0, this.runner.speed - 2 * deltaTime);

    // Se stamina acabou, velocidade diminui drasticamente
    if (this.runner.stamina <= 0) {
      this.runner.speed = Math.max(0, this.runner.speed - 4 * deltaTime);
    }

    // Mover corredor
    this.runner.position += this.runner.speed * 60 * deltaTime;
  }

  protected render(): void {
    // Desenhar fundo
    if (this.assets.background) {
      this.ctx.drawImage(this.assets.background, 0, 0, this.canvas.width, this.canvas.height);
    } else {
      const gradient = this.ctx.createLinearGradient(0, 0, 0, this.canvas.height);
      gradient.addColorStop(0, '#87CEEB');
      gradient.addColorStop(1, '#98FB98');
      this.ctx.fillStyle = gradient;
      this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }

    // Desenhar chão/pista
    if (this.assets.ground) {
      this.ctx.drawImage(this.assets.ground, 0, this.canvas.height - 100, this.canvas.width, 100);
    } else {
      this.drawRect(0, this.canvas.height - 50, this.canvas.width, 50, '#8B4513');
    }

    // Desenhar linha de chegada
    this.ctx.strokeStyle = '#FF0000';
    this.ctx.lineWidth = 4;
    this.ctx.setLineDash([10, 5]);
    this.ctx.beginPath();
    this.ctx.moveTo(this.goalPosition, this.canvas.height - 100);
    this.ctx.lineTo(this.goalPosition, this.canvas.height - 50);
    this.ctx.stroke();
    this.ctx.setLineDash([]);

    // Desenhar corredor
    const runnerY = this.canvas.height - 90;
    if (this.assets.runner) {
      this.ctx.drawImage(this.assets.runner, this.runner.position - 15, runnerY - 15, 30, 30);
    } else {
      this.drawRect(this.runner.position - 10, runnerY - 20, 20, 40, '#FFD700');
      // Adicionar "olhos"
      this.ctx.fillStyle = '#000000';
      this.ctx.fillRect(this.runner.position - 6, runnerY - 15, 3, 3);
      this.ctx.fillRect(this.runner.position + 3, runnerY - 15, 3, 3);
    }

    // Desenhar UI
    this.renderUI();
  }

  private renderUI(): void {
    const padding = 20;
    const uiY = 20;

    // Barra de stamina
    const staminaBarWidth = 200;
    const staminaBarHeight = 20;
    const staminaX = padding;

    this.ctx.fillStyle = '#FFFFFF';
    this.ctx.fillRect(staminaX - 2, uiY - 2, staminaBarWidth + 4, staminaBarHeight + 4);
    
    this.ctx.fillStyle = '#E74C3C';
    this.ctx.fillRect(staminaX, uiY, staminaBarWidth, staminaBarHeight);
    
    const staminaPercent = this.runner.stamina / this.runner.maxStamina;
    this.ctx.fillStyle = staminaPercent > 0.3 ? '#2ECC71' : '#F39C12';
    this.ctx.fillRect(staminaX, uiY, staminaBarWidth * staminaPercent, staminaBarHeight);

    this.ctx.fillStyle = '#000000';
    this.ctx.font = '14px Arial';
    this.ctx.fillText('Stamina', staminaX, uiY - 5);

    // Velocidade atual
    const speedY = uiY + 40;
    this.ctx.fillStyle = '#2C3E50';
    this.ctx.font = '18px Arial';
    this.ctx.fillText(`Velocidade: ${this.runner.speed.toFixed(1)}`, padding, speedY);

    // Contador de teclas
    this.ctx.fillText(`Teclas: ${this.keyPressCount}`, padding, speedY + 30);

    // Distância para a meta
    const distance = Math.max(0, this.goalPosition - this.runner.position);
    const distanceY = speedY + 60;
    this.ctx.fillStyle = '#2C3E50';
    this.ctx.font = '16px Arial';
    this.ctx.fillText(`Meta: ${Math.round(distance)}m`, padding, distanceY);

    // Instruções
    this.ctx.fillStyle = '#7F8C8D';
    this.ctx.font = 'bold 16px Arial';
    this.ctx.fillText('Prima as setas rapidamente!', padding, this.canvas.height - 30);
    
    // Dica extra
    this.ctx.font = '14px Arial';
    this.ctx.fillText('Quanto mais rápido pressionares, mais rápido corres!', padding, this.canvas.height - 10);
  }

  protected checkGameEnd(): boolean {
    return this.runner.position >= this.goalPosition;
  }

  public cleanup(): void {
    super.cleanup();
  }
}