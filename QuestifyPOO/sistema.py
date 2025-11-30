import json
import os
from models import Usuario, Quest

jsonfile = "usuarios.json"

class QuestifyApp:
    def __init__(self):
        self.usuarios = {} 
        self.usuario_logado = None
        self.carregar_dados()

    def carregar_dados(self):
        if not os.path.exists(jsonfile):
            return

        with open(jsonfile, "r", encoding='utf-8') as f:
            try:
                dados_raw = json.load(f)
                for nome_user, dados_user in dados_raw.items():
                    
                    novo_usuario = Usuario(
                        nome_user, 
                        dados_user['senha'], 
                        dados_user['email'], 
                        dados_user.get('heroi')
                    )
                    self.usuarios[nome_user] = novo_usuario
            except json.JSONDecodeError:
                pass

    def save_dados(self):
        
        dados = {}
        for nome_user, obj_usuario in self.usuarios.items():
            dados[nome_user] = obj_usuario.to_dict()
        
        with open(jsonfile, "w", encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    def registrar(self, username, senha, email):
        if username in self.usuarios:
            return False, "Usuário já existe."
        
        
        novo_user = Usuario(username, senha, email)
        self.usuarios[username] = novo_user
        self.save_dados()
        return True, "Conta criada com sucesso!"

    def login(self, username, senha):
        user = self.usuarios.get(username)
        if user and user.senha == senha:
            self.usuario_logado = user
            return True
        return False
    
    def logout(self):
        self.usuario_logado = None