export class DinoEngine {
    constructor(canvas) {
        this.ctx = canvas.getContext('2d');
        this.dino_y = 500;
        this.vel_y = 0;
        this.obstaculo_x = 800;
        this.tempo = 10;
        this.finalizado = false;
        this.resultado = 0;
    }

    update(delta, teclas) {
        this.tempo -= delta;
        if (teclas['ArrowUp'] && this.dino_y >= 500) this.vel_y = -15;
        
        this.vel_y += 0.8; // Gravidade
        this.dino_y += this.vel_y;
        if (this.dino_y > 500) this.dino_y = 500;

        this.obstaculo_x -= 8;
        if (this.obstaculo_x < -20) this.obstaculo_x = 800;

        // Colisão simples
        if (this.obstaculo_x < 120 && this.obstaculo_x > 80 && this.dino_y > 460) {
            this.finalizado = true;
            this.resultado = 0;
        }

        if (this.tempo <= 0) {
            this.finalizado = true;
            this.resultado = 150;
        }
    }

    draw() {
        this.ctx.fillStyle = "#333";
        this.ctx.fillRect(0,0,800,600);
        this.ctx.fillStyle = "green";
        this.ctx.fillRect(100, this.dino_y, 40, 40); // Dino
        this.ctx.fillStyle = "red";
        this.ctx.fillRect(this.obstaculo_x, 500, 20, 40); // Obstáculo
    }
}