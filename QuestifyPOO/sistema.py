import json
import os
from models import Usuario, Quest

JSON_FILE = "usuarios.json"

class QuestifyApp:
    def __init__(self):
        self.usuarios = {} 
        self.usuario_logado = None
        self.carregar_dados()

    def carregar_dados(self):
        if not os.path.exists(JSON_FILE):
            return

        with open(JSON_FILE, "r", encoding='utf-8') as f:
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

    def salvar_dados(self):
        dados_para_salvar = {}
        for nome_user, obj_usuario in self.usuarios.items():
            dados_para_salvar[nome_user] = obj_usuario.to_dict()
        
        with open(JSON_FILE, "w", encoding='utf-8') as f:
            json.dump(dados_para_salvar, f, indent=4, ensure_ascii=False)

    def registrar(self, username, senha, email):
        if username in self.usuarios:
            return False, "Usuário já existe."
        
        novo_user = Usuario(username, senha, email)
        self.usuarios[username] = novo_user
        self.salvar_dados()
        return True, "Conta criada com sucesso!"

    def login(self, username, senha):
        user = self.usuarios.get(username)
        if user and user.senha == senha:
            self.usuario_logado = user 
            return True
        return False
    
    def logout(self):
        self.usuario_logado = None
