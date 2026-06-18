import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import numpy as np
import math
from copy import deepcopy

class QuantumTicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quantum Tic-Tac-Toe")
        self.root.geometry("800x600")
        
        # Game state
        self.board = self.initialize_board()
        self.move_history = []
        self.move_count = 1
        self.current_player = 'X'
        self.game_mode = None
        
        # GUI components
        self.create_widgets()
        
    def initialize_board(self):
        """Creates a 3x3 board with empty lists to hold quantum moves"""
        return [[[] for _ in range(3)] for _ in range(3)]
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Game mode selection
        mode_frame = ttk.LabelFrame(main_frame, text="Game Mode", padding="5")
        mode_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(mode_frame, text="Human vs Human", 
                  command=lambda: self.start_game("human_vs_human")).grid(row=0, column=0, padx=5)
        ttk.Button(mode_frame, text="Human vs AI", 
                  command=lambda: self.start_game("human_vs_ai")).grid(row=0, column=1, padx=5)
        ttk.Button(mode_frame, text="Reset Game", 
                  command=self.reset_game).grid(row=0, column=2, padx=5)
        
        # Game board frame
        board_frame = ttk.LabelFrame(main_frame, text="Quantum Board", padding="5")
        board_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Create board buttons
        self.board_buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = tk.Button(board_frame, text=f"{i*3+j+1}", width=20, height=6,
                              font=("Arial", 8), bg="lightgray")
                btn.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(btn)
            self.board_buttons.append(row_buttons)
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Game Controls", padding="5")
        control_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)
        
        # Current player display
        self.player_label = ttk.Label(control_frame, text="Current Player: X", font=("Arial", 12, "bold"))
        self.player_label.grid(row=0, column=0, pady=5)
        
        # Make move button
        self.move_button = ttk.Button(control_frame, text="Make Quantum Move", 
                                     command=self.make_move_gui, state="disabled")
        self.move_button.grid(row=1, column=0, pady=5)
        
        # Weights display
        weights_frame = ttk.LabelFrame(control_frame, text="Quantum Weights", padding="5")
        weights_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.weights_text = tk.Text(weights_frame, height=10, width=30, font=("Courier", 8))
        self.weights_text.grid(row=0, column=0)
        
        # Move history
        history_frame = ttk.LabelFrame(main_frame, text="Move History", padding="5")
        history_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.history_text = tk.Text(history_frame, height=6, width=80, font=("Courier", 8))
        self.history_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Scrollbar for history
        history_scroll = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_text.yview)
        history_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.history_text.configure(yscrollcommand=history_scroll.set)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
    def start_game(self, mode):
        """Start a new game with specified mode"""
        self.game_mode = mode
        self.reset_game()
        self.move_button.config(state="normal")
        self.update_display()
        
    def reset_game(self):
        """Reset game state"""
        self.board = self.initialize_board()
        self.move_history = []
        self.move_count = 1
        self.current_player = 'X'
        self.update_display()
        
    def get_quantum_state_gui(self, player, move_number):
        """Get quantum state input via GUI dialog"""
        dialog = QuantumStateDialog(self.root, player, move_number)
        self.root.wait_window(dialog.dialog)
        return dialog.result
    
    def make_move_gui(self):
        """Handle move making via GUI"""
        if not self.game_mode:
            messagebox.showwarning("No Game Mode", "Please select a game mode first!")
            return
            
        if self.current_player == 'X' or self.game_mode == "human_vs_human":
            # Human move
            self.make_quantum_move(self.current_player, self.move_count)
        else:
            # AI move
            self.make_ai_move()
            
    def make_quantum_move(self, player, move_number):
        """Process a quantum move with GUI input"""
        while True:
            # Get desired state from player
            desired_state = self.get_quantum_state_gui(player, move_number)
            
            if desired_state is None:
                return  # User cancelled
            
            # Get previous vectors for orthogonality check
            previous_vectors = [vec for _, vec, _, _ in self.move_history]
            
            # Calculate orthogonal move
            orthogonal_vector = self.calculate_orthogonal_move(desired_state, previous_vectors)
            
            if orthogonal_vector is None:
                messagebox.showerror("Invalid Move", 
                                   "Cannot create orthogonal move with this state. Please try different magnitudes.")
                continue
            
            # Get squares where this move will appear
            occupied_squares = self.vector_to_squares(orthogonal_vector)
            
            if len(occupied_squares) == 0:
                messagebox.showerror("Invalid Move", "No valid squares selected. Please try again.")
                continue
            
            # Update board
            move_data = {'player': player, 'move_number': move_number, 'amplitude': 0}
            for sq in occupied_squares:
                row, col = sq // 3, sq % 3
                move_data_copy = move_data.copy()
                move_data_copy['amplitude'] = float(abs(orthogonal_vector[sq]))
                self.board[row][col].append(move_data_copy)
            
            # Store in move history
            self.move_history.append((player, orthogonal_vector, move_number, occupied_squares))
            
            # Update display
            self.update_display()
            
            # Check for win
            weights = self.calculate_weights_from_amplitudes()
            winner = self.check_win(weights)
            
            if winner:
                messagebox.showinfo("Game Over", f"Player {winner} wins!")
                self.move_button.config(state="disabled")
                return
            
            # Check move limit
            if len(self.move_history) >= 9:
                messagebox.showinfo("Game Over", "Maximum moves reached! It's a draw!")
                self.move_button.config(state="disabled")
                return
            
            # Switch players
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.move_count += 1
            self.player_label.config(text=f"Current Player: {self.current_player}")
            
            break
    
    def make_ai_move(self):
        """Make AI move using minimax algorithm"""
        messagebox.showinfo("AI Move", "AI is calculating optimal move...")
        
        optimal_move, score = self.get_optimal_move('O')
        
        if optimal_move is not None:
            # Apply AI move
            occupied_squares = self.vector_to_squares(optimal_move)
            move_data = {'player': 'O', 'move_number': self.move_count, 'amplitude': 0}
            
            for sq in occupied_squares:
                row, col = sq // 3, sq % 3
                move_data_copy = move_data.copy()
                move_data_copy['amplitude'] = float(abs(optimal_move[sq]))
                self.board[row][col].append(move_data_copy)
            
            self.move_history.append(('O', optimal_move, self.move_count, occupied_squares))
            
            # Update display
            self.update_display()
            
            # Check for win
            weights = self.calculate_weights_from_amplitudes()
            winner = self.check_win(weights)
            
            if winner:
                messagebox.showinfo("Game Over", f"Player {winner} wins!")
                self.move_button.config(state="disabled")
                return
            
            # Check move limit
            if len(self.move_history) >= 9:
                messagebox.showinfo("Game Over", "Maximum moves reached! It's a draw!")
                self.move_button.config(state="disabled")
                return
            
            # Switch to human player
            self.current_player = 'X'
            self.move_count += 1
            self.player_label.config(text=f"Current Player: {self.current_player}")
        else:
            messagebox.showerror("AI Error", "AI cannot find valid move!")
    
    def update_display(self):
        """Update all GUI displays"""
        # Update board buttons
        for i in range(3):
            for j in range(3):
                cell = self.board[i][j]
                if cell:
                    text = "\n".join(f"{move['player']}{move['move_number']}\n({move['amplitude']:.2f})" 
                                   for move in cell)
                    color = "lightblue" if any(move['player'] == 'X' for move in cell) else "lightcoral"
                    if any(move['player'] == 'X' for move in cell) and any(move['player'] == 'O' for move in cell):
                        color = "lightgreen"
                else:
                    text = f"{i*3 + j + 1}"
                    color = "lightgray"
                
                self.board_buttons[i][j].config(text=text, bg=color)
        
        # Update weights display
        if self.move_history:
            weights = self.calculate_weights_from_amplitudes()
            weights_text = "Quantum Weights:\n" + "="*20 + "\n"
            line_names = ['Row 1', 'Row 2', 'Row 3', 'Col 1', 'Col 2', 'Col 3', 'Diag 1', 'Diag 2']
            
            for i, name in enumerate(line_names):
                weights_text += f"{name}:\n"
                weights_text += f"  X: {weights['X'][i]:.3f}\n"
                weights_text += f"  O: {weights['O'][i]:.3f}\n"
            
            self.weights_text.delete(1.0, tk.END)
            self.weights_text.insert(1.0, weights_text)
        
        # Update move history
        history_text = "Move History:\n" + "="*40 + "\n"
        for i, (player, vector, move_num, squares) in enumerate(self.move_history):
            history_text += f"Move {move_num}: Player {player} -> Squares {[sq+1 for sq in squares]}\n"
        
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(1.0, history_text)
    
    # Core game logic methods (from original code)
    def calculate_orthogonal_move(self, desired_state, previous_vectors):
        """Calculate orthogonal move using Gram-Schmidt"""
        if not previous_vectors:
            return desired_state / np.linalg.norm(desired_state)
        
        orthogonal_vector = desired_state.copy()
        
        for prev_vec in previous_vectors:
            projection = np.dot(np.conj(prev_vec), orthogonal_vector) * prev_vec
            orthogonal_vector = orthogonal_vector - projection
        
        norm = np.linalg.norm(orthogonal_vector)
        if norm < 1e-10:
            return None
        
        return orthogonal_vector / norm
    
    def vector_to_squares(self, vector):
        """Extract non-zero squares from vector"""
        squares = []
        for i, amp in enumerate(vector):
            if abs(amp) > 1e-10:
                squares.append(i)
        return squares
    
    def calculate_weights_from_amplitudes(self):
        """Calculate quantum weights from amplitudes"""
        total_amp_X = np.zeros(9, dtype=complex)
        total_amp_O = np.zeros(9, dtype=complex)
        
        for player, vector, _, _ in self.move_history:
            if player == 'X':
                total_amp_X += vector
            else:
                total_amp_O += vector
        
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        
        weights = {'X': [], 'O': []}
        for line in lines:
            weight_X = sum(abs(total_amp_X[sq])**2 for sq in line)
            weight_O = sum(abs(total_amp_O[sq])**2 for sq in line)
            weights['X'].append(weight_X)
            weights['O'].append(weight_O)
        
        return weights
    
    def check_win(self, weights):
        """Check for win condition"""
        for i, (wX, wO) in enumerate(zip(weights['X'], weights['O'])):
            if wX >= 1.5:
                return 'X'
            if wO >= 1.5:
                return 'O'
        return None
    
    def get_optimal_move(self, player):
        """Get optimal AI move using minimax"""
        possible_moves = self.generate_possible_moves(player)
        if not possible_moves:
            return None, 0
        
        best_move = None
        best_score = -float('inf') if player == 'X' else float('inf')
        
        for move in possible_moves:
            # Simulate move
            original_board = deepcopy(self.board)
            original_history = deepcopy(self.move_history)
            
            # Apply move
            occupied_squares = self.vector_to_squares(move)
            move_data = {'player': player, 'move_number': len(self.move_history) + 1, 'amplitude': 0}
            
            for sq in occupied_squares:
                row, col = sq // 3, sq % 3
                move_data_copy = move_data.copy()
                move_data_copy['amplitude'] = float(abs(move[sq]))
                self.board[row][col].append(move_data_copy)
            
            self.move_history.append((player, move, len(self.move_history) + 1, occupied_squares))
            
            # Evaluate
            score = self.evaluate_position(player)
            
            # Undo move
            self.board = original_board
            self.move_history = original_history
            
            # Update best move
            if player == 'X' and score > best_score:
                best_score = score
                best_move = move
            elif player == 'O' and score < best_score:
                best_score = score
                best_move = move
        
        return best_move, best_score
    
    def generate_possible_moves(self, player):
        """Generate possible quantum moves"""
        possible_moves = []
        previous_vectors = [vec for _, vec, _, _ in self.move_history]
        
        strategies = [
            [0, 0, 0, 0, 1, 0, 0, 0, 0],  # Center
            [0.5, 0, 0.5, 0, 0, 0, 0.5, 0, 0.5],  # Corners
            [0, 0.5, 0, 0.5, 0, 0.5, 0, 0.5, 0],  # Edges
            [0.6, 0, 0, 0, 0.6, 0, 0, 0, 0.6],  # Diagonal
            [0, 0, 0.6, 0, 0.6, 0, 0.6, 0, 0],  # Anti-diagonal
        ]
        
        for strategy in strategies:
            state = np.array(strategy, dtype=complex)
            if np.linalg.norm(state) > 0:
                state = state / np.linalg.norm(state)
                orthogonal_move = self.calculate_orthogonal_move(state, previous_vectors)
                if orthogonal_move is not None:
                    possible_moves.append(orthogonal_move)
        
        return possible_moves
    
    def evaluate_position(self, player):
        """Evaluate position for given player"""
        weights = self.calculate_weights_from_amplitudes()
        score = 0
        
        for i in range(8):
            my_weight = weights[player][i]
            opp_weight = weights['X' if player == 'O' else 'O'][i]
            
            if my_weight >= 1.5:
                score += 1000
            elif opp_weight >= 1.5:
                score -= 1000
            else:
                score += my_weight * 10 - opp_weight * 8
        
        return score
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

class QuantumStateDialog:
    def __init__(self, parent, player, move_number):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Quantum State Input - Player {player}, Move {move_number}")
        self.dialog.geometry("400x500")
        self.dialog.grab_set()
        
        # Instructions
        instructions = tk.Label(self.dialog, 
                              text=f"Player {player}, Move {move_number}\n"
                                   "Enter magnitudes for quantum superposition on squares 1-9:\n"
                                   "Board layout: 1 2 3\n"
                                   "              4 5 6\n"
                                   "              7 8 9\n"
                                   "Enter 0 for squares you don't want to occupy",
                              justify=tk.LEFT, font=("Arial", 10))
        instructions.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.dialog)
        input_frame.pack(pady=10)
        
        # Create input fields
        self.entries = []
        for i in range(9):
            row = i // 3
            col = i % 3
            
            tk.Label(input_frame, text=f"Square {i+1}:").grid(row=row*2, column=col, padx=5, pady=2)
            entry = tk.Entry(input_frame, width=10)
            entry.grid(row=row*2+1, column=col, padx=5, pady=2)
            entry.insert(0, "0")
            self.entries.append(entry)
        
        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)
        
        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def ok_clicked(self):
        try:
            amplitudes = []
            for entry in self.entries:
                amp = float(entry.get())
                amplitudes.append(amp)
            
            # Convert to numpy array
            state_vector = np.array(amplitudes, dtype=complex)
            
            # Check if valid
            if np.allclose(state_vector, 0):
                messagebox.showerror("Invalid Input", "All amplitudes cannot be zero")
                return
            
            # Normalize
            norm = np.linalg.norm(state_vector)
            state_vector = state_vector / norm
            
            self.result = state_vector
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers")
    
    def cancel_clicked(self):
        self.result = None
        self.dialog.destroy()

if __name__ == "__main__":
    app = QuantumTicTacToeGUI()
    app.run()
