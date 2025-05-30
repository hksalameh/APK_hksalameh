import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

class XOGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎮 لعبة X و O")
        self.root.geometry("500x700")
        self.root.configure(bg='#f0f8ff')
        self.root.resizable(False, False)
        
        # متغيرات اللعبة
        self.board = [None] * 9
        self.is_x_turn = True
        self.game_mode = "human"  # "human" أو "computer"
        self.scores = {"X": 0, "O": 0, "draws": 0}
        self.buttons = []
        self.game_over = False
        
        self.winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # صفوف
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # أعمدة
            [0, 4, 8], [2, 4, 6]  # أقطار
        ]
        
        self.create_widgets()
        
    def create_widgets(self):
        # العنوان
        title_label = tk.Label(
            self.root, 
            text="🎮 لعبة X و O", 
            font=("Arial", 24, "bold"),
            bg='#f0f8ff',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # إطار اختيار نمط اللعب
        mode_frame = tk.Frame(self.root, bg='#f0f8ff')
        mode_frame.pack(pady=10)
        
        self.mode_var = tk.StringVar(value="human")
        
        human_radio = tk.Radiobutton(
            mode_frame,
            text="👥 لاعبان",
            variable=self.mode_var,
            value="human",
            font=("Arial", 12),
            bg='#f0f8ff',
            command=self.change_game_mode
        )
        human_radio.pack(side=tk.LEFT, padx=10)
        
        computer_radio = tk.Radiobutton(
            mode_frame,
            text="🤖 ضد الكمبيوتر",
            variable=self.mode_var,
            value="computer",
            font=("Arial", 12),
            bg='#f0f8ff',
            command=self.change_game_mode
        )
        computer_radio.pack(side=tk.LEFT, padx=10)
        
        # إطار النتائج
        scores_frame = tk.Frame(self.root, bg='#f0f8ff')
        scores_frame.pack(pady=10)
        
        self.score_label = tk.Label(
            scores_frame,
            text=f"X: {self.scores['X']} | O: {self.scores['O']} | تعادل: {self.scores['draws']}",
            font=("Arial", 14, "bold"),
            bg='#e8f4fd',
            fg='#34495e',
            padx=20,
            pady=5,
            relief=tk.RAISED
        )
        self.score_label.pack()
        
        # رسالة الحالة
        self.status_label = tk.Label(
            self.root,
            text="دور اللاعب: X",
            font=("Arial", 16, "bold"),
            bg='#f0f8ff',
            fg='#3498db'
        )
        self.status_label.pack(pady=15)
        
        # إطار اللوحة
        board_frame = tk.Frame(self.root, bg='#2c3e50', padx=5, pady=5)
        board_frame.pack(pady=20)
        
        # إنشاء أزرار اللوحة
        for i in range(9):
            row = i // 3
            col = i % 3
            
            button = tk.Button(
                board_frame,
                text="",
                font=("Arial", 24, "bold"),
                width=4,
                height=2,
                bg='white',
                fg='#2c3e50',
                relief=tk.RAISED,
                borderwidth=2,
                command=lambda idx=i: self.make_move(idx)
            )
            button.grid(row=row, column=col, padx=2, pady=2)
            self.buttons.append(button)
        
        # إطار الأزرار
        buttons_frame = tk.Frame(self.root, bg='#f0f8ff')
        buttons_frame.pack(pady=20)
        
        new_game_btn = tk.Button(
            buttons_frame,
            text="🔄 لعبة جديدة",
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            command=self.reset_game
        )
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        reset_scores_btn = tk.Button(
            buttons_frame,
            text="🗑️ إعادة تعيين النقاط",
            font=("Arial", 12, "bold"),
            bg='#95a5a6',
            fg='white',
            padx=20,
            pady=10,
            command=self.reset_scores
        )
        reset_scores_btn.pack(side=tk.LEFT, padx=10)
        
        # تعليمات
        instructions = tk.Label(
            self.root,
            text="انقر على المربعات للعب\nالهدف: اجعل ثلاث علامات في خط مستقيم",
            font=("Arial", 10),
            bg='#f0f8ff',
            fg='#7f8c8d',
            justify=tk.CENTER
        )
        instructions.pack(pady=10)
    
    def change_game_mode(self):
        self.game_mode = self.mode_var.get()
        self.reset_game()
    
    def make_move(self, index):
        if self.board[index] is not None or self.game_over:
            return
        
        # حركة اللاعب
        self.board[index] = "X" if self.is_x_turn else "O"
        self.update_button(index)
        
        # فحص الفوز أو التعادل
        winner = self.check_winner()
        if winner:
            self.end_game(winner)
            return
        elif None not in self.board:
            self.end_game("draw")
            return
        
        self.is_x_turn = not self.is_x_turn
        self.update_status()
        
        # حركة الكمبيوتر
        if self.game_mode == "computer" and not self.is_x_turn and not self.game_over:
            self.root.after(500, self.computer_move)
    
    def computer_move(self):
        if self.game_over:
            return
            
        move = self.get_best_move()
        if move is not None:
            self.board[move] = "O"
            self.update_button(move)
            
            winner = self.check_winner()
            if winner:
                self.end_game(winner)
                return
            elif None not in self.board:
                self.end_game("draw")
                return
            
            self.is_x_turn = True
            self.update_status()
    
    def get_best_move(self):
        available_moves = [i for i, cell in enumerate(self.board) if cell is None]
        
        # محاولة الفوز
        for move in available_moves:
            test_board = self.board.copy()
            test_board[move] = "O"
            if self.check_winner_for_board(test_board) == "O":
                return move
        
        # منع اللاعب من الفوز
        for move in available_moves:
            test_board = self.board.copy()
            test_board[move] = "X"
            if self.check_winner_for_board(test_board) == "X":
                return move
        
        # أخذ الوسط إذا كان متاحاً
        if 4 in available_moves:
            return 4
        
        # أخذ الزوايا
        corners = [0, 2, 6, 8]
        available_corners = [corner for corner in corners if corner in available_moves]
        if available_corners:
            return random.choice(available_corners)
        
        # أي خانة متاحة
        return random.choice(available_moves) if available_moves else None
    
    def check_winner(self):
        return self.check_winner_for_board(self.board)
    
    def check_winner_for_board(self, board):
        for combination in self.winning_combinations:
            a, b, c = combination
            if board[a] and board[a] == board[b] == board[c]:
                return board[a]
        return None
    
    def update_button(self, index):
        player = self.board[index]
        color = "#3498db" if player == "X" else "#e74c3c"
        self.buttons[index].config(
            text=player,
            fg=color,
            bg='#ecf0f1',
            state=tk.DISABLED
        )
    
    def update_status(self):
        if self.game_over:
            return
            
        current_player = "X" if self.is_x_turn else "O"
        if self.game_mode == "computer" and not self.is_x_turn:
            self.status_label.config(text="🤖 الكمبيوتر يفكر...", fg='#9b59b6')
        else:
            color = "#3498db" if current_player == "X" else "#e74c3c"
            self.status_label.config(text=f"دور اللاعب: {current_player}", fg=color)
    
    def end_game(self, result):
        self.game_over = True
        
        if result == "draw":
            self.scores["draws"] += 1
            self.status_label.config(text="🤝 تعادل!", fg='#f39c12')
            messagebox.showinfo("انتهت اللعبة", "تعادل! 🤝")
        else:
            self.scores[result] += 1
            color = "#27ae60"
            winner_text = f"🏆 الفائز: {result}!"
            self.status_label.config(text=winner_text, fg=color)
            
            # تلوين الخط الفائز
            self.highlight_winning_line(result)
            
            messagebox.showinfo("انتهت اللعبة", f"الفائز هو: {result}! 🏆")
        
        self.update_scores_display()
    
    def highlight_winning_line(self, winner):
        for combination in self.winning_combinations:
            if all(self.board[i] == winner for i in combination):
                for i in combination:
                    self.buttons[i].config(bg='#2ecc71', fg='white')
                break
    
    def update_scores_display(self):
        self.score_label.config(
            text=f"X: {self.scores['X']} | O: {self.scores['O']} | تعادل: {self.scores['draws']}"
        )
    
    def reset_game(self):
        self.board = [None] * 9
        self.is_x_turn = True
        self.game_over = False
        
        # إعادة تعيين الأزرار
        for button in self.buttons:
            button.config(
                text="",
                bg='white',
                fg='#2c3e50',
                state=tk.NORMAL
            )
        
        self.update_status()
    
    def reset_scores(self):
        self.scores = {"X": 0, "O": 0, "draws": 0}
        self.update_scores_display()
        self.reset_game()
    
    def run(self):
        self.root.mainloop()

# تشغيل اللعبة
if __name__ == "__main__":
    game = XOGame()
    game.run()
