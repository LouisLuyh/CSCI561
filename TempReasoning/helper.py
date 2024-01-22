# helper, CSCI 561, Yiheng Lu

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


def initialize(s_weights, s_a_s_weights, s_o_weights, o_actions):
    """
    initialize all weights pairs, normalize s_a_s_weights and s_o_weights
    :param s_weights: normalized initial state weights
    :param s_a_s_weights: state action state weights
    :param s_o_weights: state observation weights
    :param o_actions: observation actions
    :return: tates, obs, acts, trans_matrix, emis_matrix, initial_probabilities
    """
    distinct_obs = []
    for _, o, _ in s_o_weights[1:]:
        if o not in distinct_obs:
            distinct_obs.append(o)

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
    s_a_s_default = s_a_s_weights[0][-1]
    for cur, act, next, weight in s_a_s_weights[1:]:
        if cur not in trans_matrix:
            trans_matrix[cur] = {}
        if act not in trans_matrix[cur]:
            trans_matrix[cur][act] = {}
        trans_matrix[cur][act][next] = weight

    if acts[0] == '"N"':
        for s in states:
            for ts in states:
                if ts not in trans_matrix[s]['"N"']:
                    trans_matrix[s]['"N"'][ts] = s_a_s_default

    emis_matrix = {}
    s_o_default = s_o_weights[0][-1]
    for state, observation, weight in s_o_weights[1:]:
        if state not in emis_matrix:
            emis_matrix[state] = {}
        if observation not in emis_matrix[state]:
            emis_matrix[state][observation] = {}
        emis_matrix[state][observation] = weight

    if acts[0] == '"N"':
        for s in states:
            for ob in distinct_obs:
                if ob not in emis_matrix[s]:
                    emis_matrix[s][ob] = s_o_default

    for s in states:
        if acts[0] == '"N"':
            trans_total_weight = sum(trans_matrix[s]['"N"'].values())
            emis_total_weight = sum(emis_matrix[s].values())
            for ts in states:
                trans_matrix[s]['"N"'][ts] /= trans_total_weight
            for o in distinct_obs:
                emis_matrix[s][o] /= emis_total_weight
        else:
            emis_total_weight = sum(emis_matrix[s].values())
            for a, ts in trans_matrix[s].items():
                trans_total_weight = sum(ts.values())
                for i in states:
                    trans_matrix[s][a][i] /= trans_total_weight
            for o in distinct_obs:
                emis_matrix[s][o] /= emis_total_weight

    return states, obs, acts, trans_matrix, emis_matrix, initial_probabilities

