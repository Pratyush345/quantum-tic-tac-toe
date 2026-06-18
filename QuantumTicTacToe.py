#1. Initialize board
def initialize_board():
    """
    Creates a 3×3 board where each cell is a list to hold quantum moves.
    Each cell can contain multiple quantum move entries from different players.
    Returns:
        list: A 3x3 nested list where each cell is an empty list ready to store quantum moves
    """
    return [[[] for _ in range(3)] for _ in range(3)]

#2. Get Input
def get_input(player, move_number):
    """
    Takes input from the player to place their move in exactly two different squares,
    simulating a quantum superposition.
    Args:
        player (str): Player identifier ('X' or 'O')
        move_number (int): The current move number for tracking
    Returns:
        tuple: Two different positions (row1, col1, row2, col2) for the quantum move
    """
    print(f"Player {player}, Move {move_number}")
    print("Enter your quantum move (two different squares):")
    print("Board positions are numbered 1-9:")
    print("1 2 3")
    print("4 5 6") 
    print("7 8 9")
    
    while True:
        try:
            pos1 = int(input(f"Enter first position (1-9): ")) - 1
            pos2 = int(input(f"Enter second position (1-9): ")) - 1
            if not (0 <= pos1 <= 8 and 0 <= pos2 <= 8):
                print("Positions must be between 1 and 9.")
                continue
            if pos1 == pos2:
                print("You must choose two different squares for a quantum move.")
                continue
            row1, col1 = pos1 // 3, pos1 % 3
            row2, col2 = pos2 // 3, pos2 % 3
            return (row1, col1, row2, col2)
        except ValueError:
            print("Please enter valid numbers.")

#3. Calculate Weights
def calculate_weights(board):
    """
    Calculates the weight of each player across all rows, columns, and diagonals.
    Returns:
        dict: Dictionary containing weights for each player across all lines
    """
    lines = [
        # Rows
        [(0,0), (0,1), (0,2)],
        [(1,0), (1,1), (1,2)],
        [(2,0), (2,1), (2,2)],
        # Columns  
        [(0,0), (1,0), (2,0)],
        [(0,1), (1,1), (2,1)],
        [(0,2), (1,2), (2,2)],
        # Diagonals
        [(0,0), (1,1), (2,2)],
        [(0,2), (1,1), (2,0)]
    ]
    weights = {'X': [], 'O': []}
    for line in lines:
        for player in ['X', 'O']:
            amplitude_sum = 0.0
            for row, col in line:
                moves_in_cell = len([move for move in board[row][col] if move['player'] == player])
                amplitude_sum += moves_in_cell * 0.5
            weights[player].append(amplitude_sum ** 2)
    return weights

#4. Check Win
def check_win(weights):
    """
    Checks if any line has a weight ≥ 3 for a player and declares the winner.
    Returns:
        str or None: Winner ('X', 'O') or None if no winner yet
    """
    line_names = ['Row 1', 'Row 2', 'Row 3', 'Col 1', 'Col 2', 'Col 3', 'Diagonal 1', 'Diagonal 2']
    for i, (x_weight, o_weight) in enumerate(zip(weights['X'], weights['O'])):
        if x_weight >= 3.0:
            print(f"Player X wins with {line_names[i]}! Weight: {x_weight:.2f}")
            return 'X'
        if o_weight >= 3.0:
            print(f"Player O wins with {line_names[i]}! Weight: {o_weight:.2f}")
            return 'O'
    return None

#5. DIsplay updated board
def display_board(board):
    """
    Prints the current state of the quantum tic-tac-toe board.
    Each cell shows all quantum moves present, e.g., 'X1,O2'.
    """
    print("\nCurrent Quantum Tic-Tac-Toe Board:")
    for i in range(3):
        row_display = []
        for j in range(3):
            cell = board[i][j]
            if cell:
                cell_str = ",".join(f"{move['player']}{move['move_number']}" for move in cell)
            else:
                cell_str = str(i * 3 + j + 1)
            row_display.append(cell_str.ljust(6))
        print(" | ".join(row_display))
        if i < 2:
            print("-" * 22)
    print()

#6. Check if board is full
def is_board_full(board):
    """
    Returns True if all cells have at least one move, False otherwise.
    """
    for row in board:
        for cell in row:
            if not cell:
                return False
    return True

#7. Main game loop
def play_quantum_tic_tac_toe():
    """
    Main game loop demonstrating the four functions working together
    """
    board = initialize_board()
    current_player = 'X'
    move_number = 1
    
    while True:
        display_board(board)
        row1, col1, row2, col2 = get_input(current_player, move_number)
        move_data = {'player': current_player, 'move_number': move_number}
        board[row1][col1].append(move_data)
        board[row2][col2].append(move_data)
        weights = calculate_weights(board)
        winner = check_win(weights)
        if winner:
            display_board(board)
            print(f"Congratulations, Player {winner} wins!")
            break
        if is_board_full(board):
            display_board(board)
            print("It's a draw! No more moves possible.")
            break
        current_player = 'O' if current_player == 'X' else 'X'
        move_number += 1

# Run the game
if __name__ == "__main__":
    play_quantum_tic_tac_toe()


input("Press Enter to exit...")
