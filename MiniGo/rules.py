import copy


def has_liberty(board, move):
    """
    determine whether a move has liberty
    :param board: the current board
    :param move: a selected move
    :return: if after such move has liberty
    """
    adjacent = find_adjacent(move)
    for row, col in adjacent:
        if board[row][col] == 0:
            return True

    return False


# def cluster_liberty(board, move, player):
#     """
#     determine whether a move has liberty
#     :param board: the current board
#     :param move: a selected move
#     :return: if after such move has liberty
#     """
#     cluster = find_cluster(board, move, player)
#     for i in cluster:
#         adjacent = find_adjacent(i)
#         for row, col in adjacent:
#             if board[row][col] == 0:
#                 return True
#
#     return False


def ko_rule(prev_board, curr_board, move, player):
    """
    determine if ko_rule occurs if move is made
    :param prev_board: the board in previous state
    :param curr_board: the current board
    :param move: the planned move
    :param player: the current player
    :return: T/F
    """
    tmp = copy.deepcopy(curr_board)
    tmp[move[0]][move[1]] = player
    for r in range(5):
        for c in range(5):
            if prev_board[r][c] != tmp[r][c]:
                return False
    return True


def captured(board, move, player):
    """
    determine whether the planned move will cause capture
    :param board: the current board
    :param move: the planned move
    :param player: the current player
    :return: T/F
    """
    cluster = find_cluster(board, move, player)
    for i in cluster:
        if has_liberty(board, i):
            return False
    return True


def find_adjacent(p):
    """
    find all the adjacent positions of p
    :param p: the position
    :return: adjacent positions
    """
    r, c = p[0], p[1]
    adjacent = []
    if r > 0:
        adjacent.append((r - 1, c))
    if c > 0:
        adjacent.append((r, c - 1))
    if r < 4:
        adjacent.append((r + 1, c))
    if c < 4:
        adjacent.append((r, c + 1))
    return adjacent


def find_cluster(board, pos, player):
    """
    find the clustering given current position
    :param board: the current board
    :param pos: the position
    :param player: the current player
    :return: the cluster
    """

    def find_ally(p):
        """
        find all the allies in the adjacent positions
        :param p: the position
        :return: the allies
        """
        neighbors = find_adjacent(p)
        ally = []
        for i in neighbors:
            if board[i[0]][i[1]] == player:
                ally.append(i)
        return ally

    stack = [pos]
    cluster = []

    while len(stack) != 0:
        stone = stack.pop()
        cluster.append(stone)
        allies = find_ally(stone)
        for item in allies:
            if item not in stack and item not in cluster:
                stack.append(item)

    return cluster
