import numpy as np
import math
from copy import deepcopy

class QuantumTicTacToe:
    def __init__(self):
        self.board = self.initialize_board()
        self.move_history = []  # Store (player, vector, move_number, squares) tuples
        self.move_count = 1
        self.current_player = 'X'
        
    def initialize_board(self):
        """Creates a 3x3 board with empty lists to hold quantum moves"""
        return [[[] for _ in range(3)] for _ in range(3)]
    
    def get_quantum_state_input(self, player, move_number):
        """
        Gets player input for quantum state magnitudes on 9 squares
        Returns: numpy array of 9 complex amplitudes
        """
        print(f"\nPlayer {player}, Move {move_number}")
        print("Enter magnitudes for quantum superposition on squares 1-9:")
        print("Board layout:")
        print("1 2 3")
        print("4 5 6") 
        print("7 8 9")
        print("Enter 0 for squares you don't want to occupy")
        
        while True:
            try:
                amplitudes = []
                for i in range(9):
                    amp = float(input(f"Magnitude for square {i+1}: "))
                    amplitudes.append(amp)
                
                # Convert to numpy array and normalize
                state_vector = np.array(amplitudes, dtype=complex)
                
                # Check if valid (non-zero)
                if np.allclose(state_vector, 0):
                    print("Invalid: All amplitudes cannot be zero")
                    continue
                
                # Normalize the state
                norm = np.linalg.norm(state_vector)
                state_vector = state_vector / norm
                
                return state_vector
                
            except ValueError:
                print("Please enter valid numbers")
    
    def calculate_orthogonal_move(self, desired_state, previous_vectors):
        """
        Calculates a quantum move orthogonal to all previous moves using Gram-Schmidt
        Args:
            desired_state: numpy array of 9 amplitudes
            previous_vectors: list of previous move vectors
        Returns:
            numpy array: orthogonal vector or None if impossible
        """
        if not previous_vectors:
            # First move - just normalize
            return desired_state / np.linalg.norm(desired_state)
        
        # Apply Gram-Schmidt orthogonalization
        orthogonal_vector = desired_state.copy()
        
        # Subtract projections onto all previous vectors
        for prev_vec in previous_vectors:
            projection = np.dot(np.conj(prev_vec), orthogonal_vector) * prev_vec
            orthogonal_vector = orthogonal_vector - projection
        
        # Check if the result is too small (nearly linearly dependent)
        norm = np.linalg.norm(orthogonal_vector)
        if norm < 1e-10:
            return None
        
        # Normalize the orthogonal vector
        return orthogonal_vector / norm
    
    def vector_to_squares(self, vector):
        """Extract non-zero squares from vector for board display"""
        squares = []
        for i, amp in enumerate(vector):
            if abs(amp) > 1e-10:
                squares.append(i)
        return squares
    
    def make_quantum_move(self, player, move_number):
        """
        Process a complete quantum move with orthogonality constraint
        """
        while True:
            # Get desired state from player
            desired_state = self.get_quantum_state_input(player, move_number)
            
            # Get previous vectors for orthogonality check
            previous_vectors = [vec for _, vec, _, _ in self.move_history]
            
            # Calculate orthogonal move
            orthogonal_vector = self.calculate_orthogonal_move(desired_state, previous_vectors)
            
            if orthogonal_vector is None:
                print("Cannot create orthogonal move with this state. Please try different magnitudes.")
                continue
            
            # Get squares where this move will appear
            occupied_squares = self.vector_to_squares(orthogonal_vector)
            
            if len(occupied_squares) == 0:
                print("No valid squares selected. Please try again.")
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
            
            print(f"Orthogonal move created! Squares: {[sq+1 for sq in occupied_squares]}")
            break
    
    def calculate_weights_from_amplitudes(self):
        """
        Calculate quantum weights using actual amplitudes from move history
        """
        # Initialize amplitude sums per square per player
        total_amp_X = np.zeros(9, dtype=complex)
        total_amp_O = np.zeros(9, dtype=complex)
        
        # Sum amplitudes from move history
        for player, vector, _, _ in self.move_history:
            if player == 'X':
                total_amp_X += vector
            else:
                total_amp_O += vector
        
        # Define winning lines
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        weights = {'X': [], 'O': []}
        
        for line in lines:
            # Calculate weight as sum of squared amplitudes along line
            weight_X = sum(abs(total_amp_X[sq])**2 for sq in line)
            weight_O = sum(abs(total_amp_O[sq])**2 for sq in line)
            
            weights['X'].append(weight_X)
            weights['O'].append(weight_O)
        
        return weights
    
    def check_win(self, weights):
        """Check for quantum win condition (weight >= 1.5)"""
        line_names = [
            'Row 1', 'Row 2', 'Row 3',
            'Column 1', 'Column 2', 'Column 3', 
            'Diagonal 1', 'Diagonal 2'
        ]
        
        for i, (wX, wO) in enumerate(zip(weights['X'], weights['O'])):
            if wX >= 1.5:
                print(f"Player X wins with {line_names[i]}! Weight: {wX:.3f}")
                return 'X'
            if wO >= 1.5:
                print(f"Player O wins with {line_names[i]}! Weight: {wO:.3f}")
                return 'O'
        return None
    
    def display_board(self):
        """Display current board state with quantum amplitudes"""
        print("\nQuantum Tic-Tac-Toe Board (showing amplitudes):")
        print("=" * 50)
        
        for i in range(3):
            row_display = []
            for j in range(3):
                cell = self.board[i][j]
                if cell:
                    cell_str = ", ".join(f"{move['player']}{move['move_number']}({move['amplitude']:.2f})" 
                                       for move in cell)
                else:
                    cell_str = f"[{i*3 + j + 1}]"
                row_display.append(cell_str.ljust(15))
            print(" | ".join(row_display))
            if i < 2:
                print("-" * 50)
        print()
    
    def evaluate_position(self, player):
        """
        Evaluate current position for given player
        Returns a score based on quantum weights
        """
        weights = self.calculate_weights_from_amplitudes()
        
        score = 0
        for i in range(8):  # 8 winning lines
            my_weight = weights[player][i]
            opp_weight = weights['X' if player == 'O' else 'O'][i]
            
            # Scoring system
            if my_weight >= 1.5:
                score += 1000  # Win
            elif opp_weight >= 1.5:
                score -= 1000  # Loss
            else:
                score += my_weight * 10 - opp_weight * 8
        
        return score
    
    def generate_possible_moves(self, player):
        """
        Generate possible quantum moves that satisfy orthogonality
        Returns list of valid state vectors
        """
        possible_moves = []
        previous_vectors = [vec for _, vec, _, _ in self.move_history]
        
        # Generate strategic quantum states to try
        strategies = [
            # Center focus
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            # Corner strategy
            [0.5, 0, 0.5, 0, 0, 0, 0.5, 0, 0.5],
            # Edge focus
            [0, 0.5, 0, 0.5, 0, 0.5, 0, 0.5, 0],
            # Diagonal
            [0.6, 0, 0, 0, 0.6, 0, 0, 0, 0.6],
            # Anti-diagonal
            [0, 0, 0.6, 0, 0.6, 0, 0.6, 0, 0],
        ]
        
        for strategy in strategies:
            state = np.array(strategy, dtype=complex)
            if np.linalg.norm(state) > 0:
                state = state / np.linalg.norm(state)
                orthogonal_move = self.calculate_orthogonal_move(state, previous_vectors)
                if orthogonal_move is not None:
                    possible_moves.append(orthogonal_move)
        
        return possible_moves
    
    def minimax(self, depth, is_maximizing, alpha=-float('inf'), beta=float('inf'), max_depth=3):
        """
        Minimax algorithm with alpha-beta pruning for quantum tic-tac-toe
        """
        weights = self.calculate_weights_from_amplitudes()
        winner = self.check_win(weights)
        
        # Terminal states
        if winner == 'X':
            return 1000 - depth
        elif winner == 'O':
            return -1000 + depth
        elif depth >= max_depth:
            return self.evaluate_position('X') - self.evaluate_position('O')
        
        if is_maximizing:  # X's turn
            max_eval = -float('inf')
            possible_moves = self.generate_possible_moves('X')
            
            for move in possible_moves:
                # Simulate move
                original_board = deepcopy(self.board)
                original_history = deepcopy(self.move_history)
                
                # Apply move
                occupied_squares = self.vector_to_squares(move)
                move_data = {'player': 'X', 'move_number': len(self.move_history) + 1, 'amplitude': 0}
                for sq in occupied_squares:
                    row, col = sq // 3, sq % 3
                    move_data_copy = move_data.copy()
                    move_data_copy['amplitude'] = float(abs(move[sq]))
                    self.board[row][col].append(move_data_copy)
                
                self.move_history.append(('X', move, len(self.move_history) + 1, occupied_squares))
                
                # Recursive call
                eval_score = self.minimax(depth + 1, False, alpha, beta, max_depth)
                
                # Undo move
                self.board = original_board
                self.move_history = original_history
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break
            
            return max_eval
        
        else:  # O's turn
            min_eval = float('inf')
            possible_moves = self.generate_possible_moves('O')
            
            for move in possible_moves:
                # Simulate move
                original_board = deepcopy(self.board)
                original_history = deepcopy(self.move_history)
                
                # Apply move
                occupied_squares = self.vector_to_squares(move)
                move_data = {'player': 'O', 'move_number': len(self.move_history) + 1, 'amplitude': 0}
                for sq in occupied_squares:
                    row, col = sq // 3, sq % 3
                    move_data_copy = move_data.copy()
                    move_data_copy['amplitude'] = float(abs(move[sq]))
                    self.board[row][col].append(move_data_copy)
                
                self.move_history.append(('O', move, len(self.move_history) + 1, occupied_squares))
                
                # Recursive call
                eval_score = self.minimax(depth + 1, True, alpha, beta, max_depth)
                
                # Undo move
                self.board = original_board
                self.move_history = original_history
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break
            
            return min_eval
    
    def get_optimal_move(self, player):
        """
        Find optimal move using minimax algorithm
        """
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
            
            # Evaluate using minimax
            score = self.minimax(0, player == 'O')  # Switch perspective
            
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

# Game mode implementations
def play_human_vs_human(game):
    """Human vs Human mode with magnitude selection"""
    print("\n=== HUMAN VS HUMAN MODE ===")
    print("Both players will specify quantum state magnitudes")
    print("The system will ensure orthogonality constraints are satisfied")
    
    while True:
        game.display_board()
        
        # Show current weights
        weights = game.calculate_weights_from_amplitudes()
        print("\nCurrent quantum weights:")
        line_names = ['Row 1', 'Row 2', 'Row 3', 'Col 1', 'Col 2', 'Col 3', 'Diag 1', 'Diag 2']
        for i, name in enumerate(line_names):
            print(f"{name}: X={weights['X'][i]:.3f}, O={weights['O'][i]:.3f}")
        
        # Make move
        game.make_quantum_move(game.current_player, game.move_count)
        
        # Check for win
        weights = game.calculate_weights_from_amplitudes()
        winner = game.check_win(weights)
        if winner:
            game.display_board()
            return winner
        
        # Check if we can continue (orthogonal space available)
        if len(game.move_history) >= 9:
            print("Maximum moves reached!")
            return "Draw"
        
        # Switch players
        game.current_player = 'O' if game.current_player == 'X' else 'X'
        game.move_count += 1

def play_human_vs_ai(game):
    """Human vs AI mode with optimal AI moves"""
    print("\n=== HUMAN VS AI MODE ===")
    print("You are X, AI is O")
    print("AI will calculate optimal moves using minimax algorithm")
    
    while True:
        game.display_board()
        
        if game.current_player == 'X':
            # Human move
            print("Your turn (Human):")
            game.make_quantum_move(game.current_player, game.move_count)
        else:
            # AI move
            print("AI is calculating optimal move...")
            optimal_move, score = game.get_optimal_move('O')
            
            if optimal_move is not None:
                print(f"AI chooses move with evaluation score: {score:.2f}")
                
                # Apply AI move
                occupied_squares = game.vector_to_squares(optimal_move)
                move_data = {'player': 'O', 'move_number': game.move_count, 'amplitude': 0}
                for sq in occupied_squares:
                    row, col = sq // 3, sq % 3
                    move_data_copy = move_data.copy()
                    move_data_copy['amplitude'] = float(abs(optimal_move[sq]))
                    game.board[row][col].append(move_data_copy)
                
                game.move_history.append(('O', optimal_move, game.move_count, occupied_squares))
                print(f"AI occupies squares: {[sq+1 for sq in occupied_squares]}")
            else:
                print("AI cannot find valid move!")
                return "Draw"
        
        # Check for win
        weights = game.calculate_weights_from_amplitudes()
        winner = game.check_win(weights)
        if winner:
            game.display_board()
            return winner
        
        # Check move limit
        if len(game.move_history) >= 9:
            print("Maximum moves reached!")
            return "Draw"
        
        # Switch players
        game.current_player = 'O' if game.current_player == 'X' else 'X'
        game.move_count += 1

# Example usage
if __name__ == "__main__":
    game = QuantumTicTacToe()
    
    # Choose game mode
    print("Choose game mode:")
    print("1. Human vs Human")
    print("2. Human vs AI")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        winner = play_human_vs_human(game)
    elif choice == "2":
        winner = play_human_vs_ai(game)
    else:
        print("Invalid choice")
        winner = None
    
    if winner:
        print(f"\nGame Over! Winner: {winner}")
