import importlib

class Jogo:
    def __init__(self, calorias):
        self.calorias = calorias

    def game_over(self):
        # Placeholder para lógica de game over
        return True

    def reset_jogo(self):
        # Placeholder para reiniciar o jogo
        self.calorias = 0

    def jogar(self, modulo_jogo):
        # Constrói o nome da função com base no nome do módulo (sem o prefixo do pacote)
        nome_modulo_simples = modulo_jogo.__name__.split('.')[-1]
        nome_funcao = f"minigame_{nome_modulo_simples}"
        funcao_jogo = getattr(modulo_jogo, nome_funcao)

        ganho = funcao_jogo(self.calorias)

        if ganho == 0:
            # Morreu
            if self.game_over():
                self.reset_jogo()
        else:
            # Ganhou calorias negativas (exercício)
            self.calorias -= ganho


if __name__ == "__main__":
    # Escolha do minijogo
    print("Escolha o minigame:")
    print("1 - Dinossauro")
    print("2 - Equilíbrio")
    opcao = input("Digite 1 ou 2: ").strip()

    if opcao == "1":
        nome_modulo = "MiniJogos.dinossauro"
    elif opcao == "2":
        nome_modulo = "MiniJogos.equilibrio"
    else:
        print("Opção inválida.")
        exit()

    try:
        modulo = importlib.import_module(nome_modulo)
    except ModuleNotFoundError:
        print(f"Erro: Não foi possível importar o módulo '{nome_modulo}'.")
        print("Certifique-se de que a pasta 'MiniJogos' existe e contém um ficheiro '__init__.py' (pode estar vazio).")
        exit()

    calorias_iniciais = 1000
    jogo = Jogo(calorias_iniciais)

    print("Calorias iniciais:", jogo.calorias)

    try:
        jogo.jogar(modulo)
        print("Calorias após jogar:", jogo.calorias)
    except Exception as e:
        print("Erro ao jogar:", e)