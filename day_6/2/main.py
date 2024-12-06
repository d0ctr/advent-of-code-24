from sys import argv
from time import sleep

POINT = '.'
OBSTACLE = '#'
NEW_OBSTACLE = 'O'

PATH_TURN = '+'
PATH_HOR = '-'
PATH_VER = '|'

PATH_POINTS = [
    PATH_TURN,
    PATH_HOR,
    PATH_VER
]

GUARD_UP = '^'
GUARD_RIGHT = '>'
GUARD_LEFT = '<'
GUARD_DOWN = 'v'

GUARD_DIRECTIONS = [
    GUARD_UP,
    GUARD_RIGHT,
    GUARD_LEFT,
    GUARD_DOWN
]

TURN = {
    GUARD_UP:    GUARD_RIGHT,
    GUARD_RIGHT: GUARD_DOWN,
    GUARD_DOWN:  GUARD_LEFT,
    GUARD_LEFT:  GUARD_UP
}

STEP = {
    GUARD_UP:    ( 0, -1),
    GUARD_RIGHT: (+1,  0),
    GUARD_DOWN:  ( 0, +1),
    GUARD_LEFT:  (-1,  0),
}

MAX_ITERATIONS = 10000

def replace(map, pos, c):
    map[pos[1]] = map[pos[1]][:pos[0]] + c + map[pos[1]][pos[0] + 1:]

def sum(vector, move):
    result = list()
    for i, left in enumerate(vector):
        result.append(left + move[i])
    
    return tuple(result)

def get_current(map):
    pos_x = 0
    pos_y = 0
    direction = None
    for y, row in enumerate(map):
        for x, col in enumerate(row):
            if col in GUARD_DIRECTIONS:
                pos_x = x
                pos_y = y
                direction = col
                break
        if direction is not None:
            break
    return (pos_x, pos_y), direction

def get_next(pos, direction, map, obstacle=(-1, -1)):
    x, y = pos
    dx, dy = STEP[direction]
    next_x, next_y = sum(pos, STEP[direction])
    
    if next_y >= len(map) or next_y == -1 \
        or next_x >= len(map[0]) or next_x == -1:
        
        return pos, (dx, dy), None, direction 
    
    if map[next_y][next_x] == OBSTACLE or (next_x, next_y) == obstacle:
        return get_next(pos, TURN[direction], map)
        
    return (x, y), (dx, dy), (next_x, next_y), direction

def get_moves(start, start_direction, map):
    positions = set()
    positions.add(start)
    _, _, next, direction = get_next(start, start_direction, map)
    while next is not None:
        positions.add(next)
        _, _, next, direction = get_next(next, direction, map)
    
    return positions

def is_loopy(start, start_direction, map, obstacle=(-1, -1)):
    moves = list()
    pos, step, next, direction = get_next(start, start_direction, map, obstacle=obstacle)
    iterations = 0
    while next is not None:
        # print_state(False, moves, map)
        # sleep(1)
        if ((pos, step)) in moves:
            return True, moves
        moves.append((pos, step))
        pos, step, next, direction = get_next(next, direction, map, obstacle=obstacle)
    
    return False, moves

def get_loopy_maps(start, start_direction, moves, map):
    maps = list()
    for pos in moves:
        if pos == start:
            continue
        loopy, loop_moves = is_loopy(start, start_direction, map, obstacle=pos)
        if loopy:
            entry = {
                'obstacle': pos,
                'loopy': loopy,
                'moves': loop_moves
            }
            maps.append(entry)
    
    return maps

def draw_path(moves: set, src_map, obstacle=(-1, -1)):
    last_step = (0, 0)
    map = [row for row in src_map]
    if obstacle != (-1, -1):
        replace(map, obstacle, NEW_OBSTACLE)
    for pos, step in list(moves):
        x, y = pos
        dx, dy = step
        if map[y + dy][x + dx] in GUARD_DIRECTIONS:
            continue
        
        if step != last_step and last_step != (0, 0):
            replace(map, pos, PATH_TURN)
        
        next_x, next_y = sum(pos, step)
        if (map[next_y][next_x] == PATH_HOR and dx == 0) \
            or (map[next_y][next_x] == PATH_VER and dy == 0):
            
            replace(map, (next_x, next_y), PATH_TURN)
        elif dx == 0:
            replace(map, (next_x, next_y), PATH_VER)
        elif dy == 0:
            replace(map, (next_x, next_y), PATH_HOR)
        last_step = step
    
    print('Map:')
    for row in map:
        print(row)

def print_state(loopy, moves, map, obstacle=None):
    print(f'Is loopy: {loopy}')
    draw_path(moves, map, obstacle=obstacle)
    # print('Moves:')
    # print(moves)

def main():
    filename = argv[1]
    map = []
    with open(filename) as file:
        line = file.readline()
        while line:
            map.append(line.strip('\n'))
            line = file.readline()
        
    start, start_direction = get_current(map)
    
    moves = get_moves(start, start_direction, map)
    
    maps = get_loopy_maps(start, start_direction, moves, map)
    
    print(f'Got total of {len(maps)} loopy maps')
    # for entry in maps:
    #     print_state(entry['loopy'], entry['moves'], map, entry['obstacle'])
    
if __name__ == '__main__':
    main()