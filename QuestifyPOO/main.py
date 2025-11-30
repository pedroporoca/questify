import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from sistema import QuestifyApp 

class QuestifyGUI:
    def __init__(self, root):
        self.app = QuestifyApp() 
        self.root = root
        self.root.title("Questify - RPG de Tarefas")
        self.root.geometry("500x600")
        
        
        self.style = ttk.Style()
        self.style.theme_use('clam')

        
        self.mostrar_tela_login()

    def limpar_janela(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    def mostrar_tela_login(self):
        self.limpar_janela()
        self.root.configure(bg="#ffffff")
        frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        frame.pack(expand=True)
        
        imagem_logo = self.carregar_imagem("logo.png", (400, 250))

        if imagem_logo:
            lbl_logo = tk.Label(frame, bg="#ffffff", image=imagem_logo,)
            lbl_logo.image = imagem_logo 
            lbl_logo.pack(pady=(0, 20)) 
        
        else:
            tk.Label(frame, text="QUESTIFY", font=("Impact", 40), fg="#f1c40f").pack(pady=20)
        
        tk.Label(frame, text="BEM-VINDO AO QUESTIFY", font=("Helvetica", 16, "bold")).pack(pady=20)

        tk.Label(frame, text="Usuário:").pack(anchor="w")
        self.entry_user = tk.Entry(frame)
        self.entry_user.pack(fill="x", pady=5)

        tk.Label(frame, text="Senha:").pack(anchor="w")
        self.entry_senha = tk.Entry(frame, show="*")
        self.entry_senha.pack(fill="x", pady=5)

        btn_login = tk.Button(frame, text="ENTRAR", command=self.fazer_login, bg="#031942", fg="white", font=("Arial", 10, "bold"))
        btn_login.pack(fill="x", pady=20)

        btn_registro = tk.Button(frame, text="Criar nova conta", command=self.mostrar_tela_registro)
        btn_registro.pack(fill="x")

    def mostrar_tela_registro(self):
        self.limpar_janela()
        
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="CRIAR CONTA", font=("Helvetica", 14, "bold")).pack(pady=20)

        tk.Label(frame, text="Usuário:").pack(anchor="w")
        self.reg_user = tk.Entry(frame)
        self.reg_user.pack(fill="x", pady=5)

        tk.Label(frame, text="Email:").pack(anchor="w")
        self.reg_email = tk.Entry(frame)
        self.reg_email.pack(fill="x", pady=5)

        tk.Label(frame, text="Senha:").pack(anchor="w")
        self.reg_senha = tk.Entry(frame, show="*")
        self.reg_senha.pack(fill="x", pady=5)

        btn_criar = tk.Button(frame, text="CADASTRAR", command=self.fazer_registro, bg="#2196F3", fg="white")
        btn_criar.pack(fill="x", pady=20)

        btn_voltar = tk.Button(frame, text="Voltar ao Login", command=self.mostrar_tela_login)
        btn_voltar.pack(fill="x")

   
    def fazer_login(self):
        user = self.entry_user.get()
        senha = self.entry_senha.get()
        
        if self.app.login(user, senha):
            self.mostrar_tela_jogo()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    def fazer_registro(self):
        user = self.reg_user.get()
        email = self.reg_email.get()
        senha = self.reg_senha.get()
        
        if len(user) < 3 or len(senha) < 3:
            messagebox.showwarning("Atenção", "Usuário e senha devem ter no mínimo 3 caracteres.")
            return

        sucesso, msg = self.app.registrar(user, senha, email)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.mostrar_tela_login()
        else:
            messagebox.showerror("Erro", msg)

    def abrir_criacao_heroi(self):
        
        janela_criacao = tk.Toplevel(self.root)
        janela_criacao.title("Crie seu Herói")
        janela_criacao.geometry("350x300")
        janela_criacao.configure(bg="#2c3e50")
        
        
        janela_criacao.transient(self.root)
        janela_criacao.grab_set() 
        janela_criacao.focus_force()

        tk.Label(janela_criacao, text="NOVO HERÓI", font=("Impact", 20), bg="#2c3e50", fg="#f1c40f").pack(pady=20)

      
        tk.Label(janela_criacao, text="Nome do Herói:", font=("Arial", 10, "bold"), bg="#2c3e50", fg="white").pack()
        entry_nome = tk.Entry(janela_criacao, font=("Arial", 12))
        entry_nome.pack(pady=5, padx=20, fill="x")

        
        tk.Label(janela_criacao, text="Escolha sua Classe:", font=("Arial", 10, "bold"), bg="#2c3e50", fg="white").pack(pady=(15, 5))
        
        classes_disponiveis = ["Guerreiro", "Mago", "Ladrão"]
        combo_classe = ttk.Combobox(janela_criacao, values=classes_disponiveis, state="readonly", font=("Arial", 11))
        combo_classe.current(0)
        combo_classe.pack(pady=5, padx=20, fill="x")

       
        def confirmar():
            nome = entry_nome.get().strip()
            classe = combo_classe.get()

            if len(nome) < 3:
                messagebox.showwarning("Erro", "O nome deve ter pelo menos 3 caracteres.", parent=janela_criacao)
                return

           
            self.app.usuario_logado.criar_heroi(nome, classe)
            self.app.save_dados()
            
            messagebox.showinfo("Sucesso", f"O herói {nome}, o {classe}, nasceu!", parent=self.root)
            janela_criacao.destroy()
            self.mostrar_tela_jogo()

       
        tk.Button(janela_criacao, text="INICIAR JORNADA", command=confirmar, 
                  bg="#27ae60", fg="white", font=("Arial", 11, "bold")).pack(pady=30, fill="x", padx=20)
    
    def mostrar_tela_jogo(self):
        self.limpar_janela()
        heroi = self.app.usuario_logado.heroi

        if not heroi:
           self.abrir_criacao_heroi()
           return

        painel_heroi = tk.Frame(self.root, bg="#333", pady=10)
        painel_heroi.pack(fill="x")

        tk.Label(painel_heroi, text=f"{heroi.nome} - {heroi.classe_heroi}", fg="white", bg="#333", font=("Arial", 12, "bold")).pack()
        
        xp_max = heroi.level * 100
        tk.Label(painel_heroi, text=f"Nível: {heroi.level} | XP: {heroi.xp}/{xp_max}", fg="#ddd", bg="#333").pack()
        
        barra_xp = ttk.Progressbar(painel_heroi, length=300, maximum=xp_max, value=heroi.xp)
        barra_xp.pack(pady=5)

        frame_abas = tk.Frame(self.root, bg= "#ffffff")
        frame_abas.pack(expand=True, fill="both", padx=20, pady=10)

        # Cria o componente de abas
        self.abas = ttk.Notebook(frame_abas)
        self.abas.pack(expand=True, fill="both")

        # --- ABA 1: MISSÕES ATIVAS ---
        frame_ativas = tk.Frame(self.abas, bg="white")
        self.abas.add(frame_ativas, text="  Missões Ativas  ")

        # Lista visual para as ativas
        self.lista_ativas = tk.Listbox(frame_ativas, font=("Courier", 11), height=10, 
                                       bg="#fafafa", selectbackground="#e0e0e0", selectforeground="black")
        self.lista_ativas.pack(expand=True, fill="both", padx=5, pady=5)

        # --- ABA 2: CONCLUÍDAS ---
        frame_concluidas = tk.Frame(self.abas, bg="white")
        self.abas.add(frame_concluidas, text="  Histórico  ")

        # Lista visual para as concluídas (fundo levemente verde)
        self.lista_concluidas = tk.Listbox(frame_concluidas, font=("Courier", 10), height=10, 
                                           bg="#f0fff0", fg="#555", selectbackground="#d0f0c0", selectforeground="black")
        self.lista_concluidas.pack(expand=True, fill="both", padx=5, pady=5)

        # Preenche as duas listas
        self.atualizar_lista_quests()

        frame_botoes = tk.Frame(self.root, pady=10)
        frame_botoes.pack(fill="x")

        tk.Button(frame_botoes, text="Adicionar Quest", command=self.gui_add_quest).pack(side="left", expand=True, padx=5)
        tk.Button(frame_botoes, text="Concluir Selecionada", command=self.gui_concluir_quest, bg="#8BC34A").pack(side="left", expand=True, padx=5)
        tk.Button(frame_botoes, text="Visualizar Héroi", command=self.gui_visualizar_heroi, bg="#f39c12", fg="white").pack(side="left", expand=True, padx=2)
        tk.Button(frame_botoes, text="Sair / Logout", command=self.gui_logout, bg="#F44336", fg="white").pack(side="left", expand=True, padx=5)

    def gui_visualizar_heroi(self):
    
        perfil = tk.Toplevel(self.root)
        perfil.title("Perfil do Herói")
        perfil.geometry("400x600")
        perfil.configure(bg="#ffffff") 
        
        
        perfil.transient(self.root)
        perfil.focus_force()

        heroi = self.app.usuario_logado.heroi
        nome_arquivo = heroi.classe_heroi.lower().replace("ã", "a") + ".png"
        
        img_heroi = self.carregar_imagem(nome_arquivo, (300, 300))

        frame_img = tk.Frame(perfil, bg="#ffffff", pady=20)
        frame_img.pack()

        if img_heroi:
            lbl_img = tk.Label(frame_img, image=img_heroi, bg="#ffffff")
            lbl_img.image = img_heroi 
            lbl_img.pack()
        else:
            tk.Label(frame_img, text=f"[{heroi.classe_heroi}]", font=("Impact", 30), bg="#2c3e50", fg="#95a5a6").pack()

       
        tk.Label(perfil, text=heroi.nome.upper(), font=("Impact", 24), bg="#ffffff", fg="#f1c40f").pack()
        tk.Label(perfil, text=f"Classe: {heroi.classe_heroi}", font=("Arial", 14), bg="#2c3e50", fg="white").pack(pady=5)

        
        frame_xp = tk.Frame(perfil, bg="#34495e", padx=20, pady=20)
        frame_xp.pack(fill="x", padx=20, pady=20)

        xp_max = heroi.level * 100
        porcentagem = int((heroi.xp / xp_max) * 100)

        tk.Label(frame_xp, text=f"NÍVEL {heroi.level}", font=("Arial", 16, "bold"), bg="#34495e", fg="white").pack()
        
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("green.Horizontal.TProgressbar", foreground='green', background='#27ae60')
        
        barra = ttk.Progressbar(frame_xp, length=300, maximum=xp_max, value=heroi.xp, style="green.Horizontal.TProgressbar")
        barra.pack(pady=10, fill="x")

        tk.Label(frame_xp, text=f"XP: {heroi.xp} / {xp_max} ({porcentagem}%)", bg="#34495e", fg="#bdc3c7").pack()

        
        tk.Button(perfil, text="FECHAR", command=perfil.destroy, bg="#c0392b", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
    
   

    def carregar_imagem(self, nome_arquivo, tamanho=(200, 200)):
        pasta_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_completo = os.path.join(pasta_atual, nome_arquivo)
        
        print(f"DEBUG: Procurando imagem em: {caminho_completo}")

        if not os.path.exists(caminho_completo):
            print(f"ERRO: Arquivo não encontrado!")
            return None 
        
        try:
            img_original = Image.open(caminho_completo)
            img_redimensionada = img_original.resize(tamanho)
            return ImageTk.PhotoImage(img_redimensionada)
        except Exception as e:
            print(f"Erro ao abrir imagem: {e}")
            return None

    def atualizar_lista_quests(self):
        self.lista_ativas.delete(0, tk.END)
        self.lista_concluidas.delete(0, tk.END)
        
        heroi = self.app.usuario_logado.heroi
        
        self.quests_ativas_objs = [] 
        
        for q in heroi.quests:
            if q.status == "ativa":
                texto = f"{q.titulo} ({q.dificuldade} - {q.xp} XP)"
                self.lista_ativas.insert(tk.END, texto)
                self.quests_ativas_objs.append(q) 
            
            else: 
                data = q.data_conclusao if hasattr(q, 'data_conclusao') and q.data_conclusao else "---"
                texto = f"[OK] {q.titulo} - Data: {data}"
                self.lista_concluidas.insert(tk.END, texto)

    def gui_add_quest(self):
        janela_quest = tk.Toplevel(self.root)
        janela_quest.title("Nova Quest")
        janela_quest.geometry("300x250")
        
        tk.Label(janela_quest, text="Título da Tarefa:", font=("Arial", 10)).pack(pady=(20, 5))
        entry_titulo = tk.Entry(janela_quest, font=("Arial", 11))
        entry_titulo.pack(pady=5, padx=20, fill="x")

        tk.Label(janela_quest, text="Dificuldade:", font=("Arial", 10)).pack(pady=(10, 5))
        
        opcoes = ["Fácil (30 XP)", "Média (60 XP)", "Difícil (120 XP)"]
        combo_dificuldade = ttk.Combobox(janela_quest, values=opcoes, state="readonly", font=("Arial", 10))
        combo_dificuldade.current(1) 
        combo_dificuldade.pack(pady=5, padx=20, fill="x")

        def confirmar_adicao():
            titulo = entry_titulo.get().strip()
            selecao = combo_dificuldade.get()
            
            if not titulo:
                messagebox.showwarning("Erro", "O título é obrigatório!", parent=janela_quest)
                return

            if "Fácil" in selecao:
                dif, xp = "Fácil", 30
            elif "Média" in selecao:
                dif, xp = "Média", 60
            else:
                dif, xp = "Difícil", 120

            from models import Quest
            nova_quest = Quest(titulo, dif, xp)
            
            sucesso, msg = self.app.usuario_logado.heroi.adicionar_quest(nova_quest)
            
            if sucesso:
                self.app.save_dados()
                self.atualizar_lista_quests()
                janela_quest.destroy()
                messagebox.showinfo("Sucesso", "Quest criada!", parent=self.root)
            else:
                messagebox.showerror("Erro", msg, parent=janela_quest)

        tk.Button(janela_quest, text="CRIAR", command=confirmar_adicao, 
                  bg="#2196F3", fg="white").pack(pady=20, fill="x", padx=20)
    
    def gui_concluir_quest(self):
       
        if self.abas.index("current") != 0:
            messagebox.showinfo("Info", "Vá para a aba 'Missões Ativas' para concluir tarefas.")
            return

        # Pega a seleção da lista de ATIVAS
        selecionado = self.lista_ativas.curselection()
        
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma missão ativa para concluir.")
            return

        index_visual = selecionado[0]
        
        # Pega o objeto Quest real usando nossa lista auxiliar
        quest = self.quests_ativas_objs[index_visual]

        # Lógica de conclusão
        quest.concluir()
        heroi = self.app.usuario_logado.heroi
        heroi.adicionar_xp(quest.xp)
        
        self.app.save_dados()
        
        messagebox.showinfo("Sucesso", f"Quest concluída! +{quest.xp} XP")
        
        # Redesenha a tela (a quest vai mover para a outra aba automaticamente)
        self.mostrar_tela_jogo()

    def gui_logout(self):
        self.app.logout()
        self.mostrar_tela_login()

if __name__ == "__main__":
    root = tk.Tk()
    app_gui = QuestifyGUI(root)
    root.mainloop()