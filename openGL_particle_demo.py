import pygame
import random
import math
from OpenGL.GL import *
from OpenGL.GLU import *
import ctypes

# Initialize Pygame and OpenGL
pygame.init()
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("OpenGL Particle Benchmark")

# OpenGL setup
glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
gluOrtho2D(0, WIDTH, 0, HEIGHT)   # 2D orthographic projection

# Particle effects list
particle_effects = ["pixel", "line", "circle", "polygon"]

# Particle class
class Particle:
    def __init__(self, effect_type):
        self.effect_type = effect_type
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.color = [random.random(), random.random(), random.random()]
        self.size = random.uniform(2, 10)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(1, 5)
        self.life = random.randint(30, 100)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.life -= 1

    def draw(self):
        glColor3f(*self.color)
        if self.effect_type == "pixel":
            glBegin(GL_POINTS)
            glVertex2f(self.x, self.y)
            glEnd()
        elif self.effect_type == "line":
            glBegin(GL_LINES)
            glVertex2f(self.x, self.y)
            glVertex2f(self.x + math.cos(self.angle) * self.size,
                       self.y + math.sin(self.angle) * self.size)
            glEnd()
        elif self.effect_type == "circle":
            glBegin(GL_POLYGON)
            for i in range(20):  # Approximate circle with polygon
                theta = 2.0 * math.pi * i / 20
                cx = self.x + math.cos(theta) * self.size
                cy = self.y + math.sin(theta) * self.size
                glVertex2f(cx, cy)
            glEnd()
        elif self.effect_type == "polygon":
            glBegin(GL_TRIANGLES)
            for _ in range(3):  # Random triangle
                vx = self.x + random.uniform(-10, 10)
                vy = self.y + random.uniform(-10, 10)
                glVertex2f(vx, vy)
            glEnd()

# Function to render text
def render_text(text, x, y, font, color=(255, 255, 255)):
    surface = font.render(text, True, color)
    texture_data = pygame.image.tostring(surface, "RGBA", True)
    width, height = surface.get_size()

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Render text as a textured quad
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2f(x, y)
    glTexCoord2f(1, 1)
    glVertex2f(x + width, y)
    glTexCoord2f(1, 0)
    glVertex2f(x + width, y + height)
    glTexCoord2f(0, 0)
    glVertex2f(x, y + height)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)

    # Properly delete the texture
    glDeleteTextures(1, [texture_id])



# Particle system
particles = []
current_effect = 0
particle_count = 10
fullscreen = False

# Pygame font for FPS and particle count
font = pygame.font.Font(None, 36)

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    glClear(GL_COLOR_BUFFER_BIT)  # Clear screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Cycle through effects
                current_effect = (current_effect + 1) % len(particle_effects)
            if event.key == pygame.K_RETURN:  # Toggle fullscreen
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.OPENGL | pygame.FULLSCREEN)
                    WIDTH, HEIGHT = screen.get_size()
                    gluOrtho2D(0, WIDTH, 0, HEIGHT)
                else:
                    screen = pygame.display.set_mode((1024, 768), pygame.OPENGL | pygame.DOUBLEBUF)
                    WIDTH, HEIGHT = 1024, 768
                    gluOrtho2D(0, WIDTH, 0, HEIGHT)

    # Spawn particles dynamically
    for _ in range(particle_count - len(particles)):
        particles.append(Particle(particle_effects[current_effect]))

    # Update and draw particles
    for particle in particles[:]:
        particle.update()
        particle.draw()
        if particle.life <= 0:
            particles.remove(particle)

    # Adjust particle count dynamically based on FPS
    fps = clock.get_fps()
    if fps >= 60:
        particle_count += 100
    elif fps < 50:
        particle_count = max(1, particle_count - 10)

    
    # Render FPS and particle count
    glPushMatrix()
    glLoadIdentity()
    render_text(f"FPS: {fps:.2f}", 10, HEIGHT - 40, font)
    render_text(f"Particles: {particle_count}", 10, HEIGHT - 80, font)
    glPopMatrix()

    # Swap buffers
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
