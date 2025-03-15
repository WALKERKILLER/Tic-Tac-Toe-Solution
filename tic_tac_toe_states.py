# -*- coding: utf-8 -*-

import itertools
import json
from collections import defaultdict

def is_valid_board(board):
    """Check if a board state is valid according to Tic-Tac-Toe rules."""
    # Convert board to flat list
    flat_board = [cell for row in board for cell in row]
    
    # Count X's and O's
    x_count = flat_board.count(1)  # X is represented by 1
    o_count = flat_board.count(2)  # O is represented by 2
    
    # Check if counts are valid (X goes first, so X count should be equal to or one more than O count)
    if not (x_count == o_count or x_count == o_count + 1):
        return False
    
    # Check if game is already won
    x_won = has_won(board, 1)
    o_won = has_won(board, 2)
    
    # If both have winning lines, it's invalid
    if x_won and o_won:
        return False
    
    # If X has won, X count should be one more than O count
    if x_won and x_count != o_count + 1:
        return False
    
    # If O has won, counts should be equal
    if o_won and x_count != o_count:
        return False
    
    return True

def has_won(board, player):
    """Check if the specified player has won."""
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    
    # Check diagonals
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    
    return False

def generate_all_possible_boards():
    """Generate all possible board configurations."""
    # All possible ways to place 0, 1, 2 in a 3x3 grid
    all_boards = []
    for config in itertools.product([0, 1, 2], repeat=9):
        board = [list(config[i:i+3]) for i in range(0, 9, 3)]
        all_boards.append(board)
    return all_boards

def find_valid_boards():
    """Find all valid board states according to Tic-Tac-Toe rules."""
    all_boards = generate_all_possible_boards()
    valid_boards = []
    
    for board in all_boards:
        if is_valid_board(board):
            valid_boards.append(board)
    
    # Verify we have the correct number of states
    print(f"Generated {len(valid_boards)} valid board states")
    
    # Check if empty state (all 0) exists
    empty_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    empty_board_found = False
    for board in valid_boards:
        if board == empty_board:
            empty_board_found = True
            break
    
    if not empty_board_found:
        print("Warning: Empty board not found in valid states!")
        valid_boards.append(empty_board)
    
    return valid_boards

def board_to_string(board):
    """Convert a board to a string representation for comparison."""
    return ''.join(str(cell) for row in board for cell in row)

def remove_duplicates(boards):
    """Remove duplicate boards (considering rotations and reflections)."""
    unique_boards = []
    seen = set()
    
    for board in boards:
        variants = get_all_variants(board)
        variant_strings = [board_to_string(v) for v in variants]
        
        if not any(vs in seen for vs in variant_strings):
            unique_boards.append(board)
            for vs in variant_strings:
                seen.add(vs)
    
    return unique_boards

def get_all_variants(board):
    """Get all rotations and reflections of a board."""
    variants = []
    
    # Original board
    b = [row[:] for row in board]
    variants.append(b)
    
    # Rotate 90 degrees
    b = [[board[2-j][i] for j in range(3)] for i in range(3)]
    variants.append(b)
    
    # Rotate 180 degrees
    b = [[board[2-i][2-j] for j in range(3)] for i in range(3)]
    variants.append(b)
    
    # Rotate 270 degrees
    b = [[board[j][2-i] for j in range(3)] for i in range(3)]
    variants.append(b)
    
    # Reflect horizontally
    b = [[board[i][2-j] for j in range(3)] for i in range(3)]
    variants.append(b)
    
    # Reflect vertically
    b = [[board[2-i][j] for j in range(3)] for i in range(3)]
    variants.append(b)
    
    # Reflect along main diagonal
    b = [[board[j][i] for j in range(3)] for i in range(3)]
    variants.append(b)
    
    # Reflect along other diagonal
    b = [[board[2-j][2-i] for j in range(3)] for i in range(3)]
    variants.append(b)
    
    return variants

def find_transitions(boards):
    """Find all possible transitions between board states."""
    transitions = defaultdict(list)
    board_to_id = {board_to_string(board): i for i, board in enumerate(boards)}
    
    # Check each state
    for i, board in enumerate(boards):
        board_str = board_to_string(board)
        
        # If game is over, no transitions
        if has_won(board, 1) or has_won(board, 2) or board_str.count('0') == 0:
            continue
        
        # Determine whose turn it is
        flat_board = [cell for row in board for cell in row]
        x_count = flat_board.count(1)
        o_count = flat_board.count(2)
        current_player = 1 if x_count == o_count else 2
        
        # Try each empty cell
        for r in range(3):
            for c in range(3):
                if board[r][c] == 0:
                    new_board = [row[:] for row in board]
                    new_board[r][c] = current_player
                    
                    # Verify the new state is valid
                    if is_valid_board(new_board):
                        new_board_str = board_to_string(new_board)
                        if new_board_str in board_to_id:
                            new_id = board_to_id[new_board_str]
                            if new_id not in transitions[i]:
                                transitions[i].append(new_id)
    
    # Verify transitions
    total_transitions = sum(len(targets) for targets in transitions.values())
    print(f"Generated {total_transitions} transitions between states")
    
    return transitions

def generate_html(boards, transitions, filename, title):
    """Generate HTML visualization of board states and transitions."""
    # Add more information to HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            h1, h2 {{
                color: #333;
            }}
            .board-container {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                margin-bottom: 30px;
            }}
            .board-wrapper {{
                background-color: white;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                width: 180px;
            }}
            .board {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                grid-template-rows: repeat(3, 1fr);
                gap: 2px;
                width: 150px;
                height: 150px;
                margin: 0 auto;
                background-color: #333;
            }}
            .cell {{
                background-color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                font-weight: bold;
            }}
            .cell-0 {{ color: #aaa; }} /* Make empty cells more visible */
            .cell-1 {{ color: #e74c3c; }} /* X */
            .cell-2 {{ color: #3498db; }} /* O */
            .board-id {{
                text-align: center;
                margin-top: 10px;
                font-weight: bold;
            }}
            .transitions {{
                font-size: 12px;
                margin-top: 5px;
                text-align: center;
                color: #666;
                height: 40px;
                overflow-y: auto;
            }}
            .search-container {{
                margin-bottom: 20px;
            }}
            #boardSearch {{
                padding: 8px;
                width: 300px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }}
            .stats {{
                margin-bottom: 20px;
                padding: 15px;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .filters {{
                margin-bottom: 20px;
            }}
            .filter-btn {{
                margin-right: 10px;
                padding: 5px 10px;
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                border-radius: 4px;
                cursor: pointer;
            }}
            .filter-btn.active {{
                background-color: #3498db;
                color: white;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <div class="stats">
            <p>Total board states: <strong>{len(boards)}</strong></p>
            <p>Total transitions: <strong>{sum(len(t) for t in transitions.values())}</strong></p>
        </div>
        
        <div class="search-container">
            <input type="text" id="boardSearch" placeholder="Search board by ID...">
        </div>
        
        <div class="filters">
            <button class="filter-btn active" data-filter="all">All States</button>
            <button class="filter-btn" data-filter="x-turn">X's Turn</button>
            <button class="filter-btn" data-filter="o-turn">O's Turn</button>
            <button class="filter-btn" data-filter="x-win">X Wins</button>
            <button class="filter-btn" data-filter="o-win">O Wins</button>
            <button class="filter-btn" data-filter="draw">Draw</button>
        </div>
        
        <div class="board-container" id="boardContainer">
    """
    
    # Add each board to the HTML
    for i, board in enumerate(boards):
        # Convert board cells to X and O for display
        display_cells = []
        for row in board:
            for cell in row:
                if cell == 0:
                    display_cells.append(".")
                elif cell == 1:
                    display_cells.append("X")
                else:  # cell == 2
                    display_cells.append("O")
        
        # Get transitions for this board
        outgoing = transitions.get(i, [])
        transition_text = ", ".join(str(t) for t in outgoing) if outgoing else "None"
        
        # Determine game state
        flat_board = [cell for row in board for cell in row]
        x_count = flat_board.count(1)
        o_count = flat_board.count(2)
        x_won = has_won(board, 1)
        o_won = has_won(board, 2)
        is_draw = flat_board.count(0) == 0 and not x_won and not o_won
        
        # Determine whose turn it is
        current_player = "x-turn" if x_count == o_count else "o-turn"
        
        # Set filter class
        filter_class = current_player
        if x_won:
            filter_class = "x-win"
        elif o_won:
            filter_class = "o-win"
        elif is_draw:
            filter_class = "draw"
        
        html += f"""
            <div class="board-wrapper" data-id="{i}" data-filter="{filter_class}">
                <div class="board">
        """
        
        for j, cell_value in enumerate(display_cells):
            cell_class = f"cell cell-{board[j//3][j%3]}"
            html += f'<div class="{cell_class}">{cell_value}</div>'
        
        html += f"""
                </div>
                <div class="board-id">ID: {i}</div>
                <div class="transitions">Transitions to: {transition_text}</div>
            </div>
        """
    
    html += """
        </div>
        
        <script>
            // Search functionality
            document.getElementById('boardSearch').addEventListener('input', function() {
                const searchValue = this.value.trim();
                const boardWrappers = document.querySelectorAll('.board-wrapper');
                
                boardWrappers.forEach(wrapper => {
                    const boardId = wrapper.getAttribute('data-id');
                    if (searchValue === '' || boardId.includes(searchValue)) {
                        wrapper.style.display = 'block';
                    } else {
                        wrapper.style.display = 'none';
                    }
                });
            });
            
            // Filter functionality
            const filterButtons = document.querySelectorAll('.filter-btn');
            filterButtons.forEach(button => {
                button.addEventListener('click', function() {
                    // Update active button
                    filterButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');
                    
                    const filter = this.getAttribute('data-filter');
                    const boardWrappers = document.querySelectorAll('.board-wrapper');
                    
                    boardWrappers.forEach(wrapper => {
                        if (filter === 'all' || wrapper.getAttribute('data-filter') === filter) {
                            wrapper.style.display = 'block';
                        } else {
                            wrapper.style.display = 'none';
                        }
                    });
                });
            });
        </script>
    </body>
    </html>
    """
    
    with open(filename, 'w') as f:
        f.write(html)

def main():
    # Generate all valid states
    valid_boards = find_valid_boards()
    print(f"Total valid boards (with duplicates): {len(valid_boards)}")
    
    # Verify state count is correct
    if len(valid_boards) != 5478:
        print(f"Warning: Expected 5478 valid states, but found {len(valid_boards)}")
    
    # Calculate transitions for all valid states
    all_transitions = find_transitions(valid_boards)
    
    # Generate HTML with all valid states
    generate_html(valid_boards, all_transitions, 'tic_tac_toe_all_states.html', 'Tic-Tac-Toe All Valid States (5478)')
    
    # Remove duplicate states (considering rotations and reflections)
    unique_boards = remove_duplicates(valid_boards)
    print(f"Total unique boards (after removing duplicates): {len(unique_boards)}")
    
    # Verify unique state count is correct
    if len(unique_boards) != 765:
        print(f"Warning: Expected 765 unique states, but found {len(unique_boards)}")
    
    # Calculate transitions for unique states
    unique_transitions = find_unique_transitions(unique_boards)
    
    # Generate HTML with unique states
    generate_html(unique_boards, unique_transitions, 'tic_tac_toe_unique_states.html', 'Tic-Tac-Toe Unique Valid States (765)')

def find_unique_transitions(unique_boards):
    """Find transitions between unique board states."""
    unique_transitions = defaultdict(list)
    unique_board_to_id = {board_to_string(board): i for i, board in enumerate(unique_boards)}
    
    for i, board in enumerate(unique_boards):
        board_str = board_to_string(board)
        
        # If game is over, no transitions
        if has_won(board, 1) or has_won(board, 2) or board_str.count('0') == 0:
            continue
        
        # Determine whose turn it is
        flat_board = [cell for row in board for cell in row]
        x_count = flat_board.count(1)
        o_count = flat_board.count(2)
        current_player = 1 if x_count == o_count else 2
        
        # Try each empty cell
        for r in range(3):
            for c in range(3):
                if board[r][c] == 0:
                    new_board = [row[:] for row in board]
                    new_board[r][c] = current_player
                    
                    if is_valid_board(new_board):
                        # Find canonical form of the new board
                        canonical_found = False
                        for variant in get_all_variants(new_board):
                            variant_str = board_to_string(variant)
                            if variant_str in unique_board_to_id:
                                new_id = unique_board_to_id[variant_str]
                                if new_id not in unique_transitions[i]:
                                    unique_transitions[i].append(new_id)
                                canonical_found = True
                                break
                        
                        if not canonical_found:
                            print(f"Warning: Could not find canonical form for board after move")
    
    # Verify transitions
    total_transitions = sum(len(targets) for targets in unique_transitions.values())
    print(f"Generated {total_transitions} transitions between unique states")
    
    return unique_transitions

if __name__ == "__main__":
    main() 