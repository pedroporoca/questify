# 📌 Questify - Release v1

## 🎮 Sobre o Projeto
O **Questify** é um aplicativo gamificado que transforma sua lista de tarefas em um **jogo de RPG** para combater a procrastinação.  
Cada tarefa do dia a dia vira uma **missão** que concede **pontos de experiência (XP)** ao seu herói virtual.  
Ao completar as missões, o herói sobe de nível, criando um ciclo de **motivação e produtividade**.

---

## 🚀 Funcionalidades da Release v1

### 👤 Criação de Conta
- Cadastro de usuário com **login e senha**.

### 🦸‍♂️ Criação e Visualização do Herói
- Criar um herói com **nome personalizado**.
- Exibir status básicos:
  - Nome  
  - Nível  
  - Quantidade de Experiência (XP)  

### 📜 Missões (Tarefas)
- Adicionar novas missões com:
  - **Título**  
  - **Dificuldade** (Pequena, Média ou Grande) → que define o XP recebido.  

### ✅ Conclusão de Missões
- Marcar uma missão como concluída.  
- XP correspondente é adicionado ao herói.  
- Missão é removida da lista de pendentes.  
 

### 📈 Sistema de Level Up
- Ao encher a barra de XP, o herói sobe de nível.  
- Exibir notificação de **“Level Up!”**.  
- A cada nível, a quantidade de XP necessária aumenta.  

### 💾 Persistência de Dados
- Progresso do herói e lista de missões salvos em **arquivo JSON**.  
- Dados preservados mesmo ao fechar o programa.  

---
## 🌟 Funcionalidades da (Release v2)

- Para a próxima grande atualização, planejamos expandir o universo do Questify com as seguintes funcionalidades:

### 🖥️ Interface Gráfica

 - Migrar a aplicação do console para uma interface gráfica (GUI) intuitiva e visualmente agradável, melhorando a experiência do usuário.

### 📊 Sistema de Atributos

 - Introduzir atributos clássicos de RPG (ex: Força, Inteligência, Constituição).
 - A cada level up, o usuário ganha pontos para distribuir nesses atributos.
 - Permitir que as missões sejam categorizadas por atributo (ex: "Ir à academia" = Força, "Estudar para o exame" = Inteligência).


### 🐲 "Missões de Chefão" (Projetos)

- Permitir a criação de "Chefões", que são projetos grandes.
- Um "Chefão" deve ser composto por várias sub-missões.
- Derrotar o "Chefão" (completar todas as sub-missões) concede uma grande recompensa de XP e um item especial.

### 🏆 Histórico e Conquistas

- Criar uma tela de "Hall da Fama" para exibir todas as missões que o usuário já completou.
- Implementar um sistema de "Conquistas" (Achievements) por marcos alcançados (ex: "Chegue ao Nível 10", "Complete 50 missões").


## 🎯 Público-Alvo
- Estudantes (Universitários e Vestibulandos)  
- Concurseiros e Jovens Profissionais  
- Pessoas com dificuldade de foco e disciplina (incluindo TDAH)  
---
## 🛠️ Tecnologias Utilizadas

O projeto foi desenvolvido utilizando **Python 3** e as seguintes bibliotecas/paradigmas:

* **Tkinter:** Para construção da Interface Gráfica (GUI) moderna.
* **Pillow (PIL):** Para manipulação e exibição de imagens.
* **JSON:** Para persistência de dados (Banco de dados local).
* **POO (Programação Orientada a Objetos):** Arquitetura modular e escalável.

## 👥 Autor
- **Pedro Lucca**  
---

## Fluxogramas V1
- https://drive.google.com/drive/folders/19ikFMs2wD3OZVv0rQaw7K5s6Q7Jl7efQ?usp=drive_link
