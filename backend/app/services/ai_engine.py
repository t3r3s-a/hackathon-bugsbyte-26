import os
from openai import OpenAI
from dotenv import load_dotenv
from app.schemas import DadosUsuario

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_plano_completo(dados: DadosUsuario):
    prompt = f"""
Cria um plano alimentar saudável de 1 dia para:
- Peso: {dados.peso}kg, Altura: {dados.altura}cm
- Objetivo: {dados.objetivo}
- Restrições: {dados.restricoes}
Estrutura o plano em 4 ou 5 refeições: Pequeno-almoço, Lanche matinal(nem sempre necessário), Almoço, Lanche, Jantar.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def responder_chat_nutrium(pergunta: str, plano_contexto: str):
    prompt_sistema = "És um assistente da Nutrium. Ajuda o utilizador a adaptar o plano dele."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"Plano atual: {plano_contexto}. Pergunta: {pergunta}"}
        ]
    )
    return response.choices[0].message.content
