from rules import *
import copy


def next_board(board, move, player):
    """
    create the next game board if move is placed
    :param board: the current game board
    :param move: the planed move
    :param player: the player
    :return: a next game board
    """
    tmp = copy.deepcopy(board)
    tmp[move[0]][move[1]] = player
    return tmp


def find_move(board):
    """
    return all moves that are legal (KO rule not checked)
    :param board: current board
    :return: all legal moves
    """
    moves = []
    for i in range(5):
        for j in range(5):
            if board[i][j] == 0:
                moves.append((i, j))

    return moves


def possible_move(prev_board, curr_board, move, player):
    """
    checks whether a selected move is possible
    :param prev_board: previous game board
    :param curr_board: current game board
    :param move: move
    :param player: player
    :return: T/F
    """
    tmp = next_board(curr_board, move, player)
    dead_stones = find_captures(tmp, 3-player)
    if dead_stones:
        tmp = remove_captures(tmp, dead_stones)
    if not captured(tmp, move, player) and not ko_rule(prev_board, tmp, move, player):
        return True
    return False


def valid_moves(prev_board, curr_board, player):
    """
    return all moves that are valid
    :param prev_board: previous game board
    :param curr_board: current game board
    :param player: player
    :return: a list of moves
    """
    moves = find_move(curr_board)
    result = list()
    for move in moves:
        if possible_move(prev_board, curr_board, move, player):
            result.append(move)

    return result


def find_captures(board, player):
    """
    find all the stones that are captured
    :param board: the current game board
    :param player: the player
    :return: a list of captured cluster
    """
    captures = []
    for r in range(5):
        for c in range(5):
            if board[r][c] == player:
                if captured(board, (r, c), player):
                    captures.append((r, c))
    return captures


def remove_captures(board, caps):
    """
    remove all the captured stone
    :param board: current game board
    :param caps: captured stones
    :return: the cleared game board
    """
    temp = copy.deepcopy(board)
    for r, c in caps:
        temp[r][c] = 0
    return temp

# board = [[0, 1, 1, 1, 1],
#          [1, 2, 1, 1, 1],
#          [0, 2, 2, 2, 2],
#          [2, 2, 2, 2, 1],
#          [0, 0, 2, 1, 0]
#          ]
# p =     [[0, 1, 1, 1, 1],
#          [1, 2, 1, 1, 1],
#          [0, 2, 2, 2, 2],
#          [2, 2, 2, 2, 1],
#          [1, 0, 2, 1, 0]
#          ]
# # cluster = find_cluster(board, (4, 4), 1)
# # print(captured(board, (0,0), 2))
# #print(find_captures(p, 1))
# # print(find_move(p))
# # print(possible_move(p, board, (0,0), 2))
# print(valid_moves(p, board, 2))