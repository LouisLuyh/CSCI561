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


def initialize(s_weights, s_a_s_weights, s_o_weights, o_actions):
    states, initial_probabilities = [], []
    for item in s_weights[1:]:
        states.append(item[0])
        initial_probabilities.append(item[1])

    obs, acts = [], []
    for item in o_actions[1:-1]:
        obs.append(item[0])
        acts.append(item[1])
    obs.append(o_actions[-1][0])

    trans_matrix = {}
    for cur, act, next, weight in s_a_s_weights[1:]:
        if cur not in trans_matrix:
            trans_matrix[cur] = {}
        if act not in trans_matrix[cur]:
            trans_matrix[cur][act] = {}
        trans_matrix[cur][act][next] = weight

    print(trans_matrix)

    emis_matrix = {}
    for state, observation, weight in s_o_weights[1:]:
        if state not in emis_matrix:
            emis_matrix[state] = {}
        if observation not in emis_matrix[state]:
            emis_matrix[state][observation] = {}
        emis_matrix[state][observation] = weight

    print(emis_matrix)

    return states, obs, acts, trans_matrix, emis_matrix, initial_probabilities


