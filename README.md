# A-algorithm-for-Traffic-puzzle

## Overview

The Traffic Puzzle Problem involves maneuvering cars on a grid to achieve a specific goal: moving the red car to the rightmost column. This is achieved by managing car positions and checking for blockages while implementing a search algorithm to find the optimal solution.

## Features

- **State Representation**: Each state in the puzzle is represented by the `PuzzleState` class, which captures the grid dimensions, car positions, and movement costs.
- **Goal Checking**: The implementation includes a method to verify if the red car has reached the goal.
- **Car Movement**: Functions to check if a car can move in a specified direction without being blocked.

## Installation

To use this implementation, copy the class code into your Python environment or integrate it into your project.

## Usage

### Initialization

To create a new puzzle state, initialize the `PuzzleState` with the dimensions of the grid, car positions, and other optional parameters.

```python
# Example of initializing a PuzzleState
rows = 6  # Number of rows in the grid
cols = 6  # Number of columns in the grid
cars = [
    (0, 0, 'horizontal', 2),  # (row, col, orientation, length)
    (1, 0, 'vertical', 2),
    (2, 1, 'horizontal', 2),
    (3, 2, 'horizontal', 2),  # Red car
    # Add more cars as needed
]

# Create a new puzzle state
initial_state = PuzzleState(rows, cols, cars)
