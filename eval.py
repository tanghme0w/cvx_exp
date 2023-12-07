import matlab.engine
from PIL import Image
from scipy.io import loadmat
import numpy as np


def eval_psnr(img_file, ref_file, mask_file):
    img = np.array(Image.open(img_file)).astype(np.uint8)
    ref = np.array(Image.open(ref_file)).astype(np.uint8)
    mask = loadmat(mask_file)['matrix']
    eng = matlab.engine.start_matlab()
    eng.cd(r'.', nargout=0)
    return eng.eval_psnr(img, ref, mask, nargout=2)


def eval_ssim(img_file, ref_file):
    img = np.array(Image.open(img_file)).astype(np.uint8)
    ref = np.array(Image.open(ref_file)).astype(np.uint8)
    eng = matlab.engine.start_matlab()
    eng.cd(r'.', nargout=0)
    return eng.eval_ssim(img, ref, nargout=1)


target_img = 1
p_total, p_mask = eval_psnr(f'data/recovered{target_img}.png', f'data/figure{target_img}.png', f'data/A_{target_img}')
ssim_total = eval_ssim(f'data/recovered{target_img}.png', f'data/figure{target_img}.png')
print(f'psnr_total: {p_total}, psnr_mask: {p_mask}, ssim_total: {ssim_total}')
