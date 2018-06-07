import math


def data_reader(path):
    """
    This function read the data file
    :param path: path to the data
    :return read data and convert it to the list
    """
    file = open(path, "r")
    data = file.readlines()[4:]
    file.close()
    return data


def create_graph_out_bound(data):
    """
    This function create graph where node and all nodes to which it refers are presented
    :param data: data to create graph
    :return out bound graph
    """
    out_bound = {}
    for file_index in range(len(data)):
        fromNodeID = data[file_index].split()[0]
        toNodeID = data[file_index].split()[1]

        if fromNodeID in out_bound:
            out_bound[fromNodeID].append(toNodeID)
        else:
            out_bound[fromNodeID] = [toNodeID]
    return out_bound


def create_graph_in_bound(data):
    """
    This function create graph where node and all nodes which are refers to it are presented
    :param data: data to create graph
    :return in bound graph
    """
    in_bound = {}
    for file_index in range(len(data)):
        fromNodeID = data[file_index].split()[0]
        toNodeID = data[file_index].split()[1]
        if toNodeID in in_bound:
            in_bound[toNodeID].append(fromNodeID)
        else:
            in_bound[toNodeID] = [fromNodeID]

    return in_bound


def euclidean_distance(vector1, vector2):
    """
    This function calculate the euclidean distance between two vectors
    :param vector1: first vector
    :param vector2: second vector
    :return euclidean distance between vectors
    """
    e_dist = [(v1 - v2) ** 2 for v1, v2 in zip(vector1, vector2)]
    e_dist = math.sqrt(sum(e_dist))
    return e_dist


def compute_ranks(graph_out, graph_in, beta, epsilon):
    """
    This function compute ranks for all nodes
    :param graph_out: graph where node and all nodes to which it refers are presented
    :param graph_in: graph where node and all nodes which are refers to it are presented
    :param beta: relative weight parameter
    :param epsilon: converges parameter
    :return euclidean distance between vectors
    """
    ranks = {}
    n_pages = len(graph_out)
    for page in graph_out:
        ranks[page] = 1.0 / n_pages

    old_ranks = ranks

    e_dist_list = []
    iteration = 0
    converges = False
    while not converges:
        updated_ranks = {}
        for page in graph_out:
            updated_rank = (1 - beta) / n_pages
            if page in graph_in.keys():
                for i in graph_in[page]:
                    updated_rank = updated_rank + beta * ranks[i] / len(graph_out[i])
                updated_ranks[page] = updated_rank
            else:
                updated_ranks[page] = updated_rank
        ranks = updated_ranks

        e_dist = euclidean_distance(old_ranks.values(), ranks.values())
        print("Iteration: " + str(iteration) + " loss: " + str(e_dist))

        e_dist_list.append(e_dist)
        old_ranks = ranks
        iteration += 1
        if len(e_dist_list) > 2 and abs(e_dist_list[-1] - e_dist_list[-2]) < epsilon:
            converges = True
    return sorted(ranks.items(), key=lambda x: x[1], reverse=True)


def main():
    data = data_reader("web-Google.txt")
    graph_out = create_graph_out_bound(data)
    graph_in = create_graph_in_bound(data)
    print(compute_ranks(graph_out, graph_in, beta=0.8, epsilon=0.0001))


if __name__ == "__main__":
    main()
