import tkinter as tk
from tkinter import font
import random


class TicTacToeGUI:
    def __init__(self, root_):
        self.root = root_
        self.root.title("Unbeatable Tic-Tac-Toe")
        self.root.geometry("500x600")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)

        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        self.game_active = True

        self.title_font = font.Font(family="Arial", size=24, weight="bold")
        self.button_font = font.Font(family="Arial", size=36, weight="bold")
        self.status_font = font.Font(family="Arial", size=14)
        self.score_font = font.Font(family="Arial", size=18, weight="bold")

        self.title_label = tk.Label(
            root_,
            text="Tic-Tac-Toe",
            font=self.title_font,
            bg="#2c3e50",
            fg="#ecf0f1",
            pady=10
        )
        self.title_label.pack()

        self.score_frame = tk.Frame(root_, bg="#34495e", padx=10, pady=5)
        self.score_frame.pack(fill=tk.X, padx=20)

        self.x_score = 0
        self.o_score = 0
        self.ties = 0

        self.score_x = tk.Label(
            self.score_frame,
            text=f"AI (X): {self.x_score}",
            font=self.score_font,
            bg="#34495e",
            fg="#e74c3c",
            padx=10
        )
        self.score_x.pack(side=tk.LEFT)

        self.score_ties = tk.Label(
            self.score_frame,
            text=f"Ties: {self.ties}",
            font=self.score_font,
            bg="#34495e",
            fg="#f1c40f",
            padx=10
        )
        self.score_ties.pack(side=tk.LEFT)

        self.score_o = tk.Label(
            self.score_frame,
            text=f"You (O): {self.o_score}",
            font=self.score_font,
            bg="#34495e",
            fg="#3498db",
            padx=10
        )
        self.score_o.pack(side=tk.RIGHT)

        self.board_frame = tk.Frame(root_, bg="#34495e", padx=10, pady=10)
        self.board_frame.pack(padx=20, pady=20)

        self.buttons = []
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    font=self.button_font,
                    width=3,
                    height=1,
                    bg="#95a5a6",
                    activebackground="#bdc3c7",
                    command=lambda row=i, col=j: self.make_human_move(row * 3 + col)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(btn)

        self.status_label = tk.Label(
            root_,
            text="AI is thinking...",
            font=self.status_font,
            bg="#2c3e50",
            fg="#ecf0f1",
            pady=10
        )
        self.status_label.pack()

        self.control_frame = tk.Frame(root_, bg="#2c3e50", pady=10)
        self.control_frame.pack(pady=10)

        self.new_game_btn = tk.Button(
            self.control_frame,
            text="New Game",
            font=self.status_font,
            bg="#27ae60",
            fg="white",
            padx=10,
            pady=5,
            command=self.reset_game
        )
        self.new_game_btn.pack(side=tk.LEFT, padx=10)

        self.quit_btn = tk.Button(
            self.control_frame,
            text="Quit",
            font=self.status_font,
            bg="#c0392b",
            fg="white",
            padx=10,
            pady=5,
            command=self.root.destroy
        )
        self.quit_btn.pack(side=tk.LEFT, padx=10)

        self.root.after(1000, self.ai_move)

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.check_winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def check_winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            self.highlight_winning_line([(row_ind, i) for i in range(3)])
            return True

        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):
            self.highlight_winning_line([(i, col_ind) for i in range(3)])
            return True

        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                self.highlight_winning_line([(i, i) for i in range(3)])
                return True

            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                self.highlight_winning_line([(i, 2 - i) for i in range(3)])
                return True

        return False

    def highlight_winning_line(self, positions):
        for row, col in positions:
            button_index = row * 3 + col
            if self.current_winner == 'X':
                self.buttons[button_index].config(bg="#e74c3c")
            else:
                self.buttons[button_index].config(bg="#3498db", fg="#ffffff")

    def make_human_move(self, square):
        if not self.game_active or self.board[square] != ' ' or self.current_winner:
            return

        self.buttons[square].config(text="O", fg="#3498db")
        self.make_move(square, 'O')

        if self.current_winner == 'O':
            self.status_label.config(text="You win! (This shouldn't happen!)")
            self.o_score += 1
            self.update_score()
            self.game_active = False
            return

        if not self.empty_squares():
            self.status_label.config(text="It's a tie!")
            self.ties += 1
            self.update_score()
            self.game_active = False
            return

        self.status_label.config(text="AI is thinking...")
        self.root.update()
        self.root.after(500, self.ai_move)

    def ai_move(self):
        if not self.game_active or self.current_winner:
            return

        move = self.get_best_move()
        self.buttons[move].config(text="X", fg="#e74c3c")
        self.make_move(move, 'X')

        if self.current_winner == 'X':
            self.status_label.config(text="AI wins!")
            self.x_score += 1
            self.update_score()
            self.game_active = False
            return

        if not self.empty_squares():
            self.status_label.config(text="It's a tie!")
            self.ties += 1
            self.update_score()
            self.game_active = False
            return

        self.status_label.config(text="Your turn")

    def update_score(self):
        self.score_x.config(text=f"AI (X): {self.x_score}")
        self.score_o.config(text=f"You (O): {self.o_score}")
        self.score_ties.config(text=f"Ties: {self.ties}")

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        self.game_active = True

        for button in self.buttons:
            button.config(text="", bg="#95a5a6", fg="#3498db")

        self.status_label.config(text="AI is thinking...")
        self.root.after(500, self.ai_move)

    def minimax(self, depth, is_maximizing, alpha, beta):
        if self.current_winner == 'X':
            return 10 - depth
        elif self.current_winner == 'O':
            return depth - 10
        elif not self.empty_squares():
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for move in self.available_moves():
                self.make_move(move, 'X')
                eval_ = self.minimax(depth + 1, False, alpha, beta)
                self.board[move] = ' '
                self.current_winner = None
                max_eval = max(max_eval, eval_)
                alpha = max(alpha, eval_)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.available_moves():
                self.make_move(move, 'O')
                eval_ = self.minimax(depth + 1, True, alpha, beta)
                self.board[move] = ' '
                self.current_winner = None
                min_eval = min(min_eval, eval_)
                beta = min(beta, eval_)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self):
        for move in self.available_moves():
            self.board[move] = 'X'
            if self.check_winner(move, 'X'):
                self.board[move] = ' '
                self.current_winner = None
                return move
            self.board[move] = ' '

        for move in self.available_moves():
            self.board[move] = 'O'
            if self.check_winner(move, 'O'):
                self.board[move] = ' '
                return move
            self.board[move] = ' '

        if self.board[4] == ' ':
            return 4

        corners = [0, 2, 6, 8]
        available_corners = [move for move in corners if self.board[move] == ' ']
        if available_corners:
            return random.choice(available_corners)

        sides = [1, 3, 5, 7]
        available_sides = [move for move in sides if self.board[move] == ' ']
        if available_sides:
            return random.choice(available_sides)

        best_score = float('-inf')
        best_move = None
        for move in self.available_moves():
            self.board[move] = 'X'
            score = self.minimax(0, False, float('-inf'), float('inf'))
            self.board[move] = ' '
            self.current_winner = None
            if score > best_score:
                best_score = score
                best_move = move

        return best_move


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()

"""
მიმოხილვა
ეს არის Tic-Tac-Toe თამაში Python-ის Tkinter ბიბლიოთეკის გამოყენებით შექმნილი გრაფიკული ინტერფეისით. თამაში მოიცავს:

3×3 ზომის ღილაკების ბადეს, რომელიც წარმოადგენს სათამაშო დაფას
მოთამაშის ქულების თვალყურის დევნება (O), ხელოვნური ინტელექტი (X) და ფრე
სუფთა, თანამედროვე ინტერფეისი ფერადი კოდირებული ელემენტებით
სტრატეგიული ხელოვნური ინტელექტი, რომელიც თამაშობს ოპტიმალურად, მაგრამ სამართლიანად

კლასის სტრუქტურა
კოდი განსაზღვრავს ერთ კლას TicTacToeGUI-ს, რომელიც ამუშავებს თამაშის ყველა ლოგიკას და ინტერფეისის ელემენტს. ინიციალიზაცია
ინიციალიზაციისას, თამაში:

ქმნის 500×600 პიქსელის ფანჯარას მუქი ლურჯი ფონით
აწყობს სათამაშო დაფას 9 ცარიელი სივრცის სიის სახით
კონფიგურირებს შრიფტებს სხვადასხვა ინტერფეისის ელემენტებისთვის
ქმნის სათაურის ეტიკეტს ზედა ნაწილში
აწყობს ქულების ჩვენებას, რომელიც აჩვენებს ხელოვნურ ინტელექტს (X), მოთამაშეს (O) და ფრეს რაოდენობას
ქმნის ღილაკების 3×3 ბადეს სათამაშო დაფისთვის
ამატებს სტატუსის ეტიკეტს თამაშის მდგომარეობის ინფორმაციის საჩვენებლად
მოიცავს საკონტროლო ღილაკებს ახალი თამაშის დასაწყებად ან დასასრულებლად
იწყება ხელოვნური ინტელექტის მიერ პირველი სვლით

თამაშის ლოგიკა
თამაში იყენებს სტანდარტულ Tic-Tac-Toe წესებს:

მოთამაშეები რიგრიგობით ათავსებენ თავიანთ სიმბოლოებს (X ან O) ცარიელ კვადრატებზე
პირველი მოთამაშე, რომელიც ზედიზედ სამ სიმბოლოს მიიღებს (ჰორიზონტალურად, ვერტიკალურად ან დიაგონალურად), იმარჯვებს
თუ ყველა კვადრატი შეივსება გამარჯვებულის გარეშე, თამაში მთავრდება ფრედ

ხელოვნური ინტელექტის ლოგიკა
ხელოვნური ინტელექტი იყენებს სტრატეგიულ მიდგომას:

ჯერ ამოწმებს, შეუძლია თუ არა მას დაუყოვნებლივ გამარჯვება
თუ არა, ამოწმებს, სჭირდება თუ არა მოთამაშის დაბლოკვა გამარჯვება
თუ არც ერთი, ის მიჰყვება სტრატეგიულ სვლებს:

იღებს ცენტრალურ კვადრატს, თუ შესაძლებელია
ადგენს პოტენციურ მომგებიან ნიმუშებს
იღებს კუთხის კვადრატებს, როდესაც ეს ხელსაყრელია
უკან ბრუნდება გვერდზე ან შემთხვევით მოძრაობს, თუ უკეთესი ვარიანტი არ არსებობს

თამაშის მიმდინარეობა

თამაში იწყება ხელოვნური ინტელექტით, რომელიც ასრულებს სვლას (ჩვეულებრივ იღებს ცენტრს ან კუთხეს)
მოთამაშე დააწკაპუნებს ცარიელ კვადრატზე O-ს დასაყენებლად
თითოეული სვლის შემდეგ, თამაში ამოწმებს გამარჯვებულს
თუ გამარჯვებულია, ის გამოყოფს მომგებიან ხაზს და აახლებს ანგარიშს
თუ დაფა გაივსება გამარჯვებულის გარეშე, ის აცხადებს ფრეს
მოთამაშეებს შეუძლიათ ახალი თამაშის დაწყება ნებისმიერ დროს
"""
