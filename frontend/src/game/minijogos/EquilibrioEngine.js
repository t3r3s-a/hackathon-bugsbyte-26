export class EquilibrioEngine {
    constructor(canvas, calorias) {
        this.ctx = canvas.getContext('2d');
        this.pivo = { x: canvas.width / 2, y: canvas.height - 100 };
        this.num_segmentos = Math.max(3, Math.floor(calorias / 100));
        this.angulo = 0;
        this.vel_angular = 0;
        this.tempo = 10;
        this.finalizado = false;
        this.resultado = 0;
    }

    update(delta, teclas) {
        this.tempo -= delta;
        if (teclas['ArrowLeft']) this.vel_angular -= 0.005;
        if (teclas['ArrowRight']) this.vel_angular += 0.005;

        this.vel_angular *= 0.98; // Atrito
        this.angulo += this.vel_angular;

        if (Math.abs(this.angulo) > 0.8) {
            this.finalizado = true;
            this.resultado = 0;
        } else if (this.tempo <= 0) {
            this.finalizado = true;
            this.resultado = 200;
        }
    }

    draw() {
        this.ctx.fillStyle = "#fff";
        this.ctx.fillRect(0,0,800,600);
        for (let i = 0; i < this.num_segmentos; i++) {
            let yRel = -i * 20;
            let rotX = -yRel * Math.sin(this.angulo);
            let rotY = yRel * Math.cos(this.angulo);
            this.ctx.fillStyle = i === this.num_segmentos-1 ? "darkgreen" : "green";
            this.ctx.fillRect(this.pivo.x + rotX - 10, this.pivo.y + rotY - 10, 20, 20);
        }
    }
}