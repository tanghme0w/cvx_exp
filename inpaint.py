import matplotlib.pyplot as plt
import cvxpy as cp
import numpy as np
from scipy.io import loadmat
from imageio import imread


def total_variation(arr):
    dx = cp.vec(arr[1:, :-1] - arr[:-1, :-1])
    dy = cp.vec(arr[:-1, 1:] - arr[:-1, :-1])
    D = cp.vstack((dx, dy))
    norm = cp.norm(D, p=1, axis=0)
    return cp.sum(norm)


def inpaint(corrupted, rows, cols, verbose=False):
    result = np.zeros(shape=corrupted.shape)
    for channel in range(3):
        corrupted_channel = corrupted[:, :, channel]
        x = cp.Variable(corrupted_channel.shape)
        objective = cp.Minimize(total_variation(x))
        knowledge = x[rows, cols] == corrupted_channel[rows, cols]
        constraints = [0 <= x, x <= 255, knowledge]
        prob = cp.Problem(objective, constraints)
        prob.solve(solver=cp.SCS, verbose=verbose)
        result[:, :, channel] = x.value
    return result


def main():
    mask = loadmat('data/A_1.mat')['matrix']
    rows, cols = np.where(mask == 0)
    corrupted = imread('data/corrupted1.png')
    recovered = inpaint(corrupted, rows, cols)
    # plot recovered figure
    plt.imshow(recovered)
    plt.savefig('data/recovered1')
    np.save('data/recovered1.mat', recovered)


if __name__ == '__main__':
    main()
