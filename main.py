import sdl2
import sdl2.ext
import sdl2.sdlgfx as gfx
import math
import random

# Inisialisasi SDL2
sdl2.ext.init()
window = sdl2.ext.Window("Multiple Car Animation with Sky", size=(800, 600))
window.show()
renderer = sdl2.ext.Renderer(window)
fps_manager = gfx.FPSManager()
gfx.SDL_initFramerate(fps_manager)
gfx.SDL_setFramerate(fps_manager, 60)  # Set frame rate to 60 FPS

# Properti mobil
cars = [
    {"x": 0, "y": 410, "width": 100, "height": 50, "speed": 0.8, "color": (0, 255, 0), "wheel_color": (0, 0, 0)},
    {"x": 150, "y": 425, "width": 100, "height": 50, "speed": 0.3, "color": (255, 0, 0), "wheel_color": (0, 0, 0)},
    {"x": 15, "y": 460, "width": 100, "height": 50, "speed": 0.7, "color": (0, 0, 255), "wheel_color": (0, 0, 0)}
]

striproad = [
    {'x': 0, 'y': 485, 'width': 75, 'height': 10, 'speed': 30, 'color': (255, 255, 255)},
    {'x': 150, 'y': 485, 'width': 75, 'height': 10, 'speed': 30, 'color': (255, 255, 255)},
    {'x': 300, 'y': 485, 'width': 75, 'height': 10, 'speed': 30, 'color': (255, 255, 255)},
    {'x': 450, 'y': 485, 'width': 75, 'height': 10, 'speed': 30, 'color': (255, 255, 255)},
    {'x': 600, 'y': 485, 'width': 75, 'height': 10, 'speed': 30, 'color': (255, 255, 255)},
    {'x': 750, 'y': 485, 'width': 75, 'height': 10, 'speed': 30, 'color': (255, 255, 255)}
]

# Properti bulan dan matahari
moon = {"x": 0, "y": 0, "radius": 30, "angle": 0, "speed": -0.0025, "color": (255, 255, 255)}
sun = {"x": 0, "y": 0, "radius": 50, "angle": 0, "speed": -0.0025, "color": (255, 255, 0)}

# Properti gedung
buildings = [
    {"x": random.randint(0, 800), "y": 300, "width": 100, "height": 150, "speed": random.randint(1, 2), "color": (200, 200, 200)},
    {"x": random.randint(0, 800), "y": 250, "width": 120, "height": 200, "speed": random.randint(1, 2), "color": (180, 180, 180)},
    {"x": random.randint(0, 800), "y": 280, "width": 80, "height": 170, "speed": random.randint(1, 2), "color": (160, 160, 160)},
    {"x": random.randint(0, 800), "y": 240, "width": 150, "height": 210, "speed": random.randint(1, 2), "color": (140, 140, 140)},
    {"x": random.randint(0, 800), "y": 290, "width": 110, "height": 160, "speed": random.randint(1, 2), "color": (120, 120, 120)},
    {"x": random.randint(0, 800), "y": 270, "width": 90, "height": 180, "speed": random.randint(1, 2), "color": (100, 100, 100)}
]

# Dimensi layar
screen_width, screen_height = 800, 600
center_x, center_y = screen_width // 2, screen_height // 2 + 165

# Loop utama
running = True
while running:
    # Tangani event
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False

    # Update posisi mobil
    for car in cars:
        car["x"] += car["speed"]
        if car["x"] > screen_width:
            car["x"] = -car["width"]  # Reset posisi mobil di luar layar

    # Update posisi garis jalan
    for perstrip in striproad:
        perstrip["x"] -= perstrip["speed"]
        if perstrip["x"] < -perstrip["width"]:
            perstrip["x"] = screen_width  # Reset posisi garis jalan di luar layar

    # Update posisi gedung
    for building in buildings:
        building["x"] -= building["speed"]
        if building["x"] < -building["width"]:
            building["x"] = screen_width  # Reset posisi gedung di luar layar
    
    print(f"Sun position: ({sun['x']:.2f}, {sun['y']:.2f}); Moon position: ({moon['x']:.2f}, {moon['y']:.2f})")
    
    # Update posisi bulan dan matahari
    moon["angle"] += moon["speed"]
    moon["x"] = center_x - 390 * math.cos(moon["angle"])
    moon["y"] = center_y - 390 * math.sin(moon["angle"])

    sun["angle"] += sun["speed"]
    sun["x"] = center_x + 450 * math.cos(sun["angle"])
    sun["y"] = center_y + 450 * math.sin(sun["angle"])

    if moon['y'] < 410:
        renderer.clear(sdl2.ext.Color(10, 1, 30))  # Warna biru langit (sky blue)
    elif moon['y'] < 490 or sun['y'] + sun['radius'] > 410:
        renderer.clear(sdl2.ext.Color(70, 141, 170))
    else:
        renderer.clear(sdl2.ext.Color(135, 206, 235))

    # Gambar bulan dan matahari
    gfx.filledCircleRGBA(renderer.sdlrenderer, int(moon["x"]), int(moon["y"]), moon["radius"], moon["color"][0], moon["color"][1], moon["color"][2], sdl2.SDL_ALPHA_OPAQUE)
    gfx.filledCircleRGBA(renderer.sdlrenderer, int(sun["x"]), int(sun["y"]), sun["radius"], sun["color"][0], sun["color"][1], sun["color"][2], sdl2.SDL_ALPHA_OPAQUE)

    # Gambar gedung
    for building in buildings:
        renderer.fill((building["x"], building["y"], building["width"], building["height"]), sdl2.ext.Color(*building["color"]))

    # Gambar jalan dengan warna abu-abu di bagian bawah
    road_rect = sdl2.SDL_Rect(0, 450, screen_width, 90)
    renderer.fill(road_rect, sdl2.ext.Color(50, 50, 50))  # Warna abu-abu jalan
    grass_rect = sdl2.SDL_Rect(0, 540, screen_width, 90)
    renderer.fill(grass_rect, sdl2.ext.Color(25, 200, 46))  # Warna hijau rumput
    
    # Gambar garis jalan
    for perstrip in striproad:
        renderer.fill((perstrip["x"], perstrip["y"], perstrip["width"], perstrip["height"]), sdl2.ext.Color(*perstrip["color"]))
    
    # Gambar setiap mobil
    for car in cars:
        # Gambar badan mobil
        renderer.fill((car["x"], car["y"], car["width"], car["height"]), sdl2.ext.Color(*car["color"]))
        # Gambar roda mobil
        gfx.filledCircleRGBA(renderer.sdlrenderer, int(car["x"] + 20), int(car["y"] + car["height"] - 0), 10, 0, 0, 0, sdl2.SDL_ALPHA_OPAQUE)
        gfx.filledCircleRGBA(renderer.sdlrenderer, int(car["x"] + car["width"] - 20), int(car["y"] + car["height"] - 0), 10, 0, 0, 0, sdl2.SDL_ALPHA_OPAQUE)
        gfx.filledCircleRGBA(renderer.sdlrenderer, int(car["x"] + 20), int(car["y"] + car["height"] - 0), 3, 200, 200, 200, sdl2.SDL_ALPHA_OPAQUE)
        gfx.filledCircleRGBA(renderer.sdlrenderer, int(car["x"] + car["width"] - 20), int(car["y"] + car["height"] - 0), 3, 200, 200, 200, sdl2.SDL_ALPHA_OPAQUE)

    # Update layar
    renderer.present()
    gfx.SDL_framerateDelay(fps_manager)  # Delay untuk menjaga frame rate

# Cleanup
sdl2.ext.quit()