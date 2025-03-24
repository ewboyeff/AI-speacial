def center_element(screen_width, screen_height, element_width, element_height):
    return place_elements_offset(
        screen_width, screen_height, element_width, element_height, 0.5, 0.6
    )


def place_elements_offset(
    screen_width, screen_height, element_width, element_height, xoffset, yoffset
):
    x = (screen_width - element_width) * xoffset
    y = (screen_height - element_height) * yoffset
    return x, y


def __get_x_y(pos, num_rows, num_cols):
    x = pos[0]
    y = pos[1]
    if pos[0] < 0:
        x = num_rows + x
    if pos[1] < 0:
        y = num_cols + y
    return x, y


def get_coords_from_idx(
    pacman_pos, start_x, start_y, cell_w, cell_h, num_rows, num_cols
):
    x, y = __get_x_y(pacman_pos, num_rows, num_cols)
    x_coord = start_x + (y * cell_w)
    y_coord = start_y + (x * cell_h)
    return x_coord, y_coord


def precompute_matrix_coords(start_x, start_y, cell_size, num_rows, num_cols):
    matrix_coords = []
    col_start = start_y
    for _ in range(num_rows):
        row_start = start_x
        m = []
        for _ in range(num_cols):
            m.append([row_start, col_start])
            row_start += cell_size
        col_start += cell_size
        matrix_coords.append(m)
    return matrix_coords


def get_idx_from_coords(x_coord, y_coord, start_x, start_y, cell_size):
    x_pos = int((x_coord - start_x) // cell_size)
    y_pos = int((y_coord - start_y) // cell_size)
    return y_pos, x_pos  # in matrix, horizontal is columns and vertical are rows

def get_tiny_matrix(matrix, cell_size, pacman_speed):
    sub_div = cell_size // pacman_speed
    num_rows = len(matrix) * sub_div
    num_cols = len(matrix[0]) * sub_div
    tiny_matrix = [["null"] * num_cols for _ in range(num_rows)]
    tiny_r, tiny_c = 0, 0
    for row in matrix:
        for cell in row:
            if cell != "wall":
                cell = "null"
            for sx in range(sub_div):
                for sy in range(sub_div):
                    tiny_matrix[tiny_r + sx][tiny_c + sy] = cell
            tiny_c += sub_div
        tiny_r += sub_div
        tiny_c = 0
    return tiny_matrix

def get_movable_locations(matrix, max_cell_size=20, 
                          cell_size=20):
    movables = []
    rows, cols = len(matrix), len(matrix[0])  # Matrix dimensions
    subdiv = max_cell_size // cell_size

    def is_free(r, c):
        return 0 <= r < rows and 0 <= c < cols and matrix[r][c] not in ('wall', 'elec')
    
    def is_valid(r, c):
        for x in range(subdiv*2):
            for y in range(subdiv*2):
                if not is_free(r+x, c+y):
                    return False
        return True

    for r_idx in range(rows):
        for c_idx in range(cols):
            if (r_idx + (subdiv*2) <= rows and \
                 c_idx + (subdiv*2) <= cols) and is_valid(r_idx, c_idx):
                movables.append((r_idx, c_idx))

    return movables

def is_any_wall(matrix, x, y):
    rows, cols = len(matrix), len(matrix[0])  # Matrix dimensions

    def is_wall(r, c):
        """Check if the cell is 'wall' and within bounds."""
        return 0 <= r < rows and 0 <= c < cols and matrix[r][c] == 'wall'

    # Check all four positions
    return (
        is_wall(x, y) or
        is_wall(x, y + 1) or
        is_wall(x + 1, y + 1) or
        is_wall(x + 1, y)
    )