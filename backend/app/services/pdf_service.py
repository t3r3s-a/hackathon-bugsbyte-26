import os
from openai import OpenAI
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class NutriumPDF(FPDF):
    def header(self):
        # Retângulo decorativo no topo (Verde Nutrium)
        self.set_fill_color(39, 174, 96) 
        self.rect(0, 0, 210, 40, 'F')
        
        # Título Branco sobre o Verde
        self.set_font('Arial', 'B', 24)
        self.set_text_color(255, 255, 255)
        self.cell(0, 20, 'NUTRIUM AI', 0, 1, 'C')
        
        self.set_font('Arial', 'I', 10)
        self.cell(0, -5, 'O teu plano alimentar inteligente', 0, 1, 'C')
        self.ln(25) # Espaço para sair de cima da barra verde

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Nutrium Hackathon 2026 - Pagina {self.page_no()}', 0, 0, 'C')

def criar_pdf_real(username: str, user_data: dict):
    q = user_data.get("questionnaire", {})
    
    # --- LOGICA DA IA (IGUAL AO TEU ROBO) ---
    prompt = f"""
    Cria um plano alimentar de 1 dia para {username}:
    Peso: {q.get('peso')}kg, Altura: {q.get('altura')}cm, Objetivo: {q.get('objetivo')}.
    Restricoes: {q.get('alergias')}.
    Estrutura: Pequeno-almoco, Almoço, Lanche e Jantar. 
    Usa linguagem profissional. Sem markdown.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        texto_plano = response.choices[0].message.content
    except:
        texto_plano = "Erro ao carregar plano. Contacte o SOS Nutrium."

    # --- MONTAGEM DO PDF ESTILIZADO ---
    pdf = NutriumPDF()
    pdf.add_page()
    
    # 1. Info do Utilizador (Caixa Cinza)
    pdf.set_fill_color(245, 245, 245)
    pdf.rect(10, 45, 190, 25, 'F')
    
    pdf.set_y(48)
    pdf.set_x(15)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 10, f"Plano para: {username.upper()}", ln=True)
    
    pdf.set_x(15)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, f"Objetivo: {q.get('objetivo')} | Peso: {q.get('peso')}kg | Alergias: {q.get('alergias')}", ln=True)
    
    pdf.ln(15)

    # 2. Titulo do Plano (Verde)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(39, 174, 96)
    pdf.cell(0, 10, "SUGESTOES DIARIAS", ln=True)
    
    # Linha horizontal verde
    pdf.set_draw_color(39, 174, 96)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # 3. Conteúdo da IA
    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(60, 60, 60)
    
    # Tratamento de texto para evitar erros de encoding
    texto_seguro = texto_plano.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, texto_seguro)
    
    # 4. Mensagem Final
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(39, 174, 96)
    pdf.cell(0, 10, "Bons treinos! Come bem, vive melhor.", 0, 0, 'C')

    return pdf.output(dest='S').encode('latin-1'), None