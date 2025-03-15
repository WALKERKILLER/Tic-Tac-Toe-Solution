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
- `tic_tac_toe_all_states.html`: HTML visualization of all 5,478 valid states
- `tic_tac_toe_unique_states.html`: HTML visualization of 765 unique states (after removing duplicates)

## How to Use

1. Run the Python script:
   ```
   python tic_tac_toe_states.py
   ```

2. Open the generated HTML files in a web browser to view the states:
   - `tic_tac_toe_all_states.html` - All valid states (5,478)
   - `tic_tac_toe_unique_states.html` - Unique states after removing duplicates (765)

3. In the HTML viewer:
   - Each board state is displayed with its unique ID
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

## Statistics

- Total valid board states: 5,478
- Unique board states (after removing rotations and reflections): 765 