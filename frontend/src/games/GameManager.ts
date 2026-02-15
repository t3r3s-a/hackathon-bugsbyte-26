// GameManager.ts - Gerenciador de jogos

import { GameBase } from './GameBase';
import { SnakeJumpGame } from './SnakeJumpGame';
import { BalanceGame } from './BalanceGame';
import { RaceGame } from './RaceGame';
import type { GameConfig, GameResult, GameType } from './types';

export class GameManager {
  private currentGame: GameBase | null = null;
  private canvas: HTMLCanvasElement;
  private config: GameConfig;

  constructor(canvas: HTMLCanvasElement, config: GameConfig) {
    this.canvas = canvas;
    this.config = config;
  }

  /**
   * Inicia um jogo específico
   * @param gameType Tipo do jogo a iniciar
   * @returns Promise que resolve com o resultado do jogo
   */
  public async startGame(gameType: GameType): Promise<GameResult> {
    // Limpar jogo anterior se existir
    if (this.currentGame) {
      this.currentGame.cleanup();
    }

    // Criar novo jogo baseado no tipo
    switch (gameType) {
      case 'jump':
        this.currentGame = new SnakeJumpGame(this.canvas, this.config);
        break;
      case 'balance':
        this.currentGame = new BalanceGame(this.canvas, this.config);
        break;
      case 'race':
        this.currentGame = new RaceGame(this.canvas, this.config);
        break;
      default:
        throw new Error(`Tipo de jogo desconhecido: ${gameType}`);
    }

    // Iniciar o jogo e aguardar resultado
    return await this.currentGame.start();
  }

  /**
   * Para o jogo atual
   */
  public stopGame(): void {
    if (this.currentGame) {
      this.currentGame.stop();
    }
  }

  /**
   * Limpa recursos do jogo atual
   */
  public cleanup(): void {
    if (this.currentGame) {
      this.currentGame.cleanup();
      this.currentGame = null;
    }
  }

  /**
   * Atualiza a configuração (por exemplo, se as calorias mudarem)
   */
  public updateConfig(config: Partial<GameConfig>): void {
    this.config = { ...this.config, ...config };
  }

  /**
   * Obtém o jogo atual
   */
  public getCurrentGame(): GameBase | null {
    return this.currentGame;
  }
}
