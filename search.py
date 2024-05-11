import pygame, heapq
from collections import deque

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

class BreadthFirstSearchVisualization:
    def __init__(self, maze):
        self.maze = maze
        self.start = None
        self.goal = None

        pygame.init()

        # Display
        self.screen_width = len(maze[0]) * 30
        self.screen_height = len(maze) * 30
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pacman Search Visualization")

        # Fame rate
        self.clock = pygame.time.Clock()

        # Drav wall
        self.wall_img = pygame.Surface((30, 30))
        self.wall_img.fill(BLUE)

    def draw_maze(self):
        self.screen.fill(WHITE)
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == '#':
                    self.screen.blit(self.wall_img, (x * 30, y * 30))

    def draw_food(self, position):
        pygame.draw.circle(self.screen, GREEN, (position[1] * 30 + 15, position[0] * 30 + 15), 10)

    def draw_pacman(self, position):
        pygame.draw.circle(self.screen, ORANGE, (position[1] * 30 + 15, position[0] * 30 + 15), 10)

    def find_food(self, start, goal):
        self.start = start
        self.goal = goal

        frontier = deque([start])
        visited = set()
        came_from = {}

        while frontier:
            current = frontier.popleft()
            visited.add(current)

            if current == goal:
                break

            for next_node in self.get_neighbors(current):
                if next_node not in visited:
                    frontier.append(next_node)
                    came_from[next_node] = current

        path = self.reconstruct_path(came_from, start, goal)
        for position in path:
            self.draw_maze()
            self.draw_food(goal)
            self.draw_pacman(position)
            pygame.display.update()
            pygame.time.delay(200)  # Delay animation
        return path

    def get_neighbors(self, node):
        neighbors = []
        x, y = node
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(self.maze) and 0 <= new_y < len(self.maze[0]) and self.maze[new_x][new_y] != '#':
                neighbors.append((new_x, new_y))
        return neighbors

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def run_visualization(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

class DepthFirstSearchVisualization:
    def __init__(self, maze):
        self.maze = maze
        self.start = None
        self.goal = None

        pygame.init()

        # Display
        self.screen_width = len(maze[0]) * 30
        self.screen_height = len(maze) * 30
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pacman Search Visualization")

        # Frame rate
        self.clock = pygame.time.Clock()

        # Draw wall
        self.wall_img = pygame.Surface((30, 30))
        self.wall_img.fill(BLUE)

    def draw_maze(self):
        self.screen.fill(WHITE)
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == '#':
                    self.screen.blit(self.wall_img, (x * 30, y * 30))

    def draw_food(self, position):
        pygame.draw.circle(self.screen, GREEN, (position[1] * 30 + 15, position[0] * 30 + 15), 10)

    def draw_pacman(self, position):
        pygame.draw.circle(self.screen, ORANGE, (position[1] * 30 + 15, position[0] * 30 + 15), 10)

    def find_food(self, start, goal):
        self.start = start
        self.goal = goal

        frontier = [start]
        visited = set()
        came_from = {}

        while frontier:
            current = frontier.pop()
            visited.add(current)

            if current == goal:
                break

            for next_node in self.get_neighbors(current):
                if next_node not in visited:
                    frontier.append(next_node)
                    came_from[next_node] = current

        path = self.reconstruct_path(came_from, start, goal)
        for position in path:
            self.draw_maze()
            self.draw_food(goal)
            self.draw_pacman(position)
            pygame.display.update()
            pygame.time.delay(200)  # Delay animation
        return path

    def get_neighbors(self, node):
        neighbors = []
        x, y = node
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(self.maze) and 0 <= new_y < len(self.maze[0]) and self.maze[new_x][new_y] != '#':
                neighbors.append((new_x, new_y))
        return neighbors

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def run_visualization(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

class AStarSearchVisualization:
    def __init__(self, maze):
        self.maze = maze
        self.start = None
        self.goal = None

        pygame.init()

        # Display
        self.screen_width = len(maze[0]) * 30
        self.screen_height = len(maze) * 30
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("A* Search Visualization")

        # Frame rate
        self.clock = pygame.time.Clock()

        # Draw wall
        self.wall_img = pygame.Surface((30, 30))
        self.wall_img.fill(BLUE)

    def draw_maze(self):
        self.screen.fill(WHITE)
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == '#':
                    self.screen.blit(self.wall_img, (x * 30, y * 30))

    def draw_food(self, position):
        pygame.draw.circle(self.screen, GREEN, (position[1] * 30 + 15, position[0] * 30 + 15), 10)

    def draw_pacman(self, position):
        pygame.draw.circle(self.screen, ORANGE, (position[1] * 30 + 15, position[0] * 30 + 15), 10)

    def heuristic(self, node, goal):
        # Manhattan distance heuristic
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def find_food(self, start, goal):
        self.start = start
        self.goal = goal

        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            current_cost, current = heapq.heappop(frontier)

            if current == goal:
                break

            for next_node in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1  # Cost of moving to the next node is 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(next_node, goal)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

        path = self.reconstruct_path(came_from, start, goal)
        for position in path:
            self.draw_maze()
            self.draw_food(goal)
            self.draw_pacman(position)
            pygame.display.update()
            pygame.time.delay(200)  # Delay animation
        return path

    def get_neighbors(self, node):
        neighbors = []
        x, y = node
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(self.maze) and 0 <= new_y < len(self.maze[0]) and self.maze[new_x][new_y] != '#':
                neighbors.append((new_x, new_y))
        return neighbors

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def run_visualization(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

# Example usage:
maze = [
    "####   ### ###",
    "#    # #     #",
    "####P# #     #",
    "#   #   #    #",
    "#   ### #    #",
    "#        #    ",
    "#   ### #     ",
    "#      #     #",
    "#   ##  F    #",
    "##############"
]

start = (2, 4)  # Pacman
goal = [(5, 6), (8, 8)]   # Position of food

search = BreadthFirstSearchVisualization(maze)
path = search.find_food(start, goal[1])
search.run_visualization()
