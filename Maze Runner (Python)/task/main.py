import random

# Constants
WALL = 'w'
CELL = 'c'
UNVISITED = 'u'


# Function to print the maze
def print_maze(maze):
    for row in maze:
        for cell in row:
            if cell in (UNVISITED, CELL):
                print("  ", end="")
            else:
                print('\u2588\u2588', end='')
        print()


# Function to find the number of surrounding cells
def surrounding_cells(maze, rand_wall):
    s_cells = 0
    if maze[rand_wall[0] - 1][rand_wall[1]] == CELL:
        s_cells += 1
    if maze[rand_wall[0] + 1][rand_wall[1]] == CELL:
        s_cells += 1
    if maze[rand_wall[0]][rand_wall[1] - 1] == CELL:
        s_cells += 1
    if maze[rand_wall[0]][rand_wall[1] + 1] == CELL:
        s_cells += 1
    return s_cells


# Function to initialize the maze with unvisited cells
def initialize_maze(height, width):
    return [[UNVISITED for _ in range(width)] for _ in range(height)]


# Function to randomize the starting point
def randomize_starting_point(height, width):
    starting_height = random.randint(1, height - 2)
    starting_width = random.randint(1, width - 2)
    return starting_height, starting_width


# Function to add surrounding walls to the list
def add_surrounding_walls(maze, walls, height, width):
    walls.append([height - 1, width])
    walls.append([height, width - 1])
    walls.append([height, width + 1])
    walls.append([height + 1, width])
    maze[height - 1][width] = WALL
    maze[height][width - 1] = WALL
    maze[height][width + 1] = WALL
    maze[height + 1][width] = WALL


# Function to process the walls and create the maze
def process_walls(maze, walls, height, width):
    while walls:
        rand_wall = walls.pop(random.randint(0, len(walls) - 1))
        if valid_wall_to_path(maze, rand_wall, height, width):
            convert_wall_to_path(maze, walls, rand_wall)
    mark_unvisited_cells_as_walls(maze)


# Function to check if a wall can be converted to a path
def valid_wall_to_path(maze, rand_wall, height, width):
    if (rand_wall[1] != 0 and maze[rand_wall[0]][rand_wall[1] - 1] == UNVISITED and maze[rand_wall[0]][rand_wall[1] + 1]
            == CELL):
        return surrounding_cells(maze, rand_wall) < 2
    if (rand_wall[0] != 0 and maze[rand_wall[0] - 1][rand_wall[1]] == UNVISITED and maze[rand_wall[0] + 1][rand_wall[1]]
            == CELL):
        return surrounding_cells(maze, rand_wall) < 2
    if (rand_wall[0] != height - 1 and maze[rand_wall[0] + 1][rand_wall[1]] == UNVISITED and maze[rand_wall[0] - 1]
    [rand_wall[1]] == CELL):
        return surrounding_cells(maze, rand_wall) < 2
    if (rand_wall[1] != width - 1 and maze[rand_wall[0]][rand_wall[1] + 1] == UNVISITED and
            maze[rand_wall[0]][rand_wall[1] - 1] == CELL):
        return surrounding_cells(maze, rand_wall) < 2
    return False


# Function to convert a wall to a path
def convert_wall_to_path(maze, walls, rand_wall):
    maze[rand_wall[0]][rand_wall[1]] = CELL
    add_new_walls(maze, walls, rand_wall)


# Function to add new walls around the converted path
def add_new_walls(maze, walls, rand_wall):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for direction in directions:
        new_wall = [rand_wall[0] + direction[0], rand_wall[1] + direction[1]]
        if maze[new_wall[0]][new_wall[1]] != CELL:
            maze[new_wall[0]][new_wall[1]] = WALL
        if new_wall not in walls:
            walls.append(new_wall)


# Function to mark all unvisited cells as walls
def mark_unvisited_cells_as_walls(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == UNVISITED:
                maze[i][j] = WALL


# Function to set the entrance and exit of the maze
def set_entrance_and_exit(maze, width, height):
    for i in range(width):
        if maze[1][i] == CELL:
            maze[0][i] = CELL
            break
    for i in range(width - 1, 0, -1):
        if maze[height - 2][i] == CELL:
            maze[height - 1][i] = CELL
            break


# Main function to create the maze
def create_maze():
    try:
        print("Please, enter the size of the new maze:")
        height = int(input())
        width = height
        if height < 3 or width < 3:
            print("Maze size must be at least 3x3")
            return
    except ValueError:
        print("Invalid input. Please enter one integer.")
        return

    maze = initialize_maze(height, width)
    starting_height, starting_width = randomize_starting_point(height, width)
    maze[starting_height][starting_width] = CELL
    walls = []
    add_surrounding_walls(maze, walls, starting_height, starting_width)
    process_walls(maze, walls, height, width)
    set_entrance_and_exit(maze, width, height)
    return maze


def save_maze(maze, filename):
    try:
        with open(filename, 'w') as file:
            for row in maze:
                file.write(''.join(row) + '\n')
        print("Maze saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving the maze: {e}")


def load_maze(filename, saved):
    try:
        with open(filename, 'r') as file:
            maze = [list(line.strip()) for line in file.readlines()]
        print("Maze loaded successfully.")
        saved = True
        return maze
    except FileNotFoundError:
        print(f"The file {filename} does not exist")
        return None
    except Exception as e:
        print(f"Cannot load the maze. It has an invalid format. {e}")
        return None


def menu(saved):
    while True:
        try:
            if not saved:
                choice = int(input("=== Menu ==="
                                   "\n1. Generate a new maze."
                                   "\n2. Load a maze."
                                   "\n0. Exit."
                                   "\nPlease enter your choice: "))
                if choice not in range(0, 3):
                    print("Incorrect option. Please enter a number between 0 and 2.")
                else:
                    return choice
            else:
                choice = int(input("=== Menu ==="
                                   "\n1. Generate a new maze."
                                   "\n2. Load a maze."
                                   "\n3. Save the maze."
                                   "\n4. Display the maze."
                                   "\n0. Exit."
                                   "\nPlease enter your choice: "))
                if choice not in range(0, 5):
                    print("Incorrect option. Please enter a number between 0 and 4.")
                else:
                    return choice
        except ValueError:
            print("Incorrect option. Please enter a number between 1 and 5.")

saved = False
while True:
    # Display the menu
    choice = menu(saved)
    # Exit
    if choice == 0:
        exit()
    # Create and then print the maze
    elif choice == 1:
        maze = create_maze()
        print_maze(maze)
        saved = True
    # Load a maze from a specified file
    elif choice == 2:
        filename = input()
        maze = load_maze(filename, saved)
    # Save the maze to a file
    elif choice == 3:
        filename = input()
        save_maze(maze, filename)
    # Display the loaded maze
    elif choice == 4:
        print_maze(maze)
