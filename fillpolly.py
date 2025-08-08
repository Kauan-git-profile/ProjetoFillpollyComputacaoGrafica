# 05/08/25

# Inicializção da janela pygame
import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clique para formar o polígono")

# Variáveis globais
points = []
running = True
polygon_closed = False
filled = False

# Função de preenchimento por varredura (scanline)
def scanline_fill(polygon, width, height):
    # Matriz 2D onde 0 é vazio e 1 é preenchido
    # Representa a tela de pixels, cada célula é um pixel
    canvas = [[0 for _ in range(width)] for _ in range(height)]
    
    # Para cada linha Y, encontra interseções com as arestas do polígono
    for y in range(height):
        intersections = []
        for i in range(len(polygon)):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % len(polygon)]
            if (y1 <= y < y2) or (y2 <= y < y1):
                if y1 != y2:
                    x_intersect = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
                    intersections.append(x_intersect)
        
        # Ordena as interseções para processar pares
        intersections.sort()
        
        # Preenche entre os pares de interseções
        for i in range(0, len(intersections), 2):
            if i+1 >= len(intersections):
                break
            start = int(intersections[i])
            end = int(intersections[i+1])
            for x in range(start, end):
                if 0 <= x < width and 0 <= y < height:
                    canvas[y][x] = 1
                    
    return canvas

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and not polygon_closed:
            x, y = pygame.mouse.get_pos()
            points.append((x, y))

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(points) >= 3:
                polygon_closed = True
                # Quando pressionar ENTER, preenche o polígono
                filled = True
                fill_canvas = scanline_fill(points, WIDTH, HEIGHT)
    
    # Limpa a tela
    screen.fill((255, 255, 255))
    
    # Desenha os pontos clicados
    for point in points:
        pygame.draw.circle(screen, (0, 0, 255), point, 4)
    
    # Desenha as linhas do polígono
    if len(points) > 1:
        pygame.draw.lines(screen, (0, 0, 0), polygon_closed, points, 2)
    
    # Se o polígono foi fechado e deve ser preenchido
    if filled:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if fill_canvas[y][x] == 1:
                    screen.set_at((x, y), (255, 0, 0))  # Pinta de vermelho
    
    pygame.display.flip()

pygame.quit()
sys.exit()
