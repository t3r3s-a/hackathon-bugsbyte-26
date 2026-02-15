from fastapi import APIRouter, Response, HTTPException, Body
from app.utils import get_user_by_username
from app.services.pdf_service import criar_pdf_real

router = APIRouter()

@router.post("/gerar-pdf")
async def gerar_pdf_endpoint(payload: dict = Body(...)):
    # Extraímos o username do JSON enviado pelo Vue: { "username": "pou" }
    username = payload.get("username")

    if not username:
        raise HTTPException(status_code=400, detail="Username não fornecido no corpo do pedido")

    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilizador '{username}' não encontrado na base de dados")

    # Gerar o PDF
    pdf_bytes, erro = criar_pdf_real(username, user)

    if erro:
        raise HTTPException(status_code=400, detail=erro)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{username}_plano.pdf"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )