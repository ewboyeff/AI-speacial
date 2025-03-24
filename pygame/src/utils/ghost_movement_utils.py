import math

DIRECTION_MAPPER = {"up":[(-1, 0), (-1, 1)],
                    "left":[(0, -1), (1, -1)],
                    "down":[(2, 0), (2, 1)],
                    "right":[(0, 2), (1, 2)]}
BLOCKERS = ['wall', 'elec']

def get_is_move_valid(curr_pos, direction, matrix):
    next_indices = DIRECTION_MAPPER[direction]
    for r, c in next_indices:
        next_c = curr_pos[1] + c
        if next_c < 0 or next_c >= len(matrix[0]): #because there is only 1 place where ghost can go out of bounds.
            continue
        if matrix[curr_pos[0] + r][curr_pos[1] + c] in BLOCKERS:
            return False
    return True

def eucliad_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def get_direction(ghost_matrix_pos: tuple[int, int],
                target_matrix_pos: tuple[int, int],
                matrix: list[list[str]],
                prev: tuple[int, int]):
    g1, g2 = ghost_matrix_pos
    t1, t2 = target_matrix_pos
    num_rows, _ = len(matrix), len(matrix[0])
    next_direction_mapper = {"up":(-1, 0), "down": (1, 0), "left":(0, -1), "right": (0, 1)}
    directions = ['up', 'left', 'down','right']
    curr_min = float('inf')
    target_dir = None
    for direction in directions:
        is_movable = get_is_move_valid((g1, g2), direction, matrix)
        if not is_movable:
            continue
        direction_additives = next_direction_mapper[direction]
        next_x, next_y = g1 + direction_additives[0], g2 + direction_additives[1]
        if next_x >= num_rows or next_x < 0:
            continue
        if next_direction_mapper[direction] == prev:
            continue
        distance = eucliad_distance((next_x, next_y), (t1, t2))
        if distance < curr_min:
            curr_min = distance
            target_dir = direction
    # print(ghost_matrix_pos, matrix[ghost_matrix_pos[0]][ghost_matrix_pos[1]])
    # print(target_dir)
    if target_dir is None:
        print('error', prev, ghost_matrix_pos, matrix[ghost_matrix_pos[0]][ghost_matrix_pos[1]])
        raise ValueError("Oh my god, I don't know what to do, im crashing the game")
    return next_direction_mapper[target_dir]

def get_is_intersection(ghost_matrix_pos: tuple[int, int], 
                        matrix: list[list[str]],
                        prev=None):
    possible_moves = 0
    for k, _ in DIRECTION_MAPPER.items():
        if prev == k:
            continue
        if get_is_move_valid(ghost_matrix_pos, k, matrix):
            possible_moves += 1
    return possible_moves > 1


