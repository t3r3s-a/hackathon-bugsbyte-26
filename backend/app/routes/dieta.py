from fastapi import APIRouter, HTTPException
from app.schemas import DadosUsuario, MensagemChat
from app.services.ai_engine import gerar_plano_completo, responder_chat_nutrium

# Criamos o Router com o prefixo /nutrium
router = APIRouter(prefix="/nutrium", tags=["Nutrium Core"])

PLANO_ATUAL = ""

@router.post("/gerar-plano")
def rota_gerar_plano(dados: DadosUsuario):
    global PLANO_ATUAL
    try:
        # Chamamos a função que estudámos antes
        plano = gerar_plano_completo(dados)
        
        # Guardamos na memória para o chat saber o contexto depois
        PLANO_ATUAL = plano
        
        return {"sucesso": True, "plano": plano}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat-sos")
def rota_chat_sos(msg: MensagemChat):
    global PLANO_ATUAL
    try:
        # Se o utilizador ainda não gerou um plano, o chat avisa
        contexto = PLANO_ATUAL if PLANO_ATUAL else "O utilizador ainda não definiu um plano."
        
        resposta = responder_chat_nutrium(msg.pergunta, contexto)
        
        return {"sucesso": True, "resposta": resposta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))