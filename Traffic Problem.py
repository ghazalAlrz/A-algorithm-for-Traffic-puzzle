import heapq

class PuzzleState:
    def __init__(self, rows, cols, cars, parent=None, cost=0):
        """
        Initialize a state in the puzzle.

        Args:
        - rows (int): Number of rows in the puzzle grid.
        - cols (int): Number of columns in the puzzle grid.
        - cars (list): List of tuples representing cars with their positions and orientations.
        - parent (PuzzleState, optional): Parent state from which this state was reached.
        - cost (int, optional): Cost to reach this state from the initial state.
        """
        self.rows = rows
        self.cols = cols
        self.cars = tuple(cars)  # Convert cars list to tuple for immutability
        self.parent = parent
        self.cost = cost
        self.is_goal = self._check_goal_state()

    def _check_goal_state(self):
        """
        Check if the goal state (red car reaching the rightmost column) is reached.

        Returns:
        - bool: True if goal state is reached, False otherwise.
        """
        return self.cars[0][1] + self.cars[0][3] - 1 == self.cols

    def is_car_blocked(self, car, move_dir):
        """
        Check if a given car is blocked in a specific direction.

        Args:
        - car (tuple): Car information (row, col, orientation, length).
        - move_dir (str): Direction of movement ('left', 'right', 'up', 'down').

        Returns:
        - bool: True if car is blocked, False otherwise.
        """
        r, c, o, l = car

        if o == 'h':
            if move_dir == 'left':
                if c <= 1:
                    return True
                # Check if there's any other car blocking the left movement
                for other in self.cars:
                    if other != car:
                        if other[2] == 'h' and other[0] == r and other[1] + other[3] == c:
                            return True
                        elif other[2] == 'v' and other[0] <= r < other[0] + other[3] and other[1] == c - 1:
                            return True
                return False
            elif move_dir == 'right':
                if c + l > self.cols:
                    return True
                # Check if there's any other car blocking the right movement
                for other in self.cars:
                    if other != car:
                        if other[2] == 'h' and other[0] == r and c + l == other[1]:
                            return True
                        elif other[2] == 'v' and other[0] <= r < other[0] + other[3] and other[1] == c + l:
                            return True
                return False
        elif o == 'v':
            if move_dir == 'up':
                if r <= 1:
                    return True
                # Check if there's any other car blocking the upward movement
                for other in self.cars:
                    if other != car:
                        if other[2] == 'v' and other[1] == c and other[0] + other[3] == r:
                            return True
                        elif other[2] == 'h' and other[1] <= c < other[1] + other[3] and other[0] == r - 1:
                            return True
                return False
            elif move_dir == 'down':
                if r + l > self.rows:
                    return True
                # Check if there's any other car blocking the downward movement
                for other in self.cars:
                    if other != car:
                        if other[2] == 'v' and other[1] == c and r + l == other[0]:
                            return True
                        elif other[2] == 'h' and other[1] <= c < other[1] + other[3] and other[0] == r + l:
                            return True
                return False
        return False

    def get_next_states(self):
        """
        Generate possible next states from the current state by moving each car.

        Returns:
        - list: List of possible next states.
        """
        possible_states = []
        cars_list = list(self.cars)

        for index, car in enumerate(self.cars):
            r, c, o, l = car

            if o == 'h':
                if not self.is_car_blocked(car, 'left'):
                    cars_list[index] = (r, c - 1, o, l)
                    new_state = PuzzleState(self.rows, self.cols, cars_list, parent=self, cost=self.cost + 1)
                    possible_states.append(new_state)
                    cars_list[index] = car

                if not self.is_car_blocked(car, 'right'):
                    cars_list[index] = (r, c + 1, o, l)
                    new_state = PuzzleState(self.rows, self.cols, cars_list, parent=self, cost=self.cost + 1)
                    possible_states.append(new_state)
                    cars_list[index] = car

            elif o == 'v':
                if not self.is_car_blocked(car, 'up'):
                    cars_list[index] = (r - 1, c, o, l)
                    new_state = PuzzleState(self.rows, self.cols, cars_list, parent=self, cost=self.cost + 1)
                    possible_states.append(new_state)
                    cars_list[index] = car

                if not self.is_car_blocked(car, 'down'):
                    cars_list[index] = (r + 1, c, o, l)
                    new_state = PuzzleState(self.rows, self.cols, cars_list, parent=self, cost=self.cost + 1)
                    possible_states.append(new_state)
                    cars_list[index] = car

        return possible_states

    def heuristic(self):
        """
        Calculate the heuristic value for the current state.

        Returns:
        - int: Heuristic value.
        """
        red_car = self.cars[0]
        red_car_row, red_car_col, _, red_car_length = red_car

        distance_to_goal = self.cols - (red_car_col + red_car_length) + 1
        cars_in_front = sum(
            1 for car in self.cars[1:]
            if (
                (car[2] == 'h' and car[0] == red_car_row and car[1] > red_car_col + red_car_length - 1) or
                (car[2] == 'v' and car[1] > red_car_col and car[0] <= red_car_row < car[0] + car[3])
            )
        )

        return distance_to_goal + cars_in_front

    def __lt__(self, other):
        """
        Less than comparison method based on the cost and heuristic value.

        Args:
        - other (PuzzleState): Another state object to compare against.

        Returns:
        - bool: True if this state is less than the other, False otherwise.
        """
        return (self.cost + self.heuristic()) < (other.cost + other.heuristic())

def solve_puzzle(initial_cars, rows, cols):
    """
    Perform A* algorithm to find the shortest path solution to the puzzle.

    Args:
    - initial_cars (list): List of initial car positions.
    - rows (int): Number of rows in the puzzle grid.
    - cols (int): Number of columns in the puzzle grid.

    Returns:
    - PuzzleState or None: Final state if goal is reached, None if no solution found.
    """
    initial_state = PuzzleState(rows, cols, initial_cars)
    priority_queue = []
    heapq.heapify(priority_queue)
    state_map = {hash(initial_state.cars): initial_state}
    heapq.heappush(priority_queue, (initial_state.cost + initial_state.heuristic(), hash(initial_state.cars)))

    visited = set()
    while priority_queue:
        _, current_state_hash = heapq.heappop(priority_queue)
        current_state = state_map[current_state_hash]

        if current_state.is_goal:
            return current_state

        visited.add(current_state.cars)

        next_states = current_state.get_next_states()
        for state in next_states:
            state_hash_val = hash(state.cars)
            if state.cars not in visited and state_hash_val not in state_map:
                state_map[state_hash_val] = state
                heapq.heappush(priority_queue, (state.cost + state.heuristic(), state_hash_val))




if __name__ == '__main__':
    number_of_tests = int(input("Enter your input "))  # Fixed prompt message
    for _ in range(number_of_tests):
        line = input()  
        inputs = [int(i) for i in line.split()] 
        rows, cols, num_cars = inputs

        initial_cars = []
        for __ in range(num_cars):
            line = input()  
            parts = line.split()
            initial_cars.append((int(parts[0]), int(parts[1]), parts[2], int(parts[3])))

        result = solve_puzzle(initial_cars, rows, cols)

        current = result
        while current:
            print(*current.cars, sep="\n")
            print("---------------------")
            current = current.parent
        print("moves are printed above in reverse order")
        print("Number of moves:", result.cost)
        
