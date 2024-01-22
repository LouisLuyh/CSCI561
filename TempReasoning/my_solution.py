# Assignment 3, CSCI 561, Yiheng Lu

from helper import *
import numpy as np

def open_file():
    """
    opens and reads the files, normalize initial weights
    :return: s_weights, s_a_s_weights, s_o_weights, o_actions
    """
    root_dir = "public/speech_recognition/test_case_5/"

    def loader(name):
        file = open(root_dir + name, 'r')
        data = file.read().split('\n')
        file.close()
        if name != "observation_actions.txt":
            info = [int(i) for i in data[1].split()]
            items = data[2:]
            pairs = [info]
            for item in items:
                item = item.split()
                if item:
                    item[-1] = int(item[-1])
                    pairs.append(item)
            return pairs

        if name == "observation_actions.txt":
            num_states = int(data[1])
            observations_actions = data[2:]
            o_a_pairs = [num_states]

            for item in observations_actions:
                item = item.split()
                if item:
                    o_a_pairs.append(item)
            return o_a_pairs

    # s_weights: [[num_states, default_weights], s_w_pair_1, s_w_pair_2, ...]
    s_weights = normalize_s_w(loader("state_weights.txt"))
    # o_actions: [num_states, o_a_pair_1, o_a_pair_2, ...]
    o_actions = loader("observation_actions.txt")
    # s_a_s_weights: [[num_tuples, num_states, num_actions, default_weight], s_a_s_w_pair_1, ...]
    s_a_s_weights = loader("state_action_state_weights.txt")
    # s_o_weights: [[num_pairs, num_states, num_observations, default_weight], s_o_w_pair_1, ...]
    s_o_weights = loader("state_observation_weights.txt")

    return s_weights, s_a_s_weights, s_o_weights, o_actions


def write_result(states):
    """
    given states, write the result
    :param states: the most likely seq
    """
    file = open("states1.txt", 'w')
    file.write("states\n")
    file.write(str(len(states)) + '\n')
    for state in states:
        file.write(state + '\n')
    file.close()


def viterbi_algo(s_weights, s_a_s_weights, s_o_weights, o_actions):
    """
    the body of the Viterbi algorithm
    :param s_weights: normalized initial state weights
    :param s_a_s_weights: state action state weights
    :param s_o_weights: state observation weights
    :param o_actions: observation actions
    :return: the most likely seq
    """
    states, obs, acts, trans_matrix, emis_matrix, initial_probabilities = initialize(s_weights, s_a_s_weights, s_o_weights, o_actions)
    num_states = s_a_s_weights[0][1]
    viterbi_matrix = [[0.0 for r in range(len(obs))] for c in range(num_states)]
    backward = [[0 for r in range(len(obs))] for c in range(num_states)]

    for s in range(num_states):
        viterbi_matrix[s][0] = initial_probabilities[s] * emis_matrix[states[s]][obs[0]]

    for o in range(1, len(obs)):
        x = obs[o]
        a = acts[o-1]
        for s in range(num_states):
            maxP, maxArg = 0, 0
            for ts in range(num_states):
                prob = viterbi_matrix[ts][o-1] * trans_matrix[states[ts]][a][states[s]]
                if prob > maxP:
                    maxP = prob
                    maxArg = ts
            viterbi_matrix[s][o] = maxP * emis_matrix[states[s]][x]
            backward[s][o] = maxArg

    viterbi_matrix = np.array(viterbi_matrix)
    backward = np.array(backward)
    best_path = np.argmax(viterbi_matrix[:, -1])
    best_states = [best_path]

    for o in range(len(obs)-1, 0, -1):
        best_states.insert(0, backward[best_states[0], o])

    result = []
    for state in best_states:
        result.append(states[state])

    print(result)
    print(viterbi_matrix)
    return result


def main():
    s_weights, s_a_s_weights, s_o_weights, o_actions = open_file()
    result = viterbi_algo(s_weights, s_a_s_weights, s_o_weights, o_actions)
    write_result(result)

main()
