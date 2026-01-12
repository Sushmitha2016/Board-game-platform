from tkinter import messagebox
import sqlite3
import random
class GameDatabase:
def _init_(self, db_name="game_db.sqlite"):
self.db_name = db_name
self.initialize_db()
def initialize_db(self):
conn = sqlite3.connect(self.db_name)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS game_history (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
game TEXT,
result TEXT,
score INTEGER
)
""")
conn.commit()
conn.close()
def save_game_history(self, username, game, result, score):
conn = sqlite3.connect(self.db_name)
cursor = conn.cursor()
cursor.execute("INSERT INTO game_history (username, game, result, score) VALUES (?, ?, ?, ?)",
(username, game, result, score))
conn.commit()
conn.close()
def view_history(self, username):
conn = sqlite3.connect(self.db_name)
cursor = conn.cursor()
cursor.execute("SELECT game, result, score FROM game_history WHERE username = ?", (username,))
history = cursor.fetchall()
conn.close()
return "\n".join([f"{game}: {result} (Score: {score})" for game, result, score in history])
class GameApp:
def _init_(self, root):
self.root = root
self.root.title("Game Platform")
self.db = GameDatabase()
self.login_register_window()
def login_register_window(self):
self.login_window = tk.Frame(self.root)
self.login_window.pack()
self.username_label = tk.Label(self.login_window, text="Username")
self.username_label.grid(row=0, column=0)
self.username_entry = tk.Entry(self.login_window)
self.username_entry.grid(row=0, column=1)
self.password_label = tk.Label(self.login_window, text="Password")
self.password_label.grid(row=1, column=0)
self.password_entry = tk.Entry(self.login_window, show="*")
self.password_entry.grid(row=1, column=1)
self.register_button = tk.Button(self.login_window, text="Register", command=self.register)
self.register_button.grid(row=2, column=0)
self.login_button = tk.Button(self.login_window, text="Login", command=self.login)
self.login_button.grid(row=2, column=1)
def register(self):
username = self.username_entry.get()
password = self.password_entry.get()
conn = sqlite3.connect(self.db.db_name)
cursor = conn.cursor()
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
conn.commit()
conn.close()
messagebox.showinfo("Success", "Registered successfully!")
def login(self):
username = self.username_entry.get()
password = self.password_entry.get()
conn = sqlite3.connect(self.db.db_name)
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
user = cursor.fetchone()
conn.close()
if user:
self.login_window.destroy()
self.main_menu(username)
else:
messagebox.showerror("Error", "Invalid credentials")
def main_menu(self, username):
self.main_window = tk.Frame(self.root)
self.main_window.pack()
self.username_label = tk.Label(self.main_window, text=f"Welcome {username}")
self.username_label.grid(row=0, column=0)
self.play_button = tk.Button(self.main_window, text="Play Games", command=lambda: self.play_games(username))
self.play_button.grid(row=1, column=0)
self.view_history_button = tk.Button(self.main_window, text="View History", command=lambda: self.view_history(username))
self.view_history_button.grid(row=2, column=0)
def play_games(self, username):
self.game_select_window = tk.Toplevel(self.root)
self.game_select_window.title("Select a Game")
self.tic_tac_toe_button = tk.Button(self.game_select_window, text="Tic Tac Toe",
command=lambda: self.start_game(username, "Tic Tac Toe"))
self.tic_tac_toe_button.grid(row=0, column=0)
self.checkers_button = tk.Button(self.game_select_window, text="Checkers",
command=lambda: self.start_game(username, "Checkers"))
self.checkers_button.grid(row=1, column=0)
self.snakes_and_ladders_button = tk.Button(self.game_select_window, text="Snakes and Ladders",
command=lambda: self.start_game(username, "Snakes and Ladders"))
self.snakes_and_ladders_button.grid(row=2, column=0)
def start_game(self, username, game):
self.game_select_window.destroy()
if game == "Tic Tac Toe":
self.start_tic_tac_toe(username)
elif game == "Checkers":
self.start_checkers(username)
elif game == "Snakes and Ladders":
self.start_snakes_and_ladders(username)
def start_tic_tac_toe(self, username):
game_window = tk.Toplevel(self.root)
TicTacToe(game_window, username, self.db)
def start_checkers(self, username):
game_window = tk.Toplevel(self.root)
Checkers(game_window, username, self.db)
def start_snakes_and_ladders(self, username):
game_window = tk.Toplevel(self.root)
SnakesAndLadders(game_window, username, self.db)
def view_history(self, username):
history = self.db.view_history(username)
messagebox.showinfo("Game History", history)
class TicTacToe:
def _init_(self, window, username, db):
self.window = window
self.username = username
self.db = db
self.board = [[" " for _ in range(3)] for _ in range(3)]
self.current_player = "X"
self.game_over = False
self.create_game_window()
def create_game_window(self):
self.window.title("Tic Tac Toe")
self.window.geometry("300x300")
self.buttons = [[tk.Button(self.window, text=" ", width=10, height=3, command=lambda r=row, c=col: self.button_click(r, c))
for col in range(3)] for row in range(3)]
for row in range(3):
for col in range(3):
self.buttons[row][col].grid(row=row, column=col)
self.reset_button = tk.Button(self.window, text="Reset", command=self.reset_game)
self.reset_button.grid(row=3, column=0, columnspan=3)
def button_click(self, row, col):
if self.board[row][col] == " " and not self.game_over:
self.board[row][col] = self.current_player
self.buttons[row][col].config(text=self.current_player)
if self.check_winner():
messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
self.db.save_game_history(self.username, "Tic Tac Toe", f"Player {self.current_player} Wins", 1)
self.reset_game()
elif all(self.board[row][col] != " " for row in range(3) for col in range(3)):
messagebox.showinfo("Game Over", "It's a draw!")
self.db.save_game_history(self.username, "Tic Tac Toe", "Draw", 0)
self.reset_game()
else:
self.current_player = "O" if self.current_player == "X" else "X"
def check_winner(self):
for row in range(3):
if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
return True
for col in range(3):
if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
return True
if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
return True
if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
return True
return False
def reset_game(self):
self.board = [[" " for _ in range(3)] for _ in range(3)]
self.current_player = "X"
self.game_over = False
for row in range(3):
for col in range(3):
self.buttons[row][col].config(text=" ")
import tkinter as tk
from tkinter import simpledialog, messagebox
class Checkers:
def _init_(self, root, username, db):
self.root = root
self.username = username
self.db = db
self.player2_name = self.get_player2_name()
self.current_player = "B" # Player 1 starts with black pieces
self.selected_piece = None
self.game_window = None # Game window starts as None
self.initialize_game()
def get_player2_name(self):
# Prompt for Player 2's name
player2_name = simpledialog.askstring("Player 2", "Enter Player 2's name:")
if not player2_name:
player2_name = "Player 2"
return player2_name
def initialize_game(self):
# Debugging print statements
print("Initializing game...")
self.board = self.create_checkers_board()
# Initialize the game window only if it doesn't exist
if not self.game_window:
self.game_window = tk.Toplevel(self.root)
self.game_window.title("Checkers")
self.game_window.geometry("600x600")
# Debugging print to check if the window is being created
print("Game window created!")
self.draw_board()
# Exit button to return to the main menu
exit_button = tk.Button(self.game_window, text="Exit", command=self.quit_game)
exit_button.grid(row=8, column=0, columnspan=8, pady=10)
def create_checkers_board(self):
# Create the initial checkers board setup
board = []
for i in range(8):
row = []
for j in range(8):
if (i + j) % 2 == 1:
if i < 3:
row.append("B") # Black pieces
elif i > 4:
row.append("W") # White pieces
else:
row.append(None)
else:
row.append(None) # White squares
board.append(row)
return board
def draw_board(self):
# Debugging print to see if this function is being called
print("Drawing the board...")
for i in range(8):
for j in range(8):
color = "white" if (i + j) % 2 == 0 else "black"
piece = self.board[i][j]
text = "⚫" if piece == "B" else "⚫" if piece == "W" else " "
# Debugging print to check button creation
print(f"Creating button at ({i}, {j}) with piece: {text}")
button = tk.Button(
self.game_window,
text=text,
bg=color,
fg="white" if color == "black" else "black",
width=5,
height=2,
command=lambda i=i, j=j: self.make_move(i, j),
)
button.grid(row=i, column=j)
def make_move(self, i, j):
if self.selected_piece:
prev_i, prev_j = self.selected_piece
if self.is_valid_move(prev_i, prev_j, i, j):
# Perform the move
self.board[i][j] = self.board[prev_i][prev_j]
self.board[prev_i][prev_j] = None
# Capture opponent piece if jumping
if abs(i - prev_i) == 2:
mid_i, mid_j = (i + prev_i) // 2, (j + prev_j) // 2
self.board[mid_i][mid_j] = None
# Switch players
self.selected_piece = None
self.current_player = "W" if self.current_player == "B" else "B"
self.check_winner()
self.draw_board()
else:
self.selected_piece = None
else:
if self.board[i][j] == self.current_player:
self.selected_piece = (i, j)
def is_valid_move(self, prev_i, prev_j, i, j):
# Check if the move is valid (diagonal and within bounds)
if self.board[i][j] is not None:
return False
dx, dy = abs(i - prev_i), abs(j - prev_j)
if dx == 1 and dy == 1:
return True # Regular move
if dx == 2 and dy == 2:
mid_i, mid_j = (i + prev_i) // 2, (j + prev_j) // 2
if self.board[mid_i][mid_j] is not None and self.board[mid_i][mid_j] != self.current_player:
return True # Jump move
return False
def check_winner(self):
black_count = sum(row.count("B") for row in self.board)
white_count = sum(row.count("W") for row in self.board)
if black_count == 0:
messagebox.showinfo("Game Over", f"{self.player2_name} (White) wins!")
self.quit_game()
elif white_count == 0:
messagebox.showinfo("Game Over", f"{self.username} (Black) wins!")
self.quit_game()
def quit_game(self):
# Debugging print to check if quit_game is working
print("Quitting game...")
self.game_window.destroy()
import tkinter as tk
from tkinter import messagebox, simpledialog
import random
class SnakesAndLadders:
def _init_(self, window, username, db):
self.window = window
self.username = username
self.db = db
self.board = self.create_board()
self.position_player1 = 0
self.position_player2 = 0
self.current_turn = 1 # Player 1 starts
self.player2_name = self.ask_for_player2_name()
self.create_game_window()
def ask_for_player2_name(self):
player2_name = simpledialog.askstring("Player 2 Name", "Enter Player 2's name:")
if not player2_name:
player2_name = "Player 2" # Default name if not provided
return player2_name
def create_board(self):
board = [None for _ in range(100)]
# Add ladders (green)
for _ in range(5):
start = random.randint(1, 99)
end = random.randint(start+1, 99)
board[start] = f"Ladder to {end}"
# Add snakes (red)
for _ in range(5):
start = random.randint(1, 99)
end = random.randint(0, start-1)
board[start] = f"Snake to {end}"
return board
def create_game_window(self):
self.window.title("Snakes and Ladders")
self.window.geometry("400x400")
# Create board (10x10 grid)
self.board_buttons = []
for i in range(10):
row = []
for j in range(10):
button = tk.Button(self.window, text=str(i*10 + j + 1), width=4, height=2,
command=lambda r=i, c=j: self.cell_click(r, c))
button.grid(row=i, column=j)
row.append(button)
self.board_buttons.append(row)
# Update the board visuals based on snakes, ladders, and player positions
self.update_board()
self.roll_button = tk.Button(self.window, text="Roll Dice", command=self.roll_dice)
self.roll_button.grid(row=10, column=0, columnspan=10)
# Quit Button
self.quit_button = tk.Button(self.window, text="Quit Game", command=self.quit_game)
self.quit_button.grid(row=11, column=0, columnspan=10)
def update_board(self):
# Reset all button colors and text
for i in range(10):
for j in range(10):
index = i * 10 + j
button = self.board_buttons[i][j]
button.config(bg="white", text=str(index + 1))
# Mark snakes and ladders
for i in range(100):
if self.board[i] is not None:
row, col = divmod(i, 10)
button = self.board_buttons[row][col]
if "Ladder" in self.board[i]:
button.config(bg="green")
elif "Snake" in self.board[i]:
button.config(bg="red")
# Mark player positions
self.place_player(self.position_player1, "blue")
self.place_player(self.position_player2, "yellow")
def place_player(self, position, color):
if position >= 100:
return # Out of bounds
row, col = divmod(position, 10)
button = self.board_buttons[row][col]
button.config(bg=color)
def roll_dice(self):
dice_roll = random.randint(1, 6)
current_player = self.username if self.current_turn == 1 else self.player2_name
# Show dice roll info for current player
messagebox.showinfo("Dice Roll", f"{current_player} rolled a {dice_roll}")
if self.current_turn == 1:
self.position_player1 += dice_roll
if self.position_player1 >= 100:
self.position_player1 = 100
messagebox.showinfo(f"{self.username} Wins!", f"{self.username} reached the end!")
self.db.save_game_history(self.username, "Snakes and Ladders", f"{self.username} Wins", 1)
self.reset_game()
else:
self.check_for_snakes_or_ladders(1)
self.current_turn = 2
else:
self.position_player2 += dice_roll
if self.position_player2 >= 100:
self.position_player2 = 100
messagebox.showinfo(f"{self.player2_name} Wins!", f"{self.player2_name} reached the end!")
self.db.save_game_history(self.username, "Snakes and Ladders", f"{self.player2_name} Wins", 1)
self.reset_game()
else:
self.check_for_snakes_or_ladders(2)
self.current_turn = 1
# Update board after the roll
self.update_board()
def check_for_snakes_or_ladders(self, player):
if player == 1:
position = self.position_player1
else:
position = self.position_player2
# Check if the player landed on a snake or ladder
if self.board[position] is not None:
if "Ladder" in self.board[position]:
end_position = int(self.board[position].split()[-1])
if player == 1:
self.position_player1 = end_position
else:
self.position_player2 = end_position
messagebox.showinfo("Climbed Ladder!", f"Player {player} climbed the ladder!")
elif "Snake" in self.board[position]:
end_position = int(self.board[position].split()[-1])
if player == 1:
self.position_player1 = end_position
else:
self.position_player2 = end_position
messagebox.showinfo("Bitten by Snake!", f"Player {player} slid down the snake!")
def reset_game(self):
self.position_player1 = 0
self.position_player2 = 0
self.current_turn = 1
self.update_board()
def quit_game(self):
confirm = messagebox.askyesno("Quit Game", "Are you sure you want to quit?")
if confirm:
self.window.quit()
if _name_ == "_main_":
root = tk.Tk()
app = GameApp(root)
