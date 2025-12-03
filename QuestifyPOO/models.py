from datetime import datetime

class Quest:
    def __init__(self, titulo, dificuldade, xp, status="ativa", data_conclusao=None):
        self.titulo = titulo
        self.dificuldade = dificuldade
        self.xp = xp
        self.status = status
        self.data_conclusao = data_conclusao

    def concluir(self):
        self.status = "concluida"
        self.data_conclusao = datetime.now().strftime("%d/%m/%Y %H:%M")
    def to_dict(self):
        return {
            "titulo": self.titulo,
            "dificuldade": self.dificuldade,
            "xp": self.xp,
            "status": self.status,
            "data_conclusao": self.data_conclusao
        
        }

class Heroi:
    def __init__(self, nome, classe_heroi, level=1, xp=0, quests=None, atributos=None, pontos_distribuir=0, boss_data=None, conquistas=None):
        if atributos:
            self.atributos = atributos
        else:
            self.atributos = self.definir_atributos_base(classe_heroi)
        
        self.pontos_distribuir = pontos_distribuir
        
        if boss_data:
            self.boss_data = boss_data
        else:
            self.boss_data = {"ativo": False, "tarefas": [], "data_ultimo": None}
        
        if conquistas:
            self.conquistas = conquistas
        else:
            self.conquistas = []
        
        
        self.nome = nome
        self.classe_heroi = classe_heroi
        self.level = level
        self.xp = xp
        self.quests = []
        if quests:
            for q in quests:
                self.quests.append(Quest(q['titulo'], q['dificuldade'], q['xp'], q['status'], q.get('data_conclusao')))
    
    def definir_atributos_base(self, classe):
        if classe == "Guerreiro":
            return {"Força": 5, "Inteligência": 2, "Destreza": 3, "Carisma": 3, "Sabedoria": 2}
        elif classe == "Mago":
            return {"Força": 2, "Inteligência": 5, "Destreza": 3, "Carisma": 2, "Sabedoria": 4}
        elif classe == "Ladrão":
            return {"Força": 3, "Inteligência": 3, "Destreza": 5, "Carisma": 4, "Sabedoria": 2}
        else:
            return {"Força": 3, "Inteligência": 3, "Destreza": 3, "Carisma": 3, "Sabedoria": 3}
    
    def distribuir_ponto(self, atributo):
        if self.pontos_distribuir > 0 and atributo in self.atributos:
            self.atributos[atributo] += 1
            self.pontos_distribuir -= 1
            novas = self.verificar_conquistas()
            return True, novas
        return False, []
    
    def adicionar_xp(self, quantidade):
        self.xp += quantidade
        self.verificar_level_up()
        return self.verificar_conquistas()

    def verificar_level_up(self):
        xp_necessario = self.level * 100
        while self.xp >= xp_necessario:
            self.level += 1
            self.pontos_distribuir += 1
            self.xp -= xp_necessario
            print(f"🎉 LEVEL UP! {self.nome} alcançou o nível {self.level}!")
            xp_necessario = self.level * 100

    def adicionar_quest(self, quest):
        ativas = [q for q in self.quests if q.status == "ativa"]
        if len(ativas) >= 5:
            return False, "Limite de quests ativas atingido!"
        self.quests.append(quest)
        return True, "Quest adicionada!"
    
    def pode_iniciar_boss(self):
        if self.boss_data["ativo"]:
            return False, "Já existe uma missão de Chefe ativa!"
        
        ultimo = self.boss_data.get("data_ultimo")
        if ultimo:
            data_ultimo = datetime.strptime(ultimo, "%d/%m/%Y")
            diferenca = datetime.now() - data_ultimo
            if diferenca.days < 7:
                return False, f"O Chefe descansa. Volte em {7 - diferenca.days} dias."
        
        return True, "Pode iniciar"

    def iniciar_boss(self, lista_tarefas):
        tarefas_obj = [{"desc": t, "feita": False} for t in lista_tarefas]
        self.boss_data["ativo"] = True
        self.boss_data["tarefas"] = tarefas_obj

    def concluir_tarefa_boss(self, index):
        if self.boss_data["ativo"]:
            self.boss_data["tarefas"][index]["feita"] = True
            todas_feitas = all(t["feita"] for t in self.boss_data["tarefas"])
            if todas_feitas:
                self.boss_data["ativo"] = False
                self.boss_data["tarefas"] = []
                self.boss_data["data_ultimo"] = datetime.now().strftime("%d/%m/%Y")
                self.adicionar_xp(2000)
                return True, "CHEFÃO DERROTADO! +2000 XP"
            return False, "Tarefa do Chefe concluída!"
        return False, "Erro."

    
    def verificar_conquistas(self):
        
        novas = []
        total_concluidas = len([q for q in self.quests if q.status == "concluida"])
        total_dificeis = len([q for q in self.quests if q.status == "concluida" and q.dificuldade == "Difícil"])

        regras = [
            ("O Início (1ª Quest)", total_concluidas >= 1),
            ("Trabalhador (10 Quests)", total_concluidas >= 10),
            ("Máquina (50 Quests)", total_concluidas >= 50),       
            ("Desafiante (Hardcore)", total_dificeis >= 1),
            ("Lenda Iniciante (Nvl 5)", self.level >= 5),
            ("Herói Épico (Nvl 10)", self.level >= 10),
            ("Semideus (Nvl 20)", self.level >= 20),
            ("Hércules (10 Força)", self.atributos.get("Força", 0) >= 10),
            ("Einstein (10 Int)", self.atributos.get("Inteligência", 0) >= 10),
            ("Influenciador (10 Car)", self.atributos.get("Carisma", 0) >= 10)
        ]

        for nome_conquista, condicao_verdadeira in regras:
            if condicao_verdadeira and nome_conquista not in self.conquistas:
                self.conquistas.append(nome_conquista)
                novas.append(nome_conquista)
                print(f"🏆 CONQUISTA DESBLOQUEADA: {nome_conquista}")

        return novas
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "classe": self.classe_heroi,
            "level": self.level,
            "xp": self.xp,
            "atributos": self.atributos,
            "pontos_distribuir": self.pontos_distribuir,
            "boss_data": self.boss_data,
            "conquistas": self.conquistas,
            "quests": [q.to_dict() for q in self.quests]
        }

class Usuario: 
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
                heroi_data.get('quests', []),
                heroi_data.get('atributos'),
                heroi_data.get('pontos_distribuir', 0),
                heroi_data.get('boss_data'),
                heroi_data.get('conquistas')
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
