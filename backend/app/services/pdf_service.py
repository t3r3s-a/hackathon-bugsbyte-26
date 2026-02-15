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
            self.image(logo_path, 10, 10, 85) 
        
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
    # Extração detalhada dos dados do JSON
    q = user_data.get("questionnaire", {})
    
    nome = username.upper()
    idade = q.get('idade', 'N/A')
    peso = q.get('peso', 'N/A')
    altura = q.get('altura', 'N/A')
    objetivo = q.get('objetivo', 'Equilíbrio Alimentar')
    alergias = q.get('alergias', 'Nenhuma declarada')
    preferencias = q.get('preferencias', 'Não especificadas')
    nivel_atividade = q.get('atividade', 'Moderada')

    # --- PROMPT DE ENGENHARIA NUTRICIONAL ---
    prompt = f"""
    És um Nutricionista Clínico de alta performance. Elabora um Plano Alimentar Personalizado e Formal para o paciente {nome}.
    
    PERFIL DO PACIENTE:
    - Idade: {idade} anos | Peso: {peso}kg | Altura: {altura}cm
    - Nível de Atividade Física: {nivel_atividade}
    - Objetivo Principal: {objetivo}
    - Restrições Médicas/Alergias: {alergias}
    - Preferências Alimentares: {preferencias}

    ESTRUTURA DO PLANO (OBRIGATÓRIA):
    1. ANÁLISE INICIAL: Um parágrafo curto sobre como o plano foi adaptado ao objetivo ({objetivo}).
    2. DISTRIBUIÇÃO DE REFEIÇÕES:
       - Pequeno-almoço: Sugestão técnica com porções.
       - Lanche da Manhã: Opção prática.
       - Almoço: Foco em macronutrientes (Proteína, Hidratos, Vegetais).
       - Lanche da Tarde: Foco em saciedade.
       - Jantar: Refeição leve e reparadora.
    3. RECOMENDAÇÃO DE HIDRATAÇÃO: Cálculo sugerido de água.
    4. NOTA MOTIVACIONAL: Uma frase curta e profissional.

    REGRAS CRÍTICAS:
    - NÃO uses Markdown (sem asteriscos **, sem cardinais #).
    - Usa linguagem técnica mas acessível (ex: 'Macronutrientes', 'Índice Glicémico').
    - Sê específico nas quantidades (gramas ou colheres).
    - Formata como um documento oficial.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "És um nutricionista que escreve relatórios médicos formais em português de Portugal."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7 # Criatividade moderada para manter o rigor técnico
        )
        texto_plano = response.choices[0].message.content
    except Exception as e:
        print(f"Erro OpenAI: {e}")
        texto_plano = "Ocorreu um erro técnico na geração do plano. Por favor, tente novamente."

    # --- GERAÇÃO DO PDF ---
    pdf = NutriumFormalPDF()
    pdf.add_page()
    
    # Cabeçalho do Paciente
    pdf.set_fill_color(240, 245, 240)
    pdf.rect(10, 42, 190, 30, 'F')
    pdf.set_y(45)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_x(15)
    pdf.cell(0, 7, f"PACIENTE: {nome}", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.set_x(15)
    pdf.cell(0, 6, f"DADOS: {peso}kg | {altura}cm | Objetivo: {objetivo}", ln=True)
    pdf.set_x(15)
    pdf.cell(0, 6, f"ALERGIAS: {alergias}", ln=True)
    
    pdf.ln(12)

    # Conteúdo da IA
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(39, 174, 96)
    pdf.cell(0, 10, "DIRETRIZES NUTRICIONAIS PERSONALIZADAS", ln=True)

    texto_limpo = texto_plano.replace('*', '').replace('#', '').replace('_', '')
    
    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(50, 50, 50)


    texto_plano = response.choices[0].message.content

  
    # Remove asteriscos, cardinais e outros símbolos de formatação
    texto_limpo = texto_plano.replace('*', '').replace('#', '').replace('_', '')

    # --- GERAÇÃO DO PDF ---
    pdf = NutriumFormalPDF()
    pdf.add_page()
    


    # Limpeza final para o FPDF (Encoding)
    # Usamos o texto_limpo em vez do texto_plano
    texto_seguro = texto_limpo.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, texto_seguro)
    
    return pdf.output(dest='S').encode('latin-1'), None

