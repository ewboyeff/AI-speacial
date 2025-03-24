from pygame import draw


def draw_rect(x, y, w, h, screen, color, fill=0):
    draw.rect(screen, color, (x, y, w, h), fill)


def draw_circle(x, y, radius, screen, color):
    draw.circle(screen, color, (x, y), radius)


def draw_debug_rects(start_x, start_y, num_rows, num_cols, cell_size, color, screen):
    curr_x, curr_y = start_x, start_y
    for _ in range(num_rows):
        for _ in range(num_cols):
            draw.rect(screen, color, (curr_x, curr_y, cell_size, cell_size), 1)
            curr_x += cell_size
        curr_y += cell_size
        curr_x = start_x
