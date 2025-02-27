import pygame
import math
import config

# Pygame setup

pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("2D Robot")
clock = pygame.time.Clock()

# Background image
bg_img = pygame.image.load("background.png")  
bg_img = pygame.transform.scale(bg_img, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))  

# Arm parameters
L1, L2, L3 = 70, 70, 70  
origin = (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)  

# Joint angles (in degrees)
theta1 = 0
theta2 = 0
theta3 = 0

# Obstacle parameters
obstacle_x, obstacle_y = config.SCREEN_WIDTH // 4, config.SCREEN_HEIGHT // 3
obstacle_radius = 20

# Flags
control_arm = True
collision_detected = False

def forward_kinematics(theta1, theta2, theta3):
    """Calculate joint positions using forward kinematics."""
    t1 = math.radians(theta1)
    t2 = math.radians(theta2)
    t3 = math.radians(theta3)

    x1 = origin[0] + L1 * math.cos(t1)
    y1 = origin[1] + L1 * math.sin(t1)

    x2 = x1 + L2 * math.cos(t1 + t2)
    y2 = y1 + L2 * math.sin(t1 + t2)

    x3 = x2 + L3 * math.cos(t1 + t2 + t3)
    y3 = y2 + L3 * math.sin(t1 + t2 + t3)

    return [(origin[0], origin[1]), (x1, y1), (x2, y2), (x3, y3)]

running = True
while running:
    screen.blit(bg_img, (0, 0))  # Draw background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Switch control between arm and obstacle
                control_arm = not control_arm

    keys = pygame.key.get_pressed()
    
    if control_arm:
        # Control robotic arm
        if keys[pygame.K_q]: theta1 += 1
        if keys[pygame.K_a]: theta1 -= 1
        if keys[pygame.K_w]: theta2 += 1
        if keys[pygame.K_s]: theta2 -= 1
        if keys[pygame.K_e]: theta3 += 1
        if keys[pygame.K_d]: theta3 -= 1
    else:
        # Control obstacle
        if keys[pygame.K_LEFT]: obstacle_x -= 2
        if keys[pygame.K_RIGHT]: obstacle_x += 2
        if keys[pygame.K_UP]: obstacle_y -= 2
        if keys[pygame.K_DOWN]: obstacle_y += 2

    # Get joint positions
    joints = forward_kinematics(theta1, theta2, theta3)

    # Draw arm
    pygame.draw.lines(screen, config.LINK_COLOR, False, joints, 5)

    # Draw joints
    for joint in joints:
        pygame.draw.circle(screen, config.JOINT_COLOR, (int(joint[0]), int(joint[1])), 8)

    # Draw obstacle
    pygame.draw.circle(screen, config.OBSTACLE_COLOR, (obstacle_x, obstacle_y), obstacle_radius)

    # Display which control mode is active
    font = pygame.font.Font(None, 30)
    mode_text = "Mode: Arm Control" if control_arm else "Mode: Obstacle Control"
    text_surface = font.render(mode_text, True, config.FONT_COLOR)
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()