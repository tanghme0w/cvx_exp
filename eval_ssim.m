function ssim_total = eval_ssim(img, ref)
%EVAL_SSIM : input matrices of the same size representing color images
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
ssim_r = ssim(img_r,ref_r);
ssim_g = ssim(img_g,ref_g);
ssim_b = ssim(img_b,ref_b);
% calculate SSIM with respect to each channel
ssim_total = (ssim_r+ssim_g+ssim_b)/3;
end

