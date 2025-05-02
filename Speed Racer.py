from ursina import *
import random

# Iniciar la aplicación
app = Ursina()

# Variable para saber si estamos en el menú
menu_activo = True
game_over = False

# Crear el menú principal
menu_text = Text(text="SPEED RACER\n\nPresiona ENTER para jugar", origin=(0, 0), scale=2, color=color.white)

# Crear la carretera (con un color más oscuro)
road = Entity(model='quad', scale=(10, 20, 1), texture='white_cube', color=color.gray.tint(-0.3), position=(0, 0, 1))

# Auto del jugador con colisión
player = Entity(model='cube', color=color.red, scale=(1, 2, 1), position=(0, -3, 0), collider='box', enabled=False)

# Lista de obstáculos
obstacles = []

# **Bordes invisibles**
left_border = Entity(model='cube', color=color.clear, scale=(0.5, 20, 1), position=(-5.25, 0, 0), collider='box', enabled=False)
right_border = Entity(model='cube', color=color.clear, scale=(0.5, 20, 1), position=(5.25, 0, 0), collider='box', enabled=False)

# Texto de Game Over (inicialmente oculto)
game_over_text = Text(text="GAME OVER\nPresiona R para reiniciar", origin=(0, 0), scale=2, color=color.white)
game_over_text.enabled = False

# Función para comenzar el juego
def start_game():
    global menu_activo
    menu_activo = False
    menu_text.enabled = False
    player.enabled = True
    left_border.enabled = True
    right_border.enabled = True
    for obstacle in obstacles:
        obstacle.enabled = True

# Función para reiniciar el juego
def restart_game():
    global game_over
    game_over = False
    game_over_text.enabled = False
    player.position = (0, -3, 0)  # Reiniciar posición
    for obstacle in obstacles:
        obstacle.position = (random.uniform(-4, 4), random.uniform(1, 5), 0)  # Reposicionar obstáculos

# Función para mover el auto y detectar colisiones
def update():
    global game_over

    if menu_activo:
        if held_keys['enter']:
            start_game()
        return

    if not game_over:
        if held_keys['left arrow']:
            player.x -= 4 * time.dt
        if held_keys['right arrow']:
            player.x += 4 * time.dt

        # Movimiento de obstáculos
        for obstacle in obstacles:
            obstacle.y -= 2 * time.dt
            if obstacle.y < -4:
                obstacle.y = 5
                obstacle.x = random.uniform(-4, 4)

            # **Colisión con obstáculos**
            if player.intersects(obstacle).hit:
                game_over = True
                game_over_text.enabled = True

        # **Colisión con bordes**
        if player.intersects(left_border).hit or player.intersects(right_border).hit:
            game_over = True
            game_over_text.enabled = True

    # Si presionas "R", se reinicia el juego
    if game_over and held_keys['r']:
        restart_game()

# Crear obstáculos
for _ in range(3):
    obstacles.append(Entity(model='cube', color=color.blue, scale=(1, 2, 1), position=(random.uniform(-4, 4), random.uniform(1, 5), 0), collider='box', enabled=False))

# Iniciar el juego
app.run()
