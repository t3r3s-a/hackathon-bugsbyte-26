# backend/app/routes/plano.py
from fastapi import APIRouter, Response, HTTPException
from app.utils import get_user_by_username
from app.services.pdf_service import criar_pdf_real

router = APIRouter()

@router.get("/{username}")
async def baixar_plano(username: str):
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User não encontrado")

    pdf_bytes, erro = criar_pdf_real(username, user)
    if erro:
        raise HTTPException(status_code=400, detail=erro)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Plano_{username}.pdf"}
    )
