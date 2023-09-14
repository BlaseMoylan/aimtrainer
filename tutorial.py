import pygame
import math
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 800  # Dimensions of the game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
pygame.display.set_caption("Aim Trainer")  # Set the window title

TARGET_INCREMENT = 3000  # Time interval (in milliseconds) between target spawns
TARGET_EVENT = pygame.USEREVENT  # Custom event for target spawning

TARGET_PADDING = 30  # Minimum distance from the window edge for target spawns

BG_COLOR = (0, 25, 40)  # Background color
LIVES = 3  # Number of lives the player has
TOP_BAR_HEIGHT = 50  # Height of the top bar displaying game info

LABEL_FONT = pygame.font.SysFont("comicsans", 24)  # Font for labels

class Target:
    """
    The `Target` class represents a target in the Aim Trainer game.

    Attributes:
    - MAX_SIZE (int): The maximum size a target can grow to.
    - GROWTH_RATE (float): The rate at which the target grows.
    - COLOR (str): The primary color of the target.
    - SECOND_COLOR (str): The secondary color of the target.

    Methods:
    - __init__(x, y): Initializes a target with a given position.
    - update(): Updates the target's size and growth.
    - draw(win): Draws the target on the given Pygame window.
    - collide(x, y): Checks if a point (x, y) collides with the target.

    Example Usage:
    >>> target = Target(100, 200)
    >>> target.update()
    >>> target.draw(WIN)
    >>> collision = target.collide(120, 220)
    """

    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        """
        Initializes a target with a given position.

        Parameters:
        - x (int): The x-coordinate of the target.
        - y (int): The y-coordinate of the target.
        """
        self.x = x
        self.y = y
        self.size = 0
        self.growth = True

    def update(self):
        """
        Updates the target's size and growth.
        """
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.growth = False

        if self.growth:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        """
        Draws the target on the given Pygame window.

        Parameters:
        - win (pygame.Surface): The Pygame window surface.
        """
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):
        """
        Checks if a point (x, y) collides with the target.

        Parameters:
        - x (int): The x-coordinate of the point.
        - y (int): The y-coordinate of the point.

        Returns:
        bool: True if the point collides with the target, False otherwise.
        """
        dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return dis <= self.size

def draw(win, targets):
    """
    Draws the targets on the window.

    Parameters:
    - win (pygame.Surface): The Pygame window surface.
    - targets (list): A list of Target objects to be drawn.
    """
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)

# Function to format time as a string
def format_time(secs):
    """
    Formats time in seconds as a string in the format "MM:SS:mm".

    Parameters:
    - secs (float): Time in seconds.

    Returns:
    str: The formatted time string.
    """
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}:{milli}"

# Function to draw the top bar with game information
def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    """
    Draws the top bar with game information on the window.

    Parameters:
    - win (pygame.Surface): The Pygame window surface.
    - elapsed_time (float): Elapsed time in seconds.
    - targets_pressed (int): Number of targets pressed.
    - misses (int): Number of misses.
    """
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")
    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))

# Function to display the end screen
def end_screen(win, elapsed_time, targets_pressed, clicks):
    """
    Displays the end screen with game statistics.

    Parameters:
    - win (pygame.Surface): The Pygame window surface.
    - elapsed_time (float): Elapsed time in seconds.
    - targets_pressed (int): Number of targets pressed.
    - clicks (int): Number of clicks.
    """
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")
    accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")
    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

def get_middle(surface):
    """
    Calculates the x-coordinate to center a surface horizontally on the window.

    Parameters:
    - surface (pygame.Surface): The Pygame surface to be centered.

    Returns:
    float: The x-coordinate to center the surface.
    """
    return WIDTH / 2 - surface.get_width() / 2

def main():
    """
    The main function that runs the Aim Trainer game.
    """
    run = True
    targets = []
    clock = pygame.time.Clock()
    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

        if misses >= LIVES:
            end_screen(WIN, elapsed_time, targets_pressed, clicks)

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

# I also want to add an option to continue to play the game and also maybe compare scores from past games