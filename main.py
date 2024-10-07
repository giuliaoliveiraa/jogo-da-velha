import tkinter as tk
from tkinter import messagebox
import pygame

# Função para criar a janela principal do jogo
def create_window():
    window = tk.Tk()
    window.title("Jogo da Velha")
    return window

# Função para criar o menu inicial
def create_start_menu(window):
    frame = tk.Frame(window)
    frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    # Botão para iniciar o jogo
    btn_play = tk.Button(frame, text="Jogar", command=start_game)
    btn_play.grid(row=0, column=0, padx=10, pady=10)

    # Botão para ver os autores
    btn_authors = tk.Button(frame, text="Autores", command=show_authors)
    btn_authors.grid(row=0, column=1, padx=10, pady=10)

    # Botão para sair
    btn_exit = tk.Button(frame, text="Sair", command=window.quit)
    btn_exit.grid(row=0, column=2, padx=10, pady=10)

# Função para iniciar o jogo
def start_game():
    global game_frame
    game_frame = tk.Frame(window)
    game_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    create_scoreboard(game_frame)
    global board
    board = create_board(game_frame)
    create_control_buttons(game_frame)

# Função para exibir os autores
def show_authors():
    messagebox.showinfo("Autores", "Autores do jogo: Giulia, Luka e Felipe")

# Função para criar o placar
def create_scoreboard(frame):
    global img_cat_x, img_cat_o
    img_cat_x = tk.PhotoImage(file="cat1.png").subsample(5)  # Ajuste o fator conforme necessário
    img_cat_o = tk.PhotoImage(file="cat2.png").subsample(5)

    lbl_cat_x = tk.Label(frame, image=img_cat_x)
    lbl_cat_x.grid(row=0, column=0, padx=10, pady=10)
    lbl_player_x = tk.Label(frame, text="Jogador X: ", font=("Arial", 14))
    lbl_player_x.grid(row=1, column=0)

    lbl_player_x_score = tk.Label(frame, textvariable=player_x_score, font=("Arial", 14))
    lbl_player_x_score.grid(row=1, column=1)

    lbl_cat_o = tk.Label(frame, image=img_cat_o)
    lbl_cat_o.grid(row=0, column=2, padx=10, pady=10)
    lbl_player_o = tk.Label(frame, text="Jogador O: ", font=("Arial", 14))
    lbl_player_o.grid(row=1, column=2)

    lbl_player_o_score = tk.Label(frame, textvariable=player_o_score, font=("Arial", 14))
    lbl_player_o_score.grid(row=1, column=3)

# Função para criar o tabuleiro de botões
def create_board(frame):
    board = []
    for row in range(3):
        row_buttons = []
        for col in range(3):
            button = tk.Button(frame, text="", command=lambda r=row, c=col: button_click(r, c))
            button.grid(row=row+2, column=col, padx=5, pady=5, sticky="nsew")
            button.config(width=25, height=10)  # Define o tamanho fixo para o botão
            row_buttons.append(button)
        board.append(row_buttons)
    return board

# Função para criar os botões de controle
def create_control_buttons(frame):
    control_frame = tk.Frame(frame)
    control_frame.grid(row=5, column=0, columnspan=3)

    reset_button = tk.Button(control_frame, text="Resetar Jogo", font=("Arial", 14), command=reset_game)
    reset_button.grid(row=0, column=0, padx=20, pady=10)

    reset_scores_button = tk.Button(control_frame, text="Resetar Placar", font=("Arial", 14), command=reset_scores)
    reset_scores_button.grid(row=0, column=1, padx=20, pady=10)

    exit_button = tk.Button(control_frame, text="Sair", font=("Arial", 14), command=window.quit)
    exit_button.grid(row=0, column=2, padx=20, pady=10)

# Função chamada quando um botão é clicado
def button_click(row, col):
    global current_player
    if board[row][col]["image"] == "":
        if current_player == "X":
            board[row][col].config(image=img_cat_x)
        else:
            board[row][col].config(image=img_cat_o)

        if check_winner():
            messagebox.showinfo("Fim de Jogo", f"Jogador {current_player} venceu!")
            if current_player == "X":
                player_x_score.set(player_x_score.get() + 1)
            else:
                player_o_score.set(player_o_score.get() + 1)
            reset_game()
        elif is_board_full():
            messagebox.showinfo("Fim de Jogo", "O jogo terminou em empate!")
            reset_game()
        else:
            current_player = "O" if current_player == "X" else "X"

# Função para verificar se há um vencedor
def check_winner():
    for row in range(3):
        if board[row][0]["image"] == board[row][1]["image"] == board[row][2]["image"] != "":
            return True
    for col in range(3):
        if board[0][col]["image"] == board[1][col]["image"] == board[2][col]["image"] != "":
            return True
    if board[0][0]["image"] == board[1][1]["image"] == board[2][2]["image"] != "":
        return True
    if board[0][2]["image"] == board[1][1]["image"] == board[2][0]["image"] != "":
        return True
    return False

# Função para verificar se o tabuleiro está cheio
def is_board_full():
    for row in board:
        for button in row:
            if button["image"] == "":
                return False
    return True

# Função para reiniciar o jogo
def reset_game():
    global current_player, game_over
    current_player = "X"
    game_over = False
    for row in board:
        for button in row:
            button.config(image="")  # Limpa a imagem do botão

# Função para reiniciar o placar
def reset_scores():
    player_x_score.set(0)
    player_o_score.set(0)
    reset_game()

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Jogo da Velha - Pygame")

# Criação da janela e inicialização das variáveis globais
window = create_window()
current_player = "X"
game_over = False   
player_x_score = tk.IntVar(value=0)
player_o_score = tk.IntVar(value=0)

# Criação do menu inicial
create_start_menu(window)

# Função para atualizar a tela do Pygame
def update_pygame():
    screen.fill((255, 255, 255))
    pygame.display.flip()

# Função para rodar o loop principal do Tkinter e Pygame
def mainloop():
    while True:
        update_pygame()
        window.update_idletasks()
        window.update()

# Iniciar o loop principal
mainloop()
