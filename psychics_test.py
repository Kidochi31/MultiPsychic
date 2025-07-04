# Import and initialize the pygame library
import pygame
import math
from pygame import Color
from pygame.mixer import Sound
from psychics_test_helper import draw_circle, draw_image_to_circle, draw_line, draw_line_segment
from psychics import Circle, Line, AABB, LineSegment
from collisions import collides
from vector2 import Vector2
from random import randint, random
from rigidbody import Rigidbody, resolve_rigidbody_line_collision, resolve_rigidbody_circle_collisions
import pygame.freetype

def main():
    pygame.init()
    dt = 0
    clock = pygame.time.Clock()
    omnomnom = Sound("omnomnom.wav")
    hibaby = Sound("hibaby.wav")
    selected_image = pygame.image.load("omnomnom.png")

    GAME_FONT = pygame.freetype.SysFont("Calibri", 30)

    # Set up the drawing window
    screen = pygame.display.set_mode([1000, 750])
    aabb = AABB((-screen.get_width() * 1_000_000//2, screen.get_height()* 1_000_000//2 ), (screen.get_width() * 1_000_000//2, -screen.get_height() * 1_000_000//2))

    circles : list[Circle] = [Circle((0, 0), 50_000_000)]
    lines: list[Line] = [Line((0, -200_000_000), Vector2(1,0)), Line((0, -200_000_000), Vector2(100,-33))]
    collider_lines: list[Line] = lines
    line_segments: list[LineSegment] = [LineSegment((0,0), (0, 50_000_000), (0,0))]
    rigidbodies : list[Rigidbody] = [Rigidbody(circles[0], circles[0].radius ** 2, Vector2(0, -500), 1)]

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    circle = Circle(Vector2(randint(-screen.get_width() * 1_000_000 //2, screen.get_width()* 1_000_000//2), randint(-screen.get_height()//2* 1_000_000, screen.get_height()//2* 1_000_000)), randint(10_000_000, 100_000_000))
                    circles.append(circle)
                    rigidbodies.append(Rigidbody(circle, circle.radius ** 2, Vector2(0, -500), 1))
                    hibaby.play()
                if event.key == pygame.K_l:
                    lines.append(Line(Vector2(randint(-screen.get_width()//2 * 1_000_000, screen.get_width()//2 * 1_000_000), randint(-screen.get_height() //2 * 1_000_000, screen.get_height()//2 * 1_000_000)), random() * math.pi))
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_UP]:
        #     circles[selected_circle].position += Vector2(0,200) * dt
        # if keys[pygame.K_DOWN]:
        #     circles[selected_circle].position += Vector2(0,-200) * dt
        # if keys[pygame.K_RIGHT]:
        #     circles[selected_circle].position += Vector2(200,0) * dt
        # if keys[pygame.K_LEFT]:
        #     circles[selected_circle].position += Vector2(-200,0) * dt
        
        for rigidbody in rigidbodies:
            rigidbody.timestep(dt)

        resolve_rigidbody_line_collision(rigidbodies, collider_lines)
        resolve_rigidbody_circle_collisions(rigidbodies)

        # Fill the background with white
        screen.fill((255, 255, 255))

        # Draw a solid blue circle in the center
        for _, circle in enumerate(list(circles)):
            draw_image_to_circle(screen, circle, selected_image)

        for line in lines:
            draw_line(screen, line, Color(0,0,0), aabb)
        
        for ls in line_segments:
            draw_line_segment(screen, ls, Color(0,0,0))
        
        total_energy = get_total_energy(rigidbodies, Vector2(0, -200))
        GAME_FONT.render_to(screen, (20, 20), f"Energy: {total_energy}", (0, 0, 0))

        # Flip the display
        pygame.display.flip()

        dt = clock.tick(60)

    # Done! Time to quit.
    pygame.quit()

def get_total_energy(circles: list[Rigidbody], relative_to_position: Vector2) -> float:
    return get_total_kinetic_energy(circles) + get_total_gravitational_energy(circles, relative_to_position)

def get_total_kinetic_energy(circles: list[Rigidbody]) -> float:
    energy = 0
    for circle in circles[0:1]:
        energy += circle.mass * (circle.velocity.magnitude())**2 // 2
    return energy

def get_total_gravitational_energy(circles: list[Rigidbody], relative_to_position: Vector2) -> float:
    energy = 0
    for circle in circles[0:1]:
        #energy += circle.mass * (-circle.gravity.dot_product(circle.collider.position - relative_to_position))
        energy += circle.mass * (circle.collider.position.y - relative_to_position.y) * circle.gravity.magnitude()
    return energy

if __name__ == "__main__":
    main()
