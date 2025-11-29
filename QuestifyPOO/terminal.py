from sistema import QuestifyApp
from models import Quest
import time
import pwinput

app = QuestifyApp()

def menu_principal():
    while True:
        if not app.usuario_logado:
            print("=== QUESTIFY ===")
            print("1. Login")
            print("2. Registrar")
            print("3. Sair")
            op = input("Opção: ")

            if op == "1":
                user = input("Usuário: ")
                senha = pwinput.pwinput("Senha: ")
                if app.login(user, senha):
                    print("Logado com sucesso!")
                else:
                    print("Falha no login.")
                time.sleep(1)

            elif op == "2":
                user = input("Usuário: ")
                email = input("Email: ")
                senha = pwinput.pwinput("Senha: ")
                sucesso, msg = app.registrar(user, senha, email)
                print(msg)
                time.sleep(1)
            
            elif op == "3":
                break
        
        else:
            heroi = app.usuario_logado.heroi
            
            print(f"=== Bem-vindo, {app.usuario_logado.username} ===")
            if heroi:
                print(f"Herói: {heroi.nome} (Lvl {heroi.level})")
            else:
                print("Herói: Nenhum")
            
            print("1. Jogar / Gerenciar Herói")
            print("2. Logout")
            
            op = input("Opção: ")

            if op == "1":
                if not heroi:
                    nome = input("Nome do herói: ")
                    app.usuario_logado.criar_heroi(nome, "Guerreiro")
                    app.salvar_dados()
                else:
                    menu_jogo()
            
            elif op == "2":
                app.logout()

def menu_jogo():
    heroi = app.usuario_logado.heroi
    
    while True:
        print(f"--- {heroi.nome} ---")
        print(f"XP: {heroi.xp}")
        print("Quests:")
        for i, q in enumerate(heroi.quests):
            print(f"{i+1}. {q.titulo} ({q.status})")
        
        print("A. Adicionar Quest")
        print("V. Voltar")
        
        op = input("Opção: ").upper()
        
        if op == "A":
            titulo = input("Título: ")
            nova_quest = Quest(titulo, "Fácil", 30)
            ok, msg = heroi.adicionar_quest(nova_quest)
            print(msg)
            app.salvar_dados() 
            time.sleep(1)
            
        elif op == "V":
            break

if __name__ == "__main__":
    menu_principal()