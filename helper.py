import copy


def fetch_player(game_state):
    flat_list = [item for ylist in game_state for xlist in ylist for item in xlist]
    spheres = 64 - flat_list.count("empty")
    if spheres % 2 == 0:
        return "human"
    else:
        return "computer"


def terminal(game_state):
    # Takes a game_state as input and checks if one of the players got 4 in a row and has therefore won the game
    # returns -1 if min-player (human) won and 1 if max-player (comp) won and None if none of the above

    # y axis
    for row in game_state:
        for column in row:
            if len(set(column)) == 1 and column[0] != "empty":
                return -1 if column[0] == "human" else 1

    # x axis - straight line
    for row in game_state:
        for height in range(4):
            if row[0][height] == row[1][height] == row[2][height] == row[3][height] != "empty":
                return -1 if row[0][height] == "human" else 1

    # x axis - diagonal line
    for i in range(4):
        if game_state[i][0][0] == game_state[i][1][1] == game_state[i][2][2] == game_state[i][3][3] != "empty":
            return -1 if game_state[i][0][0] == "human" else 1
        if game_state[i][0][3] == game_state[i][1][2] == game_state[i][2][1] == game_state[i][3][0] != "empty":
            return -1 if game_state[i][0][3] == "human" else 1

    # z axis - straight line
    for i in range(4):
        for j in range(4):
            # straight line
            if game_state[0][i][j] == game_state[1][i][j] == game_state[2][i][j] == game_state[3][i][j] != "empty":
                return -1 if game_state[0][i][j] == "human" else 1

    # z axis - diagonal line
    for i in range(4):
        if game_state[0][i][0] == game_state[1][i][1] == game_state[2][i][2] == game_state[3][i][3] != "empty":
            return -1 if game_state[0][i][0] == "human" else 1
        if game_state[0][i][3] == game_state[1][i][2] == game_state[2][i][1] == game_state[3][i][0] != "empty":
            return -1 if game_state[0][i][3] == "human" else 1

    # diagonal axis - straight line
    for height in range(4):
        if game_state[0][0][height] == game_state[1][1][height] == game_state[2][2][height] == game_state[3][3][height] != "empty":
            return -1 if game_state[0][0][height] == "human" else 1
        if game_state[0][3][height] == game_state[1][2][height] == game_state[2][1][height] == game_state[3][0][height] != "empty":
            return -1 if game_state[0][3][height] == "human" else 1

    # diagonal axis - diagonal line
    if game_state[0][0][0] == game_state[1][1][1] == game_state[2][2][2] == game_state[3][3][3] != "empty":
        return -1 if game_state[0][0][0] == "human" else 1
    if game_state[0][0][3] == game_state[1][1][2] == game_state[2][2][1] == game_state[3][3][0] != "empty":
        return -1 if game_state[0][0][3] == "human" else 1

    # Check for draw
    flat_list = [item for ylist in game_state for xlist in ylist for item in xlist]
    return 0 if flat_list.count("empty") == 0 else None


def actions(game_state):
    action_list = []

    for row in range(4):
        for column in range(4):
            for height in range(4):
                if game_state[row][column][height] == "empty":
                    action_list.append((row, column, height))
                    break

    return action_list


def simulate(game_state, action):
    p = fetch_player(game_state)
    state = copy.deepcopy(game_state)
    state[action[0]][action[1]][action[2]] = p
    return state


def minimax(game_state, recursion=0, w=0):
    if recursion == 3:
        return 0

    t = terminal(game_state)
    if t is not None:
        return t

    apa = actions(game_state)
    p = fetch_player(game_state)
    v = 99 if p == "human" else -99

    if p == "human":
        for action in apa:
            m = min(v, minimax(simulate(game_state, action), recursion=recursion+1, w=v))
            a = action if v != m else a
            v = m
            if v < w: break
            if v == -1: break
        return a if recursion == 0 else v

    if p == "computer":
        for action in apa:
            m = max(v, minimax(simulate(game_state, action), recursion=recursion+1, w=v))
            a = action if v != m else a
            v = m
            if v > w: break
            if v == 1: break
        return a if recursion == 0 else v

