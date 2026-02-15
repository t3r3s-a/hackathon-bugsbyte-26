import os
from openai import OpenAI
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class NutriumFormalPDF(FPDF):
    def header(self):
        # --- CONFIGURAÇÃO DO LOGO ---
        # Caminho para o teu ficheiro Snake-e.png
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'Snake-e.png')
        
        if os.path.exists(logo_path):
            # image(caminho, x, y, largura) - o 30 é a largura em mm
            self.image(logo_path, 10, 8, 60) 
        
        # --- TÍTULO DO DOCUMENTO (ALINHADO À DIREITA) ---
        self.set_font('Arial', 'B', 15)
        self.set_text_color(39, 174, 96) # Verde Nutrium Formal
        self.cell(0, 10, 'PRESCRIÇÃO ALIMENTAR INTELIGENTE', 0, 1, 'R')
        
        self.set_font('Arial', 'I', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, 'Análise de Bioestatística via Nutrium AI', 0, 1, 'R')
        
        # Linha verde horizontal de separação
        self.set_draw_color(39, 174, 96)
        self.set_line_width(0.5)
        self.line(10, 35, 200, 35)
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(120, 120, 120)
        # Rodapé formal
        self.cell(0, 10, 'Este documento é gerado automaticamente e serve como guia nutricional.', 0, 0, 'L')
        self.cell(0, 10, f'Pág. {self.page_no()}', 0, 0, 'R')

def criar_pdf_real(username: str, user_data: dict):
    q = user_data.get("questionnaire", {})
    
    alergias = ", ".join(q.get('alergias', [])) if q.get('alergias') else "Nenhuma"

    # Prompt otimizado para a tua IA privada (OpenAI)
    prompt = f"""
    És um Nutricionista Pediátrico Especialista. Cria um plano rigoroso para o {username}.
    
    DADOS DO PACIENTE:
    - Idade: {q.get('idade')} anos
    - Sexo: {q.get('sexo')}
    - Peso: {q.get('peso')}kg | Altura: {q.get('altura')}cm
    - Atividade Física: {q.get('faz_desporto')} ({q.get('frequencia_desporto')}x/semana)
    - Alergias (PROIBIDO): {alergias}

    LOGICA DE ANÁLISE:
    1. Analisa a relação Peso/Altura: 
       - Se o peso for baixo para a altura: O plano deve ser HIPERCALÓRICO. Incentiva a comer mais proteínas e hidratos complexos para ganhar força e "combustível".
       - Se o peso for elevado para a altura: O plano deve focar em CONTROLO DE PORÇÕES, fibras e densidade nutricional, sem ser restritivo demais (é uma criança).
    2. Ajusta as calorias para o nível de desporto ({q.get('frequencia_desporto')}x semana).
    3. Dá ordens claras: "Come isto", "Evita aquilo".

    ESTRUTURA DO PDF (NÃO USAR MARKDOWN):
    - Pequeno Pequeno-almoço: [Refeição]
    - Lanche da Manhã: [Refeição]
    - Almoço: [Refeição]
    - Lanche: [Refeição]
    - Jantar: [Refeição]
    
    NOTA FINAL PARA QUEM COZINHA ({q.get('quem_cozinha')}):
    Dá um conselho técnico sobre como preparar as refeições para este perfil específico.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        texto_plano = response.choices[0].message.content
    except Exception as e:
        print(f"Erro OpenAI: {e}")
        texto_plano = "Erro na comunicação com a IA Engine. Por favor contacte o suporte."

    pdf = NutriumFormalPDF()
    pdf.add_page()
    
    # --- BOX DE IDENTIFICAÇÃO DO PACIENTE ---
    pdf.set_fill_color(240, 245, 240) # Verde muito claro
    pdf.rect(10, 42, 190, 25, 'F')
    
    pdf.set_y(45)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(40, 40, 40)
    pdf.set_x(15)
    pdf.cell(0, 7, f"PACIENTE: {username.upper()}", ln=True)
    
    pdf.set_font("Arial", '', 10)
    pdf.set_x(15)
    pdf.cell(0, 6, f"DADOS: {q.get('peso')}kg | {q.get('altura')}cm | Objetivo: {q.get('objetivo')}", ln=True)
    
    pdf.ln(15)

    # --- TEXTO DO PLANO ---
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(39, 174, 96)
    pdf.cell(0, 10, "DETALHE DO PLANO DIETÉTICO", ln=True)
    
    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(60, 60, 60)
    
    # Limpeza de caracteres especiais para evitar erros no FPDF
    texto_seguro = texto_plano.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, texto_seguro)
    
    return pdf.output(dest='S').encode('latin-1'), None
