import cvxpy as cp
import numpy as np
from scipy.io import loadmat
from imageio.v2 import imread
from PIL import Image
from render import render


def total_variation(arr):
    dx = cp.vec(arr[1:, :-1] - arr[:-1, :-1])
    dy = cp.vec(arr[:-1, 1:] - arr[:-1, :-1])
    D = cp.vstack((dx, dy))
    norm = cp.norm(D, p=1, axis=0)
    return cp.sum(norm)


def inpaint(corrupted, rows, cols, verbose=True):
    result = np.zeros(shape=corrupted.shape)
    for channel in range(3):
        corrupted_channel = corrupted[:, :, channel]
        x = cp.Variable(corrupted_channel.shape)
        objective = cp.Minimize(total_variation(x))
        knowledge = x[rows, cols] == corrupted_channel[rows, cols]
        constraints = [0 <= x, x <= 255, knowledge]
        prob = cp.Problem(objective, constraints)
        prob.solve(solver=cp.ECOS, verbose=verbose)
        result[:, :, channel] = x.value
    return result


target_img = 3


def main():
    mask = loadmat(f'data/A_{target_img}.mat')['matrix']
    rows, cols = np.where(mask == 0)
    corrupted = imread(f'data/corrupted{target_img}.png')
    recovered = inpaint(corrupted, rows, cols)
    # render recovered image
    render(target_img, recovered)


if __name__ == '__main__':
    main()
