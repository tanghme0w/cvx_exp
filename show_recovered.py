import matplotlib.pyplot as plt
import numpy as np

recovered_img = np.load('data/recovered2.npy')
print(recovered_img)

plt.imshow(recovered_img.astype(np.uint8))
plt.axis('off')
plt.savefig('recovered2')
plt.show()
