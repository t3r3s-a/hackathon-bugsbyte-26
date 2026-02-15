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
  private lastKeyPressed: 'left' | 'right' | null = null; // Rastrear última tecla pressionada
  
  // Corpo da cobra baseado nas calorias
  private numSegments: number;
  private readonly SEGMENT_DISTANCE = 30; // Distância entre segmentos
  private readonly SEGMENT_SIZE = 25; // Tamanho de cada segmento
  
  // Cores
  private readonly SNAKE_HEAD_COLOR = '#FF8C00'; // Laranja escuro
  private readonly SNAKE_BODY_COLOR = '#FFA500'; // Laranja claro

  constructor(canvas: HTMLCanvasElement, config: GameConfig) {
    super(canvas, config);
    
    this.goalPosition = this.canvas.width - 100;
    this.runner = {
      position: 50
    };
    this.timeRemaining = 8; // Reduzido de 30 para 8 segundos
    
    // Calcular número de segmentos baseado nas calorias
    this.numSegments = Math.max(1, Math.floor((config.calories || 300) / 100));
  }

  protected async loadAssets(): Promise<void> {
    try {
      this.assets.background = await this.loadImage('/src/assets/games/background_racegame.png');
      this.assets.runner = await this.loadImage('/src/assets/games/cabeca_snake.png');
      this.assets.finishLine = await this.loadImage('/src/assets/games/finish_line_racegame.png');
    } catch (error) {
      console.warn('Erro ao carregar assets da corrida:', error);
    }
  }

  protected handleKeyDown(e: KeyboardEvent): void {
    super.handleKeyDown(e);
    
    // Sistema de teclas alternadas: esquerda -> direita -> esquerda -> direita...
    if (e.key === 'ArrowLeft') {
      // Só aceita se a última tecla foi direita OU se é a primeira tecla
      if (this.lastKeyPressed === 'right' || this.lastKeyPressed === null) {
        this.runner.position += this.PIXELS_PER_PRESS;
        this.lastKeyPressed = 'left';
        this.keyPressCount++;
      }
    } else if (e.key === 'ArrowRight') {
      // Só aceita se a última tecla foi esquerda OU se é a primeira tecla
      if (this.lastKeyPressed === 'left' || this.lastKeyPressed === null) {
        this.runner.position += this.PIXELS_PER_PRESS;
        this.lastKeyPressed = 'right';
        this.keyPressCount++;
      }
    }
  }

  protected update(deltaTime: number): void {
    // Não há mais física de velocidade ou stamina
    // A cobra só se move quando pressiona teclas
  }

  protected render(): void {
    // Desenhar fundo da corrida
    if (this.assets.background) {
      this.ctx.drawImage(this.assets.background, 0, 0, this.canvas.width, this.canvas.height);
    } else {
      // Fallback: fundo azul claro
      this.ctx.fillStyle = '#ADD8E6';
      this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }

    // Desenhar linha de chegada
    if (this.assets.finishLine) {

      const finishLineWidth = 320;
      const finishLineHeight = 100;
      
      this.ctx.save();
      this.ctx.translate(this.goalPosition, this.canvas.height / 2 - 5);
      this.ctx.rotate(Math.PI / 2);
      this.ctx.drawImage(
        this.assets.finishLine,
        -finishLineWidth / 2,
        -finishLineHeight / 2,
        finishLineWidth,
        finishLineHeight
      );
      this.ctx.restore();
    } else {
      // Fallback: linha tracejada vermelha centrada
      this.ctx.strokeStyle = '#FF0000';
      this.ctx.lineWidth = 4;
      this.ctx.setLineDash([10, 5]);
      this.ctx.beginPath();
      this.ctx.moveTo(this.goalPosition, this.canvas.height / 2 - 60);
      this.ctx.lineTo(this.goalPosition, this.canvas.height / 2 + 60);
      this.ctx.stroke();
      this.ctx.setLineDash([]);
    }

    // Desenhar cobra CENTRADA NO Y com corpo de segmentos
    const runnerY = this.canvas.height / 2; // Centralizado verticalmente
    
    // Desenhar segmentos do corpo (atrás da cabeça)
    for (let i = 0; i < this.numSegments; i++) {
      const segmentX = this.runner.position - (i + 1) * this.SEGMENT_DISTANCE;
      
      // Desenhar segmento do corpo (laranja)
      this.ctx.fillStyle = this.SNAKE_BODY_COLOR;
      this.ctx.beginPath();
      this.ctx.roundRect(
        segmentX - this.SEGMENT_SIZE / 2,
        runnerY - this.SEGMENT_SIZE / 2,
        this.SEGMENT_SIZE,
        this.SEGMENT_SIZE,
        5
      );
      this.ctx.fill();
      
      // Adicionar destaque no corpo
      this.ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
      this.ctx.beginPath();
      this.ctx.roundRect(
        segmentX - this.SEGMENT_SIZE / 2 + 3,
        runnerY - this.SEGMENT_SIZE / 2 + 3,
        this.SEGMENT_SIZE - 6,
        this.SEGMENT_SIZE - 6,
        3
      );
      this.ctx.fill();
    }
    
    // Desenhar cabeça (na frente) ROTACIONADA 90º
    const headSize = 30;
    if (this.assets.runner) {
      this.ctx.save();
      this.ctx.translate(this.runner.position, runnerY);
      this.ctx.rotate(Math.PI / 2); // Rodar 90 graus (virada para a esquerda)
      this.ctx.drawImage(
        this.assets.runner,
        -headSize / 2,
        -headSize / 2,
        headSize,
        headSize
      );
      this.ctx.restore();
    } else {
      // Fallback: cabeça laranja quadrada
      this.ctx.fillStyle = this.SNAKE_HEAD_COLOR;
      this.ctx.beginPath();
      this.ctx.roundRect(
        this.runner.position - headSize / 2,
        runnerY - headSize / 2,
        headSize,
        headSize,
        6
      );
      this.ctx.fill();
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