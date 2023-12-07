from PIL import Image
import numpy as np


def render(target_img, recovered_matrix=None):
    if recovered_matrix:
        recovered_img = Image.fromarray(recovered_matrix.astype(np.uint8))
        recovered_img.save(f'data/recovered{target_img}.png')
        np.save(f'data/recovered{target_img}', recovered_matrix)
    else:
        recovered_img = Image.fromarray(np.load(f'data/recovered{target_img}.npy').astype(np.uint8))
        recovered_img.save(f'data/recovered{target_img}.png')


render(1)
