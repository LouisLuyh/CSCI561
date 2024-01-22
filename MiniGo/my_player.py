# Assignment 2, CSCI 561, Yiheng Lu

import math
import random as rd
from helpers import *


def stone_score(state, player):
    """
    Count the total scores of the two players
    :param state: the current game board
    :param player: the player
    :return: the current total score of player and opponent
    """
    player_score, opponent_score = 0, 0
    for r in range(5):
        for c in range(5):
            if state[r][c] == player:
                player_score += 1
            elif state[r][c] == 3-player:
                opponent_score += 1

    return player_score, opponent_score


def liberty_score(state, move):
    """
    Count the total liberty that a cluster has
    :param state: current game board
    :param move: the selected position
    :return: number of liberties
    """
    score = 0
    cluster = find_cluster(state, move, state[move[0]][move[1]])
    for m in cluster:
        adjs = find_adjacent(m)
        for r, c in adjs:
            if board[r][c] == 0:
                score += 1
    return score


def rewards(state, player):
    """
    Set the number of stones + liberty score + number of captures as the total score
    :param state: current game board
    :param player: the player
    :return: return reward as player - opponent for maximizer and opponent - player for minimizer
    """
    player_score, opponent_score = stone_score(state, player)

    for r in range(5):
        for c in range(5):
            if state[r][c] == player:
                player_score += liberty_score(state, (r, c))
                captures = find_captures(state, 3 - player)
                player_score += len(captures)
            elif state[r][c] == 3-player:
                opponent_score += liberty_score(state, (r, c))
                captures = find_captures(state, player)
                opponent_score += len(captures)

    return player_score, opponent_score


def minmax(prev, curr, player):
    """
    The body of min-max algorithm
    :param prev: previous game board
    :param curr: current game board
    :param player: the player
    :return: a list of best moves / the best move
    """
    best = -math.inf
    alpha, beta = -math.inf, math.inf
    actions = valid_moves(prev, curr, player)
    move = []

    for item in actions:
        temp = next_board(curr, item, player)
        value = min_value(curr, temp, alpha, beta, 3-player)

        if value > best:
            best = value
            move = [item]
        elif value == best:
            move.append(item)

    return move


def max_value(prev, curr, alpha, beta, player, d=2):
    """
    The max player of the min-max
    :param prev: previous game board
    :param curr: current game board
    :param player: the player
    :param d: depth
    :return: the best score
    """
    best_value, _ = rewards(curr, player)
    if d == 0:
        return best_value
    actions = valid_moves(prev, curr, player)

    for item in actions:

        tmp_board = next_board(curr, item, player)
        dead_stones = find_captures(tmp_board, 3-player)
        if dead_stones:
            tmp_board = remove_captures(tmp_board, dead_stones)

        best_value = max(best_value, min_value(curr, tmp_board, alpha, beta, 3-player, d-1))
        if best_value >= beta:
            return best_value
        alpha = max(best_value, alpha)

    return best_value


def min_value(prev, curr, alpha, beta, player, d=2):
    """
    the min player of the min-max
    :param prev: previous game board
    :param curr: current game board
    :param player: the player
    :param d: depth
    :return: the best score
    """
    _, best_value = rewards(curr, player)
    if d == 0:
        return best_value
    actions = valid_moves(prev, curr, player)

    for item in actions:

        tmp_board = next_board(curr, item, player)
        dead_stones = find_captures(tmp_board, 3-player)
        if dead_stones:
            tmp_board = remove_captures(tmp_board, dead_stones)

        best_value = min(best_value, max_value(curr, tmp_board, alpha, beta, 3-player, d-1))
        if best_value <= alpha:
            return best_value
        beta = min(best_value, beta)

    return best_value


def open_file():
    """
    Open and reads the input
    :return: the player, the board(both previous and current)
    """
    file = open('input.txt', 'r')
    info = []
    state = []
    for i in file:
        info.append(i.strip('\n'))
    file.close()
    for i in range(1, len(info)):
        tmp = []
        for j in info[i]:
            tmp.append(int(j))
        state.append(tmp)

    return info[0], state


def write_result(move):
    """
    write the result to the output file
    :param move: either a tuple or PASS
    :return: None
    """
    file = open('output.txt', 'w')
    if type(move) == tuple:
        print(move)
        file.write(str(move).strip('()'))
    else:
        file.write("PASS\n")
        print("PASS")

    file.close()


color, board = open_file()
prev_board = board[:5]
curr_board = board[5:]
color = int(color)

mM = minmax(prev_board, curr_board, color)
print(mM)
if not mM:
    write_result("PASS")
else:
    if (2, 2) in mM:
        write_result((2, 2))
    else:
        write_result(rd.choice(mM))

