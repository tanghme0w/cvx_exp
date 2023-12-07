import cvxpy as cp
import numpy as np
from scipy.io import loadmat
from imageio.v2 import imread
from render import render


def weighted_total_variation(arr, mask, M=1):
    dx = cp.vec(arr[1:, :-1] - arr[:-1, :-1])
    dy = cp.vec(arr[:-1, 1:] - arr[:-1, :-1])
    mask = mask.astype(np.int8)  # must change mask datatype or else subtraction operations would underflow
    w_x = cp.vec(cp.abs(mask[1:, :-1] - mask[:-1, :-1]))  # locate vertical edges
    w_y = cp.vec(cp.abs(mask[:-1, 1:] - mask[:-1, :-1]))  # locate horizontal edges
    assert M > 0
    w_x = cp.multiply(w_x, M - 1) + 1
    w_y = cp.multiply(w_y, M - 1) + 1
    weighted_dx = cp.multiply(dx, w_x)
    weighted_dy = cp.multiply(dy, w_y)
    D = cp.vstack((weighted_dx, weighted_dy))
    norm = cp.norm(D, p=1, axis=0)
    return cp.sum(norm)


def inpaint(corrupted, rows, cols, mask, verbose=True):
    result = np.zeros(shape=corrupted.shape)
    for channel in range(3):
        corrupted_channel = corrupted[:, :, channel]
        x = cp.Variable(corrupted_channel.shape)
        objective = cp.Minimize(weighted_total_variation(x, mask))
        knowledge = x[rows, cols] == corrupted_channel[rows, cols]
        constraints = [0 <= x, x <= 255, knowledge]
        prob = cp.Problem(objective, constraints)
        prob.solve(solver=cp.SCS, verbose=verbose)
        result[:, :, channel] = x.value
    return result


target_img = 1


def main():
    mask = loadmat(f'data/A_{target_img}.mat')['matrix']
    rows, cols = np.where(mask == 0)
    corrupted = imread(f'data/corrupted{target_img}.png')
    recovered = inpaint(corrupted, rows, cols, mask)
    # render recovered image
    render(target_img, recovered)


if __name__ == '__main__':
    main()
