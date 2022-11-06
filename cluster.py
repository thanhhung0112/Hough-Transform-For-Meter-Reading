import numpy as np
import copy

def compute_reliable_level(value, X):
    temp = copy.deepcopy(X)
    result = []
    for index, item in enumerate(temp):
        temp[index] = (temp[index].astype(np.float64) - np.mean(item.astype(np.float64))) / 2
        gaussian = np.exp((-1/4) * (temp[index])**2)
        compare = gaussian-0.5
        compare = np.prod(np.where(compare<0.0))
        result.append(compare)
    return result

def split_data(X):
    result = [copy.deepcopy(X)]
    if type(X) != np.ndarray:
        X = np.array([X])
    if X.shape[0] > 1:
        X = np.array(X)
        mean_X = np.mean(X)
        X1 = X[X <= mean_X]
        X2 = X[X > mean_X]
        result = [X1, X2]
    return result

def split_temp(X):
    result = []
    for item in X:
        result.extend(split_data(item))
    return result

def determine_cluster(X):
    cluster = []
    temp = [X]

    while True:
        result = np.array(compute_reliable_level(temp, temp))
        index_cluster = np.where(result > 0)[0]
        if len(index_cluster) > 0:
            temp = np.array(temp, dtype=object)
            copy_temp = copy.deepcopy(temp)
            cluster.extend(copy_temp[index_cluster])
            temp = np.delete(temp, index_cluster, axis=0)

        if len(temp) > 0:
            temp = split_temp(temp)
        else:
            break

    for i, item in enumerate(cluster):
        cluster[i] = np.mean(cluster[i])

    return np.array(cluster)

X1 = np.random.normal(5, 0.5, (100,))
X2 = np.random.normal(20, 0.5, (100,))
X3 = np.random.normal(40, 0.5, (100,))
X = np.hstack((X1, X2, X3))

cluster = determine_cluster(X)
print(cluster)
