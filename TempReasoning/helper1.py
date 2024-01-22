# helper, CSCI 561, Yiheng Lu
import numpy as np


def normalize_s_w(seq):
    """
    given state weights combinations, normalize weights
    :param seq: state weights
    :return: normalized state weights
    """
    total_weight = 0
    for item in seq[1:]:
        total_weight += item[-1]
    for item in seq[1:]:
        item[-1] = round(item[-1]/total_weight, 5)

    return seq


def normalize_s_a_s_w(seq):
    """
    given state action state weights combinations, normalize weights
    :param seq: state action state weights
    :return: normalized state action state weights
    """
    pos, i = 0, 1
    while i < len(seq):
        weight = seq[i][-1]
        for j in range(i+1, len(seq)):
            if seq[i][0] == seq[j][0] and seq[i][1] == seq[j][1]:
                weight += seq[j][-1]
                pos = j
            else:
                break
        for k in range(i, pos+1):
            seq[k][-1] = round(seq[k][-1]/weight, 5)
        i = pos + 1

    return seq


def normalize_s_o_w(seq):
    """
    given state observation weights combinations, normalize weights
    :param seq: observation weights
    :return: normalized observation weights
    """
    pos, i = 0, 1
    while i < len(seq):
        weight = seq[i][-1]
        for j in range(i+1, len(seq)):
            if seq[i][0] == seq[j][0]:
                weight += seq[j][-1]
                pos = j
            else:
                break
        for k in range(i, pos+1):
            seq[k][-1] = round(seq[k][-1]/weight, 5)
        i = pos + 1

    return seq


def initialization(o_a, s_w, s_a_s_w, s_o_w):
    states, initial_probabilities = [], []
    for item in s_w[1:]:
        states.append(item[0])
        initial_probabilities.append(item[1])

    obs, acts = [], []
    for item in o_a[1:-1]:
        obs.append(item[0])
        acts.append(item[1])
    obs.append(o_a[-1][0])

    num_states, num_actions = s_a_s_w[0][1], s_a_s_w[0][2]
    transition_matrix = np.empty((num_states, num_actions, num_states))
    i = 1
    for a in range(num_actions):
        for c in range(num_states):
            for r in range(num_states):
                transition_matrix[c, a, r] = s_a_s_w[i][-1]
                i += 1

    actions, a, mapped_actions = [], 1, []
    while len(actions) < num_actions:
        if s_a_s_w[a][1] not in actions:
            actions.append(s_a_s_w[a][1])
        a += 1

    for a in acts:
        mapped_actions.append(actions.index(a))

    num_states, num_observations = s_o_w[0][1], s_o_w[0][2]
    emission_matrix = np.empty((num_states, num_observations))
    i = 1
    for s in range(num_states):
        for o in range(num_observations):
            emission_matrix[s, o] = s_o_w[i][-1]
            i += 1

    print(initial_probabilities)

    return states, initial_probabilities, obs, mapped_actions, transition_matrix, emission_matrix

