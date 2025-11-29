# models.py
# Aqui definimos as Classes (os moldes dos objetos)
# models.py

class Quest:
    def __init__(self, titulo, dificuldade, xp, status="ativa"):
        self.titulo = titulo
        self.dificuldade = dificuldade
        self.xp = xp
        self.status = status

    def concluir(self):
        self.status = "concluida"

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "dificuldade": self.dificuldade,
            "xp": self.xp,
            "status": self.status
        }

class Heroi:
    def __init__(self, nome, classe_heroi, level=1, xp=0, quests=None):
        self.nome = nome
        self.classe_heroi = classe_heroi
        self.level = level
        self.xp = xp
        self.quests = []
        if quests:
            for q in quests:
                self.quests.append(Quest(q['titulo'], q['dificuldade'], q['xp'], q['status']))

    def adicionar_xp(self, quantidade):
        self.xp += quantidade
        self.verificar_level_up()

    def verificar_level_up(self):
        xp_necessario = self.level * 100
        while self.xp >= xp_necessario:
            self.level += 1
            self.xp -= xp_necessario
            print(f"🎉 LEVEL UP! {self.nome} alcançou o nível {self.level}!")
            xp_necessario = self.level * 100

    def adicionar_quest(self, quest):
        # Conta quantas quests ativas existem
        ativas = [q for q in self.quests if q.status == "ativa"]
        if len(ativas) >= 5:
            return False, "Limite de quests ativas atingido!"
        self.quests.append(quest)
        return True, "Quest adicionada!"

    def to_dict(self):
        return {
            "nome": self.nome,
            "classe": self.classe_heroi,
            "level": self.level,
            "xp": self.xp,
            "quests": [q.to_dict() for q in self.quests]
        }

class Usuario:  # <--- O ERRO DIZ QUE ESTA CLASSE ESTÁ FALTANDO
    def __init__(self, username, senha, email, heroi_data=None):
        self.username = username
        self.senha = senha
        self.email = email
        self.heroi = None
        if heroi_data:
            self.heroi = Heroi(
                heroi_data['nome'], 
                heroi_data['classe'], 
                heroi_data['level'], 
                heroi_data['xp'], 
                heroi_data.get('quests', [])
            )

    def criar_heroi(self, nome, classe):
        self.heroi = Heroi(nome, classe)

    def to_dict(self):
        data = {
            "senha": self.senha,
            "email": self.email,
            "heroi": None
        }
        if self.heroi:
            data["heroi"] = self.heroi.to_dict()
        return data