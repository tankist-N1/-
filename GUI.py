import tkinter as tk
from tkinter import messagebox
import Detectionboard
from chessmoves import Game
from tkinter.simpledialog import askstring
import Board
import chess

class ChessGameGUI:
    def init(self, master):
        self.master = master
        self.master.configure(bg="#F0F0F0")
        
        self.frame_buttons = tk.Frame(master, bg="#F0F0F0")
        self.frame_buttons.pack()

        self.button_start = tk.Button(self.frame_buttons, text="Начать игру", command=self.start_playing, bg="#66CDAA", fg="black", font=('Helvetica', 12, 'bold'))
        self.button_start.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_quit = tk.Button(self.frame_buttons, text="Выйти", command=self.quit_game, bg="#FF6347", fg="black", font=('Helvetica', 12, 'bold'))
        self.button_quit.pack(side=tk.LEFT, padx=10, pady=10)

        self.logs_text = tk.Text(master, width=60, height=25, background='white', font=('Helvetica', 10), wrap=tk.WORD)
        self.logs_text.pack(pady=10)

    def clear_logs(self):
        self.logs_text.delete('1.0', tk.END)

    def add_log(self, log):
        self.logs_text.insert(tk.END, log + "\n")


    def start_playing(self):
        self.Game = Game()
        self.add_log("Поиск доски")

        found_chessboard, position = Detectionboard.find_chessboard()

        if found_chessboard:
            self.add_log("Доска найдена " + position.print_custom())
            self.Game.board_position_on_screen = position
        else:
            self.add_log("Доска не найдена")
            self.add_log("Заново\n")
            return

        self.button_start.pack_forget()
        self.button_stop = tk.Button(self.frame_buttons, text="Остановить игру", command=self.stop_playing, bg="#FF4500", fg="black", font=('Helvetica', 12, 'bold'))
        self.button_stop.pack(side=tk.LEFT, padx=10, pady=10)

        self.add_log("МЫ за кого?")
        resized_chessboard = Detectionboard.get_chessboard(self.Game)

        self.Game.previous_chessboard_image = resized_chessboard

        we_are_white = Board.is_white_on_bottom(resized_chessboard)
        self.Game.we_play_white = we_are_white
        if we_are_white:
            self.add_log("Мы играем за белых")
            self.Game.moves_to_detect_before_use_engine = 0
        else:
            self.add_log("Мы играем за черных")
            self.Game.moves_to_detect_before_use_engine = 1
            first_move_registered = False
            while not first_move_registered:
                first_move_string = askstring('Первый ход', 'Введите первый ход белых?')
                if first_move_string:
                    first_move = chess.Move.from_uci(first_move_string)
                    first_move_registered = self.Game.register_move(first_move, resized_chessboard)

            self.add_log("Первый ход за белых :" + first_move_string)

        while True:
            self.master.update()

            if self.Game.moves_to_detect_before_use_engine == 0:
                self.Game.play_next_move()

            found_move, move = self.Game.register_move_if_needed()
            if found_move:
                self.clear_logs()
                self.add_log("Доска :\n" + str(self.Game.board) + "\n")
                self.add_log("\nХоды :\n" + str(self.Game.executed_moves))
