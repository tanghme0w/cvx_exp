from PIL import Image
import numpy as np


target_img = 1


recovered_img = np.load(f'data/recovered{target_img}.npy')
print(recovered_img)

image = Image.fromarray(recovered_img.astype(np.uint8))
image.save(f'data/recovered{target_img}.png')
