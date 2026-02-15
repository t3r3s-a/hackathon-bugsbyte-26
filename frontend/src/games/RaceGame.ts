import { GameBase } from './GameBase';
import type { GameConfig, GameResult } from './types';

interface RunnerState {
  position: number;
}

export class RaceGame extends GameBase {
  private runner: RunnerState;
  private goalPosition: number;
  private keyPressCount: number = 0;
  private readonly PIXELS_PER_PRESS = 15; // Pixels que a cobra avança por cada tecla pressionada
  private timeRemaining: number;

  constructor(canvas: HTMLCanvasElement, config: GameConfig) {
    super(canvas, config);
    
    this.goalPosition = this.canvas.width - 100;
    this.runner = {
      position: 50
    };
    this.timeRemaining = 8; // Reduzido de 30 para 8 segundos
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
    
    // Aceitar qualquer seta para mover
    if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
      this.runner.position += this.PIXELS_PER_PRESS;
    }
  }

  protected update(deltaTime: number): void {
    // Não há mais física de velocidade ou stamina
    // A cobra só se move quando pressiona teclas
  }

  protected render(): void {
    // Desenhar fundo simples sem imagem
    this.ctx.fillStyle = '#FFFFFF'; // Fundo branco
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Desenhar chão/pista simples
    const groundY = this.canvas.height - 100;
    this.ctx.fillStyle = '#D3D3D3'; // Cinza claro para a pista
    this.ctx.fillRect(0, groundY, this.canvas.width, 100);

    // Desenhar linha de chegada
    this.ctx.strokeStyle = '#FF0000';
    this.ctx.lineWidth = 4;
    this.ctx.setLineDash([10, 5]);
    this.ctx.beginPath();
    this.ctx.moveTo(this.goalPosition, groundY);
    this.ctx.lineTo(this.goalPosition, this.canvas.height);
    this.ctx.stroke();
    this.ctx.setLineDash([]);

    // Desenhar corredor CENTRADO NO Y
    const runnerY = this.canvas.height / 2; // Centralizado verticalmente
    const runnerSize = 30;
    if (this.assets.runner) {
      this.ctx.drawImage(
        this.assets.runner, 
        this.runner.position - runnerSize / 2, 
        runnerY - runnerSize / 2, 
        runnerSize, 
        runnerSize
      );
    } else {
      this.drawRect(
        this.runner.position - 10, 
        runnerY - 20, 
        20, 
        40, 
        '#FFD700'
      );
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

    // Distância para a meta em metros (10 pixels = 1 metro)
    const distancePixels = Math.max(0, this.goalPosition - this.runner.position);
    const distanceMeters = Math.round(distancePixels / 10);
    
    this.ctx.fillStyle = '#2C3E50';
    this.ctx.font = 'bold 24px Arial';
    this.ctx.fillText(`Distância para a meta: ${distanceMeters}m`, padding, 100);

    // Instruções
    this.ctx.fillStyle = '#7F8C8D';
    this.ctx.font = 'bold 18px Arial';
    this.ctx.fillText('Prima as setas para avançar!', padding, this.canvas.height - 20);
  }

  protected checkGameEnd(): boolean {
    return this.runner.position >= this.goalPosition;
  }

  public cleanup(): void {
    super.cleanup();
  }
}