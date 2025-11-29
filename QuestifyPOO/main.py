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

        sucesso, msg = self.app.register(user, senha, email)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.mostrar_tela_login()
        else:
            messagebox.showerror("Erro", msg)

    def mostrar_tela_jogo(self):
        self.limpar_janela()
        heroi = self.app.usuario_logado.heroi

        if not heroi:
            nome_heroi = simpledialog.askstring("Criação", "Digite o nome do seu Herói:")
            if not nome_heroi: 
                self.app.logout()
                self.mostrar_tela_login()
                return
            
            self.app.usuario_logado.criar_heroi(nome_heroi, "Guerreiro")
            self.app.salvar_dados()
            heroi = self.app.usuario_logado.heroi

        painel_heroi = tk.Frame(self.root, bg="#333", pady=10)
        painel_heroi.pack(fill="x")

        tk.Label(painel_heroi, text=f"{heroi.nome} - {heroi.classe_heroi}", fg="white", bg="#333", font=("Arial", 12, "bold")).pack()
        
        xp_max = heroi.level * 100
        tk.Label(painel_heroi, text=f"Nível: {heroi.level} | XP: {heroi.xp}/{xp_max}", fg="#ddd", bg="#333").pack()
        
        barra_xp = ttk.Progressbar(painel_heroi, length=300, maximum=xp_max, value=heroi.xp)
        barra_xp.pack(pady=5)

        frame_quests = tk.Frame(self.root, padx=20, pady=20)
        frame_quests.pack(expand=True, fill="both")

        tk.Label(frame_quests, text="SUAS QUESTS", font=("Arial", 10, "bold")).pack(anchor="w")

        self.lista_box = tk.Listbox(frame_quests, font=("Courier", 10), height=15)
        self.lista_box.pack(fill="both", expand=True, pady=10)
        
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
        self.lista_box.delete(0, tk.END) 
        heroi = self.app.usuario_logado.heroi
        
        for q in heroi.quests:
            status = "[OK]" if q.status == "concluida" else "[  ]"
            texto = f"{status} {q.titulo} ({q.dificuldade} - {q.xp} XP)"
            self.lista_box.insert(tk.END, texto)
            
            
            if q.status == "concluida":
                self.lista_box.itemconfig(tk.END, {'fg': 'gray'})

    def gui_add_quest(self):
        
        titulo = simpledialog.askstring("Nova Quest", "Título da Quest:")
        if titulo:
           
            from models import Quest
            nova_quest = Quest(titulo, "Média", 60)
            
            sucesso, msg = self.app.usuario_logado.heroi.adicionar_quest(nova_quest)
            if sucesso:
                self.app.salvar_dados()
                self.atualizar_lista_quests()
            else:
                messagebox.showwarning("Erro", msg)

    def gui_concluir_quest(self):
        selecionado = self.lista_box.curselection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma quest na lista para concluir.")
            return

        index = selecionado[0]
        heroi = self.app.usuario_logado.heroi
        quest = heroi.quests[index]

        if quest.status == "concluida":
            messagebox.showinfo("Info", "Essa quest já foi concluída!")
            return

        quest.concluir()
        heroi.adicionar_xp(quest.xp)
        self.app.salvar_dados()
        
        messagebox.showinfo("Sucesso", f"Quest concluída! +{quest.xp} XP")
        
        self.mostrar_tela_jogo()

    def gui_logout(self):
        self.app.logout()
        self.mostrar_tela_login()

if __name__ == "__main__":
    root = tk.Tk()
    app_gui = QuestifyGUI(root)
    root.mainloop()