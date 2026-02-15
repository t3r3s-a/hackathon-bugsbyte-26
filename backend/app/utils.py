import json
import os

# 1. Descobre onde está este ficheiro (backend/app/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Sobe um nível para chegar à pasta 'backend/'
# (os.path.dirname de backend/app é backend)
ROOT_DIR = os.path.dirname(BASE_DIR)

# 3. Agora aponta para o ficheiro correto
DB_PATH = os.path.join(ROOT_DIR, "database.json")

def carregar_dados_json():
    """Lê o ficheiro JSON do disco"""
    if not os.path.exists(DB_PATH):
        # Imprime o caminho para saberes onde ele está à procura (ajuda a debugar)
        print(f"❌ ERRO CRÍTICO: Ficheiro não encontrado em: {DB_PATH}")
        return {"users": []}
    
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler JSON: {e}")
        return {"users": []}

def get_user_by_username(username: str):
    """Procura um utilizador específico dentro do JSON"""
    dados = carregar_dados_json()
    lista_users = dados.get("users", [])
    
    # Debug: Mostra no terminal quantos users encontrou
    # print(f"🔍 A procurar '{username}' em {len(lista_users)} utilizadores...")
    
    for user in lista_users:
        if user.get("username") == username:
            return user
            
    return None
