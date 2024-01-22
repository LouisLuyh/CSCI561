# Assignment 3, CSCI 561, Yiheng Lu
from helper1 import *
from operator import itemgetter


def open_file():
    root_dir = "public/little_prince/test_case_2/"

    def loader(name):
        file = open(root_dir + name, 'r')
        data = file.read().replace('"', '').split('\n')
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
    s_a_s_weights = normalize_s_a_s_w(loader("state_action_state_weights.txt"))
    # s_o_weights: [[num_pairs, num_states, num_observations, default_weight], s_o_w_pair_1, ...]
    s_o_weights = normalize_s_o_w(loader("state_observation_weights.txt"))

    return s_weights, s_a_s_weights, s_o_weights, o_actions


def write_result(states):
    file = open("states1.txt", 'w')
    file.write("states\n")
    file.write(str(len(states)) + '\n')
    for state in states:
        file.write('"' + state + '"\n')
    file.close()


def find_observed_states(observation, state_observation):
    """
    given observation, find possible current state
    :param observation: observation
    :param state_observation: state_observation_weights
    :return: possible states
    """
    possible_state = []
    for item in state_observation:
        if item[1] == observation:
            possible_state.append(item)

    return possible_state


def viterbi_algorithm(o_a, s_w, s_a_s_w, s_o_w):
    states, initial_probabilities, obs, acts, transition_matrix, emission_matrix = initialization(o_a, s_w, s_a_s_w,
                                                                                                  s_o_w)

    num_states, num_actions, num_observations = s_a_s_w[0][1], s_a_s_w[0][2], s_o_w[0][2]

    observations = []
    for i in range(1, num_observations + 1):
        observations.append(s_o_w[i][1])

    viterbi_matrix = np.zeros((num_states, len(obs)))
    backward = np.zeros((num_states, len(obs)), dtype=int)

    for s in range(len(states)):
        x = observations.index(obs[0])
        viterbi_matrix[s, 0] = initial_probabilities[s] * emission_matrix[s, x]

    for o in range(1, len(obs)):
        x = observations.index((obs[o]))
        for s in range(len(states)):
            temp_actions = []
            for a in acts:

                act_prob = viterbi_matrix[:, o-1] * transition_matrix[:, a, s]
                max_act_prob = (np.max(act_prob), np.argmax(act_prob))
                temp_actions.append(max_act_prob)

            max_prob = max(temp_actions, key=itemgetter(1))
            arg_prob = max_prob[1]
            max_prob = max_prob[0] * emission_matrix[s, x]
            viterbi_matrix[s, o] = max_prob
            backward[s, o] = arg_prob

    best_path = np.argmax(viterbi_matrix[:, -1])
    best_states = [best_path]

    for o in range(len(obs)-1, 0, -1):
        best_states.insert(0, backward[best_states[0], o])

    result = []
    for state in best_states:
        result.append(states[state])

    print(result)

    return result


def main():
    s_weights, s_a_s_weights, s_o_weights, o_actions = open_file()

    result = viterbi_algorithm(o_actions, s_weights, s_a_s_weights, s_o_weights)

    #states, initial_probabilities, obs, acts, transition_matrix, emission_matrix = initialization(o_actions, s_weights, s_a_s_weights, s_o_weights)

    # print(s_weights_r)
    # print(s_a_s_weights)
    # print(s_o_weights)
    write_result(result)


main()
