import matplotlib.pyplot as plt
import numpy as np


target_img = 1


recovered_img = np.load(f'data/recovered{target_img}.npy')
print(recovered_img)

plt.imshow(recovered_img.astype(np.uint8))
plt.axis('off')
plt.savefig(f'data/recovered{target_img}')
plt.show()
