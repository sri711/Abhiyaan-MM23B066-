"""
import pygame
import time
import random
import rclpy
from std_msgs.msg import String

# Initialize pygame
pygame.init()

# Clock
clock = pygame.time.Clock()

# RGB Color
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Window size
wn_width = 500
wn_height = 400
wn = pygame.display.set_mode((wn_width, wn_height))
pygame.display.set_caption('Race car with road block')

# Load images
bg = pygame.image.load('images/3lane.png')
carimg = pygame.image.load('images/porsche.png')
DEFAULT_IMAGE_SIZE = (wn_width, wn_height)
bg = pygame.transform.scale(bg, DEFAULT_IMAGE_SIZE)
CAR_SIZE = (60, 100)
carimg = pygame.transform.scale(carimg, CAR_SIZE)

# Boundary
west_b = 100
east_b = 380

# Player class
class Player:
    def __init__(self):
        self.image = carimg
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = int(wn_width * 0.5)
        self.rect.y = int(wn_height * 0.5)
        self.speedx = 0

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
        self.rect.x = self.rect.x + self.speedx
        if self.rect.left < west_b:
            self.rect.left = west_b
        if self.rect.right > east_b:
            self.rect.right = east_b

# Obstacle class
class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speedy = 5

    def update(self):
        self.y = self.y + self.speedy
        if self.y > wn_height:
            self.y = 0 - self.height
            self.x = random.randrange(west_b, east_b - self.width)

    def draw(self, wn):
        pygame.draw.rect(wn, RED, [self.x, self.y, self.width, self.height])

def obstacle_callback(msg):
    if not msg:  # Check if message data is empty
        return  # Skip processing if data is empty

    if isinstance(msg, str):  # If the message is a string
        obstacle_info = msg.split(',')
    else:  # If the message is a ROS message
        obstacle_info = msg.data.split(',')

    block_x = int(obstacle_info[0])
    block_y = int(obstacle_info[1])
    block_width = int(obstacle_info[2])
    block_height = int(obstacle_info[3])

    block = Block(block_x, block_y, block_width, block_height)
    obstacles.append(block)

# ROS initialization
rclpy.init()
node = rclpy.create_node('pygame_node')
subscription = node.create_subscription(String, '/obstacle', obstacle_callback, 10)

# Main game loop
def game_loop():
    player = Player()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        player.update()
        wn.blit(bg, (0, 0))
        wn.blit(player.image, (player.rect.x, player.rect.y))
        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(wn)
            if player.rect.colliderect(pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)):
                crash()
        pygame.display.update()
        clock.tick(60)

RANDOM_INITIAL_MESSAGE = "123,-100,80,20"

# Initialize obstacle list with the placeholder obstacle
obstacles = []
obstacle_callback(RANDOM_INITIAL_MESSAGE)

# Start game loop
game_loop()

# Clean up ROS resources
node.destroy_node()
rclpy.shutdown()

# Quit pygame
pygame.quit()
"""
import pygame
import time
import random
import rclpy
from std_msgs.msg import String

# Initialize pygame
pygame.init()

# Clock
clock = pygame.time.Clock()

# RGB Color
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Window size
wn_width = 500
wn_height = 400
wn = pygame.display.set_mode((wn_width, wn_height))
pygame.display.set_caption('Race car with road block')

# Load images
bg = pygame.image.load('images/3lane.png')
carimg = pygame.image.load('images/porsche.png')
DEFAULT_IMAGE_SIZE = (wn_width, wn_height)
bg = pygame.transform.scale(bg, DEFAULT_IMAGE_SIZE)
CAR_SIZE = (60, 100)
carimg = pygame.transform.scale(carimg, CAR_SIZE)

# Boundary
west_b = 100
east_b = 380

# Player class
class Player:
    def __init__(self):
    
        self.image = carimg
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = int(wn_width * 0.5)
        self.rect.y = int(wn_height * 0.5)
        self.speedx = 0

    def selfdrive(self, obstacles):
    	latest_obstacle = obstacles[-1]  # Get the last obstacle from the list
    	obstacle_x = latest_obstacle.x  # Get the x-coordinate of the obstacle

    	if obstacle_x < wn_width / 2:  # Obstacle is towards the left
        	self.speedx = 10  # Move car to the right
    	elif obstacle_x > wn_width / 2:  # Obstacle is towards the right
        	self.speedx = -10  # Move car to the left

    	self.rect.x = self.rect.x + self.speedx  # Update car position

    # Check boundary (west)
    	if self.rect.left < west_b:
        	self.rect.left = west_b

    # Check boundary (east)
    	if self.rect.right > east_b:
        	self.rect.right = east_b
        

# Obstacle class
class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speedy = 3
        self.dodged = 0

    def update(self):
        self.y = self.y + self.speedy
        if self.y > wn_height:
            self.y = 0 - self.height
            self.x = random.randrange(west_b, east_b - self.width)
            
            self.dodged = self.dodged + 1

    def draw(self, wn):
        pygame.draw.rect(wn, RED, [self.x, self.y, self.width, self.height])

def obstacle_callback(msg):
    if not msg:  # Check if message data is empty
        return  # Skip processing if data is empty

    if isinstance(msg, str):  # If the message is a string
        obstacle_info = msg.split(',')
    else:  # If the message is a ROS message
        obstacle_info = msg.data.split(',')

    block_x = int(obstacle_info[0])
    block_y = int(obstacle_info[1])
    block_width = int(obstacle_info[2])
    block_height = int(obstacle_info[3])

    block = Block(block_x, block_y, block_width, block_height)
    obstacles.append(block)

# ROS initialization
rclpy.init()
node = rclpy.create_node('pygame_node')
subscription = node.create_subscription(String, '/obstacle', obstacle_callback, 10)

# Scoreboard function
def score_board(dodged):
    font = pygame.font.Font(None, 25)
    text = font.render('Dodged: ' + str(dodged), True, BLACK)
    wn.blit(text, (0, 0))

# Crash function
def crash():
    font = pygame.font.Font(None, 80)
    text = font.render('You crashed!', True, BLACK)
    text_width = text.get_width()
    text_height = text.get_height()
    x = int(wn_width / 2 - text_width / 2)
    y = int(wn_height / 2 - text_height / 2)
    wn.blit(text, (x, y))
    pygame.display.update()
    time.sleep(2)
    game_loop()

# Main game loop
def game_loop(obstacles):
    player = Player()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        player.selfdrive(obstacles)
        wn.blit(bg, (0, 0))
        wn.blit(player.image, (player.rect.x, player.rect.y))

        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(wn)
            if player.rect.colliderect(pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)):
                crash()

        # Display scoreboard
        score_board(obstacles[-1].dodged)

        pygame.display.update()
        clock.tick(60)

# Initialize obstacle list with the placeholder obstacle
obstacles = []
RANDOM_INITIAL_MESSAGE = "123,-100,80,20"
obstacle_callback(RANDOM_INITIAL_MESSAGE)

# Start game loop
game_loop(obstacles)

# Clean up ROS resources
node.destroy_node()
rclpy.shutdown()

# Quit pygame
pygame.quit()

"""
    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
        self.rect.x = self.rect.x + self.speedx
        if self.rect.left < west_b:
            self.rect.left = west_b
        if self.rect.right > east_b:
            self.rect.right = east_b
            
        
"""            
