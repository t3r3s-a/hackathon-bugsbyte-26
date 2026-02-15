// GameBase.ts - Classe base abstrata para todos os jogos

import type { GameConfig, GameResult, GameState, ImageAssets, InputState } from './types';

export abstract class GameBase {
  protected canvas: HTMLCanvasElement;
  protected ctx: CanvasRenderingContext2D;
  protected config: GameConfig;
  protected state: GameState;
  protected timeRemaining: number;
  protected animationFrameId: number | null = null;
  protected lastFrameTime: number = 0;
  protected assets: ImageAssets = {};
  protected inputState: InputState = {
    left: false,
    right: false,
    space: false,
    jump: false
  };

  constructor(canvas: HTMLCanvasElement, config: GameConfig) {
    this.canvas = canvas;
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      throw new Error('Não foi possível obter contexto 2D do canvas');
    }
    this.ctx = ctx;
    this.config = config;
    this.state = 'playing' as GameState;
    this.timeRemaining = 20.0; // 20 segundos por padrão
    
    this.setupCanvas();
    this.setupInput();
  }

  protected setupCanvas(): void {
    this.canvas.width = this.config.canvasWidth;
    this.canvas.height = this.config.canvasHeight;
    this.ctx.imageSmoothingEnabled = true;
  }

  protected setupInput(): void {
    window.addEventListener('keydown', this.handleKeyDown.bind(this));
    window.addEventListener('keyup', this.handleKeyUp.bind(this));
  }

  protected handleKeyDown(e: KeyboardEvent): void {
    switch (e.key) {
      case 'ArrowLeft':
        this.inputState.left = true;
        e.preventDefault();
        break;
      case 'ArrowRight':
        this.inputState.right = true;
        e.preventDefault();
        break;
      case ' ':
        this.inputState.space = true;
        this.inputState.jump = true;
        e.preventDefault();
        break;
    }
  }

  protected handleKeyUp(e: KeyboardEvent): void {
    switch (e.key) {
      case 'ArrowLeft':
        this.inputState.left = false;
        break;
      case 'ArrowRight':
        this.inputState.right = false;
        break;
      case ' ':
        this.inputState.space = false;
        break;
    }
  }

  protected clearCanvas(): void {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
  }

  protected drawTimer(): void {
    this.ctx.save();
    this.ctx.font = '24px Arial';
    this.ctx.fillStyle = '#000000';
    this.ctx.fillText(`${this.timeRemaining.toFixed(1)}s`, 20, 40);
    this.ctx.restore();
  }

  // Método auxiliar para desenhar retângulos
  protected drawRect(x: number, y: number, width: number, height: number, color: string): void {
    this.ctx.fillStyle = color;
    this.ctx.fillRect(x, y, width, height);
  }

  // Método auxiliar para desenhar retângulos com borda
  protected drawRectWithBorder(
    x: number, 
    y: number, 
    width: number, 
    height: number, 
    fillColor: string, 
    borderColor: string, 
    borderWidth: number = 2
  ): void {
    this.ctx.fillStyle = fillColor;
    this.ctx.fillRect(x, y, width, height);
    this.ctx.strokeStyle = borderColor;
    this.ctx.lineWidth = borderWidth;
    this.ctx.strokeRect(x, y, width, height);
  }

  // Métodos abstratos que devem ser implementados pelas subclasses
  protected abstract loadAssets(): Promise<void>;
  protected abstract update(deltaTime: number): void;
  protected abstract render(): void;
  protected abstract checkGameEnd(): boolean;

  // Loop principal do jogo
  protected gameLoop(timestamp: number): void {
    if (this.state !== 'playing') {
      return;
    }

    const deltaTime = (timestamp - this.lastFrameTime) / 1000; // Converter para segundos
    this.lastFrameTime = timestamp;

    // Atualizar estado do jogo
    this.update(deltaTime);
    this.timeRemaining -= deltaTime;

    // Verificar condições de fim de jogo
    if (this.checkGameEnd() || this.timeRemaining <= 0) {
      this.stop();
      return;
    }

    // Renderizar
    this.clearCanvas();
    this.render();
    this.drawTimer();

    // Continuar o loop
    this.animationFrameId = requestAnimationFrame(this.gameLoop.bind(this));
  }

  public async start(): Promise<GameResult> {
    await this.loadAssets();
    this.state = 'playing' as GameState;
    this.lastFrameTime = performance.now();
    this.animationFrameId = requestAnimationFrame(this.gameLoop.bind(this));

    // Retornar uma Promise que resolve quando o jogo termina
    return new Promise((resolve) => {
      const checkEnd = setInterval(() => {
        if (this.state !== 'playing') {
          clearInterval(checkEnd);
          
          const result: GameResult = {
            success: this.timeRemaining > 0,
            caloriesLost: this.timeRemaining > 0 ? Math.floor(Math.random() * 101) + 100 : 0,
            timeRemaining: this.timeRemaining
          };
          
          resolve(result);
        }
      }, 100);
    });
  }

  public stop(): void {
    this.state = this.timeRemaining > 0 ? 'victory' as GameState : 'game_over' as GameState;
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }

  public cleanup(): void {
    this.stop();
    window.removeEventListener('keydown', this.handleKeyDown.bind(this));
    window.removeEventListener('keyup', this.handleKeyUp.bind(this));
  }

  // Método auxiliar para carregar imagens
  protected loadImage(src: string): Promise<HTMLImageElement> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = () => reject(new Error(`Falha ao carregar imagem: ${src}`));
      img.src = src;
    });
  }
}
