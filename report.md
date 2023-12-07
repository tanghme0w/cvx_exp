#  Convex Optimization for Image Recovery: A Weighted Total Variance Approach

​								Haomiao Tang 	2023214257

## Abstract

In this paper I propose an Edge-Sensitive Total Variation (ES-TV) objective function for convex-optimization-based image recovery task. In addition to the standard total variance objective function, larger weights are assigned to the pixels at the edge of the mask. Experiments show that the proposed method outperforms the provided baselines. The effect of hyper-parameters are also discussed in this paper.

## Mathematical Modelling

Given a picture $C$ with corrupted pixels, and a mask indicating the position of corrupted pixels, the task of image recovery is to alter the corrupted pixels so that the picture becomes as close to the original picture as possible. Solving the problem via Convex Optimization solver requires finding a convex objective function as well as convex constraints. One of the most commonly used objective functions is the Total Variance (TV) function.

For a gray-scale picture with 512 $\times$ 512 pixels, the convex optimization problem under TV objective can be formulated as follows:
$$
\begin{align}
&\textbf{min}\quad\sum ^{511}_{j=1}\sum ^{511}_{i=1}\left( \left| C\left[ i,j+1\right] -C\left[ i,j\right] \right| +\left| C\left[ i+1,j\right] -C\left[ i,j\right] \right| \right)\\
&\textbf{s.t}\quad 1 \leq C[i, j] \leq 255, \quad C[i,j] = C_0[i,j] \quad \text{where} \quad mask[i, j] =0
\end{align}
$$
In which $C[i, j]$ denotes the grayscale valuse of the pixel on the $i$th row and $j$th column. We only maximize over pixels in $C$ that are corrupted. Partial dimension constraint is obviously a convex constraint, bucket constraint is also obviously a convex constraint. Furthermore, the total variation objective function is a convex function because it is a sum of absolute values of linear functions, and both the absolute value function and the sum of convex functions are convex. Summarizing, this problem is a convex optimization problem. 

In this expression we use l1-norm to express TV objective. In fact we can use arbitrary norm. This will not affect the convexity of the problem as long as $p \geq 1$. 

The standard TV objective function is not powerful enough. We notice that the corrupted pixels on the edges of the mask plays a more important role than other corrupted pixels, because they directly interact with uncorrupted parts of the picture. So we add a weight to the terms in the objective functions to raise the importance of edge pixels.
$$
\begin{align}
&\textbf{min}\quad\sum ^{511}_{j=1}\sum ^{511}_{i=1}\left( U(i, j) \cdot \left|  C\left[ i,j+1\right] -C\left[ i,j\right] \right| +U(i, j) \cdot \left| C\left[ i+1,j\right] -C\left[ i,j\right] \right| \right)\\
&\textbf{s.t}\quad 1 \leq C[i, j] \leq 255, \quad C[i,j] = C_0[i,j] \quad \text{where} \quad mask[i, j] =0
\end{align}
$$
In which $U[i, j]=M$ when i,j is the edge pixel of the mask.  $U[i, j]=1$ Otherwise. $M$ is a modifiable hyper-parameter.

# Experiment Results

In this task we use ECOS solver. The results are as follows. The highlighted data are the highest scores.

### Image 1

**baseline:**

psnr_total: 21.838873958709247, psnr_mask: 7.695694347392071, ssim_total: 0.9443044766596227

**Proposed Method, M=1, p=1**

psnr_total: 21.84383847721836, psnr_mask: 7.6984111712076455, ssim_total: 0.9442748539306033

**Proposed Method, M=1, p=2**

psnr_total: **21.901033372190955**, psnr_mask: **7.763178280257319**, ssim_total: **0.9450379209014498**

**Proposed Method, M=2, p=1**

psnr_total: 21.753273977351654, psnr_mask: 7.589214391310345, ssim_total: 0.94457236127409

### Image 2

**Baseline:**

psnr_total: 30.332512124311588, psnr_mask: 19.504580623808703, ssim_total: 0.9626589942548426

**Proposed Method, M=2, p=1**

psnr_total: **30.83546730899796**, psnr_mask: **19.99743259307193**, ssim_total: **0.9662111693779853**

### Image 3

**Baseline:**

psnr_total: 26.35512224141166, psnr_mask: 17.536135457658773, ssim_total: 0.9286720050758582

**Proposed Method, M=2, p=1:**

psnr_total: **27.25986393742124**, psnr_mask: **18.447892891810785**, ssim_total: **0.9391158854213759**

