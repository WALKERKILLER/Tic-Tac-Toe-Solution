# Tic-Tac-Toe States Generator

This project generates all valid states of a Tic-Tac-Toe game and visualizes them in HTML format.

## Overview

Tic-Tac-Toe is a simple game played on a 3x3 grid. Players take turns placing X's and O's on the grid, with the goal of getting three of their marks in a row (horizontally, vertically, or diagonally).

This program:
1. Generates all possible states of a Tic-Tac-Toe board
2. Filters out invalid states that couldn't occur in a real game
3. Creates visualizations showing all states and their transitions
4. Provides both a complete set and a deduplicated set (removing rotations and reflections)

## Files

- `tic_tac_toe_states.py`: The main Python script that generates the states and HTML files
- `tic_tac_toe_states.html`: HTML visualization with toggle between all states and unique states

## How to Use

1. Run the Python script:
   ```
   python tic_tac_toe_states.py
   ```

2. Open the generated HTML file in a web browser to view the states:
   - `tic_tac_toe_states.html` - Contains both all valid states (5,478) and unique states (765)

3. In the HTML viewer:
   - Use the "View Options" buttons to toggle between "All States" and "Unique States"
   - Each board state is displayed with its unique ID (starting from 1)
   - The "Transitions to:" section shows which other states can be reached from the current state
   - Use the search box to find specific board states by ID

## Board Representation

In the code:
- `0` represents an empty cell
- `1` represents X
- `2` represents O

In the HTML visualization:
- Empty cells are shown as dots (.)
- X's are shown in red
- O's are shown in blue

## New Features

### Interactive Transition Visualization

The updated visualization includes interactive features to better understand state transitions:

- **Toggle Between Views**:
  - Switch between viewing all 5,478 states and the 765 unique states with a single click

- **Transition Visualization Modes**:
  - **Click Mode**: Click on a board to see its transitions, click again to hide
  - **Hover Mode**: Hover over a board to see its transitions, move away to hide

- **Visual Transition Indicators**:
  - Source board highlighted with blue border
  - Target boards highlighted with red border
  - Animated transition lines with arrows showing direction of transitions
  - Smooth animations for better visual tracking

- **Transition Information Panel**:
  - Fixed position panel showing details about the selected transition
  - Displays the number of possible transitions and their target IDs
  - Updates dynamically as you interact with different board states

### Filtering Options

- Filter states by game condition:
  - X's turn
  - O's turn
  - X wins
  - O wins
  - Draw
- Search for specific board IDs

## State Transitions

A transition from state A to state B means that state B can be reached by making a valid move from state A. The transitions follow these rules:

1. Players alternate turns (X goes first)
2. A move can only be made in an empty cell
3. Once a player wins, no further moves are allowed

## Implementation Details

The program uses several key algorithms:

1. **Validity checking**: Ensures that a board state could legally occur in a game
2. **Duplicate detection**: Identifies and removes equivalent states (rotations and reflections)
3. **Transition mapping**: Determines all possible next states from each valid state
4. **Interactive visualization**: Uses JavaScript and CSS to create dynamic transition displays

## Statistics

- Total valid board states: 5,478
- Unique board states (after removing rotations and reflections): 765

You can visit this solution on [text](https://m3fivux8yn.yourware.so)
