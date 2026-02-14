export class SnakeEngine {
    constructor(canvas, C) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.C = C;
        
        // 🔥 ADICIONAR CONTROLO DE VELOCIDADE
        this.frameCount = 0;
        this.velocidade = 8; // Quanto MAIOR, mais DEVAGAR (8 = update a cada 8 frames)
        
        this.imgAlimento = new Image();
        this.imgCabeca = new Image();
        
        this.imgCabeca.onload = () => console.log('✅ Imagem cobra_cabeca.png carregada!');
        this.imgCabeca.onerror = () => console.error('❌ Erro ao carregar cobra_cabeca.png');
        
        this.imgAlimento.onload = () => console.log('✅ Imagem maca.png carregada!');
        this.imgAlimento.onerror = () => console.error('❌ Erro ao carregar maca.png');
        
        this.imgCabeca.src = '/assets/cobra_cabeca.png';
        this.imgAlimento.src = '/assets/maca.png';
        
        this.reset_jogo();
    }

    reset_jogo() {
        this.cobra = [[300, 300], [280, 300], [260, 300]];
        this.direcao = "DIREITA";
        this.calorias = this.C.CALORIAS_INICIAL || 100;
        this.pontuacao = 0;
        this.emTransicao = false;
        this.fase_atual = 'fase1';
        this.fase_selecionada = 0;
        this.frameCount = 0; // 🔥 Reset do contador
        this.colocar_alimento();
    }

    colocar_alimento() {
        const maxX = Math.floor(this.C.LARGURA_JANELA / 20);
        const maxY = Math.floor((this.C.ALTURA_JANELA - (this.C.HUD_ALTURA || 50)) / 20);
        
        this.alimento_pos = [
            Math.floor(Math.random() * maxX) * 20,
            Math.floor(Math.random() * maxY) * 20 + (this.C.HUD_ALTURA || 50)
        ];
    }
    
    processInput(key) {
        if (key === 'ArrowRight' && this.direcao !== 'ESQUERDA') this.direcao = 'DIREITA';
        if (key === 'ArrowLeft' && this.direcao !== 'DIREITA') this.direcao = 'ESQUERDA';
        if (key === 'ArrowUp' && this.direcao !== 'BAIXO') this.direcao = 'CIMA';
        if (key === 'ArrowDown' && this.direcao !== 'CIMA') this.direcao = 'BAIXO';
    }

    update() {
        if (this.emTransicao) return;

        // 🔥 SÓ MOVE A COBRA A CADA X FRAMES
        this.frameCount++;
        if (this.frameCount < this.velocidade) {
            return; // Ainda não é hora de mover
        }
        this.frameCount = 0; // Reset para o próximo movimento

        let novaCabeca = [...this.cobra[0]];
        if (this.direcao === "DIREITA") novaCabeca[0] += 20;
        if (this.direcao === "ESQUERDA") novaCabeca[0] -= 20;
        if (this.direcao === "CIMA") novaCabeca[1] -= 20;
        if (this.direcao === "BAIXO") novaCabeca[1] += 20;

        this.cobra.unshift(novaCabeca);

        // Comeu alimento?
        if (novaCabeca[0] === this.alimento_pos[0] && novaCabeca[1] === this.alimento_pos[1]) {
            this.calorias += 50;
            this.pontuacao += 10;
            this.colocar_alimento();
        } else {
            this.cobra.pop();
        }

        // Colisão com paredes
        const hudAltura = this.C.HUD_ALTURA || 50;
        if (novaCabeca[0] < 0 || novaCabeca[0] >= this.C.LARGURA_JANELA || 
            novaCabeca[1] < hudAltura || novaCabeca[1] >= this.C.ALTURA_JANELA) {
            this.reset_jogo();
        }

        // Colisão consigo próprio
        for (let i = 1; i < this.cobra.length; i++) {
            if (novaCabeca[0] === this.cobra[i][0] && novaCabeca[1] === this.cobra[i][1]) {
                this.reset_jogo();
            }
        }
    }

    draw() {
        // Fundo
        const corFundo = this.C.FUNDOS?.[this.fase_atual]?.cor || '#1e293b';
        this.ctx.fillStyle = corFundo;
        this.ctx.fillRect(0, 0, this.C.LARGURA_JANELA, this.C.ALTURA_JANELA);

        // Alimento
        if (this.imgAlimento.complete && this.imgAlimento.naturalWidth > 0) {
            this.ctx.drawImage(this.imgAlimento, this.alimento_pos[0], this.alimento_pos[1], 20, 20);
        } else {
            this.ctx.fillStyle = '#ef4444';
            this.ctx.fillRect(this.alimento_pos[0], this.alimento_pos[1], 20, 20);
        }

        // Cobra
        this.cobra.forEach((seg, i) => {
            if (i === 0) {
                if (this.imgCabeca.complete && this.imgCabeca.naturalWidth > 0) {
                    this.ctx.drawImage(this.imgCabeca, seg[0], seg[1], 20, 20);
                } else {
                    this.ctx.fillStyle = '#22c55e';
                    this.ctx.fillRect(seg[0], seg[1], 20, 20);
                }
            } else {
                this.ctx.fillStyle = this.C.CORES?.VERDE || '#47baac';
                this.ctx.fillRect(seg[0], seg[1], 18, 18);
            }
        });
        
        // HUD
        this.ctx.fillStyle = 'white';
        this.ctx.font = 'bold 20px Arial';
        this.ctx.fillText(`🍎 Pontos: ${this.pontuacao}`, 20, 35);
        this.ctx.fillText(`🔥 Calorias: ${Math.floor(this.calorias)}`, 220, 35);
        this.ctx.fillText(`🌍 ${this.fase_atual}`, 500, 35);
    }
    
    mudarFase(novaFase) {
        this.fase_atual = novaFase;
        this.emTransicao = false;
    }
    
    aplicarResultadoMinijogo(resultado) {
        if (resultado?.sucesso) {
            this.calorias += resultado.calorias_ganhas || 0;
            this.pontuacao += resultado.pontos || 0;
        }
    }
}