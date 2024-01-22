import public.little_prince.test_case_1 as tc


def o_a():
    file = open("public/little_prince/test_case_1/observation_actions.txt", 'r')
    input = file.read().split('\n')
    number_of_states = int(input[1])
    observations_actions = input[2:]
    o_a_pairs = []

    for item in observations_actions:
        item = item.replace('"', '')
        item = tuple(item.split())
        if item:
            o_a_pairs.append(item)


def o_w():
    file = open("public/little_prince/test_case_1/state_weights.txt", 'r')
    input = file.read().replace('"', '').split('\n')
    number_of_states = int(input[1].split()[0])
    state_weights = input[2:]
    s_w_pairs = [number_of_states]
    for item in state_weights:
        item = item.split()
        if item:
            item[1] = int(item[1])
            item = tuple(item)
            s_w_pairs.append(item)


def s_a_s_w():
    file = open("public/little_prince/test_case_1/state_action_state_weights.txt", 'r')
    data = file.read().replace('"', '').split('\n')
    info = [int(i) for i in data[1].split()]
    state_action_state_weights = data[2:]
    s_a_s_w_pairs = [info]
    for item in state_action_state_weights:
        item = item.split()
        if item:
            item[-1] = int(item[-1])
            s_a_s_w_pairs.append(tuple(item))

    print(state_action_state_weights[-2])
    print(len(s_a_s_w_pairs))


def s_o_w():
    file = open("public/little_prince/test_case_1/state_observation_weights.txt", 'r')
    data = file.read().replace('"', '').split('\n')
    info = [int(i) for i in data[1].split()]
    state_observation_weights = data[2:]
    s_o_w_pairs = [info]
    for item in state_observation_weights:
        item = item.split()
        if item:
            item[-1] = int(item[-1])
            s_o_w_pairs.append(tuple(item))

    return s_o_w_pairs  # [[num_pairs, num_states, num_observations, _default_weight], s_o_w_pair_1, ...]



def loader(name):
    file = open(name, 'r')
    data = file.read().replace('"', '').split('\n')
    if name != "public/little_prince/test_case_1/observation_actions.txt":
        info = [int(i) for i in data[1].split()]
        items = data[2:]
        pairs = [info]
        for item in items:
            item = item.split()
            if item:
                item[-1] = int(item[-1])
                pairs.append(tuple(item))
        return pairs
    if name == "public/little_prince/test_case_1/observation_actions.txt":
        num_states = int(data[1])
        observations_actions = data[2:]
        o_a_pairs = [num_states]

        for item in observations_actions:
            item = tuple(item.split())
            if item:
                o_a_pairs.append(item)
        return o_a_pairs

o_a = "public/little_prince/test_case_1/observation_actions.txt"
s_w = "public/little_prince/test_case_1/state_weights.txt"
s_a_s = "public/little_prince/test_case_1/state_action_state_weights.txt"
s_o = "public/little_prince/test_case_1/state_observation_weights.txt"

print(loader(s_o))


s_o_w()

"""
given observation action
max(P()
"""


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states)
            for prev_st in states:
                if V[t-1][prev_st]["prob"]*trans_p[prev_st][st] == max_tr_prob:
                    max_prob = max_tr_prob * emit_p[st][obs[t]]
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break

    # Find the state with the maximum probability in the last time step
    max_prob_state = max(V[-1], key=lambda x: V[-1][x]["prob"])

    # Backtrack to reconstruct the best path
    best_path = [max_prob_state]
    for t in range(len(obs) - 1, 0, -1):
        best_path.insert(0, V[t][best_path[0]]["prev"])

    return best_path


#My Example
states = ('Healthy', 'Fever')
observations = ('normal', 'cold', 'dizzy')
start_probability = {'Healthy': 0.6, 'Fever': 0.4}
transition_probability = {'Healthy': {'Healthy': 0.7, 'Fever': 0.3}, 'Fever': {'Healthy': 0.4, 'Fever': 0.6}}
emission_probability = {'Healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1}, 'Fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}}

result = viterbi(observations, states, start_probability, transition_probability, emission_probability)
print(result)

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states)
            for prev_st in states:
                if V[t-1][prev_st]["prob"]*trans_p[prev_st][st] == max_tr_prob:
                    max_prob = max_tr_prob * emit_p[st][obs[t]]
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break

    # Find the state with the maximum probability in the last time step
    max_prob_state = max(V[-1], key=lambda x: V[-1][x]["prob"])

    # Backtrack to reconstruct the best path
    best_path = [max_prob_state]
    for t in range(len(obs) - 1, 0, -1):
        best_path.insert(0, V[t][best_path[0]]["prev"])

    return best_path

def parse_state_weights(file_path):
    state_weights = []

    try:
        with open(file_path, 'r') as file:
            # Skip the first two lines ("state_weights" and metadata)
            file.readline()
            metadata = file.readline().strip().split()
            num_states = int(metadata[0])

            # Read state weights
            for _ in range(num_states):
                line = file.readline().strip()
                if line:
                    parts = line.split()
                    if len(parts) == 2:
                        state, weight = parts
                        state = state.strip('"')
                        state_weights.append(state)
                    else:
                        print(f"Illegal format in line: {line}")

    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return tuple(set(state_weights))  # Convert to a tuple to make it immutable and return only unique states

def parse_observation_actions(file_path):
    observations = []

    try:
        with open(file_path, 'r') as file:
            # Skip the first two lines ("observation_actions" and the number of pairs)
            file.readline()
            file.readline()

            # Read observation-action pairs
            for line in file:
                line = line.strip()
                if line:
                    # Split the line into observation and action
                    parts = line.split()
                    if len(parts) == 1:
                        observation = parts[0].strip('"')
                        observations.append(observation)
                    elif len(parts) == 2:
                        observation = parts[0].strip('"')
                        observations.append(observation)
                    else:
                        print(f"Illegal format in line: {line}")

    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return tuple(set(observations))  # Convert to a tuple to make it immutable and return only unique observations

def parse_normalize_state_weights(file_path):
    state_weights = {}

    try:
        with open(file_path, 'r') as file:
            # Skip the first two lines ("state_weights" and metadata)
            file.readline()
            metadata = file.readline().strip().split()
            num_states = int(metadata[0])

            # Read state weights
            for _ in range(num_states):
                line = file.readline().strip()
                if line:
                    parts = line.split()
                    if len(parts) == 2:
                        state, weight = parts
                        state = state.strip('"')
                        weight = int(weight)
                        state_weights[state] = weight
                    else:
                        print(f"Illegal format in line: {line}")

    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return state_weights

def normalize_weights(state_weights):
    total_weight = sum(state_weights.values())
    normalized_prob = {state: weight / total_weight for state, weight in state_weights.items()}
    return normalized_prob


file_path = "observation_actions.txt"
unique_observations = parse_observation_actions(file_path)

file_path = "state_weights.txt"
states = parse_state_weights(file_path)
print("Unique States:")
print(states)
print("Unique Observations:")
print(unique_observations)

normalize_states = parse_normalize_state_weights(file_path)
start_probability = normalize_weights(normalize_states)
print("State Weights Normalized:")
print(start_probability)


def viterbi_algorithm(hmm, obs_with_actions):
    num_states = len(hmm.states)
    num_actions = len(hmm.actions)
    num_obs = len(obs_with_actions)

    # Step 2: Initialize Variables
    viterbi_table = [[0.0 for _ in range(num_actions)] for _ in range(num_obs)]
    backpointer = [[0 for _ in range(num_actions)] for _ in range(num_obs)]

    # Step 3: Calculate Probabilities
    for t in range(num_obs):
        obs, action = obs_with_actions[t]

        # create the index of obs, and index of action (by mapping the obs str to int index)

        for s in range(num_states):
            #for a in range(num_actions):
            if t == 0:
                viterbi_table[t][s] = hmm.start_prob[s] * hmm.emission_prob[s][obs]
            else:
                max_prob, prev_state = max(
                        (viterbi_table[t - 1][prev_s] * hmm.transition_prob[prev_s][s][a], prev_s)
                        for prev_s in range(num_states)
                )
                viterbi_table[t][s] = max_prob * hmm.emission_prob[s][obs]
                backpointer[t][s] = prev_state

    # Step 4: Traceback and Find Best Path
    best_last_state = max(range(num_states), key=lambda s: viterbi_table[-1][0][s])  # Assuming action 0
    best_path = [best_last_state]  # Assuming action 0
    for t in range(num_obs - 1, 0, -1):
        best_last_state = backpointer[t][0][best_last_state]  # Assuming action 0
        best_path.insert(0, best_last_state)  # Assuming action 0

    # Map state indices to state names
    state_mapping = {0: 'S0', 1: 'S1', 2: 'S2'}

    # Convert state indices to state names in the result_path
    result_path_states = [state_mapping[state] for state in best_path]

    # Step 5: Return Best Path
    return result_path_states


# Example HMM parameters
start_prob = [0.2222222222222222, 0.5555555555555556, 0.2222222222222222]
emission_prob = [[0.57143, 0.14286, 0.28571],
 [0.55556, 0.33333, 0.11111],
 [0.09091, 0.45455, 0.45455]]
transition_prob = [
    [
        [0.5714285714285714, 0.14285714285714285, 0.2857142857142857], [0.5, 0.3333333333333333, 0.16666666666666666],
        [0.5, 0.4, 0.1]],
    [[0.3333333333333333, 0.5, 0.16666666666666666], [0.2857142857142857, 0.42857142857142855, 0.2857142857142857],
     [0.16666666666666666, 0.6666666666666666, 0.16666666666666666]],
    [[0.4166666666666667, 0.16666666666666666, 0.4166666666666667], [0.3333333333333333, 0.4166666666666667, 0.25],
     [0.6, 0.2, 0.2]
     ]
]


class Hmm:
    def _init_(self, start_prob, emission_prob, transition_prob, states, actions):
        self.start_prob = start_prob
        self.emission_prob = emission_prob
        self.transition_prob = transition_prob
        self.states = states
        self.actions = actions


states = ['S0', 'S1', 'S2']
actions = ['Forward', 'Backward', 'Turnaround']

# Create an HMM object
hmm_model = Hmm(start_prob, emission_prob, transition_prob, states, actions)

# Sequence of observations with actions
observations_with_actions = [(0, 'Forward'), (1, 'Forward'), (2, 'Backward'), (0, None)]

# Call the Viterbi algorithm
result_path = viterbi_algorithm(hmm_model, observations_with_actions)

# Display the result
print("Most likely state sequence:", result_path)