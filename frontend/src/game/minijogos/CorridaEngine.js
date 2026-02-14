export class CorridaEngine {
    constructor(canvas) {
        this.ctx = canvas.getContext('2d');
        this.player_x = 50;
        this.goal_x = 700;
        this.tempo = 10;
        this.last_key = null;
        this.finalizado = false;
        this.resultado = 0;
    }

    update(delta, teclas) {
        this.tempo -= delta;
        if (teclas['ArrowLeft'] && this.last_key !== 'L') {
            this.player_x += 15;
            this.last_key = 'L';
        }
        if (teclas['ArrowRight'] && this.last_key !== 'R') {
            this.player_x += 15;
            this.last_key = 'R';
        }

        if (this.player_x >= this.goal_x) {
            this.finalizado = true;
            this.resultado = 300;
        } else if (this.tempo <= 0) {
            this.finalizado = true;
            this.resultado = 0;
        }
    }

    draw() {
        this.ctx.fillStyle = "#DD5A11";
        this.ctx.fillRect(0,0,800,600);
        this.ctx.fillStyle = "white";
        this.ctx.fillRect(this.goal_x, 100, 50, 400); // Meta
        this.ctx.fillStyle = "green";
        this.ctx.fillRect(this.player_x, 300, 40, 40); // Jogador
    }
}