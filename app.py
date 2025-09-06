
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, time, sys, random

# ---------------------------
# Window settings
# ---------------------------
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
ASPECT = WINDOW_WIDTH / WINDOW_HEIGHT

# ---------------------------
# Game physics
# ---------------------------
gravity = -500.0
jump_strength = 250.0
max_jump_duration = 0.35

# ---------------------------
# Ball properties
# ---------------------------
ball_radius = 15.0
ball_pos = [0.0, 0.0, ball_radius]
ball_vel = [0.0, 0.0, 0.0]
jumping = False
jump_start_time = 0.0

# ---------------------------
# Game state
# ---------------------------
score = 0
lives = 3
game_over = False
game_won = False
last_tile = None
time_on_tile = 0.0
max_tile_time = 5
show_timer = False
time_last = time.time()
move_keys = {"a": False, "d": False, "w": False, "s": False}
space_pressed = False
difficulty_timer = None
difficulty_mode = False
camera_distance = 500.0
camera_angle = 45
camera_height = 300.0
wall_height = 80.0

# ---------------------------
# Grid settings
# ---------------------------
grid_size_x = 30
grid_size_y = 20
tile_size = 60
half_size_x = grid_size_x * tile_size / 2
half_size_y = grid_size_y * tile_size / 2

# ---------------------------
# Themes
# ---------------------------
themes = ["default", "dark", "desert", "ice", "space", "lava", "forest", "neon", "sunset", "ocean"]
theme = "default"
theme_colors = {
    "default": {"floor1": (0.302, 0.471, 0.388), "floor2": (0.8, 0.8, 0.8), "wall": (0.2, 0.2, 0.8), "hole": (0.0, 0.0, 0.0)},
    "dark": {"floor1": (0.1, 0.1, 0.1), "floor2": (0.3, 0.3, 0.3), "wall": (0.2, 0.2, 0.8), "hole": (0.5, 0.0, 0.0)},
    "desert": {"floor1": (0.761, 0.698, 0.502), "floor2": (0.9, 0.8, 0.6), "wall": (0.8, 0.7, 0.5), "hole": (0.4, 0.3, 0.1)},
    "ice": {"floor1": (0.8, 0.9, 1.0), "floor2": (0.9, 0.95, 1.0), "wall": (0.7, 0.8, 1.0), "hole": (0.2, 0.5, 0.8)},
    "space": {"floor1": (0.1, 0.1, 0.2), "floor2": (0.2, 0.2, 0.3), "wall": (0.1, 0.1, 0.3), "hole": (0.0, 0.0, 0.3)},
    "lava": {"floor1": (0.8, 0.2, 0.1), "floor2": (0.9, 0.4, 0.2), "wall": (0.8, 0.3, 0.1), "hole": (0.5, 0.0, 0.0)},
    "forest": {"floor1": (0.2, 0.5, 0.2), "floor2": (0.3, 0.6, 0.3), "wall": (0.3, 0.6, 0.3), "hole": (0.1, 0.3, 0.1)},
    "neon": {"floor1": (0.1, 0.8, 0.8), "floor2": (0.8, 0.1, 0.8), "wall": (0.1, 0.8, 0.8), "hole": (0.8, 0.1, 0.8)},
    "sunset": {"floor1": (0.9, 0.5, 0.2), "floor2": (0.8, 0.4, 0.1), "wall": (0.8, 0.4, 0.1), "hole": (0.4, 0.2, 0.1)},
    "ocean": {"floor1": (0.2, 0.4, 0.8), "floor2": (0.3, 0.5, 0.9), "wall": (0.2, 0.4, 0.8), "hole": (0.1, 0.2, 0.4)}
}

# ---------------------------
# Game objects
# ---------------------------
obstacles = []
collectibles = []
special_points = []
holes = set()
speed_multiplier = 1.0

# ---------------------------
# Power-ups
# ---------------------------
shields = [{'pos': [200, 200, 15], 'collected': False}, {'pos': [-200, -200, 15], 'collected': False}]
shield_active = False
shield_time = 0

# ---------------------------
# Moving platforms
# ---------------------------
moving_platforms = [
    {'pos': [0, 0, 25], 'size': [80, 30, 8], 'vel': [60, 0, 0], 'limits': [-250, 250]},
    {'pos': [150, -150, 30], 'size': [50, 50, 8], 'vel': [0, 60, 0], 'limits': [-200, 200]},
]

# ---------------------------
# Teleporters
# ---------------------------
teleporters = [
    {'pos': [300, 300, 15], 'target': [-300, -300, 15]},
    {'pos': [-300, 300, 15], 'target': [300, -300, 15]},
]

# ---------------------------
# Speed boosts / slows / etc.
# ---------------------------
speed_boosts = [
    {'pos': [150, 150, 15], 'active': True, 'duration': 5.0},
    {'pos': [-150, -150, 15], 'active': True, 'duration': 5.0},
]
speed_boost_active = False
speed_boost_timer = 0.0

slow_traps = [
    {'pos': [150, -150, 15], 'active': True, 'duration': 3.0},
    {'pos': [-150, 150, 15], 'active': True, 'duration': 3.0},
]
slow_trap_active = False
slow_trap_timer = 0.0

time_bonuses = [
    {'pos': [250, 250, 15], 'active': True, 'time': 3.0},
    {'pos': [-250, -250, 15], 'active': True, 'time': 3.0},
]

life_collectibles = [
    {'pos': [300, 0, 15], 'active': True},
    {'pos': [-300, 0, 15], 'active': True},
]

multipliers = [
    {'pos': [0, 300, 15], 'active': True, 'duration': 10.0, 'factor': 2},
]
multiplier_active = False
multiplier_timer = 0.0
multiplier_factor = 1

# ---------------------------
# Level progression
# ---------------------------
level = 1
max_level = 10

# ---------------------------
# Pause, scoring, camera
# ---------------------------
paused = False
high_score = 0
camera_mode = "follow"  # "follow", "overhead", "first_person"
ball_color = [1.0, 0.2, 0.2]  # Default red
particles = []

# ---------------------------
# Lighting / Skybox
# ---------------------------
light_position = [0.0, 0.0, 500.0, 1.0]   # <-- FIX: must be length 4
light_color = [1.0, 1.0, 1.0, 1.0]
ambient_light = [0.3, 0.3, 0.3, 1.0]
skybox_size = 2000

# ---------------------------
# Game state management
# ---------------------------
game_state = "menu"  # "menu", "playing", "paused", "game_over", "win", "help"
font = GLUT_BITMAP_HELVETICA_18

# ---------------------------
# Helpers
# ---------------------------
def generate_holes():
    global holes
    holes = set()
    num_holes = min(30 + level * 3, 150)
    while len(holes) < num_holes:
        i = random.randint(0, grid_size_x - 1)
        j = random.randint(0, grid_size_y - 1)
        # Don't place holes near the starting position
        if abs(i - grid_size_x//2) > 3 or abs(j - grid_size_y//2) > 3:
            holes.add((i, j))

def find_safe_tile():
    while True:
        i = random.randint(0, grid_size_x - 1)
        j = random.randint(0, grid_size_y - 1)
        if (i, j) not in holes:
            x = i * tile_size - half_size_x + tile_size / 2
            y = j * tile_size - half_size_y + tile_size / 2
            return (x, y)

def find_safe_start_tile():
    # Find a safe tile near the center
    center_i = grid_size_x // 2
    center_j = grid_size_y // 2
    for radius in range(0, max(grid_size_x, grid_size_y)):
        for i in range(center_i - radius, center_i + radius + 1):
            for j in range(center_j - radius, center_j + radius + 1):
                if 0 <= i < grid_size_x and 0 <= j < grid_size_y and (i, j) not in holes:
                    x = i * tile_size - half_size_x + tile_size / 2
                    y = j * tile_size - half_size_y + tile_size / 2
                    return [x, y, ball_radius]
    return [0.0, 0.0, ball_radius]

def reset_game(reset_score=True, reset_lives=True):
    global ball_pos, ball_vel, jumping, jump_start_time, score, lives, game_over, game_won
    global collectibles, time_last, obstacles, last_tile, time_on_tile, show_timer, special_points
    global difficulty_timer, difficulty_mode, speed_multiplier, level, paused, high_score
    global speed_boost_active, speed_boost_timer, slow_trap_active, slow_trap_timer
    global multiplier_active, multiplier_timer, multiplier_factor, ball_color, particles
    global shield_active, shield_time, game_state

    if score > high_score:
        high_score = score

    ball_pos[:] = find_safe_start_tile()
    ball_vel[:] = [0.0, 0.0, 0.0]
    jumping = False
    jump_start_time = 0.0

    if reset_score:
        score = 0
        generate_holes()
        collectibles = []
        for _ in range(15 + level * 2):
            x, y = find_safe_tile()
            collectibles.append({
                'type': random.choice(['cube', 'torus', 'pyramid', 'sphere', 'teapot']),
                'pos': (x, y, 15),
                'color': (random.random(), random.random(), random.random())
            })

        special_points = []
        for _ in range(5 + level):
            x, y = find_safe_tile()
            special_points.append({'pos': (x, y, 15), 'collected': False})

        # Reset power-ups
        for boost in speed_boosts:
            boost['active'] = True
        for trap in slow_traps:
            trap['active'] = True
        for bonus in time_bonuses:
            bonus['active'] = True
        for life in life_collectibles:
            life['active'] = True
        for mult in multipliers:
            mult['active'] = True
        for shield in shields:
            shield['collected'] = False

        speed_boost_active = False
        speed_boost_timer = 0.0
        slow_trap_active = False
        slow_trap_timer = 0.0
        multiplier_active = False
        multiplier_timer = 0.0
        multiplier_factor = 1
        ball_color = [1.0, 0.2, 0.2]
        shield_active = False
        shield_time = 0
        particles = []

        # Generate obstacles
        obstacles = []
        num_obstacles = min(5 + level * 2, 20)
        for _ in range(num_obstacles):
            x = random.uniform(-half_size_x + 50, half_size_x - 50)
            y = random.uniform(-half_size_y + 50, half_size_y - 50)
            obstacles.append({
                'pos': [x, y, 30],
                'size': random.uniform(15, 30),
                'type': random.choice(['sphere', 'cube', 'cone']),
                'color': (random.random() * 0.5 + 0.5, random.random() * 0.3, random.random() * 0.3)
            })

    if reset_lives:
        lives = 3

    game_over = False
    game_won = False
    time_last = time.time()
    last_tile = None
    time_on_tile = 0.0
    show_timer = False

    difficulty_timer = None
    difficulty_mode = False
    speed_multiplier = 1.0 + level * 0.1

    # Reset moving platforms
    for platform in moving_platforms:
        platform['pos'] = [platform['pos'][0], platform['pos'][1], platform['pos'][2]]

    game_state = "playing"

def setup_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, ASPECT, 1.0, 3000.0)
    glMatrixMode(GL_MODELVIEW)

def reshape(w, h):
    global WINDOW_WIDTH, WINDOW_HEIGHT, ASPECT
    WINDOW_WIDTH = max(1, w)
    WINDOW_HEIGHT = max(1, h)
    ASPECT = WINDOW_WIDTH / WINDOW_HEIGHT
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    setup_projection()

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

def setup_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Set background color based on theme
    if theme == "space":
        glClearColor(0.0, 0.0, 0.1, 1.0)
    elif theme == "ocean":
        glClearColor(0.2, 0.4, 0.8, 1.0)
    elif theme == "sunset":
        glClearColor(0.8, 0.5, 0.2, 1.0)
    elif theme == "lava":
        glClearColor(0.5, 0.2, 0.1, 1.0)
    else:
        glClearColor(0.5, 0.8, 1.0, 1.0)

    # Camera
    if camera_mode == "follow":
        angle_rad = math.radians(camera_angle)
        eye_x = ball_pos[0] - camera_distance * math.cos(angle_rad)
        eye_y = ball_pos[1] + camera_distance * math.sin(angle_rad)
        eye_z = ball_pos[2] + camera_height
        gluLookAt(eye_x, eye_y, eye_z, ball_pos[0], ball_pos[1], ball_pos[2], 0.0, 0.0, 1.0)
    elif camera_mode == "overhead":
        gluLookAt(0, 0, 800, 0, 0, 0, 0, 1, 0)
    elif camera_mode == "first_person":
        gluLookAt(ball_pos[0], ball_pos[1], ball_pos[2] + 10,
                  ball_pos[0] + math.cos(math.radians(camera_angle)) * 10,
                  ball_pos[1] + math.sin(math.radians(camera_angle)) * 10,
                  ball_pos[2] + 10,
                  0.0, 0.0, 1.0)

    setup_lighting()

def draw_skybox():
    glDisable(GL_LIGHTING)
    glBegin(GL_QUADS)

    size = skybox_size
    # Front
    glColor3f(0.6, 0.8, 1.0)
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(-size, size, -size)

    # Back
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)

    # Top - sky
    if theme == "space":
        glColor3f(0.0, 0.0, 0.2)
    elif theme == "sunset":
        glColor3f(0.9, 0.6, 0.3)
    else:
        glColor3f(0.4, 0.6, 1.0)
    glVertex3f(-size, size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)

    # Bottom - ground
    glColor3f(0.3, 0.2, 0.1)
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, -size, size)
    glVertex3f(-size, -size, size)

    # Left
    glColor3f(0.5, 0.7, 0.9)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, size, -size)
    glVertex3f(-size, size, size)
    glVertex3f(-size, -size, size)

    # Right
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, size, size)
    glVertex3f(size, -size, size)

    glEnd()
    glEnable(GL_LIGHTING)

def draw_floor():
    colors = theme_colors[theme]
    for i in range(grid_size_x):
        for j in range(grid_size_y):
            x = i * tile_size - half_size_x
            y = j * tile_size - half_size_y
            if (i, j) in holes:
                glColor3f(*colors["hole"])
                glBegin(GL_QUADS)
                glVertex3f(x, y, 0.0)
                glVertex3f(x + tile_size, y, 0.0)
                glVertex3f(x + tile_size, y + tile_size, 0.0)
                glVertex3f(x, y + tile_size, 0.0)
                glEnd()

                # Draw hole depth
                glColor3f(colors["hole"][0] * 0.7, colors["hole"][1] * 0.7, colors["hole"][2] * 0.7)
                glBegin(GL_QUADS)
                glVertex3f(x + 5, y + 5, -20.0)
                glVertex3f(x + tile_size - 5, y + 5, -20.0)
                glVertex3f(x + tile_size - 5, y + tile_size - 5, -20.0)
                glVertex3f(x + 5, y + tile_size - 5, -20.0)
                glEnd()
            else:
                if (i + j) % 2 == 0:
                    glColor3f(*colors["floor2"])
                else:
                    glColor3f(*colors["floor1"])
                glBegin(GL_QUADS)
                glVertex3f(x, y, 0.0)
                glVertex3f(x + tile_size, y, 0.0)
                glVertex3f(x + tile_size, y + tile_size, 0.0)
                glVertex3f(x, y + tile_size, 0.0)
                glEnd()

def draw_walls():
    colors = theme_colors[theme]
    glColor3f(*colors["wall"])
    for sx, sy in [(-half_size_x,0),(half_size_x,0),(0,half_size_y),(0,-half_size_y)]:
        glBegin(GL_QUADS)
        if sx != 0:
            x = sx
            glVertex3f(x, -half_size_y, 0)
            glVertex3f(x,  half_size_y, 0)
            glVertex3f(x,  half_size_y, wall_height)
            glVertex3f(x, -half_size_y, wall_height)
        else:
            y = sy
            glVertex3f(-half_size_x, y, 0)
            glVertex3f( half_size_x, y, 0)
            glVertex3f( half_size_x, y, wall_height)
            glVertex3f(-half_size_x, y, wall_height)
        glEnd()

def draw_collectibles():
    for c in collectibles:
        glPushMatrix()
        x, y, z = c['pos']
        glTranslatef(x, y, z)
        glColor3f(*c['color'])
        if c['type'] == 'cube':
            glutSolidCube(20)
        elif c['type'] == 'torus':
            glutSolidTorus(5, 10, 16, 16)
        elif c['type'] == 'pyramid':
            glBegin(GL_TRIANGLES)
            glVertex3f(0, 0, 10); glVertex3f(-10, -10, 0); glVertex3f(10, -10, 0)
            glVertex3f(0, 0, 10); glVertex3f(10, -10, 0); glVertex3f(10, 10, 0)
            glVertex3f(0, 0, 10); glVertex3f(10, 10, 0); glVertex3f(-10, 10, 0)
            glVertex3f(0, 0, 10); glVertex3f(-10, 10, 0); glVertex3f(-10, -10, 0)
            glEnd()
            glBegin(GL_QUADS)
            glVertex3f(-10, -10, 0); glVertex3f(10, -10, 0); glVertex3f(10, 10, 0); glVertex3f(-10, 10, 0)
            glEnd()
        elif c['type'] == 'sphere':
            glutSolidSphere(10, 16, 16)
        elif c['type'] == 'teapot':
            glutSolidTeapot(10)
        glPopMatrix()

def draw_special_points():
    for sp in special_points:
        if not sp['collected']:
            glPushMatrix()
            x, y, z = sp['pos']
            glTranslatef(x, y, z)
            glColor3f(1.0, 1.0, 0.0)
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(0, 0, 0)
            for i in range(11):
                angle = i * 2 * math.pi / 10
                radius = 12 if i % 2 == 0 else 6
                glVertex3f(math.cos(angle) * radius, math.sin(angle) * radius, 0)
            glEnd()
            glPopMatrix()

def draw_obstacles():
    for o in obstacles:
        glPushMatrix()
        x, y, z = o['pos']
        glTranslatef(x, y, z)
        glColor3f(*o['color'])
        if o['type'] == 'sphere':
            glutSolidSphere(o['size'], 32, 32)
        elif o['type'] == 'cube':
            glutSolidCube(o['size'] * 2)
        elif o['type'] == 'cone':
            glutSolidCone(o['size'], o['size'] * 1.5, 32, 32)
        glPopMatrix()

def draw_ball():
    glPushMatrix()
    glTranslatef(ball_pos[0], ball_pos[1], ball_pos[2])
    glColor3f(*ball_color)
    glutSolidSphere(ball_radius, 32, 32)
    # Shield effect
    if shield_active:
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glColor4f(0.0, 0.8, 1.0, 0.2)
        glutSolidSphere(ball_radius * 1.5, 32, 32)
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
    glPopMatrix()

def draw_particles():
    if not particles:
        return
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    for p in particles:
        glPushMatrix()
        glTranslatef(p['pos'][0], p['pos'][1], p['pos'][2])
        glColor4f(p['color'][0], p['color'][1], p['color'][2], max(0.0, min(1.0, p['life'] / 30.0)))
        glutSolidSphere(p['size'], 8, 8)
        glPopMatrix()
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)

def draw_moving_platforms():
    for platform in moving_platforms:
        glPushMatrix()
        x, y, z = platform['pos']
        glTranslatef(x, y, z)
        glColor3f(0.5, 0.5, 0.5)
        glScalef(platform['size'][0], platform['size'][1], platform['size'][2])
        glutSolidCube(1)
        glPopMatrix()

def draw_power_ups():
    def draw_box(pos, color, size=15):
        glPushMatrix()
        x, y, z = pos
        glTranslatef(x, y, z)
        glColor3f(*color)
        glutSolidCube(size)
        glPopMatrix()

    for boost in speed_boosts:
        if boost['active']:
            draw_box(boost['pos'], (0.0, 0.0, 1.0), 15)

    for trap in slow_traps:
        if trap['active']:
            draw_box(trap['pos'], (1.0, 0.0, 1.0), 15)

    for bonus in time_bonuses:
        if bonus['active']:
            draw_box(bonus['pos'], (0.5, 0.5, 0.0), 15)

    for life in life_collectibles:
        if life['active']:
            draw_box(life['pos'], (1.0, 0.0, 0.0), 20)

    for mult in multipliers:
        if mult['active']:
            draw_box(mult['pos'], (1.0, 1.0, 0.0), 18)

    for shield in shields:
        if not shield['collected']:
            draw_box(shield['pos'], (0.0, 1.0, 1.0), 25)

def draw_teleporters():
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    for tele in teleporters:
        glPushMatrix()
        x, y, z = tele['pos']
        glTranslatef(x, y, z)
        glColor4f(0.0, 1.0, 0.0, 0.7)
        glutSolidTorus(5, 15, 16, 16)
        glRotatef(time.time() * 100 % 360, 0, 0, 1)
        glColor4f(1.0, 1.0, 1.0, 0.5)
        glutSolidCone(10, 20, 16, 16)
        glPopMatrix()
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

def draw_hud():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)

    # Draw score / lives
    glColor3f(1, 1, 1)
    draw_text(10, WINDOW_HEIGHT - 30, f"Score: {score}")
    draw_text(10, WINDOW_HEIGHT - 60, f"Lives: {lives}")
    draw_text(10, WINDOW_HEIGHT - 90, f"Level: {level}")
    draw_text(10, WINDOW_HEIGHT - 120, f"High Score: {high_score}")

    y_offset = 150
    if speed_boost_active:
        glColor3f(0, 1, 1); draw_text(10, WINDOW_HEIGHT - y_offset, f"Speed Boost: {speed_boost_timer:.1f}s"); y_offset += 30
    if slow_trap_active:
        glColor3f(1, 0, 1); draw_text(10, WINDOW_HEIGHT - y_offset, f"Slow Trap: {slow_trap_timer:.1f}s"); y_offset += 30
    if multiplier_active:
        glColor3f(1, 1, 0); draw_text(10, WINDOW_HEIGHT - y_offset, f"Multiplier x{multiplier_factor}: {multiplier_timer:.1f}s"); y_offset += 30
    if shield_active:
        glColor3f(0, 1, 1); draw_text(10, WINDOW_HEIGHT - y_offset, f"Shield: {shield_time:.1f}s"); y_offset += 30

    if show_timer:
        time_left = max(0, max_tile_time - time_on_tile)
        glColor3f(1, 0.5, 0); draw_text(10, WINDOW_HEIGHT - y_offset, f"Move in: {time_left:.1f}s"); y_offset += 30

    glColor3f(1, 1, 1)
    draw_text(WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30, f"Camera: {camera_mode}")
    draw_text(WINDOW_WIDTH - 200, WINDOW_HEIGHT - 60, f"Theme: {theme}")
    if paused:
        glColor3f(1, 0, 0); draw_text(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2, "PAUSED")

    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_menu():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)

    glColor4f(0.1, 0.1, 0.1, 0.8)
    glBegin(GL_QUADS)
    glVertex2f(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 + 150)
    glVertex2f(WINDOW_WIDTH // 2 + 200, WINDOW_HEIGHT // 2 + 150)
    glVertex2f(WINDOW_WIDTH // 2 + 200, WINDOW_HEIGHT // 2 - 150)
    glVertex2f(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 150)
    glEnd()

    glColor3f(1, 1, 1)
    draw_text(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 + 100, "3D BALL GAME")
    draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50, "Press SPACE to Start")
    draw_text(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2, "Press H for Help")
    draw_text(WINDOW_WIDTH // 2 - 70, WINDOW_HEIGHT // 2 - 50, "Press Q to Quit")
    draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 100, f"High Score: {high_score}")

    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_help():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)

    glColor4f(0.1, 0.1, 0.1, 0.9)
    glBegin(GL_QUADS)
    glVertex2f(50, WINDOW_HEIGHT - 50)
    glVertex2f(WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50)
    glVertex2f(WINDOW_WIDTH - 50, 50)
    glVertex2f(50, 50)
    glEnd()

    glColor3f(1, 1, 1)
    draw_text(100, WINDOW_HEIGHT - 80, "CONTROLS:")
    draw_text(100, WINDOW_HEIGHT - 110, "W/A/S/D - Move ball")
    draw_text(100, WINDOW_HEIGHT - 140, "SPACE - Jump")
    draw_text(100, WINDOW_HEIGHT - 170, "Arrow Keys - Rotate camera")
    draw_text(100, WINDOW_HEIGHT - 200, "C - Change camera mode")
    draw_text(100, WINDOW_HEIGHT - 230, "T - Change theme")
    draw_text(100, WINDOW_HEIGHT - 260, "P - Pause game")
    draw_text(100, WINDOW_HEIGHT - 290, "R - Restart game")
    draw_text(100, WINDOW_HEIGHT - 320, "M - Toggle menu")
    draw_text(100, WINDOW_HEIGHT - 350, "Q or ESC - Quit")

    draw_text(100, WINDOW_HEIGHT - 400, "OBJECTIVE:")
    draw_text(100, WINDOW_HEIGHT - 430, "Collect all items while avoiding holes and obstacles.")
    draw_text(100, WINDOW_HEIGHT - 460, "Don't stay on the same tile for too long!")

    draw_text(WINDOW_WIDTH // 2 - 100, 80, "Press any key to return")

    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_game_over():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)

    glColor4f(0.5, 0.0, 0.0, 0.8)
    glBegin(GL_QUADS)
    glVertex2f(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 + 100)
    glVertex2f(WINDOW_WIDTH // 2 + 200, WINDOW_HEIGHT // 2 + 100)
    glVertex2f(WINDOW_WIDTH // 2 + 200, WINDOW_HEIGHT // 2 - 100)
    glVertex2f(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 100)
    glEnd()

    glColor3f(1, 1, 1)
    draw_text(WINDOW_WIDTH // 2 - 70, WINDOW_HEIGHT // 2 + 50, "GAME OVER")
    draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2, f"Score: {score}")
    draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50, "Press R to Restart")
    draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 80, "Press M for Menu")

    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_win_screen():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)

    glColor4f(0.0, 0.5, 0.0, 0.8)
    glBegin(GL_QUADS)
    glVertex2f(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 + 100)
    glVertex2f(WINDOW_WIDTH // 2 + 200, WINDOW_HEIGHT // 2 + 100)
    glVertex2f(WINDOW_WIDTH // 2 + 200, WINDOW_HEIGHT // 2 - 100)
    glVertex2f(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 100)
    glEnd()

    glColor3f(1, 1, 1)
    draw_text(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 + 50, "YOU WIN!")
    draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2, f"Score: {score}")
    draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50, "Press R to Restart")
    draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 80, "Press M for Menu")

    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def update_particles(dt):
    global particles
    for p in particles[:]:
        p['pos'][0] += p['vel'][0] * dt
        p['pos'][1] += p['vel'][1] * dt
        p['pos'][2] += p['vel'][2] * dt
        p['life'] -= 1
        if p['life'] <= 0:
            particles.remove(p)
    # Emit some trailing particles
    if random.random() < 0.3:
        particles.append({
            'pos': [ball_pos[0] + random.uniform(-10, 10),
                    ball_pos[1] + random.uniform(-10, 10),
                    ball_pos[2] + random.uniform(-5, 5)],
            'vel': [random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(2, 5)],
            'color': ball_color[:],
            'size': random.uniform(2, 5),
            'life': random.randint(10, 30)
        })
