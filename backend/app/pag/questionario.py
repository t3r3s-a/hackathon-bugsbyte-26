import httpx
from fastapi import APIRouter, HTTPException
# Importamos os teus schemas e os do teu colega
from app.schemas import QuestionarioInput, DadosUsuario 

router = APIRouter()

# 1. DEFINIR O DESTINO (A IA do teu colega)
# Se estiveres a correr tudo no mesmo PC, usa "127.0.0.1"
# Se ele estiver noutro PC, usa o IP que ele te deu (ex: 192.168.1.15)
IP_DA_IA = "127.0.0.1" 
URL_GERAR_PLANO = f"http://{IP_DA_IA}:8000/nutrium/gerar-plano"

@router.post("/enviar-formulario", tags=["Inputs Nutrição"])
async def enviar_direto_para_ia(dados_do_site: QuestionarioInput):
    """
    Este endpoint recebe os inputs do utilizador, limpa os dados
    e envia-os diretamente para o motor de IA do teu colega.
    """
    
    # --- PASSO A: TRATAR OS TEUS INPUTS ---
    # O teu colega quer as restrições numa única string.
    # Vamos juntar a tua lista ["Lactose", "Glúten"] numa string "Lactose, Glúten"
    restricoes_formatadas = ", ".join(dados_do_site.alergias)
    
    if dados_do_site.outros:
        restricoes_formatadas += f", {dados_do_site.outros}"

    # --- PASSO B: MONTAR O PACOTE PARA A IA ---
    # Criamos o dicionário com os campos EXATOS que o teu colega definiu no DadosUsuario
    payload_para_ia = {
        "idade": dados_do_site.idade,
        "peso": dados_do_site.peso,
        "altura": dados_do_site.altura,
        "objetivo": dados_do_site.objetivo,
        "restricoes": restricoes_formatadas if restricoes_formatadas else "Nenhuma"
    }

    # --- PASSO C: O DISPARO (A ENTREGA DIRETA) ---
    async with httpx.AsyncClient() as client:
        try:
            # Tu aqui estás a "fingir" ser o utilizador a chamar a IA dele
            resposta = await client.post(URL_GERAR_PLANO, json=payload_para_ia, timeout=30.0)
            
            # Se a IA dele responder com sucesso, entregas o plano ao teu utilizador
            if resposta.status_code == 200:
                return resposta.json()
            else:
                # Se a IA dele der erro (ex: falta de saldo na OpenAI)
                raise HTTPException(status_code=resposta.status_code, detail="A IA do colega falhou.")
        
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Não consegui ligar ao servidor da IA. Verifica o IP!")