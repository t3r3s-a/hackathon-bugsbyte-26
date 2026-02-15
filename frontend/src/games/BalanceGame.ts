// BalanceGame.ts - Jogo de equilíbrio da cobra no pau

import { GameBase } from './GameBase';
import type { GameConfig, Vector2D } from './types';

export class BalanceGame extends GameBase {
  // Constantes do jogo
  private readonly GROUND_HEIGHT = 100;
  private readonly CELL_SIZE = 20;

  // Estado da cobra
  private numSegments: number;
  private pivot: Vector2D;
  private relativePositions: Vector2D[] = [];
  private angle: number = 0;
  private angularVelocity: number = 0;

  // Sistema de perturbação (ventos)
  private readonly PERTURBATION_FORCE = 0.02;
  private readonly PERTURBATION_INTERVAL = 30;
  private perturbationTimer: number = 0;
  private perturbationDirection: number = 0;

  // Cores
  private readonly COLORS = {
    snakeBody: '#F97316',    // Laranja claro
    snakeHead: '#BE4B00',    // Laranja escuro
    perturbationArrow: '#DC2626'  // Vermelho
  };

  constructor(canvas: HTMLCanvasElement, config: GameConfig) {
    super(canvas, config);

    // Calcular número de segmentos baseado nas calorias
    this.numSegments = Math.max(1, Math.floor(config.calories / 100));

    // Definir ponto de pivô (base da cobra)
    this.pivot = {
      x: config.canvasWidth / 2,
      y: config.canvasHeight - this.GROUND_HEIGHT
    };

    // Construir posições relativas (da cabeça para a base)
    // A cabeça é o segmento mais distante (índice 0)
    for (let i = this.numSegments - 1; i >= 0; i--) {
      this.relativePositions.push({
        x: 0,
        y: -i * this.CELL_SIZE
      });
    }

    this.timeRemaining = 10.0; // 10 segundos de duração
  }

  protected async loadAssets(): Promise<void> {
    try {
      this.assets.snakeHead = await this.loadImage('/assets/cabeca_snake.png');
      this.assets.background = await this.loadImage('/assets/background_equilibrio.png');
      this.assets.ground = await this.loadImage('/assets/chao_equilibrio.png');
    } catch (error) {
      console.warn('Algumas imagens não foram carregadas, usando gráficos simples');
    }
  }

  protected update(deltaTime: number): void {
    // Controle do jogador (rotação)
    if (this.inputState.left) {
      this.angularVelocity -= 0.005;
    }
    if (this.inputState.right) {
      this.angularVelocity += 0.005;
    }

    // Sistema de perturbação (ventos aleatórios)
    this.perturbationTimer++;
    if (this.perturbationTimer >= this.PERTURBATION_INTERVAL) {
      this.perturbationTimer = 0;
      // Escolher direção aleatória (mais chance de ter vento)
      const options = [-1, -1, 0, 1, 1];
      this.perturbationDirection = options[Math.floor(Math.random() * options.length)];
      this.angularVelocity += this.perturbationDirection * this.PERTURBATION_FORCE;
    }

    // Aplicar fricção
    this.angularVelocity *= 0.98;

    // Atualizar ângulo
    this.angle += this.angularVelocity;
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
    if (this.assets.ground) {
      this.ctx.drawImage(
        this.assets.ground,
        10,
        this.canvas.height - this.GROUND_HEIGHT,
        this.canvas.width,
        this.GROUND_HEIGHT
      );
    } else {
      this.drawRect(
        0,
        this.canvas.height - this.GROUND_HEIGHT,
        this.canvas.width,
        this.GROUND_HEIGHT,
        '#8B4513'
      );
    }

    // Desenhar segmentos da cobra (da base para a cabeça)
    for (let i = this.numSegments - 1; i >= 0; i--) {
      const relPos = this.relativePositions[i];
      const rotated = this.rotatePoint(relPos, this.angle);
      const x = this.pivot.x + rotated.x;
      const y = this.pivot.y + rotated.y;

      if (i === 0) {
        // Desenhar cabeça
        if (this.assets.snakeHead) {
          // Redimensionar e rotacionar a cabeça
          const scaledSize = Math.floor(this.CELL_SIZE * 0.8);
          this.ctx.save();
          this.ctx.translate(x, y);
          this.ctx.rotate(-this.angle - Math.PI / 2); // -90 graus extra
          this.ctx.drawImage(
            this.assets.snakeHead,
            -scaledSize / 2,
            -scaledSize / 2,
            scaledSize,
            scaledSize
          );
          this.ctx.restore();
        } else {
          this.drawRect(
            x - this.CELL_SIZE / 2,
            y - this.CELL_SIZE / 2,
            this.CELL_SIZE,
            this.CELL_SIZE,
            this.COLORS.snakeHead
          );
        }
      } else {
        // Desenhar corpo
        this.drawRectWithBorder(
          x - this.CELL_SIZE / 2,
          y - this.CELL_SIZE / 2,
          this.CELL_SIZE,
          this.CELL_SIZE,
          this.COLORS.snakeBody,
          '#8B4513',
          2
        );
      }
    }

    // Desenhar seta de perturbação (vento)
    if (this.perturbationDirection !== 0) {
      const arrowStart = {
        x: this.pivot.x + this.perturbationDirection * 80,
        y: this.pivot.y + 30
      };
      const arrowEnd = {
        x: arrowStart.x + this.perturbationDirection * 75,
        y: arrowStart.y
      };

      // Linha da seta
      this.ctx.strokeStyle = this.COLORS.perturbationArrow;
      this.ctx.lineWidth = 4;
      this.ctx.beginPath();
      this.ctx.moveTo(arrowStart.x, arrowStart.y);
      this.ctx.lineTo(arrowEnd.x, arrowEnd.y);
      this.ctx.stroke();

      // Ponta da seta
      this.ctx.fillStyle = this.COLORS.perturbationArrow;
      this.ctx.beginPath();
      if (this.perturbationDirection > 0) {
        // Seta para direita
        this.ctx.moveTo(arrowEnd.x, arrowEnd.y);
        this.ctx.lineTo(arrowEnd.x - 10, arrowEnd.y - 5);
        this.ctx.lineTo(arrowEnd.x - 10, arrowEnd.y + 5);
      } else {
        // Seta para esquerda
        this.ctx.moveTo(arrowEnd.x, arrowEnd.y);
        this.ctx.lineTo(arrowEnd.x + 10, arrowEnd.y - 5);
        this.ctx.lineTo(arrowEnd.x + 10, arrowEnd.y + 5);
      }
      this.ctx.closePath();
      this.ctx.fill();
    }
  }

  protected checkGameEnd(): boolean {
    // O jogo termina se a cobra cair muito (ângulo > 0.9 radianos ≈ 51.5 graus)
    return Math.abs(this.angle) > 0.9;
  }

  private rotatePoint(point: Vector2D, angle: number): Vector2D {
    const cos = Math.cos(angle);
    const sin = Math.sin(angle);
    return {
      x: point.x * cos - point.y * sin,
      y: point.x * sin + point.y * cos
    };
  }
}
