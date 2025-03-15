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
    # Adjust board_to_id to use 1-based indexing
    board_to_id = {board_to_string(board): i+1 for i, board in enumerate(boards)}
    
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
                            if new_id not in transitions[i+1]:  # Use 1-based index for transitions
                                transitions[i+1].append(new_id)
    
    # Verify transitions
    total_transitions = sum(len(targets) for targets in transitions.values())
    print(f"Generated {total_transitions} transitions between states")
    
    return transitions

def generate_html(all_boards, all_transitions, unique_boards, unique_transitions, filename, title):
    """Generate HTML visualization of board states and transitions with toggle between all and unique states."""
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
                position: relative; /* For transition lines */
            }}
            .board-wrapper {{
                background-color: white;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                width: 180px;
                position: relative; /* For transition lines */
                transition: transform 0.3s, box-shadow 0.3s;
                z-index: 1;
            }}
            .board-wrapper:hover {{
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                z-index: 10;
            }}
            .board-wrapper.highlight {{
                border: 3px solid #3498db;
                box-shadow: 0 0 15px rgba(52, 152, 219, 0.7);
            }}
            .board-wrapper.transition-target {{
                border: 3px solid #e74c3c;
                box-shadow: 0 0 15px rgba(231, 76, 60, 0.7);
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
            .filter-btn, .view-btn, .transition-btn {{
                margin-right: 10px;
                padding: 5px 10px;
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                border-radius: 4px;
                cursor: pointer;
            }}
            .filter-btn.active, .view-btn.active, .transition-btn.active {{
                background-color: #3498db;
                color: white;
            }}
            .view-controls, .transition-controls {{
                margin-bottom: 20px;
                padding: 15px;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .board-view {{
                display: none;
            }}
            .board-view.active {{
                display: block;
            }}
            .transition-line {{
                position: absolute;
                pointer-events: none;
                z-index: 0;
                opacity: 0;
                transition: opacity 0.3s;
            }}
            .transition-line.visible {{
                opacity: 1;
            }}
            .transition-arrow {{
                position: absolute;
                width: 0;
                height: 0;
                border-left: 8px solid transparent;
                border-right: 8px solid transparent;
                border-bottom: 12px solid #e74c3c;
                transform-origin: center bottom;
                pointer-events: none;
                z-index: 0;
                opacity: 0;
                transition: opacity 0.3s;
            }}
            .transition-arrow.visible {{
                opacity: 1;
            }}
            .transition-info {{
                position: fixed;
                bottom: 20px;
                right: 20px;
                background-color: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                z-index: 100;
                display: none;
            }}
            .transition-info.visible {{
                display: block;
            }}
            .transition-mode-info {{
                margin-top: 10px;
                font-style: italic;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        
        <div class="view-controls">
            <h2>View Options</h2>
            <button class="view-btn active" data-view="all">All States ({len(all_boards)})</button>
            <button class="view-btn" data-view="unique">Unique States ({len(unique_boards)})</button>
        </div>
        
        <div class="transition-controls">
            <h2>Transition Visualization</h2>
            <button class="transition-btn active" data-mode="click">Click Mode (Click on a board to see transitions)</button>
            <button class="transition-btn" data-mode="hover">Hover Mode (Hover over a board to see transitions)</button>
            <div class="transition-mode-info">
                In Click Mode: Click on a board to see its transitions. Click again to hide.
                <br>In Hover Mode: Hover over a board to see its transitions. Move away to hide.
            </div>
        </div>
        
        <div id="all-boards-view" class="board-view active">
            <div class="stats">
                <p>Total board states: <strong>{len(all_boards)}</strong></p>
                <p>Total transitions: <strong>{sum(len(t) for t in all_transitions.values())}</strong></p>
            </div>
            
            <div class="search-container">
                <input type="text" id="allBoardSearch" placeholder="Search board by ID...">
            </div>
            
            <div class="filters">
                <button class="filter-btn active" data-filter="all" data-view="all">All States</button>
                <button class="filter-btn" data-filter="x-turn" data-view="all">X's Turn</button>
                <button class="filter-btn" data-filter="o-turn" data-view="all">O's Turn</button>
                <button class="filter-btn" data-filter="x-win" data-view="all">X Wins</button>
                <button class="filter-btn" data-filter="o-win" data-view="all">O Wins</button>
                <button class="filter-btn" data-filter="draw" data-view="all">Draw</button>
            </div>
            
            <div class="board-container" id="allBoardContainer">
    """
    
    # Add each board to the HTML (all boards)
    for i, board in enumerate(all_boards):
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
        
        # Get transitions for this board - use 1-based indexing
        board_id = i + 1
        outgoing = all_transitions.get(board_id, [])
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
        
        # Store transitions as data attribute for JavaScript
        transitions_attr = " ".join(str(t) for t in outgoing) if outgoing else ""
        
        html += f"""
            <div class="board-wrapper" data-id="{board_id}" data-filter="{filter_class}" data-transitions="{transitions_attr}">
                <div class="board">
        """
        
        for j, cell_value in enumerate(display_cells):
            cell_class = f"cell cell-{board[j//3][j%3]}"
            html += f'<div class="{cell_class}">{cell_value}</div>'
        
        html += f"""
                </div>
                <div class="board-id">ID: {board_id}</div>
                <div class="transitions">Transitions to: {transition_text}</div>
            </div>
        """
    
    html += """
            </div>
        </div>
        
        <div id="unique-boards-view" class="board-view">
            <div class="stats">
                <p>Total unique board states: <strong>{0}</strong></p>
                <p>Total transitions: <strong>{1}</strong></p>
            </div>
            
            <div class="search-container">
                <input type="text" id="uniqueBoardSearch" placeholder="Search board by ID...">
            </div>
            
            <div class="filters">
                <button class="filter-btn active" data-filter="all" data-view="unique">All States</button>
                <button class="filter-btn" data-filter="x-turn" data-view="unique">X's Turn</button>
                <button class="filter-btn" data-filter="o-turn" data-view="unique">O's Turn</button>
                <button class="filter-btn" data-filter="x-win" data-view="unique">X Wins</button>
                <button class="filter-btn" data-filter="o-win" data-view="unique">O Wins</button>
                <button class="filter-btn" data-filter="draw" data-view="unique">Draw</button>
            </div>
            
            <div class="board-container" id="uniqueBoardContainer">
    """.format(len(unique_boards), sum(len(t) for t in unique_transitions.values()))
    
    # Add each board to the HTML (unique boards)
    for i, board in enumerate(unique_boards):
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
        
        # Get transitions for this board - use 1-based indexing
        board_id = i + 1
        outgoing = unique_transitions.get(board_id, [])
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
        
        # Store transitions as data attribute for JavaScript
        transitions_attr = " ".join(str(t) for t in outgoing) if outgoing else ""
        
        html += f"""
            <div class="board-wrapper" data-id="{board_id}" data-filter="{filter_class}" data-transitions="{transitions_attr}">
                <div class="board">
        """
        
        for j, cell_value in enumerate(display_cells):
            cell_class = f"cell cell-{board[j//3][j%3]}"
            html += f'<div class="{cell_class}">{cell_value}</div>'
        
        html += f"""
                </div>
                <div class="board-id">ID: {board_id}</div>
                <div class="transitions">Transitions to: {transition_text}</div>
            </div>
        """
    
    html += """
            </div>
        </div>
        
        <div class="transition-info">
            <h3>Transition Details</h3>
            <p id="transitionDetails"></p>
        </div>
        
        <script>
            // View toggle functionality
            const viewButtons = document.querySelectorAll('.view-btn');
            const boardViews = document.querySelectorAll('.board-view');
            
            viewButtons.forEach(button => {
                button.addEventListener('click', function() {
                    // Clear any active transitions
                    clearAllTransitions();
                    
                    // Update active button
                    viewButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Show the selected view
                    const viewType = this.getAttribute('data-view');
                    boardViews.forEach(view => {
                        if (view.id === viewType + '-boards-view') {
                            view.classList.add('active');
                        } else {
                            view.classList.remove('active');
                        }
                    });
                });
            });
            
            // Search functionality for all boards
            document.getElementById('allBoardSearch').addEventListener('input', function() {
                const searchValue = this.value.trim();
                const boardWrappers = document.querySelectorAll('#allBoardContainer .board-wrapper');
                
                boardWrappers.forEach(wrapper => {
                    const boardId = wrapper.getAttribute('data-id');
                    if (searchValue === '' || boardId.includes(searchValue)) {
                        wrapper.style.display = 'block';
                    } else {
                        wrapper.style.display = 'none';
                    }
                });
                
                // Clear any active transitions when searching
                clearAllTransitions();
            });
            
            // Search functionality for unique boards
            document.getElementById('uniqueBoardSearch').addEventListener('input', function() {
                const searchValue = this.value.trim();
                const boardWrappers = document.querySelectorAll('#uniqueBoardContainer .board-wrapper');
                
                boardWrappers.forEach(wrapper => {
                    const boardId = wrapper.getAttribute('data-id');
                    if (searchValue === '' || boardId.includes(searchValue)) {
                        wrapper.style.display = 'block';
                    } else {
                        wrapper.style.display = 'none';
                    }
                });
                
                // Clear any active transitions when searching
                clearAllTransitions();
            });
            
            // Filter functionality
            const filterButtons = document.querySelectorAll('.filter-btn');
            filterButtons.forEach(button => {
                button.addEventListener('click', function() {
                    // Clear any active transitions
                    clearAllTransitions();
                    
                    // Update active button within the same view
                    const viewType = this.getAttribute('data-view');
                    document.querySelectorAll(`.filter-btn[data-view="${viewType}"]`).forEach(btn => {
                        btn.classList.remove('active');
                    });
                    this.classList.add('active');
                    
                    const filter = this.getAttribute('data-filter');
                    const containerId = viewType === 'all' ? 'allBoardContainer' : 'uniqueBoardContainer';
                    const boardWrappers = document.querySelectorAll(`#${containerId} .board-wrapper`);
                    
                    boardWrappers.forEach(wrapper => {
                        if (filter === 'all' || wrapper.getAttribute('data-filter') === filter) {
                            wrapper.style.display = 'block';
                        } else {
                            wrapper.style.display = 'none';
                        }
                    });
                });
            });
            
            // Transition mode toggle
            const transitionButtons = document.querySelectorAll('.transition-btn');
            let transitionMode = 'click'; // Default mode
            
            transitionButtons.forEach(button => {
                button.addEventListener('click', function() {
                    // Clear any active transitions
                    clearAllTransitions();
                    
                    // Update active button
                    transitionButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Set the transition mode
                    transitionMode = this.getAttribute('data-mode');
                    
                    // Update event listeners based on mode
                    setupTransitionEventListeners();
                });
            });
            
            // Function to setup transition event listeners based on current mode
            function setupTransitionEventListeners() {
                // Remove existing event listeners
                const boardWrappers = document.querySelectorAll('.board-wrapper');
                boardWrappers.forEach(wrapper => {
                    wrapper.removeEventListener('click', handleBoardClick);
                    wrapper.removeEventListener('mouseenter', handleBoardHover);
                    wrapper.removeEventListener('mouseleave', handleBoardLeave);
                });
                
                // Add new event listeners based on mode
                if (transitionMode === 'click') {
                    boardWrappers.forEach(wrapper => {
                        wrapper.addEventListener('click', handleBoardClick);
                    });
                } else if (transitionMode === 'hover') {
                    boardWrappers.forEach(wrapper => {
                        wrapper.addEventListener('mouseenter', handleBoardHover);
                        wrapper.addEventListener('mouseleave', handleBoardLeave);
                    });
                }
            }
            
            // Variables to track active board and transitions
            let activeBoard = null;
            let transitionLines = [];
            let transitionArrows = [];
            
            // Handle board click for click mode
            function handleBoardClick(event) {
                const clickedBoard = this;
                const boardId = clickedBoard.getAttribute('data-id');
                
                // If this board is already active, clear transitions
                if (clickedBoard === activeBoard) {
                    clearAllTransitions();
                    return;
                }
                
                // Clear any existing transitions
                clearAllTransitions();
                
                // Set this board as active
                activeBoard = clickedBoard;
                clickedBoard.classList.add('highlight');
                
                // Show transitions
                showTransitions(clickedBoard);
            }
            
            // Handle board hover for hover mode
            function handleBoardHover(event) {
                const hoveredBoard = this;
                
                // Clear any existing transitions
                clearAllTransitions();
                
                // Set this board as active
                activeBoard = hoveredBoard;
                hoveredBoard.classList.add('highlight');
                
                // Show transitions
                showTransitions(hoveredBoard);
            }
            
            // Handle board leave for hover mode
            function handleBoardLeave(event) {
                clearAllTransitions();
            }
            
            // Function to show transitions from a board
            function showTransitions(boardElement) {
                const boardId = boardElement.getAttribute('data-id');
                const transitionsStr = boardElement.getAttribute('data-transitions');
                
                if (!transitionsStr) {
                    // No transitions
                    document.querySelector('.transition-info').classList.add('visible');
                    document.getElementById('transitionDetails').textContent = `Board ${boardId} has no possible transitions.`;
                    return;
                }
                
                const transitions = transitionsStr.split(' ').map(Number);
                const container = boardElement.parentElement;
                const sourceRect = boardElement.getBoundingClientRect();
                const containerRect = container.getBoundingClientRect();
                
                // Show transition info
                document.querySelector('.transition-info').classList.add('visible');
                document.getElementById('transitionDetails').textContent = 
                    `Board ${boardId} transitions to ${transitions.length} state(s): ${transitions.join(', ')}`;
                
                // Find and highlight target boards
                transitions.forEach(targetId => {
                    const targetBoard = container.querySelector(`.board-wrapper[data-id="${targetId}"]`);
                    if (targetBoard) {
                        targetBoard.classList.add('transition-target');
                        
                        // Create transition line
                        drawTransitionLine(boardElement, targetBoard, container);
                    }
                });
            }
            
            // Function to draw a transition line between two boards
            function drawTransitionLine(sourceBoard, targetBoard, container) {
                const sourceRect = sourceBoard.getBoundingClientRect();
                const targetRect = targetBoard.getBoundingClientRect();
                const containerRect = container.getBoundingClientRect();
                
                // Calculate center points
                const sourceX = sourceRect.left + sourceRect.width / 2 - containerRect.left;
                const sourceY = sourceRect.top + sourceRect.height / 2 - containerRect.top;
                const targetX = targetRect.left + targetRect.width / 2 - containerRect.left;
                const targetY = targetRect.top + targetRect.height / 2 - containerRect.top;
                
                // Calculate distance and angle
                const dx = targetX - sourceX;
                const dy = targetY - sourceY;
                const distance = Math.sqrt(dx * dx + dy * dy);
                const angle = Math.atan2(dy, dx) * 180 / Math.PI;
                
                // Create line element
                const line = document.createElement('div');
                line.className = 'transition-line';
                line.style.width = `${distance}px`;
                line.style.height = '3px';
                line.style.backgroundColor = '#e74c3c';
                line.style.position = 'absolute';
                line.style.left = `${sourceX}px`;
                line.style.top = `${sourceY}px`;
                line.style.transformOrigin = '0 50%';
                line.style.transform = `rotate(${angle}deg)`;
                line.style.zIndex = '0';
                
                // Create arrow element
                const arrow = document.createElement('div');
                arrow.className = 'transition-arrow';
                arrow.style.left = `${targetX}px`;
                arrow.style.top = `${targetY - 10}px`;
                arrow.style.transform = `translateX(-50%) rotate(${angle}deg)`;
                
                // Add to container
                container.appendChild(line);
                container.appendChild(arrow);
                
                // Store for later cleanup
                transitionLines.push(line);
                transitionArrows.push(arrow);
                
                // Trigger reflow and add visible class for animation
                void line.offsetWidth;
                void arrow.offsetWidth;
                line.classList.add('visible');
                arrow.classList.add('visible');
            }
            
            // Function to clear all transitions
            function clearAllTransitions() {
                // Remove highlight from active board
                if (activeBoard) {
                    activeBoard.classList.remove('highlight');
                    activeBoard = null;
                }
                
                // Remove target highlights
                document.querySelectorAll('.transition-target').forEach(board => {
                    board.classList.remove('transition-target');
                });
                
                // Remove transition lines and arrows
                transitionLines.forEach(line => line.remove());
                transitionArrows.forEach(arrow => arrow.remove());
                transitionLines = [];
                transitionArrows = [];
                
                // Hide transition info
                document.querySelector('.transition-info').classList.remove('visible');
            }
            
            // Initialize transition event listeners
            setupTransitionEventListeners();
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
    
    # Remove duplicate states (considering rotations and reflections)
    unique_boards = remove_duplicates(valid_boards)
    print(f"Total unique boards (after removing duplicates): {len(unique_boards)}")
    
    # Verify unique state count is correct
    if len(unique_boards) != 765:
        print(f"Warning: Expected 765 unique states, but found {len(unique_boards)}")
    
    # Calculate transitions for unique states
    unique_transitions = find_unique_transitions(unique_boards)
    
    # Generate HTML with both all states and unique states
    generate_html(valid_boards, all_transitions, unique_boards, unique_transitions, 
                 'tic_tac_toe_states.html', 'Tic-Tac-Toe States Visualization')

def find_unique_transitions(unique_boards):
    """Find transitions between unique board states."""
    unique_transitions = defaultdict(list)
    # Adjust unique_board_to_id to use 1-based indexing
    unique_board_to_id = {board_to_string(board): i+1 for i, board in enumerate(unique_boards)}
    
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
                                if new_id not in unique_transitions[i+1]:  # Use 1-based index for transitions
                                    unique_transitions[i+1].append(new_id)
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