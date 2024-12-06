from sys import argv
from time import sleep

POINT = '.'
OBSTACLE = '#'
PAST_STEP = 'X'

GUARD_UP = '^'
GUARD_RIGHT = '>'
GUARD_LEFT = '<'
GUARD_DOWN = 'v'

GUARD_DIRECTION = [
    GUARD_UP,
    GUARD_RIGHT,
    GUARD_LEFT,
    GUARD_DOWN
]

def turn(direction):
    if direction == GUARD_UP:
        return GUARD_RIGHT
    if direction == GUARD_RIGHT:
        return GUARD_DOWN
    if direction == GUARD_DOWN:
        return GUARD_LEFT
    if direction == GUARD_LEFT:
        return GUARD_UP

def get_current(map):
    pos_x = 0
    pos_y = 0
    direction = None
    for y, row in enumerate(map):
        for x, col in enumerate(row):
            if col in GUARD_DIRECTION:
                pos_x = x
                pos_y = y
                direction = col
                break
        if direction is not None:
            break
    return pos_x, pos_y, direction

def get_next(pos_x, pos_y, direction, map):
    if direction == GUARD_UP:
        if pos_y == 0:
            return None, None, None
        
        if map[pos_y - 1][pos_x] == OBSTACLE:
            return get_next(pos_x, pos_y, turn(direction), map)
        
        return pos_x, pos_y - 1, direction
    
    if direction == GUARD_RIGHT:
        if pos_x == len(map[0]) - 1:
            return None, None, None
        
        if map[pos_y][pos_x + 1] == OBSTACLE:
            return get_next(pos_x, pos_y, turn(direction), map)
        
        return pos_x + 1, pos_y, direction
    
    if direction == GUARD_DOWN:
        if pos_y == len(map) - 1:
            return None, None, None
        
        if map[pos_y + 1][pos_x] == OBSTACLE:
            return get_next(pos_x, pos_y, turn(direction), map)
        
        return pos_x, pos_y + 1, direction
    
    if direction == GUARD_LEFT:
        if pos_x == 0:
            return None, None, None
        
        if map[pos_y][pos_x - 1] == OBSTACLE:
            return get_next(pos_x, pos_y, turn(direction), map)
        
        return pos_x - 1, pos_y, direction
    
    raise Exception('how?')

def get_positions_count(start_x, start_y, start_direction, map):
    map[start_y] = map[start_y][:start_x] + PAST_STEP + map[start_y][start_x + 1:]
    counter = 1
    next_x, next_y, direction = get_next(start_x, start_y, start_direction, map)
    while next_x is not None:
        if map[next_y][next_x] != PAST_STEP:
            counter += 1
            map[next_y] = map[next_y][:next_x] + PAST_STEP + map[next_y][next_x + 1:]
        next_x, next_y, direction = get_next(next_x, next_y, direction, map)
    
    return counter

def print_state(count, map):
    print(f'Number of positions: {count}')
    print('Map:')
    for row in map:
        print(row)
    

def main():
    filename = argv[1]
    map = []
    with open(filename) as file:
        line = file.readline()
        while line:
            map.append(line.strip('\n'))
            line = file.readline()
        
    start_x, start_y, start_direction = get_current(map)
    
    count = get_positions_count(start_x, start_y, start_direction, map)
    
    print_state(count, map)
    
if __name__ == '__main__':
    main()