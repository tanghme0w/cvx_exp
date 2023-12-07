function [psnr_total,psnr_mask] = eval_psnr(img, ref, mask)
%EVAL_PSNR : input two matrices of the same size representing color images, 
%            and a third matrix of the same size consisting of 0/1-valued
%            entries only
if isinteger(img)
    img = double(img)/255;
end
if isinteger(ref)
    ref = double(ref)/255;
end
% standardize both images
img_r = img(:,:,1);
img_g = img(:,:,2);
img_b = img(:,:,3);
ref_r = ref(:,:,1);
ref_g = ref(:,:,2);
ref_b = ref(:,:,3);
% calculate PSNR with respect to each channel
psnr_r = psnr(img_r, ref_r);
psnr_g = psnr(img_g, ref_g);
psnr_b = psnr(img_b, ref_b);
psnr_total = (psnr_r + psnr_g + psnr_b) / 3;
% calculate PSNR with respect to each channel, on masked (corrupted)
% pixels only
psnr_r_mask = psnr(img_r(mask == 1), ref_r(mask == 1));
psnr_g_mask = psnr(img_g(mask == 1), ref_g(mask == 1));
psnr_b_mask = psnr(img_b(mask == 1), ref_b(mask == 1));
psnr_mask = (psnr_r_mask + psnr_g_mask + psnr_b_mask) / 3;
end

