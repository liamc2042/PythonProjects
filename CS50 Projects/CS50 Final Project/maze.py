import pygame
import math
from queue import PriorityQueue, Queue
import random 

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255 , 0)
CYAN = (0, 255, 255)
GREY = (128, 128, 128)

WINDOW_LENGTH = 800

WINDOW = pygame.display.set_mode((WINDOW_LENGTH, WINDOW_LENGTH))
pygame.display.set_caption("Maze Solver")

class Square():
    def __init__(self, row, column, length, total_rows):
        self.row = row
        self.column = column
        self.x = row * length
        self.y = column * length
        self.colour = WHITE
        self.neighbours = []
        self.length = length
        self.total_rows = total_rows

    def get_position(self):
        return (self.row, self.column)
    
    def is_visited(self):
        return self.colour == BLUE
    
    def is_available(self):
        return self.colour == CYAN
    
    def is_wall(self):
        return self.colour == BLACK
    
    def is_beginning(self):
        return self.colour == GREEN
    
    def is_finish(self):
        return self.colour == RED
    
    def is_free(self):
        return self.colour == WHITE
    
    def make_free(self):
        self.colour = WHITE

    def make_visited(self):
        self.colour = BLUE
    
    def make_available(self):
        self.colour = CYAN

    def make_wall(self):
        self.colour = BLACK

    def make_finish(self):
        self.colour = RED

    def make_beginning(self):
        self.colour = GREEN
    
    def make_route(self):
        self.colour = YELLOW

    def draw_rect(self, window):
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.length, self.length))

    def update_surrounding(self, maze):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not maze[self.row + 1][self.column].is_wall(): # Down direction
            self.neighbours.append(maze[self.row + 1][self.column])

        if self.column < self.total_rows - 1 and not maze[self.row][self.column + 1].is_wall(): # right direction
            self.neighbours.append(maze[self.row][self.column + 1])

        if self.row > 0 and not maze[self.row - 1][self.column].is_wall(): # Up direction
            self.neighbours.append(maze[self.row - 1][self.column])

        if self.column > 0 and not maze[self.row][self.column - 1].is_wall(): # Left direction
            self.neighbours.append(maze[self.row][self.column - 1])

    def __lt__(self, other):
        return False
    
def a_star_h(point_1, point_2):
    x_1, y_1 = point_1
    x_2, y_2 = point_2
    return abs(x_2 - x_1) + abs(y_2 - y_1)

def make_maze(rows, length):
    maze = []
    space = length // rows
    for i in range(rows):
        maze.append([])
        for j in range(rows):
            square = Square(i, j, space, rows)
            maze[i].append(square)
    return maze

def draw_grid(window, rows, length):
    space = length // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * space), (length, i * space))
        for j in range(rows):
            pygame.draw.line(window, GREY, (j * space, 0), (j * space, length))

def draw_maze(window, maze, rows, length):
    window.fill(WHITE)

    for row in maze:
        for square in row:
            square.draw_rect(window)

    draw_grid(window, rows, length)
    pygame.display.update()

def get_clicked_square(position, rows, length):
    space = length // rows
    y, x = position

    row = y // space
    column = x // space

    return row, column

def update_neighbours(maze):
    for row in maze:
        for square in row:
            square.update_surrounding(maze)

def create_path(prev, curr, draw_maze):
    while curr in prev:
        curr = prev[curr]
        curr.make_route()
        draw_maze()

def reset_search(draw_maze, maze, beginning, finish):
    for row in maze:
        for square in row:
            if not square.is_beginning() and not square.is_finish() and not square.is_wall():
                square.make_free()
    draw_maze()

def a_star_algorithm(draw_maze, maze, beginning, finish):
    count = 0
    available_set = PriorityQueue()
    available_set.put((0, count, beginning))
    prev = {}
    g_score = {square: float("inf") for row in maze for square in row}
    g_score[beginning] = 0
    h_score = {square: float("inf") for row in maze for square in row}
    h_score[beginning] = a_star_h(beginning.get_position(), finish.get_position())

    available_set_hash = {beginning}

    while not available_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = available_set.get()[2]
        available_set_hash.remove(curr)

        if curr == finish:
            create_path(prev, finish, draw_maze)
            finish.make_finish()
            beginning.make_beginning()
            return True
        
        for neighbour in curr.neighbours:
            temp_g_score = g_score[curr] + 1

            if temp_g_score < g_score[neighbour]:
                prev[neighbour] = curr
                g_score[neighbour] = temp_g_score
                h_score[neighbour] = temp_g_score + a_star_h(neighbour.get_position(), finish.get_position())
                if neighbour not in available_set_hash:
                    count += 1
                    available_set.put((h_score[neighbour], count, neighbour))
                    available_set_hash.add(neighbour)
                    neighbour.make_available()
        
        draw_maze()
        
        if curr != beginning:
            curr.make_visited()

    return False


def breadth_first_search(draw_maze, maze, beginning, finish):
    available_set = Queue()
    available_set.put(beginning)
    prev = {}
    available_set_hash = {beginning}

    while not available_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = available_set.get()

        if curr == finish:
            create_path(prev, finish, draw_maze)
            finish.make_finish()
            beginning.make_beginning()
            return True
        
        for neighbour in curr.neighbours:
            if neighbour not in available_set_hash:
                prev[neighbour] = curr
                available_set.put(neighbour)
                available_set_hash.add(neighbour)
                neighbour.make_available()
        
        draw_maze()

        if curr != beginning:
            curr.make_visited()

    return False


def depth_first_search(draw_maze, maze, beginning, finish):
    available_set = [beginning]
    available_set_hash = {beginning}
    prev = {}

    while available_set:

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        curr = available_set.pop()

        if curr == finish:
            create_path(prev, finish, draw_maze)
            finish.make_finish()
            beginning.make_beginning()
            return True
        
        neighbours = [neighbour for neighbour in curr.neighbours]
        random.shuffle(neighbours)

        for neighbour in neighbours:
            if neighbour not in available_set_hash:
                prev[neighbour] = curr
                available_set.append(neighbour)
                available_set_hash.add(neighbour)
                neighbour.make_available()
        
        draw_maze()

        if curr != beginning:
            curr.make_visited()

    return False

def generate_maze_random(draw_maze, maze):
    for rows in maze:
        for square in rows:
            coin = random.randint(0,3)
            if coin > 0:
                square.make_free()
            else:
                square.make_wall()
            draw_maze()

def generate_maze_DFS(draw_maze, maze, rows):
    start = maze[random.randint(0, rows)][random.randint(0,rows)]
    #start = maze[0][0]
    available_set = [start]
    available_set_hash = {start}
    prev = {}

    while available_set:

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        curr = available_set.pop()

        neighbours = [neighbour for neighbour in curr.neighbours]
        random.shuffle(neighbours)

        for neighbour in neighbours:
            if neighbour.is_free() and prev[curr] != neighbour:
                curr.make_wall()
                break

            else:
                curr.make_free()

        if curr.is_free():
            for neighbour in neighbours:
                if neighbour not in available_set_hash:
                    prev[neighbour] = curr
                    available_set.append(neighbour)
                    available_set_hash.add(neighbour)

        draw_maze()
    
    return True


def main(window, length):
    ROWS = 50 # Change to whatever user wants
    maze = make_maze(ROWS, length)
    
    beginning = None
    finish = None

    running = True
    while running:
        draw_maze(window, maze, ROWS, length)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]: # Left mouse
                position = pygame.mouse.get_pos()
                row, column = get_clicked_square(position, ROWS, length)
                square = maze[row][column]
                if not beginning and square != finish:
                    beginning = square
                    beginning.make_beginning()

                elif not finish and square != beginning:
                    finish = square
                    finish.make_finish()

                elif square != beginning and square != finish:
                    square.make_wall()

            elif pygame.mouse.get_pressed()[2]: # right mouse
                position = pygame.mouse.get_pos()
                row, column = get_clicked_square(position, ROWS, length)
                square = maze[row][column]
                if square == beginning:
                    beginning = None
                
                elif square == finish:
                    finish = None

                square.make_free()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and beginning and finish:
                    # A star
                    update_neighbours(maze)
                    a_star_algorithm(lambda: draw_maze(window, maze, ROWS, length), maze, beginning, finish)
                
                
                elif event.key == pygame.K_b and beginning and finish:
                    # Breadth First
                    update_neighbours(maze)
                    breadth_first_search(lambda: draw_maze(window, maze, ROWS, length), maze, beginning, finish)

                elif event.key == pygame.K_d and beginning and finish:
                    # Depth First
                    update_neighbours(maze)
                    depth_first_search(lambda: draw_maze(window, maze, ROWS, length), maze, beginning, finish)
                    pass

                if event.key == pygame.K_r:
                    beginning = None
                    finish = None
                    maze = make_maze(ROWS, length)

                if event.key == pygame.K_m:
                    reset_search(lambda: draw_maze(window, maze, ROWS, length), maze, beginning, finish)

                if event.key == pygame.K_g:
                    beginning = None
                    finish = None
                    maze = make_maze(ROWS, length)

                    update_neighbours(maze)

                    for rows in maze:
                        for square in rows:
                            square.make_wall()

                    generate_maze_DFS(lambda: draw_maze(window, maze, ROWS, length), maze, ROWS)

    pygame.quit()


main(WINDOW, WINDOW_LENGTH)