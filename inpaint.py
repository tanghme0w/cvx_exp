import matplotlib.pyplot as plt
import cvxpy as cp
import numpy as np
from scipy.io import loadmat
from imageio.v2 import imread


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


target_img = 2


def main():
    mask = loadmat(f'data/A_{target_img}.mat')['matrix']
    rows, cols = np.where(mask == 0)
    corrupted = imread(f'data/corrupted{target_img}.png')
    recovered = inpaint(corrupted, rows, cols)
    # plot recovered figure
    plt.imshow(recovered.astype(np.uint8))
    plt.axis('off')
    plt.savefig(f'data/recovered{target_img}')
    plt.show()
    np.save(f'data/recovered{target_img}', recovered)


if __name__ == '__main__':
    main()
