import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
from imageio.v2 import imread
from inpaint import inpaint, total_variation


def crop_img(img_file, mask_file, area_coordinates):
    image = imread(img_file)
    mask = loadmat(mask_file)['matrix']
    x1, y1, x2, y2 = area_coordinates
    assert image.shape[0] > x2 > x1 >= 0 and image.shape[1] > y2 > y1 >= 0
    return image[x1:x2, y1:y2, :], mask[x1:x2, y1:y2]


corrupted, mask = crop_img('data/corrupted3.png', 'data/A_3.mat', [0, 0, 511, 511])
plt.imshow(corrupted)
# r, c = np.where(mask == 1)
# plt.scatter(c, r)
plt.show()

rows, cols = np.where(mask == 0)
recovered = inpaint(corrupted, rows, cols)
plt.imshow(recovered.astype(np.uint8))
plt.axis('off')
plt.savefig(f'data/recovered3_partial')
plt.show()
np.save(f'data/recovered3_partial', recovered)